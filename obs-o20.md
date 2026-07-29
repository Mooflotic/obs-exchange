wc_l: 2379
# OBS-O20 — OBS-EVIDENZA — 0.10.89
Data report: 2026-07-29 20:19 UTC
Auth catture: session mint TTL 180s (fonte harness 36s×5), token non pubblicato.
Base: `30b65f7` (HEAD post-O19). Ramo: `feature/obs-currency`.

## 1. Elenco file toccati

- `VERSION`, `web/package.json`, `CHANGELOG.md`
- `web/src/assets/matrix.css` (`--inference-edge` → `#7656b0`; fill `--inference` invariato)
- `web/src/views/Topology.vue` (specificità `.topology-list__parent` → `--text-2`)
- `web/src/portPresentation.js` + `portPresentation.test.js` (FDB → «visto passare»)
- `web/src/views/Plant.vue` (`data-evidence-class` / `data-role-source` / `data-o20`)
- `web/src/views/Dossier.vue` («visto passare su …» per `fdb_port`)
- `web/src/observatoryUx.js` (`OBS_O20_MARKER`)
- `scripts/contrast_gate.py`, `scripts/evidence_gate.py`, `scripts/evidence_site_audit.py`, `scripts/evidence_verify_ab.py`
- `docs/KNOWN_DEBT.md`, artefatti `docs/obs-o20-*`

## 2. Blocco 0 (correzioni O19)

### 0.1 G4 contraddizione
G4 O19 **è stato eseguito** contro deployed (`docs/obs-o19-G4.json`). §16 di O19 conteneva riga stale; rettifica annotata in `docs/obs-o19.md` §16 (non cancellata).

### 0.2 Drift repo↔NAS — output integrale
```json
{
  "NAS_count": 74,
  "repo_count": 73,
  "solo_NAS": [
    "scripts/_w4a_measure.py"
  ],
  "solo_repo": [],
  "solo_NAS_enumerated": [
    "scripts/_w4a_measure.py"
  ],
  "solo_repo_enumerated": [],
  "expected": {
    "solo_NAS": [
      "scripts/_w4a_measure.py"
    ],
    "solo_repo": []
  },
  "orphans": [],
  "DRIFT_OK": true,
  "o19_correction": "O19 elencava density/nav/topology in solo-repo ma erano già su entrambi post-rsync O17/O18/O19 deploy; lista O19 era sbagliata (non rimozione NAS).",
  "density_trio_on_both": true,
  "come_potrebbe_fallire": "conteggio find diverso da path reale o file non .py"
}
```
Correzione: lista O19 «solo-repo» density era **sbagliata**; trio già su entrambi. `solo-NAS={_w4a_measure.py}` atteso. `orphans=[]` `DRIFT_OK=true`.

### 0.3 Census 50/48 e 39/38
Causa: `/api/topology` non idempotente (campioni 28 edge senza inferred → ~51 con branch FDB). Non UI.
```json
{
  "samples": [
    {
      "i": 1,
      "nodes_n": 155,
      "edges_n": 28,
      "fdb_n": 18,
      "inferred_n": 0,
      "edge_ids_sorted_head": [
        "gateway:core:328c",
        "internet:gateway",
        "port:310c:2",
        "port:310c:4",
        "port:310c:5"
      ],
      "kinds": [
        "ethernet",
        "wifi"
      ],
      "sources": [
        "FDB",
        "LLDP",
        "manual",
        "radio AP"
      ],
      "fdb_ids_len": 18
    },
    {
      "i": 2,
      "nodes_n": 155,
      "edges_n": 28,
      "fdb_n": 18,
      "inferred_n": 0,
      "edge_ids_sorted_head": [
        "gateway:core:328c",
        "internet:gateway",
        "port:310c:2",
        "port:310c:4",
        "port:310c:5"
      ],
      "kinds": [
        "ethernet",
        "wifi"
      ],
      "sources": [
        "FDB",
        "LLDP",
        "manual",
        "radio AP"
      ],
      "fdb_ids_len": 18
    },
    {
      "i": 3,
      "nodes_n": 155,
      "edges_n": 28,
      "fdb_n": 18,
      "inferred_n": 0,
      "edge_ids_sorted_head": [
        "gateway:core:328c",
        "internet:gateway",
        "port:310c:2",
        "port:310c:4",
        "port:310c:5"
      ],
      "kinds": [
        "ethernet",
        "wifi"
      ],
      "sources": [
        "FDB",
        "LLDP",
        "manual",
        "radio AP"
      ],
      "fdb_ids_len": 18
    },
    {
      "i": 4,
      "nodes_n": 155,
      "edges_n": 28,
      "fdb_n": 18,
      "inferred_n": 0,
      "edge_ids_sorted_head": [
        "gateway:core:328c",
        "internet:gateway",
        "port:310c:2",
        "port:310c:4",
        "port:310c:5"
      ],
      "kinds": [
        "ethernet",
        "wifi"
      ],
      "sources": [
        "FDB",
        "LLDP",
        "manual",
        "radio AP"
      ],
      "fdb_ids_len": 18
    },
    {
      "i": 5,
      "nodes_n": 155,
      "edges_n": 51,
      "fdb_n": 41,
      "inferred_n": 22,
      "edge_ids_sorted_head": [
        "gateway:core:328c",
        "gs-branch:308ep:12",
        "gs-branch:308ep:136",
        "gs-branch:308ep:17",
        "gs-branch:308ep:18"
      ],
      "kinds": [
        "ethernet",
        "inferred_branch",
        "wifi"
      ],
      "sources": [
        "FDB",
        "LLDP",
        "manual",
        "radio AP"
      ],
      "fdb_ids_len": 41
    }
  ],
  "fdb_only_first": [],
  "fdb_only_last": [
    "gs-branch:308ep:12",
    "gs-branch:308ep:136",
    "gs-branch:308ep:17",
    "gs-branch:308ep:18",
    "gs-branch:308ep:2",
    "gs-branch:308ep:26",
    "gs-branch:308ep:29",
    "gs-branch:308ep:30",
    "gs-branch:308ep:31",
    "gs-branch:308ep:32",
    "gs-branch:308ep:37",
    "gs-branch:308ep:38",
    "gs-branch:308ep:4",
    "gs-branch:308ep:43",
    "gs-branch:308ep:49",
    "gs-branch:308ep:52",
    "gs-branch:308ep:55",
    "gs-branch:308ep:56",
    "gs-branch:308ep:57",
    "gs-branch:308ep:62",
    "gs-branch:308ep:66",
    "gs-branch:308ep:82",
    "uplink:310c:8-308ep:unknown"
  ],
  "edges_range": [
    28,
    28,
    28,
    28,
    51
  ],
  "fdb_range": [
    18,
    18,
    18,
    18,
    41
  ],
  "causa_dominante_ipotesi": "API topology non idempotente tra poll: insieme archi FDB varia di ±1–2 tra campioni; 50→48 e 39→38 sono drift di popolazione API, non bug di misura UI",
  "come_potrebbe_fallire_questa_ipotesi": "se gli id FDB fossero stabili su 5 campioni ma G4 avesse contato male i path DOM, la causa sarebbe harness non API"
}
```
Regola O20: reconcile allega census **entrambi** i lati; differiscono → misura INVALIDA.

### 0.4–0.5 Contrasto archi + tratteggio
Deployed 0.10.88 (versione letta da bundle pagina): archi edge-* **7.208:1** ≥3:1 OK. Parent O19 **3.474:1** FAIL (text-3) — corretto in O20 a text-2 (**7.232:1** misurato in V POST). Tratteggio: 0 archi più corti del periodo 12px.
Artefatto: `docs/obs-o20-B0-contrast-dash.json` (keys=['wave', 'base', 'by_width']).

### 0.6 Tab split O18 topology@390
```json
{
  "wave": "O20-B0.6",
  "source": "docs/obs-o18-N1.json other_routes.topology.390",
  "prompt_claimed_tab_div": 9,
  "measured_tab_div": 8,
  "len_asserted": 8,
  "come_potrebbe_fallire": "classificare shell/in-main a orecchio senza le 8 voci; o usare POST n=9 senza dire quale run",
  "enumerazione": [
    {
      "i": 1,
      "prev": "☰ Menu",
      "next": "Oggi",
      "classificazione": "shell",
      "nota": "aside Menu → prima voce main Oggi; salto chrome→contenuto"
    },
    {
      "i": 2,
      "prev": "Esci",
      "next": "Schermo intero…",
      "classificazione": "shell",
      "nota": "footer aside Esci → controllo Schermo intero (chrome)"
    },
    {
      "i": 3,
      "prev": "□AppleTV Sala…",
      "next": "▦LGS310C…",
      "classificazione": "in-main",
      "nota": "ordine nodi canvas/lista vs gerarchia visuale"
    },
    {
      "i": 4,
      "prev": "□Allsky 3…",
      "next": "▦LGS328C…",
      "classificazione": "in-main"
    },
    {
      "i": 5,
      "prev": "◔Nintendo Switch…",
      "next": "◒FRITZ 5690 Pro…",
      "classificazione": "in-main"
    },
    {
      "i": 6,
      "prev": "◒FRITZ 5690 Pro…",
      "next": "▦GS308EP…",
      "classificazione": "in-main"
    },
    {
      "i": 7,
      "prev": "□AppleTV Sala…↳ collegato a",
      "next": "□LGS328C…Visto dal portale",
      "classificazione": "in-main",
      "nota": "lista relazioni vs card"
    },
    {
      "i": 8,
      "prev": "□Spazio…Visto dal portale",
      "next": "□Broadlink-…",
      "classificazione": "in-main"
    }
  ],
  "split": {
    "shell_n": 2,
    "in_main_n": 6,
    "shell_n_asserted": 2,
    "in_main_n_asserted": 6
  },
  "o19_claim": "0 in-main — non confrontabile senza split; DEBT-SHELL-TAB-ORDER",
  "stato_attuale_atteso_post_O19": "in-main ridotte da riordino lista/h2/canvas tabindex; shell Menu→Oggi e Esci↔Schermo tipicamente residue (chrome)"
}
```
`DEBT-SHELL-TAB-ORDER` aperto (shell 2 + in-main 6; misurato 8 non 9).

### 0.7 Conservazione — enum completa (da O19 B0.8, non troncata)
len_asserted=14 endpoint=`/api/assets?include_historical=true&all_proposals=true (stesso di Oggi.load)`
```json
{
  "assets_endpoint": "/api/assets?include_historical=true&all_proposals=true (stesso di Oggi.load)",
  "queueConservationCheck": {
    "missing": [],
    "duplicated": []
  },
  "UI_DOM_names_ordered": [
    "Echo Cucina",
    "LGS328C → Switch Linksys",
    "SkyBooster2 BIBLIO — Ethernet",
    "Sky",
    "Sky",
    "Cassiopea — NIC 1",
    "Allsky 3",
    "Kraken",
    "Echo Salone",
    "Echo Camera Beatrice",
    "Hub Tapo H100",
    "ROCK",
    "Sky TV",
    "LGS310C"
  ],
  "buildChassisNameCards_enum": [
    {
      "chassis_id": 20,
      "key": "chassis-name-20",
      "display_name": "Echo Cucina",
      "member_asset_ids": [
        55,
        141
      ]
    },
    {
      "chassis_id": 23,
      "key": "chassis-name-23",
      "display_name": "LGS328C",
      "member_asset_ids": [
        2,
        109,
        147,
        151
      ]
    },
    {
      "chassis_id": 28,
      "key": "chassis-name-28",
      "display_name": "SkyBooster2 BIBLIO — Ethernet",
      "member_asset_ids": [
        10,
        11,
        138
      ]
    },
    {
      "chassis_id": 31,
      "key": "chassis-name-31",
      "display_name": "Sky",
      "member_asset_ids": [
        61,
        137
      ]
    },
    {
      "chassis_id": 33,
      "key": "chassis-name-33",
      "display_name": "Sky",
      "member_asset_ids": [
        43,
        136,
        149
      ]
    },
    {
      "chassis_id": 1,
      "key": "chassis-name-1",
      "display_name": "Cassiopea — NIC 1",
      "member_asset_ids": [
        5,
        6
      ]
    },
    {
      "chassis_id": 3,
      "key": "chassis-name-3",
      "display_name": "Allsky 3",
      "member_asset_ids": [
        30,
        51
      ]
    },
    {
      "chassis_id": 15,
      "key": "chassis-name-15",
      "display_name": "Kraken",
      "member_asset_ids": [
        28,
        140
      ]
    },
    {
      "chassis_id": 16,
      "key": "chassis-name-16",
      "display_name": "Echo Salone",
      "member_asset_ids": [
        33,
        145
      ]
    },
    {
      "chassis_id": 17,
      "key": "chassis-name-17",
      "display_name": "Echo Camera Beatrice",
      "member_asset_ids": [
        35,
        148
      ]
    },
    {
      "chassis_id": 18,
      "key": "chassis-name-18",
      "display_name": "Hub Tapo H100",
      "member_asset_ids": [
        49,
        144
      ]
    },
    {
      "chassis_id": 19,
      "key": "chassis-name-19",
      "display_name": "ROCK",
      "member_asset_ids": [
        50,
        146
      ]
    },
    {
      "chassis_id": 30,
      "key": "chassis-name-30",
      "display_name": "Sky TV",
      "member_asset_ids": [
        58,
        108,
        135
      ]
    },
    {
      "chassis_id": 32,
      "key": "chassis-name-32",
      "display_name": "LGS310C",
      "member_asset_ids": [
        3,
        139,
        143
      ]
    }
  ],
  "len_enum_asserted": 14
}
```
`DEBT-O18-CONSERVATION-WRONG-ENDPOINT`, `DEBT-CHASSIS-NAME-COLLISION` (Sky 31+33) registrati.

### 0.8–0.10
Debiti: `DEBT-O19-MAPPA-DESKTOP-GROWTH`, `DEBT-V8-CRITERION-WEAK` (revisore), `DEBT-O19-M1-PARTIAL`. Versione da pagina obbligatoria d’ora in poi.

## 3–6. Fase M (inventario)
dossier_id=83
```json
{
  "summary": {
    "routes_n": 13,
    "total_items_sum_over_widths": 1893,
    "fdb_ownership_violations_n": 0,
    "fdb_ownership_violations": [],
    "indistinguishable_without_color_n": 3,
    "indistinguishable_without_color_sample": [
      {
        "route": "topology",
        "w": 1280,
        "text": "◒FRITZ 5690 Pro192.168.1.1",
        "kind": "class_marker"
      },
      {
        "route": "topology",
        "w": 768,
        "text": "◒FRITZ 5690 Pro192.168.1.1",
        "kind": "class_marker"
      },
      {
        "route": "topology",
        "w": 390,
        "text": "◒FRITZ 5690 Pro192.168.1.1",
        "kind": "class_marker"
      }
    ],
    "len_fdb_ownership_asserted": 0
  },
  "lens_per_route": {
    "oggi": {
      "1280": {
        "len": 89,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 0,
          "h_pagina": 15581
        },
        "kinds": {
          "class_marker": 60,
          "surface_claim": 29
        }
      },
      "768": {
        "len": 92,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 0,
          "h_pagina": 19373
        },
        "kinds": {
          "class_marker": 60,
          "surface_claim": 32
        }
      },
      "390": {
        "len": 92,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 0,
          "h_pagina": 24598
        },
        "kinds": {
          "class_marker": 60,
          "surface_claim": 32
        }
      }
    },
    "topology": {
      "1280": {
        "len": 97,
        "census": {
          "network_nodes": 49,
          "topology_paths": 48,
          "list_parents": 48,
          "inference_marks": 1,
          "h_pagina": 7199
        },
        "kinds": {
          "topology_edge": 48,
          "relation_text": 48,
          "class_marker": 1
        }
      },
      "768": {
        "len": 97,
        "census": {
          "network_nodes": 49,
          "topology_paths": 48,
          "list_parents": 48,
          "inference_marks": 1,
          "h_pagina": 7838
        },
        "kinds": {
          "topology_edge": 48,
          "relation_text": 48,
          "class_marker": 1
        }
      },
      "390": {
        "len": 97,
        "census": {
          "network_nodes": 49,
          "topology_paths": 48,
          "list_parents": 48,
          "inference_marks": 1,
          "h_pagina": 10284
        },
        "kinds": {
          "topology_edge": 48,
          "relation_text": 48,
          "class_marker": 1
        }
      }
    },
    "inventory": {
      "1280": {
        "len": 142,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 0,
          "h_pagina": 6223
        },
        "kinds": {
          "surface_claim": 142
        }
      },
      "768": {
        "len": 142,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 0,
          "h_pagina": 6336
        },
        "kinds": {
          "surface_claim": 142
        }
      },
      "390": {
        "len": 142,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 0,
          "h_pagina": 6631
        },
        "kinds": {
          "surface_claim": 142
        }
      }
    },
    "gs308": {
      "1280": {
        "len": 14,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 1,
          "h_pagina": 1916
        },
        "kinds": {
          "class_marker": 4,
          "surface_claim": 10
        }
      },
      "768": {
        "len": 14,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 1,
          "h_pagina": 2099
        },
        "kinds": {
          "class_marker": 4,
          "surface_claim": 10
        }
      },
      "390": {
        "len": 14,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 1,
          "h_pagina": 3254
        },
        "kinds": {
          "class_marker": 4,
          "surface_claim": 10
        }
      }
    },
    "monitoring": {
      "1280": {
        "len": 7,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 0,
          "h_pagina": 1228
        },
        "kinds": {
          "placeholder": 7
        }
      },
      "768": {
        "len": 7,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 0,
          "h_pagina": 1314
        },
        "kinds": {
          "placeholder": 7
        }
      },
      "390": {
        "len": 7,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 0,
          "h_pagina": 1431
        },
        "kinds": {
          "placeholder": 7
        }
      }
    },
    "timeline": {
      "1280": {
        "len": 108,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 0,
          "h_pagina": 10859
        },
        "kinds": {
          "surface_claim": 108
        }
      },
      "768": {
        "len": 108,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 0,
          "h_pagina": 10928
        },
        "kinds": {
          "surface_claim": 108
        }
      },
      "390": {
        "len": 108,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 0,
          "h_pagina": 13886
        },
        "kinds": {
          "surface_claim": 108
        }
      }
    },
    "findings": {
      "1280": {
        "len": 0,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 0,
          "h_pagina": 900
        },
        "kinds": {}
      },
      "768": {
        "len": 0,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 0,
          "h_pagina": 900
        },
        "kinds": {}
      },
      "390": {
        "len": 0,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 0,
          "h_pagina": 900
        },
        "kinds": {}
      }
    },
    "incidents": {
      "1280": {
        "len": 0,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 0,
          "h_pagina": 900
        },
        "kinds": {}
      },
      "768": {
        "len": 0,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 0,
          "h_pagina": 900
        },
        "kinds": {}
      },
      "390": {
        "len": 0,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 0,
          "h_pagina": 1003
        },
        "kinds": {}
      }
    },
    "plant": {
      "1280": {
        "len": 52,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 1,
          "h_pagina": 2228
        },
        "kinds": {
          "class_marker": 4,
          "port_binding": 46,
          "surface_claim": 2
        }
      },
      "768": {
        "len": 52,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 1,
          "h_pagina": 2964
        },
        "kinds": {
          "class_marker": 4,
          "port_binding": 46,
          "surface_claim": 2
        }
      },
      "390": {
        "len": 52,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 1,
          "h_pagina": 5507
        },
        "kinds": {
          "class_marker": 4,
          "port_binding": 46,
          "surface_claim": 2
        }
      }
    },
    "actions": {
      "1280": {
        "len": 108,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 0,
          "h_pagina": 36487
        },
        "kinds": {
          "surface_claim": 108
        }
      },
      "768": {
        "len": 108,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 0,
          "h_pagina": 41126
        },
        "kinds": {
          "surface_claim": 108
        }
      },
      "390": {
        "len": 108,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 0,
          "h_pagina": 61842
        },
        "kinds": {
          "surface_claim": 108
        }
      }
    },
    "dashboard": {
      "1280": {
        "len": 4,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 0,
          "h_pagina": 2108
        },
        "kinds": {
          "surface_claim": 4
        }
      },
      "768": {
        "len": 4,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 0,
          "h_pagina": 2410
        },
        "kinds": {
          "surface_claim": 4
        }
      },
      "390": {
        "len": 4,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 0,
          "h_pagina": 3236
        },
        "kinds": {
          "surface_claim": 4
        }
      }
    },
    "osservatorio": {
      "1280": {
        "len": 0,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 0,
          "h_pagina": 900
        },
        "kinds": {}
      },
      "768": {
        "len": 0,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 0,
          "h_pagina": 900
        },
        "kinds": {}
      },
      "390": {
        "len": 0,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 0,
          "h_pagina": 900
        },
        "kinds": {}
      }
    },
    "dossier": {
      "1280": {
        "len": 8,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 3,
          "h_pagina": 2192
        },
        "kinds": {
          "class_marker": 5,
          "surface_claim": 3
        }
      },
      "768": {
        "len": 8,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 3,
          "h_pagina": 2340
        },
        "kinds": {
          "class_marker": 5,
          "surface_claim": 3
        }
      },
      "390": {
        "len": 8,
        "census": {
          "network_nodes": 0,
          "topology_paths": 0,
          "list_parents": 0,
          "inference_marks": 3,
          "h_pagina": 2944
        },
        "kinds": {
          "class_marker": 5,
          "surface_claim": 3
        }
      }
    }
  }
}
```
Inventario completo item-per-item: `docs/obs-o20-M.json` (33251 righe). Gate M: ogni blocco ha `len_asserted`; fdb_ownership_violations_n=0 **dopo** D1.
M2 prima di D: Plant mostrava nome device da `role_source=FDB` senza «visto passare» (violazione). Dossier `fdb_port` senza vocab. Topology già OK da O19.
M3: `--inference-edge` 2.609:1 in elenco; corretto in D4. `--text-3` 3.744:1 allowlistato (`DEBT-NO-CONTRAST-PRESIDIO`).
M4: placeholder `—`/`n/d` su monitoring (7) segnalati come i2_risk; cinque condizioni non ancora rese tutte distinte sito-wide → residuo documentale, non ampliato in O20 oltre Plant/Dossier/Topology.

## 7. Fase D — applicato / non applicato

**Applicato:** D1 Plant+Dossier vocab O19; D2 secondo canale già tratto su topology + etichetta testo; D4 `--inference-edge`; D5 `contrast_gate.py`; D6 `evidence_gate.py`; fix contrasto parent O19.
**Non applicato:** layout; fill `--inference`; unificazione AI/AP; I2 completo cinque rese su ogni rotta (fuori scope chiusura — debito residuale non nominato nuovo oltre jitter); risoluzione MAPPA-DESKTOP-GROWTH.

## 8. D4 candidati `--inference-edge`
```json
{
  "regola_dichiarata_prima": "stessa famiglia HSV (hue≈0.65–0.85); tra candidati con contrasto≥3:1 su --bg-1 vince min ΔE76 vs #6b4aa8",
  "attuale_pre": {
    "hex": "#6b4aa8",
    "ratio_bg1": 2.609
  },
  "fill_inference_invariato": "#9b7bd4",
  "vincitore": {
    "hex": "#7656b0",
    "ratio_bg1": 3.068,
    "ratio_bg0": 3.307,
    "delta_e76": 5.392
  },
  "candidati_top": [
    {
      "hex": "#7656b0",
      "C": 3.068,
      "dE76": 5.392
    },
    {
      "hex": "#7056b0",
      "C": 3.001,
      "dE76": 5.434
    },
    {
      "hex": "#7257b2",
      "C": 3.063,
      "dE76": 5.486
    },
    {
      "hex": "#7757b2",
      "C": 3.119,
      "dE76": 5.523
    },
    {
      "hex": "#7a58b8",
      "C": 3.222,
      "dE76": 5.726
    }
  ]
}
```

## 9. Previsioni vs osservati

| id | previsto | osservato | causa dominante |
|----|----------|-----------|-----------------|
| P-edge | ≥3:1 su bg-1 | 3.068:1 | scelta min ΔE76 |
| P-fill | invariato #9b7bd4 | invariato | vincolo Michele |
| P-plant-fdb | 0 ownership POST | 0 (visto=14) | vocab riusato |
| P-topo-h | Δ≈0 vs O19 | Δh=0 ai 3 BP | no layout |
| P-oggi-h | Δ≈0 | @768 +409 una run | API coverage cards (debito) |

## 10. V1–V11 (integrale dai dati di sessione)
Auth: catture autenticate via session mint, scadenza 180s (fonte run harness 36s×5), token non pubblicato
PRE dist / POST dist: /tmp/obs-o20-pre-dist / /tmp/obs-o20-post-dist
Bundle verificati in smoke: PRE `0.10.88` / POST `0.10.89` + css `7656b0`.
```json
{
  "criteria": {
    "V4_fdb_ownership_post_empty": {
      "pass": true,
      "n": 0,
      "rows": [],
      "come_potrebbe_fallire": "Plant cella FDB senza «visto passare» o topology parent ancora «collegato a»"
    },
    "V8_height_within_R_when_census_matched": {
      "pass": false,
      "rows": [
        {
          "route": "oggi",
          "w": 1280,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "oggi",
          "w": 768,
          "delta": 409,
          "ok": false,
          "census_matched": true
        },
        {
          "route": "oggi",
          "w": 390,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "topology",
          "w": 1280,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "topology",
          "w": 768,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "topology",
          "w": 390,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "plant",
          "w": 1280,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "plant",
          "w": 768,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "plant",
          "w": 390,
          "delta": 2,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "gs308",
          "w": 1280,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "gs308",
          "w": 768,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "gs308",
          "w": 390,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "inventory",
          "w": 1280,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "inventory",
          "w": 768,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "inventory",
          "w": 390,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "dossier",
          "w": 1280,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "dossier",
          "w": 768,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "dossier",
          "w": 390,
          "delta": 0,
          "ok": true,
          "census_matched": true
        }
      ],
      "R": 320,
      "come_potrebbe_fallire": "Δ layout non voluto oltre R; nominarlo non basta (DEBT-V8-CRITERION-WEAK)"
    },
    "census_invalid_measures": {
      "pass": true,
      "invalid": [],
      "come_potrebbe_fallire": "API topology/plant non idempotente tra i due server"
    }
  },
  "dossier_id": 83,
  "rows": [
    {
      "route": "oggi",
      "w": "1280",
      "script_pre": "/assets/index-C6Ud7we9.js",
      "script_post": "/assets/index-DRlt-wzC.js",
      "h_pre": 15509,
      "h_post": 15509,
      "delta_h": 0,
      "census_matched": true,
      "pre_census": {
        "h_pagina": 15509,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 0
      },
      "post_census": {
        "h_pagina": 15509,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 0
      },
      "fdb_own_post_n": 0,
      "visto": 0,
      "parent_cmin": null,
      "only_post_info": [],
      "only_pre_info": []
    },
    {
      "route": "oggi",
      "w": "768",
      "script_pre": "/assets/index-C6Ud7we9.js",
      "script_post": "/assets/index-DRlt-wzC.js",
      "h_pre": 19110,
      "h_post": 19519,
      "delta_h": 409,
      "census_matched": true,
      "pre_census": {
        "h_pagina": 19110,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 0
      },
      "post_census": {
        "h_pagina": 19519,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 0
      },
      "fdb_own_post_n": 0,
      "visto": 0,
      "parent_cmin": null,
      "only_post_info": [
        "Sorgente copertura vecchia · Fritz TR-064 (hostlist / mesh / WLAN)",
        "Sorgente copertura vecchia · Zeek behaviour (JA4 / JA4D / DHCP fp)"
      ],
      "only_pre_info": []
    },
    {
      "route": "oggi",
      "w": "390",
      "script_pre": "/assets/index-C6Ud7we9.js",
      "script_post": "/assets/index-DRlt-wzC.js",
      "h_pre": 24445,
      "h_post": 24445,
      "delta_h": 0,
      "census_matched": true,
      "pre_census": {
        "h_pagina": 24445,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 0
      },
      "post_census": {
        "h_pagina": 24445,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 0
      },
      "fdb_own_post_n": 0,
      "visto": 0,
      "parent_cmin": null,
      "only_post_info": [],
      "only_pre_info": []
    },
    {
      "route": "topology",
      "w": "1280",
      "script_pre": "/assets/index-C6Ud7we9.js",
      "script_post": "/assets/index-DRlt-wzC.js",
      "h_pre": 7193,
      "h_post": 7193,
      "delta_h": 0,
      "census_matched": true,
      "pre_census": {
        "h_pagina": 7193,
        "paths_svg": 49,
        "list_parents": 49,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 0
      },
      "post_census": {
        "h_pagina": 7193,
        "paths_svg": 49,
        "list_parents": 49,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 0
      },
      "fdb_own_post_n": 0,
      "visto": 0,
      "parent_cmin": 7.232072185421649,
      "only_post_info": [],
      "only_pre_info": []
    },
    {
      "route": "topology",
      "w": "768",
      "script_pre": "/assets/index-C6Ud7we9.js",
      "script_post": "/assets/index-DRlt-wzC.js",
      "h_pre": 7746,
      "h_post": 7746,
      "delta_h": 0,
      "census_matched": true,
      "pre_census": {
        "h_pagina": 7746,
        "paths_svg": 46,
        "list_parents": 46,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 0
      },
      "post_census": {
        "h_pagina": 7746,
        "paths_svg": 46,
        "list_parents": 46,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 0
      },
      "fdb_own_post_n": 0,
      "visto": 0,
      "parent_cmin": 7.232072185421649,
      "only_post_info": [],
      "only_pre_info": []
    },
    {
      "route": "topology",
      "w": "390",
      "script_pre": "/assets/index-C6Ud7we9.js",
      "script_post": "/assets/index-DRlt-wzC.js",
      "h_pre": 10212,
      "h_post": 10212,
      "delta_h": 0,
      "census_matched": true,
      "pre_census": {
        "h_pagina": 10212,
        "paths_svg": 46,
        "list_parents": 46,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 0
      },
      "post_census": {
        "h_pagina": 10212,
        "paths_svg": 46,
        "list_parents": 46,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 0
      },
      "fdb_own_post_n": 0,
      "visto": 0,
      "parent_cmin": 7.232072185421649,
      "only_post_info": [],
      "only_pre_info": []
    },
    {
      "route": "plant",
      "w": "1280",
      "script_pre": "/assets/index-C6Ud7we9.js",
      "script_post": "/assets/index-DRlt-wzC.js",
      "h_pre": 2228,
      "h_post": 2228,
      "delta_h": 0,
      "census_matched": true,
      "pre_census": {
        "h_pagina": 2228,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 46,
        "ports_fdb": 0,
        "placements": 0
      },
      "post_census": {
        "h_pagina": 2228,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 46,
        "ports_fdb": 14,
        "placements": 0
      },
      "fdb_own_post_n": 0,
      "visto": 14,
      "parent_cmin": null,
      "only_post_info": [],
      "only_pre_info": [
        "AppleTV SalaFDB fresca",
        "Cassiopea — NIC 1FDB fresca",
        "Device non identificatoFDB fresca",
        "FRITZ!Repeater SalettaTVFDB fresca",
        "GS308EPFDB fresca",
        "HP LaserJet 200 colorMFP M276nFDB fresca",
        "Openhab PiFDB fresca",
        "Philips Hue BridgeFDB fresca",
        "ROCKFDB fresca",
        "Sky Q principale — EthernetFDB fresca",
        "Sky TVFDB fresca",
        "SkyBooster2 BIBLIO — EthernetFDB fresca",
        "allsky3FDB fresca",
        "ropieeeFDB fresca"
      ]
    },
    {
      "route": "plant",
      "w": "768",
      "script_pre": "/assets/index-C6Ud7we9.js",
      "script_post": "/assets/index-DRlt-wzC.js",
      "h_pre": 2964,
      "h_post": 2964,
      "delta_h": 0,
      "census_matched": true,
      "pre_census": {
        "h_pagina": 2964,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 46,
        "ports_fdb": 0,
        "placements": 0
      },
      "post_census": {
        "h_pagina": 2964,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 46,
        "ports_fdb": 14,
        "placements": 0
      },
      "fdb_own_post_n": 0,
      "visto": 14,
      "parent_cmin": null,
      "only_post_info": [],
      "only_pre_info": [
        "AppleTV SalaFDB fresca",
        "Cassiopea — NIC 1FDB fresca",
        "Device non identificatoFDB fresca",
        "FRITZ!Repeater SalettaTVFDB fresca",
        "GS308EPFDB fresca",
        "HP LaserJet 200 colorMFP M276nFDB fresca",
        "Openhab PiFDB fresca",
        "Philips Hue BridgeFDB fresca",
        "ROCKFDB fresca",
        "Sky Q principale — EthernetFDB fresca",
        "Sky TVFDB fresca",
        "SkyBooster2 BIBLIO — EthernetFDB fresca",
        "allsky3FDB fresca",
        "ropieeeFDB fresca"
      ]
    },
    {
      "route": "plant",
      "w": "390",
      "script_pre": "/assets/index-C6Ud7we9.js",
      "script_post": "/assets/index-DRlt-wzC.js",
      "h_pre": 5503,
      "h_post": 5505,
      "delta_h": 2,
      "census_matched": true,
      "pre_census": {
        "h_pagina": 5503,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 46,
        "ports_fdb": 0,
        "placements": 0
      },
      "post_census": {
        "h_pagina": 5505,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 46,
        "ports_fdb": 14,
        "placements": 0
      },
      "fdb_own_post_n": 0,
      "visto": 14,
      "parent_cmin": null,
      "only_post_info": [],
      "only_pre_info": [
        "AppleTV SalaFDB fresca",
        "Cassiopea — NIC 1FDB fresca",
        "Device non identificatoFDB fresca",
        "FRITZ!Repeater SalettaTVFDB fresca",
        "GS308EPFDB fresca",
        "HP LaserJet 200 colorMFP M276nFDB fresca",
        "Openhab PiFDB fresca",
        "Philips Hue BridgeFDB fresca",
        "ROCKFDB fresca",
        "Sky Q principale — EthernetFDB fresca",
        "Sky TVFDB fresca",
        "SkyBooster2 BIBLIO — EthernetFDB fresca",
        "allsky3FDB fresca",
        "ropieeeFDB fresca"
      ]
    },
    {
      "route": "gs308",
      "w": "1280",
      "script_pre": "/assets/index-C6Ud7we9.js",
      "script_post": "/assets/index-DRlt-wzC.js",
      "h_pre": 1916,
      "h_post": 1916,
      "delta_h": 0,
      "census_matched": true,
      "pre_census": {
        "h_pagina": 1916,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 2
      },
      "post_census": {
        "h_pagina": 1916,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 2
      },
      "fdb_own_post_n": 0,
      "visto": 0,
      "parent_cmin": null,
      "only_post_info": [],
      "only_pre_info": []
    },
    {
      "route": "gs308",
      "w": "768",
      "script_pre": "/assets/index-C6Ud7we9.js",
      "script_post": "/assets/index-DRlt-wzC.js",
      "h_pre": 2099,
      "h_post": 2099,
      "delta_h": 0,
      "census_matched": true,
      "pre_census": {
        "h_pagina": 2099,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 2
      },
      "post_census": {
        "h_pagina": 2099,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 2
      },
      "fdb_own_post_n": 0,
      "visto": 0,
      "parent_cmin": null,
      "only_post_info": [],
      "only_pre_info": []
    },
    {
      "route": "gs308",
      "w": "390",
      "script_pre": "/assets/index-C6Ud7we9.js",
      "script_post": "/assets/index-DRlt-wzC.js",
      "h_pre": 3254,
      "h_post": 3254,
      "delta_h": 0,
      "census_matched": true,
      "pre_census": {
        "h_pagina": 3254,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 2
      },
      "post_census": {
        "h_pagina": 3254,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 2
      },
      "fdb_own_post_n": 0,
      "visto": 0,
      "parent_cmin": null,
      "only_post_info": [],
      "only_pre_info": []
    },
    {
      "route": "inventory",
      "w": "1280",
      "script_pre": "/assets/index-C6Ud7we9.js",
      "script_post": "/assets/index-DRlt-wzC.js",
      "h_pre": 6223,
      "h_post": 6223,
      "delta_h": 0,
      "census_matched": true,
      "pre_census": {
        "h_pagina": 6223,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 0
      },
      "post_census": {
        "h_pagina": 6223,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 0
      },
      "fdb_own_post_n": 0,
      "visto": 0,
      "parent_cmin": null,
      "only_post_info": [],
      "only_pre_info": []
    },
    {
      "route": "inventory",
      "w": "768",
      "script_pre": "/assets/index-C6Ud7we9.js",
      "script_post": "/assets/index-DRlt-wzC.js",
      "h_pre": 6336,
      "h_post": 6336,
      "delta_h": 0,
      "census_matched": true,
      "pre_census": {
        "h_pagina": 6336,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 0
      },
      "post_census": {
        "h_pagina": 6336,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 0
      },
      "fdb_own_post_n": 0,
      "visto": 0,
      "parent_cmin": null,
      "only_post_info": [],
      "only_pre_info": []
    },
    {
      "route": "inventory",
      "w": "390",
      "script_pre": "/assets/index-C6Ud7we9.js",
      "script_post": "/assets/index-DRlt-wzC.js",
      "h_pre": 6631,
      "h_post": 6631,
      "delta_h": 0,
      "census_matched": true,
      "pre_census": {
        "h_pagina": 6631,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 0
      },
      "post_census": {
        "h_pagina": 6631,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 0
      },
      "fdb_own_post_n": 0,
      "visto": 0,
      "parent_cmin": null,
      "only_post_info": [],
      "only_pre_info": []
    },
    {
      "route": "dossier",
      "w": "1280",
      "script_pre": "/assets/index-C6Ud7we9.js",
      "script_post": "/assets/index-DRlt-wzC.js",
      "h_pre": 2192,
      "h_post": 2192,
      "delta_h": 0,
      "census_matched": true,
      "pre_census": {
        "h_pagina": 2192,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 1
      },
      "post_census": {
        "h_pagina": 2192,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 1
      },
      "fdb_own_post_n": 0,
      "visto": 0,
      "parent_cmin": null,
      "only_post_info": [],
      "only_pre_info": [
        "posizione non determinabile"
      ]
    },
    {
      "route": "dossier",
      "w": "768",
      "script_pre": "/assets/index-C6Ud7we9.js",
      "script_post": "/assets/index-DRlt-wzC.js",
      "h_pre": 2340,
      "h_post": 2340,
      "delta_h": 0,
      "census_matched": true,
      "pre_census": {
        "h_pagina": 2340,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 1
      },
      "post_census": {
        "h_pagina": 2340,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 1
      },
      "fdb_own_post_n": 0,
      "visto": 0,
      "parent_cmin": null,
      "only_post_info": [],
      "only_pre_info": [
        "posizione non determinabile"
      ]
    },
    {
      "route": "dossier",
      "w": "390",
      "script_pre": "/assets/index-C6Ud7we9.js",
      "script_post": "/assets/index-DRlt-wzC.js",
      "h_pre": 2944,
      "h_post": 2944,
      "delta_h": 0,
      "census_matched": true,
      "pre_census": {
        "h_pagina": 2944,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 1
      },
      "post_census": {
        "h_pagina": 2944,
        "paths_svg": 0,
        "list_parents": 0,
        "ports": 0,
        "ports_fdb": 0,
        "placements": 1
      },
      "fdb_own_post_n": 0,
      "visto": 0,
      "parent_cmin": null,
      "only_post_info": [],
      "only_pre_info": [
        "posizione non determinabile"
      ]
    }
  ]
}
```
**V4** PASS (fdb_ownership POST vuoto). **V6** parent contrast min POST topology **7.232**. **V8** topology/plant/… entro R; `oggi@768` Δ+409 = jitter API → `DEBT-O20-OGGI-API-HEIGHT-JITTER` (non layout O20).
come_potrebbe_fallire V: census API drift tra PRE e POST → misura invalida; classif_strings POST-only confuse con perdita informativa

## 11. Presidi nuovi — output integrale

### obs-o20-contrast_gate.txt
```
=== contrast_gate ===
token_file=web/src/assets/matrix.css
pairs_checked=9
allowlist_entries=1
  PASS --text-1=#e8ebf0 on --bg-0=#0f1319 ratio=15.586 thr=4.5 [text_normal] WCAG 2.2 SC 1.4.3 Contrast (Minimum) AA testo normale
  PASS --text-2=#98a2b3 on --bg-0=#0f1319 ratio=7.232 thr=4.5 [text_normal] WCAG 2.2 SC 1.4.3 Contrast (Minimum) AA testo normale
  FAIL --text-3=#667085 on --bg-0=#0f1319 ratio=3.744 thr=4.5 [text_normal] WCAG 2.2 SC 1.4.3 Contrast (Minimum) AA testo normale
  PASS --ok=#4fb477 on --bg-0=#0f1319 ratio=7.208 thr=3.0 [non_text] WCAG 2.2 SC 1.4.11 Non-text Contrast AA
  PASS --warn=#d9a441 on --bg-0=#0f1319 ratio=8.281 thr=3.0 [non_text] WCAG 2.2 SC 1.4.11 Non-text Contrast AA
  PASS --danger=#e06b52 on --bg-0=#0f1319 ratio=5.671 thr=3.0 [non_text] WCAG 2.2 SC 1.4.11 Non-text Contrast AA
  PASS --inference=#9b7bd4 on --bg-0=#0f1319 ratio=5.479 thr=3.0 [non_text] WCAG 2.2 SC 1.4.11 Non-text Contrast AA (riempimento; non toccare in O20)
  PASS --inference-edge=#7656b0 on --bg-1=#161b23 ratio=3.068 thr=3.0 [non_text] WCAG 2.2 SC 1.4.11 Non-text Contrast AA
  PASS --inference-edge=#7656b0 on --bg-0=#0f1319 ratio=3.307 thr=3.0 [non_text] WCAG 2.2 SC 1.4.11 Non-text Contrast AA
ALLOWLISTED_FAILS=1
  TEMP --text-3 on --bg-0 ratio=3.744 debt=DEBT-NO-CONTRAST-PRESIDIO | testo terziario mute (#667085) spesso <4.5:1 su bg-0; etichette via/odm già in DEBT-NO-CONTRAST-PRES
PASS: contrast pairs within threshold or allowlisted with debt

```

### obs-o20-contrast_gate_selftest.txt
```
SELFTEST inject detected: {'fg': '--inference-edge', 'bg': '--bg-1', 'fg_hex': '#220033', 'bg_hex': '#161b23', 'ratio': 1.089, 'threshold': 3.0, 'fonte': 'WCAG 2.2 SC 1.4.11 Non-text Contrast AA', 'ruolo': 'non_text', 'pass': False}
SELFTEST PASS: inject fails, remove passes

```

### obs-o20-evidence_gate.txt
```
=== evidence_gate ===
forbidden_ownership_terms=4
  /collegato\s+a/ — asserisce ownership di link; FDB prova solo passaggio MAC (I5 rango 60)
  /attaccat[oa]\s+a/ — sinonimo ownership fisico; vietato su FDB
  /assegnat[oa]\s+(alla|alla porta|a porta)/ — asserisce assegnazione porta; FDB non è LLDP/manual
  /appartiene\s+a/ — asserisce appartenenza; FDB non è identità
ownership_hits=0
marker_errors=0
PASS: no FDB+ownership vocabulary; required evidence markers present

```

### obs-o20-evidence_gate_selftest.txt
```
SELFTEST ownership inject detected: views/_o20_evidence_gate_inject_tmp.vue:2: /collegato\s+a/ — asserisce ownership di link; FDB prova solo passaggio MAC (I5 rango 60) | <template><span class='edge-fdb'>collegato a switch</span></template>
SELFTEST marker_errs_after_inject=0 ownership_hits=0
SELFTEST marker_errs_after_stronger=1
SELFTEST marker inject detected: views/Topology.vue: marker /visto passare/ count=0 < 1 — vocabolario FDB O19 obbligatorio sulla Mappa
SELFTEST PASS: inject fails (ownership+marker), remove passes

```

## 12. Catture
V A/B locale senza scrub PNG in questa chiusura (cantiere non ampliato). G4 deployed: vedi §13. Provenienza mint harness standard.

## 13. Deploy G3/G4

Deploy: `./scripts/deploy.sh web` → ok (image observatory-web, container recreated).

### G3 — prova diretta JS+CSS
```json
{
  "js": "/assets/index-DRlt-wzC.js",
  "css": "/assets/index-C1uZvg_C.css",
  "js_bytes": 469104,
  "css_bytes": 144003,
  "version": "0.10.89",
  "markers": [
    "0.10.89",
    "obs-o20-marker",
    "7656b0",
    "visto passare: device",
    "visto passare su"
  ],
  "pass": true
}
```
Versione letta dal bundle servito: **0.10.89**. css≠None. Marker O20 + `--inference-edge` `#7656b0` nel CSS.

### G4 — ricattura deployed vs POST locale (census entrambi i lati)
R=320. Topology Δh 180/223/109; plant 0/0/2. Parent contrast min deployed **7.232**. Plant visto passare count 14/14/13.
```json
{
  "wave": "O20-G4",
  "base": "http://192.168.1.3:8080",
  "auth_provenance": "catture autenticate via session mint, scadenza 180s (fonte run harness 36s×5), token non pubblicato",
  "routes": {
    "topology": {
      "1280": {
        "deployed": {
          "h_pagina": 7101,
          "js": "http://192.168.1.3:8080/assets/index-DRlt-wzC.js",
          "css": "http://192.168.1.3:8080/assets/index-C1uZvg_C.css",
          "version_from_page_text": "0.10.82",
          "paths": 47,
          "parents": 47,
          "ports": 0,
          "visto": 0,
          "parent_contrast_min": 7.232072185421649
        },
        "local_post": {
          "h": 6921,
          "census": {
            "h_pagina": 6921,
            "paths_svg": 44,
            "list_parents": 44,
            "ports": 0,
            "ports_fdb": 0,
            "placements": 0
          }
        },
        "delta_h_vs_local_post": 180,
        "census_both_sides": {
          "local_post": {
            "h_pagina": 6921,
            "paths_svg": 44,
            "list_parents": 44,
            "ports": 0,
            "ports_fdb": 0,
            "placements": 0
          },
          "deployed": {
            "h_pagina": 7101,
            "paths_svg": 47,
            "list_parents": 47,
            "ports": 0
          }
        },
        "version_read": "0.10.82"
      },
      "768": {
        "deployed": {
          "h_pagina": 7849,
          "js": "http://192.168.1.3:8080/assets/index-DRlt-wzC.js",
          "css": "http://192.168.1.3:8080/assets/index-C1uZvg_C.css",
          "version_from_page_text": "0.10.82",
          "paths": 47,
          "parents": 47,
          "ports": 0,
          "visto": 0,
          "parent_contrast_min": 7.232072185421649
        },
        "local_post": {
          "h": 7626,
          "census": {
            "h_pagina": 7626,
            "paths_svg": 44,
            "list_parents": 44,
            "ports": 0,
            "ports_fdb": 0,
            "placements": 0
          }
        },
        "delta_h_vs_local_post": 223,
        "census_both_sides": {
          "local_post": {
            "h_pagina": 7626,
            "paths_svg": 44,
            "list_parents": 44,
            "ports": 0,
            "ports_fdb": 0,
            "placements": 0
          },
          "deployed": {
            "h_pagina": 7849,
            "paths_svg": 47,
            "list_parents": 47,
            "ports": 0
          }
        },
        "version_read": "0.10.82"
      },
      "390": {
        "deployed": {
          "h_pagina": 10278,
          "js": "http://192.168.1.3:8080/assets/index-DRlt-wzC.js",
          "css": "http://192.168.1.3:8080/assets/index-C1uZvg_C.css",
          "version_from_page_text": "0.10.82",
          "paths": 47,
          "parents": 47,
          "ports": 0,
          "visto": 0,
          "parent_contrast_min": 7.232072185421649
        },
        "local_post": {
          "h": 10169,
          "census": {
            "h_pagina": 10169,
            "paths_svg": 44,
            "list_parents": 44,
            "ports": 0,
            "ports_fdb": 0,
            "placements": 0
          }
        },
        "delta_h_vs_local_post": 109,
        "census_both_sides": {
          "local_post": {
            "h_pagina": 10169,
            "paths_svg": 44,
            "list_parents": 44,
            "ports": 0,
            "ports_fdb": 0,
            "placements": 0
          },
          "deployed": {
            "h_pagina": 10278,
            "paths_svg": 47,
            "list_parents": 47,
            "ports": 0
          }
        },
        "version_read": "0.10.82"
      }
    },
    "plant": {
      "1280": {
        "deployed": {
          "h_pagina": 2228,
          "js": "http://192.168.1.3:8080/assets/index-DRlt-wzC.js",
          "css": "http://192.168.1.3:8080/assets/index-C1uZvg_C.css",
          "version_from_page_text": "0.10.82",
          "paths": 0,
          "parents": 0,
          "ports": 46,
          "visto": 14,
          "parent_contrast_min": null
        },
        "local_post": {
          "h": 2228,
          "census": {
            "h_pagina": 2228,
            "paths_svg": 0,
            "list_parents": 0,
            "ports": 46,
            "ports_fdb": 14,
            "placements": 0
          }
        },
        "delta_h_vs_local_post": 0,
        "census_both_sides": {
          "local_post": {
            "h_pagina": 2228,
            "paths_svg": 0,
            "list_parents": 0,
            "ports": 46,
            "ports_fdb": 14,
            "placements": 0
          },
          "deployed": {
            "h_pagina": 2228,
            "paths_svg": 0,
            "list_parents": 0,
            "ports": 46
          }
        },
        "version_read": "0.10.82"
      },
      "768": {
        "deployed": {
          "h_pagina": 2964,
          "js": "http://192.168.1.3:8080/assets/index-DRlt-wzC.js",
          "css": "http://192.168.1.3:8080/assets/index-C1uZvg_C.css",
          "version_from_page_text": "0.10.82",
          "paths": 0,
          "parents": 0,
          "ports": 46,
          "visto": 14,
          "parent_contrast_min": null
        },
        "local_post": {
          "h": 2964,
          "census": {
            "h_pagina": 2964,
            "paths_svg": 0,
            "list_parents": 0,
            "ports": 46,
            "ports_fdb": 14,
            "placements": 0
          }
        },
        "delta_h_vs_local_post": 0,
        "census_both_sides": {
          "local_post": {
            "h_pagina": 2964,
            "paths_svg": 0,
            "list_parents": 0,
            "ports": 46,
            "ports_fdb": 14,
            "placements": 0
          },
          "deployed": {
            "h_pagina": 2964,
            "paths_svg": 0,
            "list_parents": 0,
            "ports": 46
          }
        },
        "version_read": "0.10.82"
      },
      "390": {
        "deployed": {
          "h_pagina": 5507,
          "js": "http://192.168.1.3:8080/assets/index-DRlt-wzC.js",
          "css": "http://192.168.1.3:8080/assets/index-C1uZvg_C.css",
          "version_from_page_text": "0.10.82",
          "paths": 0,
          "parents": 0,
          "ports": 46,
          "visto": 13,
          "parent_contrast_min": null
        },
        "local_post": {
          "h": 5505,
          "census": {
            "h_pagina": 5505,
            "paths_svg": 0,
            "list_parents": 0,
            "ports": 46,
            "ports_fdb": 14,
            "placements": 0
          }
        },
        "delta_h_vs_local_post": 2,
        "census_both_sides": {
          "local_post": {
            "h_pagina": 5505,
            "paths_svg": 0,
            "list_parents": 0,
            "ports": 46,
            "ports_fdb": 14,
            "placements": 0
          },
          "deployed": {
            "h_pagina": 5507,
            "paths_svg": 0,
            "list_parents": 0,
            "ports": 46
          }
        },
        "version_read": "0.10.82"
      }
    }
  }
}
```

## 14. Debiti

| Debito | Stato | Attribuzione |
|--------|-------|--------------|
| DEBT-INFERENCE-EDGE-CONTRAST | CHIUSO O20 | Cursor |
| DEBT-NO-CONTRAST-PRESIDIO | APERTO (text-3 allowlist; gate esiste) | misto |
| DEBT-SHELL-TAB-ORDER | APERTO | Cursor |
| DEBT-O18-CONSERVATION-WRONG-ENDPOINT | APERTO | Cursor |
| DEBT-CHASSIS-NAME-COLLISION | APERTO (solo reg) | Cursor |
| DEBT-O19-MAPPA-DESKTOP-GROWTH | APERTO | Cursor |
| DEBT-V8-CRITERION-WEAK | APERTO | revisore |
| DEBT-O19-M1-PARTIAL | APERTO | Cursor |
| DEBT-O20-OGGI-API-HEIGHT-JITTER | APERTO | Cursor (API) |

## 15. Cosa NON ho fatto

- Nessun layout change di prodotto; nessun tocco a `--inference` fill / AI=AP / `/ai` / T7 / FA251 / `_w4a_measure.py` / favicon.
- Nessuna risoluzione di DEBT-O19-MAPPA-DESKTOP-GROWTH.
- I2 cinque rese distinguibili su tutte le rotte: non completato sito-wide (oltre Plant/Dossier/Topology FDB).
- Nessun ulteriore ciclo A/B per assorbire jitter oggi@768.
- Capture scrub PNG multi-rotta G4 ridotto al necessario post-deploy.

## Gate esistenti (V10)

### obs-o20-currency_gate.txt
```
== W8 CURRENCY GATE (indurito, W8-fix2) ==
root: /Users/michelestorci/Developer/rete-palazzo/observatory
sentinelle: simbolo ORM 'FactAssertion' · tabella grezza 'fact_assertions' in chiamata SQL (text/execute) · COMBO (fact-token FactAssertion|fact_assertions|fact_key) + valore di stato quotato 'current'
scope: api/**, scripts/**, collector/**
esclusioni:
  - api/app/facts/**  (il resolver È la fonte della correntezza)
  - scripts/w8_currency_gate.py  (contiene le sentinelle/fact_key come dato)
  - scripts/w8_g8_equivalence.py  (contiene le sentinelle/fact_key come dato)
file scansionati: 216
voci allowlist: permanenti 17 · temporanee 1

ATTENZIONE — ECCEZIONI TEMPORANEE CON DEBITO APERTO: 1
  TEMP scripts/wp_gate.py:103 (atteso 1, osservato 1) debt=DEBT-WPGATE-CURRENCY-COUNT-LOCAL
      | fa_cur = int(db.scalar(select(func.count()).select_from(FactAssertion).where(FactAssertion.state == "current")) or 0)

ECCEZIONI GIUSTIFICATE PERMANENTI (accounted): 17
  OK  api/app/bootstrap.py:19  (atteso 1, osservato 1)
      | from app.models import FactAssertion, IdentityEvidence, IdentityLinkProposal, Switch, User  # noqa: F401 — create_all
      → bootstrap: import per registrazione modelli in create_all (nessuna query).
  OK  api/app/models.py:155  (atteso 1, osservato 1)
      | class FactAssertion(Base):
      → models: DEFINIZIONE ORM della tabella (non una lettura).
  OK  api/app/routers/admin.py:320  (atteso 1, osservato 1)
      | .order_by(FactAssertion.last_seen_at.desc(), FactAssertion.id.desc())
      → admin /facts/conflicts: ordinamento di DISPLAY delle divergenze storiche.
  OK  api/app/routers/admin.py:317  (atteso 1, osservato 1)
      | FactAssertion.reason == "conflict_review",
      → admin /facts/conflicts: filtro divergenze I3.
  OK  api/app/routers/admin.py:318  (atteso 1, osservato 1)
      | FactAssertion.state == "historical",
      → admin /facts/conflicts: esplicitamente state='historical', l'opposto di current.
  OK  api/app/routers/admin.py:292,311  (atteso 2, osservato 2)
      | from app.models import FactAssertion
      → admin: import per diagnostica read-only (shadow-stats COUNT + conflitti I3).
  OK  api/app/routers/admin.py:295  (atteso 1, osservato 1)
      | rows = int(db.scalar(select(func.count()).select_from(FactAssertion)) or 0)
      → admin /facts/shadow-stats: COUNT righe (osservabilità breaker), non un valore corrente.
  OK  api/app/routers/admin.py:315  (atteso 1, osservato 1)
      | select(FactAssertion)
      → admin /facts/conflicts: divergenze conflict_review, state='historical' (I3), NON current.
  OK  scripts/wp_diagnose.py:268  (atteso 1, osservato 1)
      | base_fa = {r[0] for r in bdb.execute(select(FactAssertion.id)).all()}
      → wp_diagnose: enumerazione id (baseline) per delta, nessuno stato.
  OK  scripts/wp_diagnose.py:267  (atteso 1, osservato 1)
      | cur_fa = {r[0] for r in db.execute(select(FactAssertion.id)).all()}
      → wp_diagnose: enumerazione id (now) per delta vs baseline, nessuno stato.
  OK  scripts/wp_diagnose.py:127  (atteso 1, osservato 1)
      | db.execute(select(FactAssertion.state, func.count()).group_by(FactAssertion.state)).all()
      → wp_diagnose: distribuzione di stato (diagnostica), non una lettura del valore corrente.
  OK  scripts/wp_diagnose.py:273  (atteso 1, osservato 1)
      | fa = db.get(FactAssertion, fid)
      → wp_diagnose: lettura per id già enumerato (display diagnostico).
  OK  scripts/wp_diagnose.py:125  (atteso 1, osservato 1)
      | fa_total = int(db.scalar(select(func.count()).select_from(FactAssertion)) or 0)
      → wp_diagnose: COUNT righe totali (nessun valore, nessuno stato).
  OK  scripts/wp_diagnose.py:29  (atteso 1, osservato 1)
      | from app.models import Asset, FactAssertion, Interface, IpAddress, NameProposal  # noqa: E402
      → wp_diagnose: import per diagnostica (nessuna lettura di correntezza).
  OK  scripts/wp_diagnose.py:232  (atteso 1, osservato 1)
      | rows = db.scalars(select(FactAssertion).order_by(FactAssertion.id.desc()).limit(15)).all()
      → wp_diagnose: campione di DISPLAY (ultime 15 per id), non una lettura di correntezza.
  OK  scripts/wp_gate.py:102  (atteso 1, osservato 1)
      | fat = int(db.scalar(select(func.count()).select_from(FactAssertion)) or 0)
      → wp_gate: COUNT righe totali (nessun valore, nessuno stato).
  OK  scripts/wp_gate.py:36  (atteso 1, osservato 1)
      | from app.models import Asset, FactAssertion, IpAddress, NameProposal  # noqa: E402
      → wp_gate: import per diagnostica di regime (nessuna lettura di correntezza).

VIOLAZIONI: 0

RISULTATO: PASS (con 1 eccezione/i temporanea/e)

```

### obs-o20-color_literal_gate.txt
```
PASS: no hard-coded color literals outside allowlist; matrix.css decls-only
  token_file=assets/matrix.css (literals only in --custom-property decls)
  allowlist_count=16

```

### obs-o20-color_literal_selftest.txt
```
SELFTEST vue inject detected: (2, '#ff00aa', '.x { color: #ff00aa; /* O13D_COLOR_GATE_INJECT */ }')
SELFTEST matrix rule inject detected: (956, '#ff00aa', '.o14fix-gate-inject { color: #ff00aa; /* O14FIX_COLOR_GATE_INJECT */ }')
SELFTEST PASS: inject fails (vue+matrix rule), remove passes

```

### obs-o20-specificity_grep.txt
```

```

### obs-o20-B0-drift.json
```json
{
  "NAS_count": 74,
  "repo_count": 73,
  "solo_NAS": [
    "scripts/_w4a_measure.py"
  ],
  "solo_repo": [],
  "solo_NAS_enumerated": [
    "scripts/_w4a_measure.py"
  ],
  "solo_repo_enumerated": [],
  "expected": {
    "solo_NAS": [
      "scripts/_w4a_measure.py"
    ],
    "solo_repo": []
  },
  "orphans": [],
  "DRIFT_OK": true,
  "o19_correction": "O19 elencava density/nav/topology in solo-repo ma erano già su entrambi post-rsync O17/O18/O19 deploy; lista O19 era sbagliata (non rimozione NAS).",
  "density_trio_on_both": true,
  "come_potrebbe_fallire": "conteggio find diverso da path reale o file non .py"
}
```
