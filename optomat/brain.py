"""
OPTIMAT Brain — l'automatisation qui gère les automatisations.
Décide quoi lancer selon l'heure, le jour, et la config.
Représente le compte mdavo5270 et fait le travail à ta place.
"""
from __future__ import annotations

import os
import random
from datetime import datetime, timezone
from pathlib import Path

from optomat.catalog import CATALOG, by_status, summary

# Contenu de représentation (personnalisable via secrets)
TIPS = [
    "Astuce Bluesky : utilise des App Passwords, jamais ton vrai mot de passe. 🐛",
    "L'AT Protocol permet des clients alternatifs et des feeds custom. Explore !",
    "Poste régulièrement > poster beaucoup d'un coup. La constance gagne.",
    "Répondre aux vrais humains convertit mieux que liker en masse.",
    "Une bio claire + un pinned post = plus de follows qualifiés.",
    "Les starter packs aident à découvrir ta niche rapidement.",
    "Moins de spam, plus de valeur = croissance durable.",
    "Automatise le répétitif, garde l'humain pour les conversations.",
]

QUESTIONS = [
    "Tu construis quoi en ce moment ?",
    "Quelle est ta stack préférée en 2026 ?",
    "Bluesky ou autre : où tu passes le plus de temps et pourquoi ?",
    "Une automatisation qui t'a vraiment fait gagner du temps ?",
    "Conseil rapide pour quelqu'un qui débute sur Bluesky ?",
]

QUOTES = [
    "Ship early, learn fast.",
    "Done is better than perfect — puis itère.",
    "Build in public. Apprends en public.",
    "L'attention est rare. Le spam est gratuit. Choisis.",
]

SERIES = [
    "Série AUTO #1 : un bot qui poste, like et répond — sans serveur dédié, via GitHub Actions.",
    "Série AUTO #2 : sépare App Password et vrai mot de passe. Toujours.",
    "Série AUTO #3 : mesure ce qui amène des follows, coupe le reste.",
    "Série AUTO #4 : RSS → Bluesky = contenu régulier sans y penser.",
    "Série AUTO #5 : l'orchestrateur OPTIMAT décide quoi lancer selon l'heure.",
]


def _hour_utc() -> int:
    return datetime.now(timezone.utc).hour


def _weekday() -> int:
    return datetime.now(timezone.utc).weekday()  # 0=lundi


def decide_jobs() -> list[str]:
    """Choisit les jobs à lancer pour ce run (méta-décision)."""
    h = _hour_utc()
    jobs: list[str] = []

    # Toujours : rate-limit friendly, pas tout en même temps
    mode = os.getenv("OPTIMAT_MODE", "auto")  # auto | content | engage | full

    if mode == "content":
        return ["post_smart"]
    if mode == "engage":
        return ["engage", "replies"]
    if mode == "full":
        return ["post_smart", "rss", "engage", "replies", "stats"]

    # auto : selon l'heure UTC
    if h in (7, 8, 9, 12, 17, 18, 20):
        jobs.append("post_smart")
    if h % 2 == 0:
        jobs.append("rss")
    if h in (8, 12, 16, 20):
        jobs.append("engage")
    if h % 1 == 0:  # chaque heure possible
        jobs.append("replies")
    if h == 21 and _weekday() == 6:  # dimanche soir
        jobs.append("weekly_report")
    if h == 10:
        jobs.append("stats")

    # dédoublonne en gardant l'ordre
    seen = set()
    out = []
    for j in jobs:
        if j not in seen:
            seen.add(j)
            out.append(j)
    return out or ["replies"]  # au minimum check mentions


def pick_content() -> tuple[str, str]:
    """Choisit le type + texte d'un post de représentation."""
    custom = os.getenv("POST_TEXT", "").strip()
    if custom:
        return "custom", custom

    h = _hour_utc()
    pool = []
    if h < 12:
        pool = [("tip", random.choice(TIPS)), ("question", random.choice(QUESTIONS))]
    elif h < 18:
        pool = [("series", random.choice(SERIES)), ("tip", random.choice(TIPS))]
    else:
        pool = [("quote", random.choice(QUOTES)), ("question", random.choice(QUESTIONS))]

    kind, text = random.choice(pool)
    brand = os.getenv("BRAND_SUFFIX", "\n\n— via OPTIMAT 🐛")
    if brand and brand not in text:
        text = text + brand
    return kind, text


def catalog_report() -> str:
    s = summary()
    active = len(by_status("active"))
    lines = [
        f"OPTIMAT catalogue: {len(CATALOG)} automatisations",
        f"active={s.get('active', 0)} scheduled={s.get('scheduled', 0)} stub={s.get('stub', 0)}",
        f"Ce run exécute le cerveau + jobs active ({active} prêtes).",
    ]
    return "\n".join(lines)
