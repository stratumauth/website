# Copyright (C) 2024 jmh
# SPDX-License-Identifier: GPL-3.0-only

import base64
import shutil
import tempfile
import random

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


def _get_icon_pack_previews(proto: icon_pack_pb2.IconPack) -> list[str]:
    previews = []

    for icon in random.sample(proto.icons, k=14):
        previews.append(base64.b64encode(icon.data).decode("ascii"))

    return previews


def _get_icon_pack_from_asset(asset: dict) -> IconPack:
    url = asset["browser_download_url"]

    with tempfile.TemporaryFile("rb+") as file:
        with requests.get(url, stream=True) as res:
            res.raise_for_status()
            shutil.copyfileobj(res.raw, file)

        file.flush()
        file.seek(0)

        proto = icon_pack_pb2.IconPack()
        proto.ParseFromString(file.read())

        return IconPack(
            name=proto.name,
            description=proto.description,
            download_url=url,
            source_url=proto.url,
            download_count=asset["download_count"],
            icon_count=len(proto.icons),
            previews=_get_icon_pack_previews(proto),
        )


@cache.cached(timeout=86400)
def _get_icon_packs() -> list[IconPack]:
    release = _get_latest_release()
    return [_get_icon_pack_from_asset(a) for a in release["assets"]]


@bp.get("/icon-packs")
def tools():
    return render_template("iconpacks.jinja", packs=_get_icon_packs())
