"""Commands related to classes in Neon and Airtable"""
import argparse
import datetime
import logging
import re
from collections import defaultdict

import markdown
import yaml
from dateutil import parser as dateparser

from protohaven_api.class_automation.builder import (
    ClassEmailBuilder,
    gen_calendar_reminders,
)
from protohaven_api.commands.decorator import arg, command
from protohaven_api.config import tz, tznow  # pylint: disable=import-error
from protohaven_api.integrations import (  # pylint: disable=import-error
    airtable,
    comms,
    neon,
)

log = logging.getLogger("cli.classes")


class Commands:
    """Commands for managing classes in Airtable and Neon"""

    @command(
        arg(
            "--start",
            help="start date for calendar reminder window",
            type=str,
            required=True,
        ),
        arg(
            "--end",
            help="end date for calendar reminder window",
            type=str,
            required=True,
        ),
    )
    def gen_instructor_calendar_reminder(self, args):
        """Reads the list of instructors from Airtable and generates
        reminder comms to all instructors, plus the #instructors discord,
        to update their calendars for availability"""
        start = dateparser.parse(args.start)
        end = dateparser.parse(args.end)
        print(
            yaml.dump(
                gen_calendar_reminders(start, end),
                default_flow_style=False,
                default_style="",
            )
        )

    @command(
        arg(
            "--confirm",
            help="class IDs to auto-confirm when generating emails",
            type=int,
            nargs="+",
        ),
        arg(
            "--cancel",
            help="class IDs to auto-cancel when generating emails",
            type=int,
            nargs="+",
        ),
        arg(
            "--ignore",
            help="class IDs to ignore when generating emails",
            type=int,
            nargs="+",
        ),
        arg(
            "--filter",
            help="class IDs to restrict processing to when generating emails",
            type=int,
            nargs="+",
        ),
    )
    def gen_class_emails(self, args):
        """Reads schedule of classes from Neon and Airtable and outputs
        a list of emails to send to instructors, techs, and students.
        This does not actually send the emails; for that, see send_comms."""
        builder = ClassEmailBuilder(logging.getLogger("cli.email_builder"))
        builder.ignore_ovr = args.ignore or []
        builder.cancel_ovr = args.cancel or []
        builder.confirm_ovr = args.confirm or []
        builder.filter_ovr = args.filter or []
        # Add the rest here as needed

        result = builder.build()
        print(yaml.dump(result, default_flow_style=False, default_style=""))
        log.info(f"Generated {len(result)} notification(s)")

    def _handle_comms_event(self, e, dryrun=True):
        """Handle a single entry in a comms YAML file"""
        for k, v in e.get("side_effect", {}).items():
            if k.lower().strip() == "cancel":
                log.info(f"Cancelling #{v}")
                if not dryrun:
                    neon.set_event_scheduled_state(str(v), scheduled=False)

        if e["target"].startswith("#"):
            content = f"{e['subject']}\n\n{e['body']}"
            if dryrun:
                log.info(f"DRY RUN to discord {e['target']}")
                log.info(content)
            else:
                comms.send_discord_message(content, e["target"].split("#")[1])
                log.info(f"Sent to discord {e['target']}: {e['subject']}")
        else:
            email_validate_pattern = r"\S+@\S+\.\S+"
            emails = re.findall(
                email_validate_pattern,
                e["target"].replace(";", " ").replace(",", " ").lower(),
            )
            emails = [
                e.replace("(", "").replace(")", "").replace('"', "").replace("'", "")
                for e in emails
            ]

            if dryrun:
                log.info(f"\nDRY RUN to {', '.join(emails)}")
                log.info(f"Subject: {e['subject']}")
                log.info(e["body"])
            else:
                comms.send_email(e["subject"], e["body"], emails)
                log.info(f"Sent to {emails}: '{e['subject']}'")
                airtable.log_email(e["id"], ", ".join(emails), e["subject"], "Sent")
                log.info("Logged to airtable")

    @command(
        arg(
            "--start",
            help="Start date (yyyy-mm-dd)",
            type=str,
            required=True,
        ),
        arg(
            "--end",
            help="End date (yyyy-mm-dd)",
            type=str,
            required=True,
        ),
        arg(
            "--filter",
            help="CSV of subset instructors to filter scheduling to",
            type=str,
            required=False,
        ),
    )
    def build_scheduler_env(self, args):
        """Construct an environment for assigning classes at times to instructors"""
        start = dateparser.parse(args.start).astimezone(tz)
        end = dateparser.parse(args.end).astimezone(tz)
        inst = {a.strip() for a in args.filter.split(",")} if args.filter else None
        env = scheduler.generate_env(start, end, inst)
        print(yaml.dump(env, default_flow_style=False, default_style=""))

    @command(
        arg(
            "--path",
            help="path to env file",
            type=str,
            required=True,
        )
    )
    def run_scheduler(self, args):
        """Run the class scheduler on a provided env"""
        with open(args.path, "r", encoding="utf-8") as f:
            env = yaml.safe_load(f.read())
        instructor_classes, final_score = scheduler.solve_with_env(env)
        log.info(f"Final score: {final_score}")
        print(yaml.dump(instructor_classes, default_flow_style=False, default_style=""))

    @command(
        arg(
            "--path",
            help="path to schedule file",
            type=str,
            required=True,
        )
    )
    def append_schedule(self, args):
        """Adds a schedule (created with `run_scheduler`) to Airtable for
        instructor confirmation."""
        with open(args.path, "r", encoding="utf-8") as f:
            sched = yaml.safe_load(f.read())
        notifications = scheduler.gen_schedule_push_notifications(sched)
        scheduler.push_schedule(sched)
        print(yaml.dump(notifications, default_flow_style=False, default_style=""))

    @command(
        arg(
            "--id",
            help="class IDs to cancel",
            type=str,
            nargs="+",
        )
    )
    def cancel_classes(self, args):
        """cancel passed classes by unpublishing and disabling registration"""
        for i in args.id:
            i = i.strip()
            log.info(f"Cancelling #{i}")
            neon.set_event_scheduled_state(i, scheduled=False)
        log.info("Done")

    def _apply_pricing(self, event_id, evt):
        price = evt["fields"]["Price (from Class)"][0]
        qty = evt["fields"]["Capacity (from Class)"][0]
        log.debug(event_id, evt["fields"]["Name (from Class)"], price, qty)
        neon.assign_pricing(event_id, price, qty, clear_existing=True)

    def _schedule_event(
        self, event, desc, dry_run=True, archived=False, apply_tz_offset=True
    ):
        start = dateparser.parse(event["fields"]["Start Time"]).astimezone(tz)
        end = start + datetime.timedelta(hours=event["fields"]["Hours (from Class)"][0])
        days = event["fields"]["Days (from Class)"][0]
        if days > 1:
            end += datetime.timedelta(days=days)
        name = event["fields"]["Name (from Class)"][0]
        price = event["fields"]["Price (from Class)"]
        capacity = event["fields"]["Capacity (from Class)"][0]
        return neon.create_event(
            name,
            desc,
            start,
            end,
            price,
            max_attendees=capacity,
            dry_run=dry_run,
            apply_tz_offset=apply_tz_offset,
        )

    @command(
        arg(
            "--min-future-days",
            help="Don't schedule classes closer than this many days",
            type=int,
            default=14,
        ),
        arg(
            "--archived",
            help="Publish as archived",
            action=argparse.BooleanOptionalAction,
            default=False,
        ),
        arg(
            "--apply",
            help="Actually push the classes; will only print otherwise",
            action=argparse.BooleanOptionalAction,
            default=False,
        ),
    )
    def post_classes_to_neon(self, args):
        """Post a list of classes to Neon"""
        boilerplate = airtable.get_all_records("class_automation", "boilerplate")
        rules_and_expectations = [
            b["fields"]["Notes"]
            for b in boilerplate
            if b["fields"]["Name"] == "Rules & Expectations"
        ][0]
        cancellation_policy = [
            b["fields"]["Notes"]
            for b in boilerplate
            if b["fields"]["Name"] == "Cancellation Policy"
        ][0]
        age_section_fmt = [
            b["fields"]["Notes"]
            for b in boilerplate
            if b["fields"]["Name"] == "Age Requirement"
        ][0]

        def format_class_description(cls, suf=" (from Class)"):
            result = (
                markdown.markdown(cls["fields"]["Short Description" + suf][0]) + "\n"
            )
            sections = []
            for col in (
                "What you Will Create" + suf,
                "What to Bring/Wear" + suf,
                "Clearances Earned" + suf,
            ):
                body = cls["fields"].get(col, [""])[0]
                if body.strip() != "":
                    sections.append((col, body))

            if cls["fields"].get("Age Requirement" + suf) is not None:
                sections.append(
                    (
                        "Age Requirement",
                        age_section_fmt.format(
                            age=cls["fields"]["Age Requirement" + suf][0]
                        ),
                    )
                )

            result += "\n\n".join(
                [markdown.markdown(f"**{hdr}**\n\n{body}") for hdr, body in sections]
            )
            result += markdown.markdown(rules_and_expectations)
            result += markdown.markdown(cancellation_policy)
            return result

        scheduled_by_instructor = defaultdict(list)
        event_ids = []
        schedule_ids = []
        num = 0
        skip_unconfirmed = []
        skip_too_soon = []
        log.info("Scheduling:")
        now = tznow()
        for event in airtable.get_class_automation_schedule():
            cid = event["fields"]["ID"]
            start = dateparser.parse(event["fields"]["Start Time"]).astimezone(tz)
            if start < now:
                log.debug(
                    f"Skipping event {cid} from the past {event['fields']['Name (from Class)']}"
                )
                continue
            # Quietly ignore already-scheduled events
            if event["fields"].get("Neon ID", "") != "":
                log.debug(
                    f"Skipping scheduled event {cid} {event['fields']['Neon ID']}: {event['fields']['Name (from Class)']}"
                )
                continue

            if not event["fields"].get("Confirmed"):
                skip_unconfirmed.append(
                    f"{start} {event['fields']['Name (from Class)'][0]} with {event['fields']['Instructor']}"
                )
                continue
            if start < now + datetime.timedelta(days=args.min_future_days):
                skip_too_soon.append(
                    f"{start} {event['fields']['Name (from Class)'][0]} with {event['fields']['Instructor']}"
                )
                continue

            log.info(f"{start} {cid} {event['fields']['Name (from Class)']}")
            if args.apply:
                num += 1
                raise Exception("TODO")
                self._schedule_event(
                    event,
                    format_class_description(event),
                    not args.apply,
                    args.archived,
                )
                log.debug("Neon event created")
                self._apply_pricing(result_id, event)
                log.debug("Pricing applied")
                airtable.update_record(
                    {"Neon ID": str(result_id)},
                    "class_automation",
                    "schedule",
                    event["id"],
                )
                log.debug("Neon ID updated in Airtable")
                event_ids.append((result_id, event))
                schedule_ids.append(cid)
                scheduled_by_instructor[event["fields"]["Instructor"]].append(event)

        log.info(f"Total events scheduled: {num}")

        if num > 0:
            log.info("Reserving equipment for scheduled classes")
            args.cls = ",".join(schedule_ids)
            self.reserve_equipment_for_class(args)

        log.info("Skipping unconfirmed:")
        for s in skip_unconfirmed:
            log.info(s)
        log.info(f"Skipping too-soon ({args.min_future_days}d or sooner):")
        for s in skip_too_soon:
            log.info(s)
