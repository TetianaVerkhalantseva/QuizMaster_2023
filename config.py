import secrets

# Database config
HOST = "kark.uit.no"
PORT = 3306
USER = "stud_v23_tda072"
PASSWORD = "2021T-Dakhno32"
DATABASE = "stud_v23_tda072"
CHARSET = "utf8"


class BaseConfig:
    SECRET_KEY = secrets.token_urlsafe(32)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset={CHARSET}"
