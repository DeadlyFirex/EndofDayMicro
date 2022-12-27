from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager

from services.config import Config
from services.utilities import Utilities
from services.database import init_db

from flaskr.auth import auth
from flaskr.generics import generics
from flaskr.entry import entry

from models.user import User
from models.entry import Entry


# Get configuration, create Flask application
config = Config().get_config()


def create_app():
    app = Flask(config.application.name)

    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(generics)
    app.register_blueprint(entry)

    # Setup configuration
    app.config.from_mapping(
        DEBUG=config.application.debug,
        SECRET_KEY=Utilities.generate_secret(),
        DATABASE=(config.database.type + config.database.absolute_path),
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
    limiter.limit(config.ratelimiting.default)(auth)
    limiter.limit(config.ratelimiting.default)(generics)
    limiter.limit(config.ratelimiting.default)(entry)

    # Register JWT
    jwt = JWTManager(app).init_app(app)

    # Check database status
    # TODO: Improve this function to be more flexible.
    # @app.before_first_request
    # def first_time_run():
    #     app.logger.info("Checking for database initialization.")
    #     try:
    #         result = (User.query.all(), Entry.query.all())
    #     except:
    #         init_db()
    #         app.logger.info("Performing new database initialization.")
    #         return
    #     if None in result or [] in result:
    #         init_db()
    #         app.logger.info("Repopulating database tables.")
    #         return
    #     app.logger.info("Finished checking, no new initialization required.")

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return {"status": 429, "message": f"Exceeded ratelimit: {e.description}"}, 429

    @app.errorhandler(422)
    def ratelimit_handler(e):
        return {"status": 422, "message": f"Unable to verify token, probably due to restart: {e.description}"}, 422

    return app


if __name__ == "__main__":
    create_app().run(config.server.host, config.server.port, config.server.debug)
