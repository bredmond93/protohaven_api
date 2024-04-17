# pylint: skip-file
import json

from protohaven_api.integrations import airtable as a


def test_set_booked_resource_id(mocker):
    mocker.patch.object(a, "get_connector")
    a.get_connector().airtable_request.return_value = mocker.MagicMock(content="{}")
    a.set_booked_resource_id("airtable_id", "resource_id")
    fname, args, kwargs = a.get_connector().airtable_request.mock_calls[0]
    assert kwargs["data"] == json.dumps({"fields": {"BookedResourceId": "resource_id"}})
    assert "airtable_id" in args[2]


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
    _, args, _ = a.get_connector().airtable_request.mock_calls[0]
    assert args[0] == "test_token"
    assert args[2].endswith("test_tbl_id?offset=&a=test_suffix")

    _, args, _ = a.get_connector().airtable_request.mock_calls[1]
    assert args[2].endswith("test_tbl_id?offset=1&a=test_suffix")
