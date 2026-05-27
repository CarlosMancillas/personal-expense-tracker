import os


BASE_DIR: str = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY: str = "your-secret-key"

    SQLALCHEMY_DATABASE_URI: str = (
        "sqlite:///"
        + os.path.join(BASE_DIR, "instance", "expense_tracker.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False