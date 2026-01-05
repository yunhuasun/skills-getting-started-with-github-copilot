from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

TEST_ACTIVITY = "Tennis Club"
TEST_EMAIL = "test_user@example.com"


def test_get_activities():
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert TEST_ACTIVITY in data


def test_signup_and_unregister_flow():
    # Ensure clean state
    if TEST_EMAIL in activities[TEST_ACTIVITY]["participants"]:
        activities[TEST_ACTIVITY]["participants"].remove(TEST_EMAIL)

    # Sign up
    r = client.post(f"/activities/{TEST_ACTIVITY}/signup?email={TEST_EMAIL}")
    assert r.status_code == 200
    assert "Signed up" in r.json().get("message", "")

    # Confirm participant appears in activities
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert TEST_EMAIL in data[TEST_ACTIVITY]["participants"]

    # Unregister
    r = client.delete(f"/activities/{TEST_ACTIVITY}/participants?email={TEST_EMAIL}")
    assert r.status_code == 200
    assert "Unregistered" in r.json().get("message", "")

    # Confirm participant removed
    r = client.get("/activities")
    data = r.json()
    assert TEST_EMAIL not in data[TEST_ACTIVITY]["participants"]

    # Unregister again should return 404
    r = client.delete(f"/activities/{TEST_ACTIVITY}/participants?email={TEST_EMAIL}")
    assert r.status_code == 404
