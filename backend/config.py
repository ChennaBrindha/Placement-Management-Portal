import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "placementportal-secret-key")
    # SQLite for easy local dev — swap to MySQL URI in production
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///placement.db"
    )
    # MySQL example (uncomment and set env var for production):
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:password@localhost/placementdb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-placement-secret")
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB max upload