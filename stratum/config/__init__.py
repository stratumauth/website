# Copyright (C) 2024 jmh
# SPDX-License-Identifier: GPL-3.0-only


class BaseConfig(object):
    APP_RELEASE_INFO_URL = (
        "https://api.github.com/repos/stratumauth/app/releases/latest"
    )
    ICON_PACK_RELEASE_INFO_URL = (
        "https://api.github.com/repos/stratumauth/icons/releases/latest"
    )
    WIKI_FILE_URL = "https://raw.githubusercontent.com/wiki/stratumauth/app"
    MARKDOWN_FILE_URL = "https://raw.githubusercontent.com/stratumauth/app/master"

    RECAPTCHA_DIV_CLASS = "h-captcha"
    RECAPTCHA_SCRIPT = "https://js.hcaptcha.com/1/api.js"
    RECAPTCHA_VERIFY_SERVER = "https://api.hcaptcha.com/siteverify"
