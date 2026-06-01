from __future__ import annotations

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for
)

from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

from . import db
from .models import User

from flask_login import login_user

auth: Blueprint = Blueprint(
    "auth",
    __name__
)

@auth.route("/register", methods=["GET", "POST"])
def register() -> str:
    if request.method == "POST":

        username: str = request.form["username"]

        password: str = request.form["password"]

        existing_user: User | None = User.query.filter_by(
            username=username
        ).first()

        if existing_user:
            flash("Username already exists.")

            return redirect(url_for("auth.register"))

        hashed_password: str = generate_password_hash(password)

        new_user: User = User(
            username=username,
            password=hashed_password
        )

        db.session.add(new_user)

        db.session.commit()

        flash("Registration successful.")

        return redirect(url_for("main.home"))

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login() -> str:

    if request.method == "POST":

        username: str = request.form["username"]

        password: str = request.form["password"]

        user: User | None = User.query.filter_by(
            username=username
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            flash("Login successful.")

            return redirect(
                url_for("main.home")
            )

        flash("Invalid username or password.")

    return render_template("login.html")