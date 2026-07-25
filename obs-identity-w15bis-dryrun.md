<!-- BLOCK-ID: OBS-IDENTITY-W15BIS-DRYRUN -->

# OBS-IDENTITY W1.5-bis — dry-run linker (RO)

**Generated:** 2026-07-25T18:39:05Z · **Tool:** `tools/obs_identity_linker_dryrun.py`  
**Readonly proof:** `OK: write rejected (OperationalError: attempt to write a readonly database)`

## Vacuità dichiarata

identity_evidence=0 e proposals=0 in produzione sono la conseguenza dei writer spenti, non una verifica. La verifica del rifiuto è questo dry-run, che ha valutato **11175** coppie.

## PREVISIONE (dichiarata PRIMA dell’esecuzione)

| Metrica | Predetto |
|---------|----------|
| pairs D2 | **0** |
| pairs D3 | **0** |

## OBSERVED

| Metrica | Valore |
|---------|--------|
| Coppie valutate | **11175** (150 asset con MAC → C(150,2)) |
| by max E | `E2-temporal: 11175` |
| by D | `D1: 11149` · `D0: 26` |
| D2 | **0** (scarto 0) |
| D3 | **0** (scarto 0) |
| max E3 | **0** |
| E3 available | **false** |

E3: `access_port_measured` / `mac_count_measured` / `simultaneity_window` non misurabili (SNMP timeout). `mac_count_threshold` non inventato (None → degrada a E2).

## Reference — 147 ↔ 151

| Campo | Valore |
|-------|--------|
| MAC | `D8:EC:5E:CC:1C:05` / `…:08` |
| chassis_id | 23 / 23 |
| max_level | **E2-temporal** |
| decision | **D0** |
| would_propose | false |
| relation | unresolved |

**Motivi di rifiuto (stampati):**
1. K7: evidenza circolare da chassis_id preesistente
2. E3 available=false (access_port/mac_count/simultaneity non misurati)
3. identità non dimostrata — richiede E5 via SNMP/LLDP; ultimo poll fallito in timeout, non ritentato
4. decisione=D0 (nessuna IdentityLinkProposal)

## Reference — LGS328C

Associazione storica chassis 23 (asset 2↔147/151): K7 su chassis_id → **D0**, nessuna promozione a `proven_same`, nessun canonico derivato.

## Reference — LGS310C (asset 3)

- name=`LGS310C`, MAC `D8:EC:5E:C5:7E:C7` (+ `…:CF`)
- `used_as_chassis_identity_evidence=false`
- `meta.manual_overrides` assente in DB (pin dichiarato da Michele; non usato come evidenza identity a nessun livello)

## UI non risolvibile (B.7)

Il modello dry-run emette il testo «identità non dimostrata — richiede E5…». Superficie UI card informativa **non collegata** → rimandata a **W4a**. Nessuna card alta priorità generata da questa ondata.

## Tabella completa

11175 righe nel JSON `/tmp/w15bis-dryrun.json` sul NAS (non pubblicate per dimensione). Estratto: tutte le coppie hanno max_E≤E2 e D∈{D0,D1}; zero D2/D3.
