from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt, cors
from .routes import register_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config.get("FRONTEND_URL")}})

    # Register routes
    register_routes(app)

    @app.route("/")
    def index():
        return {"message": "WorkBridge Backend is running"}, 200

    return app
