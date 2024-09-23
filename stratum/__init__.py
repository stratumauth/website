# Copyright (C) 2024 jmh
# SPDX-License-Identifier: GPL-3.0-only

import os
import datetime

from flask import Flask, render_template
from flask_caching import Cache
from flask_mail import Mail

cache = Cache()
mail = Mail()


def copyright_year():
    return {"copyright_year": datetime.datetime.now().strftime("%Y")}


def handle_not_found(e):
    return (
        render_template(
            "error.jinja",
            title="404 Not Found",
            description="The page could not be found",
        ),
        404,
    )


def create_app(test_config=None):
    app = Flask(__name__, static_url_path="/")

    if test_config is not None:
        app.config.from_mapping(test_config)
        app.config.from_object("stratum.config.TestingConfig")
    elif os.environ["FLASK_ENV"] == "development":
        app.config.from_object("stratum.config.DevelopmentConfig")
    else:
        app.config.from_object("stratum.config.ProductionConfig")

    cache.init_app(app)
    mail.init_app(app)

    from .blueprints import home, download, wiki, iconpacks, tools, feedback, privacy

    app.register_blueprint(home.bp)
    app.register_blueprint(download.bp)
    app.register_blueprint(wiki.bp)
    app.register_blueprint(tools.bp)
    app.register_blueprint(iconpacks.bp)
    app.register_blueprint(feedback.bp)
    app.register_blueprint(privacy.bp)

    app.context_processor(copyright_year)

    app.register_error_handler(404, handle_not_found)

    return app
