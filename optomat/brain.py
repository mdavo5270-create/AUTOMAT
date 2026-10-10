"""OPTIMAT Brain — cadence HUMAINE : peu de posts, bien espacés."""
from __future__ import annotations

import os
import random
from datetime import datetime, timezone

from optomat.catalog import CATALOG, by_status, summary

TIPS_AUTO = [
    "Astuce : App Password ≠ mot de passe principal.",
    "GitHub Actions = cron gratuit pour bots.",
    "Un orchestrateur > dix scripts qui spam.",
    "Automatise le répétitif, reste humain sur les convos.",
    "Build in public attire plus que le produit fini silencieux.",
    "Rate limit = garde-fou, pas un bug.",
]
TIPS_BSKY = [
    "Custom feeds + AT Proto : autre logique qu'un algo fermé.",
    "Bio claire + pinned > follows au hasard.",
    "Répondre dans la niche > liker en masse.",
    "Starter packs = découverte, pas spam.",
]
TIPS_CRYPTO = [
    "DYOR. Personne ne garantit un rendement.",
    "On-chain > hype.",
    "Self-custody = responsabilité totale.",
    "Régulation et adoption pèsent autant que le prix.",
    "Sépare protocole Bitcoin et narratif du jour.",
    "DeFi : risque smart contract avant l'APY.",
]
TIPS_WORLD = [
    "L'IA déplace : produire → diriger et vérifier.",
    "Open source reste un avantage stratégique.",
    "Moins d'outils, plus de systèmes connectés.",
    "Attention rare, contenu médiocre partout.",
    "Décentralisation = pari sur la portabilité du social.",
]
QUESTIONS = [
    "Tu automatises quoi en ce moment ?",
    "Bluesky : tech, commu ou croissance ?",
    "Crypto : prix, on-chain ou régulation ?",
    "IA : coder, écrire ou déléguer ?",
    "Build in public : wins, fails, ou les deux ?",
    "Sujet de la semaine que tu suis vraiment ?",
]
QUOTES = [
    "Ship early, learn fast.",
    "Not financial advice — signal over noise.",
    "Done > perfect, puis itère.",
    "Build systems, not just goals.",
]
SERIES = [
    "Série AUTO : bot 24/7 sans VPS.",
    "Série AUTO : méta-bot qui pilote le reste.",
    "Série CRYPTO : protocole vs prix.",
    "Série CRYPTO : self-custody.",
    "Série MONDE : IA au travail.",
    "Série BSKY : croissance éthique.",
]


def _hour_utc() -> int:
    return datetime.now(timezone.utc).hour


def _weekday() -> int:
    return datetime.now(timezone.utc).weekday()


def decide_jobs() -> list[str]:
    """
    Règle d'or : JAMAIS post_smart + news + rss dans le même run.
    Max 2–4 posts publics / jour au total (heures fixes).
    Le reste du temps = silence, likes légers, replies si besoin.
    """
    h = _hour_utc()
    mode = os.getenv("OPTIMAT_MODE", "auto")

    if mode == "content":
        return ["post_smart"]
    if mode == "engage":
        return ["engage", "replies"]
    if mode == "growth":
        return ["growth"]
    if mode == "news":
        return ["news"]
    if mode == "full":
        # full ne veut plus dire "tout poster" : 1 contenu + engage + growth
        return ["post_smart", "engage", "growth"]

    jobs: list[str] = []

    # --- CONTENU : seulement 3 créneaux UTC / jour, UN seul type ---
    # 8h = post perso, 13h = actu, 19h = post perso (autre niche)
    if h == 8:
        jobs.append("post_smart")
    elif h == 13:
        jobs.append("news")
    elif h == 19:
        jobs.append("post_smart")

    # --- engagement discret (pas de post) ---
    if h in (10, 16, 22):
        jobs.append("engage")

    # mentions : max 2x / jour
    if h in (11, 20):
        jobs.append("replies")

    # growth follows : 1x / jour
    if h == 15:
        jobs.append("growth")

    # stats silencieux (pas de post)
    if h == 23:
        jobs.append("stats")

    if h == 21 and _weekday() == 6:
        jobs.append("weekly_report")

    # dédoublonnage
    seen, out = set(), []
    for j in jobs:
        if j not in seen:
            seen.add(j)
            out.append(j)

    # si aucune heure clé : ne rien faire (silence = humain)
    return out


def _rotate_niche() -> str:
    h = _hour_utc()
    if h < 12:
        return random.choice(["auto", "bluesky"])
    if h < 18:
        return random.choice(["crypto", "world"])
    return random.choice(["auto", "world", "bluesky"])


def pick_content() -> tuple[str, str]:
    custom = os.getenv("POST_TEXT", "").strip()
    if custom:
        return "custom", custom
    niche = os.getenv("FORCE_NICHE", "").strip() or _rotate_niche()

    if niche == "crypto":
        pool = [
            ("crypto_tip", random.choice(TIPS_CRYPTO)),
            ("question", "Crypto : sécurité, usage ou spéculation ?"),
            ("series", random.choice([s for s in SERIES if "CRYPTO" in s] or SERIES)),
        ]
    elif niche == "bluesky":
        pool = [
            ("bsky_tip", random.choice(TIPS_BSKY)),
            ("question", random.choice(QUESTIONS)),
        ]
    elif niche == "world":
        pool = [
            ("world_tip", random.choice(TIPS_WORLD)),
            ("quote", random.choice(QUOTES)),
        ]
    else:
        pool = [
            ("tip", random.choice(TIPS_AUTO)),
            ("series", random.choice([s for s in SERIES if "AUTO" in s] or SERIES)),
            ("question", random.choice(QUESTIONS)),
        ]

    kind, text = random.choice(pool)
    # pas de signature bot par défaut
    brand = os.getenv("BRAND_SUFFIX", "")
    if brand and brand.strip() not in text:
        text = text + brand
    return f"{niche}:{kind}", text


def catalog_report() -> str:
    s = summary()
    return (
        f"OPTIMAT cadence humaine | active={s.get('active', 0)} | "
        f"max ~3 posts/jour espacés"
    )
