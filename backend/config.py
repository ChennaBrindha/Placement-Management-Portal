class Config:
    SECRET_KEY = "placementportal"

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:bru%402026@localhost/placementdb"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "jwt-secret"