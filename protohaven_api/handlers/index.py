"""handlers for main landing page"""
import datetime
import json

import pytz
from dateutil import parser as dateparser
from flask import Blueprint, render_template, request, session

from protohaven_api.handlers.auth import user_email, user_fullname
from protohaven_api.integrations.booked import get_reservations
from protohaven_api.integrations.neon import (
    fetch_attendees,
    fetch_published_upcoming_events,
    soft_search,
)
from protohaven_api.integrations.schedule import fetch_shop_events
from protohaven_api.rbac import require_login

page = Blueprint("index", __name__, template_folder="templates")


@page.route("/")
@require_login
def index():
    """Show the main dashboard page"""
    neon_account = session.get("neon_account")
    clearances = []
    roles = []
    neon_account["custom_fields"] = {"Clearances": {"optionValues": []}}
    neon_json = json.dumps(neon_account, indent=2)
    for cf in neon_account["individualAccount"]["accountCustomFields"]:
        if cf["name"] == "Clearances":
            clearances = [v["name"] for v in cf["optionValues"]]
        if cf["name"] == "API server role":
            roles = [v["name"] for v in cf["optionValues"]]
        neon_account["custom_fields"][cf["name"]] = cf

    return render_template(
        "dashboard.html",
        fullname=user_fullname(),
        email=user_email(),
        neon_id=session.get("neon_id"),
        neon_account=neon_account,
        neon_json=neon_json,
        clearances=clearances,
        roles=roles,
    )


@page.route("/neon_lookup", methods=["GET", "POST"])
def neon_id_lookup():
    """Look up the ID of a user in Neon based on a search by name or email"""
    if request.method == "GET":
        return render_template("search.html")
    elif request.method == "POST":
        result = []
        search = request.values.get("search")
        if search is None:
            return result
        rep = soft_search(search)
        if not rep.get("success"):
            raise RuntimeError(rep)

        for i in rep["data"]["individuals"]:
            i = i["data"]
            result.append(f"{i['firstName']} {i['lastName']} (#{i['accountId']})")
        return result


@page.route("/events/attendees")
def events_dashboard_attendee_count():
    """Gets the attendee count for a given event, by its neon ID"""
    event_id = request.args.get("id")
    if event_id is None:
        raise RuntimeError("Requires param id")
    attendees = 0
    for a in fetch_attendees(event_id):
        if a["registrationStatus"] == "SUCCEEDED":
            attendees += 1
    return str(attendees)


@page.route("/events")
def events_dashboard():
    """Show relevant upcoming events - designed for a kiosk display"""
    events = []
    now = datetime.datetime.now()
    # NOTE: does not currently support intensive date periods. Need to expand
    # dates to properly show this.
    try:
        for e in fetch_published_upcoming_events():
            date = dateparser.parse(e["startDate"] + " " + e["startTime"])
            if date < now:
                continue
            events.append(
                {
                    "id": e["id"],
                    "name": e["name"],
                    "date": date,
                    "capacity": e["capacity"],
                    "registration": e["enableEventRegistrationForm"],
                }
            )

        events.sort(key=lambda e: e["date"])
    except json.decoder.JSONDecodeError:
        print("Neon error, proceeding anyways")

    shop_events = []
    for e, dates in fetch_shop_events().items():
        for start, end in dates:
            shop_events.append((e, dateparser.parse(start)))

    reservations = []
    tz = pytz.timezone("EST")
    now = now.astimezone(tz)
    for r in get_reservations(
        now.replace(hour=0, minute=0, second=0),
        now.replace(hour=23, minute=59, second=59),
    )["reservations"]:
        start = dateparser.parse(r["startDate"]).astimezone(tz)
        end = dateparser.parse(r["endDate"]).astimezone(tz)
        open_time = now.replace(hour=10)
        close_time = now.replace(hour=22)
        reservations.append(
            {
                "start": start.strftime("%-I:%M %p") if start > open_time else "open",
                "end": end.strftime("%-I:%M %p") if start < close_time else "close",
                "name": f"{r['firstName']} {r['lastName']}",
                "resource": r["resourceName"],
            }
        )
    print(reservations)
    return render_template(
        "events.html", events=events, shop_events=shop_events, reservations=reservations
    )
