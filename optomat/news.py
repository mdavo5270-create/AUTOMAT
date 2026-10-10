"""Posts d'actualité depuis plusieurs flux RSS (tech, crypto, monde)."""
from __future__ import annotations

import json
import os
import random
from pathlib import Path

import feedparser

from optomat.human import humanize_text
from optomat.experiments import log_event

CACHE = Path("data/posted_news.json")

DEFAULT_FEEDS = [
    ("tech", "https://hnrss.org/frontpage"),
    ("crypto", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
    ("world", "https://feeds.bbci.co.uk/news/world/rss.xml"),
    ("tech2", "https://www.theverge.com/rss/index.xml"),
]


def _cache() -> set:
    if CACHE.exists():
        return set(json.loads(CACHE.read_text(encoding="utf-8")))
    return set()


def _save(c: set):
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(list(c)[-500:], indent=2), encoding="utf-8")


def post_news(client, max_posts: int = 1):
    feeds_env = os.getenv("NEWS_FEEDS", "")
    if feeds_env.strip():
        feeds = []
        for part in feeds_env.split(";"):
            part = part.strip()
            if not part:
                continue
            if "|" in part:
                tag, url = part.split("|", 1)
                feeds.append((tag.strip(), url.strip()))
            else:
                feeds.append(("news", part))
    else:
        feeds = DEFAULT_FEEDS

    random.shuffle(feeds)
    cache = _cache()
    posted = 0

    for tag, url in feeds:
        if posted >= max_posts:
            break
        try:
            feed = feedparser.parse(url)
        except Exception as e:
            print(f"news feed error {url}: {e}")
            continue
        for entry in (feed.entries or [])[:8]:
            if posted >= max_posts:
                break
            link = entry.get("link") or entry.get("id")
            if not link or link in cache:
                continue
            title = (entry.get("title") or "Actu").strip()
            # post style humain
            templates = [
                f"{title}\n\n{link}",
                f"À lire : {title}\n{link}",
                f"{title}\n\nSource : {link}",
            ]
            text = humanize_text(random.choice(templates))
            if len(text) > 300:
                text = title[:120] + "\n" + link
                text = text[:300]
            try:
                client.send_post(text=text)
                cache.add(link)
                posted += 1
                print(f"news [{tag}]: {title[:60]}")
                log_event("news", {"tag": tag, "title": title[:120], "link": link})
            except Exception as e:
                print(f"news post fail: {e}")

    _save(cache)
    print(f"news: {posted} post(s)")
