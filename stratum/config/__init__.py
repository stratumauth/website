# Copyright (C) 2024 jmh
# SPDX-License-Identifier: GPL-3.0-only


class BaseConfig(object):
    APP_RELEASE_INFO_URL = (
        "https://api.github.com/repos/jamie-mh/AuthenticatorPro/releases/latest"
    )
    ICON_PACK_RELEASE_INFO_URL = (
        "https://api.github.com/repos/jamie-mh/AuthenticatorProIcons/releases/latest"
    )
    WIKI_FILE_URL = "https://raw.githubusercontent.com/wiki/jamie-mh/AuthenticatorPro"
    MARKDOWN_FILE_URL = (
        "https://raw.githubusercontent.com/jamie-mh/AuthenticatorPro/master"
    )


class TestingConfig(BaseConfig):
    CACHE_TYPE = "NullCache"


class DevelopmentConfig(BaseConfig):
    SECRET_KEY = "testing"
    CACHE_TYPE = "SimpleCache"

    RECAPTCHA_PUBLIC_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
    RECAPTCHA_PRIVATE_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"

    MAIL_SERVER = "localhost"
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = "username"
    MAIL_PASSWORD = "password"
    MAIL_DEFAULT_SENDER = "test@example.com"
    MAIL_RECIPIENT = "test@example.com"


class ProductionConfig(BaseConfig):
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "redis"
    CACHE_REDIS_PORT = 6379
    # todo recapthca
    # todo secretkey
    # todo mail
