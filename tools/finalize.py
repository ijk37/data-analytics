#!/usr/bin/env python3
"""
finalize.py — make the course markdown safe for the MkDocs site.

Idempotent, so running it repeatedly is safe. It fixes the things that break
the published site (https://ijk37.com/data-analytics/):

  1. Converts raw-HTML nav (<a href="x.md"><img ...></a>, <a href="x.md">text</a>,
     banner <img>) into MARKDOWN links/images so MkDocs rewrites them to .html
     (raw HTML links are NOT rewritten -> they 404 / open .md on the site).
  2. Adds the `markdown` attribute to the centered nav divs so the links inside
     get processed.
  3. Retargets root-home links to index.md (the site excludes README.md because
     it conflicts with index.md), depth-aware.
  4. Points quiz-README links at the quiz hub (03-quiz/README.md -> 03-quiz/),
     since the quiz app's index.html owns that folder.
  5. Ensures the "View the Live Site" badge sits under the banner in every
     README (re-inserts it if a formatting pass strips it).

The 05-resources page lives at 05-resources/README.md (published on the site
and on GitHub); it is maintained by hand, not generated here.

Usage:
    python tools/finalize.py
    python -m mkdocs build     # or: python -m mkdocs serve
"""
import os
import re
import glob

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO)

BANNER_LINKED = re.compile(r'<a href="[^"]*"><img src="([^"]*banner\.svg)" alt="([^"]*)"[^>]*></a>')
BANNER_PLAIN = re.compile(r'<img src="([^"]*banner\.svg)" alt="([^"]*)"[^>]*>')
BADGE_LINK = re.compile(r'<a href="([^"]+)"><img src="([^"]+)" alt="([^"]*)"></a>')
TEXT_LINK = re.compile(r'<a href="([^"]+)">([^<]+)</a>')

LIVE_SITE_BADGE = (
    '[![View the live site — ijk37.com]'
    '(https://img.shields.io/badge/%F0%9F%87%A7%F0%9F%87%A9_View_the_Live_Site-IJK37.COM-F42A41'
    '?style=for-the-badge&labelColor=006A4E)]'
    '(https://ijk37.com/data-analytics/)'
)


def ensure_live_site_badge(s: str) -> str:
    """Insert the flag live-site badge on the line after the banner, once."""
    if 'View_the_Live_Site' in s:
        return s
    lines = s.split('\n')
    out, done = [], False
    for ln in lines:
        out.append(ln)
        if not done and 'banner.svg' in ln:
            out.append('')
            out.append(LIVE_SITE_BADGE)
            done = True
    return '\n'.join(out) if done else s


def convert_nav(s: str) -> str:
    s = BANNER_LINKED.sub(r'![\2](\1)', s)
    s = BANNER_PLAIN.sub(r'![\2](\1)', s)
    s = BADGE_LINK.sub(r'[![\3](\2)](\1)', s)
    s = TEXT_LINK.sub(r'[\2](\1)', s)
    s = s.replace('<div align="center">', '<div align="center" markdown>')
    return s


def fix_file(path: str) -> bool:
    s = open(path, encoding="utf-8").read()
    orig = s
    depth = path.replace("\\", "/").count("/")   # 01-notes/x.md -> 1 ; 04-projects/n/README.md -> 2

    s = convert_nav(s)

    # live-site badge (README pages only)
    if path.replace("\\", "/").endswith("README.md"):
        s = ensure_live_site_badge(s)

    # quiz README -> quiz hub
    s = s.replace("](../../03-quiz/README.md)", "](../../03-quiz/)")
    s = s.replace("](../03-quiz/README.md)", "](../03-quiz/)")
    s = s.replace("](03-quiz/README.md)", "](03-quiz/)")

    # root-home retarget (depth aware)
    if depth >= 2:
        s = s.replace("](../../README.md)", "](../../index.md)")
    else:
        s = s.replace("](../README.md)", "](../index.md)")

    if s != orig:
        open(path, "w", encoding="utf-8", newline="\n").write(s)
        return True
    return False


def main():
    files = (
        glob.glob("01-notes/*.md")
        + glob.glob("02-exercises/*.md")
        + ["04-projects/README.md", "05-resources/README.md"]
        + glob.glob("04-projects/*/README.md")
    )
    changed = sum(fix_file(f) for f in sorted(set(files)) if os.path.exists(f))

    print(f"finalize: fixed {changed} file(s). Now run:  python -m mkdocs build")


if __name__ == "__main__":
    main()
