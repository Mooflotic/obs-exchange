<!-- BLOCK-ID: OBS-DESIGN-SPEC-025 -->

# LAN Observatory — specifica di design

Documento di riferimento per il restyle. Non è un prompt di esecuzione:
è la fonte di verità visiva e di interazione. I cantieri di
implementazione lo citano invece di ripetere le regole.

---

## 0. Vincoli

**Prima di tutto**: il bug Inventario (render poi crash) va risolto.
Non si ridisegna una vista rotta.

**Non toccare**: la logica dati (gate `resolve_asset_by_ip_at`, coverage,
attribuzione chassis-aware, `ip_intel`). Questo è un lavoro di
presentazione e interazione.

**Ordine dei lavori** in §9. Il restyle non si deploya in un colpo.

---

## 1. Direzione visiva

### Il problema del punto di partenza

Il tema Matrix (fosforo verde su nero, mono ovunque) ha due difetti:
il verde è *ambiente* invece che *accento*, e il mono impedisce la
gerarchia — quando tutto è mono, niente risalta.

La correzione non è "verde più spento su nero". Quella resta la stessa
famiglia. Serve cambiare la base.

### La metafora: strumento di misura

Il sistema osserva e misura. La sua parentela visiva sono gli strumenti
di laboratorio — oscilloscopi, analizzatori di spettro — non i terminali
di *Matrix*. Da lì derivano le scelte:

- **base blu-ardesia profonda**, non nera: superficie di chassis, non
  schermo di terminale
- **colore usato per misurare**, non per decorare
- **densità alta e precisa**: i numeri si confrontano incolonnati

### La scelta di rischio: la direzione come temperatura

La barra out/in usa una scala di temperatura: **out freddo, in caldo**.

Il caso d'uso che ha originato il behavioural è *"scaricano MB su un
IoT"* — cioè il traffico **in entrata** anomalo. Con questa scala, il
device che riceve molto **si scalda visivamente**: l'anomalia si vede
prima di leggerla.

È anche coerente con la scala di magnitudine stellare (blu caldo →
ambra → rosso), che è una convenzione scientifica reale e non una
decorazione.

---

## 2. Token

### Superfici

```
--bg-0        #0F1319   canvas pagina
--bg-1        #161B23   card, riga
--bg-2        #1D242E   elevato (popover, drawer)
--border      #262E3A   hairline
--border-2    #323C4A   divisore enfatizzato
```

Base blu-ardesia (hue ~215), non nera. La leggera dominante fredda è
ciò che la distingue da un terminale.

### Testo

```
--text-1      #E8EBF0   primario
--text-2      #98A2B3   secondario, etichette
--text-3      #667085   muted, hint, unità
```

Mai opacità sul testo: usare i livelli.

### Dati — scala di temperatura

```
--data-out    #6BC5DB   freddo · traffico in uscita
--data-in     #E0A048   caldo · traffico in entrata
--data-idle   #323C4A   neutro · barre senza valore
```

### Semantica

```
--ok          #4FB477   presente, completo, salvato
--attn        #D9A441   parziale, probabile, attenzione
--alert       #E06B52   problema, discordanza
--accent      #6BC5DB   selezione, focus, link
```

Un solo accento (coincide con `--data-out`). Le tinte pallide per i
badge si ottengono con la stessa hue al 12% di opacità su `--bg-1`.

### Tipografia

```
--font-sans   Inter, -apple-system, system-ui, sans-serif
--font-mono   "JetBrains Mono", ui-monospace, SFMono-Regular, monospace
```

**Regola ferrea**: mono **solo per i dati** — MAC, IP, byte, porte,
JA4, hostname tecnico, timestamp. Etichette, titoli, descrizioni,
messaggi: sans.

È la singola modifica che toglie il sapore da terminale.

Scala:

```
11px  caption, unità, hint
12px  metadato, etichetta di campo
13px  corpo denso (righe di tabella)
14px  corpo, titolo di sezione
18px  titolo pagina
22px  titolo device nel Dossier
```

Pesi: **400 e 500 soltanto**. Mai 600/700 — appesantiscono.

Sentence case ovunque. Mai Title Case, mai maiuscolo.

### Spaziature e forme

```
grid base 4px
--radius      6px    controlli, badge, righe
--radius-lg  10px    card, pannelli
```

Bordi sempre `0.5px solid var(--border)`. Nessuna ombra, nessun
gradiente, nessun glow.

---

## 3. Componenti primitivi

Costruire questi **prima** delle viste: tutte le pagine li useranno.

### 3.1 Riga densa

Altezza ~34px, tre zone: identificatore (flessibile, tronca a
middle-ellipsis), metrica (larghezza fissa), valore (allineato a destra,
mono).

Quando l'identificatore ha due livelli — nome leggibile e riferimento
tecnico — il nome va sopra in sans 13px `--text-1`, il tecnico sotto in
mono 11px `--text-3`.

Separatore: `border-bottom 0.5px var(--border)`. Mai card separate per
riga: sono liste, non oggetti.

### 3.2 Badge di stato

Testo 11px, padding 2px 8px, radius 20px, fondo = hue semantica al 12%,
testo = hue semantica piena. Mai fondo saturo.

```
presente        --ok
parziale        --attn
non rilevato    --text-3 su --bg-1
discordante     --alert
```

### 3.3 Barra direzione

Altezza 6px, radius 3px, due segmenti proporzionali:
`--data-out` a sinistra, `--data-in` a destra. Fondo `--data-idle`
quando la direzione non è disponibile.

Nessuna etichetta sulla barra. Una legenda **una volta** in cima alla
sezione: `out = verso destinazione · in = dalla destinazione`.

Se `direction_sample_ratio < 0.20`: niente barra, solo volume e la nota
"direzione ancora scarsa".

### 3.4 Sparkline oraria

24 barre, altezza max 30px, gap 2px. Barre neutre `--border-2`; le tre
ore di picco prendono `--accent`. Asse sotto: 0 / 6 / 12 / 18 / 23 in
mono 10px. Ore locali (Europe/Rome), con footnote.

Tooltip per cella: `21:00 · 12 MB · 34 oss.`

### 3.5 Lista candidati con confidenza

Usata per: OS multi-match, proposte nome, contesto AI.

```
Sistema operativo                        rilevato 18:42 · 34s
Tre corrispondenze. Scegli quella giusta, oppure lascia la prima.

┌────────────────────────────────────────────────────────┐
│ ◉  Linux 4.15 – 5.19                    ▓▓▓▓▓▓▓▓▓░  95 │ ← bordo accento
│    kernel generico                                      │
└────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────┐
│ ○  OpenWrt 21.02                        ▓▓▓▓▓▓▓▓▓░  92 │
│    Linux 5.4 · firmware router                          │
└────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────┐
│ ○  MikroTik RouterOS 7.2 – 7.5          ▓▓▓▓▓▓▓▓░░  88 │
│    Linux 5.6.3                                          │
└────────────────────────────────────────────────────────┘
Porte usate 22 · 443 · nessuna delle tre? scrivila   ✓ salvato
```

Ogni riga: indicatore di selezione, nome, sottotitolo, barra di
confidenza (74px) + valore numerico mono. Il primo candidato è
**preselezionato**; selezionandone un altro la scelta diventa
`source=manual`.

Le accuracy vicine (95 / 92 / 88) sono il caso in cui la scelta umana
conta di più. La riga sotto mostra **su cosa** si fonda l'ipotesi — le
porte da cui nmap ha dedotto.

In fondo: campo libero per "nessuna di queste".


### 3.6 Indicatore di salvataggio

Testo 11px accanto al campo. `Salvataggio…` in `--text-3` durante,
`✓ salvato` in `--ok` per ~2s, poi sfuma. In errore: messaggio esplicito
in `--alert` e **il valore non si perde**.

---

## 4. Pattern trasversali

Questi valgono ovunque. Devono essere lo stesso identico gesto visivo
in tutte le viste — si impara una volta.

### 4.1 Proposta / scelta umana

**La macchina propone classificata per confidenza, l'umano sceglie, la
scelta umana diventa la fonte più autorevole.**

Vale per: contesto degli IP, proposte nome, OS multi-match, uso probabile
del device.

Gerarchia delle fonti:

```
umano (manual)     — sempre vincente, mai sovrascritto
ai (fingerprint)   — sintetizza più segnali
dhcp parlante      0.95
fritz              0.90
oui                0.70
```

### 4.2 Fatto vs inferenza

I fatti osservati e le inferenze **non si mescolano visivamente**.

- fatto: riga normale
- inferenza: bordo accento a sinistra, etichetta che dichiara la fonte
  e le evidenze — `Uso probabile · inferito dalle destinazioni`
- ipotesi debole (confidenza 0.3–0.7): prefisso `probabile:` in `--attn`
- ignoto: **dichiarato**, mai nascosto — `OS: non rilevato`,
  `nessun hostname annunciato`

### 4.3 Divergenza

Quando una fonte automatica dissente da una scelta umana, il sistema
**lo dice** invece di tacere:

> la scansione di oggi propone OpenWrt 21.02, la tua scelta resta
> ADM 4.x (ASUSTOR)

Stesso principio dell'osservabilità sul MAC mismatch.

### 4.4 Auto-save

Nessun bottone Salva.

| elemento | quando salva |
|---|---|
| note (textarea) | debounce 800ms + blur + chiusura pannello |
| rename | **solo** blur o Invio — mai debounce |
| toggle | immediato |

Il rename mai in debounce: un nome parziale non deve finire nel DB né
nelle proposte. Dopo il rename, `Annulla` disponibile ~5s.

Il debounce protegge anche dal write-lock SQLite.

### 4.5 Stati vuoti

Un vuoto è un'informazione, non un'assenza. Distinguere sempre:

```
silenzio osservato      copertura completa, nessun flusso → il device tace
può esserci traffico    copertura parziale → non lo sappiamo
non sappiamo            copertura sconosciuta
campione sottile        pochi dati, mostrali comunque
```

Mai placeholder inventati. Mai giudizi ("dormiente" è vietato:
descrittivo, non valutativo).

---

## 5. Struttura di navigazione

```
RADAR                    non so cosa cerco — scoperta e approfondimento
  Oggi                   coda di triage · cosa richiede attenzione
  Osservatorio           radar del traffico · chi merita un'occhiata
  Dossier                il fascicolo del device

MAPPA                    so cosa cerco — consultazione mirata
  Inventario             griglia densa filtrabile
  Impianto               porte, patch, ruoli
  Topologia              il grafo
  Monitor                raggiungibilità
  Timeline               cronologia globale

SISTEMA                  in fondo alla sidebar
  Come funziona          assunzioni, calibrazione, cosa non fa ancora
  Azioni                 coda job (pannello, non pagina)
```

**Regola di divisione del lavoro**: le code si smaltiscono in **Oggi**
con azioni inline; i singoli casi si approfondiscono nel **Dossier**.

**Findings** confluisce nell'Osservatorio a calibrazione chiusa
(~5/8): "anomalie" e "chi merita un'occhiata" sono la stessa domanda.

Sotto 800px i gruppi restano invisibili (comportamento attuale,
accettato).

---

## 6. Dossier — `/dossier/:id`

La vista di riferimento. Le altre ne ereditano il linguaggio.

### Struttura

```
┌──────────────────────────────────────────────────────────┐
│ Robot Roborock  ✎  [presente]        [watch]  [azioni ▾] │
│ 64:90:c1:0a:3f:12 · 192.168.2.94 · wifi · vista dal 18lug│
│ 2 interfacce ▾                                           │
├──────────────────────────────────────────────────────────┤
│ chi sei · come sei connesso · cosa è cambiato · abitudini │ ← sticky
├──────────────────────────────────────────────────────────┤
│ Chi sei                                                   │
│ Identità osservata                                        │
│ ┌────────┐┌────────┐┌────────┐  griglia auto-fit 150px    │
│ │Vendor  ││Tipo    ││OS      │                            │
│ │Roborock││domotica││non ril.│                            │
│ └────────┘└────────┘└────────┘                            │
│ ▎Uso probabile · inferito dalle destinazioni              │
│ ▎Robot aspirapolvere che sincronizza mappe…               │
├──────────────────────────────────────────────────────────┤
│ Come sei connesso                                         │
│ [device]→[wifi 5GHz ch44]→[Repeater]→[p9 328C]→[Fritz]    │
│ Nota fisica — dove sta, come raggiungerlo…                │
├──────────────────────────────────────────────────────────┤
│ Cosa è cambiato                          ultimi 7 giorni  │
│ oggi 09:12  nuova destinazione · ultronsplus-eu           │
│ 21 lug      cambio IP · .2.88 → .2.94                     │
├──────────────────────────────────────────────────────────┤
│ Abitudini                          [copertura parziale]   │
│ out = verso destinazione · in = dalla destinazione        │
│ Destinazione            out/in        7 giorni            │
│ Tencent Cloud Object…  ▓▓▓▓▓▓▓▓░       47 MB              │
│  conf-eu…myqcloud.com                                     │
│ PETKIT · probabile     ▓▓░░░░░░░░      697 KB             │
│  api-eu.petkt.com                                         │
│ +5 destinazioni                                           │
│ ▁▁▂▃▁▁▂▄▃▂▃█▇▅▂▁▁▂▃▄▂▁▁▁    0  6  12  18  23              │
├──────────────────────────────────────────────────────────┤
│ Note — scrivi qui…                          ✓ salvato     │
└──────────────────────────────────────────────────────────┘
```

Proporzioni della riga destinazione: identificatore flessibile ·
barra 88px fissa · valore 76px allineato a destra.

### Regole specifiche

**Il nome vive sul chassis.** Un device fisico ha un nome solo. Le
interfacce hanno **etichette tecniche**, non nomi: `eth · 192.168.2.138 ·
p24 328C`. Rinominare dal Dossier scrive sul chassis.

**Multi-interfaccia**: aggregato di default nell'header, espandibile per
vedere le singole. I dati mostrati sono la somma; l'espansione permette
di vederli per interfaccia.

**Indice sticky** in alto, salta alle sezioni. Non nasconde niente.

**Ancore**: `/dossier/:id#abitudini` — l'Osservatorio ci porta
direttamente quando segnala un comportamento.

**Il percorso fisico è una catena**, letta da sinistra a destra, che
finisce sull'informazione operativa: la porta da staccare (cablato) o il
repeater (WiFi).

**Azioni occasionali** (OS scan, opt-out, proposte) nel menu `azioni ▾`.
Non occupano la pagina.

### OS scan

Su richiesta, inline: progresso nella sezione, risultati al loro posto,
nessuna navigazione. Durata reale 25-60s.

Al termine mostra **tutti i candidati** con accuracy (componente §3.5),
il primo preselezionato. Sotto: le porte usate per la deduzione — è
l'evidenza. Campo libero per "nessuna di queste".

Oggi il parser tiene un solo match e scarta gli altri in silenzio:
va cambiato.

---

## 7. Oggi — la coda di triage

La vista nuova più importante. Risponde a: *cosa richiede me, adesso*.

Una lista ordinata di item azionabili, ognuno con azione inline —
nessun cambio pagina per smaltire.

```
proposta nome      Amazon Air Quality Monitor        [adotta] [ignora]
                   da hostname dhcp · conf 0.92
device nuovo       68:13:F3:E7:D2:B2 · Amazon        [apri] [ignora]
                   nessun nome, visto 18 lug
monitor degradato  DVR Hikvision                     [silenzia] [apri]
                   3 flap nelle ultime 2h
```

**Criterio d'oro**: se la coda è vuota, la rete non ha bisogno di te
oggi. Quello è lo stato di successo — non un cruscotto pieno di numeri
da interpretare.

Ordinamento per tipo + età. Nessuno scoring finché i detector dormono.

Ogni riga porta al Dossier del soggetto con un click.

---

## 8. Proposta nome AI (Wave 1d)

L'AI sintetizza il fingerprint completo e propone un **nome tecnico**;
il nome umano resta all'utente.

**Input** (solo segnali tecnici e destinazioni pubbliche):
OUI · JA4 · DHCP vendor class + option 55 · hostname · destinazioni con
contesto · porte · pattern orario · direzione.

**Mai**: IP privati, hostname interni, nomi di stanza (rivelano la
disposizione di casa).

**Output**: proposta in `name_proposals` con `source='ai'`, che finisce
nella coda di **Oggi** insieme alle altre. Un solo posto dove smaltire
le proposte, qualunque sia la fonte.

**Con le evidenze**: `Amazon Echo Show 8 — da OUI Amazon 2023+, stack
Android/Fire OS, destinazioni Alexa API`.

**"non deducibile" è una risposta valida.**

**Policy** (già decisa):

- device **personali** (telefoni, tablet, computer, wearable): solo su
  richiesta esplicita. Mai batch, mai notturno. Default per
  `category` + override per-asset.
- device **non personali**: notturno, ma **solo se il profilo è
  cambiato** — hash del set dei nomi delle top destinazioni vs la notte
  prima. Uguale → skip, nessuna chiamata.

Da decidere: on-demand o batch sui device anonimi.

---

## 9. Ordine dei lavori

Il restyle non si deploya in un colpo. Un restyle a metà è peggio di un
Matrix coerente.

**1. Fix Inventario** — è rotto, viene prima di tutto.

**2. Token e tipografia** — un solo file: variabili colore + regola
mono/sans. Cambia tutto senza toccare un componente. Verificare vista
per vista che nulla si rompa.

**3. Componenti primitivi** (§3) — riga densa, badge, barra direzione,
sparkline, lista candidati, indicatore salvataggio. Sono le primitive
che tutte le viste useranno: farle bene una volta.

**4. Dossier** — è la vetrina, ed è dove il linguaggio si definisce.

**5. Inventario** — griglia densa filtrabile, ora che l'approfondimento
sta nel Dossier.

**6. Oggi** — la coda di triage. Dati già disponibili.

**7. Navigazione** — spostare Azioni e Findings quando le viste sono
stabili.

**8. Osservatorio** — quando la direzione ha ~7 giorni di dati
(~30 luglio), con soglie tarate sui dati reali.

---

## 10. Debiti noti da questo documento

- **Findings** resta in MAPPA finché la calibrazione non chiude; poi
  confluisce nell'Osservatorio.
- **Inventario** ha un tema dedicato (`--inv-*`) fuori dai token
  comuni — va allineato al punto 2, non prima.
- **Nomi per-asset esistenti** sui chassis multi-NIC: si consolidano
  sul chassis, ma **non si cancellano** dal DB (storico utile).

---

## 11. Guard sul refactoring

Il bug che ha rotto l'Inventario (`ReferenceError: catLabel is not
defined`, 0.10.11 → fix 0.10.15) è la firma di una classe intera: la
funzione è migrata in `AssetDecide.vue` durante l'estrazione dei
componenti, ma `Inventory.vue` continuava a chiamarla. La review di un
diff vede ciò che **cambia**, non ciò che resta **orfano**.

Con la quantità di estrazioni previste in §9 (componenti primitivi,
Dossier, Inventario), serve una rete automatica:

**ESLint con `no-undef`** attivo sul build — un simbolo non definito
fallisce la compilazione invece di smontare la vista a runtime. In
alternativa `vue-tsc` per il type-check completo, più severo e più
utile a lungo termine.

Da attivare **prima** del punto 3 (componenti primitivi), che è la fase
con più spostamenti di codice.

---

## 12. Presidio permanente della correntezza (W8)

**Principio.** La correntezza dei FATTI (nome, alias, IP eletto, mgmt IP,
presenza, FDB, link, OS, proposte) si legge da UN SOLO posto: il resolver in
`api/app/facts/`. Nessun altro punto di `api/` può interrogare `FactAssertion`
per decidere «qual è il valore adesso». L'evidenza si scrive, lo stato si
deriva (F-7): i consumatori leggono lo STATO derivato (`classify_asset`) o il
resolver, mai un calcolo di correntezza per conto proprio.

**Gate (versione realmente consegnata, W8-fix / W8-fix2).**
`scripts/w8_currency_gate.py` scansiona **`api/** · scripts/** · collector/****,
escludendo `api/app/facts/**` (la FONTE protetta) e i due file d'ondata
(`w8_currency_gate.py`, `w8_g8_equivalence.py`, che contengono le sentinelle come
dato). Usa **tre sentinelle**:
1. simbolo ORM `FactAssertion` (qualunque uso);
2. tabella grezza `fact_assertions` **dentro una chiamata SQL** (`text(`/`.execute(`/
   `.exec_driver_sql(`);
3. **COMBO**: fact-token (`FactAssertion|fact_assertions|fact_key`) + valore di stato
   **quotato** `'current'`.
**Fallisce** su ogni accesso non giustificato. L'allowlist è **per (file, snippet, N)**
con conteggio: N+1 occorrenze = violazione (atteso vs osservato in output). Esiste una
sezione **TEMPORANEA** `(file, snippet, N, debt)` con `debt` OBBLIGATORIO: una voce
senza debito è un errore di configurazione (exit 1); le temporanee sono stampate **in
testa** e l'esito riporta `PASS (con n eccezioni temporanee)`. Ha `--selftest`
(controllo negativo). Va eseguito, output completo, a ogni ondata **insieme a I6**.

**Criterio del ruling (W8-fix2).** `api/app/facts/**` è escluso perché è la fonte
protetta della correntezza. **Ogni altro consumatore — tooling di gate/diagnosi
compreso — si allowlista riga per riga** (come `admin.py`), MAI per path intero:
un'esclusione di file è più permissiva di un pattern generico, e i pattern generici
sono vietati.

**LIMITAZIONE DICHIARATA (R6): B1(i) è MITIGATO, non chiuso.** Una stringa SQL
costruita su **più righe** e concatenata prima dell'esecuzione non è catturata da
nessuna delle tre sentinelle. Non va dichiarato «chiuso» in alcun documento.

**Eccezioni giustificate (allowlist permanente, stato W8-fix2: 17).**
- api/: `models.py` (def ORM), `bootstrap.py` (import `create_all`), `admin.py`
  (`/facts/shadow-stats` COUNT; `/facts/conflicts` divergenze `state="historical"` I3).
- scripts/ (tooling read-only, riga per riga): `wp_gate.py` (import; COUNT totale) e
  `wp_diagnose.py` (import; COUNT totale; distribuzione di stato; campione display;
  enumerazione id per delta; get per id) — conteggi/diagnostica, **nessuna lettura del
  valore corrente**.

**Eccezione TEMPORANEA (1, con debito).** `wp_gate.py:103`
(`COUNT(FactAssertion WHERE state=="current")`) è una **seconda definizione di
«corrente»** nello strumento che certifica la produzione (il resolver applica
TTL/`_maybe_stale`/R-E; un `state=="current"` grezzo può divergere). Sanata TEMPORANEAMENTE
con `debt=DEBT-WPGATE-CURRENCY-COUNT-LOCAL`; risoluzione = helper di conteggio in
`api/app/facts/` (micro-ondata runtime successiva). Vietato dichiararla chiusa
allowlistandola in permanenza.

**Falsi positivi legittimi non presidiati qui (criterio dichiarato).**
- `ip_addresses.is_current` = **meccanismo di elezione** dell'IP eletto (F-15), non
  correntezza dei fatti (pre-condizione W3).
- Colonne di stato derivate di `Asset` (name/os_guess/presence_state): STATO derivato
  dall'unico derivatore (F-7).
- Evidenza grezza / oggetti di dominio (ObservationRaw, Event, ScanRun, SpeedTestResult,
  Finding, Suggestion, Snapshot, ActionRequest): non sono fatti del registry.
- `resolver.history()`: codice **senza chiamanti**, nessun `?history=true`
  (`DEBT-HISTORY-PATH-UNWIRED`); l'API resta corrente per default perché lo storico non
  è esposto.

**Equivalenza (G8).** `scripts/w8_g8_equivalence.py` è **read-only sulla TRANSAZIONE
DB** (`db.rollback()` finale, nessun commit; il file È versionato). Confronta a writer
fermi la correntezza di `asset.name` (resolver vs presentazione vs endpoint) e di
`os.guess` (resolver vs colonna derivata `Asset.os_guess`, store diverso): `DIVERGE=0`
è la non-regressione. `--mutate-probe <id>` è il controllo negativo (deve produrre
`DIVERGE=1` e FAIL).
