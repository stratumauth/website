# Copyright (C) 2024 jmh
# SPDX-License-Identifier: GPL-3.0-only

from . import BaseConfig


def _get_secret(name: str) -> str:
    with open(f"/run/secrets/{name}", "r") as file:
        return file.read()


class ProductionConfig(BaseConfig):
    URL = "https://stratumauth.com"
    ALT_URL = "http://www.stratumauth.com"

    VITE_DEV_SERVER = None

    SECRET_KEY = _get_secret("flask_secret_key")

    CACHE_TYPE = "FileSystemCache"
    CACHE_DIR = "/tmp/cache"

    RECAPTCHA_PUBLIC_KEY = "6Le0bZYUAAAAAC9gQDwwwRCEnN8l2rcG-o_kCd95"
    RECAPTCHA_PRIVATE_KEY = _get_secret("recaptcha_private_key")

    MAIL_SERVER = "email-smtp.eu-central-1.amazonaws.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = _get_secret("mail_username")
    MAIL_PASSWORD = _get_secret("mail_password")
    MAIL_RECIPIENT = _get_secret("mail_recipient")
    MAIL_DEFAULT_SENDER = _get_secret("mail_recipient")
