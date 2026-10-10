"""Publier un flux RSS sur Bluesky (code adapté de joschi/blueskyfeedbot + feedparser)
Usage: python -m automat.rss --feed URL --max 2
"""
import argparse
import json
from pathlib import Path
import feedparser
from automat.client import get_client

CACHE_FILE = Path("data/posted_rss.json")

def load_cache() -> set:
    if CACHE_FILE.exists():
        return set(json.loads(CACHE_FILE.read_text(encoding="utf-8")))
    return set()

def save_cache(cache: set):
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(list(cache), indent=2), encoding="utf-8")

def post_from_rss(feed_url: str, max_posts: int = 2):
    client = get_client()
    feed = feedparser.parse(feed_url)
    if not feed.entries:
        print("Aucun article dans le flux.")
        return

    cache = load_cache()
    posted = 0
    for entry in feed.entries[:15]:
        link = entry.get("link") or entry.get("id")
        if not link or link in cache:
            continue
        title = (entry.get("title") or "Sans titre").strip()
        text = f"{title}\n\n{link}"
        if len(text) > 300:
            text = text[:297] + "..."
        try:
            client.send_post(text=text)
            cache.add(link)
            posted += 1
            print(f"Publié: {title[:70]}")
            if posted >= max_posts:
                break
        except Exception as e:
            print(f"Erreur: {e}")
    save_cache(cache)
    print(f"Terminé. {posted} post(s).")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--feed", default="https://www.githubstatus.com/history.rss")
    parser.add_argument("--max", type=int, default=2)
    args = parser.parse_args()
    post_from_rss(args.feed, args.max)

if __name__ == "__main__":
    main()
