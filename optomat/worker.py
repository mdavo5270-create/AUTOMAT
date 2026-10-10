"""
OPTIMAT Worker — exécute les jobs décidés par le brain.
Une seule entrée: python -m optomat.worker
"""
from __future__ import annotations

import json
import os
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

# réutilise le client AUTOMAT
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from optomat.brain import decide_jobs, pick_content, catalog_report
from optomat.catalog import by_status


def log(msg: str):
    print(f"[{datetime.now(timezone.utc).isoformat()}] {msg}")


def run_post_smart():
    from automat.client import get_client
    kind, text = pick_content()
    client = get_client()
    if len(text) > 300:
        text = text[:297] + "..."
    client.send_post(text=text)
    log(f"post_smart ({kind}): {text[:80]}...")


def run_rss():
    from automat.rss import post_from_rss
    feed = os.getenv("RSS_FEED", "https://www.githubstatus.com/history.rss")
    post_from_rss(feed, max_posts=int(os.getenv("RSS_MAX", "2")))


def run_engage():
    from automat.engage import engage
    engage()


def run_replies():
    from automat.replies import reply_to_mentions
    reply_to_mentions(max_replies=int(os.getenv("MAX_REPLIES", "5")))


def run_stats():
    from automat.client import get_client
    client = get_client()
    profile = client.get_profile(client.me.did)
    data = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "handle": profile.handle,
        "followers": getattr(profile, "followers_count", None),
        "follows": getattr(profile, "follows_count", None),
        "posts": getattr(profile, "posts_count", None),
    }
    path = Path("data/stats.jsonl")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(data) + "\n")
    log(f"stats: followers={data['followers']} follows={data['follows']} posts={data['posts']}")


def run_weekly_report():
    from automat.client import get_client
    client = get_client()
    profile = client.get_profile(client.me.did)
    text = (
        f"Rapport hebdo OPTIMAT \ud83d\udcca\n"
        f"@{profile.handle}\n"
        f"Followers: {getattr(profile, 'followers_count', '?')}\n"
        f"Posts: {getattr(profile, 'posts_count', '?')}\n"
        f"Automatisations actives: {len(by_status('active'))}/100\n"
        f"Le reste du catalogue est en stub, activable à la demande."
    )
    client.send_post(text=text[:300])
    log("weekly_report publié")


JOBS = {
    "post_smart": run_post_smart,
    "rss": run_rss,
    "engage": run_engage,
    "replies": run_replies,
    "stats": run_stats,
    "weekly_report": run_weekly_report,
}


def main():
    log("OPTIMAT démarre")
    log(catalog_report())
    jobs = decide_jobs()
    # override manuel
    only = os.getenv("OPTIMAT_ONLY", "").strip()
    if only:
        jobs = [j.strip() for j in only.split(",") if j.strip()]
    log(f"Jobs décidés: {jobs}")

    errors = []
    for name in jobs:
        fn = JOBS.get(name)
        if not fn:
            log(f"Job inconnu (stub): {name}")
            continue
        try:
            log(f"→ {name}")
            fn()
            log(f"✓ {name}")
        except Exception as e:
            log(f"✗ {name}: {e}")
            traceback.print_exc()
            errors.append(name)

    if errors:
        log(f"Terminé avec erreurs: {errors}")
        sys.exit(1)
    log("OPTIMAT terminé OK")


if __name__ == "__main__":
    main()
