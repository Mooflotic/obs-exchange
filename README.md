# obs-exchange

Repo **pubblico** per passare blocchi/diff all’assistente esterno (il monorepo `rete-palazzo` resta privato).

## Nomenclatura
```
obs-<sigla>-faseA-NNN.md
obs-<sigla>-diff-NNN.md
```
Prima riga obbligatoria:
```
<!-- BLOCK-ID: OBS-…-NNN -->
```

## Workflow
```bash
cp rete-palazzo/observatory/docs/<file> ~/Developer/obs-exchange/
cd ~/Developer/obs-exchange
git add . && git commit -m "<file>" && git push
```

File qui dentro possono essere cancellati dopo la lettura.
