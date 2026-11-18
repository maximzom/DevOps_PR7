import json
import pytest


@pytest.mark.parametrize(
    "path, expected_status",
    [
        ("/", 200),
        ("/health.json", 200),
        ("/missing-page", 404),
    ],
)
def test_http_status_codes(http_get, path: str, expected_status: int):
    status, _ = http_get(path)
    assert status == expected_status


def test_index_page_release(http_get, expected_release: str):
    status, body = http_get("/")
    assert status == 200
    assert expected_release in body


def test_health_json_payload(http_get, expected_release: str):
    status, body = http_get("/health.json")
    assert status == 200
    payload = json.loads(body)
    assert payload["status"] == "ok"
    assert payload["release"] == expected_release