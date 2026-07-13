from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def restore_activities():
    original = deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)


def test_unregister_participant_from_activity():
    with TestClient(app) as client:
        response = client.delete(
            "/activities/Chess Club/participants",
            params={"email": "michael@mergington.edu"},
        )

        assert response.status_code == 200
        assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
        assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"
