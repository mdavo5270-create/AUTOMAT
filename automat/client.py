"""Client Bluesky unifié pour AUTOMAT"""
import os
from dotenv import load_dotenv
from atproto import Client

load_dotenv()

def get_client() -> Client:
    handle = os.getenv("BLUESKY_HANDLE") or os.getenv("BSKY_HANDLE") or os.getenv("BLUESKY_USERNAME")
    password = os.getenv("BLUESKY_APP_PASSWORD") or os.getenv("BSKY_PASSWORD") or os.getenv("BLUESKY_PASSWORD")

    if not handle or not password:
        raise SystemExit("ERREUR: Définis BLUESKY_HANDLE et BLUESKY_APP_PASSWORD (secrets GitHub ou .env)")

    client = Client()
    client.login(handle, password)
    print(f"Connecté en tant que {handle}")
    return client
