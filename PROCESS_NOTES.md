# Note di processo (permanenti)

Regole operative accettate e non da ri-litigare ogni ondata. Non sono debiti aperti.

## Hash del report ≠ hash del commit che lo pubblica

Un report **non può** contenere l’hash del commit che lo pubblica: l’hash dipende dal
contenuto del tree, e il contenuto dipenderebbe dall’hash — impossibilità strutturale di git.

**Metodo corretto (da O21 in poi):** ogni ondata, nel Blocco 0.1, conferma con `git log` /
`git rev-parse` dal vivo l’hash finale **reale** dell’ondata precedente. Il lag di un’ondata
è **permanente e accettato**. Non va «risolto» con amend ricorsivi, tip auto-referenziali,
né registrato di nuovo come debito a ogni ondata.

Nel report finale (G5) si pubblica l’hash del commit **principale** (codice/D o misura+STOP),
con nota esplicita a questa regola per l’eventuale commit successivo di sola pubblicazione
documentale.

## URL raw obs-exchange: sempre commit-pinned

Nei report e nelle prove di share, l’URL raw di un artefatto su `Mooflotic/obs-exchange`
deve puntare a un **commit SHA** (`…/obs-exchange/<sha>/file`), mai a `main`.
`main` può divergere dopo share successivi; il pin è la prova riproducibile (curl 200 +
doppio sha256 locale/raw). `./scripts/share.sh` può stampare ancora un URL `main` come
scorciatoia: il report deve comunque citare l’hash del commit di share appena creato.
