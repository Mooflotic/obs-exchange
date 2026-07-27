# Guida d'uso — LAN Observatory

Scritta per l'operatore. Per ogni situazione reale: **dove si vede**, **cosa significa**,
**cosa puoi fare**, **cosa succede dopo**, **cosa non si può sapere**. Niente termini tecnici interni.

Il punto di partenza è sempre **Oggi**: è la coda unica di cose da decidere. Le altre schermate
servono ad approfondire (Dossier), vedere le porte (Impianto), come sono collegati i device
(Topologia) e la salute (Monitor).

---

## 1. È comparso un device nuovo

- **Dove:** in **Oggi**, tra le voci in cima; e in **Inventario**, riquadro «Nuovi».
- **Cosa significa:** un apparato mai visto prima si è presentato in rete. Finché non lo
  riconosci resta segnalato.
- **Cosa puoi fare:** apri il suo **Dossier** per capire cos'è (marca, cosa annuncia, dove è
  attaccato). Se il nome proposto è giusto, **adottalo**; se è rumore, **ignora**.
- **Cosa succede dopo:** adottando, il device prende quel nome ovunque; ignorando, esce dalla
  coda ma resta in Inventario.
- **Cosa non si può sapere:** se il device non annuncia nulla e non è raggiungibile, marca e
  modello possono restare indeterminati: vengono dichiarati «non determinati», non inventati.

## 2. Un nome è sbagliato

- **Dove:** in **Oggi**, sezione «Nomi da decidere → Da verificare»; o nel **Dossier** del device.
- **Cosa significa:** c'è un nome già scelto a mano e una proposta automatica che lo contraddice,
  oppure il nome attuale è debole e ne esiste uno migliore.
- **Cosa puoi fare:** dal Dossier confermi a mano il nome giusto. In Oggi puoi adottare la
  proposta solo se vuoi **sostituire** la scelta manuale.
- **Cosa succede dopo:** il nome che confermi diventa quello ufficiale; l'altro resta come
  storico/divergenza, non sparisce.
- **Cosa non si può sapere:** l'automatismo non decide al posto tuo quando c'è una scelta
  manuale: la tua scelta ha sempre la precedenza.

## 3. Un apparato con più schede di rete va rinominato

- **Dove:** nel **Dossier**. Un apparato con più interfacce (multi-NIC) è mostrato come **un solo
  device**; le singole schede compaiono come sue interfacce, non come device separati.
- **Cosa significa:** rinominando l'apparato, il nome vale per tutto l'insieme, non per la
  singola scheda.
- **Cosa puoi fare:** rinomina l'apparato dal suo Dossier.
- **Cosa succede dopo:** tutte le interfacce di quell'apparato mostrano lo stesso nome.
- **Cosa non si può sapere:** le singole schede non hanno un nome proprio per scelta di
  progetto: non cercare di nominarle una per una.

## 4. Una porta non torna / un cavo è cambiato

- **Dove:** in **Impianto** (le porte dei switch) e in **Topologia** (dove è attaccato).
- **Cosa significa:** l'associazione porta → device può non corrispondere alla realtà attuale.
- **Cosa puoi fare:** in Impianto correggi patch, ruolo o note della porta.
- **Cosa succede dopo:** la correzione manuale resta finché non la cambi.
- **Cosa non si può sapere / ATTENZIONE:** la mappa porte si aggiorna da una fonte che in questo
  momento **è ferma** (vedi punto 8). Se in cima a Impianto vedi «copertura FDB non aggiornata»,
  l'occupazione delle porte mostrata può essere **vecchia di giorni**: verifica prima di fidarti.

## 5. Un device è sparito

- **Dove:** in **Inventario**, riquadro «Non visti di recente»; e nel **Dossier** (stato di presenza).
- **Cosa significa:** non lo vediamo da oltre 24 ore **oppure** la fonte che lo rilevava non è
  disponibile. «Non visto» non vuol dire per forza «spento».
- **Cosa puoi fare:** apri il Dossier per vedere l'ultima volta che è stato visto e da quale fonte.
- **Cosa succede dopo:** se torna a farsi vedere, rientra automaticamente tra gli attivi.
- **Cosa non si può sapere:** se la fonte di rilevamento è muta, non possiamo distinguere «assente»
  da «non misurabile»: lo diciamo esplicitamente invece di dare un numero finto.

## 6. C'è un conflitto da verificare

- **Dove:** in **Oggi**, tra i problemi (voce «conflitto»).
- **Cosa significa:** due informazioni forti si contraddicono (es. due nomi diversi con pari
  autorevolezza).
- **Cosa puoi fare:** apri il Dossier e conferma a mano quale valore tenere.
- **Cosa succede dopo:** il valore che confermi diventa quello corrente; l'altro resta storico.
- **Cosa non si può sapere:** lo strumento non «indovina» il vincitore: aspetta la tua conferma.

## 7. Il FRITZ!Box non risponde

- **Dove:** banner in cima al portale quando la fonte FRITZ!Box è muta.
- **Cosa significa:** una delle fonti principali di presenza non sta rispondendo; alcuni device
  potrebbero risultare «non visti» solo per questo.
- **Cosa puoi fare:** è una segnalazione informativa; la presenza va letta con cautela finché la
  fonte non torna.
- **Cosa succede dopo:** quando la fonte torna, la presenza si riallinea da sola.
- **Cosa non si può sapere:** durante l'assenza della fonte, la presenza di alcuni device non è
  misurabile con certezza.

## 8. I dati di porta sono vecchi

- **Dove:** banner in cima a **Impianto** e badge su ogni switch; in **Monitor**, colonne traffico
  ed errori.
- **Cosa significa:** la mappa che dice «quale device sta su quale porta» non si aggiorna da un po'.
  In Impianto è scritto **quando** è stata l'ultima misura (es. «circa 55 ore fa»).
- **Cosa puoi fare:** usa quei dati come **ultima fotografia nota**, non come stato attuale.
- **Cosa succede dopo:** quando la fonte tornerà ad aggiornarsi, la mappa si aggiornerà.
- **Cosa non si può sapere:** per gli switch che non rispondono, **traffico ed errori sono
  mostrati come «—» (non disponibili)**, non come «0»: uno zero direbbe una cosa falsa.

## 9. Un'inferenza dell'assistente propone un nome

- **Dove:** nel **Dossier** («Proposte nome») e in **Oggi**, dove la proposta porta l'etichetta
  **«Inferenza AI»** con la percentuale di confidenza.
- **Cosa significa:** è un'**ipotesi** dell'assistente, non un fatto misurato. È sempre marcata come
  tale, con la confidenza e le evidenze usate.
- **Cosa puoi fare:** valuta le evidenze; adotta solo se ti convince. Resta sempre sotto la tua scelta.
- **Cosa succede dopo:** se adotti, diventa il nome; se non fai nulla, resta solo una proposta.
- **Cosa non si può sapere:** l'inferenza può sbagliare — per questo non è mai presentata come
  certezza e non modifica da sola lo stato del device.

## 10. Vista di uno switch senza telemetria (es. GS308EP)

- **Dove:** in **Impianto** (riquadro dello switch e «Ramo GS308EP») e in **Topologia** (ramo).
- **Cosa significa:** di questo switch sappiamo con certezza nome/modello, che risponde al ping sul
  suo indirizzo di gestione attuale, la mappa porte inserita a mano, e cosa c'è a valle dedotto dai
  dati dello switch a monte (con confidenza dichiarata).
- **Cosa puoi fare:** consultare e correggere la mappa porte manuale in Impianto.
- **Cosa non si può sapere (dichiarato, non nascosto):** porte interne, contatori, consumo PoE,
  traffico locale della porta. Non vengono mostrati numeri finti né barre vuote. L'indirizzo storico
  del passato è marcato come storico, non come attuale.
