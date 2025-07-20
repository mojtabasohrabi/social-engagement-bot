import pytest
from fastapi.testclient import TestClient


def test_create_profile(client: TestClient, test_user, auth_headers):
    response = client.post(
        "/api/v1/profiles/",
        json={"platform": "twitter", "username": "test_handle"},
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["platform"] == "twitter"
    assert data["username"] == "test_handle"
    assert data["user_id"] == test_user.id


def test_create_duplicate_profile(client: TestClient, test_user, auth_headers):
    # Create first profile
    client.post(
        "/api/v1/profiles/",
        json={"platform": "twitter", "username": "test_handle"},
        headers=auth_headers
    )

    # Try to create duplicate
    response = client.post(
        "/api/v1/profiles/",
        json={"platform": "twitter", "username": "test_handle"},
        headers=auth_headers
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Profile already exists"


def test_get_profiles(client: TestClient, test_user, auth_headers):
    # Create profiles
    client.post(
        "/api/v1/profiles/",
        json={"platform": "twitter", "username": "twitter_user"},
        headers=auth_headers
    )
    client.post(
        "/api/v1/profiles/",
        json={"platform": "instagram", "username": "insta_user"},
        headers=auth_headers
    )

    response = client.get("/api/v1/profiles/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert {p["platform"] for p in data} == {"twitter", "instagram"}


def test_get_profile_insights(client: TestClient, test_user, auth_headers):
    # Create profile
    response = client.post(
        "/api/v1/profiles/",
        json={"platform": "twitter", "username": "test_handle"},
        headers=auth_headers
    )
    profile_id = response.json()["id"]

    response = client.get(f"/api/v1/profiles/{profile_id}/insights", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "follower_change_24h" in data
    assert "recent_history" in data


def test_update_profile(client: TestClient, test_user, auth_headers):
    # Create profile
    response = client.post(
        "/api/v1/profiles/",
        json={"platform": "twitter", "username": "old_handle"},
        headers=auth_headers
    )
    profile_id = response.json()["id"]

    # Update profile
    response = client.put(
        f"/api/v1/profiles/{profile_id}",
        json={"username": "new_handle"},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["username"] == "new_handle"


def test_delete_profile(client: TestClient, test_user, auth_headers):
    # Create profile
    response = client.post(
        "/api/v1/profiles/",
        json={"platform": "twitter", "username": "test_handle"},
        headers=auth_headers
    )
    profile_id = response.json()["id"]

    # Delete profile
    response = client.delete(f"/api/v1/profiles/{profile_id}", headers=auth_headers)
    assert response.status_code == 200

    # Verify deletion
    response = client.get(f"/api/v1/profiles/{profile_id}", headers=auth_headers)
    assert response.status_code == 404


def test_unauthorized_access(client: TestClient):
    response = client.get("/api/v1/profiles/")
    assert response.status_code == 401
