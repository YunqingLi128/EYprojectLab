from flask import Flask
from config import DevelopmentConfig


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(DevelopmentConfig())

    from . import views
    app.register_blueprint(views.bp)

    return app


app = create_app()
