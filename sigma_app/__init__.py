import os
from pathlib import Path

from flask import Flask, g, session

from sigma_app.auth import auth
from sigma_app.routes import main
from sigma_app.storage import get_user_by_id, initialize_database


def create_app(test_config=None):
    base_dir = Path(__file__).resolve().parent.parent
    app = Flask(
        __name__,
        template_folder=str(base_dir / "templates"),
        static_folder=str(base_dir / "static"),
    )
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-key"),
        DATABASE_PATH=os.environ.get("DATABASE_PATH", str(base_dir / "database.db")),
    )
    if test_config is not None:
        app.config.update(test_config)

    initialize_database(app.config["DATABASE_PATH"])

    @app.before_request
    def load_current_user():
        g.database_path = app.config["DATABASE_PATH"]
        user_id = session.get("user_id")
        g.user = get_user_by_id(app.config["DATABASE_PATH"], user_id) if user_id else None

    @app.context_processor
    def inject_current_user():
        return {"current_user": g.get("user")}

    app.register_blueprint(main)
    app.register_blueprint(auth)
    return app