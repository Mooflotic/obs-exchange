<!-- BLOCK-ID: OBS-UX-IP-308-VERIFICA -->

# OBS-UX — Verifica IP GS308EP `.1.8` / `.3.20` (sola lettura)

**Data:** 2026-07-25 · **Live:** 0.10.37 · **Scope:** RO, nessuna modifica a dati autorevoli

Correzione utente: non assumere che `192.168.3.20` sia IP secondario/inventariale del GS308EP; potrebbe essere legato a SPAN/Cassiopea.

---

## Fatti (DB + config + codice)

| Voce | Evidenza |
|------|----------|
| `.1.8` | `ip_addresses` id=7 → interface 4 → **asset 4 GS308EP**; `is_current=1`; `source=mgmt`; `role=mgmt`; MAC `54:07:7D:1E:4F:B9`; `last_seen` 2026-07-25 15:47Z |
| Switch 308ep | `switches.ip = 192.168.1.8` (codice `308ep`) |
| `.3.20` in DB | `ip_addresses` id=133 → **stessa** interface 4 / stesso MAC asset 4; `is_current=0`; `source=fritz`; `role=secondario`; first 2026-07-17 · last **2026-07-23** 01:18Z |
| Fritz su asset 4 | `meta.discovery.fritz.hostname = PC-54-07-7D-1E-4F-B9` (synthetic) |
| Cassiopea NIC 1 | asset **5**, MAC `24:4B:FE:84:6A:01`, IP corrente **`.1.3`** |
| Cassiopea NIC 2 | asset **6**, MAC `24:4B:FE:84:6A:02`, IP corrente **`.3.24`** (non `.3.20`); legacy `.1.3` non corrente |
| SPAN topologia | `KNOWN_SPAN_PORTS` = LGS328C **p22**; `switches.meta.port_role_overrides['22'].role=span` (manual); `switch_ports` 328c:22 notes «Seconda scheda dello stesso NAS», `asset_id=6` |
| SPAN L3 | `KNOWN_DEBT` / topologia post-bond: eth1 sink **`10.255.255.2/30`** (non `192.168.3.x`) |

Unici owner di `.3.20` in `ip_addresses`: **solo asset 4** (binding non corrente). Nessuna riga `.3.20` su asset 5/6.

---

## Ipotesi

| Ipotesi | Stato |
|---------|--------|
| `.3.20` = IP inventariale/secondario “vero” del GS308EP | **Respinta come fatto di prodotto** — era un’etichetta UI/doc sopra un binding Fritz storico; non c’è conferma operativa (non current, non `switches.ip`) |
| `.3.20` = porta/interfaccia SPAN di Cassiopea | **Non supportata dai dati attuali** — SPAN = p22 → asset 6; LAN NIC2 = `.3.24`; sink = `10.255.255.2/30`. `.3.20` ≠ nessuna di queste |
| `.3.20` = errore/ghost Fritz sullo stesso MAC del 308 | **Plausibile, da confermare** da Michele (ARP/DHCP reale, UI switch Netgear, storico router) |

---

## Conflitto / da confermare

- Il DB **associa** `.3.20` al MAC del GS308EP via Fritz, ma l’associazione è **stale** e non allineata a `switches.ip`.
- L’intuizione SPAN↔Cassiopea è **corretta per p22/NIC2**, ma l’IP LAN di quella NIC è **`.3.24`**, non `.3.20`.
- **Ownership reale di `.3.20`:** da confermare. Vietato presentarlo come indirizzo del 308 finché non c’è adozione manuale.

---

## Correzione prodotto (UI/copy, no write DB)

- `GS308EP_IP_DIVERGENCE_NOTE`: rimossa la formulazione «inventariale .3.20»; dichiara fatto `.1.8`, binding storico `.3.20` **da confermare**, SPAN ≠ `.3.20`.
- Report ondata B / debiti: aggiornati di conseguenza.
- Nessuna modifica a `ip_addresses` / trust / nomi senza adozione umana.
