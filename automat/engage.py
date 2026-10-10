"""
Module d'engagement
Like / Repost des posts contenant certains mots-clés.

Usage:
  python -m automat.engage
"""

import yaml
from pathlib import Path
from automat.client import get_client
from rich.console import Console

console = Console()
CONFIG_FILE = Path("config/engage.yaml")


def load_config():
    if not CONFIG_FILE.exists():
        # Config par défaut
        return {
            "keywords": ["python", "automatisation", "bluesky", "open source"],
            "actions": {"like": True, "repost": False},
            "max_per_run": 10,
            "search_limit": 30
        }
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def engage():
    client = get_client()
    config = load_config()

    keywords = config.get("keywords", [])
    do_like = config.get("actions", {}).get("like", True)
    do_repost = config.get("actions", {}).get("repost", False)
    max_actions = config.get("max_per_run", 10)

    actions_done = 0

    for keyword in keywords:
        if actions_done >= max_actions:
            break

        console.print(f"[cyan]Recherche : {keyword}[/cyan]")
        try:
            results = client.app.bsky.feed.search_posts(params={
                "q": keyword,
                "limit": config.get("search_limit", 20)
            })

            for post in results.posts:
                if actions_done >= max_actions:
                    break

                uri = post.uri
                cid = post.cid

                try:
                    if do_like:
                        client.like(uri, cid)
                        console.print(f"  ❤️  Like → {post.author.handle}")
                        actions_done += 1

                    if do_repost and actions_done < max_actions:
                        client.repost(uri, cid)
                        console.print(f"  🔄 Repost → {post.author.handle}")
                        actions_done += 1

                except Exception as e:
                    # déjà liké / rate limit / etc.
                    pass

        except Exception as e:
            console.print(f"[red]Erreur recherche '{keyword}' : {e}[/red]")

    console.print(f"[green]✅ {actions_done} action(s) effectuée(s)[/green]")


def main():
    engage()


if __name__ == "__main__":
    main()
