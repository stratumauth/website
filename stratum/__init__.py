# Copyright (C) 2024 jmh
# SPDX-License-Identifier: GPL-3.0-only

import functools
import json
import os
import datetime

from typing import Optional

from flask import Flask, render_template, current_app
from flask_caching import Cache
from flask_mail import Mail
from markupsafe import Markup

cache = Cache()
mail = Mail()


def copyright_year_processor():
    return {"copyright_year": datetime.datetime.now().strftime("%Y")}

@functools.lru_cache(maxsize=1)
def _get_asset_manifest() -> dict[str, dict]:
    with open(
            os.path.join(current_app.root_path, ".vite", "manifest.json"),
            "r",
            encoding="utf-8",
    ) as file:
        return json.load(file)


@functools.lru_cache(maxsize=None)
def _get_manifest_chunk(name: str) -> Optional[dict]:
    manifest = _get_asset_manifest()
    return next((c for c in manifest.values() if c["name"] == name), None)


def module_path_processor(name: str) -> str:
    vite_dev_server = current_app.config["VITE_DEV_SERVER"]

    if vite_dev_server is not None:
        return f"{vite_dev_server}/src/{name}/index.js"

    chunk = _get_manifest_chunk(name)

    if chunk is None:
        return ""

    return chunk["file"][len("static") :]


def module_style_processor(name: str) -> Markup:
    if current_app.config["VITE_DEV_SERVER"] is not None:
        return Markup()

    chunk = _get_manifest_chunk(name)

    if chunk is None or "css" not in chunk:
        return Markup()

    result = ""

    for css in chunk["css"]:
        dist_path = css[len("static") :]
        result += f'<link rel="stylesheet" href="{dist_path}">'

    return Markup(result)


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
        app.config.from_object("stratum.config.development.TestingConfig")
    elif os.environ["FLASK_ENV"] == "development":
        app.config.from_object("stratum.config.development.DevelopmentConfig")
    else:
        app.config.from_object("stratum.config.production.ProductionConfig")

    cache.init_app(app)
    mail.init_app(app)

    from .blueprints import (
        home,
        download,
        wiki,
        iconpacks,
        tools,
        feedback,
        privacy,
    )

    app.register_blueprint(home.bp)
    app.register_blueprint(download.bp)
    app.register_blueprint(wiki.bp)
    app.register_blueprint(tools.bp)
    app.register_blueprint(iconpacks.bp)
    app.register_blueprint(feedback.bp)
    app.register_blueprint(privacy.bp)

    app.context_processor(copyright_year_processor)

    app.context_processor(
        lambda: {
            "get_module_path": module_path_processor,
            "include_module_style": module_style_processor,
        }
    )

    app.register_error_handler(404, handle_not_found)

    return app
