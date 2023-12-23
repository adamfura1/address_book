from flask import Flask, session
from database import check_user_existence, create_user
from flashcards import app, change_password, create_db_connection


def test_create_user(test_db):
    username = "test_user"
    password = "test_password"

    result = create_user(test_db, username, password)

    assert result is not None
    assert check_user_existence(test_db, username)


def test_change_password():
    connection = create_db_connection()
    with app.test_request_context('/change_password', method='POST',
                                  data={'old_password': 'old_pass', 'new_password': 'new_pass',
                                        'new_password_repeat': 'new_pass'}):
        session['user_id'] = 1
        result = change_password(connection, 1, 'old_pass', 'new_pass')
        assert result is None


def test_change_password_mismatch():
    connection = create_db_connection()
    with app.test_request_context('/change_password', method='POST',
                                  data={'old_password': 'old_pass', 'new_password': 'new_pass',
                                        'new_password_repeat': 'different_pass'}):
        session['user_id'] = 1
        result = change_password(connection, 1, 'old_pass', 'new_pass')
        assert result == 'New passwords do not match'
