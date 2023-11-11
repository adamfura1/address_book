from flask import Flask, render_template, request, redirect
import psycopg2
from database import (
    create_user,
    create_db_connection,
    check_user_existence,
    check_password_existence,
    get_all_users,
    delete_user
)

app = Flask(__name__)

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


@app.route("/change_password")
def change_password():
    return render_template("/change_password.html", title="change_password")


if __name__ == "__main__":
    app.run(debug=True)
