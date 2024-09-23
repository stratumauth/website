# Copyright (C) 2024 jmh
# SPDX-License-Identifier: GPL-3.0-only

from flask import Blueprint, render_template

bp = Blueprint("privacy", __name__)


@bp.get("/privacy")
def privacy():
    return render_template("privacy.jinja")
