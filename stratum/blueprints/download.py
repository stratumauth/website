# Copyright (C) 2024 jmh
# SPDX-License-Identifier: GPL-3.0-only

import requests

from flask import Blueprint, render_template, current_app

from stratum import cache

bp = Blueprint("download", __name__)


@cache.cached(timeout=3600)
def _get_latest_tag() -> str:
    release_info_url = current_app.config["APP_RELEASE_INFO_URL"]
    res = requests.get(release_info_url)
    res.raise_for_status()
    return res.json()["tag_name"]


@bp.get("/download")
def download():
    return render_template("download.jinja", latest_tag=_get_latest_tag())
