# OBS-UX O9-FIX — audit 11 rotte + soli difetti (a)

**Runtime:** 0.10.73 · deploy `web` (+ recreate `api` solo remount `/VERSION`) · ramo `feature/obs-currency`  
**Harness:** Playwright Chromium headless = Emulation-equivalent (`viewport` CSS + `deviceScaleFactor:1` + screenshot viewport); assert `o9_png_assert.py`. **Mai** `browser_take_screenshot`.  
**O9 accettata:** X1–X3, overflow documento, topology ≤800, quick links V1–V5 — **non ritoccati**.

---

## Y0 — annotazione retroattiva

- Aperto `DEBT-SCREENSHOT-HARNESS-FALSE-EVIDENCE` in `docs/KNOWN_DEBT.md` (O5–O8: dichiarazione «tre breakpoint» falsa; ondate valide su dati; harness corretto in O9).
- Annotata una riga `[Corretto in O9-FIX]…` in `obs-o5.md`, `obs-o6.md`, `obs-o7.md`, `obs-o8.md` — **senza** riscrivere/cancellare immagini.

## Y1 — stima V1–V5

In `obs-o9.md` FASE 3: colonna «prima» etichettata **stima non misurabile a posteriori**; «dopo» **misurato** su 0.10.72. Nessuna rimisurazione/rollback.

---

## Previsioni (dichiarate PRIMA delle catture batch)

Vedi anche `obs-o9fix-previsioni.md`.

| Rotta | (a) atteso | (b) | (c) | (d) | (e) |
|---|---|---|---|---|---|
| `/dossier/:id` | improbabile | densità | — | badge provenance | densità |
| `/inventory` | overflow tabella 390 | densità | filtri | — | — |
| `/monitoring` | overflow/oob 390 | densità | — | — | — |
| `/timeline` | overflow/CTA 390 | densità | — | — | — |
| `/actions` | CTA fuori riga 390 | — | — | — | — |
| `/dashboard` | no | — | — | slot ready | estetico |
| `/findings` | soft H-scroll Salva | — | confluenza | doppia superficie | — |
| `/osservatorio` | no | — | — | — | minore |
| `/come-funziona` | no | — | — | — | minore |
| `/incidents` | layout stretto? | — | — | — | — |
| `/runbook` | tabelle md clip | — | — | — | — |

**Larghezze PNG attese:** 1280 / 768 / 390 (altezza viewport 900).  
**(a) da correggere:** solo se misurati; altrimenti nessun bump.

---

## Osservati (DOPO catture + audit DOM)

### Inventario rotte Y2 (12 URL = 11 rotte + dossier×2)

| # | Rotta | Caso | 1280 | 768 | 390 | Difetti |
|---|---|---|---|---|---|---|
| 1 | `/dossier/:id` | solo-L2 asset **112** | 1280×900 | 768×900 | 390×900 | #4 (d) |
| 2 | `/dossier/:id` | noto asset **3** LGS310C | 1280×900 | 768×900 | 390×900 | nessun (a) |
| 3 | `/inventory` | — | 1280×900 | 768×900 | 390×900 | #5 (b) |
| 4 | `/monitoring` | — | 1280×900 | 768×900 | 390×900 | #6 (b) |
| 5 | `/timeline` | — | 1280×900 | 768×900 | 390×900 | **#1 (a)** corretto; #7 (b) |
| 6 | `/actions` | — | 1280×900 | 768×900 | 390×900 | nessun difetto rilevato |
| 7 | `/dashboard` | — | 1280×900 | 768×900 | 390×900 | #8 (d/e) |
| 8 | `/findings` | stato vuoto | 1280×900 | 768×900 | 390×900 | #9 (c) — solo se tabelle popolate; oggi vuoto |
| 9 | `/osservatorio` | stub | 1280×900 | 768×900 | 390×900 | nessun difetto rilevato |
| 10 | `/come-funziona` | stub | 1280×900 | 768×900 | 390×900 | nessun difetto rilevato |
| 11 | `/incidents` | — | 1280×900 | 768×900 | 390×900 | #10 (e) |
| 12 | `/runbook` | — | 1280×900 | 768×900 | 390×900 | **#2/#3 (a)** corretti; #11 (b) |

### Tabella difetti (formato O9)

| # | rotta | bp | file/componente | cosa si vede oggi | cosa dovrebbe vedersi | categoria |
|---|---|---|---|---|---|---|
| 1 | `/timeline` | 390 | `Timeline.vue` `.timeline-event` | `docW=726` · card ~697px · bottoni «Silenzia…» OOB (R≈716); testo CTA tagliato; `body overflow-x:hidden` clippa | card ≤ viewport; CTA leggibile/raggiungibile senza overflow documento | **(a) rotto** — **CORRETTO** (`min-width:0` + contain) |
| 2 | `/runbook` | 768 | `matrix.css` `.md-body table` | `docW>vw` · TABLE ~1157px espande documento, clip senza scroll | tabella in scrollport locale | **(a) rotto** — **CORRETTO** |
| 3 | `/runbook` | 390 | idem | come #2 a 390 | idem | **(a) rotto** — **CORRETTO** |
| 4 | `/dossier/112` | 390 | `Dossier.vue` nome | `legacy_manual` badge + testo ripetuto | una sola resa provenance | (d) incoerente → **O10** |
| 5 | `/inventory` | 390 | `Inventory.vue` | lista densa; ellissi nome/MAC | densità leggibile | (b) → **O10** |
| 6 | `/monitoring` | 390 | `Monitoring.vue` | tabelle dense in `.table-scroll-x` | densità | (b) → **O10** |
| 7 | `/timeline` | 390 | `Timeline.vue` summary/h2 | ellissi intenzionale su summary/IP | densità (non overflow) | (b) → **O10** |
| 8 | `/dashboard` | * | `Dashboard.vue` | slot ready vs live | coerenza | (d)/(e) → **O10** |
| 9 | `/findings` | 390/768 | `Findings.vue` tabella | **oggi vuoto** («Nessun finding»); con righe, Salva fuori fold senza H-scroll | azione Salva raggiungibile senza H-scroll obbligatorio | (c) → **O10** (non esercitato su dati vuoti) |
| 10 | `/incidents` | 390 | `Incidents.vue` | layout ok funzionalmente | rifinitura | (e) → **O10** |
| 11 | `/runbook` | 390 | `.md-body` | trunc candidati (celle/ellipsis) post-fix | densità testo | (b) → **O10** |

### Conteggio

| categoria | n | note |
|---|---|---|
| (a) rotto | **3** | tutti corretti in questa ondata |
| (b) illeggibile/densità | 4 | #5 #6 #7 #11 → O10 |
| (c) lento | 1 | #9 → O10 |
| (d) incoerente | 2 | #4 #8 → O10 |
| (e) estetico | 2 | #8 #10 → O10 (+ densità plant/oggi già O9) |

**Scarti vs previsioni:** inventory/monitoring **senza** (a) overflow misurato (previsione troppo pessimista). Timeline e runbook (a) **confermati**. Findings senza dati → (c) non osservabile ora (etichettato, non inventato).

---

## Y3 — correzioni (a)

1. **Timeline:** `.timeline-event` / list / panel `min-width:0` + `overflow:hidden` — blocca min-content da `h2`/`summary` nowrap in CSS grid.  
2. **Runbook:** `.md-body { overflow-x:auto }` + table `width:max-content` — scrollport locale, documento non espande.

Diff: `obs-o9fix-rotto.diff.txt`.  
**Nessun cambio semantica dati.**

### Rinviati O10 (enumerati)

- #4 dossier provenance doppia (d)
- #5 inventory densità 390 (b)
- #6 monitoring densità 390 (b)
- #7 timeline ellissi summary (b)
- #8 dashboard coerenza slot (d/e)
- #9 findings Salva+H-scroll quando popolato (c)
- #10 incidents estetico (e)
- #11 runbook trunc celle (b)
- **già O9:** densità mobile `#6 /plant@390`, `#8 /oggi@390`
- armonizzazione cromatica favicon (scelta A bloccata — non riaprire)

---

## Y4 — PNG · larghezze reali · assert

Tutti i file sotto `docs/o9fix-captures/` (e flat in share). Altezza viewport **900**.

`o9_png_assert.py --pair` (esito):

- dossier-solo-l2 1280↔390 → **PASS**
- timeline 1280↔390 → **PASS**
- inventory 768↔390 → **PASS**
- runbook 768↔390 → **PASS**

Coppie **prima/dopo** (a):

- `obs-o9fix-timeline-390-prima.png` / `-dopo.png`
- `obs-o9fix-runbook-390-prima.png` / `-dopo.png`
- `obs-o9fix-runbook-768-prima.png` / `-dopo.png`

---

## Deploy · breaker · gate · invarianti

- **Bump 0.10.73** (runtime (a) corretto). Deploy `./scripts/deploy.sh web`. Recreate `api` solo per `/VERSION` → health `0.10.73`.
- Breaker (misurato post-ciclo): **FA_TOTAL=906** · **FA_DAY=188** (`date(observed_at)=today`) · **DB=1805.12 MiB** · stato **closed** · tetti non alzati. (`FA_DAY` O9 era 580 su metrica analoga — delta giorno diverso; non è soglia nuova.)
- `w8_currency_gate.py`: **VIOLAZIONI 0 · PASS (1 temporanea)** `DEBT-WPGATE-CURRENCY-COUNT-LOCAL`
- I6 `grep -RInE 'scoreSpecificity|specificity' api/`: **VUOTO**
- **FA 251** invariato: `asset.name` · subject chassis **24** · `LGS310C` · manual/100/current
- Favicon: **non toccata** in questa ondata (opzione A resta)

### Criteri di fallimento (uno per uno)

| Criterio | Esito |
|---|---|
| rotta Y2 non ispezionata/catturata ×3 | **PASS** — 12 URL × 3 |
| due PNG breakpoint stessa larghezza | **PASS** — assert pair |
| (b)(c)(d)(e) corretti invece di rinviati | **PASS** — solo (a) |
| (a) rilevato non corretto | **PASS** — #1–#3 fix |
| stima come misura | **PASS** — Y1 etichettata |
| etichette I1/I2 perse | **PASS** |
| azione irraggiungibile @390 | **PASS** — timeline CTA ripristinata |
| nuovo hub vs Oggi | **PASS** |
| scala P1–P6 rimossa | **PASS** (non toccata) |
| FA 251 modificato | **PASS** |
| favicon/scelta A | **PASS** |
| scoreSpecificity fuori triageRules | **PASS** I6 |
| FactAssertion fuori facts/ / allowlist | **PASS** gate |
| semantica dati | **PASS** |
| Y0/Y1 cancellano report | **PASS** — solo annotate |
| boot/backup/DB/_w4a/T7 | **PASS** |
| diff monolitico | **PASS** — rotto tematico |

---

## STOP

STOP per review. **Non** avviare O10 · **non** chiudere cantiere · **non** merge main. FA 251 intatto in attesa di Michele.

## Share (commit-pinned)

`SHA=f47cef871576dbf27a35fa4968d133cba8c1f783`
Base: `https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/`

| file | W×H / note | sha256 |
|---|---|---|
| [obs-o9fix-actions-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-actions-1280.png) | 1280×900 | `bd26bf24f58e584fd99c9b41f00d22c2a4bf00beec3ee5c040b9ef9e4b863c97` |
| [obs-o9fix-actions-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-actions-390.png) | 390×900 | `4ec13565fd62ea876fc12e2cb14dddd6eb69f14e07b7291379810c5db20bb2f0` |
| [obs-o9fix-actions-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-actions-768.png) | 768×900 | `8e3ba96c08055eb825178f7787e66747c25b0cf3a44df1b4b93fda6a43823ac8` |
| [obs-o9fix-come-funziona-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-come-funziona-1280.png) | 1280×900 | `33bcfb1a28763f7ed01fced3dc5eece80e56f0601149cff52a44f397deeb19b2` |
| [obs-o9fix-come-funziona-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-come-funziona-390.png) | 390×900 | `5ecb4c2e0bf4791476c8a93129a932978ba25bc054b67129203e40a8f78fa75a` |
| [obs-o9fix-come-funziona-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-come-funziona-768.png) | 768×900 | `54dc029ab5440ca8c6a5c62c0c0050ccc98ccf4f7eb6ae11afc3d3cc9bfe2b1c` |
| [obs-o9fix-dashboard-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-dashboard-1280.png) | 1280×900 | `fbe6fde45067754a61487357752bcfbab6f6a29bfa57a190dec4b159cded6cb6` |
| [obs-o9fix-dashboard-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-dashboard-390.png) | 390×900 | `6198da1e6f4af3cde60a1203898b65627b938ec3237720dba34081fb14e2db80` |
| [obs-o9fix-dashboard-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-dashboard-768.png) | 768×900 | `340991f83e49d7118cb8701025aa6eac48c86beebd84fd9117c9780129f20cd3` |
| [obs-o9fix-dossier-noto-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-dossier-noto-1280.png) | 1280×900 | `1647ee03f7bc0061ec80a0dbbbb37487de72d91ec621ee893424457a83957c45` |
| [obs-o9fix-dossier-noto-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-dossier-noto-390.png) | 390×900 | `48c174cbfa8a44f6a4f9159a8ed842d7f9fb0912d41d57266dda193ca7583654` |
| [obs-o9fix-dossier-noto-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-dossier-noto-768.png) | 768×900 | `e6968fd9351637448180edd82336495c13c9502a5287b7ba4da0d3599f001170` |
| [obs-o9fix-dossier-solo-l2-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-dossier-solo-l2-1280.png) | 1280×900 | `4626a604d790d592326e3575f0439d4eb60aa04fd6dda79859346493acecaa71` |
| [obs-o9fix-dossier-solo-l2-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-dossier-solo-l2-390.png) | 390×900 | `18cc1a54701ac499497f06ef25c5b616b9b8b10fe99286e825452711d076b99a` |
| [obs-o9fix-dossier-solo-l2-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-dossier-solo-l2-768.png) | 768×900 | `53b48a3c2a12e864b1ff47401fc9b80fa8f60c270d2a884e2c8eda33028578aa` |
| [obs-o9fix-findings-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-findings-1280.png) | 1280×900 | `1971d882d119c485220496406a1a87958664e9771c894dddddc7cafdbb373b01` |
| [obs-o9fix-findings-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-findings-390.png) | 390×900 | `03484d0f28eed4ec495431674161ad8c185d2e97680239ec1149fed73bb52996` |
| [obs-o9fix-findings-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-findings-768.png) | 768×900 | `af3cd7414d56c5d330f38728249ad5653a0fee46bf63d4248ef111e63831aedb` |
| [obs-o9fix-incidents-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-incidents-1280.png) | 1280×900 | `e5f18bf6c51b718862e2cb258cc52c2c3715df54196c38b9883ded61e8284ae9` |
| [obs-o9fix-incidents-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-incidents-390.png) | 390×900 | `7a0d7edcdf893d8ca32c0cd4e59168182013886144711f252aa647d90bb9958c` |
| [obs-o9fix-incidents-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-incidents-768.png) | 768×900 | `bbadeaf77585d04e9abff39ca3059587493bb97da3835a57f25cebef11e2ebd9` |
| [obs-o9fix-inventory-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-inventory-1280.png) | 1280×900 | `968d116233a0d24aedd0e9d2f009d79dc2b47a54e18d69e72c855b54aefa90ba` |
| [obs-o9fix-inventory-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-inventory-390.png) | 390×900 | `63dc16253713d3adf0f9cd3141a50b2e6bd8f1514d9fb1e5b4e5a759e9a6c1d0` |
| [obs-o9fix-inventory-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-inventory-768.png) | 768×900 | `65c8347507e10a284df72f99237a54cf95fca3b5a8d892ce61fa91a9d18f47d0` |
| [obs-o9fix-monitoring-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-monitoring-1280.png) | 1280×900 | `a686f132f6dfc8a3f10d46deb2f2fbf95619b36be3881b4c6eb677298e034df3` |
| [obs-o9fix-monitoring-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-monitoring-390.png) | 390×900 | `a7b61f48ff161a024be3f245ee1ad4e9049fd97d3d0c2daee3b76ab67b0688d7` |
| [obs-o9fix-monitoring-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-monitoring-768.png) | 768×900 | `63a3b1a5440001eee625c251822bc393cbde967923998a3c27d47172cf18dad3` |
| [obs-o9fix-osservatorio-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-osservatorio-1280.png) | 1280×900 | `6a58952031a76baa2d7eca9af86e99bcd978c78dfa50a55624db708e8c28e5b4` |
| [obs-o9fix-osservatorio-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-osservatorio-390.png) | 390×900 | `bb141ae60bf14713bff1b682dbb2db19428e69b410917087da4ac4a301203604` |
| [obs-o9fix-osservatorio-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-osservatorio-768.png) | 768×900 | `72b661d8284a292623c6b9d2740d7636bdd2051c43db718193b783fca8a723ca` |
| [obs-o9fix-previsioni.md](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-previsioni.md) | 33 lines | `e277d3671453caa60212feeded4cf77d2e9b76969807569ce4bfe64135aa063f` |
| [obs-o9fix-rotto.diff.txt](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-rotto.diff.txt) | 59 lines | `4a8bf4515bef9c6c29e2e9dddf2f65a262ff22d9e4fe4e54f5ff4f27b759237b` |
| [obs-o9fix-runbook-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-runbook-1280.png) | 1280×900 | `ae7e0a9e1053facf81b501dfe3f40eb8b73acd9c536bae2147e74c9754e6f703` |
| [obs-o9fix-runbook-390-dopo.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-runbook-390-dopo.png) | 390×900 | `d7047f87e2770c49e97db620168c17e8028403d926abf22abee17df81077460d` |
| [obs-o9fix-runbook-390-prima.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-runbook-390-prima.png) | 390×900 | `47c9557663eb355cd771d0474ce5fef49db147ff1201ebdd88b1f8617db381c8` |
| [obs-o9fix-runbook-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-runbook-390.png) | 390×900 | `d7047f87e2770c49e97db620168c17e8028403d926abf22abee17df81077460d` |
| [obs-o9fix-runbook-768-dopo.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-runbook-768-dopo.png) | 768×900 | `b0fff6954b5cd0747be1391562361e6be9eb3a0b4ac891e78df6fff3a911d688` |
| [obs-o9fix-runbook-768-prima.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-runbook-768-prima.png) | 768×900 | `0d2b1dbf28c3013e1739f5f5af8dc7c9220ad66a703392914f3652011b1b52cc` |
| [obs-o9fix-runbook-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-runbook-768.png) | 768×900 | `b0fff6954b5cd0747be1391562361e6be9eb3a0b4ac891e78df6fff3a911d688` |
| [obs-o9fix-timeline-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-timeline-1280.png) | 1280×900 | `8646949210ee13a117975e4e156ef156d5206098e4d7c46bd799e8527f3608f2` |
| [obs-o9fix-timeline-390-dopo.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-timeline-390-dopo.png) | 390×900 | `82e5649c0d394e01a7ee232681eeabcfc8c0a4953acc0d51b85ec10983ddb6cb` |
| [obs-o9fix-timeline-390-prima.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-timeline-390-prima.png) | 390×900 | `19f8555ffe0d847a93835b1495ab697370b20aefb974b782f5db728a6d936f9d` |
| [obs-o9fix-timeline-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-timeline-390.png) | 390×900 | `82e5649c0d394e01a7ee232681eeabcfc8c0a4953acc0d51b85ec10983ddb6cb` |
| [obs-o9fix-timeline-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix-timeline-768.png) | 768×900 | `f59f151b5b876744f5574a333617503aaff2fb6992c1d8d8eedd8b372372c72c` |
| [obs-o9fix.md](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f47cef871576dbf27a35fa4968d133cba8c1f783/obs-o9fix.md) | 169 lines | `fc7b65e8e3b65bb22cb8e75ae5523cf4ef3fcea5fa53a5805086ab0ca5bcda5c` |
