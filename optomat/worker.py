"""OPTIMAT Worker — autopilote complet."""
from __future__ import annotations

import json
import os
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from optomat.brain import decide_jobs, pick_content, catalog_report
from optomat.human import humanize_text, jitter_skip, pick_daily_experiment
from optomat.experiments import log_event


def log(msg: str):
    print(f"[{datetime.now(timezone.utc).isoformat()}] {msg}")


def run_post_smart():
    from automat.client import get_client
    from optomat.media import post_with_optional_image

    if jitter_skip(0.08):
        log("post_smart: skip jitter")
        log_event("post_skip", {"reason": "jitter"})
        return

    kind, text = pick_content()
    text = humanize_text(text)
    exp = pick_daily_experiment()
    client = get_client()
    response = post_with_optional_image(client, text)
    uri = getattr(response, "uri", None)
    log(f"post_smart ({kind}) exp={exp}: {text[:90]}...")
    log_event("post", {"kind": kind, "experiment": exp, "uri": uri, "len": len(text)})


def run_news():
    from automat.client import get_client
    from optomat.news import post_news

    client = get_client()
    post_news(client, max_posts=int(os.getenv("NEWS_MAX", "1")))


def run_rss():
    from automat.rss import post_from_rss

    feed = os.getenv("RSS_FEED", "")
    if not feed:
        # délègue au module news multi-flux
        return run_news()
    post_from_rss(feed, max_posts=int(os.getenv("RSS_MAX", "1")))
    log_event("rss", {"feed": feed})


def run_engage():
    from automat.engage import engage

    engage()
    log_event("engage", {})


def run_replies():
    from automat.replies import reply_to_mentions

    reply_to_mentions(max_replies=int(os.getenv("MAX_REPLIES", "5")))
    log_event("replies", {})


def run_growth():
    from automat.client import get_client
    from optomat.growth import discover_and_follow, unfollow_non_reciprocal

    client = get_client()
    discover_and_follow(client)
    unfollow_non_reciprocal(client)
    log_event("growth", {})


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
    log_event("stats", data)


def run_weekly_report():
    from automat.client import get_client

    client = get_client()
    profile = client.get_profile(client.me.did)
    text = humanize_text(
        f"Notes de la semaine \ud83d\udcca @{profile.handle} \u00b7 "
        f"{getattr(profile, 'followers_count', '?')} followers \u2014 on teste, on garde ce qui marche."
    )
    client.send_post(text=text[:300])
    log("weekly_report")
    log_event("weekly_report", {})


JOBS = {
    "post_smart": run_post_smart,
    "news": run_news,
    "rss": run_rss,
    "engage": run_engage,
    "replies": run_replies,
    "growth": run_growth,
    "stats": run_stats,
    "weekly_report": run_weekly_report,
}


def main():
    log("OPTIMAT autopilote")
    log(catalog_report())
    log(f"expérience du jour: {pick_daily_experiment()}")

    jobs = decide_jobs()
    only = os.getenv("OPTIMAT_ONLY", "").strip()
    if only:
        jobs = [j.strip() for j in only.split(",") if j.strip()]

    log(f"Jobs: {jobs}")
    errors = []
    for name in jobs:
        fn = JOBS.get(name)
        if not fn:
            log(f"stub: {name}")
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
        log(f"erreurs: {errors}")
        sys.exit(1)
    log("OK")


if __name__ == "__main__":
    main()
