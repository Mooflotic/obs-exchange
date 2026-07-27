# W-P — Presenza: un solo proprietario, stato derivato (0.10.53)

Gate BLOCCANTE per W5. Misure eseguite in produzione (Cassiopea), writer fermi dove
richiesto. Segreti Fritz mai letti/riportati.

## W-P.0 — Delta non enumerati di 0.10.52 (chiusi)

Baseline mobile: il collector è attivo, quindi `ip_current`, `fact_assertions` e `AD`
sono conteggi in movimento (elezione IP / crescita per cambiamento / finestra 24h).

### W-P.0.1 — `ip_current` 100 → 99
NON è una perdita di device: è **churn di elezione multi-IP** (DEBT-IFACE-IP-CARDINALITY-ROLE /
DEBT-TOPO-IP-CONTEXTUAL). Le righe `is_current=0` recenti sono tutte IP secondari/vpn su
interfacce multi-IP: Fritz asset 1 (`.1.4`/`.1.5`/`.1.6` secondari, `.1.9` vpn) e IP fritz
secondari su asset 34/36/40/42/50/51/108. Ad ogni ciclo l'IP eletto (primario) cambia →
`is_current` oscilla ±1. Misura live successiva: `ip_current` risalito a 100→101. È un
conteggio mobile come AD, non un evento di demotion di dispositivo.

### W-P.0.2 — `fact_assertions` 253 → 260 (+7)
Diff esatto vs backup `observatory-20260727-130350` (FA=251): i nuovi id sono 252–261.
I **+7** citati dalla baseline (253→260) sono i binding `asset.iface_ip` `source=fritz`
`state=current` creati dal ripristino Fritz (F0):

| id | fact_key | subject | source | state | value |
|----|----------|---------|--------|-------|-------|
| 254 | asset.iface_ip | interface:70 | fritz | current | 192.168.2.193 |
| 255 | asset.iface_ip | interface:6  | fritz | current | 192.168.3.24 |
| 256 | asset.iface_ip | interface:5  | fritz | current | 192.168.1.3 |
| 257 | asset.iface_ip | interface:40 | fritz | current | 192.168.2.74 |
| 258 | asset.iface_ip | interface:34 | fritz | current | 192.168.2.64 |
| 259 | asset.iface_ip | interface:42 | fritz | current | 192.168.2.80 |
| 260 | asset.iface_ip | interface:36 | fritz | current | 192.168.2.71 |

Sono **cambiamenti** (nuovi binding correnti dopo l'outage TR-064, che aveva lasciato quelle
interfacce senza binding fritz corrente), non osservazioni ripetute: invariante W4b.0.b
rispettata (lo store cresce per cambiamento). Gli id 252/253 (nmap `weak_evidence`
`historical`) sono divergenze distinte, non refresh. FA continua a crescere live per
cambiamento (id 261 = interface:112 `.2.195`).

### W-P.0.3 — `AD` 62 → 68 (+6)
Finestra mobile 24h (non conteggio stabile). Coerente col ritorno di Fritz: gli host la cui
`last_seen` è stata rinfrescata dal ciclo hostlist (17:57) sono rientrati in finestra. La
classe declassata durante l'outage (136/140/145/148, chassis 29/15/16/17) più altri membri
tornano attivi; AD misurato ora = 68. Trattato come **osservazione**, non gate.

## W-P.1 — Diagnosi MISURATA dell'asset 109 (IPOTESI A)

- **W-P.1.1 discriminante:** il MAC `D8:EC:5E:CC:1C:01` → interface 114 → **asset 109**.
  `meta.discovery.fritz.active=True`, `last_observed_at` fresco (fresh_24h=True). **Fritz VEDE
  il 109.** `meta.discovery.fritz` completo: `active=true`, `hostname="PC-D8-EC-5E-CC-1C-01"`,
  `last_observed_at=…17:57:50Z`. Portale: `portal_last_seen=null`, 0 IP correnti, chassis 23.
- **W-P.1.2 (codice):** `classify_asset` (`trust.py`) legge `name/status/is_critical/`
  `manual_overrides/infrastructure_identity` e `portal_last_seen`. `lift_fritz_quarantine_on_active`
  scriveva `trust_level`, `meta.operational_state`, `meta.trust.*`. **Insiemi disgiunti**:
  `classify` non leggeva nulla di ciò che il lift scriveva. La derivazione tornava
  `fritz_historical` (109 senza portale, non protetto) ≠ stato scritto dal lift → `structural`
  permanente (la derivazione vince a `_build_trust_plan` e disfa l'apply). L'elenco della
  differenza È la diagnosi.
- **W-P.1.4 esito:** regge l'**IPOTESI A** (Fritz vede il 109; il lift è legittimo; la
  classificazione non consumava l'evidenza consumata dal lift). Non è l'ipotesi B (trigger su
  soggetto sbagliato): `update_fritz_evidence` risolve per **MAC** e l'evidenza è sul membro
  corretto (interface 114 = asset 109).
- **W-P.1.5 classe:** divergenti reali (trust_level vs operational_state) = **1 solo → 109**
  (membro chassis 23, 1 iface, 0 IP correnti). 136 (chassis 29) è `stale_unlocated` stabile ma
  con `fritz.active=True` fresh → facet del debito; 140/145/148 hanno fritz **non** fresh
  (07-21) → restano stale correttamente; 116 coerente (`fritz_historical`, 0 iface, fritz
  inactive).

## W-P.2 — Fix: l'evidenza si scrive, lo stato si deriva

Un solo percorso determina `operational_state`/`trust_level`: la **derivazione**
`classify_asset`. Modifiche in `api/app/services/trust.py`:

1. `classify_asset` legge l'evidenza fritz-active fresca (`_has_fresh_fritz_active`, da
   `meta.discovery.fritz` con finestra staleness): fresh fritz-active → `known`, posizionato
   dopo `recent`(portale)/`protected` e **prima** del ramo portale-stale. Autorità fritz (I5
   0.90): mai `confirmed_present` (vertice portale). Nessun caso speciale su `asset_id`, nessuna
   seconda gerarchia, nessuna soglia alzata (default 24h invariato).
2. `lift_fritz_quarantine_on_active` **non scrive più lo stato**: registra l'edge nel trail di
   evidenza e ri-esegue la derivazione unica (l'evidenza autorevole è già in
   `meta.discovery.fritz`, scritta da `update_fritz_evidence`). Scope: solo record auto-hidden
   (`fritz_historical`/`stale_unlocated`); confirmed/known non toccati.
3. Mapping `livello → (operational_state, hide flags, trust meta)` estratto in
   `_apply_level_meta` + `_write_trust_state`: **un solo writer** condiviso con
   `_apply_trust_plan` (nessun secondo autore del campo).

- **W-P.2.5 (non-regressione D.0.b):** `fritz_historical` NON assorbente — evidenza fritz-active
  fresca solleva a `known`; scaduta l'evidenza il piano torna a `fritz_historical`/`stale_unlocated`
  senza oscillare. Mai `confirmed_present`.
- **W-P.2.6 (W-C):** inventory non può sollevare/smashare la quarantena — il lift è il path FRITZ
  (0.90), non inventory; `test_quarantine_zero_interfaces_inventory_cannot_set_active` verde.
- **W-P.2.7 (DEBT-PRESENCE-SOURCE-OUTAGE):** migliorato (fritz vivo → `known`, non stale) ma
  **NON chiuso**: manca la distinzione «sorgente non disponibile» vs «dispositivo assente»
  (durante un'outage l'evidenza invecchia e l'asset ridiscende). Serve un segnale di copertura
  sorgente. RESTA APERTO (no chiusura per prossimità).

## W-P.3 — Test (comportamento, non stringhe) — `tests/test_wp_presence.py`

- **W-P.3.1 round-trip:** dallo stato divergente → apply → build `structural==[]` → build `[]`
  (due piani consecutivi). Stato stabile `known/active`.
- **W-P.3.2:** fixture 109-like (NIC membro chassis, no nome, no IP, fritz fresh) → stabile,
  derivato.
- **W-P.3.3:** 109-like senza evidenza fritz (ipotesi B) → il lift NON spara; stato derivato,
  nessuna oscillazione.
- **W-P.3.4:** D.0.b fresh → `known` (mai `confirmed_present`) + reversibilità.
- **W-P.3.4b/3.5:** stale_unlocated+fritz fresh → `known` (136); fritz **non** fresh → resta
  stale (140/145/148).
- **W-P.3.6:** rieseguiti solo i nodi nominati — trust_converge, w4b_chassis, facts_resolver,
  facts_shadow_w2, m1_observation_store, mac_ip_policy, w4a_chassis_proposals, identity (evidence/
  asset/migrate), T-b/T-e/T-f (nmap/printer/ssdp/topo/ingest), oggiTriage/oggiProblems/
  observatoryUx/portPresentation/topologyLayout. **Tutti verdi.** Non è «suite verde».
- **Gate I6:** `rg 'scoreSpecificity|specificity' api/` → **vuoto**.

## W-P.4 — Previsioni (PRIMA) vs osservati (DOPO)

| Metrica | Previsto | Osservato |
|---------|----------|-----------|
| boot1 structural | 2 → {109, 136} known/active | **2 {109,136}** ✓ |
| boot1 needs_apply / T_backup | true / >0 (una tantum) | true / **99.0s** |
| regime structural (2 piani, writer fermi) | 0 | **0 / 0** ✓ |
| regime needs_apply / T_backup | false / 0 | **false / 0** ✓ |
| assets | 151 | **151** ✓ |
| name_proposals | 409 (no archiviazioni: 109/136 escono dalla quarantena) | **409** ✓ |
| AD | ~68 (109/136 già in finestra) | **68** ✓ |
| breaker | closed | **closed** ✓ |
| unknown_source | 0 | **0** ✓ |
| observations in sqlite_master | assente | **assente** ✓ |
| ip_current | mobile (osservazione) | 100→101 |
| fact_assertions | mobile per cambiamento (osservazione) | 260→261 |
| T_total | osservazione (non gate) | 108.4s |

## W-P.5 — Deploy e gate

Deploy `scripts/deploy.sh api` (snapshot pre-deploy `observatory-20260727-201706-123044.db`,
rsync, rebuild image `observatory-api`, versione **0.10.53**).

**Assert (una riga, boot1 e regime):**
`boot1 0.10.53: structural=2 {109,136}→known/active · needs_apply=true · T_backup=99.0s · confermati=63 noti=48 quarantena=25 proposte_archiviate=0 · T_total=108.4s(obs)`
`regime 0.10.53: DUE piani a writer fermi structural=0/0 · needs_apply=false · T_backup=0 · breaker=closed · assets=151 · ip_current=101(mobile) · NP=409 · FA=261(cur=68) · AD=68 · unknown_source=0 · observations=absent · I6=vuoto · 109=known/active · 136=known/active`

**GATE W-P (tutti verdi):**
1. due piani consecutivi a writer fermi `structural_actions == []` — ✓
2. regime `needs_apply=false · T_backup=0 · structural=0 · breaker=closed` — ✓
3. W-P.3.1–3.5 verdi — ✓
4. nessuna soglia alzata, nessun caso speciale su asset_id, nessuna esclusione dal conteggio —
   ✓ (diff: `classify_asset` derivazione generale su `meta.discovery.fritz`; `_apply_level_meta`
   writer unico; stale_hours=24 invariato)
5. delta W-P.0 enumerati — ✓

Rollback: revert del bump + deploy tag `v0.10.52`.

## Diff
`obs-wp.diff.txt` — file toccati: `api/app/services/trust.py`, `tests/test_wp_presence.py`,
`VERSION`, `web/package.json`, `CHANGELOG.md`, `docs/KNOWN_DEBT.md`, `scripts/wp_diagnose.py`,
`scripts/wp_predict.py`, `scripts/wp_gate.py`. **Esclusi dichiarati:** `docs/obs-wp.md` (questo
report) e `docs/obs-wp.diff.txt` (l'artefatto stesso).
