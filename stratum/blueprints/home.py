# Copyright (C) 2024 jmh
# SPDX-License-Identifier: GPL-3.0-only

from flask import Blueprint, render_template

bp = Blueprint("home", __name__)


@bp.get("/")
def home():
    return render_template("home.jinja")
