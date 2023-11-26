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


# def create_user_for_logged(connection, user_id, name, last_name, phone_number, email, address):
#     cursor = connection.cursor()
#     try:
#         query = """INSERT INTO contacts (user_id, name, last_name, phone_number, email, address) VALUES
#                                         (%s, %s, %s, %s, %s, %s)"""
#         cursor.execute(query, (user_id, name, last_name, phone_number, email, address))
#         connection.commit()
#     except Exception as e:
#         connection.rollback()
#         raise e
#     finally:
#         cursor.close()

# nieużywana funkcja - zdecydować co z nią zrobić
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


def check_password_existence(connection, password):
    cursor = connection.cursor()
    try:
        query = "SELECT password FROM users WHERE password = %s"
        cursor.execute(query, [password])
        user = cursor.fetchone()
        return user is not None
    except Exception as e:
        raise e
    finally:
        cursor.close()


def change_password(connection, user_id, old_password, new_password):
    cursor = connection.cursor()
    try:
        # Sprawdź czy stare hasło jest poprawne
        query_check_old_password = "SELECT password FROM users WHERE id = %s"
        cursor.execute(query_check_old_password, (user_id,))
        stored_password = cursor.fetchone()[0]

        if stored_password != old_password:
            return "Old password is incorrect!"

        # Zmiana hasła użytkownika
        query_change_password = "UPDATE users SET password = %s WHERE id = %s"
        cursor.execute(query_change_password, (new_password, user_id))
        connection.commit()

        return None # Zwróc None, aby oznaczyć udaną zmianę hasła

    except Exception as e:
        connection.rollback()
        return str(e)

    finally:
        cursor.close()


def get_all_users(connection):
    cursor = connection.cursor()
    try:
        query = "SELECT id, username FROM users"
        cursor.execute(query)
        users = cursor.fetchall()
        return users
    except Exception as e:
        return e
    finally:
        cursor.close()


def delete_user(connection, user_id):
    try:
        cursor = connection.cursor()
        query = "DELETE FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        connection.commit()
        cursor.close()
        return True
    except Exception as e:
        connection.rollback()
        return False


def get_id_by_username(connection, username):
    cursor = connection.cursor()
    try:
        query = "SELECT id FROM users WHERE username = %s"
        cursor.execute(query, [username])
        _id = cursor.fetchone()
        return _id[0] if _id else None
    except Exception as e:
        raise e
    finally:
        cursor.close()


def get_contacts_by_user_id(connection, user_id):
    cursor = connection.cursor()
    try:
        query = "SELECT id, name, last_name FROM contacts WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        contacts = cursor.fetchall()
        return contacts
    except Exception as e:
        return e
    finally:
        cursor.close()


def get_user_by_id(connection, user_id):
    cursor = connection.cursor()
    try:
        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        user_info = cursor.fetchall()
        return user_info
    except Exception as e:
        return e
    finally:
        cursor.close()


def get_contact_info_by_id(connection, contact_id):
    cursor = connection.cursor()
    try:
        query = "SELECT phone_number, email, address FROM contacts WHERE id = %s"
        cursor.execute(query, (contact_id,))
        contact_info = cursor.fetchone()
        return contact_info
    except Exception as e:
        return e
    finally:
        cursor.close()


def create_contact_for_logged(connection, user_id, name, last_name, phone_number, email, address):
    cursor = connection.cursor()
    try:
        query = """INSERT INTO contacts (user_id, name, last_name, phone_number, email, address) VALUES 
                                        (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (user_id, name, last_name, phone_number, email, address))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()


def delete_contact_from_db(connection, user_id, contact_id):
    cursor = connection.cursor()
    try:
        query = "DELETE FROM contacts WHERE user_id = %s AND id = %s"
        cursor.execute(query, (user_id, contact_id))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
