# W5 — Migrazione dei consumatori dello stato corrente (0.10.54)

Parte a gate W-P verde (0.10.53). Migrazione di sola LETTURA. Segreti Fritz mai toccati.

## W5.0 — Perimetro e censimento (classe b, W4d.1.2)

Migrati/verificati i lettori di stato corrente noti:
- **API asset (`routers/assets.py` `_serialize`)** — nome display già via resolver
  (`presentation_name_for_asset` → `current("chassis", …, "asset.name")`, fallback I2).
- **Oggi / Dossier / Inventory** — consumano il payload `_serialize` (nome canonico via
  resolver; IP reali multi-valore non collassati).
- **`_resolve_ap_asset` in `topology.py`** — unico punto backend che usava `is_current`
  per RISOLVERE un asset per IP (DEBT-TOPO-IP-CONTEXTUAL): migrato.

Fuori perimetro (dichiarato): fingerprinting/AI/generazione proposte (W6); scans, conflitti,
wire `mac_ip_policy` (W7). La presenza è stata trattata in W-P.

## W5.1 — Regole di migrazione applicate

- **W5.1.1:** i consumatori migrati leggono dal resolver (`current`/`current_map`/`history`);
  nessuna reimplementazione della correntezza nel consumatore. Il nome canonico delle viste
  passa da `presentation_name_for_asset` (resolver, subject=chassis).
- **W5.1.2:** `stale`/`superseded` non entrano nel corrente (garantito da `resolver.current`,
  che filtra `state="current"`); la storia resta leggibile via `history`.
- **W5.1.3 (IP multi-valore — dichiarato):** `asset.iface_ip` ha `cardinality=single` (solo
  IP eletto). Il Fritz ha 5 IP simultanei. Finché il **ruolo** non è nella `excl_key`
  (pre-condizione W3 — DEBT-IFACE-IP-CARDINALITY-ROLE), il resolver NON è fonte esclusiva per
  gli IP: la UI continua a mostrare **tutti gli IP reali** (nessun collasso). Nessuna
  sostituzione della lista IP di `_serialize` con l'IP eletto del resolver.
- **W5.1.4:** nessuna scrittura su colonne di Asset né su campi confrontati dal reconcile —
  migrazione di sola lettura.
- **W5.1.5 (S1):** `resolve_asset_by_ip_at` che ritorna None non fa crollare il consumatore:
  fall-through dichiarato (I2).

## W5 — Modifica di codice: `_resolve_ap_asset` (DEBT-TOPO-IP-CONTEXTUAL)

Prima: fallback per-IP `select(Asset)…where(IpAddress.ip==ap_ip, is_current==True)` → risolveva
l'AP con chi detiene l'IP ADESSO.
Dopo: `resolve_asset_by_ip_at(db, ap_ip, observed_at)` con `observed_at` dal link
(`_parse_observed_at`, fallback `now`) → risolve chi DETENEVA l'IP al momento
dell'associazione. Tie temporale → None → fall-through all'euristica sul nome (I2, nessun
proprietario indovinato). `is_current` non toccato alla cieca su multi-NIC storiche (W5.4.6).

## W5.2 — Gate di equivalenza G5 (writer fermi)

Collector fermo, api unico writer. Confronto per ogni associazione Wi-Fi che ricade sul path
`ap_ip` (dopo `ap_asset_id`/`ap_mac`) fra risoluzione vecchia (`is_current`) e nuova
(contestuale `@observed_at`):

`G5 AP-resolution: wifi_links=62 ip_path=0 differenze=0`

- **0 differenze.** Nessuna associazione Wi-Fi ricade oggi sul path `ap_ip` (tutte risolvono
  per `ap_asset_id` o `ap_mac`). La migrazione è un **fix latente**: equivalenza-preservante
  sui dati correnti, corretta quando in futuro un IP migra fra asset.
- Classificazione differenze: (a) 0 · (b) 0 · (c) **0 regressioni** → gate verde.
- Baseline presa a **writer fermi** (evitato il falso positivo del gate 2.7 di 4b).

## W5.3 — Previsioni (PRIMA) vs osservati (DOPO)

| Metrica | Previsto | Osservato |
|---------|----------|-----------|
| differenze G5 | 0 (tutti i link Wi-Fi via id/mac) | **0** ✓ |
| campi API modificati (dati correnti) | nessuno (AP identico; nome invariato) | nessuno ✓ |
| assets | 151 | 151 |
| regime structural / needs_apply / T_backup | 0 / false / 0 (W5 non tocca il trust) | **0 / false / 0** ✓ (boot 0.10.54 T_total=9.2s) |
| breaker | closed | closed |
| unknown_source | 0 | 0 |
| ip_current / fact_assertions | mobili (osservazione) | — |

## W5.4 — Test (solo nodi nominati) — `tests/test_w5_consumers.py`

- **W5.4.6:** `_resolve_ap_asset` contestuale (AP che deteneva l'IP all'associazione, non il
  detentore `is_current`) + tie → None → fall-through sul nome.
- **W5.4.5:** chassis = un nome canonico dal resolver per ogni membro.
- **W5.4.1:** fatto assente → `presentation_name_for_asset` = None (I2, mai "").
- **W5.4.2/4.4:** `stale`/`superseded` esclusi dal corrente, storia leggibile — coperti da
  `test_facts_resolver` / `test_facts_shadow_w2` (rieseguiti).
- **W5.4.7:** rieseguiti i nodi W-P.3.6 + test W-P + test W5. **124 verdi** nel set
  consolidato. Gate I6: `rg 'scoreSpecificity|specificity' api/` vuoto (invariato).

## W5.5 — Deploy e gate

Deploy `scripts/deploy.sh api` (rebuild image, versione **0.10.54**). Boot a regime
(`needs_backup=false`, `needs_apply=false`, `T_backup=0`, `T_total=9.2s`).

**Assert (una riga) + esito G5:**
`0.10.54 W5: boot regime needs_apply=false · T_backup=0 · structural=0 · breaker=closed · assets=151 · unknown_source=0 · G5 AP-resolution wifi_links=62 ip_path=0 differenze=0 (0 regressioni) · I6=vuoto`

Gate di regime W-P (due piani consecutivi puliti) confermato al boot post-W5. Rollback: revert
del bump + deploy tag `v0.10.53`; kill switch shadow prima del rollback se il problema fosse
nel solo layer assertion.

## Note di dominio
- DEBT-TOPO-IP-CONTEXTUAL: facet «consumatore di correntezza» **chiuso**; la cardinalità/ruolo
  multi-IP resta in DEBT-IFACE-IP-CARDINALITY-ROLE (pre-condizione W3).
- IP: il ruolo nella `excl_key` NON è stato implementato (pre-condizione W3): dichiarato.

## Diff
`obs-w5.diff.txt` — file toccati: `api/app/services/topology.py`, `tests/test_w5_consumers.py`,
`scripts/w5_gate.py`, `VERSION`, `web/package.json`, `CHANGELOG.md`, `docs/KNOWN_DEBT.md`.
**Esclusi dichiarati:** `docs/obs-w5.md` (questo report) e `docs/obs-w5.diff.txt` (l'artefatto).
