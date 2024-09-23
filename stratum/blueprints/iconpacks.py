# Copyright (C) 2024 jmh
# SPDX-License-Identifier: GPL-3.0-only

import shutil
import tempfile

import requests

from flask import Blueprint, current_app, render_template

from stratum import cache
from stratum.models.iconpack import IconPack
from stratum.models import icon_pack_pb2

bp = Blueprint("iconpacks", __name__)


def _get_latest_release() -> dict:
    release_info_url = current_app.config["ICON_PACK_RELEASE_INFO_URL"]
    res = requests.get(release_info_url)
    res.raise_for_status()
    return res.json()


@cache.cached(timeout=86400)
def _get_icon_packs() -> list[IconPack]:
    release = _get_latest_release()
    packs = []

    for asset in release["assets"]:
        url = asset["browser_download_url"]

        with tempfile.TemporaryFile("rb+") as file:
            with requests.get(url, stream=True) as res:
                res.raise_for_status()
                shutil.copyfileobj(res.raw, file)

            file.flush()
            file.seek(0)

            proto = icon_pack_pb2.IconPack()
            proto.ParseFromString(file.read())

            pack = IconPack(
                proto.name,
                proto.description,
                url,
                asset["download_count"],
                len(proto.icons),
            )

            packs.append(pack)

    return packs


@bp.get("/icon-packs")
def tools():
    return render_template("iconpacks.jinja", packs=_get_icon_packs())
