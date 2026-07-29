#!/usr/bin/env python3
"""Post-deploy Q checks + gates helpers (RO where possible)."""
import json
import os
import sqlite3
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

DB = "/volume1/Docker/observatory/data/db/observatory.db"


def sh(cmd):
    return subprocess.check_output(cmd, shell=True, text=True)


def main():
    c = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    c.row_factory = sqlite3.Row

    fa = c.execute(
        "SELECT id,subject_type,subject_id,fact_key,value_norm,source,authority,state "
        "FROM fact_assertions WHERE id=251"
    ).fetchone()
    print("FA251", dict(fa) if fa else None)

    tot = c.execute("SELECT COUNT(*) FROM zeek_behavior_evidence").fetchone()[0]
    today = datetime.utcnow().strftime("%Y-%m-%d")
    today_n = c.execute(
        "SELECT COUNT(*) FROM zeek_behavior_evidence WHERE first_seen >= ?",
        (today,),
    ).fetchone()[0]
    print("ZEEK_ROWS", tot, "TODAY", today_n)
    print(
        "DB_MIB",
        round(Path(DB).stat().st_size / (1024 * 1024), 3),
    )

    # G5 remesaure
    ev = c.execute(
        "SELECT id, json_extract(evidence,'$.fact_id') AS fact_id "
        "FROM zeek_behavior_evidence WHERE association='certain' ORDER BY id"
    ).fetchall()
    flip = []
    for r in ev:
        fid = r["fact_id"]
        if fid is None:
            continue
        fa = c.execute(
            "SELECT valid_from, valid_from_truncated FROM fact_assertions WHERE id=?",
            (int(fid),),
        ).fetchone()
        if fa and (fa["valid_from"] is None or fa["valid_from_truncated"]):
            flip.append(r["id"])
    print("G5_FLIP_IDS", flip)

    # G6
    for mac in ("70:50:AF:FC:0A:F8", "70:50:AF:FC:0A:F9"):
        rows = c.execute(
            "SELECT id,kind,src_mac FROM zeek_behavior_evidence "
            "WHERE upper(replace(src_mac,'-',':'))=? ORDER BY id",
            (mac,),
        ).fetchall()
        print("G6", mac, [r["id"] for r in rows])

    # F8 list
    rows = c.execute(
        "SELECT id FROM name_proposals WHERE status_reason IN (?,?) ORDER BY id",
        ("w4a_chassis_manual_blocks_weaker", "w4a_chassis_value_dedup"),
    ).fetchall()
    print("F8_SOFT_IDS", [r["id"] for r in rows])

    # fact_assertions breaker-ish counts
    fa_tot = c.execute("SELECT COUNT(*) FROM fact_assertions").fetchone()[0]
    print("FACT_ASSERTIONS_ROWS", fa_tot)
    c.close()


if __name__ == "__main__":
    main()
