from flask import Flask, render_template, request, redirect, session, url_for
from database import (
    create_user,
    create_db_connection,
    check_user_existence,
    check_password_existence,
    get_all_users,
    delete_user,
    get_id_by_username,
    create_contact_for_logged,
    get_contacts_by_user_id,
    get_user_by_id,
    get_contact_info_by_id,
    change_password,
    delete_contact_from_db
)


app = Flask(__name__)
app.secret_key = 'some_secret_key' # Klucz do szyfrowania sesji

connection = create_db_connection()


@app.route("/")
def first_page():
    return render_template("first_page.html", title="Welcome!")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        check_username = check_user_existence(connection, username)
        check_password = check_password_existence(connection, password)

        if check_username is True and check_password is True:
            _id = get_id_by_username(connection, username)
            session['user_id'] = _id
            return redirect("/logged")
        else:
            return "Błędne hasło lub nazwa użytkownika!"

    return render_template("login.html", title="Logowanie")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_existence = check_user_existence(connection, username)
        if user_existence is True:
            return "Nazwa użytkownika jest już zajęta"

        else:
            create_user(connection, username, password)
            return redirect('/login')

    return render_template("register.html", title="Rejestracja")


@app.route("/users", methods=["GET", "POST"])
def users_list():
    if request.method == "POST":
        user_id = request.form.get("id")
        if user_id:
            result = delete_user(connection, user_id)
            if result:
                return redirect("/users")
            else:
                return "Błąd podczas usuwania użytkownika."

    users = get_all_users(connection)
    return render_template("users.html", users=users, title="Users")


@app.route("/logged")
def logged():
    return render_template("/logged.html", title="Logged")


@app.route("/change_password", methods=["GET", "POST"])
def change_password_route():
    user_id = session.get('user_id')

    if request.method == "POST":
        old_password = request.form["old_password"]
        new_password = request.form["new_password"]
        new_password_repeat = request.form["new_password_repeat"]

        if new_password != new_password_repeat:
            return "New passwords do not match"

        result = change_password(connection, user_id, old_password, new_password)

        if result is None:
            return "Password changed successfully"
        else:
            return result

    return render_template("/change_password.html", title="change_password")


@app.route("/contacts", methods=["GET"])
def contacts():
    user_id = session.get('user_id')
    if user_id:
        contacts_ = get_contacts_by_user_id(connection, user_id)
        print(contacts_)
        return render_template("contacts.html", title="Contacts", contacts=contacts_)
    else:
        return redirect(url_for('login'))


@app.route("/add_new_contact", methods=["GET", "POST"])
def add_new_contact():
    if request.method == "POST":
        name = request.form["name"]
        last_name = request.form["last_name"]
        phone_number = request.form["phone_number"]
        email = request.form["email"]
        address = request.form["address"]
        user_id = session.get('user_id')
        create_contact_for_logged(connection, user_id, name, last_name, phone_number,
                                  email, address)

    return render_template("/add_new_contact.html", title="Dodaj nowy kontakt")

@app.route("/delete_contact/<int:contact_id>", methods=["POST"])
def delete_contact(contact_id):
    user_id = session.get('user_id')
    delete_contact_from_db(connection, user_id, contact_id)
    contacts_ = get_contacts_by_user_id(connection, user_id)
    return render_template("contacts.html", title="Contacts", contacts=contacts_)


@app.route("/logout", methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('first_page'))


@app.route("/user_profile/<int:contact_id>")
def user_profile(contact_id):
    user_info = get_user_by_id(connection, contact_id)
    contact_info = get_contact_info_by_id(connection, contact_id)
    return render_template("user_profile.html", title="User Profile", user_info=user_info, contact_info=contact_info)


if __name__ == "__main__":
    app.run(debug=True)
