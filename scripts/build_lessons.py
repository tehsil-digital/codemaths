#!/usr/bin/env python3
"""Regenerate site/index.html's lesson cards and JSON-LD from lessons/*.md.

Each lesson is one Markdown file in lessons/ with YAML frontmatter for
metadata and a plain-text description as the body. Run this after adding,
editing, or removing a lesson file:

    python3 scripts/build_lessons.py

It rewrites only the generated regions of site/index.html (between
LESSON_CARDS markers, and inside the ld+json script block) — nothing else
in index.html, css/, or js/ is touched.
"""

import html
import json
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
LESSONS_DIR = REPO_ROOT / "lessons"
INDEX_HTML = REPO_ROOT / "site" / "index.html"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?\n)---\s*\n(.*)$", re.DOTALL)
CARDS_MARKER_RE = re.compile(
    r"<!-- LESSON_CARDS:START -->.*?<!-- LESSON_CARDS:END -->", re.DOTALL
)
JSONLD_RE = re.compile(
    r'<script type="application/ld\+json">.*?</script>', re.DOTALL
)

CARD_TEMPLATE = """      <li class="lesson-card group flex flex-col overflow-hidden rounded-2xl border border-slate-800 bg-slate-900 transition hover:-translate-y-0.5 hover:border-indigo-500/40 hover:shadow-xl hover:shadow-indigo-950/40">
        <a class="relative block aspect-video overflow-hidden bg-black" href="{watch_url}" target="_blank" rel="noopener">
          <img class="h-full w-full object-cover opacity-90 transition duration-300 group-hover:scale-105 group-hover:opacity-100"
               src="{thumbnail_url}" alt="Video thumbnail for {title}" loading="lazy" width="480" height="360">
          <span class="absolute inset-0 flex items-center justify-center bg-slate-950/10 opacity-0 transition group-hover:opacity-100" aria-hidden="true">
            <span class="flex h-12 w-12 items-center justify-center rounded-full bg-white/95 text-slate-900 shadow-lg">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 translate-x-0.5" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
            </span>
          </span>
        </a>
        <div class="flex flex-1 flex-col gap-3 p-5">
          <h2 class="text-lg font-semibold leading-snug text-white">
            <a class="transition hover:text-indigo-400" href="{watch_url}" target="_blank" rel="noopener">{title}</a>
          </h2>
          <p class="line-clamp-2 text-sm text-slate-400">{description}</p>
          <ul class="flex flex-wrap gap-2">
{tags_html}
          </ul>
          <div class="mt-auto flex flex-wrap gap-2 pt-2">
            <a class="inline-flex items-center gap-1.5 rounded-lg bg-indigo-500 px-3 py-1.5 text-sm font-medium text-white transition hover:bg-indigo-400" href="{watch_url}" target="_blank" rel="noopener">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
              Watch on YouTube
            </a>{repo_link}
          </div>
        </div>
      </li>"""

REPO_LINK_TEMPLATE = """
            <a class="inline-flex items-center gap-1.5 rounded-lg border border-slate-700 px-3 py-1.5 text-sm font-medium text-slate-300 transition hover:border-slate-600 hover:text-white" href="{repo_url}" target="_blank" rel="noopener">
              Code repo
            </a>"""

TAG_TEMPLATE = '            <li class="rounded-full border border-slate-700 bg-slate-800/70 px-2.5 py-0.5 text-xs text-slate-400">{tag}</li>'


def load_lessons():
    lessons = []
    for path in sorted(LESSONS_DIR.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(raw)
        if not match:
            raise ValueError(f"{path}: missing '---' frontmatter delimiters")

        front = yaml.safe_load(match.group(1)) or {}
        description = match.group(2).strip()

        for field in ("title", "youtube_id"):
            if not front.get(field):
                raise ValueError(f"{path}: missing required frontmatter field '{field}'")
        if not description:
            raise ValueError(f"{path}: description body is empty")

        lessons.append(
            {
                "slug": path.stem,
                "title": str(front["title"]),
                "youtube_id": str(front["youtube_id"]),
                "tags": [str(t) for t in (front.get("tags") or [])],
                "repo_url": front.get("repo_url"),
                "description": description,
            }
        )
    return lessons


def render_card(lesson):
    tags_html = "\n".join(TAG_TEMPLATE.format(tag=html.escape(tag)) for tag in lesson["tags"])
    repo_link = (
        REPO_LINK_TEMPLATE.format(repo_url=html.escape(lesson["repo_url"]))
        if lesson["repo_url"]
        else ""
    )
    watch_url = f"https://www.youtube.com/watch?v={lesson['youtube_id']}"
    thumbnail_url = f"https://i.ytimg.com/vi/{lesson['youtube_id']}/hqdefault.jpg"
    return CARD_TEMPLATE.format(
        watch_url=html.escape(watch_url),
        thumbnail_url=html.escape(thumbnail_url),
        title=html.escape(lesson["title"]),
        description=html.escape(lesson["description"]),
        tags_html=tags_html,
        repo_link=repo_link,
    )


def build_jsonld(lessons):
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Lean 4 Lessons",
        "description": "Video lessons on Lean 4 and formal theorem proving for undergraduate students.",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i,
                "name": lesson["title"],
                "url": f"https://www.youtube.com/watch?v={lesson['youtube_id']}",
            }
            for i, lesson in enumerate(lessons, start=1)
        ],
    }


def replace_cards(html_text, lessons):
    cards_html = "\n\n".join(render_card(lesson) for lesson in lessons)
    replacement = "<!-- LESSON_CARDS:START -->\n" + cards_html + "\n<!-- LESSON_CARDS:END -->"
    if not CARDS_MARKER_RE.search(html_text):
        raise ValueError("LESSON_CARDS:START/END markers not found in site/index.html")
    return CARDS_MARKER_RE.sub(lambda m: replacement, html_text, count=1)


def replace_jsonld(html_text, lessons):
    payload = json.dumps(build_jsonld(lessons), indent=2)
    replacement = '<script type="application/ld+json">\n' + payload + "\n  </script>"
    if not JSONLD_RE.search(html_text):
        raise ValueError('could not find <script type="application/ld+json"> block in site/index.html')
    return JSONLD_RE.sub(lambda m: replacement, html_text, count=1)


def main():
    lessons = load_lessons()
    if not lessons:
        print("No lessons found in lessons/*.md", file=sys.stderr)
        sys.exit(1)

    html_text = INDEX_HTML.read_text(encoding="utf-8")
    html_text = replace_cards(html_text, lessons)
    html_text = replace_jsonld(html_text, lessons)
    INDEX_HTML.write_text(html_text, encoding="utf-8")

    print(f"Regenerated {len(lessons)} lesson card(s) into {INDEX_HTML.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
