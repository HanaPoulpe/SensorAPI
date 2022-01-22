"""benzaitensensor API"""
import importlib.util
import logging
import os

import flask

from .config import ApplicationConfiguration, DefaultConfig


def create_app() -> flask.Flask:
    """
    Creates and configure flask application

    Configuration is loaded from .config module.

    The application will dynamically import modules with blueprints stored in the default
    "application.dir.blueprints" path.

    :return: Flask Application
    """
    # If no configuration was provided, load the configuration
    conf = ApplicationConfiguration()

    # Prepare Flask Appplicaiton
    app = flask.Flask("benzaitensendord", instance_relative_config=True)
    # Setup logger
    logger: logging.Logger = app.logger
    logger.setLevel(conf.get("logger.level"))
    conf.update(DefaultConfig(default_logger=logger))

    # Create instance path
    os.makedirs(app.instance_path, exist_ok=True)

    # Imports blueprints
    blueprint_dir = conf.get("application.dir.blueprints")
    for file in os.listdir(blueprint_dir):
        if not file.endswith(".py"):
            # No a python file
            continue

        module_spec = importlib.util.spec_from_file_location(
            f"blueprint.{file[:file.rfind('.')]}", os.path.join(blueprint_dir, file)
        )
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)

        if not hasattr(module, "blue_print") or not isinstance(
            module.blue_print, flask.Blueprint  # noqa
        ):
            # If module have no function called blue_print
            continue

        logger.info(f"Loading: {file[:file.rfind('.')]}")
        app.register_blueprint(module.blue_print)  # noqa

    return app


if __name__ == "__main__":
    create_app().run()
