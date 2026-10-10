"""
Journal d'expériences : on enregistre ce qu'on a posté / follow
pour plus tard comparer ce qui amène le plus d'abonnés.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

LOG = Path("data/experiments.jsonl")


def log_event(kind: str, payload: dict):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "kind": kind,
        **payload,
    }
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
