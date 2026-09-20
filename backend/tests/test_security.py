from app.security.jwt import (
    create_access_token,
    decode_access_token,
)
from app.security.password import (
    hash_password,
    verify_password,
)


def test_password_hashing():
    password = "SecurePass123!"

    hashed = hash_password(password)

    assert hashed != password

    assert verify_password(
        password,
        hashed,
    )


def test_wrong_password_fails():
    hashed = hash_password(
        "SecurePass123!"
    )

    assert not verify_password(
        "WrongPassword123!",
        hashed,
    )


def test_access_token():
    token = create_access_token(
        subject="42"
    )

    subject = decode_access_token(
        token
    )

    assert subject == "42"


def test_invalid_token():
    subject = decode_access_token(
        "invalid.token.value"
    )

    assert subject is None