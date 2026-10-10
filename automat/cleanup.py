"""
Module de nettoyage – supprime les vieux posts

Usage:
  python -m automat.cleanup --days 90
"""

import argparse
from datetime import datetime, timezone, timedelta
from automat.client import get_client
from rich.console import Console

console = Console()


def cleanup(days: int = 90, dry_run: bool = True):
    client = get_client()
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    console.print(f"[cyan]Recherche des posts plus vieux que {days} jours...[/cyan]")

    # On récupère le feed de l'utilisateur
    feed = client.get_author_feed(actor=client.me.did, limit=50)

    to_delete = []
    for item in feed.feed:
        post = item.post
        created = datetime.fromisoformat(post.record.created_at.replace("Z", "+00:00"))
        if created < cutoff:
            to_delete.append(post)

    console.print(f"Trouvé {len(to_delete)} post(s) à supprimer.")

    if dry_run:
        console.print("[yellow]Mode dry-run : aucune suppression réelle.[/yellow]")
        for p in to_delete[:5]:
            console.print(f"  - {p.record.text[:60]}...")
        return

    for post in to_delete:
        try:
            client.delete_post(post.uri)
            console.print(f"[green]Supprimé : {post.uri}[/green]")
        except Exception as e:
            console.print(f"[red]Erreur : {e}[/red]")


def main():
    parser = argparse.ArgumentParser(description="Nettoyer les vieux posts")
    parser.add_argument("--days", type=int, default=90, help="Âge minimum en jours")
    parser.add_argument("--confirm", action="store_true", help="Vraiment supprimer (sinon dry-run)")
    args = parser.parse_args()

    cleanup(days=args.days, dry_run=not args.confirm)


if __name__ == "__main__":
    main()
