# F2 — Revisione strutturale UI/UX (0.10.51)

**Data:** 2026-07-27 · **Ramo:** `feature/obs-currency` · **Base:** W4c **0.10.50** (gate verde)  
**Rinumerazione:** W5 → dopo F2 · W6 · W7 · W8 a seguire.

---

## F2.0 — Identificazione «Mappa»

| Etichetta Michele | Route | Componente |
|---|---|---|
| Gruppo nav **MAPPA** | `/inventory` · `/plant` · `/topology` · `/monitoring` · (+ Timeline/Findings/Azioni) | `App.vue` nav-group |
| Mappa **porte fisiche** («varie parti rotte») | **`/plant`** | `Plant.vue` + `Branch308Card.vue` |
| Collocazione device | `/topology` | `Topology.vue` |

Dichiarato **prima** delle modifiche: la superficie «Mappa» operativa porte = **Impianto `/plant`**; il gruppo laterale MAPPA è composito.

---

## Assert di produzione (UNA RIGA)

`boot1 0.10.51: needs_apply=false T_backup=0 structural=0 · NP_total=409 (Δ0; pending=78) · assets=151 ip_cur=100 AD=62 · fact_assertions=253 (Δ0) · breaker=closed · unknown_source=0 · observations=absent · asset3=manual LGS310C · VERSION=0.10.51`

### Previsioni (dichiarate pre-deploy) → osservati

| Metrica | Previsto | Osservato | Scarto |
|---|---|---|---|
| name_proposals **total** | 409 Δ0 | **409** | 0 |
| fact_assertions | 253 Δ0 | **253** | 0 |
| assets / ip_current | 151 / 100 | 151 / 100 | 0 |
| needs_apply / T_backup / structural | false / 0 / 0 | false / 0 / 0 | 0 |
| breaker / unknown_source | closed / 0 | closed / 0 | 0 |
| AD (finestra 24h) | rimisurare | **62** | — (finestra mobile) |
| nomi valore modificati | 0 | 0 (asset 3 = LGS310C) | 0 |
| provenance_unreliable rimossi | 0 | 0 | 0 |

Nota: il conteggio «NP» di gate è il **totale** righe `name_proposals` (=409), non solo `pending`.

---

## F2.1 — Difetti Mappa (`/plant`) enumerati

| # | Componente | Riproduzione | Causa | Gravità | Origine | Esito |
|---|---|---|---|---|---|---|
| M1 | `Plant.vue` | Apri `/plant?asset=N` | query ignorata | rotto | FE | **fix**: deep-link `?asset=` / `?asset_id=` → pick porta + scroll |
| M2 | griglia porte GS308 | pallini grigi mute | SNMP assente ma UI mostra `oper_status` vuoto come «sconosciuto» | degradato | FE | **fix**: `snmpLiveSupported` → «—» + titolo «non misurabile» |
| M3 | `Branch308Card` | vista 308 | limiti I2/I7 non espliciti (`.3.20`, PoE, flapping) | degradato | FE | **fix**: blocco «Non misurabile» |
| M4 | Topology deep-link | `?highlight=` | solo `asset_id` | degradato | FE | **fix**: accetta `highlight`/`asset` |
| M5 | Topology tooltip | inglese «stale» | copy EN | cosmetico | FE | **fix**: «non recente» |
| M6 | Presence invent./Oggi | `stale` / `stale_unlocated` | letto come «assente» | rotto (I2) | FE (+ debito trust a monte) | **fix presentazione**; trust **non** toccato (W4c.5.2) |
| M7 | Fritz muto | nessuna schermata lo dice | credenziali assenti (F-4) | rotto (visibilità) | FE | **fix**: `FritzOutageBanner` su Oggi/Dashboard/Inventario |
| M8 | Chassis N nomi | inventory/dossier | post W4c.1 i membri non hanno tutti il nome; compose usava solo primary.name | degradato | FE | **fix**: `chassis_canonical_name` in `composeDevices` + dossier |
| M9 | Favicon | cache / palette legacy verde neon | fuori token | cosmetico | FE | **fix**: token matrix + versioned links |

Cause a monte **non mascherate**: declassamento trust `stale_unlocated` (DEBT-PRESENCE-SOURCE-OUTAGE) — UI dichiara «copertura sorgente non disponibile».

---

## F2.2 — Oggi

- Banner Fritz; `stale_unlocated` → «copertura sorgente non disponibile».
- Conflitti R-H nel flusso (sezione problematica con Impatto / Se ignori / Se agisci).
- Chassis / rename / move restano **nella** coda Oggi (nessun hub parallelo).
- Soppressione sibling: dipende da `chassis_role === "interface"` (W4c.1) — invariata.

Verifica LGS (logica già in triage + presentation API): chassis 24 manual LGS310C; chassis 23 LGS328C resta `unknown_nonempty` (F-2); nessuna marcatura aggiuntiva in F2.

---

## F2.3 — Matrice vista × breakpoint

**Correzione W4d.3.1:** la matrice F2 con celle «OK» era un’autocertificazione da lettura codice, non un esercizio runtime. Celle **non verificate a runtime**.

| Vista | Mobile | Tablet | Desktop |
|---|---|---|---|
| `/oggi` | non verificato a runtime | non verificato a runtime | non verificato a runtime |
| `/dossier/:id` | non verificato a runtime | non verificato a runtime | non verificato a runtime |
| `/inventory` | non verificato a runtime | non verificato a runtime | non verificato a runtime |
| `/plant` | non verificato a runtime | non verificato a runtime | non verificato a runtime |
| `/topology` | non verificato a runtime | non verificato a runtime | non verificato a runtime |
| `/monitoring` | non verificato a runtime | non verificato a runtime | non verificato a runtime |
| `/suggestions` | non verificato a runtime | non verificato a runtime | non verificato a runtime |

### Checklist operativa (max 10) — W4d.3.2

1. Apri `/plant?asset=4` → la porta del GS308EP associata è selezionata e in vista.
2. Su Impianto, card GS308EP: nessun pallino SNMP grigio mute; compare «non misurabile» / «—».
3. Apri `/oggi` → se Fritz è muto o degradato, compare il banner «Presenza Fritz non misurabile».
4. In Inventario, un device `stale_unlocated` non dice «assente» / «non presente» senza qualifica.
5. Dossier di un membro chassis 23 → titolo = nome apparato (canon) e «interfaccia di …».
6. `/topology?highlight=4` (o `asset_id=4`) → il nodo GS308EP è messo a fuoco.
7. Conflitto R-H in Oggi (se presente) → card con Impatto / Se ignori / Se agisci.
8. Favicon in scheda nuova (finestra pulita) → marchio scuro con accent/ok, non verde neon legacy.
9. Branch308 in Impianto → elenco «Non misurabile» include PoE/NSDP/`.3.20` storico.
10. `/monitoring` → Salute sensori elenca eventuali fallimenti Fritz senza richiedere azioni impossibili.

**F2.3.4 Fritz:** banner + copy; stato Fritz muto dichiarato. Trust layer **non** corretto.

---

## F2.4 — Vista 308 (GS308EP)

Dichiarato in `Branch308Card`: fatto (ping `.1.8`, mappa manuale, FDB upstream conf. 0.65); **non misurabile** (porta interna, PoE, NSDP, rx/tx locale, flapping); `.3.20` storico; SPAN = inferenza.

---

## F2.5 — Favicon

### Token misurati (`matrix.css` `:root`)

| Nome | Valore | Uso favicon |
|---|---|---|
| `--bg-0` | `#0f1319` | fondo (tema scuro) |
| `--accent` | `#6bc5db` | forma L |
| `--ok` | `#4fb477` | forma O |
| `--text-1` | `#e8ebf0` | (tema chiaro SVG: L su `--bg-0`, fondo `#e8ebf0`) |

Nessun colore nuovo. Forma: **due** primarie (L + O a foratura), nessuno schema topologia. Strategia: `prefers-color-scheme` nell’SVG + marchio scuro leggibile su tab chiare via ICO/PNG opachi.

Asset: `favicon.svg` · `favicon.ico` (16/32/48) · `apple-touch-icon.png` 180 · PNG 16/32/48. Link versionati `?v=0.10.51` in `index.html`.

**Cache Caddy `:8080`:** `200` SVG/ICO; `Server: Caddy` + nginx; `Etag`/`Last-Modified` presenti; bust query.

### Render obbligatori (allegati)

![favicon 16px](https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-ux2-favicon-16.png)

![favicon 32px](https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-ux2-favicon-32.png)

Leggibilità a 16px: L ciano + O verde distinti su fondo `--bg-0` (una iterazione).

---

## F2.6 — Dipendenze dichiarate → W5 / W7

| Caso | Perché FE non risolve | Ondata |
|---|---|---|
| Consumatori correntezza / identity | logica identità non in FE | **W5** |
| Wire `mac_ip_policy` | classifier puro non wired | **W7** |
| Trust `stale_unlocated` vs source outage | classificazione presenza | ondata dedicata (non F2) |
| `excl_key` IP ruolo | pre-condizione W3 | W3 |

Gate I6 post-F2: `rg 'scoreSpecificity|specificity' api/` → **VUOTO**.

---

## Debiti aperti (aggiornati, nessuna riga estranea rimossa)

- **DEBT-FRITZ-TR064-CREDENTIALS** — **CHIUSO** F0 (vedi obs-fritz-restore.md)
- **DEBT-PRESENCE-SOURCE-OUTAGE** — APERTO; UI F2 dichiara; trust non corretto

---

## Test eseguiti (nodi nominati F2 / regressione UI)

- `oggiTriage` · `oggiProblems` · `observatoryUx` · `portPresentation` · `topologyLayout` → pass
- I6 → vuoto
- **Non** rieseguita suite completa. **Non** dichiarato «suite verde».

---

## Esclusioni dal diff

- `data/`, `.env`, `.venv`, `node_modules`, `web/dist`, DB/backups
- Report/diff di ondate precedenti già pubblicati (w4c, w4b, …) non re-inclusi come contenuto nuovo salvo riferimenti
- `prepara-cursor.sh` fuori scope

---

## Publish

- https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-ux2.md (200)
- https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-ux2.diff.txt (200)
- https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-ux2-favicon-16.png (200)
- https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-ux2-favicon-32.png (200)
