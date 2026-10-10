"""Croissance follow ciblée + unfollow non-réciproque prudent."""
from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

STATE_FILE = Path("data/growth_state.json")


def _load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {"followed": {}, "seen": []}


def _save_state(state: dict):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def discover_and_follow(client, max_follows: int | None = None):
    max_follows = min(max_follows or int(os.getenv("MAX_FOLLOWS_PER_RUN", "8")), 15)
    keywords = os.getenv(
        "GROWTH_KEYWORDS",
        os.getenv("KEYWORDS", "bluesky,automatisation,bitcoin,ethereum,ia,python,open source"),
    )
    kws = [k.strip() for k in keywords.split(",") if k.strip()]
    state = _load_state()
    followed_today = 0
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    already_today = sum(1 for m in state.get("followed", {}).values() if m.get("date") == today)
    daily_cap = int(os.getenv("MAX_FOLLOWS_PER_DAY", "35"))
    if already_today >= daily_cap:
        print(f"Growth: plafond jour ({daily_cap})")
        return
    room = min(max_follows, daily_cap - already_today)

    for kw in kws:
        if followed_today >= room:
            break
        try:
            results = client.app.bsky.feed.search_posts(params={"q": kw, "limit": 20})
        except Exception as e:
            print(f"search {kw}: {e}")
            continue
        for post in getattr(results, "posts", []) or []:
            if followed_today >= room:
                break
            author = post.author
            did, handle = author.did, author.handle
            if did in state.get("followed", {}) or did in state.get("seen", []):
                continue
            try:
                client.follow(did)
                state.setdefault("followed", {})[did] = {
                    "handle": handle,
                    "date": today,
                    "keyword": kw,
                    "ts": datetime.now(timezone.utc).isoformat(),
                }
                state.setdefault("seen", []).append(did)
                state["seen"] = state["seen"][-2000:]
                followed_today += 1
                print(f"  follow @{handle} ({kw})")
                time.sleep(2.5)
            except Exception as e:
                print(f"  skip @{handle}: {e}")
                state.setdefault("seen", []).append(did)
    _save_state(state)
    print(f"Growth: +{followed_today} follows")


def unfollow_non_reciprocal(client, min_days: int | None = None, max_unfollows: int | None = None):
    """Unfollow après N jours si activé."""
    if os.getenv("ENABLE_UNFOLLOW", "1") not in ("1", "true", "yes"):
        print("Unfollow: off")
        return
    min_days = min_days or int(os.getenv("UNFOLLOW_AFTER_DAYS", "10"))
    max_unfollows = max_unfollows or int(os.getenv("MAX_UNFOLLOWS_PER_RUN", "5"))
    state = _load_state()
    now = datetime.now(timezone.utc)
    done = 0
    for did, meta in list(state.get("followed", {}).items()):
        if done >= max_unfollows:
            break
        try:
            ts = datetime.fromisoformat(meta["ts"].replace("Z", "+00:00"))
        except Exception:
            continue
        if (now - ts).days < min_days:
            continue
        try:
            client.unfollow(did)
            del state["followed"][did]
            done += 1
            print(f"  unfollow @{meta.get('handle', did)}")
            time.sleep(2)
        except Exception as e:
            print(f"  unfollow fail: {e}")
    _save_state(state)
    print(f"Unfollow: {done}")
