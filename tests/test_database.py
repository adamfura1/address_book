from database import create_db_connection, get_all_users
import pytest

def test_create_db_connection():
    connection = create_db_connection()

    assert connection is not None