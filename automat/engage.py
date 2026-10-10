"""Engagement (like) basé sur mots-clés — adapté de Endless-Range/bluesky-engagement-bot
Usage: python -m automat.engage
"""
import os
import time
from automat.client import get_client

def engage():
    client = get_client()
    keywords_raw = os.getenv("KEYWORDS", "python,bluesky,automatisation,open source")
    keywords = [k.strip() for k in keywords_raw.split(",") if k.strip()]
    max_actions = int(os.getenv("MAX_ENGAGE_PER_RUN", "8"))
    actions = 0

    for keyword in keywords:
        if actions >= max_actions:
            break
        print(f"Recherche: {keyword}")
        try:
            results = client.app.bsky.feed.search_posts(params={"q": keyword, "limit": 15})
            for post in results.posts:
                if actions >= max_actions:
                    break
                # ignorer les réponses
                if getattr(post.record, "reply", None):
                    continue
                try:
                    client.like(post.uri, post.cid)
                    print(f"  Like -> @{post.author.handle}")
                    actions += 1
                    time.sleep(2)
                except Exception:
                    pass
            time.sleep(1)
        except Exception as e:
            print(f"Erreur recherche '{keyword}': {e}")
    print(f"Terminé. {actions} like(s).")

def main():
    engage()

if __name__ == "__main__":
    main()
