<!-- BLOCK-ID: OBS-IDENTITY-W15-DIAGNOSI -->

# OBS-IDENTITY-EVIDENCE W1.5 — Fase 2 Diagnosi (RO)

**Data misura:** 2026-07-25 ~20:20 Europe/Rome · **Prod:** 0.10.41 · **Traffico:** minimo (solo SELECT)  
**Precondizione:** W1 chiusa (`obs-currency-w1.md` curl 200).

---

## 2.1 Sorgenti di evidenza di identità disponibili oggi

| Sorgente | Protocollo / campo | Ultima riuscita | Ultimo tentativo | Esito (K3) |
|----------|--------------------|-----------------|------------------|------------|
| FDB managed (328c/310c) | SNMP Bridge / `switch_ports.observed_macs` + `last_fdb_at` | `last_fdb_at` max **2026-07-25 14:52Z** (38/46 porte) | 328c/310c `fdb_poll` **2026-07-25 18:16–18:19Z** | **fallimento misurato** (timeout) — non «assenza» |
| SNMP switch poll | SNMP system/if | fallito (meta `snmp_poll.ok=false`) | stesso timestamp | **fallimento misurato** |
| LLDP | SNMP LLDP | non presente in meta poll ok | non ritentato oltre fdb/snmp falliti | **non misurato / fallito** (nessun neighbor fresco) |
| ENTITY-MIB serial/UUID | SNMP ENTITY | mai in store identity (tabella assente pre-W1.5) | non tentato come identity writer | **non tentato** (writer spento) |
| Bridge base MAC dichiarato | SNMP `dot1dBaseBridgeAddress` | non in identity store | non tentato | **non tentato** |
| ARP/ND Cassiopea | `ip neigh` | mgmt `.1.2`/`.1.7`/`.1.8` REACHABLE | probe RO precedente | **successo** solo su MAC mgmt; `:05`/`:08` **no hit** |
| Fritz hostlist | portal | `:05` last ~2026-07-24 03Z · `:08` ~19Z · `active=false` | continuo | **successo storico**; live **assente misurato** sul Fritz |
| OUI / hostname | lookup / manual | continuo su NP | — | **corroborante** (E1), non identità |
| `chassis_id` grouping R1/R2 | `chassis_grouping.py` RULE_VERSION=2 | last_confirmed ~boot | auto | **NON usabile come evidenza** (D5a / K7) — generato da euristiche |

Tempi query HDD: chassis 0.002 s · U/L 0.003 s · switch meta <1 s. Nessuna query >60 s.

---

## 2.2 Coppia candidata `:05` / `:08` (147 / 151)

| Asset | MAC | chassis_id oggi | Evidenza live | Livello max (scala E) | Provenienza | Età |
|-------|-----|-----------------|---------------|------------------------|-------------|-----|
| 147 | `D8:EC:5E:CC:1C:05` | **23** (LGS328C) | no IP · no ARP · 0 FDB hit | **E0-unmeasured** (SNMP timeout) + storia → **E2** max | Fritz+FDB storici | last ~2026-07-24 03Z |
| 151 | `D8:EC:5E:CC:1C:08` | **23** (LGS328C) | idem | idem | Fritz+FDB storici | last ~2026-07-24 19Z |

Nessuna stima. Relazione dichiarata: **unresolved**. Nessuna proposta consolidabile da misurare in DB (tabelle identity assenti fino a deploy W1.5).

Chassis 23 meta: `origin=auto`, `confirmations=["C4","R2"]`, R2 linka 147/151 a mgmt `CC:1B:FF` via **OUI allowlist** — evidenza di **euristica di grouping**, non E5.

---

## 2.3 Assets con `chassis_id`

- **35 / 151** assets con `chassis_id` valorizzato  
- **15** gruppi chassis (`1,3,6,9,14–24`)  
- Provenienza: `chassis.meta.origin="auto"`, `rule_version="2"`, confirmations C1/C2/C3/C4/R1/R2  
- **Questi `chassis_id` NON sono evidenza di identità** per W1.5 (D5a): riciclo di euristiche (incluso R1 adiacenza MAC / R2 OUI).

---

## 2.4 MAC localmente amministrati (U/L)

- Interfacce totali: **158**  
- Interfacce U/L (bit 0x02): **52**  
- Asset distinti con ≥1 MAC U/L: **~50** (enumerati in misura RO; esclusi da ogni evidenza E5)

---

## 2.5 Copertura SNMP/LLDP (tre numeri)

| Stato | N | Note |
|-------|---|------|
| Disponibile (poll ok recente) | **0** switch | 328c/310c/308ep tutti `fdb_poll.ok=false` / `snmp_poll.ok=false` |
| Poll fallito (misurato) | **3** switch | timeout SNMP |
| Mai tentato come identity ENTITY/LLDP writer | **151** asset | writer identity **non esiste ancora in prod** |

Porte con `last_fdb_at`: **38/46** (cache storica, non poll corrente ok).

---

## 2.6 K1 — campi reconcile trust (bootstrap backup)

`reconcile_trust_history` confronta / può riscrivere:

| Campo | Ruolo |
|-------|--------|
| `Asset.trust_level` | structural se ≠ atteso |
| `Asset.meta.operational_state` | structural se ≠ atteso |
| `Asset.portal_first_seen` / `portal_last_seen` | timestamp refresh (non structural da solo) |
| `Asset.presence_state` | presence refresh |
| `NameProposal.status` (archivio fritz_historical) | proposals_archived |

**NON** confrontati per structural backup: `Asset.name`, `Asset.chassis_id`.

→ Stato di identità W1.5 vive in `identity_evidence` / `identity_link_proposals` (**store separato**). Scrivere lì non innesca da solo `needs_apply` trust. Scrivere `chassis_id`/`name` resta fuori scope W1.5.

---

## 2.7 Costo query

Tutte le SELECT di questa fase < 1 s su HDD. Nessun chunk necessario.
