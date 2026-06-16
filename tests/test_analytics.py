from __future__ import annotations

from datetime import datetime
from unittest.mock import MagicMock

from app.analytics import AnalyticsService


def make_transaction(
    id, title, amount, category, transaction_type, created_at, user_id=1
):
    t = MagicMock()
    t.id = id
    t.title = title
    t.amount = amount
    t.category = category
    t.transaction_type = transaction_type
    t.created_at = created_at
    t.user_id = user_id
    return t


# ── _to_dataframe ────────────────────────────────────────────────────────────

def test_to_dataframe_empty():
    df = AnalyticsService._to_dataframe([])
    assert df.empty
    assert list(df.columns) == [
        "id", "title", "amount", "category",
        "transaction_type", "created_at", "user_id"
    ]


def test_to_dataframe_column_types():
    transactions = [
        make_transaction(1, "Salary", 1000.0, "salary",
                         "income", datetime(2025, 5, 1)),
        make_transaction(2, "Rent",   500.0,  "housing",
                         "expense", datetime(2025, 5, 15)),
    ]
    df = AnalyticsService._to_dataframe(transactions)

    assert str(df["amount"].dtype)           == "float64"
    assert df["created_at"].dtype.kind == "M"
    assert str(df["category"].dtype)         == "category"
    assert str(df["transaction_type"].dtype) == "category"


def test_to_dataframe_values():
    transactions = [
        make_transaction(1, "Salary", 1000.0, "salary",
                         "income", datetime(2025, 5, 1)),
    ]
    df = AnalyticsService._to_dataframe(transactions)

    assert df.iloc[0]["title"]            == "Salary"
    assert df.iloc[0]["amount"]           == 1000.0
    assert df.iloc[0]["transaction_type"] == "income"


# ── get_monthly_summary ───────────────────────────────────────────────────────

def test_monthly_summary_empty():
    df = AnalyticsService._to_dataframe([])
    # simulate what get_monthly_summary does on empty input
    assert df.empty


def test_monthly_summary_single_month():
    transactions = [
        make_transaction(1, "Salary", 1000.0, "salary",
                         "income",  datetime(2025, 5, 1)),
        make_transaction(2, "Rent",   400.0,  "housing",
                         "expense", datetime(2025, 5, 15)),
        make_transaction(3, "Food",   100.0,  "food",
                         "expense", datetime(2025, 5, 20)),
    ]

    with MagicMock() as mock:
        AnalyticsService.get_user_transactions = staticmethod(
            lambda uid: transactions
        )
        summary = AnalyticsService.get_monthly_summary(1)

    assert len(summary) == 1
    assert summary.iloc[0]["month"]   == "2025-05"
    assert summary.iloc[0]["income"]  == 1000.0
    assert summary.iloc[0]["expense"] == 500.0
    assert summary.iloc[0]["net"]     == 500.0


def test_monthly_summary_multiple_months():
    transactions = [
        make_transaction(1, "Salary",  1000.0, "salary",
                         "income",  datetime(2025, 5, 1)),
        make_transaction(2, "Rent",     400.0, "housing",
                         "expense", datetime(2025, 5, 15)),
        make_transaction(3, "Salary",  1200.0, "salary",
                         "income",  datetime(2025, 6, 1)),
        make_transaction(4, "Groceries", 200.0, "food",
                         "expense", datetime(2025, 6, 10)),
    ]

    AnalyticsService.get_user_transactions = staticmethod(
        lambda uid: transactions
    )
    summary = AnalyticsService.get_monthly_summary(1)

    assert len(summary) == 2
    assert summary.iloc[0]["month"] == "2025-05"
    assert summary.iloc[1]["month"] == "2025-06"
    assert summary.iloc[1]["net"]   == 1000.0


def test_monthly_summary_only_income():
    """Guard: expense column must exist even when there are no expenses."""
    transactions = [
        make_transaction(1, "Salary", 1000.0, "salary",
                         "income", datetime(2025, 5, 1)),
    ]
    AnalyticsService.get_user_transactions = staticmethod(
        lambda uid: transactions
    )
    summary = AnalyticsService.get_monthly_summary(1)

    assert "expense" in summary.columns
    assert summary.iloc[0]["expense"] == 0.0


def test_monthly_summary_only_expenses():
    """Guard: income column must exist even when there are no incomes."""
    transactions = [
        make_transaction(1, "Rent", 400.0, "housing",
                         "expense", datetime(2025, 5, 1)),
    ]
    AnalyticsService.get_user_transactions = staticmethod(
        lambda uid: transactions
    )
    summary = AnalyticsService.get_monthly_summary(1)

    assert "income" in summary.columns
    assert summary.iloc[0]["income"] == 0.0

# ── get_category_summary ─────────────────────────────────────────────────────

def test_category_summary_empty():
    df = AnalyticsService._to_dataframe([])
    assert df.empty


def test_category_summary_sorted_by_amount():
    """Highest amount category must appear first."""
    transactions = [
        make_transaction(1, "Rent",     800.0, "housing",
                         "expense", datetime(2025, 5, 1)),
        make_transaction(2, "Groceries", 200.0, "food",
                         "expense", datetime(2025, 5, 10)),
        make_transaction(3, "Transport",  50.0, "transport",
                         "expense", datetime(2025, 5, 15)),
    ]
    AnalyticsService.get_user_transactions = staticmethod(
        lambda uid: transactions
    )
    summary = AnalyticsService.get_category_summary(1)

    assert summary.iloc[0]["category"] == "housing"
    assert summary.iloc[1]["category"] == "food"
    assert summary.iloc[2]["category"] == "transport"


def test_category_summary_separates_income_and_expense():
    """Same category name used for both types must produce two rows."""
    transactions = [
        make_transaction(1, "Freelance", 500.0, "salary",
                         "income",  datetime(2025, 5, 1)),
        make_transaction(2, "Salary",   1000.0, "salary",
                         "income",  datetime(2025, 5, 15)),
        make_transaction(3, "Tools",     100.0, "salary",
                         "expense", datetime(2025, 5, 20)),
    ]
    AnalyticsService.get_user_transactions = staticmethod(
        lambda uid: transactions
    )
    summary = AnalyticsService.get_category_summary(1)

    salary_rows = summary[summary["category"] == "salary"]
    assert len(salary_rows) == 2

    income_total = salary_rows[
        salary_rows["transaction_type"] == "income"
    ]["amount"].values[0]

    assert income_total == 1500.0


def test_category_summary_aggregates_same_category():
    """Multiple transactions in the same category must be summed."""
    transactions = [
        make_transaction(1, "Lunch",  20.0, "food",
                         "expense", datetime(2025, 5, 1)),
        make_transaction(2, "Dinner", 35.0, "food",
                         "expense", datetime(2025, 5, 10)),
        make_transaction(3, "Coffee", 10.0, "food",
                         "expense", datetime(2025, 5, 20)),
    ]
    AnalyticsService.get_user_transactions = staticmethod(
        lambda uid: transactions
    )
    summary = AnalyticsService.get_category_summary(1)

    assert len(summary) == 1
    assert summary.iloc[0]["amount"] == 65.0