from __future__ import annotations

from flask import Blueprint

from flask_login import current_user

main: Blueprint = Blueprint(
    "main",
    __name__
)


@main.route("/")
def home() -> str:
    
    if current_user.is_authenticated:
        return f"Welcome {current_user.username}"

    return "Expense Tracker App"