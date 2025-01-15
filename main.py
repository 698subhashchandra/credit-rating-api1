import os
from flask import Flask
from configs.config import apply_config_to_app
from configs.constants import ENV_KEY, HOST_KEY, PORT_KEY, RELOADED_KEY, PORT, HOST, USE_RELOADER, LOG_LISTENING_AT, \
    FLASK_ENV, DEFAULT_ENV, LOCAL
from routes.rating_route import api
from abc import ABCMeta

from utils.decorators import limiter
from utils.logger import project_logger


class HookServer(metaclass=ABCMeta):
    def __call__(self, flask_app, *args, **kwargs):
        # Manipulate app before the server starts
        if flask_app.config[ENV_KEY] in [LOCAL]:
            # Use Flask's built-in server
            kwargs[HOST] = flask_app.config[HOST_KEY]
            kwargs[PORT] = flask_app.config[PORT_KEY]
            kwargs[USE_RELOADER] = flask_app.config[RELOADED_KEY]
            flask_app.run(*args, **kwargs)
        else:
            # Use WSGI server
            from gevent.pywsgi import WSGIServer
            http_server = WSGIServer((flask_app.config[HOST_KEY], flask_app.config[PORT_KEY]), flask_app,
                                     log=project_logger)
            project_logger.info(f"{LOG_LISTENING_AT} : {flask_app.config[HOST_KEY]}:{flask_app.config[PORT_KEY]}")
            http_server.serve_forever()


def create_app():
    flask_app = Flask(__name__)

    # Register Limiter with the Flask app
    limiter.init_app(flask_app)

    # Apply configuration
    apply_config_to_app(flask_app)

    # Register blueprints or extensions
    flask_app.register_blueprint(api)

    return flask_app


if __name__ == "__main__":
    app = create_app()
    server = HookServer()  # Instantiate HookServer
    server(app)  # Use HookServer to run the app
