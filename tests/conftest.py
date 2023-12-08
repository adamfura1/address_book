import pytest
from flashcards import create_db_connection


@pytest.fixture(scope="session")
def test_db():
    connection = create_db_connection()

    yield connection
    connection.close()

