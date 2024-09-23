# Copyright (C) 2024 jmh
# SPDX-License-Identifier: GPL-3.0-only

from . import BaseConfig


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
    MAIL_RECIPIENT = "test@example.com"
    MAIL_DEFAULT_SENDER = "test@example.com"
