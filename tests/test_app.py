import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def restore_activity_state():
    original_activities = copy.deepcopy(app_module.activities)
    yield
    app_module.activities = original_activities


client = TestClient(app_module.app)


def test_unregister_participant_from_activity():
    response = client.delete(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "unregistered" in data["message"].lower()

    activities = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_unknown_participant_returns_404():
    response = client.delete(
        "/activities/Chess Club/signup",
        params={"email": "missing@mergington.edu"},
    )

    assert response.status_code == 404
