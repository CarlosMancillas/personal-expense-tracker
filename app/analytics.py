from __future__ import annotations

import pandas as pd
import io
import base64
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from app.models import Transaction


class AnalyticsService:

    @staticmethod
    def get_user_transactions(
        user_id: int
    ) -> list[Transaction]:

        return (
            Transaction.query
            .filter_by(user_id=user_id)
            .all()
        )

    @staticmethod
    def _to_dataframe(
        transactions: list[Transaction]
    ) -> pd.DataFrame:

        if not transactions:
            return pd.DataFrame(columns=[
                "id",
                "title",
                "amount",
                "category",
                "transaction_type",
                "created_at",
                "user_id"
            ])

        df = pd.DataFrame([{
            "id":               t.id,
            "title":            t.title,
            "amount":           t.amount,
            "category":         t.category,
            "transaction_type": t.transaction_type,
            "created_at":       t.created_at,
            "user_id":          t.user_id,
        } for t in transactions])

        df["amount"] = df["amount"].astype("float64")
        df["created_at"] = pd.to_datetime(df["created_at"])
        df["category"] = df["category"].astype("category")
        df["transaction_type"] = df["transaction_type"].astype("category")

        return df

    @staticmethod
    def get_user_dataframe(
        user_id: int
    ) -> pd.DataFrame:

        transactions = AnalyticsService.get_user_transactions(
            user_id
        )

        return AnalyticsService._to_dataframe(transactions)
    
    @staticmethod
    def get_monthly_summary(
        user_id: int
    ) -> pd.DataFrame:

        df = AnalyticsService.get_user_dataframe(user_id)

        if df.empty:
            return df

        df["month"] = df["created_at"].dt.to_period("M")

        summary = (
            df.groupby(["month", "transaction_type"])["amount"]
            .sum()
            .unstack(fill_value=0)
            .reset_index()
        )

        summary.columns.name = None

        if "income" not in summary.columns:
            summary["income"] = 0.0

        if "expense" not in summary.columns:
            summary["expense"] = 0.0

        summary["net"] = summary["income"] - summary["expense"]

        summary["month"] = summary["month"].astype(str)

        return summary

    @staticmethod
    def get_category_summary(
        user_id: int
    ) -> pd.DataFrame:

        df = AnalyticsService.get_user_dataframe(user_id)

        if df.empty:
            return df

        summary = (
            df.groupby(["category", "transaction_type"])["amount"]
            .sum()
            .reset_index()
            .sort_values("amount", ascending=False)
            .reset_index(drop=True)
        )

        summary["amount"] = summary["amount"].astype("float64")

        return summary

    @staticmethod
    def get_insights(
        user_id: int
    ) -> dict:

        df = AnalyticsService.get_user_dataframe(user_id)

        if df.empty:
            return {}

        expenses = df[df["transaction_type"] == "expense"]

        # Top spending category
        if not expenses.empty:
            top_category: str = (
                expenses.groupby("category")["amount"]
                .sum()
                .idxmax()
            )
            top_category_total: float = (
                expenses.groupby("category")["amount"]
                .sum()
                .max()
            )
        else:
            top_category = "N/A"
            top_category_total = 0.0

        # Biggest single expense
        if not expenses.empty:
            biggest_idx = expenses["amount"].idxmax()
            biggest_expense_title: str  = expenses.loc[biggest_idx, "title"]
            biggest_expense_amount: float = expenses.loc[biggest_idx, "amount"]
        else:
            biggest_expense_title  = "N/A"
            biggest_expense_amount = 0.0

        # Month-over-month spending change
        df["month"] = df["created_at"].dt.to_period("M")
        monthly_expenses = (
            expenses.assign(month=expenses["created_at"].dt.to_period("M"))
            .groupby("month")["amount"]
            .sum()
            .sort_index()
        )

        if len(monthly_expenses) >= 2:
            current_month_spend: float  = float(monthly_expenses.iloc[-1])
            previous_month_spend: float = float(monthly_expenses.iloc[-2])
            mom_change: float = current_month_spend - previous_month_spend
            mom_change_pct: float = (
                (mom_change / previous_month_spend) * 100
                if previous_month_spend > 0
                else 0.0
            )
        else:
            current_month_spend  = float(monthly_expenses.iloc[-1]) if len(monthly_expenses) == 1 else 0.0
            previous_month_spend = 0.0
            mom_change           = 0.0
            mom_change_pct       = 0.0

        return {
            "top_category":          top_category,
            "top_category_total":    top_category_total,
            "biggest_expense_title":  biggest_expense_title,
            "biggest_expense_amount": biggest_expense_amount,
            "current_month_spend":   current_month_spend,
            "previous_month_spend":  previous_month_spend,
            "mom_change":            mom_change,
            "mom_change_pct":        round(mom_change_pct, 1),
        }
    
    @staticmethod
    def get_monthly_chart(
        user_id: int
    ) -> str:

        summary = AnalyticsService.get_monthly_summary(user_id)

        if summary.empty:
            return ""

        months = summary["month"].tolist()
        income = summary["income"].tolist()
        expense = summary["expense"].tolist()

        x = range(len(months))
        width = 0.35

        fig, ax = plt.subplots(figsize=(8, 4))

        ax.bar(
            [i - width / 2 for i in x],
            income,
            width=width,
            label="Income",
            color="#4CAF50"
        )
        ax.bar(
            [i + width / 2 for i in x],
            expense,
            width=width,
            label="Expenses",
            color="#F44336"
        )

        ax.set_xticks(list(x))
        ax.set_xticklabels(months, rotation=45, ha="right")
        ax.set_ylabel("Amount ($)")
        ax.set_title("Monthly Income vs Expenses")
        ax.legend()

        plt.tight_layout()

        return AnalyticsService._fig_to_base64(fig)


    @staticmethod
    def get_category_chart(
        user_id: int
    ) -> str:

        df = AnalyticsService.get_user_dataframe(user_id)

        if df.empty:
            return ""

        expenses = df[df["transaction_type"] == "expense"]

        if expenses.empty:
            return ""

        category_totals = (
            expenses.groupby("category")["amount"]
            .sum()
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots(figsize=(6, 6))

        ax.pie(
            category_totals.values,
            labels=category_totals.index,
            autopct="%1.1f%%",
            startangle=140
        )

        ax.set_title("Spending by Category")

        plt.tight_layout()

        return AnalyticsService._fig_to_base64(fig)


    @staticmethod
    def _fig_to_base64(fig) -> str:

        buffer = io.BytesIO()

        fig.savefig(buffer, format="png")

        plt.close(fig)

        buffer.seek(0)

        encoded = base64.b64encode(
            buffer.read()
        ).decode("utf-8")

        return f"data:image/png;base64,{encoded}"