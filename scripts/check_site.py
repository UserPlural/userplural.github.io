#!/usr/bin/env python3
"""Validate the workshop's static pages and local links, without dependencies."""

from collections import Counter
from datetime import date
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import parse_qs, unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    "index.html", "themes.html", "cfp.html", "dates.html",
    "submissions.html", "program.html", "organizers.html", "contact.html",
)
PUBLIC_FILES = PAGES + ("assets/styles.css", "assets/favicon.svg", ".nojekyll")
OFFICIAL_EMAIL = "theuserplural@gmail.com"
EMAIL = re.compile(r"[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}", re.I)
errors = []


class Page(HTMLParser):
    def __init__(self, name):
        super().__init__(convert_charrefs=True)
        self.name = name
        self.ids = []
        self.links = []
        self.viewport = False
        self.titles = []
        self._title = None
        self.main_count = 0
        self.h1_count = 0
        self.h1_text = []
        self._in_h1 = False
        self.navs = []
        self._nav_stack = []
        self.table_rows = []
        self._row = None
        self._cell = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            if attrs["id"]:
                self.ids.append(attrs["id"])
            else:
                errors.append(f"{self.name}: empty id attribute")
        for attribute in ("href", "src", "poster"):
            if attribute in attrs:
                self.links.append((attrs[attribute], f"<{tag}> {attribute}"))
        if tag == "meta" and attrs.get("name", "").lower() == "viewport":
            self.viewport = bool(re.search(
                r"(?:^|[,;\s])width\s*=\s*device-width(?:$|[,;\s])",
                attrs.get("content", ""), re.I,
            ))
        if tag == "title":
            self._title = []
        if tag == "main":
            self.main_count += 1
        if tag == "h1":
            self.h1_count += 1
            self._in_h1 = True
        if tag == "nav":
            nav = {"links": [], "label": attrs.get("aria-label", "")}
            self.navs.append(nav)
            self._nav_stack.append(nav)
        if tag == "a" and self._nav_stack:
            self._nav_stack[-1]["links"].append(attrs)
        if tag == "tr":
            self._row = []
        if tag in ("th", "td") and self._row is not None:
            self._cell = {"tag": tag, "text": [], "datetimes": []}
            self._row.append(self._cell)
        if tag == "time" and self._cell is not None and attrs.get("datetime"):
            self._cell["datetimes"].append(attrs["datetime"])
        if tag == "img" and "alt" not in attrs:
            errors.append(f"{self.name}: image missing an alt attribute")

    def handle_data(self, data):
        if self._title is not None:
            self._title.append(data)
        if self._in_h1:
            self.h1_text.append(data)
        if self._cell is not None:
            self._cell["text"].append(data)

    def handle_endtag(self, tag):
        if tag == "title" and self._title is not None:
            self.titles.append(" ".join("".join(self._title).split()))
            self._title = None
        if tag == "h1":
            self._in_h1 = False
        if tag == "nav" and self._nav_stack:
            self._nav_stack.pop()
        if tag in ("th", "td"):
            self._cell = None
        if tag == "tr" and self._row is not None:
            self.table_rows.append(self._row)
            self._row = None


parsed = {}


def read_page(path):
    if path not in parsed:
        name = str(path.relative_to(ROOT))
        page = Page(name)
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{name}: cannot read file: {exc}")
            return None
        page.feed(content)
        page.close()
        parsed[path] = page
        for value, count in Counter(page.ids).items():
            if count > 1:
                errors.append(f"{name}: duplicate id: {value}")
        # Also catch addresses written as text, encoded entities, or URL parameters.
        for address in sorted(set(EMAIL.findall(unquote(unescape(content))))):
            if address.lower() != OFFICIAL_EMAIL:
                errors.append(f"{name}: non-official email address: {address}")
    return parsed[path]


def local_target(url, origin):
    path = unquote(url.path)
    if path.startswith("/") or "\\" in path:
        raise ValueError("use a relative path within the site")
    target = (origin.parent / path).resolve() if path else origin
    try:
        target.relative_to(ROOT)
    except ValueError:
        raise ValueError("path leaves the public site directory") from None
    if target.is_dir():
        target /= "index.html"
    return target


def check_url(value, origin, context):
    label = f"{origin.relative_to(ROOT)} {context}"
    if not value or value.strip() in ("", "#"):
        errors.append(f"{label}: empty or placeholder destination")
        return
    value = value.strip()
    try:
        url = urlsplit(value)
    except ValueError as exc:
        errors.append(f"{label}: invalid URL {value!r}: {exc}")
        return
    if url.scheme.lower() in ("javascript", "vbscript"):
        errors.append(f"{label}: executable URL is not a destination")
        return
    if url.scheme.lower() == "mailto":
        if unquote(url.path).lower() != OFFICIAL_EMAIL:
            errors.append(f"{label}: mailto must address {OFFICIAL_EMAIL}")
        for key, values in parse_qs(url.query).items():
            if key.lower() in ("to", "cc", "bcc"):
                for recipient in values:
                    if recipient.lower() != OFFICIAL_EMAIL:
                        errors.append(f"{label}: non-official mail recipient")
        return
    if url.scheme.lower() == "data":
        return
    if url.netloc:
        host = (url.hostname or "").lower().rstrip(".")
        dummy_hosts = ("example.com", "example.org", "example.net", "localhost")
        if (any(host == item or host.endswith("." + item) for item in dummy_hosts)
                or host.endswith((".invalid", ".test"))
                or host in ("127.0.0.1", "0.0.0.0", "::1")
                or re.search(r"(?:^|/)(?:OWNER|REPOSITORY|YOUR[-_]?[A-Z_]+)(?:/|$)", url.path)):
            errors.append(f"{label}: placeholder URL: {value}")
        if host == "mail.google.com":
            errors.append(f"{label}: private correspondence URL in public site")
        return  # External services are not contacted by this offline check.
    if url.scheme:
        errors.append(f"{label}: unsupported destination scheme: {url.scheme}")
        return
    try:
        target = local_target(url, origin)
    except ValueError as exc:
        errors.append(f"{label}: {exc}: {value}")
        return
    if not target.is_file():
        errors.append(f"{label}: missing local file: {value}")
        return
    if url.fragment and target.suffix.lower() in (".html", ".htm", ".svg"):
        destination = read_page(target)
        fragment = unquote(url.fragment)
        if destination and fragment not in destination.ids:
            errors.append(f"{label}: missing destination id: {value}")


def nav_destination(attrs, origin):
    value = attrs.get("href", "")
    try:
        url = urlsplit(value)
        if not value or url.scheme or url.netloc or url.fragment or url.query:
            return None
        # Page navigation must name the page, rather than link to an empty path.
        if not url.path:
            return None
        return local_target(url, origin)
    except ValueError:
        return None


def check_navigation(page, origin):
    expected = {ROOT / name for name in PAGES}
    candidates = []
    for nav in page.navs:
        destinations = [nav_destination(link, origin) for link in nav["links"]]
        if expected.issubset(set(destinations)):
            candidates.append((nav, destinations))
    if not candidates:
        errors.append(f"{page.name}: navigation must link to all eight local HTML pages")
        return
    nav, destinations = candidates[0]
    for target, count in Counter(destinations).items():
        if target in expected and count > 1:
            errors.append(f"{page.name}: repeated page in navigation: {target.name}")
    current = [link for link in nav["links"] if link.get("aria-current") not in (None, "false")]
    if len(current) != 1:
        errors.append(f"{page.name}: navigation needs exactly one aria-current=\"page\" link")
    elif current[0].get("aria-current") != "page" or nav_destination(current[0], origin) != origin:
        errors.append(f"{page.name}: aria-current=\"page\" must identify this page")


def check_dates(page):
    """Dates use valid machine-readable values; unannounced items remain TBD/TBA."""
    rows = [row for row in page.table_rows if any(cell["tag"] == "td" for cell in row)]
    if not rows:
        errors.append("dates.html: missing milestone table")
        return
    for row in rows:
        if len(row) < 2:
            errors.append("dates.html: milestone row needs an event and date")
            continue
        event = " ".join("".join(row[0]["text"]).split())
        value = " ".join("".join(row[1]["text"]).split())
        datetimes = row[1]["datetimes"]
        if value.upper() in ("TBD", "TBA"):
            if datetimes:
                errors.append(f"dates.html: unannounced milestone has a date: {event}")
            continue
        if not datetimes:
            errors.append(f"dates.html: announced date needs a time element: {event}")
        for stamp in datetimes:
            try:
                date.fromisoformat(stamp)
            except ValueError:
                errors.append(f"dates.html: invalid date {stamp!r}: {event}")


for name in PUBLIC_FILES:
    if not (ROOT / name).is_file():
        errors.append(f"Missing public file: {name}")

# Parse every page before checking links, so cross-page fragments are available.
for name in PAGES:
    path = ROOT / name
    if path.is_file():
        read_page(path)

titles = {}
for name in PAGES:
    path = ROOT / name
    page = parsed.get(path)
    if page is None:
        continue
    if not page.viewport:
        errors.append(f"{name}: missing width=device-width viewport meta tag")
    if len(page.titles) != 1 or not page.titles[0]:
        errors.append(f"{name}: needs one nonempty title")
    else:
        title_key = page.titles[0].casefold()
        if title_key in titles:
            errors.append(f"{name}: title duplicates {titles[title_key]}; use a page-specific title")
        titles[title_key] = name
    if page.main_count != 1:
        errors.append(f"{name}: expected one main element, found {page.main_count}")
    if page.h1_count != 1 or not "".join(page.h1_text).strip():
        errors.append(f"{name}: needs one nonempty h1")
    check_navigation(page, path)
    if name == "dates.html":
        check_dates(page)
    for value, context in page.links:
        check_url(value, path, context)
    if name == "contact.html":
        if not any(value and value.lower().startswith("mailto:" + OFFICIAL_EMAIL)
                   for value, _ in page.links):
            errors.append(f"{name}: missing official contact mailto link")

# Validate CSS file references as well as HTML references.
for css_path in sorted((ROOT / "assets").rglob("*.css")):
    try:
        css = css_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"{css_path.relative_to(ROOT)}: cannot read CSS: {exc}")
        continue
    for match in re.finditer(r"url\(\s*(['\"]?)(.*?)\1\s*\)", css, re.I):
        check_url(match.group(2), css_path, "CSS url()")
    for match in re.finditer(r"@import\s+(['\"])(.*?)\1", css, re.I):
        check_url(match.group(2), css_path, "CSS @import")

if errors:
    print("Site checks failed:")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)

print("PASS: eight pages, unique titles, landmarks, navigation, official contact,")
print("      local assets, cross-page fragments, relative paths, and milestone dates.")
print("This check does not verify external URLs or confirm workshop facts.")
