from __future__ import annotations

from flask import Blueprint


main: Blueprint = Blueprint(
    "main",
    __name__
)


@main.route("/")
def home() -> str:
    return "Expense Tracker App"