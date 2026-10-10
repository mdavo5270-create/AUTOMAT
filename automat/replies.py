"""
Module de réponses automatiques aux mentions

Usage:
  python -m automat.replies
"""

from automat.client import get_client
from rich.console import Console

console = Console()

# Réponses possibles (tu peux les personnaliser)
DEFAULT_REPLIES = [
    "Merci pour le message ! 🦋",
    "Hello ! Merci de m'avoir mentionné 😊",
    "Salut ! Content de te lire.",
]


def reply_to_mentions(max_replies: int = 5):
    client = get_client()

    # Récupère les notifications non lues
    notifs = client.app.bsky.notification.list_notifications()

    replied = 0
    for notif in notifs.notifications:
        if replied >= max_replies:
            break

        if notif.reason != "mention":
            continue

        # On évite de répondre à soi-même
        if notif.author.handle == client.me.handle:
            continue

        try:
            # Réponse simple
            import random
            text = random.choice(DEFAULT_REPLIES)

            # On construit la réponse en thread
            parent = {
                "uri": notif.uri,
                "cid": notif.cid
            }
            root = parent  # simplifié

            client.send_post(
                text=text,
                reply_to={
                    "root": root,
                    "parent": parent
                }
            )
            console.print(f"[green]✅ Répondu à @{notif.author.handle}[/green]")
            replied += 1

        except Exception as e:
            console.print(f"[yellow]Impossible de répondre à {notif.author.handle} : {e}[/yellow]")

    console.print(f"[cyan]Terminé. {replied} réponse(s) envoyée(s).[/cyan]")


def main():
    reply_to_mentions()


if __name__ == "__main__":
    main()
