#!/usr/bin/env python3
"""Fetch each post's source_url and update source_title to match the page <title>.

Usage:
    python scripts/update_source_titles.py [--dry-run]

By default it rewrites files in place. Use --dry-run to only report differences.
"""
from __future__ import annotations

import argparse
import html
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "_posts"


TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", flags=re.I | re.S)
OG_TITLE_RE = re.compile(
    r"<meta[^>]+property=['\"]og:title['\"][^>]+content=['\"](.*?)['\"]",
    flags=re.I | re.S,
)


# Common phrases that sometimes leak into <title> from consent or banner markup.
TITLE_NOISE_PATTERNS = [
    r"\bclose\s+banner\b",
    r"\bclose\s+this\s+banner\b",
    r"\bclose\s+this\s+(message|window)\b",
    r"\bopen\s+menu\b",
    r"\bopen\s+navigation\b",
    r"\bskip\s+to\s+content\b",
    r"\bskip\s+to\s+main\s+content\b",
    r"\bmanage\s+cookies\b",
    r"\baccept\s+all\s+cookies\b",
    r"\breject\s+all\s+cookies\b",
]


def _clean_html_text(raw: str) -> str:
    cleaned = html.unescape(raw)
    return " ".join(cleaned.split())


def _normalize_title(raw: str) -> str:
    """Normalize and de-noise a raw HTML title string."""
    text = _clean_html_text(raw)
    for pattern in TITLE_NOISE_PATTERNS:
        text = re.sub(pattern, " ", text, flags=re.I)
    text = re.sub(r"\s{2,}", " ", text).strip(" |:-")
    return text


def extract_front_matter(text: str) -> Optional[Tuple[str, str]]:
    """Return (front_matter_yaml, body) if delimiters are present, else None."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, flags=re.S)
    if not match:
        return None
    return match.group(1), match.group(2)


def fetch_title(url: str, timeout: float = 10.0) -> Optional[str]:
    try:
        resp = requests.get(url, timeout=timeout, headers={"User-Agent": "source-title-updater/1.0"})
        resp.raise_for_status()
    except Exception as exc:  # noqa: BLE001
        print(f"[error] {url} -> {exc}")
        return None

    # Respect encoding detected by requests; fall back to utf-8.
    resp.encoding = resp.encoding or "utf-8"
    html_text = resp.text

    # Try the <title> tag inside <head>. Restricting to <head> avoids grabbing stray
    # "<title>" strings that appear in inline scripts or unclosed tags.
    head_match = re.search(r"<head[^>]*>(.*?)</head>", html_text, flags=re.I | re.S)
    head = head_match.group(1) if head_match else html_text[:50000]

    title_match = TITLE_RE.search(head)
    if title_match:
        title = _normalize_title(title_match.group(1))
        if title:
            return title

    og_match = OG_TITLE_RE.search(head)
    if og_match:
        title = _normalize_title(og_match.group(1))
        if title:
            return title

    print(f"[error] failed to parse title for {url}: no <title> or og:title found")
    return None


@dataclass
class UpdateResult:
    path: Path
    old_title: Optional[str]
    new_title: Optional[str]
    changed: bool
    skipped_reason: Optional[str] = None


def update_file(path: Path, dry_run: bool = False, pause: float = 0.0) -> UpdateResult:
    text = path.read_text(encoding="utf-8")
    split = extract_front_matter(text)
    if split is None:
        return UpdateResult(path, None, None, False, "no front matter")

    fm_text, body = split
    try:
        frontmatter = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError as exc:
        return UpdateResult(path, None, None, False, f"bad yaml: {exc}")

    source_url = frontmatter.get("source_url")
    if not source_url:
        return UpdateResult(path, None, None, False, "missing source_url")

    fetched_title = fetch_title(source_url)
    if pause:
        time.sleep(pause)

    if not fetched_title:
        return UpdateResult(path, frontmatter.get("source_title"), None, False, "no title fetched")

    current_title = frontmatter.get("source_title")
    if current_title == fetched_title:
        return UpdateResult(path, current_title, fetched_title, False, "up-to-date")

    frontmatter["source_title"] = fetched_title
    new_fm = yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True).strip() + "\n"
    new_text = f"---\n{new_fm}---\n{body}"
    if not new_text.endswith("\n"):
        new_text += "\n"

    if not dry_run:
        path.write_text(new_text, encoding="utf-8")

    return UpdateResult(path, current_title, fetched_title, True, None)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Update source_title fields from source_url titles.")
    parser.add_argument("--dry-run", action="store_true", help="only report changes, do not rewrite files")
    parser.add_argument("--pause", type=float, default=0.1, help="seconds to pause between requests")
    args = parser.parse_args(argv)

    md_files = sorted(POSTS_DIR.glob("*.md"))
    results: list[UpdateResult] = []

    for path in md_files:
        result = update_file(path, dry_run=args.dry_run, pause=args.pause)
        results.append(result)
        if result.changed:
            print(f"[updated] {path.relative_to(ROOT)}: '{result.old_title}' -> '{result.new_title}'")
        else:
            reason = result.skipped_reason or "no change"
            print(f"[skip] {path.relative_to(ROOT)} ({reason})")

    changed = sum(1 for r in results if r.changed)
    failed = sum(1 for r in results if r.skipped_reason not in (None, "up-to-date"))
    print(f"\nSummary: {changed} updated, {len(md_files) - changed} untouched, {failed} with issues")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
