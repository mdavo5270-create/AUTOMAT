"""
OPTIMAT Brain — niches : automatisation, Bluesky, crypto, sujets monde.
Représente @mdavo5270.bsky.social
"""
from __future__ import annotations

import os
import random
from datetime import datetime, timezone

from optomat.catalog import CATALOG, by_status, summary

# --- Automatisation / agents / build in public ---
TIPS_AUTO = [
    "Astuce : sépare App Password et vrai mot de passe. Toujours. 🐛",
    "GitHub Actions = serveur gratuit pour bots planifiés. Pas besoin de VPS pour du cron.",
    "Un orchestrateur qui décide des jobs > 10 scripts qui tournent en même temps.",
    "Automatise le répétitif. Garde l'humain pour les vraies conversations.",
    "Build in public : montrer le bot en construction attire plus que le produit fini seul.",
    "Rate limit = fonctionnalité. Qui spam se fait restreindre.",
]

# --- Bluesky ---
TIPS_BSKY = [
    "Bluesky : les custom feeds et l'AT Protocol changent la donne vs algo fermé.",
    "Une bio claire + un post épinglé > 50 follows aléatoires.",
    "Répondre sous les posts de ta niche convertit mieux que liker en masse.",
    "Starter packs = découverte rapide de communautés. À utiliser, pas à spammer.",
]

# --- Crypto (factuel, pas de conseil financier) ---
TIPS_CRYPTO = [
    "Crypto : DYOR reste la base. Personne ne peut garantir un rendement.",
    "On-chain data > hype Twitter. Les blocs ne mentent pas, les narratives si.",
    "Self-custody = responsabilité. Perdre une seed = perdre les fonds.",
    "Régulation et adoption institutionnelle façonnent le cycle autant que le prix.",
    "Bitcoin = réseau + actif. Séparer le protocole du prix du jour aide à réfléchir.",
    "DeFi : lis le smart contract risk avant l'APY affiché.",
]

# --- Sujets monde / tech très discutés ---
TIPS_WORLD = [
    "L'IA générative déplace le travail de 'produire' vers 'diriger et vérifier'.",
    "Open source : la transparence du code reste un avantage stratégique.",
    "Productivité : moins d'outils, plus de systèmes qui se parlent entre eux.",
    "Internet 2026 : attention rare, contenu médiocre en quantité infinie.",
    "Les réseaux décentralisés tentent de rendre la portabilité du social réelle.",
]

QUESTIONS = [
    "Tu automatises quoi en ce moment — et ça te fait gagner combien de temps / semaine ?",
    "Bluesky : tu es là pour la tech, la commu, ou la croissance ?",
    "Crypto : tu suis plutôt le prix, l'on-chain, ou la régulation ?",
    "IA : tu l'utilises pour coder, écrire, ou décider ?",
    "Build in public : tu partages tes wins, tes fails, ou les deux ?",
    "Quel sujet monde tu suis le plus en ce moment (tech, éco, géo) ?",
]

QUOTES = [
    "Ship early, learn fast.",
    "Not financial advice — just signal over noise.",
    "Done > perfect, puis itère.",
    "Build systems, not just goals.",
]

SERIES = [
    "Série AUTO #1 : un bot Bluesky 24/7 sans VPS (GitHub Actions).",
    "Série AUTO #2 : méta-bot — une automatisation qui pilote les autres.",
    "Série CRYPTO #1 : séparer protocole, prix et narratif.",
    "Série CRYPTO #2 : self-custody et hygiène de clés, les bases.",
    "Série MONDE #1 : IA + automatisation = le duo qui redéfinit le travail.",
    "Série BSKY #1 : croissance éthique > follow spam.",
]


def _hour_utc() -> int:
    return datetime.now(timezone.utc).hour


def _weekday() -> int:
    return datetime.now(timezone.utc).weekday()


def decide_jobs() -> list[str]:
    h = _hour_utc()
    jobs: list[str] = []
    mode = os.getenv("OPTIMAT_MODE", "auto")

    if mode == "content":
        return ["post_smart"]
    if mode == "engage":
        return ["engage", "replies"]
    if mode == "full":
        return ["post_smart", "rss", "engage", "replies", "stats"]

    if h in (7, 8, 9, 12, 15, 17, 18, 20):
        jobs.append("post_smart")
    if h % 2 == 0:
        jobs.append("rss")
    if h in (8, 12, 16, 20):
        jobs.append("engage")
    jobs.append("replies")
    if h == 21 and _weekday() == 6:
        jobs.append("weekly_report")
    if h == 10:
        jobs.append("stats")

    seen = set()
    out = []
    for j in jobs:
        if j not in seen:
            seen.add(j)
            out.append(j)
    return out or ["replies"]


def _rotate_niche() -> str:
    """Répartition des niches selon l'heure (diversité anti-spam thématique)."""
    h = _hour_utc()
    # 0-5 auto, 6-11 bluesky/world, 12-17 crypto, 18-23 mix build+world
    if h < 6:
        return "auto"
    if h < 12:
        return random.choice(["bluesky", "world", "auto"])
    if h < 18:
        return random.choice(["crypto", "world", "auto"])
    return random.choice(["auto", "bluesky", "crypto", "world"])


def pick_content() -> tuple[str, str]:
    custom = os.getenv("POST_TEXT", "").strip()
    if custom:
        return "custom", custom

    niche = os.getenv("FORCE_NICHE", "").strip() or _rotate_niche()
    h = _hour_utc()

    if niche == "crypto":
        pool = [
            ("crypto_tip", random.choice(TIPS_CRYPTO)),
            ("question", "Crypto : tu priorises sécurité, usage, ou spéculation — et pourquoi ?"),
            ("series", random.choice([s for s in SERIES if "CRYPTO" in s] or SERIES)),
        ]
    elif niche == "bluesky":
        pool = [
            ("bsky_tip", random.choice(TIPS_BSKY)),
            ("question", random.choice(QUESTIONS)),
            ("series", random.choice([s for s in SERIES if "BSKY" in s or "AUTO" in s] or SERIES)),
        ]
    elif niche == "world":
        pool = [
            ("world_tip", random.choice(TIPS_WORLD)),
            ("question", random.choice(QUESTIONS)),
            ("quote", random.choice(QUOTES)),
        ]
    else:  # auto
        pool = [
            ("tip", random.choice(TIPS_AUTO)),
            ("series", random.choice([s for s in SERIES if "AUTO" in s] or SERIES)),
            ("question", random.choice(QUESTIONS)),
            ("quote", random.choice(QUOTES)),
        ]

    # matin = plus tips, soir = plus questions
    if h < 12:
        pool = [p for p in pool if p[0] != "question"] + pool
    kind, text = random.choice(pool)

    brand = os.getenv("BRAND_SUFFIX", "\n\n— OPTIMAT 🐛")
    if brand and brand.strip() not in text:
        text = text + brand
    return f"{niche}:{kind}", text


def catalog_report() -> str:
    s = summary()
    return (
        f"OPTIMAT catalogue: {len(CATALOG)} autos | "
        f"active={s.get('active', 0)} stub={s.get('stub', 0)} | "
        f"niches=auto,bluesky,crypto,monde"
    )
