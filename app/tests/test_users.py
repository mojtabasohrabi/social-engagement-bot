import pytest
from fastapi.testclient import TestClient
from app.models import User


def test_register_user(client: TestClient, db):
    response = client.post(
        "/api/v1/users/register",
        json={"username": "newuser", "password": "newpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"
    assert "id" in data
    assert "created_at" in data


def test_register_duplicate_user(client: TestClient, test_user):
    response = client.post(
        "/api/v1/users/register",
        json={"username": "testuser", "password": "anypassword"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"
