# Session mint — autenticazione dell’harness di cattura

## Che cos’è

Il **session mint** è un file di sessione a vita breve che contiene il cookie di autenticazione Observatory (`obs_session`, e opzionalmente `obs_csrf`) già emesso dal runtime. L’harness di cattura screenshot (`scripts/o13dfix_capture.py`, procedura O9) lo legge e lo inietta nel browser headless.

Non è una password, non è un utente, non è un nuovo canale di login.

## Perché esiste

`ADMIN_PASSWORD` in `.env` è un **valore di seed** consumato al primo bootstrap. Dopo il bootstrap lo store autoritativo è il database: l’hash utente in DB può divergere dal valore in `.env`. In quel caso `POST /api/auth/login` con le chiavi `.env` fallisce (401), mentre una sessione già valida nel cookie continua a funzionare.

Il mint evita di modificare password, utenti o store di autenticazione solo per far girare le catture.

## Come si genera

1. Si ottiene una sessione valida sul runtime (login UI o cookie già emesso dal server con `SESSION_HOURS`).
2. Si scrive il file **fuori dall’albero del repo**:
   - percorso ufficiale: `/tmp/obs_session_mint.txt`
   - formato (valori mai stampati nei log dell’harness):
     - riga 1: `obs_session=<token>` oppure `nome` + riga 2 `valore`
     - opzionale: `obs_csrf=<token>`
3. L’harness legge il file, autentica la cattura, emette la riga di provenienza, poi **cancella** il file.

Durata della sessione sottostante: parametro esistente **`SESSION_HOURS`** (`api/app/config.py`, default `168`; stesso nome in `.env` / `.env.example`). Nessuna durata scelta a gusto dall’harness.

## Dove finisce / dove non finisce

| destinazione | ammesso |
|--------------|---------|
| `/tmp/obs_session_mint.txt` (host che lancia l’harness) | sì, temporaneo |
| albero git / commit / obs-exchange / report | **no** |
| endpoint HTTP nuovo | **no** |
| uso come login generale dell’UI | **no** |

`.gitignore` copre comunque `obs_session_mint.txt` se il file venisse creato per errore sotto il repo.

## Circoscrizione (O14)

- Metodo **ufficiale** e **unico prioritario** per l’harness di cattura screenshot.
- Non è una via d’accesso generale all’API o all’UI.
- Vita breve dichiarata: allineata a `SESSION_HOURS`; il file mint viene rimosso a fine cattura.
- I report che pubblicano screenshot devono riportare la riga di provenienza **emessa dall’harness** (non riscritta a mano), del tipo:
  `catture autenticate via session mint, scadenza <SESSION_HOURS>h, token non pubblicato`

## Cosa non si tocca

Password admin, utenti, store di autenticazione, `.env` (oltre alla lettura indiretta di nomi/lunghezze e di `SESSION_HOURS` numerico). Nessun nuovo endpoint di autenticazione.
