import pytest
from fastapi.testclient import TestClient


def test_create_alert(client: TestClient, test_user, auth_headers):
    # Create profile first
    response = client.post(
        "/api/v1/profiles/",
        json={"platform": "twitter", "username": "test_handle"},
        headers=auth_headers
    )
    profile_id = response.json()["id"]

    # Create alert
    response = client.post(
        "/api/v1/alerts/",
        json={"profile_id": profile_id, "threshold": 1000},
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["profile_id"] == profile_id
    assert data["threshold"] == 1000
    assert data["is_active"] == True
    assert data["triggered"] == False


def test_create_duplicate_alert(client: TestClient, test_user, auth_headers):
    # Create profile
    response = client.post(
        "/api/v1/profiles/",
        json={"platform": "twitter", "username": "test_handle"},
        headers=auth_headers
    )
    profile_id = response.json()["id"]

    # Create first alert
    client.post(
        "/api/v1/alerts/",
        json={"profile_id": profile_id, "threshold": 1000},
        headers=auth_headers
    )

    # Try to create duplicate
    response = client.post(
        "/api/v1/alerts/",
        json={"profile_id": profile_id, "threshold": 1000},
        headers=auth_headers
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Alert already exists"


def test_get_alerts(client: TestClient, test_user, auth_headers):
    # Create profile
    response = client.post(
        "/api/v1/profiles/",
        json={"platform": "twitter", "username": "test_handle"},
        headers=auth_headers
    )
    profile_id = response.json()["id"]

    # Create alerts
    client.post(
        "/api/v1/alerts/",
        json={"profile_id": profile_id, "threshold": 1000},
        headers=auth_headers
    )
    client.post(
        "/api/v1/alerts/",
        json={"profile_id": profile_id, "threshold": 5000},
        headers=auth_headers
    )

    response = client.get("/api/v1/alerts/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert {a["threshold"] for a in data} == {1000, 5000}


def test_update_alert(client: TestClient, test_user, auth_headers):
    # Create profile and alert
    response = client.post(
        "/api/v1/profiles/",
        json={"platform": "twitter", "username": "test_handle"},
        headers=auth_headers
    )
    profile_id = response.json()["id"]

    response = client.post(
        "/api/v1/alerts/",
        json={"profile_id": profile_id, "threshold": 1000},
        headers=auth_headers
    )
    alert_id = response.json()["id"]

    # Update alert
    response = client.put(
        f"/api/v1/alerts/{alert_id}",
        json={"threshold": 2000, "is_active": False},
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["threshold"] == 2000
    assert data["is_active"] == False


def test_delete_alert(client: TestClient, test_user, auth_headers):
    # Create profile and alert
    response = client.post(
        "/api/v1/profiles/",
        json={"platform": "twitter", "username": "test_handle"},
        headers=auth_headers
    )
    profile_id = response.json()["id"]

    response = client.post(
        "/api/v1/alerts/",
        json={"profile_id": profile_id, "threshold": 1000},
        headers=auth_headers
    )
    alert_id = response.json()["id"]

    # Delete alert
    response = client.delete(f"/api/v1/alerts/{alert_id}", headers=auth_headers)
    assert response.status_code == 200

    # Verify deletion
    response = client.get(f"/api/v1/alerts/{alert_id}", headers=auth_headers)
    assert response.status_code == 404
