"""
Couche "vraie personne" : variation d'horaires, tons, longueurs, émojis.
Le but : paraître humain même si c'est automatisé.
"""
from __future__ import annotations

import random
import re
from datetime import datetime, timezone


def jitter_skip(probability: float = 0.12) -> bool:
    """Parfois on ne poste pas : comme quelqu'un qui a autre chose à faire."""
    return random.random() < probability


def humanize_text(text: str) -> str:
    text = text.strip()
    # parfois enlever la signature trop "bot"
    if random.random() < 0.35:
        text = re.sub(r"\n*\u2014\s*OPTIMAT.*$", "", text, flags=re.I | re.M).strip()
        text = re.sub(r"\n*\u2014\s*via OPTIMAT.*$", "", text, flags=re.I | re.M).strip()
    # parfois minuscule en début (style chat)
    if random.random() < 0.15 and text and text[0].isupper():
        text = text[0].lower() + text[1:]
    # parfois ajouter un emoji unique
    emojis = ["", " 👍", " ✨", " 💡", " 🐛", " 👋"]
    if random.random() < 0.4 and not any(e.strip() and e.strip() in text for e in emojis):
        text = text + random.choice(emojis)
    # parfois raccourcir agressivement
    if random.random() < 0.2 and len(text) > 120:
        text = text[:117].rstrip(".") + "..."
    return text[:300]


def pick_daily_experiment() -> str:
    """
    Chaque jour on 'teste' une stratégie (pour plus tard mesurer ce qui marche).
    """
    day = datetime.now(timezone.utc).timetuple().tm_yday
    experiments = [
        "short_tips",
        "questions",
        "crypto_factual",
        "bluesky_growth",
        "build_in_public",
        "world_tech",
        "thread_teaser",
        "soft_cta_follow",
        "no_hashtag",
        "with_emoji",
    ]
    return experiments[day % len(experiments)]
