from flashcards import create_user, check_user_existence
import pytest


def test_create_user(test_db):
    username = "test_user"
    password = "test_password"

    result = create_user(test_db, username, password)

    assert result is not None
    assert check_user_existence(test_db, username)
