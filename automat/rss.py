"""
Module RSS → Bluesky
Publie automatiquement les nouveaux articles d'un flux RSS.

Usage:
  python -m automat.rss
  python -m automat.rss --feed https://exemple.com/rss
"""

import argparse
import json
import feedparser
from pathlib import Path
from automat.client import get_client
from rich.console import Console

console = Console()
CACHE_FILE = Path("data/posted_rss.json")


def load_cache() -> set:
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()


def save_cache(cache: set):
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(list(cache), f, indent=2)


def post_from_rss(feed_url: str, max_posts: int = 3):
    client = get_client()
    feed = feedparser.parse(feed_url)

    if not feed.entries:
        console.print("[yellow]Aucun article trouvé dans le flux.[/yellow]")
        return

    cache = load_cache()
    posted = 0

    for entry in feed.entries[:10]:  # on regarde les 10 plus récents
        link = entry.get("link") or entry.get("id")
        if not link or link in cache:
            continue

        title = entry.get("title", "Sans titre").strip()
        text = f"{title}\n\n{link}"

        try:
            client.send_post(text=text)
            cache.add(link)
            posted += 1
            console.print(f"[green]✅ Publié : {title[:60]}...[/green]")

            if posted >= max_posts:
                break
        except Exception as e:
            console.print(f"[red]Erreur sur {title[:40]} : {e}[/red]")

    save_cache(cache)
    console.print(f"[cyan]Terminé. {posted} nouveau(x) post(s).[/cyan]")


def main():
    parser = argparse.ArgumentParser(description="Poster un flux RSS sur Bluesky")
    parser.add_argument("--feed", default="https://www.githubstatus.com/history.rss",
                        help="URL du flux RSS")
    parser.add_argument("--max", type=int, default=2, help="Nombre max de posts par exécution")
    args = parser.parse_args()

    post_from_rss(args.feed, args.max)


if __name__ == "__main__":
    main()
