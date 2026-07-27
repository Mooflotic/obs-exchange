"""W8.5 G8 — equivalenza della correntezza (writer fermi, read-only, mai commit).

Dimostra che la correntezza del NOME (unico fatto di identita' consumer-facing
pienamente nel resolver) e' prodotta SOLO dal resolver, e che la presentazione
NON diverge da esso per un calcolo locale parallelo.

Per ogni asset confronta:
  R = resolver.current("asset.name") sul subject corretto (chassis o asset)
  P = presentation_name_for_asset(db, asset)  (consumer-facing)
  S = asset.name (colonna di stato derivata, F-7)

Classi enumerate per id:
  - RESOLVER : P == R (la presentazione viene dal fatto risolto)
  - FALLBACK : R is None, P from derived state (I2: assenza del fatto dichiarata,
               ripiego legittimo sullo stato derivato F-7 — NON una divergenza)
  - DIVERGE  : R is not None e P != R  → sospetto calcolo locale (deve essere 0: (c))
  - ABSENT   : R is None e P is None   → assenza dichiarata (I2)

Un solo caso DIVERGE ⇒ STOP (regressione (c)). Nessuna tolleranza percentuale.
Va eseguito a collector fermo (api unico writer), `now` implicito nel resolver.
"""

from __future__ import annotations

import sys

sys.path.insert(0, "/app")

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.config import get_settings
from app.facts.resolver import current, subject_of
from app.models import Asset
from app.services.name_proposal_chassis import presentation_name_for_asset


def main() -> int:
    settings = get_settings()
    db = sessionmaker(bind=create_engine(f"sqlite:///{settings.sqlite_path}"))()
    try:
        assets = db.scalars(select(Asset)).all()
        resolver_ids: list[int] = []
        fallback: list[tuple[int, str]] = []
        diverge: list[tuple[int, str, str]] = []
        absent: list[int] = []
        for a in assets:
            st, sid = subject_of("asset.name", a)
            row = current(db, st, sid, "asset.name")
            r = (row.value_norm or "").strip() if row is not None else None
            p = presentation_name_for_asset(db, a)
            p = (p or "").strip() or None
            if r is not None and p == r:
                resolver_ids.append(a.id)
            elif r is None and p is not None:
                fallback.append((a.id, p))
            elif r is not None and p != r:
                diverge.append((a.id, r, p or ""))
            else:
                absent.append(a.id)
        print(
            f"G8 name currency — assets={len(assets)} "
            f"resolver={len(resolver_ids)} fallback={len(fallback)} "
            f"diverge={len(diverge)} absent={len(absent)}"
        )
        print("RESOLVER ids:", sorted(resolver_ids))
        print("FALLBACK (R=None → stato derivato, I2):")
        for aid, p in sorted(fallback):
            print(f"  id={aid} presentation={p!r}")
        print("ABSENT (R=None, P=None, I2):", sorted(absent))
        print("DIVERGE (sospetto calcolo locale — deve essere vuoto):")
        for aid, r, p in sorted(diverge):
            print(f"  id={aid} resolver={r!r} presentation={p!r}")
        print("RISULTATO:", "PASS" if not diverge else "FAIL (c)")
        return 1 if diverge else 0
    finally:
        db.rollback()
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())
