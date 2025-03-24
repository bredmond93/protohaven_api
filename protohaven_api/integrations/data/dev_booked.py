"""A mock version of Booked serving results pulled from mock_data"""

import logging
from urllib.parse import urlparse

from flask import Flask, request

app = Flask(__file__)

log = logging.getLogger("integrations.data.dev_booked")


@app.route("/Reservations/", methods=["GET", "POST"])
def get_events():
    """Mock events endpoint for Neon - needs to be completed"""
    # start = dateparser.parse(request.values["startDateTime"])
    # end = dateparser.parse(request.values["endDateTime"])
    # for m in mock_data["booked"]...
    if request.method == "POST":
        log.warning(f"Dev POST to /Reservations/: {request.data}")
    return {"reservations": []}


client = app.test_client()


def handle(mode, url, json=None):
    """Local execution of mock flask endpoints for Booked"""
    url = urlparse(url).path
    if mode == "GET":
        return client.get(url)
    if mode == "POST":
        return client.post(url, json=json)
    raise RuntimeError(f"mode not supported: {mode}")
