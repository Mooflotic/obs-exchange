"""W8.5 / W8-fix — Gate di equivalenza G8, eseguibile · discriminante · esteso.

Cosa fa: confronta, per ogni asset e a writer fermi, la correntezza prodotta dal
RESOLVER con la superficie osservata dai consumatori, e enumera OGNI differenza
per id in quattro classi:
  RESOLVER  R!=None e consumatore == R          (il valore viene dal fatto)
  FALLBACK  R==None e consumatore ha un valore   (I2: assenza del fatto, ripiego
            sullo STATO derivato — legittimo, non una divergenza)
  ABSENT    R==None e consumatore assente         (I2: assenza dichiarata)
  DIVERGE   R!=None e consumatore != R            (sospetto calcolo locale — (c))
Un solo DIVERGE ⇒ RISULTATO FAIL. Nessuna tolleranza percentuale.

Fatti confrontati:
  - asset.name : resolver.current("asset.name") vs presentation_name_for_asset().
    NB (T1): presentation_name_for_asset NON è un wrapper puro del resolver — usa
    il resolver per il nome chassis-scoped ma RIPIEGA su Asset.name (stato
    derivato) quando il fatto è assente. Quindi su asset.name la classe DIVERGE è
    TAUTOLOGICAMENTE 0 tra funzione interna e resolver: la discriminazione reale
    è provata da --mutate-probe (sotto) e, se abilitata, dal confronto con
    l'ENDPOINT GET /api/assets/{id} (superficie consumer reale, env OBS_G8_*).
  - os.guess  : resolver.current("os.guess") vs Asset.os_guess (COLONNA di stato
    derivata — store DIVERSO dal fact store: confronto NON tautologico).

Controllo negativo (--mutate-probe <id>): monkeypatch IN-PROCESSO della sola
funzione di presentazione perché restituisca una sentinella per quell'unico id.
G8 deve riportare DIVERGE=1 esattamente su quell'id e RISULTATO FAIL. Prova che
il gate sa fallire.

READ-ONLY (T4e): il gate NON scrive mai sul DB (db.rollback() finale, nessun
commit). «mai commit» si riferisce alla TRANSAZIONE DB, non al versionamento git:
questo file È committato come tooling versionato (repo + obs-exchange). Durante
G8 nessuna azione viene innescata sull'api (unico writer vivo): sono sole letture.

Uso (nel container api, a collector fermo):
    docker compose exec -T api python3 - < scripts/w8_g8_equivalence.py
    docker compose exec -T api python3 - < scripts/w8_g8_equivalence.py --mutate-probe 3
Env opzionali per il confronto con l'endpoint (T4b):
    OBS_G8_BASE (es. http://127.0.0.1:8000)  OBS_G8_TOKEN (cookie obs_session)
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, "/app")

MUTATE_SENTINEL = "__G8_MUTATE_SENTINEL__"


def _import_smoke():
    """T4a — verifica che ogni simbolo importato esista davvero (no import fittizi)."""
    problems = []
    syms = {}
    try:
        from app.facts.resolver import current, subject_of
        syms["current"] = current
        syms["subject_of"] = subject_of
    except Exception as exc:  # noqa: BLE001
        problems.append(f"app.facts.resolver.current/subject_of: {exc!r}")
    try:
        from app.config import get_settings
        syms["get_settings"] = get_settings
    except Exception as exc:  # noqa: BLE001
        problems.append(f"app.config.get_settings: {exc!r}")
    try:
        from app.models import Asset
        syms["Asset"] = Asset
    except Exception as exc:  # noqa: BLE001
        problems.append(f"app.models.Asset: {exc!r}")
    try:
        import app.services.name_proposal_chassis as npc
        if not hasattr(npc, "presentation_name_for_asset"):
            problems.append("name_proposal_chassis.presentation_name_for_asset: assente")
        syms["npc"] = npc
    except Exception as exc:  # noqa: BLE001
        problems.append(f"app.services.name_proposal_chassis: {exc!r}")
    print("== G8 IMPORT-SMOKE ==")
    for name in ("current", "subject_of", "get_settings", "Asset", "npc"):
        ok = name in syms
        print(f"  {'OK ' if ok else 'FAIL'} {name}")
    if problems:
        for p in problems:
            print(f"  ! {p}")
        print("IMPORT-SMOKE: FAIL")
        raise SystemExit(2)
    print("IMPORT-SMOKE: PASS\n")
    return syms


def _norm(v) -> str | None:
    s = " ".join(str(v or "").strip().split())
    return s or None


def _api_name(base: str, token: str, asset_id: int) -> tuple[str | None, str]:
    """T4b — nome dalla superficie consumer reale GET /api/assets/{id} (read-only)."""
    import json
    import urllib.request

    url = f"{base.rstrip('/')}/api/assets/{asset_id}"
    req = urllib.request.Request(url, headers={"Cookie": f"obs_session={token}"})
    with urllib.request.urlopen(req, timeout=8) as r:  # noqa: S310
        d = json.loads(r.read().decode("utf-8"))
    name = d.get("chassis_canonical_name") or d.get("display_name") or d.get("name")
    return _norm(name), "chassis_canonical_name|display_name|name"


def _classify(r, consumer):
    if r is not None and consumer == r:
        return "RESOLVER"
    if r is None and consumer is not None:
        return "FALLBACK"
    if r is None and consumer is None:
        return "ABSENT"
    return "DIVERGE"


def main(argv: list[str]) -> int:
    mutate_id = None
    if "--mutate-probe" in argv:
        i = argv.index("--mutate-probe")
        try:
            mutate_id = int(argv[i + 1])
        except (IndexError, ValueError):
            print("--mutate-probe richiede un asset_id intero")
            return 2

    syms = _import_smoke()
    current = syms["current"]
    subject_of = syms["subject_of"]
    get_settings = syms["get_settings"]
    Asset = syms["Asset"]
    npc = syms["npc"]

    from sqlalchemy import create_engine, select
    from sqlalchemy.orm import sessionmaker

    base = os.environ.get("OBS_G8_BASE")
    token = os.environ.get("OBS_G8_TOKEN")
    api_enabled = bool(base and token)

    # T4d — monkeypatch SOLO della funzione di presentazione, in-processo, per un id.
    orig_pna = npc.presentation_name_for_asset
    if mutate_id is not None:
        def _patched(db, asset):
            if getattr(asset, "id", None) == mutate_id:
                return MUTATE_SENTINEL
            return orig_pna(db, asset)
        npc.presentation_name_for_asset = _patched
        print(f"== MUTATE-PROBE attivo su id={mutate_id} (sentinella di presentazione) ==\n")

    settings = get_settings()
    db = sessionmaker(bind=create_engine(f"sqlite:///{settings.sqlite_path}"))()
    fail = False
    try:
        # T7.0(b) — pre-condizione del controllo negativo: il probe è valido SOLO se
        # l'asset ha asset.name corrente dal resolver (R!=None). Altrimenti la classe
        # onesta sarebbe FALLBACK e il probe non eserciterebbe il ramo DIVERGE.
        if mutate_id is not None:
            probe_asset = db.get(Asset, mutate_id)
            pr = None
            if probe_asset is not None:
                pst, psid = subject_of("asset.name", probe_asset)
                prow = current(db, pst, psid, "asset.name")
                pr = _norm(prow.value_norm) if prow is not None else None
            if pr is None:
                print(f"MUTATE-PROBE NON VALIDO: l'asset {mutate_id} non ha asset.name "
                      f"corrente dal resolver; il probe non eserciterebbe il ramo DIVERGE")
                return 2
            print(f"MUTATE-PROBE pre-condizione OK: id={mutate_id} R={pr!r}\n")

        assets = db.scalars(select(Asset)).all()

        def run_fact(fact_key, consumer_fn, label):
            nonlocal fail
            buckets = {"RESOLVER": [], "FALLBACK": [], "ABSENT": [], "DIVERGE": []}
            for a in assets:
                st, sid = subject_of(fact_key, a)
                row = current(db, st, sid, fact_key)
                r = _norm(row.value_norm) if row is not None else None
                c = consumer_fn(a)
                cls = _classify(r, c)
                if cls in ("DIVERGE", "FALLBACK"):
                    buckets[cls].append((a.id, r, c))
                else:
                    buckets[cls].append(a.id)
            print(f"== G8 {fact_key} — consumatore: {label} ==")
            print(f"  RESOLVER={len(buckets['RESOLVER'])} FALLBACK={len(buckets['FALLBACK'])} "
                  f"ABSENT={len(buckets['ABSENT'])} DIVERGE={len(buckets['DIVERGE'])}")
            print(f"  RESOLVER ids: {sorted(buckets['RESOLVER'])}")
            print("  FALLBACK (R=None → stato derivato, I2):")
            for aid, r, c in sorted(buckets["FALLBACK"]):
                print(f"    id={aid} resolver=None consumatore={c!r}")
            print(f"  ABSENT ids (R=None, consumatore=None, I2): {sorted(buckets['ABSENT'])}")
            print("  DIVERGE (sospetto calcolo locale, (c)):")
            for aid, r, c in sorted(buckets["DIVERGE"]):
                print(f"    id={aid} resolver={r!r} consumatore={c!r}")
            if buckets["DIVERGE"]:
                fail = True
            print()
            return buckets

        # asset.name — funzione interna (tautologica su DIVERGE, dichiarato T1)
        run_fact("asset.name", lambda a: _norm(npc.presentation_name_for_asset(db, a)),
                 "presentation_name_for_asset() [interna]")

        # asset.name — endpoint reale (T4b), se abilitato
        if api_enabled:
            run_fact("asset.name", lambda a: _api_name(base, token, a.id)[0],
                     f"GET /api/assets/{{id}} [{base}]")
        else:
            print("== G8 asset.name — endpoint GET /api/assets/{id} ==")
            print("  SKIP (K4): OBS_G8_BASE/OBS_G8_TOKEN non impostati; "
                  "leg non esercitata a runtime.\n")

        # os.guess — resolver vs colonna di stato derivata (store diverso: non tautologico)
        run_fact("os.guess", lambda a: _norm(getattr(a, "os_guess", None)),
                 "Asset.os_guess [colonna derivata]")

        print("RISULTATO G8:", "FAIL" if fail else "PASS")
        if mutate_id is not None:
            print(f"MUTATE-PROBE: atteso DIVERGE=1 su id={mutate_id} e FAIL — "
                  f"{'confermato' if fail else 'NON confermato (controllo negativo rotto)'}")
        return 1 if fail else 0
    finally:
        npc.presentation_name_for_asset = orig_pna
        db.rollback()
        db.close()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
