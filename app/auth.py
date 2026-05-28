from __future__ import annotations

from flask import Blueprint


auth: Blueprint = Blueprint(
    "auth",
    __name__
)