#!/usr/bin/env python3
"""W8.3 — Gate permanente della correntezza (presidio ripetibile).

Regola presidiata (W8): la correntezza dei FATTI si legge SOLO dal resolver
(`api/app/facts/`). Nessun altro punto di `api/` puo' interrogare direttamente
`FactAssertion` per decidere «qual e' il valore adesso».

Sentinella: ogni riga che nomina `FactAssertion` in un file sotto `api/app/`
FUORI da `api/app/facts/`. Ogni riga cosi' individuata DEVE comparire
nell'allowlist per (file, snippet) con la sua motivazione. Un'eccezione che
ammette qualunque riga non e' un'eccezione: qui l'allowlist e' per snippet esatto.

NON presidiato qui (per costruzione, con criterio dichiarato):
- `ip_addresses.is_current`: e' il MECCANISMO DI ELEZIONE dell'IP eletto
  (F-15, W8.1.3), non una correntezza dei fatti. Il resolver non e' fonte
  esclusiva per gli IP finche' il ruolo non entra nella excl_key (pre-condizione
  W3). Presidiarlo qui sarebbe un falso positivo.
- Colonne di stato derivate di `Asset` (name/os_guess/presence_state): sono lo
  STATO derivato dall'unico derivatore `classify_asset` (F-7); leggerle e'
  legittimo, non e' ricalcolo di correntezza.
- Letture di evidenza grezza / oggetti di dominio (ObservationRaw, Event,
  ScanRun, SpeedTestResult, Finding, Suggestion, Snapshot, ActionRequest):
  non sono fatti del registry.

Uso:
    python3 scripts/w8_currency_gate.py
Esce 0 se pulito, 1 se compare un accesso nuovo non giustificato.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_APP = ROOT / "api" / "app"
FACTS_DIR = API_APP / "facts"
SENTINEL = "FactAssertion"

# Allowlist: (path relativo a repo, snippet stripped esatto) -> motivazione.
# Ogni voce e' una riga specifica, non un pattern generico.
ALLOWLIST: dict[tuple[str, str], str] = {
    (
        "api/app/models.py",
        "class FactAssertion(Base):",
    ): "models: DEFINIZIONE ORM della tabella. Non e' una lettura di correntezza.",
    (
        "api/app/bootstrap.py",
        "from app.models import FactAssertion, IdentityEvidence, IdentityLinkProposal, Switch, User  # noqa: F401 — create_all",
    ): "bootstrap: import per la registrazione dei modelli in create_all (schema). Nessuna query.",
    (
        "api/app/routers/admin.py",
        "from app.models import FactAssertion",
    ): "admin: import per diagnostica read-only (shadow-stats COUNT + conflitti I3). Nessuna lettura di correntezza.",
    (
        "api/app/routers/admin.py",
        "rows = int(db.scalar(select(func.count()).select_from(FactAssertion)) or 0)",
    ): "admin /facts/shadow-stats: COUNT totale righe (osservabilita' breaker), non una lettura del valore corrente.",
    (
        "api/app/routers/admin.py",
        "select(FactAssertion)",
    ): "admin /facts/conflicts: elenco divergenze conflict_review (I3), state='historical' — NON current.",
    (
        "api/app/routers/admin.py",
        'FactAssertion.reason == "conflict_review",',
    ): "admin /facts/conflicts: filtro divergenze I3 (non correntezza).",
    (
        "api/app/routers/admin.py",
        'FactAssertion.state == "historical",',
    ): "admin /facts/conflicts: esplicitamente state='historical', l'opposto di current.",
    (
        "api/app/routers/admin.py",
        ".order_by(FactAssertion.last_seen_at.desc(), FactAssertion.id.desc())",
    ): "admin /facts/conflicts: ordinamento di DISPLAY delle divergenze storiche.",
}


def _rel(p: Path) -> str:
    return str(p.relative_to(ROOT)).replace("\\", "/")


def scan() -> tuple[list[tuple[str, int, str]], list[tuple[str, int, str, str]]]:
    violations: list[tuple[str, int, str]] = []
    accounted: list[tuple[str, int, str, str]] = []
    for path in sorted(API_APP.rglob("*.py")):
        if FACTS_DIR in path.parents or path == FACTS_DIR:
            continue
        rel = _rel(path)
        for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if SENTINEL not in raw:
                continue
            snippet = raw.strip()
            reason = ALLOWLIST.get((rel, snippet))
            if reason is None:
                violations.append((rel, lineno, snippet))
            else:
                accounted.append((rel, lineno, snippet, reason))
    return violations, accounted


def main() -> int:
    violations, accounted = scan()
    print("== W8 CURRENCY GATE ==")
    print(f"scope: {_rel(API_APP)}/**  (escluso {_rel(FACTS_DIR)}/**)")
    print(f"sentinella: righe che nominano `{SENTINEL}`\n")

    print(f"ECCEZIONI GIUSTIFICATE (accounted): {len(accounted)}")
    for rel, lineno, snippet, reason in accounted:
        print(f"  OK  {rel}:{lineno}  | {snippet}")
        print(f"      → {reason}")

    print(f"\nVIOLAZIONI (accessi nuovi non giustificati): {len(violations)}")
    for rel, lineno, snippet in violations:
        print(f"  FAIL {rel}:{lineno}  | {snippet}")

    print("\nRISULTATO:", "PASS" if not violations else "FAIL")
    return 1 if violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
