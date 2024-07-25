# pylint: skip-file
import json

import pytest
from dateutil import parser as dateparser
import datetime

from protohaven_api.config import tz
from protohaven_api.integrations import airtable as a


def d(i, h=0):
    """Returns a date based on an integer, for testing"""
    return datetime.datetime(year=2025, month=1, day=1) + datetime.timedelta(
        days=i, hours=h
    )


def test_set_booked_resource_id(mocker):
    mocker.patch.object(a, "get_connector")
    mocker.patch.object(
        a,
        "cfg",
        return_value={
            "base_id": "test_base_id",
            "token": "test_token",
            "tools": "tools_id",
        },
    )
    a.get_connector().airtable_request.return_value = mocker.MagicMock(content="{}")
    a.set_booked_resource_id("airtable_id", "resource_id")
    fname, args, kwargs = a.get_connector().airtable_request.mock_calls[0]
    assert kwargs["data"] == json.dumps({"fields": {"BookedResourceId": "resource_id"}})
    assert "airtable_id" == kwargs["rec"]


def test_get_all_records(mocker):
    mocker.patch.object(
        a,
        "cfg",
        return_value={
            "base_id": "test_base_id",
            "token": "test_token",
            "test_tbl": "test_tbl_id",
        },
    )
    mocker.patch.object(a, "get_connector")
    a.get_connector().airtable_request.side_effect = [
        mocker.MagicMock(
            status_code=200,
            content=json.dumps({"records": ["foo", "bar", "baz"], "offset": 1}),
        ),
        mocker.MagicMock(
            status_code=200, content=json.dumps({"records": ["fizz", "buzz"]})
        ),
    ]
    assert a.get_all_records("test_base", "test_tbl", suffix="a=test_suffix") == [
        "foo",
        "bar",
        "baz",
        "fizz",
        "buzz",
    ]
    _, args, kwargs = a.get_connector().airtable_request.mock_calls[0]
    print(kwargs)
    assert kwargs["suffix"] == "?offset=&a=test_suffix"

    _, args, kwargs = a.get_connector().airtable_request.mock_calls[1]
    print(kwargs)
    assert kwargs["suffix"] == "?offset=1&a=test_suffix"


@pytest.mark.parametrize(
    "desc, data, want",
    [
        (
            "correct role & tool code",
            {
                "Published": "2024-04-01",
                "Roles": ["role1"],
                "Tool Name (from Tool Codes)": ["Sandblaster"],
            },
            True,
        ),
        (
            "correct role, non cleared tool code",
            {
                "Published": "2024-04-01",
                "Roles": ["role1"],
                "Tool Name (from Tool Codes)": ["Planer"],
            },
            False,
        ),
        (
            "wrong role, cleared tool",
            {
                "Published": "2024-04-01",
                "Roles": ["badrole"],
                "Tool Name (from Tool Codes)": ["Sandblaster"],
            },
            False,
        ),
        (
            "Correct role, no tool",
            {
                "Published": "2024-04-01",
                "Roles": ["role1"],
                "Tool Name (from Tool Codes)": [],
            },
            True,
        ),
        (
            "too old",
            {
                "Published": "2024-03-01",
                "Roles": ["role1"],
                "Tool Name (from Tool Codes)": [],
            },
            False,
        ),
    ],
)
def test_get_announcements_after(desc, data, want, mocker):
    mocker.patch.object(
        a, "_get_announcements_cached_impl", return_value=[{"fields": data}]
    )
    got = a.get_announcements_after(
        dateparser.parse("2024-03-14").astimezone(tz), ["role1"], ["Sandblaster"]
    )
    if want:
        assert got
    else:
        assert not got


def _arec(email, start, end, interval, interval_end=None):
    return {"fields": {'Email (from Instructor)': email, 'Start': start.isoformat(), 'End': end.isoformat(), 'Interval': interval, "Interval End": interval_end.isoformat() if interval_end else None}}

@pytest.mark.parametrize("desc,records,email,t0,t1,want", [
        (   "Mismatch instructor email",
            [_arec("a", d(0, 18), d(0, 21), 0)], 
            "b", d(0), d(1), 
            [],
        ),
        ( "Email match, simple inclusion",
            [_arec("a", d(0, 18), d(0, 21), 0)], 
            "a", d(0), d(1), 
            [(d(0, 18), d(0, 21))],
        ),
        ( "Daily repeat returns on next day availability",
            [_arec("a", d(0, 18), d(0, 21), 1)], 
            "a", d(1), d(2), 
            [(d(1, 18), d(1, 21))],
        ),
        ( "No returns if before repeating event",
            [_arec("a", d(0, 18), d(0, 21), 1)], 
            "a", d(-2), d(-1), 
            [],
        ),
        ( "Availability is clamped by t0 and t1",
            [_arec("a", d(0, 18), d(0, 21), 0)], 
            "a", d(0, 19), d(0, 20), 
            [(d(0, 19), d(0, 20))],
        ),
        (   "2d repetition skips over search window",
            [_arec("a", d(0, 18), d(0, 21), 2)], 
            "a", d(1), d(2), 
            [],
        ),
        (   "Long repetition test",
            [_arec("a", d(0, 18), d(0, 21), 1)], 
            "a", d(365), d(366), 
            [(d(365, 18), d(365, 21))],
        ),
        (   "Multiple returns",
            [_arec("a", d(0, 18), d(0, 21), 1)], 
            "a", d(1), d(3), 
            [(d(1, 18), d(1, 21)), (d(2, 18), d(2, 21))],
        ),
        (
            "Search after interval end returns nothing",
            [_arec("a", d(0, 18), d(0, 21), 1, d(5))],
             "a", d(6), d(7),
            [],
        ),

    ])
def test_get_instructor_availability(mocker, desc, records, email, t0, t1, want):
    mocker.patch.object(a, "get_all_records", return_value=records)
    got = list(a.get_instructor_availability(email, t0, t1))
    assert got == want


@pytest.mark.parametrize("desc,rec,cut_start,cut_end,want", [
        (   "Delete",
            _arec("a", d(0, 18), d(0, 21), 1), 
            None, None, 
            (None, None),
        ),

    ])
def test_trim_availability(mocker, desc, rec, cut_start, cut_end, want):
    mocker.patch.object(a, "get_record", return_value=rec)
    mocker.patch.object(a, "update_record", side_effect = lambda data, _0, _1, _2: data)
    mocker.patch.object(a, "delete_record", side_effect = lambda _0, _1, _2: None)
    mocker.patch.object(a, "insert_records", side_effect = lambda data, _0, _1: {"fields": data})
    got = a.trim_availability("rec_id", cut_start, cut_end)
    assert got == want

