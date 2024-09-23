# Copyright (C) 2024 jmh
# SPDX-License-Identifier: GPL-3.0-only

from flask import Blueprint, render_template

bp = Blueprint("tools", __name__)


@bp.get("/tools")
def tools():
    return render_template("tools.jinja")
