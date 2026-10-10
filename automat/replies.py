"""Réponses automatiques aux mentions
Usage: python -m automat.replies
"""
import random
from atproto import models
from automat.client import get_client

REPLIES = [
    "Merci pour le message ! 🐛",
    "Hello ! Merci de m'avoir mentionné 😊",
    "Salut ! Content de te lire.",
]

def reply_to_mentions(max_replies: int = 5):
    client = get_client()
    notifs = client.app.bsky.notification.list_notifications()
    replied = 0
    my_did = client.me.did

    for notif in notifs.notifications:
        if replied >= max_replies:
            break
        if notif.reason != "mention":
            continue
        if notif.author.did == my_did:
            continue
        try:
            text = random.choice(REPLIES)
            parent = models.ComAtprotoRepoStrongRef.Main(uri=notif.uri, cid=notif.cid)
            client.send_post(
                text=text,
                reply_to=models.AppBskyFeedPost.ReplyRef(parent=parent, root=parent),
            )
            print(f"Répondu à @{notif.author.handle}")
            replied += 1
        except Exception as e:
            print(f"Impossible de répondre à @{notif.author.handle}: {e}")
    print(f"Terminé. {replied} réponse(s).")

def main():
    reply_to_mentions()

if __name__ == "__main__":
    main()
