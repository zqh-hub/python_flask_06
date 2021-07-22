import os


class Config:
    ENV = "development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:zqh139499@127.0.0.1:3306/flask_restful"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_DIR = os.path.join(BASE_DIR, "static")
    ICON_DIR = os.path.join(STATIC_DIR, "icon")

