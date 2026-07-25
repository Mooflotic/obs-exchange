<!-- BLOCK-ID: OBS-CURRENCY-W0-REGISTRY -->

# OBS-CURRENCY — W0 Registro dei fatti (proposta)

Ogni riga cita misure W0. Nessuna riga senza numero.

Legenda soggetto: `chassis` | `asset` (NIC) | `port` | `relation`  
Cardinality: `single` | `multi` | `scoped`  
TTL: basato su p99 misurato in finestra 7gg **oppure** `None` / available=false.

---

## Registro

| fact_key | subject_scope | cardinality | excl_key proposta | autorità (I5) | ttl_window | giustificazione misura | consumers (oggi) |
|----------|---------------|-------------|-------------------|---------------|------------|------------------------|------------------|
| `asset.name` | **chassis** | single | `name` | manual>ai>dhcp>fritz>oui | **None** (non misurata su raw; nomi non in observations_raw) | 29 manual; 15 chassis ≥2; 0 chassis con >1 manuale distinto | Oggi, Dossier, Inventario, adopt-name |
| `iface.alias` | **asset** | single | `alias` | manual only | None | **Assente oggi** (Interface.label tecnico only) — da introdurre in W1 come store, non su Asset | futuro Dossier/Plant |
| `asset.iface_ip` | **asset** (MAC/iface) | single per excl | `ip` **per MAC** (non per subnet) | mgmt/dhcp/fritz/nmap… (riusa rank elezione) | p99 fritz≈180s; nmap≈940s → proposta partenza **1h fritz / 2h nmap** entro 7gg; oltre available=false | 6 MAC sequenziali; 0 multi-current stesso MAC; 9 istanze storia non-current | elect_interface_primary, topology, scans, monitoring |
| `asset.mgmt_ip` | **asset** (switch infra) | single | `mgmt_ip` | mgmt > altri | come iface_ip | switches.ip + role=mgmt (asset 2/3/4) | monitoring pin, plant |
| `presence.portal` | asset | single | `presence` | portal evidence | 24h già hardcoded trust | trust.py 24h | trust, inventory buckets |
| `port.fdb_mac` | port | multi/scoped | `(switch,port,mac)` | fdb | stale_after_hours topology | FDB last_fdb_at | topology, presence |
| `rel.physical_link` | relation | single scoped | link id | manual/auto_links | None | PhysicalSwitchLink state=current | plant/topology |
| `os.guess` | asset | single | `os` | manual > nmap | None finché non misurato | fingerprint non auto-write | Dossier |
| `name_proposal` | **chassis** (per rename apparato) | multi pending ma 1 azione | `(chassis,value_norm)` | non è fatto autoritativo; coda | n/a | 3 dup ch23 Switch Linksys; 18 pending su asset già named | Oggi triage |

---

## Ambiguïtà (non decidere — STOP-5 limitato)

| Riga | Perché |
|------|--------|
| Fusione LGS310C ↔ MAC `…:1C:05`/`…:1C:08` | UI/caso utente = un apparato; DB = chassis **24** vs **23** (con LGS328C). Misura contraddice l’assunzione. |
| Autorità nome `LGS310C` (asset 3) | Nome presente ma `manual_overrides` **non** contiene `name` → non conteggiato nei 29 manual. Serve conferma se trattarlo come manual pinned. |
| `scans=68` | Non ricostruito come conteggio live; non usato come assert finché Michele non definisce la metrica. |

---

## Implicazioni W1 (senza implementare)

1. `subject_of(asset.name)` → chassis_id se presente, altrimenti asset.  
2. `excl_key` IP = MAC (o interface_id), **mai** «un solo IP per asset» cieco.  
3. Cassiopea `.1.3`/`.3.24` restano entrambi current su subject asset distinti.  
4. K1: `asset.name` **non** è nei campi reconcile → canonical name può vivere in `fact_assertion` **senza** scrivere colonne Asset (W1–W2).
