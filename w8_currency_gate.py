#!/usr/bin/env python3
"""W8.3 / W8-fix — Gate permanente della correntezza (presidio statico su sorgente).

PRESIDIO STATICO SU SORGENTE — eccezione consapevole alla regola «mai test su
stringhe di codice sorgente». Motivo: questo NON verifica il comportamento del
codice, verifica un INVARIANTE ARCHITETTURALE («la correntezza dei fatti si
legge solo dal resolver `api/app/facts/`»). Un invariante di questo tipo si può
presidiare solo staticamente: a runtime un consumatore che ricalcola il corrente
darebbe comunque un risultato «plausibile», quindi non fallirebbe alcun test di
comportamento. Perciò il gate scandisce il sorgente e fallisce se compare un
accesso ai fatti fuori dal resolver.

Correzioni W8-fix (buchi dimostrati nella review di W8):
  B1(i)  ora la sentinella copre ANCHE il nome tabella grezzo `fact_assertions`
         in contesto SQL (`text("… FROM fact_assertions …")`), non solo il
         simbolo ORM `FactAssertion`.
  B1(ii) allowlist per (file, snippet, N): autorizza ESATTAMENTE N righe. N+1 =
         violazione di conteggio (riporta atteso vs osservato). Inoltre ogni riga
         che contiene un riferimento a fatti (FactAssertion|fact_assertions|
         fact_key) E il literal `current` è SEMPRE una violazione (una lettura di
         correntezza), anche se il singolo simbolo sarebbe in allowlist.
  B1(iii) scope allargato al censimento dichiarato: `api/**`, `scripts/**`,
         `collector/**`.

Uso:
    python3 scripts/w8_currency_gate.py            # scansione repo reale
    python3 scripts/w8_currency_gate.py --selftest # controllo negativo (sa fallire?)
Esce 0 se pulito, 1 se compare una violazione (o se il selftest non trova
esattamente le violazioni attese).
"""

from __future__ import annotations

import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SCAN_DIRS = ("api", "scripts", "collector")
EXCLUDE_DIRS = ("api/app/facts",)  # il resolver È la fonte: qui i fatti si leggono
EXCLUDE_FILES = (
    "scripts/w8_currency_gate.py",   # questo file: contiene le sentinelle come dato
    "scripts/w8_g8_equivalence.py",  # gate G8: contiene i fact_key come dato
)

FACT_TOKENS = ("FactAssertion", "fact_assertions", "fact_key")
# Raw-SQL sul nome tabella grezzo: solo dentro una CHIAMATA SQL reale (text/execute),
# così `text("… FROM fact_assertions …")` è colto ma prosa/DDL(op.)/label/log no.
RAW_SQL_CALLS = ("text(", ".execute(", ".exec_driver_sql(")
# COMBO: `current` come VALORE DI STATO quotato (state='current' / state=="current" /
# filter_by(state="current")), NON come sottostringa di un identificatore
# (es. l'indice `uq_fact_assertions_current_slot`) né come label (`current={x}`).
CURRENT_VALUE_RE = re.compile(r"""['"]current['"]""")

# Allowlist per (relpath, snippet_stripped) -> (occorrenze_attese, motivazione).
# Autorizza ESATTAMENTE N righe identiche a snippet in quel file.
ALLOWLIST: dict[tuple[str, str], tuple[int, str]] = {
    ("api/app/models.py", "class FactAssertion(Base):"): (
        1, "models: DEFINIZIONE ORM della tabella (non una lettura)."),
    ("api/app/bootstrap.py",
     "from app.models import FactAssertion, IdentityEvidence, IdentityLinkProposal, Switch, User  # noqa: F401 — create_all"): (
        1, "bootstrap: import per registrazione modelli in create_all (nessuna query)."),
    ("api/app/routers/admin.py", "from app.models import FactAssertion"): (
        2, "admin: import per diagnostica read-only (shadow-stats COUNT + conflitti I3)."),
    ("api/app/routers/admin.py",
     "rows = int(db.scalar(select(func.count()).select_from(FactAssertion)) or 0)"): (
        1, "admin /facts/shadow-stats: COUNT righe (osservabilità breaker), non un valore corrente."),
    ("api/app/routers/admin.py", "select(FactAssertion)"): (
        1, "admin /facts/conflicts: divergenze conflict_review, state='historical' (I3), NON current."),
    ("api/app/routers/admin.py", 'FactAssertion.reason == "conflict_review",'): (
        1, "admin /facts/conflicts: filtro divergenze I3."),
    ("api/app/routers/admin.py", 'FactAssertion.state == "historical",'): (
        1, "admin /facts/conflicts: esplicitamente state='historical', l'opposto di current."),
    ("api/app/routers/admin.py",
     ".order_by(FactAssertion.last_seen_at.desc(), FactAssertion.id.desc())"): (
        1, "admin /facts/conflicts: ordinamento di DISPLAY delle divergenze storiche."),
}


def _rel(p: Path, root: Path) -> str:
    return str(p.relative_to(root)).replace("\\", "/")


def _is_excluded(rel: str) -> bool:
    if rel in EXCLUDE_FILES:
        return True
    return any(rel == d or rel.startswith(d + "/") for d in EXCLUDE_DIRS)


def _classify_line(line: str) -> tuple[str, str] | None:
    """Return (kind, snippet) if the line touches the fact store, else None.

    kind ∈ {"combo", "symbol", "sql"}. "combo" è SEMPRE violazione.
    """
    strip = line.strip()
    has_token = any(tok in line for tok in FACT_TOKENS)
    if has_token and CURRENT_VALUE_RE.search(line):
        return ("combo", strip)
    if "FactAssertion" in line:
        return ("symbol", strip)
    if "fact_assertions" in line and any(k in line for k in RAW_SQL_CALLS):
        return ("sql", strip)
    return None


def scan(root: Path, allowlist: dict[tuple[str, str], tuple[int, str]]):
    """Return (files_scanned, accounted, violations)."""
    files_scanned = 0
    # (rel, snippet) -> {"kind": kind, "lines": [lineno,...]}
    groups: dict[tuple[str, str], dict] = {}
    combos: list[tuple[str, int, str]] = []
    for d in SCAN_DIRS:
        base = root / d
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.py")):
            rel = _rel(path, root)
            if _is_excluded(rel):
                continue
            files_scanned += 1
            for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                res = _classify_line(raw)
                if res is None:
                    continue
                kind, snippet = res
                if kind == "combo":
                    combos.append((rel, lineno, snippet))
                    continue
                g = groups.setdefault((rel, snippet), {"kind": kind, "lines": []})
                g["lines"].append(lineno)

    accounted: list[dict] = []
    violations: list[dict] = []

    # Combo: sempre violazioni (lettura di correntezza: fact-token + "current").
    for rel, lineno, snippet in combos:
        violations.append({
            "rel": rel, "lines": [lineno], "snippet": snippet,
            "reason": "COMBO fact-token + 'current' (lettura di correntezza)",
            "atteso": 0, "osservato": 1,
        })

    for (rel, snippet), g in sorted(groups.items()):
        lines = g["lines"]
        entry = allowlist.get((rel, snippet))
        if entry is None:
            violations.append({
                "rel": rel, "lines": lines, "snippet": snippet,
                "reason": f"accesso ai fatti fuori da facts/ non in allowlist ({g['kind']})",
                "atteso": 0, "osservato": len(lines),
            })
            continue
        exp, reason = entry
        if len(lines) == exp:
            accounted.append({
                "rel": rel, "lines": lines, "snippet": snippet,
                "reason": reason, "atteso": exp, "osservato": len(lines),
            })
        else:
            violations.append({
                "rel": rel, "lines": lines, "snippet": snippet,
                "reason": f"CONTEGGIO: atteso {exp}, osservato {len(lines)} — {reason}",
                "atteso": exp, "osservato": len(lines),
            })
    return files_scanned, accounted, violations


def _print_report(root: Path, files_scanned: int, accounted, violations, allowlist) -> None:
    print("== W8 CURRENCY GATE (indurito, W8-fix) ==")
    print(f"root: {root}")
    print("sentinelle: simbolo ORM 'FactAssertion' · tabella grezza 'fact_assertions' "
          "in chiamata SQL (text/execute) · COMBO (fact-token "
          f"{'|'.join(FACT_TOKENS)}) + valore di stato quotato 'current'")
    print(f"scope: {', '.join(d + '/**' for d in SCAN_DIRS)}")
    print("esclusioni:")
    for d in EXCLUDE_DIRS:
        print(f"  - {d}/**  (il resolver È la fonte della correntezza)")
    for f in EXCLUDE_FILES:
        print(f"  - {f}  (contiene le sentinelle/fact_key come dato)")
    print(f"file scansionati: {files_scanned}")
    print(f"voci allowlist: {len(allowlist)}")
    print()
    print(f"ECCEZIONI GIUSTIFICATE (accounted): {len(accounted)}")
    for a in accounted:
        locs = ",".join(str(x) for x in a["lines"])
        print(f"  OK  {a['rel']}:{locs}  (atteso {a['atteso']}, osservato {a['osservato']})")
        print(f"      | {a['snippet']}")
        print(f"      → {a['reason']}")
    print()
    print(f"VIOLAZIONI: {len(violations)}")
    for v in violations:
        locs = ",".join(str(x) for x in v["lines"])
        print(f"  FAIL {v['rel']}:{locs}  (atteso {v['atteso']}, osservato {v['osservato']})")
        print(f"      | {v['snippet']}")
        print(f"      → {v['reason']}")
    print()
    print("RISULTATO:", "PASS" if not violations else "FAIL")


def run_repo() -> int:
    files_scanned, accounted, violations = scan(ROOT, ALLOWLIST)
    _print_report(ROOT, files_scanned, accounted, violations, ALLOWLIST)
    return 1 if violations else 0


def run_selftest() -> int:
    """Controllo negativo: corpus sintetico in dir TEMPORANEA (mai in api/, mai committato).

    Quattro file:
      1. definizione ORM lecita (accounted)
      2. lettura SQL grezza su fact_assertions con state='current' (violazione)
      3. composizione filter_by(fact_key=…, state='current') (violazione)
      4. ripetizione extra di una riga in allowlist (violazione di conteggio)
    Atteso: 3 gruppi di violazione (file 2,3,4), 1 gruppo accounted (file 1).
    """
    tmp = Path(tempfile.mkdtemp(prefix="w8gate_selftest_"))
    try:
        api = tmp / "api" / "app"
        api.mkdir(parents=True)
        orm_line = "class FactAssertion(Base):"
        (api / "file1_orm.py").write_text(
            f"{orm_line}\n    __tablename__ = 'fact_assertions'\n", encoding="utf-8")
        (api / "file2_rawsql.py").write_text(
            'stmt = text("SELECT value_norm FROM fact_assertions '
            "WHERE fact_key='asset.name' AND state='current' ORDER BY id DESC LIMIT 1\")\n",
            encoding="utf-8")
        (api / "file3_filterby.py").write_text(
            'row = db.scalars(select(FactAssertion)'
            '.filter_by(fact_key="asset.name", state="current")).first()\n',
            encoding="utf-8")
        (api / "file4_count.py").write_text(
            f"{orm_line}\n{orm_line}\n", encoding="utf-8")

        allowlist = {
            ("api/app/file1_orm.py", orm_line): (1, "selftest: ORM def lecita"),
            ("api/app/file4_count.py", orm_line): (1, "selftest: autorizzata 1 volta"),
        }
        files_scanned, accounted, violations = scan(tmp, allowlist)
        _print_report(tmp, files_scanned, accounted, violations, allowlist)

        viol_files = sorted({v["rel"].split("/")[-1] for v in violations})
        expected_files = ["file2_rawsql.py", "file3_filterby.py", "file4_count.py"]
        ok = (len(violations) == 3 and viol_files == expected_files and len(accounted) == 1)
        print()
        print(f"SELFTEST atteso: 3 violazioni {expected_files} + 1 accounted (file1)")
        print(f"SELFTEST osservato: {len(violations)} violazioni {viol_files} + "
              f"{len(accounted)} accounted")
        print("SELFTEST:", "PASS (il gate sa fallire)" if ok else "FAIL (gate non discrimina)")
        return 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return run_selftest()
    return run_repo()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
