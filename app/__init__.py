from flask import Flask
from flask_session import Session

from app import config


def create_app():
    app = Flask(__name__)
    app.secret_key = config.SECRET_KEY
    app.config['SESSION_TYPE'] = config.SESSION_TYPE
    app.config['SESSION_PERMANENT'] = config.SESSION_PERMANENT
    app.config['PERMANENT_SESSION_LIFETIME'] = config.PERMANENT_SESSION_LIFETIME
    Session(app)

    app.app_context().push()

    from .routes import auth, documents, query
    app.register_blueprint(auth.bp)
    app.register_blueprint(documents.bp)
    app.register_blueprint(query.bp)

    return app
