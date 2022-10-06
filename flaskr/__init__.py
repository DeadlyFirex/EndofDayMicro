from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager

from os import path

from services.config import Config
from services.utilities import Utilities

# Get configuration, create Flask application
config = Config().get_config()


def create_app():
    app = Flask(config.application.name)

    # Setup configuration
    app.config.from_mapping(
        DEBUG=config.application.debug,
        SECRET_KEY=Utilities.generate_secret(),
        DATABASE=path.join(app.instance_path, config.database.filename),
        SQLALCHEMY_DATABASE_URI=config.database.type + config.database.absolute_path,
        JWT_SECRET_KEY=Utilities.generate_secret(),
        RATELIMIT_ENABLED=True
    )

    # Configure blueprints/views and ratelimiting
    # TODO: Make every limit configurable
    limiter = Limiter(app, key_func=get_remote_address, default_limits=[config.ratelimiting.default],
                      storage_uri="memory://",
                      enabled=True,
                      headers_enabled=True
                      )

    # Register JWT
    jwt = JWTManager(app).init_app(app)

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return {"status": 429, "message": f"Exceeded ratelimit: {e.description}"}, 429

    @app.errorhandler(422)
    def ratelimit_handler(e):
        return {"status": 422, "message": f"Unable to verify token, probably due to restart: {e.description}"}, 422

    return app


if __name__ == "__main__":
    create_app().run(config.server.host, config.server.port, config.server.debug)
