# Copyright (C) 2024 jmh
# SPDX-License-Identifier: GPL-3.0-only

import re

import requests
import mistune

from flask import Blueprint, render_template, current_app
from mistune import HTMLRenderer

from stratum import cache


class WikiRenderer(HTMLRenderer):
    def link(self, text, url, title=None):
        if title is not None:
            return f'<a href="{mistune.escape_url(url)}" title="{mistune.escape(title)}" rel="nofollow noopener">{mistune.escape(text)}</a>'
        else:
            return f'<a href="{mistune.escape_url(url)}" rel="nofollow noopener">{mistune.escape(text)}</a>'


bp = Blueprint("wiki", __name__)
markdown = mistune.create_markdown(renderer=WikiRenderer(), plugins=["table"])


@cache.cached(timeout=21600)
def _get_wiki_page(file_name: str) -> str:
    file_url = current_app.config["WIKI_FILE_URL"] + "/" + file_name
    res = requests.get(file_url)
    res.raise_for_status()
    return markdown(res.text)


@cache.cached(timeout=21600)
def _get_markdown_file(file_name: str) -> str:
    file_url = current_app.config["MARKDOWN_FILE_URL"] + "/" + file_name
    res = requests.get(file_url)
    res.raise_for_status()
    text = re.sub(r"# (.*)\n", "", res.text)
    return markdown(text)


@bp.get("/wiki")
def index():
    return render_template("wiki/index.jinja")


@bp.get("/wiki/faq")
def faq():
    return render_template(
        "wiki/page.jinja",
        title="F.A.Q.",
        description="Questions and answers for frequently asked questions",
        content=_get_wiki_page("Frequently-Asked-Questions.md"),
    )


@bp.get("/wiki/backup-format")
def backup_format():
    return render_template(
        "wiki/page.jinja",
        title="Backup Format",
        description="File format and encryption for Stratum backup files",
        content=_get_markdown_file("doc/BACKUP_FORMAT.md"),
    )


@bp.get("/wiki/import-from-google-authenticator")
def google_authenticator():
    return render_template(
        "wiki/page.jinja",
        title="Import from Google Authenticator",
        description="Here's how to transfer your accounts from Google Authenticator to Stratum",
        content=_get_wiki_page("Importing-from-Google-Authenticator.md"),
    )


@bp.get("/wiki/import-from-authy")
def authy():
    return render_template(
        "wiki/page.jinja",
        title="Import from Authy",
        description="Here's how to transfer your accounts from Authy to Stratum",
        content=_get_wiki_page("Importing-from-Authy.md"),
    )


@bp.get("/wiki/import-from-blizzard-authenticator")
def blizzard_authenticator():
    return render_template(
        "wiki/page.jinja",
        title="Import from Blizzard Authenticator",
        description="Here's how to transfer your accounts from Blizzard Authenticator to Stratum",
        content=_get_wiki_page("Importing-from-Blizzard-Authenticator.md"),
    )


@bp.get("/wiki/import-from-steam")
def steam():
    return render_template(
        "wiki/page.jinja",
        title="Import from Steam",
        description="Here's how to transfer your accounts from Steam to Stratum",
        content=_get_wiki_page("Importing-from-Steam.md"),
    )
