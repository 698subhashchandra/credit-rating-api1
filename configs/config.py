import configparser
import os
from typing import Dict, Any
from flask import Flask
from flask.cli import load_dotenv
from configs.constants import (
    DEFAULT_ENV,
    CONFIG_FILE_NAME,
    FLASK_ENV,
    DEBUG_KEY,
    HOST_KEY,
    PORT_KEY,
    LOGGING_TYPE_KEY,
    CACHE_TYPE_KEY,
    DEFAULT_CONFIG_VALUES, TRUE_VALUES, RELOADED_KEY,
)
from utils.logger import project_logger

# Load environment variables from .env file
load_dotenv()


# Load the configuration from an .ini file
CONFIG_PATH = os.path.join(os.path.dirname(__file__), CONFIG_FILE_NAME)
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

# Determine the current environment
ENV = os.environ.get(FLASK_ENV, DEFAULT_ENV)


class Config:
    """Central configuration class for Flask application settings."""

    def __init__(self):
        # General Flask Configurations
        self.ENV = self._get_config_value(FLASK_ENV, default=DEFAULT_CONFIG_VALUES[FLASK_ENV])
        self.DEBUG = self._get_config_value(DEBUG_KEY, default=DEFAULT_CONFIG_VALUES[DEBUG_KEY], is_boolean=True)
        self.HOST = self._get_config_value(HOST_KEY, default=DEFAULT_CONFIG_VALUES[HOST_KEY])
        self.PORT = self._get_config_value(PORT_KEY, default=DEFAULT_CONFIG_VALUES[PORT_KEY], is_integer=True)
        self.LOGGING_TYPE = self._get_config_value(LOGGING_TYPE_KEY, default=DEFAULT_CONFIG_VALUES[LOGGING_TYPE_KEY])
        self.RELOADED = self._get_config_value(RELOADED_KEY, default=DEFAULT_CONFIG_VALUES[RELOADED_KEY],
                                               is_boolean=True)

        # Application-Specific Configurations
        self.CACHE_TYPE = self._get_config_value(CACHE_TYPE_KEY, default=DEFAULT_CONFIG_VALUES[CACHE_TYPE_KEY])
    
    def _get_config_value(self, key: str, default: Any, is_boolean: bool = False, is_integer: bool = False) -> Any:
        """
        Helper function to retrieve the config value from environment variables, config file, or fallback to defaults.

        :param key: The configuration key to look up.
        :param default: The default value to use if neither environment nor config file provides a value.
        :param is_boolean: Whether the value is expected to be a boolean (default: False).
        :param is_integer: Whether the value is expected to be an integer (default: False).
        :return: The configuration value.
        """
        # First check environment variable
        value = os.getenv(key)

        if value is not None:
            if is_boolean:
                value = value.strip().lower() in TRUE_VALUES
            elif is_integer:
                value = int(value)
            return value

        # Check in the .ini file
        value = config.get(ENV, key.lower(), fallback=None)

        if value is not None:
            if is_boolean:
                value = value.strip().lower() in TRUE_VALUES
            elif is_integer:
                value = int(value)
            return value

        # If no value is found, use the default and log it
        project_logger.warning(
            f"Config key '{key}' is missing in both environment and config file. Falling back to default value.")
        return default

    def as_dict(self) -> Dict[str, Any]:
        """Returns configuration as a dictionary for debugging or external usage."""
        return self.__dict__


def apply_config_to_app(app: Flask):
    """
    Apply the loaded configuration to a Flask application instance.

    :param app: Flask application object
    :return: None
    """
    cfg = Config()
    for key, value in cfg.as_dict().items():
        app.config[key] = value
