import copy
from urllib.parse import quote

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    original_activities = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(original_activities))


def build_signup_url(activity_name: str, email: str) -> str:
    return f"/activities/{quote(activity_name, safe='')}/signup?email={quote(email, safe='')}"


def build_unregister_url(activity_name: str, email: str) -> str:
    return build_signup_url(activity_name, email)


def test_get_activities_returns_activity_list():
    # Arrange: no setup required beyond the default activity state

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200

    payload = response.json()
    assert isinstance(payload, dict)
    assert "Chess Club" in payload
    assert "Programming Class" in payload
    assert payload["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
    assert isinstance(payload["Chess Club"]["participants"], list)


def test_signup_adds_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    signup_url = build_signup_url(activity_name, email)

    # Act
    response = client.post(signup_url)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    updated = client.get("/activities").json()
    assert email in updated[activity_name]["participants"]


def test_duplicate_signup_returns_400():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    signup_url = build_signup_url(activity_name, email)

    # Act
    response = client.post(signup_url)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_removes_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    unregister_url = build_unregister_url(activity_name, email)

    # Act
    response = client.delete(unregister_url)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    updated = client.get("/activities").json()
    assert email not in updated[activity_name]["participants"]


def test_unregister_nonexistent_participant_returns_400():
    # Arrange
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"
    unregister_url = build_unregister_url(activity_name, email)

    # Act
    response = client.delete(unregister_url)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up for this activity"


def test_unregister_missing_activity_returns_404():
    # Arrange
    unregister_url = "/activities/Nonexistent%20Club/signup?email=test@mergington.edu"

    # Act
    response = client.delete(unregister_url)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
