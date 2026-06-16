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
from app.analytics import AnalyticsService

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

    transactions = (
        AnalyticsService.get_user_transactions(
            current_user.id
        )
    )

    total_income: float = sum(
        t.amount for t in transactions
        if t.transaction_type == "income"
    )

    total_expenses: float = sum(
        t.amount for t in transactions
        if t.transaction_type == "expense"
    )

    balance: float = total_income - total_expenses

    transaction_count: int = len(transactions)

    monthly_summary = (
        AnalyticsService.get_monthly_summary(
            current_user.id
        )
    )

    monthly_rows = (
        monthly_summary.to_dict(orient="records")
        if not monthly_summary.empty
        else []
    )

    category_summary = (
        AnalyticsService.get_category_summary(
            current_user.id
        )
    )

    category_rows = (
        category_summary.to_dict(orient="records")
        if not category_summary.empty
        else []
    )

    return render_template(
        "dashboard.html",
        total_income=total_income,
        total_expenses=total_expenses,
        balance=balance,
        transaction_count=transaction_count,
        monthly_rows=monthly_rows,
        category_rows=category_rows
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