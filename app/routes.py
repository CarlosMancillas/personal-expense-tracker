from __future__ import annotations

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
) 

from flask_login import (
    current_user,
    login_required
)

from app import db
from app.models import Transaction

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

    transactions: list[Transaction] = (
        Transaction.query.filter_by(
            user_id=current_user.id
        ).all()
    )

    total_income: float = sum(
        transaction.amount
        for transaction in transactions
        if transaction.transaction_type == "income"
    )

    total_expenses: float = sum(
        transaction.amount
        for transaction in transactions
        if transaction.transaction_type == "expense"
    )

    balance: float = (
        total_income - total_expenses
    )

    transaction_count: int = len(
        transactions
    )

    return render_template(
        "dashboard.html",
        total_income=total_income,
        total_expenses=total_expenses,
        balance=balance,
        transaction_count=transaction_count
    )



@main.route(
    "/transactions/add",
    methods=["GET", "POST"]
)
@login_required
def add_transaction() -> str:

    if request.method == "POST":

        title: str = request.form["title"]

        amount: float = float(
            request.form["amount"]
        )

        category: str = request.form["category"]

        transaction_type: str = request.form[
            "transaction_type"
        ]

        transaction: Transaction = Transaction(
            title=title,
            amount=amount,
            category=category,
            transaction_type=transaction_type,
            user_id=current_user.id
        )

        db.session.add(transaction)

        db.session.commit()

        flash("Transaction added successfully.")

        return redirect(
            url_for("main.dashboard")
        )

    return render_template(
        "add_transaction.html"
    )

@main.route("/transactions")
@login_required
def transactions() -> str:

    user_transactions: list[Transaction] = (
        Transaction.query.filter_by(
            user_id=current_user.id
        )
        .order_by(
            Transaction.created_at.desc()
        )
        .all()
    )

    return render_template(
        "transactions.html",
        transactions=user_transactions
    )