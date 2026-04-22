import os

from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_restful import Api

try:
    from .config import Config
    from .models import bcrypt, db
    from .resources import register_resources
except ImportError:
    from config import Config
    from models import bcrypt, db
    from resources import register_resources


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    Migrate(app, db)
    api = Api(app)
    register_resources(api)

    @app.get("/")
    def index():
        return {"message": "Productivity API is running."}, 200

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Route not found."}), 404

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5555))
    app.run(host="0.0.0.0", port=port, debug=True)
