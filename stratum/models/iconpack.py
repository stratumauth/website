# Copyright (C) 2024 jmh
# SPDX-License-Identifier: GPL-3.0-only

from dataclasses import dataclass


@dataclass
class IconPack:
    name: str
    description: str
    download_url: str
    download_count: int
    icon_count: int
