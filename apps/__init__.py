from flask import Flask
from exts import db, migrate, api
from apps.user.user_05 import user_bp
import settings


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings.Config)
    db.init_app(app)
    migrate.init_app(app, db=db)
    api.init_app(app)

    app.register_blueprint(user_bp)
    print(app.url_map)
    return app
