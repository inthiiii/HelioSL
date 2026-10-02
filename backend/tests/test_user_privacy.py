from datetime import UTC, datetime
from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.main import app
from app.security.dependencies import (
    get_current_user,
)


client = TestClient(app)


def household_user():
    return SimpleNamespace(
        id=21,
        full_name="Household Demo",
        email="household.demo@heliosl.lk",
        district="Colombo",
        user_type="household",
        role="user",
        is_active=True,
        created_at=datetime.now(UTC),
    )


def test_user_can_read_only_own_profile():
    app.dependency_overrides[
        get_current_user
    ] = household_user

    try:
        own_response = client.get(
            "/api/v1/users/21"
        )
        other_response = client.get(
            "/api/v1/users/22"
        )
    finally:
        app.dependency_overrides.clear()

    assert own_response.status_code == 200
    assert own_response.json()["id"] == 21
    assert other_response.status_code == 403
    assert other_response.json()["detail"] == (
        "Access to another user is forbidden"
    )


def test_user_profile_lookup_requires_authentication():
    response = client.get(
        "/api/v1/users/21"
    )

    assert response.status_code in {401, 403}
