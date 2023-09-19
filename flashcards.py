from flask import Flask, render_template, request, redirect
import psycopg2
from database import create_user, create_db_connection, check_user_existence


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
        stored_password = check_user_existence(connection, username)
        print(stored_password)

        if stored_password is not None and password == stored_password:
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
