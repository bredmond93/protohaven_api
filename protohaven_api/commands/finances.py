"""Commands related to financial information and alerting"""
import argparse
import datetime
import logging
import pickle
import random
import re
import string
import sys
from collections import defaultdict
from functools import lru_cache

from dateutil import parser as dateparser

from protohaven_api.commands.decorator import arg, command, print_yaml
from protohaven_api.comms_templates import Msg
from protohaven_api.config import (  # pylint: disable=import-error
    exec_details_footer,
    tz,
    tznow,
)
from protohaven_api.integrations import neon, sales  # pylint: disable=import-error
from protohaven_api.rbac import Role

log = logging.getLogger("cli.finances")

# The "start date" for members' memberships which haven't yet been
# activated via logging in at the front desk
PLACEHOLDER_START_DATE = dateparser.parse("9001-01-01")


class Commands:
    """Commands for managing classes in Airtable and Neon"""

    @command()
    def transaction_alerts(self, _):  # pylint: disable=too-many-locals
        """Send alerts about recent/unresolved transaction issues"""
        log.info("Fetching customer mapping")
        cust_map = sales.get_customer_name_map()
        log.info(f"Fetched {len(cust_map)} customers")
        log.info("Fetching subscription plans")
        sub_plan_map = sales.get_subscription_plan_map()
        log.info(f"Fetched {len(sub_plan_map)} subscription plans")
        assert len(sub_plan_map) > 0  # We should at least have some plans
        now = tznow()
        log.info("Fetching subscriptions")

        unpaid = []
        untaxed = []
        n = 0
        for sub in sales.get_subscriptions()["subscriptions"]:
            if sub["status"] != "ACTIVE":
                continue
            n += 1

            sub_id = sub["id"]
            url = f"https://squareup.com/dashboard/subscriptions-list/{sub_id}"
            log.debug(f"Subscription {sub_id}: {sub}")
            plan, price = sub_plan_map.get(
                sub["plan_variation_id"], (sub["plan_variation_id"], 0)
            )
            if price == 0:
                log.warning(
                    f"Subscription plan not resolved: {sub['plan_variation_id']}"
                )
                continue
            tax_pct = sales.subscription_tax_pct(sub, price)

            log.debug(f"{plan} ${price/100} tax={tax_pct}%")
            cust = cust_map.get(sub["customer_id"], sub["customer_id"])

            if tax_pct < 6.9 or tax_pct > 7.1:
                untaxed.append(f"- {cust} - {plan} - {tax_pct}% tax ([link]({url}))")
                log.info(untaxed[-1])

            charged_through = dateparser.parse(sub["charged_through_date"]).astimezone(
                tz
            )
            if charged_through + datetime.timedelta(days=1) < now:
                unpaid.append(
                    f"- {cust} - {plan} - charged through {charged_through} ([link]({url}))"
                )
                log.info(unpaid[-1])

        log.info(
            f"Processed {n} active subscriptions - {len(unpaid)} unpaid, {len(untaxed)} untaxed"
        )
        if len(unpaid) > 0 or len(untaxed) > 0:
            print_yaml(
                Msg.tmpl(
                    "square_validation_action_needed",
                    unpaid=unpaid,
                    untaxed=untaxed,
                    footer=exec_details_footer(),
                    target="#finance-automation",
                )
            )
        log.info("Done")

    def _validate_role_membership(self, details, role):
        log.debug(f"Validate role membership: {role['name']}")
        results = []
        roles = details.get("roles", [])
        if role["name"] not in roles:
            results.append(f"Needs role {role['name']}, has {roles}")
            log.info(f"Missing role {role['name']}: {details}")
        return results

    def _validate_addl_family_membership(self, details):
        log.debug("Validate additional family membership")
        results = []
        if details["household_paying_member_count"] <= 0:
            results.append(
                f"Missing required non-additional paid member in household #{details['hid']}"
            )
            log.info(f"Missing paid family member: {details}")
        return results

    def _validate_employer_membership(self, details):
        log.debug("Validate employer membership")
        results = []
        if details["company_member_count"] < 2:
            results.append(f"Missing required 2+ members in company #{details['cid']}")
            log.info(f"Missing company members: {details}")
        return results

    def _validate_amp_membership(self, details):
        log.debug("Validate AMP membership")
        results = []
        if not details.get("amp"):
            results.append("Income based rate field not set for AMP membership")
        # We may wish to enable this later, once we have the time to request it of all AMP members
        # if not details.get('income_proof'):
        #    results.append(f"Proof of income not provided for AMP membership")
        if details.get("amp"):
            term_type = re.search(r"(ELI|VLI|LI)", details["term"])
            ibr = details["amp"]
            if term_type is not None:
                ibr_match = {
                    "LI": "Low Income",
                    "VLI": "Very Low Income",
                    "ELI": "Extremely Low Income",
                }.get(term_type[1])
                if ibr_match not in ibr:
                    results.append(
                        f"Mismatch between Income based rate ({ibr}) "
                        f"and membership type {term_type[1]}"
                    )
                    log.info(f"AMP mismatch: {details}")
        return results

    def _suggest_membership(  # pylint: disable=too-many-return-statements
        self, details, num_household, num_addl_household, num_company
    ):
        """Look at role bits, AMP information, and company association to see whether
         the 'best' membership fit is applied.

        Zero-cost memberships matching the highest role are prioritized, followed by
        Company, family, amp, and finally general memberships.
        """
        if details.get("roles"):
            if Role.STAFF["name"] in details["roles"]:
                return ["Staff"]
            if Role.BOARD_MEMBER["name"] in details["roles"]:
                return ["Board Member"]
            if Role.SHOP_TECH_LEAD["name"] in details["roles"]:
                return ["Shop Tech Lead"]
            if Role.SHOP_TECH["name"] in details["roles"]:
                return ["Shop Tech"]
            if (
                Role.INSTRUCTOR["name"] in details["roles"]
                or Role.ONBOARDING["name"] in details["roles"]
            ):
                return ["Instructor"]
        if num_company > 0:
            return ["Non-Profit Membership", "Company Membership"]
        if num_household > 1 and (num_household - num_addl_household) > 0:
            return ["Additional Family Membership"]
        if details.get("amp"):
            return details["amp"]
        return ["General"]

    @command(
        arg(
            "--write_cache",
            help="write intermediate data to a cache file",
            type=str,
        ),
        arg("--read_cache", help="run off pickle cache file", type=str),
        arg(
            "--member_ids",
            help="Space-separated list of Neon IDs to validate",
            type=str,
        ),
    )
    def validate_memberships(self, args):
        """Loops through all accounts and verifies that memberships are correctly set"""
        if args.member_ids is not None:
            args.member_ids = [m.strip() for m in args.member_ids.split(",")]
            log.warning(f"Filtering to member IDs: {args.member_ids}")
        problems = self._validate_memberships_internal(
            args.write_cache, args.read_cache, args.member_ids
        )
        if len(problems) > 0:
            print_yaml(
                Msg.tmpl(
                    "membership_validation_problems",
                    problems=problems,
                    target="#membership-automation",
                )
            )
        log.info(f"Done ({len(problems)} validation problems found)")

    def _validate_memberships_internal(
        self, write_cache=None, read_cache=None, member_ids=None
    ):  # pylint: disable=too-many-locals,too-many-branches,too-many-statements
        """Implementation of validate_memberships, callable internally"""
        results = []

        household_paying_member_count = defaultdict(int)
        household_num_addl_members = defaultdict(int)
        company_member_count = defaultdict(int)
        member_data = {}

        if read_cache:
            with open(read_cache, "rb") as f:
                (
                    member_data,
                    household_paying_member_count,
                    household_num_addl_members,
                    company_member_count,
                ) = pickle.load(f)
        else:
            # We search for NOT a bogus email to get all members, then collect
            # data before analysis in order to count paying household & company members
            log.info("Collecting member details")
            n = 0
            for mem in neon.search_member(
                "noreply@protohaven.org", operator="NOT_EQUAL"
            ):
                if n % 10 == 0:
                    sys.stderr.write(".")
                    sys.stderr.flush()
                if mem["Account Current Membership Status"].lower() != "active":
                    continue
                aid = mem["Account ID"]
                if member_ids is not None and aid not in member_ids:
                    continue
                hid = mem["Household ID"]
                level = mem["Membership Level"]
                acct = neon.fetch_account(mem["Account ID"])
                if (acct.get("companyAccount") or {}).get("accountId"):
                    continue  # Don't collect companies

                active_memberships = []
                now = tznow().replace(hour=0, minute=0, second=0, microsecond=0)
                has_fee = False
                for ms in neon.fetch_memberships(mem["Account ID"]):
                    start = (
                        dateparser.parse(ms.get("termStartDate")).astimezone(tz)
                        if ms.get("termEndDate")
                        else None
                    )
                    end = (
                        dateparser.parse(ms.get("termEndDate")).astimezone(tz)
                        if ms.get("termEndDate")
                        else None
                    )
                    if not end or end >= now:
                        has_fee = has_fee or ms["fee"] != 0
                        active_memberships.append(
                            {
                                "fee": ms["fee"],
                                "renew": ms["autoRenewal"],
                                "level": ms["membershipLevel"]["name"],
                                "term": ms["membershipTerm"]["name"],
                                "status": ms["status"],
                                "start_date": start,
                                "end_date": end,
                            }
                        )

                details = {
                    "aid": aid,
                    "hid": hid,
                    "name": f"{mem['First Name']} {mem['Last Name']}",
                    "cid": mem["Company ID"],
                    "level": level,
                    "term": mem["Membership Term"],
                    "active_memberships": active_memberships,
                }
                for acf in acct is not None and (
                    acct.get("individualAccount") or {}
                ).get("accountCustomFields", []):
                    if acf["name"] == "Zero-Cost Membership OK Until Date":
                        details["zero_cost_ok_until"] = dateparser.parse(
                            acf["value"]
                        ).astimezone(tz)
                    if acf["name"] == "Income Based Rate":
                        details["amp"] = acf["optionValues"][0]["name"]
                    elif acf["name"] == "Proof of Income":
                        details["income_proof"] = acf
                    elif acf.get("company"):
                        details["company"] = acf
                    elif acf["name"] == "API server role":
                        details["roles"] = [ov["name"] for ov in acf["optionValues"]]
                member_data[aid] = details
                if "Additional" in level:
                    household_num_addl_members[hid] += 1
                elif has_fee:
                    household_paying_member_count[hid] += 1
                company_member_count[mem["Company ID"]] += 1
                n += 1
            sys.stderr.write("\n")
            if write_cache:
                with open(write_cache, "wb") as f:
                    pickle.dump(
                        (
                            member_data,
                            dict(household_paying_member_count),
                            dict(household_num_addl_members),
                            dict(company_member_count),
                        ),
                        f,
                    )

        log.info(
            f"Loaded details of {len(member_data)} active members, "
            f"{len(household_paying_member_count)} households, "
            f"{len(company_member_count)} companies"
        )

        log.info("Validating member details")

        for aid, details in member_data.items():
            if member_ids is not None and aid not in member_ids:
                continue

            # suggested = self._suggest_membership(details,
            #                                     household_member_count.get(details['hid'], 0),
            #                                     household_num_addl_members.get(details['hid'], 0),
            #                                     company_member_count.get(details['cid'], 0))
            # if level not in suggested:
            #     result.append(f"has level {level}, suggest {suggested}")
            details[
                "household_paying_member_count"
            ] = household_paying_member_count.get(details["hid"], 0)
            details["household_num_addl_members"] = household_num_addl_members.get(
                details["hid"], 0
            )
            details["company_member_count"] = company_member_count.get(
                details["cid"], 0
            )
            result = self._validate_membership_singleton(details)
            results += [
                f"{details['name']}: {r} - "
                f"https://protohaven.app.neoncrm.com/admin/accounts/{details['aid']}"
                for r in result
            ]
        return results

    def _validate_membership_singleton(
        self, details, now=None
    ):  # pylint: disable=too-many-branches
        """Validate membership of a single member"""
        level = details["level"].strip()
        result = []
        if now is None:
            now = tznow()
        # Filter out future and unsuccessful membership registrations

        num = 0
        for am in details["active_memberships"]:
            if (
                am.get("start_date", now) > now
                or am.get("status", "SUCCEEDED") != "SUCCEEDED"
            ):
                continue
            num += 1

            if am["fee"] <= 0 and am["level"] not in (
                "Shop Tech",
                "Board Member",
                "Staff",
            ):
                if (
                    details.get("zero_cost_ok_until") is None
                    or details["zero_cost_ok_until"] < tznow()
                ):
                    result.append(f"Abnormal zero-cost membership {am['level']}")
                    log.info(f"Abnormal zero-cost: {details} - active membership {am}")
            if am.get("end_date") is None:
                result.append(
                    f"Membership {am.get('level')} with no end date (infinite duration)"
                )
                log.info(f"Infinite duration: {details} - active membership {am}")

        if num > 1:
            result.append(
                f"Multiple active memberships: {len(details['active_memberships'])} total"
            )
            log.info(f"Multiple active memberships: {details}")

        if level in (
            "General Membership",
            "Weekend Membership",
            "Weeknight Membership",
            "Founding Member",
            "Primary Family Membership",
            "Youth Program",
        ):
            return result  # Ignore remaining validations

        if "AMP" in level:
            result += self._validate_amp_membership(details)
        elif level == "Shop Tech":
            result += self._validate_role_membership(details, Role.SHOP_TECH)
        elif level == "Instructor":
            result += self._validate_role_membership(details, Role.INSTRUCTOR)
        elif level in "Board Member":
            result += self._validate_role_membership(details, Role.BOARD_MEMBER)
        elif level == "Staff":
            result += self._validate_role_membership(details, Role.STAFF)
        elif level == "Additional Family Membership":
            result += self._validate_addl_family_membership(details)
        elif level in (
            "Corporate Membership",
            "Company Membership",
            "Non-Profit Membership",
        ):
            result += self._validate_employer_membership(details)
        else:
            result += [f"Unhandled membership: '{level}'"]
        return result

    def _generate_coupon_id(self, n=8):
        """https://stackoverflow.com/a/2257449"""
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=n))

    @lru_cache(maxsize=1)
    def _get_sample_classes(self, coupon_amount):
        """Fetch sample classes within the coupon amount for advertising in the welcome email"""
        sample_classes = []
        for e in neon.fetch_published_upcoming_events(back_days=-1):
            ok, num_remaining = self._event_is_suggestible(e["id"], coupon_amount)
            if not ok:
                continue
            d = dateparser.parse(e["startDate"] + " " + e["startTime"]).astimezone(tz)
            d = d.strftime("%A %b %-d, %-I%p")
            s = f"{d}: {e['name']}"
            s += f", https://protohaven.org/e/{e['id']}"
            if num_remaining < 2:
                s += f" ({num_remaining} seat{'s' if num_remaining != 1 else ''} left!)"
            sample_classes.append(s)
            log.info(sample_classes[-1])
            if len(sample_classes) >= 3:
                break
        return sample_classes

    def _init_membership(  # pylint: disable=too-many-arguments
        self, account_id, fname, coupon_amount, apply=True, target=None, _id=None
    ):
        """
        This method initializes a membership by setting a start date,
        generating a coupon if applicable, and updating the automation run status.
        """
        log.info(f"Setting #{account_id} start date to {PLACEHOLDER_START_DATE}")

        def _ok(rep, action):
            if rep.status_code != 200:
                log.error(f"Error {rep.status_code} {action}: {rep.content}")
                return False
            return True

        if apply and not _ok(
            neon.set_membership_start_date(account_id, PLACEHOLDER_START_DATE),
            "setting start date",
        ):
            return None

        cid = None
        if coupon_amount > 0:
            cid = self._generate_coupon_id()
            if apply and not _ok(
                neon.create_coupon_code(cid, coupon_amount), "generating coupon"
            ):
                return None

        if apply and not _ok(
            neon.update_account_automation_run_status(account_id, "deferred"),
            "logging automation run",
        ):
            return None

        if cid:
            return Msg.tmpl(
                "init_membership",
                fname=fname,
                coupon_amount=coupon_amount,
                coupon_code=cid,
                sample_classes=self._get_sample_classes(coupon_amount),
                target=target,
                id=_id,
            )

    def _event_is_suggestible(self, event_id, max_price):
        """Return True if the event with `event_id` has open seats within $`max_price`"""
        for t in neon.fetch_tickets(event_id):
            if (
                t["name"] == "Single Registration"
                and t["fee"] > 0
                and t["fee"] <= max_price
                and t["numberRemaining"] > 0
            ):
                return True, t["numberRemaining"]
        return False, 0

    @command(
        arg(
            "--apply",
            help="When true, actually defer membership start date",
            action=argparse.BooleanOptionalAction,
            default=False,
        ),
        arg(
            "--coupon_amount",
            help="Create a copon with this price and generate comms about it",
            type=int,
            default=102,
        ),
        arg(
            "--created_after",
            help="Only apply to Neon accounts created after YYYY-MM-DD",
            type=str,
            required=True,
        ),
        arg(
            "--filter",
            help="CSV of Neon IDs to restrict processing",
            type=str,
            default="",
        ),
    )
    def init_new_memberships(self, args):
        """Perform initialization steps for new members: deferring membership until first
        sign-in and creation of a coupon for their first class.

        See proposal doc:
        https://docs.google.com/document/d/1O8qsvyWyVF7qY0cBQTNUcT60DdfMaLGg8FUDQdciivM/edit
        """
        if args.filter:
            args.filter = {a.strip() for a in args.filter.split(",")}
            log.info(f"Filtering to {args.filter}")

        log.info(
            "Looping through new members to defer their start date and provide coupons"
        )
        result = []
        for m in neon.get_new_members_needing_setup(
            dateparser.parse(args.created_after), extra_fields=["Email 1"]
        ):
            aid = m["Account ID"]
            if args.filter and aid not in args.filter:
                log.debug(f"Skipping {aid}: not in filter")
                continue
            result.append(
                self._init_membership(
                    m["Account ID"],
                    m["First Name"],
                    args.coupon_amount,
                    apply=args.apply,
                    target=m["Email 1"],
                    _id=f"init member {m['Account ID']}",
                )
            )
        result = [r for r in result if r is not None]
        if len(result) > 0:
            print_yaml(result)
