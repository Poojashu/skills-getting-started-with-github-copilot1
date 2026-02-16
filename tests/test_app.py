import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data, "Activities list should not be empty."

def test_signup_and_unregister():
    # Pick an activity from the list
    activities = client.get("/activities").json()
    activity_name = next(iter(activities))
    test_email = "pytest-student@mergington.edu"

    # Sign up
    signup_url = f"/activities/{activity_name}/signup?email={test_email}"
    response = client.post(signup_url)
    assert response.status_code == 200
    assert "message" in response.json()

    # Duplicate signup should fail
    response2 = client.post(signup_url)
    assert response2.status_code == 400
    assert "already signed up" in response2.json().get("detail", "")

    # Unregister
    unregister_url = f"/activities/{activity_name}/unregister?email={test_email}"
    response3 = client.post(unregister_url)
    assert response3.status_code == 200
    assert "message" in response3.json()

    # Unregister again should fail
    response4 = client.post(unregister_url)
    assert response4.status_code == 400
    assert "not registered" in response4.json().get("detail", "")
