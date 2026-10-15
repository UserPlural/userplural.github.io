#!/usr/bin/env python3
"""Check this static site's local links and project-path compatibility, offline."""

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_FILES = (
    "index.html", "assets/styles.css", "assets/site.js", "assets/favicon.svg"
)
errors = []


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.viewport = False
        self.has_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        for attribute in ("href", "src"):
            if attribute in attrs:
                self.links.append((attrs[attribute], f"<{tag}> {attribute}"))
        if tag == "meta" and attrs.get("name") == "viewport":
            self.viewport = True
        if tag == "title":
            self.has_title = True
        if tag == "img" and "alt" not in attrs:
            errors.append("Image missing an alt attribute")


def check_url(value, origin, label, ids=None):
    if not value or value == "#":
        errors.append(f"{label}: empty or placeholder destination")
        return
    url = urlsplit(value)
    if url.scheme in ("javascript", "vbscript"):
        errors.append(f"{label}: executable URL is not a destination")
        return
    if url.scheme == "data":
        return
    if url.netloc:
        host = (url.hostname or "").lower()
        if host in ("example.com", "example.org", "example.net", "localhost"):
            errors.append(f"{label}: placeholder URL {value}")
        if host == "mail.google.com":
            errors.append(f"{label}: private correspondence URL in public site")
        return
    if url.scheme:
        return  # e.g. mailto:; external services are not checked offline.
    if url.path.startswith("/"):
        errors.append(f"{label}: root-relative path breaks repository subpaths: {value}")
        return
    target = (origin.parent / unquote(url.path)).resolve() if url.path else origin
    try:
        target.relative_to(ROOT)
    except ValueError:
        errors.append(f"{label}: path leaves site directory: {value}")
        return
    if not target.exists():
        errors.append(f"{label}: missing local file: {value}")
    if url.fragment and target == ROOT / "index.html" and ids is not None:
        if unquote(url.fragment) not in ids:
            errors.append(f"{label}: missing section: {value}")


for name in PUBLIC_FILES:
    if not (ROOT / name).is_file():
        errors.append(f"Missing public file: {name}")

html_path = ROOT / "index.html"
if html_path.is_file():
    page = Page()
    page.feed(html_path.read_text(encoding="utf-8"))
    errors.extend(f"Duplicate section id: {key}" for key, n in Counter(page.ids).items() if n > 1)
    if not page.viewport:
        errors.append("Missing viewport meta tag")
    if not page.has_title:
        errors.append("Missing page title")
    for value, label in page.links:
        check_url(value, html_path, label, set(page.ids))

css_path = ROOT / "assets/styles.css"
if css_path.is_file():
    css = css_path.read_text(encoding="utf-8")
    for match in re.finditer(r"url\(\s*(['\"]?)(.*?)\1\s*\)", css):
        check_url(match.group(2), css_path, "CSS url()")

if errors:
    print("Site checks failed:")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)

print("PASS: required files, local assets, section anchors, and relative paths.")
print("This check does not verify external URLs or confirm workshop facts.")
