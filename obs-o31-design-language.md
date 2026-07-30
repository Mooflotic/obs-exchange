# O31 — linguaggio «prima vista» (proposta, non applicata)

Documento di regole concrete per la sola rotta **Oggi**, ispirate a un’interfaccia
pulita, minimale, ad alta gerarchia. **Nessuna modifica prodotto in O31.**

Compatibile con principi già bloccati:

- progressive disclosure (dettaglio dietro summary/`title`, non davanti)
- segnale discreto per i sospetti (non banner gridati)
- fatti vs inferenze sempre distinguibili (`--ok` / `--inference*`, vocabolario FDB)

**Fuori scope:** matrice decisionale O15 (APPROFONDISCI / APPLICA / NON APPLICARE),
layout di altre rotte, branding Matrix (fase A, decisione separata).

---

## 1. Tipografia (pesi / dimensioni)

Usare stack già in `matrix.css` (`--font-sans`, Inter; mono solo per ID tecnici).

| Ruolo | Dimensione | Peso | Colore | Note |
|-------|------------|------|--------|------|
| Titolo pagina (`Oggi`) | ~1.5–1.75rem | 600 | `--text-1` | Un solo H1; letter-spacing leggermente negativo |
| Sottotitolo / help | ~0.95rem | 400 | `--text-2` | Max ~42rem; una frase; niente elenco nella help |
| Etichetta sezione (H2) | ~1.05–1.15rem | 500–600 | `--text-1` | Una per sezione; niente griglia di meta sotto |
| Etichetta chrome (quick/legend) | ~0.7rem | 500 | `--text-3` | Uppercase + tracking; secondaria |
| Corpo card | ~0.9–0.95rem | 400 | `--text-1` / `--text-2` | Numeri tecnici in mono |

Non alzare `--text-3` per corpo leggibile (debito contrasto già noto).

---

## 2. Spaziatura (`--space-1…4`)

- Tra titolo e primo contenuto operativo: almeno `--space-3` / `--space-4` (non comprimere).
- Tra sezioni di lavoro: `--space-4` o più; evitare stack di nav+legenda+indice senza aria.
- Dentro card: padding esistente; non aggiungere strip di meta sopra la piega.

---

## 3. Cosa stare sopra la piega (@1280, viewport ~900)

**Sì (ordine proposto):**

1. H1 `Oggi` + una riga di help orientata all’azione («coda di interventi aperti»).
2. Banner di stato solo se rilevante (errore, outage Fritz, partial) — assente se idle.
3. Chrome «N casi chiusi» **solo se N>0** (già O28).
4. **Prima sezione operativa** con almeno una card aperta (es. FDB / conflitti / prima coda non vuota).

**No (spostare sotto o chiudere di default su desktop):**

1. Legenda P1–P7 espansa (oggi aperta su `!narrowUi` — occupa piega senza dare lavoro).
2. Blocco «Domande rapide» + indice sezioni (orientamento utile, ma dopo il primo lavoro).
3. Qualsiasi elenco di ancore che ripete i titoli H2 già in pagina.

Regola: la prima viewport deve rispondere a «cosa devo fare adesso?», non a «come è organizzato il sistema?».

---

## 4. Progressive disclosure (allineamento)

- Legenda: `details` **chiuso** di default anche a 1280 (simmetrico al mobile), summary una riga.
- Domande rapide: sotto la prima sezione operativa, o in footer di pagina.
- Matrice O15: invariata; resta sul card quando eleggibile — non è chrome di pagina.

---

## 5. Varianti mockup locali O31 (C3)

| ID | Idea | File |
|----|------|------|
| `c3_v1_quiet` | Solo tipografia/spazio su header; legenda/quick restano | `obs-o31-c3_v1_quiet-fold-1280.png` |
| `c3_v2_workfirst` | Legenda forzata chiusa + ordine CSS (chrome dopo) | `obs-o31-c3_v2_workfirst-fold-1280.png` |

Confronto vs `obs-o31-c1-oggi-fold-1280.png` (produzione).

---

## 6. Domande per Michele (prima di un’eventuale D)

1. Preferisci **work-first** (legenda chiusa + quick sotto) o solo **quiet header** (tipografia)?
2. Il help di PageHeader deve restare descrittivo («coda unica…») o diventare imperativo («Apri il primo caso P1»)?
3. L’indice sezioni O18 resta obbligatorio in pagina o può vivere solo in nav laterale?
