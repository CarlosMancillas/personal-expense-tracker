from __future__ import annotations

from flask import Blueprint

from flask_login import (
    current_user,
    login_required
)

main: Blueprint = Blueprint(
    "main",
    __name__
)


@main.route("/")
def home() -> str:
    
    if current_user.is_authenticated:
        return f"Welcome {current_user.username}"

    return "Expense Tracker App"

@main.route("/dashboard")
@login_required
def dashboard() -> str:
    return f"Welcome to your dashboard, {current_user.username}"