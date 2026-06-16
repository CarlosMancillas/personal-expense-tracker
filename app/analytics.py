from __future__ import annotations

import pandas as pd

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