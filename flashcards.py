from flask import Flask, render_template, request, redirect
import psycopg2
from database import create_user, create_db_connection, check_user_existence, check_password_existence

app = Flask(__name__)


@app.route("/")
def first_page():
    return render_template("first_page.html", title="Welcome!")


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        connection = create_db_connection()
        check_username = check_user_existence(connection, username)
        check_password = check_password_existence(connection, password)

        if check_username is True and check_password is True:
            return redirect("/")
        else:
            return "Błędne hasło lub nazwa użytkownika!"

    return render_template("login_page.html", title="Logowanie")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        create_user(username, password)
        return redirect('/login')

    return render_template("register.html", title="Rejestracja")


if __name__ == "__main__":
    app.run(debug=True)
