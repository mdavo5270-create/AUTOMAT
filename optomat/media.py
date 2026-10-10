"""
Médias : poster avec image si un fichier est dispo dans media/ready/
ou si MEDIA_URL est fourni (téléchargement simple).
Pour l'instant : images locales commitées dans le repo sous media/ready/
"""
from __future__ import annotations

import os
import random
from pathlib import Path

READY = Path("media/ready")


def pick_image() -> Path | None:
    if not READY.exists():
        return None
    files = [
        p
        for p in READY.iterdir()
        if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".gif"}
    ]
    if not files:
        return None
    return random.choice(files)


def post_with_optional_image(client, text: str):
    img = pick_image()
    force = os.getenv("FORCE_MEDIA", "0") == "1"
    if img is None and not force:
        return client.send_post(text=text)

    if img is None:
        return client.send_post(text=text)

    data = img.read_bytes()
    # limite grossière taille
    if len(data) > 900_000:
        print(f"Image trop lourde, post texte seul: {img.name}")
        return client.send_post(text=text)

    upload = client.upload_blob(data)
    embed = {
        "$type": "app.bsky.embed.images",
        "images": [{"alt": text[:100] or img.stem, "image": upload.blob}],
    }
    print(f"Post avec média: {img.name}")
    return client.send_post(text=text, embed=embed)
