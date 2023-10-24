from flask import Flask, render_template, request, redirect
import psycopg2
from database import create_user, create_db_connection, check_user_existence, check_password_existence, get_all_users

app = Flask(__name__)

connection = create_db_connection()


@app.route("/")
def first_page():
    return render_template("first_page.html", title="Welcome!")


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        check_username = check_user_existence(connection, username)
        check_password = check_password_existence(connection, password)

        if check_username is True and check_password is True:
            return redirect("/logged_page")
        else:
            return "Błędne hasło lub nazwa użytkownika!"

    return render_template("login_page.html", title="Logowanie")


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


@app.route("/users")
def users_list():
    users = get_all_users(connection)
    return render_template("list_of_users.html", users=users, title="Users")


@app.route("/delete_user", methods=["POST"])
def delete_user():
    user_id = request.form["id"]
    if id:
        try:
            cursor = connection.cursor()
            query = "DELETE FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            connection.commit()
            cursor.close()
        except Exception as e:
            connection.rollback()
            raise e

    return redirect("/users")


@app.route("/logged")
def logged_page():
    return render_template("/logged.html", title="Logged")


if __name__ == "__main__":
    app.run(debug=True)
