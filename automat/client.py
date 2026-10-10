"""
Client Bluesky unifié pour AUTOMAT
Utilise le SDK officiel atproto (Python)
"""

import os
from dotenv import load_dotenv
from atproto import Client
from rich.console import Console

load_dotenv()
console = Console()


def get_client() -> Client:
    """Crée et authentifie un client Bluesky."""
    handle = os.getenv("BLUESKY_HANDLE")
    password = os.getenv("BLUESKY_APP_PASSWORD")

    if not handle or not password:
        console.print("[red]❌ BLUESKY_HANDLE et BLUESKY_APP_PASSWORD doivent être définis dans .env[/red]")
        raise SystemExit(1)

    client = Client()
    try:
        client.login(handle, password)
        console.print(f"[green]✅ Connecté en tant que {handle}[/green]")
        return client
    except Exception as e:
        console.print(f"[red]❌ Erreur de connexion : {e}[/red]")
        raise SystemExit(1)
