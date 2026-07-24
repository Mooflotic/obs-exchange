#!/usr/bin/env python3
"""OBS-DB-SLIM passo 1 — drop indici duplicati (una-tantum).

Eseguire NEL container api (o host con path DB), DOPO GO esplicito.
NON fa VACUUM. Snapshot obbligatorio prima dei DROP.

Esempio Cassiopea (dopo scp dello script in data/db/):
  sudo docker compose exec -T -e PYTHONPATH=/app api \\
    python /data/db/obs_db_slim_p1_drop_dup_indexes.py

Env:
  OBS_DB_PATH   default /data/db/observatory.db
  OBS_BACKUP_DIR default /data/db/../backups  (= data/backups)
  DRY_RUN=1     solo EXPLAIN + previsione, nessun DROP
"""
from __future__ import annotations

import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

DB = Path(os.environ.get("OBS_DB_PATH", "/data/db/observatory.db"))
BACKUP_DIR = Path(os.environ.get("OBS_BACKUP_DIR", str(DB.parent.parent / "backups")))
DRY = os.environ.get("DRY_RUN", "").strip() in {"1", "true", "yes"}

# Solo indici espliciti ridondanti. NON toccare sqlite_autoindex_* (UNIQUE constraint).
DROP_INDEXES = (
    # Coppia A: UNIQUE(dedup_key) già coperto da sqlite_autoindex_observations_raw_1
    "ix_observations_raw_dedup_key",
    # Coppia B: stesso (seen_at); tenere ix_obs_seen (già preferito dal planner)
    "ix_observations_seen_at",
    # ix_metric_snapshots_taken_at escluso: guadagno ~0 e nessuna PROBE dedicata
)

KEEP = {
    "ix_observations_raw_dedup_key": "sqlite_autoindex_observations_raw_1",
    "ix_observations_seen_at": "ix_obs_seen",
}

PROBES = [
    (
        "dedup_lookup",
        'EXPLAIN QUERY PLAN SELECT * FROM observations_raw WHERE dedup_key=?',
        ("probe-dedup-key-00000000000000000000000000000000",),
    ),
    (
        "presence_mac_seen",
        'EXPLAIN QUERY PLAN SELECT * FROM observations WHERE mac=? AND seen_at >= datetime("now","-24 hours")',
        ("00:00:00:00:00:00",),
    ),
    (
        "seen_at_range",
        'EXPLAIN QUERY PLAN SELECT id FROM observations WHERE seen_at < datetime("now","-3 days")',
        (),
    ),
    (
        "seen_at_count_24h",
        'EXPLAIN QUERY PLAN SELECT COUNT(*) FROM observations WHERE seen_at >= datetime("now","-24 hours")',
        (),
    ),
]


def log(msg: str) -> None:
    print(msg, flush=True)


def index_bytes(con: sqlite3.Connection, name: str) -> int:
    con.execute("CREATE VIRTUAL TABLE IF NOT EXISTS temp.stat USING dbstat")
    row = con.execute(
        "SELECT COALESCE(SUM(pgsize),0) FROM temp.stat WHERE name=?", (name,)
    ).fetchone()
    return int(row[0] or 0)


def snapshot(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dst = sqlite3.connect(str(dest))
    src_con = sqlite3.connect(f"file:{src}?mode=ro", uri=True)
    src_con.backup(dst)
    dst.close()
    src_con.close()
    log(f"SNAPSHOT {dest} size={dest.stat().st_size}")


def explain_all(con: sqlite3.Connection, label: str) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    log(f"=== EXPLAIN {label} ===")
    for name, sql, params in PROBES:
        # SQLite EXPLAIN QUERY PLAN → (id, parent, notused, detail)
        details = [str(r[3]) for r in con.execute(sql, params)]
        out[name] = details
        log(f"-- {name}")
        for d in details:
            log(f"   {d}")
    return out


def assert_no_scan(plans: dict[str, list[str]], phase: str) -> None:
    """Reject new full-table SCAN on probed queries (presence/dedup/seen_at)."""
    for name, details in plans.items():
        joined = " ".join(details)
        if name == "dedup_lookup" and "USING INDEX" not in joined and "USING COVERING INDEX" not in joined:
            if "SCAN observations_raw" in joined and "INDEX" not in joined:
                raise SystemExit(f"FAIL {phase} {name}: expected index, got {details}")
        if name in {"seen_at_range", "seen_at_count_24h"}:
            if "SCAN observations" in joined and "INDEX" not in joined:
                raise SystemExit(f"FAIL {phase} {name}: full scan {details}")
            if "USING INDEX" not in joined and "USING COVERING INDEX" not in joined:
                raise SystemExit(f"FAIL {phase} {name}: no index {details}")
        if name == "presence_mac_seen":
            # presence uses mac index (or seen_at); must not be bare SCAN
            if "SCAN observations" in joined and "INDEX" not in joined:
                raise SystemExit(f"FAIL {phase} {name}: full scan {details}")


def main() -> int:
    if not DB.is_file():
        log(f"ERR missing DB {DB}")
        return 2

    size_before = DB.stat().st_size
    log(f"DB {DB} size={size_before} DRY_RUN={DRY}")

    # Read-only probe for sizes
    ro = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    logical = 0
    for name in DROP_INDEXES:
        b = index_bytes(ro, name)
        keep = KEEP[name]
        kb = index_bytes(ro, keep)
        log(f"DROP_CANDIDATE {name} bytes={b} KEEP {keep} bytes={kb}")
        logical += b
    freelist = ro.execute("PRAGMA freelist_count").fetchone()[0]
    page_size = ro.execute("PRAGMA page_size").fetchone()[0]
    log(f"LOGICAL_FREE_EST_BYTES {logical} ({logical/1024/1024:.1f} MiB)")
    log(f"FILE_WILL_STAY ~{size_before} until VACUUM (passo 4); freelist_now={freelist}")
    before_plans = explain_all(ro, "BEFORE")
    assert_no_scan(before_plans, "BEFORE")
    ro.close()

    if DRY:
        log("DRY_RUN done — nessun DROP")
        return 0

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    snap = BACKUP_DIR / f"pre-db-slim-p1-{stamp}.db"
    log(f"==> snapshot → {snap}")
    snapshot(DB, snap)
    snap_size = snap.stat().st_size
    # Guard: non procedere al DROP se lo snapshot non è ~file live
    min_ok = int(size_before * 0.95)
    if snap_size < min_ok:
        log(f"ERR snapshot troppo piccolo: {snap_size} < {min_ok} (95% di {size_before})")
        return 3
    log(f"SNAPSHOT_OK size={snap_size} (>= {min_ok})")

    con = sqlite3.connect(str(DB))
    con.execute("PRAGMA busy_timeout=60000")
    try:
        for name in DROP_INDEXES:
            exists = con.execute(
                "SELECT 1 FROM sqlite_master WHERE type='index' AND name=?", (name,)
            ).fetchone()
            if not exists:
                log(f"SKIP missing {name}")
                continue
            log(f"DROP INDEX {name}")
            con.execute(f'DROP INDEX IF EXISTS "{name}"')
        con.commit()
        after_plans = explain_all(con, "AFTER")
        assert_no_scan(after_plans, "AFTER")
        # dedup must still hit UNIQUE autoindex
        dedup = " ".join(after_plans["dedup_lookup"])
        if "sqlite_autoindex_observations_raw_1" not in dedup and "USING INDEX" not in dedup and "USING COVERING INDEX" not in dedup:
            raise SystemExit(f"FAIL AFTER dedup not indexed: {after_plans['dedup_lookup']}")
        seen = " ".join(after_plans["seen_at_range"])
        if "ix_obs_seen" not in seen:
            raise SystemExit(f"FAIL AFTER seen_at not on ix_obs_seen: {after_plans['seen_at_range']}")
        fc = con.execute("PRAGMA freelist_count").fetchone()[0]
        log(f"FREELIST_AFTER {fc} pages (~{fc * page_size} bytes = {fc * page_size / 1024 / 1024:.1f} MiB)")
        log(f"OS_SIZE_AFTER {DB.stat().st_size} (atteso invariato ~{size_before})")
        log(f"SNAPSHOT_PATH {snap}")
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()

    log("DONE passo 1 — nessun VACUUM")
    return 0


if __name__ == "__main__":
    sys.exit(main())
