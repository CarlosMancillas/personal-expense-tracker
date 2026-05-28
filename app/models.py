from __future__ import annotations

from datetime import datetime
from typing import List

from flask_login import UserMixin

from app import db
from app import login_manager

@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__: str = "user"

    id: int = db.Column(db.Integer, primary_key=True)

    username: str = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    password: str = db.Column(
        db.String(200),
        nullable=False
    )

    transactions: List[Transaction] = db.relationship(
        "Transaction",
        backref="owner",
        lazy=True
    )

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Transaction(db.Model):
    __tablename__: str = "transaction"

    id: int = db.Column(
        db.Integer,
        primary_key=True
    )

    title: str = db.Column(
        db.String(100),
        nullable=False
    )

    amount: float = db.Column(
        db.Float,
        nullable=False
    )

    category: str = db.Column(
        db.String(50),
        nullable=False
    )

    transaction_type: str = db.Column(
        db.String(20),
        nullable=False
    )

    created_at: datetime = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user_id: int = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    def __repr__(self) -> str:
        return (
            f"<Transaction {self.title} - "
            f"{self.amount}>"
        )