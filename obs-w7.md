# W7 — Presence: T-a uplink→portal + wire mac_ip_policy (deploy 1/2, 0.10.58)

Wave presence. Correzioni di codice: `topology.apply_fdb_observation` (T-a) e
`inventory.reconcile_asset_presence` (wire additivo). Bump **0.10.58**. Diff integrale:
[`obs-w7.diff.txt`](obs-w7.diff.txt). F-3/F-4 intatti (chassis non fusi, segreti Fritz mai
letti). **F-7 preservato:** `classify_asset` resta l'UNICO deriver di
`trust_level`/`operational_state`; il wire è solo un segnale di presenza.

## W7.0 — Perimetro

Dentro: T-a (DEBT-FDB-UPLINK-PORTAL) e wire `mac_ip_policy` come **segnale di presenza**
(regole #1/#4). Fuori (dichiarato): riclassificazione ampia della policy (regole #3/#5,
`stale`/`superseded`) → **deploy 2/2** (W7.2.3, blast-radius alto — decisione dominio
Michele). Fuori wave: W8 enforcement, backfill W3, revisione UI/UX.

## W7.1 — Correntezza dei consumatori

`reconcile_asset_presence` legge evidenza **corrente** già oggi: `IpAddress.is_current`,
`SwitchPort.last_fdb_at`, `presence_sources` (portal kinds da `observe_portal`),
`reachability`. Nessun fatto `stale`/`superseded` entra nello stato corrente: il wire
aggiunge SOLO segnali positivi (`present_l2_unaddressed`/`l2_only_allowed`) e **non** fa
mai entrare `stale`/`superseded` come stato. `asset.iface_ip` resta cardinalità singola
(`current_ip` = primo `is_current`). FDB ≠ ownership: il wire non crea binding né elegge
IP. I7 rispettato (nessun IP reale non eletto sparisce dalla topologia: il wire non tocca
topologia).

## W7.2 — Wire `mac_ip_policy` (deploy 1/2, additivo)

**W7.2.1 aggancio.** `classify_mac_ip_presence` è collegato in
`reconcile_asset_presence` (`inventory.py`) tramite `_mac_ip_policy_present`: costruisce
`MacIpPresenceInputs` da dati **misurati** (FDB fresco su porta legata all'asset; IP
corrente proprio; IP corrente di chassis via `_chassis_has_current_ip`; eccezione
powerline/510E da nome/categoria) e usa SOLO le decisioni della famiglia «presente» come
termine aggiuntivo di `reliable`.

**W7.2.2 confini.** Non fusione chassis (solo rollup read-only dell'IP di chassis). Non
inventa management IP (`chassis_mgmt_ip=None`, `present_l2_unaddressed` resta tale). Non
forza mai `stale`/`superseded`: quelle decisioni della policy **non** sono usate qui
(F-7). `present_l2_unaddressed` è **dichiarato** dalla freschezza FDB misurata, mai
dedotto dal solo IP di chassis (test `test_w762_present_l2_unaddressed_declared_not_deduced`).

**W7.2.3 misura pre-attivazione + split.** Read-only prod:
- Blast-radius della policy PIENA (regole #3/#5 incluse) = **52/151 asset** in disaccordo
  con `operational_state`, inclusi device **oggi `active`** che la policy marcherebbe
  `stale`: FritzBox Router (id=112), FRITZ!Powerline 510E (id=7), Sky box (id=8/82/88/135…).
  Attivarle in blocco = regressioni (c) e `stale`/`superseded` nello stato corrente →
  **VIETATO in questo deploy**. Rinviato al deploy 2/2 (decisione dominio: quali device
  attivi declassare — Michele).
- Wire **ristretto** (solo `present_l2_unaddressed`/`l2_only_allowed`, additivo):
  **0 hit correnti ⇒ 0 cambi di `operational_state`**. Inerte oggi; esercitato dai test
  unitari (`test_w7_consumers`, K4).

## W7.3 — T-a (DEBT-FDB-UPLINK-PORTAL)

**Diagnosi.** `apply_fdb_observation` (`api/app/services/topology.py`, righe ~1252) faceva
`interface.interface_role = role_for_interface_on_port(...)` **prima** della guardia
portale: su un singolo hit FDB una porta a MAC-singolo → `role_for_interface_on_port`
ritorna `endpoint` (`interface_roles.py:131`), declassando un'interfaccia `uplink` → la
guardia `role in {uplink,infra,virtual}` falliva → `observe_portal` valorizzava
`portal_last_seen`. Presenza attribuita a una porta uplink.

**Fix (W7.3.1).** Un hit FDB per-porta NON declassa più un'interfaccia strutturale
(`uplink`/`infra`) a `endpoint`; i downgrade restano di competenza del reclassify globale
(`role_for_interface_global`). Guardia portale invariata. Test T-a
(`test_m2_discovery::test_fdb_skips_observe_portal_on_uplink_role`) VERDE, non indebolito.

**W7.3.2 effetto su asset reali.** Il fix NON azzera retroattivamente `portal_last_seen`:
riguarda solo le FUTURE osservazioni FDB su interfacce strutturali. Effetto su presence al
boot = nullo (misurato: G7 changes=0). Effetto atteso su structural: **0** (boot1
`needs_apply=false`, `structural=0`).

## W7.4 — Gate G7 (equivalenza a writer fermi)

Collector fermo, `now` implicito nel reconcile idempotente. Confronto per id di
`(operational_state, presence_state, trust_level)` prima/dopo la riesecuzione del
`reconcile_asset_presence` DEPLOYATO:

`G7 reconcile equivalence — assets=151 changes=0`

**Zero differenze** → nessun (a), nessun (b), nessun (c). Equivalenza piena: il wire
additivo e il fix T-a non spostano lo stato corrente. (Topologia: il wire non la tocca;
T-a cambia solo osservazioni FDB future su uplink, non lo stato persistito.)

## W7.5 — Previsioni (dichiarate prima del deploy)

boot1 `needs_apply=false · T_backup=0 · structural=0`; G7 `changes=0`; wp_gate
CONVERGENZA=OK; regime invariato (assets=151, ip_current=100, NP=409/pending=78,
FA=261/cur=68, AD=68, breaker=closed, observations=0); best_guess/G6 invariati (nessun
cambio naming). **Tutte confermate.**

## W7.6 — Test (nodi nominati)

- `test_w7_consumers` (nuovo, 5): chassis con ≥1 IP mantiene presente il membro FDB-fresh
  (`present_l2_unaddressed`); dichiarato-non-dedotto; eccezione powerline; wire additivo
  che non forza `stale` (F-7).
- `test_m2_discovery` (7, T-a verde). Nodi presence/trust/scans nominati verdi (94 nel
  gruppo). Gate I6 `rg 'scoreSpecificity|specificity' api/` vuoto.

## W7.7 — Deploy 0.10.58 e gate

Bump `0.10.58` (`VERSION`, `web/package.json`). Deploy `scripts/deploy.sh api` (snapshot
pre-deploy + rsync + backup_rotate + rebuild). Codice: `topology.py`, `inventory.py`.

Assert post-deploy (una riga):
`0.10.58: boot1 version=0.10.58 · needs_apply=false · needs_backup=false · T_backup=0 · T_total=9.104s · G7 reconcile changes=0 · wire hits=0/changes=0 · wp_gate CONVERGENZA=OK (0→0→0) · assets=151 · ip_current=100 · NP=409(pending=78) · FA=261(cur=68) · AD=68 · breaker=closed · observations=0 · I6=vuoto`

**Delta enumerati per id:** nessuno (G7 changes=0).

### GATE W7 (deploy 1/2) — VERDE

1. T-a chiuso, test verde non indebolito — ✓
2. Wire `mac_ip_policy` additivo, F-7 intatto, `present_l2_unaddressed` dichiarato — ✓
3. G7 equivalenza `changes=0` (nessun (c)) — ✓
4. Convergenza al regime (`structural=0`, `needs_apply=false`) — ✓
5. Split ampio dichiarato e misurato (52/151) rinviato al deploy 2/2 — ✓

**Rollback:** revert bump + deploy tag `v0.10.57`. Non necessario (gate verdi).

## Follow-up dichiarato (deploy 2/2, NON in questo deploy)

Riclassificazione ampia `mac_ip_policy` (regole #3/#5): richiede la conferma di dominio su
quali device oggi `active` declassare a `stale`/`superseded` (FritzBox router, powerline,
Sky box — 52/151). Da fare come deploy separato con G7 dedicato (enumerazione per id,
un solo (c) → STOP), previa decisione di Michele.

## Diff

`obs-w7.diff.txt` — file toccati (integrale): `api/app/services/topology.py`,
`api/app/services/inventory.py`, `VERSION`, `web/package.json`, `CHANGELOG.md`,
`docs/KNOWN_DEBT.md`, `tests/test_w7_consumers.py` (nuovo), `scripts/w7_macip_blast.py`,
`scripts/w7_wire_predict.py`, `scripts/w7_g7.py` (nuovi). **Esclusi dichiarati:**
`docs/obs-w7.md` (questo report) e `docs/obs-w7.diff.txt` (l'artefatto stesso).
