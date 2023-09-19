import psycopg2


# TODO ten plik musi być rozdzielony pomiędzy logowanie i rejestracje
# ze względu na to, że zapytanie INSERT będzie miało mniej kolumn niż przy logowaniu


# Funkcja do tworzenia połączenia do bazy danych
def create_db_connection():
    return psycopg2.connect("postgresql://postgres:postgres@localhost:5432/address_book_db")


def create_user(connection, username, password):
    cursor = connection.cursor()
    try:
        query = """INSERT INTO users (username, password) VALUES (%s, %s)"""
        cursor.execute(query, (username, password))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()


def check_user_existence(connection, username):
    cursor = connection.cursor()
    try:
        query = "SELECT username FROM users WHERE username = %s"
        cursor.execute(query, [username])
        user = cursor.fetchone()
        return user is not None
    except Exception as e:
        raise e
    finally:
        cursor.close()
