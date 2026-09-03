#!/usr/bin/env python3
"""Small dependency-free integrity check for the static site."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1] / "site"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.refs = []
        self.images_without_alt = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            self.ids.append(attributes["id"])
        if tag in {"a", "link"} and "href" in attributes:
            self.refs.append(attributes["href"])
        if tag in {"img", "script"} and "src" in attributes:
            self.refs.append(attributes["src"])
        if tag == "img" and "alt" not in attributes:
            self.images_without_alt.append(attributes.get("src", "<unknown>"))


def check_page(path: Path):
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    errors = []

    duplicates = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
    if duplicates:
        errors.append(f"duplicate ids: {', '.join(duplicates)}")
    if parser.images_without_alt:
        errors.append(f"images missing alt: {', '.join(parser.images_without_alt)}")

    ids = set(parser.ids)
    for ref in parser.refs:
        parsed = urlparse(ref)
        if parsed.scheme in {"http", "https", "mailto", "tel", "data"}:
            continue
        if ref.startswith("#"):
            if ref[1:] not in ids:
                errors.append(f"missing fragment target: {ref}")
            continue
        target = (path.parent / parsed.path).resolve()
        try:
            target.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"reference escapes site root: {ref}")
            continue
        if parsed.path and not target.exists():
            errors.append(f"missing local reference: {ref}")

    return errors


def main():
    failures = []
    pages = sorted(ROOT.glob("*.html"))
    for page in pages:
        errors = check_page(page)
        failures.extend(f"{page.name}: {error}" for error in errors)

    if failures:
        print("Site checks failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print(f"Site checks passed for {len(pages)} HTML pages.")


if __name__ == "__main__":
    main()
