"""benzaitensensor API"""
import importlib
import logging
import os

import flask

import configuration

from .config import ApplicationConfiguration


def create_app(conf: configuration.AppConfig | None = None) -> flask.Flask:
    """
    Creates and configure flask application

    :param config: Configuration to use, if none is provided a default config is created
    :return: Flask Application
    """
    # If no configuration was provided, load the configuration
    if not conf:
        conf = ApplicationConfiguration()

    # Setup logger
    logger: logging.Logger = conf.get("logger")
    logger.setLevel(conf.get("logger.level"))

    # Prepare Flask Appplicaiton
    app = flask.Flask("benzaitensendord", instance_relative_config=True)

    # Create instance path
    os.makedirs(app.instance_path, exist_ok=True)

    # Imports blueprints
    for file in os.listdir(conf.get("application.dir.blueprints")):
        if not file.endswith(".py"):
            # No a python file
            continue

        module = importlib.import_module(file)
        if not hasattr(module, "blue_print") or not isinstance(
            module.blue_print, flask.Blueprint  # noqa
        ):
            # If module have no function called blue_print
            continue
        app.register_blueprint(module.blue_print)  # noqa

    return app
