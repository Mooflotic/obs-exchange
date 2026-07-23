<!-- BLOCK-ID: OBS-FINGERPRINT-FASEA-024 -->

# OBS-FINGERPRINT-FASEA-024 — Fingerprinting device (sola lettura)

**STOP FASE A** — nessuna modifica a codice/immagine/Zeek.  
**Live:** Cassiopea · Zeek `zeek/zeek:8.2` (8.2.0) · profilo `span` · log `data/zeek/`  
**Data verifica:** 2026-07-23

Obiettivo futuro: sintesi AI sul **fingerprint completo** (bundle di segnali
passivi), non su un singolo dato. Questa fase mappa cosa c’è e cosa manca.

---

## VERIFICA 1 — JA3 / JA4 (make-or-break)

### 1. `ssl.log` ha `ja3` / `ja3s` / `ja4`?

**No.** Campione su ~71k record JSON (file correnti + rotati letti fino a
cap). Chiavi osservate:

```
cert_chain_fps, cipher, client_cert_chain_fps, curve, established,
id.orig_h, id.orig_p, id.resp_h, id.resp_p, last_alert, next_protocol,
resumed, server_name, sni_matches_cert, ssl_history, ts, uid, version
```

Conteggi: `ja3_filled=0` · `ja3s_filled=0` · `ja4_filled=0` · `ja3_distinct=0`.

### 5 righe reali (tutti i campi presenti)

```json
{"cert_chain_fps":["98f358cde2814cf83ca4db99321a67a240c552ad9d37801bca265f7e0f3d2518","138bdf6e23ac971eb4e626b279dd6a26f057510f1de394293a5eea2860de019b","87dcd4dc74640a322cd205552506d1be64f12596258096544986b4850bc72706"],"cipher":"TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256","client_cert_chain_fps":[],"curve":"secp256r1","established":true,"id.orig_h":"192.168.2.93","id.orig_p":42750,"id.resp_h":"13.224.119.231","id.resp_p":443,"next_protocol":"h2","resumed":false,"server_name":"api.amazonalexa.com","sni_matches_cert":true,"ssl_history":"CsxknGIti","ts":1784818803.631269,"uid":"CauMBA4wtCxB53EMR2","version":"TLSv12"}
```

```json
{"cert_chain_fps":["f492d657f9095e199a3921f7154310be7e3afae75e6335a0217515c84081588f","e5674847f46d75b18e2317d5e57d59018e602a521d00d8c0c3e6e52e9057bb96","45f805760a824a94615056182f267c25f775346549d6137d94c4e00bf9075aca"],"cipher":"TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256","client_cert_chain_fps":[],"curve":"secp256r1","established":true,"id.orig_h":"192.168.2.109","id.orig_p":47278,"id.resp_h":"52.48.41.28","id.resp_p":443,"resumed":false,"server_name":"diag.meethue.com","sni_matches_cert":true,"ssl_history":"CsxknGIi","ts":1784818805.79792,"uid":"CtSbkS2gGguc7Nu4fe","version":"TLSv12"}
```

```json
{"cipher":"TLS_AES_256_GCM_SHA384","curve":"X25519MLKEM768","established":true,"id.orig_h":"192.168.1.3","id.orig_p":40748,"id.resp_h":"104.16.123.96","id.resp_p":443,"resumed":false,"server_name":"www.cloudflare.com","ssl_history":"CsiI","ts":1784818806.659079,"uid":"C15Oprdv0CQiRGWx8","version":"TLSv13"}
```

```json
{"cipher":"TLS_AES_256_GCM_SHA384","curve":"X25519MLKEM768","established":true,"id.orig_h":"192.168.1.3","id.orig_p":37140,"id.resp_h":"142.251.209.35","id.resp_p":443,"resumed":false,"server_name":"connectivitycheck.gstatic.com","ssl_history":"CsiI","ts":1784818806.648712,"uid":"CKDrsy3nD0ZCw4C3j6","version":"TLSv13"}
```

```json
{"cipher":"TLS_AES_256_GCM_SHA384","curve":"x25519","established":true,"id.orig_h":"192.168.1.3","id.orig_p":56346,"id.resp_h":"192.168.1.117","id.resp_p":443,"resumed":false,"ssl_history":"CsiI","ts":1784818808.703429,"uid":"CzE2c24X2z2yX8fxWk","version":"TLSv13"}
```

Nota collaterale utile: c’è già `ssl_history` (sequenza eventi handshake
Zeek). Su ~14k righe (file recenti): **23** valori distinti; top stack
`CsiI` / `CsxknGIti` / `CsxknGIi`. È un proxy grezzo di “stack”, **non**
un JA3 — troppo collassato (es. `CsxknGIi` visto su 41 IP client diversi).

### 2. Se non c’è: package? Installazione? Impatto? Rischio?

**Serve un package.** Stock `zeek/zeek:8.2` **non** scrive JA3/JA4.

| Opzione | Pacchetto | Output tipico |
|---|---|---|
| **Consigliata (2026)** | `zkg install zeek/foxio/ja4` (FoxIO JA4+) | `ja4` / `ja4s` in `ssl.log`; anche JA4H/L/T; **JA4D** → `ja4d.log` (DHCP) |
| Legacy | `zeek/ja3` (Salesforce / community) | `ja3` / `ja3s` in `ssl.log` |

**Come nell’immagine Observatory (oggi = image ufficiale, nessun Dockerfile Zeek custom):**

1. Introdurre `zeek/Dockerfile` basato su `zeek/zeek:8.2`:
   ```dockerfile
   FROM zeek/zeek:8.2
   RUN zkg refresh && zkg install --force zeek/foxio/ja4 \
       && echo '@load packages' >> /usr/local/zeek/share/zeek/site/local.zeek
   ```
   oppure vendoring dei script in `observatory/zeek/site/ja4` + `@load ja4`
   in `zeek/local.zeek` (niente zkg a runtime).
2. `docker-compose.yml`: `image:` → `build: ./zeek` (solo profilo `span`).
3. Policy: oggi `local.zeek` carica solo `@load base/protocols/conn`;
   ssl/dns/dhcp arrivano perché **non** si usa `-b` (init-default).
   Per JA4: aggiungere `@load ja4` (o `@load packages`) in
   `zeek/local.zeek` **e** assicurarsi che il package sia nel path site
   (attenzione: con policy custom senza `local` site, `@load ja4`
   esplicito è obbligatorio — issue nota FoxIO).
4. Entrypoint: estendere prune a `ja4d*.log` / eventuali log extra.
5. Collector: nuovo provider (FASE B+) che legge `ja4` da ssl e lo
   associa a `src_ip` → asset (stesso gate `resolve_asset_by_ip_at`).

**Costo / rischio**

| Voce | Valutazione |
|---|---|
| CPU/RAM | Medio-basso: script Bro su ClientHello già visto; monitorare tetto compose `768m` |
| Stabilità | Medio: package esterno; pin versione zkg; rebuild immagine riproducibile |
| Privacy | Hash/client fingerprint ≠ PII; OK se non si logga SNI+nome interno insieme nel prompt |
| Ops | Rebuild Zeek + recreate container SPAN; breve buco mirror |
| Alternativa JA3 only | Più stretta; JA4 è il successore e porta JA4D (DHCP) nello stesso pezzo |

**Verdetto make-or-break:** senza package **non** c’è fingerprint TLS
client utilizzabile. Con FoxIO JA4+ si sblocca anche il filone DHCP
(JA4D) che oggi manca (vedi §2).

### 3. Se ci fosse: coverage? (non misurabile ora)

Con `ja3_filled=0` le metriche richieste sono tutte **0**.  
Dopo install: da misurare su 24–48h — % `ssl` con `ja4` valorizzato,
`count(distinct id.orig_h)`, `count(distinct ja4)`.

---

## VERIFICA 2 — DHCP fingerprint

### 4. `dhcp.log` — option 55 / campi / coverage

**Esiste** (pruned 48h). **Non** c’è un `dhcp.log` “current” sempre:
solo rotati orari. Formato JSON.

**Campi osservati (172 eventi su retention locale):**

```
assigned_addr, client_addr, client_fqdn, domain, duration, host_name,
lease_time, mac, msg_types, requested_addr, server_addr, ts, uids
```

- **Option 55 (parameter request list):** **assente** — nessun
  `request_list` / equivalente. `rows_with_request_listish=0`.
- Coverage grezza: **37 MAC distinti** · **28** con `host_name` ·
  msg tipici DISCOVER/REQUEST/ACK (lease Fritz 10g).
- Copertura = solo host che rinnovano/ottengono lease **mentre** Zeek
  guarda lo SPAN. Non è inventariato continuo: è un campione dipendente
  dal churn DHCP.

Esempio:

```json
{"assigned_addr":"192.168.2.94","client_addr":"192.168.2.94","domain":"fritz.box","duration":0.317,"host_name":"ROMO-A3021K","lease_time":864000.0,"mac":"0c:9a:e6:b4:d6:e8","msg_types":["DISCOVER","DISCOVER","OFFER","REQUEST","REQUEST","ACK"],"requested_addr":"192.168.2.94","server_addr":"192.168.1.1","ts":1784815950.362196,"uids":["CEHTKl4X3EYI53OqO9","C0l32ycgt5ymSWbl4"]}
```

### 5. Vendor class identifier (option 60)?

**No** nei campi loggati (`rows_with_vendorish=0`).

Per fingerprint DHCP “classico” (opt 55+60) serve policy/package aggiuntivo;
**JA4D** (stesso pacchetto FoxIO) è la strada più allineata al pezzo JA4.

**Ingest attuale:** `dhcp.log` **non** è letto dal collector — solo prune.
Hostname DHCP arriva indiretto via Fritz (`name_proposals` / source dhcp|fritz).

---

## VERIFICA 3 — segnali già disponibili (mappa)

Per un asset, oggi:

| # | Segnale | Dove | Note |
|---|---|---|---|
| 1 | OUI / vendor | `interfaces.oui_vendor`, `oui_vendors`, `identity.vendor*` | Affidabile se MAC non privacy |
| 2 | Hostname multi-source | `name_proposals` (mdns, dns, fritz, ssdp, oui, ai, …) | Ranking in `asset_identity` |
| 3 | Categoria / device_class | `assets.category`, `fingerprint_facts` (`device_class`, `model`, `ssdp_type`) | Dopo adopt o classifier |
| 4 | OS | `fingerprint_facts` kind=`os` (nmap); `assets.os_guess` solo post-adopt | Opt-out fragile |
| 5 | Porte aperte / banner | `endpoints` + `services` (nmap) | Attivo, non passivo |
| 6 | Destinazioni + contesto AI | `habits.destinations` ← `flow_observations` + `ip_intel` | Pubbliche; conf/source |
| 7 | Porte contattate | `habits.ports` (dst_port aggregati) | Passivo SPAN |
| 8 | Volume / direzione | `habits.totals`, `bytes_in/out`, `direction_sample_ratio` | |
| 9 | Pattern orario | `habits.hours[0..23]` | UTC + label TZ |
| 10 | Coverage SPAN | `habits.coverage` | Topologia, non “ho visto traffic” |
| 11 | Chassisenza / chassis | `presence_state`, chassis members, media eth/wifi | |
| 12 | SNI / nomi remoti | `ip_intel` (dns\|ssl) | Destinazione, non client FP |
| 13 | TLS server cert | `tls_certificates` / evidence scan | Non JA client |
| 14 | `ssl_history` (Zeek) | solo su disco `ssl.log` | **Non ingerito** |
| 15 | DHCP host_name/mac | `dhcp.log` su disco | **Non ingerito**; no opt55/60 |
| 16 | JA3/JA4 | — | **Assente** |
| 17 | HTTP User-Agent client | — | `http.log` pruned, non ingerito |

API utili: `GET /api/assets/{id}`, `/identity`, `/habits`.

---

## PROPOSTA (su carta)

### 7. Fingerprint bundle (compatto per prompt)

Obiettivo: ≤ ~1.5–2k token, solo tecnici, **zero** PII domestica.

```json
{
  "schema": "fp_bundle/v0",
  "signals": {
    "link": { "media": ["wifi"|"eth"], "oui_vendor": "Amazon Technologies Inc.", "oui_reliable": true },
    "stack_tls": {
      "ja4_top": [{"h": "t13d…", "n": 120}, …],
      "ja4_n": 3,
      "ssl_history_top": [{"h": "CsxknGIi", "n": 40}]
    },
    "dhcp": { "ja4d": "…", "host_name_raw": null },
    "open_ports": [{"p": 443, "prod": "…"}],
    "contacted_ports": [{"p": 443, "bytes": 1.2e7}, {"p": 853, "bytes": 9e4}],
    "destinations": [
      {"cat": "iot", "what": "Amazon Minerva IoT", "conf": 0.75, "share": 0.41},
      {"cat": "cdn", "what": "CloudFront", "conf": 0.4, "share": 0.12}
    ],
    "when": { "peak_hours_local": [7, 8, 19, 20], "bytes_7d": 5.2e8 },
    "facts": { "device_class": "speaker", "os": null, "coverage": "parziale" }
  },
  "cluster": { "ja4_key": "t13d…", "siblings_known": 2, "sibling_labels": ["kind:echo"] }
}
```

Regole di riduzioni: top-K destinazioni (max 8), top-3 JA4, top-5 porte,
niente IP, niente MAC grezzo (solo OUI vendor), niente hostname LAN.

### 8. Clustering JA4 (anche senza sapere “cosa è”)

1. Ingest: per ogni `ssl` con `ja4`, lega `id.orig_h` → asset_id (stesso
   gate temporale dei flow).
2. Tabella `tls_client_fp(asset_id, ja4, first_seen, last_seen, hits)`.
3. Cluster = stesso `ja4` (eventualmente + stesso OUI vendor).
4. Se un membro ha `device_class`/`name` adottato con conf alta →
   **ipotesi soft** sugli altri (`fingerprint_facts` source=`ja4_cluster`,
   conf bassa 0.35–0.55) — mai overwrite di `manual` / nomi umani.
5. UI: “stesso stack TLS di X (non identificato)” finché non c’è adopt.

Senza JA4, un clustering su `ssl_history` è possibile ma **debole**
(pochi bucket, molti IP per bucket) — solo sperimentale, non SoT.

### 9. Privacy (vincolo duro per il prompt)

| Mai nel prompt | Ok |
|---|---|
| Hostname interni / mDNS / Fritz | OUI vendor string |
| Nomi dati da te (“Echo Cucina”) | `device_class` / category slug |
| IP privati / MAC | JA4/JA3 hash, porte, categorie destinazione |
| Path topologia casa | Coverage label astratta |

Le destinazioni entrano solo come `dst_context` / `dst_category` già
classificati (pubblici), non come FQDN lunghi se evitabili.

---

## Sintesi gate FASE B

| Gate | Stato |
|---|---|
| JA3/JA4 in `ssl.log` | ❌ assente — **bloccante** per fingerprint TLS |
| Package FoxIO JA4+ | non installato; percorso chiaro (Dockerfile Zeek + `@load`) |
| DHCP opt55/60 | ❌ assenti; hostname sì; JA4D candidato |
| Segnali passivi già in DB | ✅ habits + ip_intel + OUI + facts (parziale) |
| Ingest ssl_history / dhcp / ja4 | ❌ non esiste |

**Prossimo passo (solo dopo GO esplicito):** spike FASE B —
immagine Zeek con `zeek/foxio/ja4`, misura 24h di fill-rate `ja4`,
poi disegno ingest + bundle. Nessun retry AI / nessun deploy in questa fase.

---

## 10. Ricognizione fonti esterne (sola lettura)

### 10.1 FoxIO JA4+ Database ([ja4db.com](https://ja4db.com/))

| Voce | Stato |
|---|---|
| Endpoint/dump | Docs: `GET /api/download/` → JSON di fingerprint sets ([docs.ja4db.com](https://docs.ja4db.com/ja4+-database/usage/download-the-database)). Accesso tipicamente account/API key (docs pubbliche; download live non verificato qui — 403 senza auth). Sul repo: sample `ja4plus-mapping.csv` (poche app note). |
| Formato | JSON fingerprint sets; CSV sample application↔JA4 |
| Licenza | **JA4 TLS (client)**: BSD 3-Clause. **JA4+** (JA4S/H/L/T/D/…): **FoxIO License 1.1** — uso interno/accademico OK; **vietata monetizzazione** senza OEM. Uso domestico/interno LAN Observatory = non-commercial purpose (consentito). |
| Offline | Previsto via download dump; da confermare auth + refresh periodico |

**Vale la pena?** **Sì, in coda a JA4 live** — come *lookup opzionale* (“questo hash è tipico di Chromium / Python requests”), non come SoT. Priorità bassa rispetto al clustering interno. Non bloccare FASE B sul DB commerciale.

### 10.2 abuse.ch SSLBL — JA3 blacklist

| Voce | Stato |
|---|---|
| Endpoint | `https://sslbl.abuse.ch/blacklist/ja3_fingerprints.csv` (CSV pubblico, refresh ≤ ogni 5 min) |
| Formato | `ja3_md5,Firstseen,Lastseen,Listingreason` |
| Licenza / ToS | Gratis; vendor OK anche commerciale (ToS abuse.ch) |
| Caveat ufficiale | Hash da malware PCAP **non** testati su traffico buono → **FP possibili** |

**Vale la pena?** **Sì, come lista di ESCLUSIONE / alert**, non identificazione. Match → finding `tls_client_fp_sslbl` (severity), non “è un Echo”. Utile solo dopo che abbiamo JA3 **oppure** se restiamo su JA3 legacy; con solo JA4 serve feed JA4 (oggi SSLBL è JA3-centrico). Priorità: bassa finché non c’è fingerprint client ingerito.

### 10.3 Fingerbank (API)

| Voce | Stato |
|---|---|
| Input | `dhcp_fingerprint` (opt 55: `1,3,6,15,…`), `dhcp_vendor` (opt 60), `mac`, `user_agents[]` (max 5), UPnP UA, … (`/api/v2/combinations/interrogate`) |
| Output | device match + **score 0–100** |
| Tier gratis | Community: ~**600 req/ora**; rate limit globale **250/min** (anche premium) |
| Offline DB | Endpoint static download **solo con licensing** a pagamento |

**Vale la pena?** **Non ora.** Dipende da opt 55/60 che **non logghiamo**. Dopo JA4D / DHCP fingerprint: rivalutare come *secondo parere* su device sconosciuti (poche query/giorno). Privacy: inviare MAC/UA a terzi — solo opt-in esplicito.

### 10.4 Raccolte GitHub JA3/JA4 “IoT”

| Fonte | Cosa offre | Qualità / rischio |
|---|---|---|
| FoxIO `ja4plus-mapping.csv` | Sample ufficiale piccolo | Affidabile ma scarsa copertura |
| Huginn-Muninn | Dump enormi DHCP/MAC/device (CSV/JSON/SQLite) | Ottimo per **opt55/60** e OUI esteso; TLS JA3/JA4 ancora thin |
| leetha / aggregatori | Meta-DB multi-source | Comodo ma licenze miste + manutenzione; overkill per casa |
| Repo JA3 IoT sparsi | Liste ad hoc | Qualità variabile, stale, overlap malware/browser |

**Vale la pena?** **Huginn-Muninn DHCP**: sì *dopo* che logghiamo opt55/60 (o JA4D). Liste JA3 IoT random: **no** come SoT. Preferire clustering interno + (poi) ja4db ufficiale.

### Riepilogo fonti

| Fonte | Integrare? | Perché |
|---|---|---|
| FoxIO ja4db | Più tardi (lookup) | Licenza OK uso interno; completa il JA4 live |
| SSLBL JA3 | Sì come denylist | Barato, chiaro, non identifica device |
| Fingerbank | No finché no opt55 | API cloud + privacy; input che non abbiamo |
| GitHub IoT JA3 | No SoT | Rumore; Huginn utile solo lato DHCP |

---

## 11. Clustering interno (funziona anche senza DB esterni)

### Stato numerico OGGI (senza JA4)

| Metrica | Valore live 2026-07-23 |
|---|---|
| JA3/JA4 distinti | **0** (non in `ssl.log`) |
| Proxy `ssl_history` distinti (LAN) | **31** |
| Client LAN con history | **56** |
| Cluster con ≥2 membri (primary history) | **5** |
| Top cluster | `CsxknGIi`→17 · `CsxkrnXGYIi`→16 · `CsiI`→15 |

Conclusione: `ssl_history` **collassa troppo** (tre bucket tengono ~48 client). Utile solo come smoke test di UI clustering; **non** per propagare identità. Il clustering serio parte da **JA4** (FASE B).

### Modello dati (proposta)

```
tls_client_fp
  asset_id, fp_kind ('ja4'|'ja3'|'ssl_history'),
  fp_value, hits, first_seen, last_seen, is_primary

fp_cluster_hypothesis   (come name_proposals / ip_intel manual)
  cluster_key (= fp_kind:fp_value),
  suggested_device_class | suggested_label_slug,
  source ('user_adopt'|'ja4db'|'sslbl'),
  confidence, created_by, created_at
  — mai scrive assets.name umano; solo class/slug tecnico
```

Priorità: ipotesi `user_adopt` su cluster **non** sovrascrive `context_source=manual` / nomi adottati; conf ≤ 0.55 finché non c’è secondo segnale (OUI+dest).

### Vista UI — «Stesso stack»

```
Stack TLS  ja4=t13d1516h2_…
  ● Echo Sala          (adottato · tu)     → ancora
  ○ 192.168.x.x        (ipotesi 0.45)      [Adotta class] [Ignora]
  ○ 192.168.y.y        (sconosciuto)
  3 device · stesso ClientHello
```

Flusso:
1. Utente apre un device → sezione **Stack / twin**.
2. Vede gli altri asset con stesso `ja4` primario (e opz. stesso OUI).
3. «Propaga class a tutti i sconosciuti del gruppo» → scrive
   `fingerprint_facts` source=`ja4_cluster` (come adopt soft).
4. SSLBL match → badge rosso sul cluster, non sul nome.

Privacy UI: niente «Echo Cucina» nel prompt AI; in UI locale i nomi
restano (sono già in Inventario). Propagazione = solo `device_class`
tecnico.

### Ordine di implementazione suggerito

1. FASE B: Zeek+JA4 → ingest `tls_client_fp`
2. Vista cluster + propagate (senza DB esterni)
3. SSLBL denylist (se anche JA3, o feed JA4 se disponibile)
4. Lookup ja4db offline (opzionale)
5. Fingerbank solo se DHCP fingerprint reale
