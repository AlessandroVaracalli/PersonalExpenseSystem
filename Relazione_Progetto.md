Progetto università – Esame fondamenti di Informatica (9 CFU)  
Studente: Alessandro Varacalli  
Matricola: 0092500221  
Mail: alessandro.varacalli@studenti.uniroma5.it  

---

### Progetto: Software di gestione delle Spese personali basato su console

Per lo sviluppo del progetto ho utilizzato Python e un database SQL.

Di seguito una breve sintesi delle logiche e dei costrutti applicati nella scrittura del codice e nella progettazione del database:

---

### Architettura del Database

Il database è strutturato su tre tabelle principali: Categorie, Spese e Budget. Per garantire l'integrità dei dati, ho preferito applicare i controlli e i vincoli direttamente al database: 

- Chiavi esterne (Foreign Key): Le ho utilizzate per assicurarmi che ogni spesa o budget inserito sia sempre associato a una categoria realmente esistente e già validata.

- NOT NULL: Ho applicato questo vincolo sui campi fondamentali per rendere obbligatorio l'inserimento dei dati ed evitare la registrazione di dati incompleti.

- UNIQUE: L'ho usato sui nomi delle categorie per garantirne l'unicità e prevenire la creazione di eventuali duplicati.

- CHECK: Tramite lo script di creazione, ho inserito il vincolo CHECK (importo > 0) per far sì che il database accetti solo valori positivi.

---

### Struttura del Codice Python

L'interfaccia utente rispetta i parametri richiesti:

- Gestione del menu: Il programma è gestito da un ciclo `while` che mantiene il menu sempre attivo fino a quando l'utente non seleziona l'opzione "6" per uscire.

- Validazione preventiva: Per i controlli numerici ho utilizzato un costrutto `if/else` combinato con il metodo `importo.replace('.', '', 1).isdigit()`, in modo da verificare subito se il testo digitato è un numero decimale valido (rifiutando lettere o segni negativi) prima di provare a converitlo in virgola mobile (`float`).

- Logica del Budget: Il modulo per l'inserimento del budget interroga prima il database tramite una `SELECT`. Se esiste già un limite impostato per quel mese e per quella categoria, lo sovrascrive aggiornandolo con un `UPDATE`; altrimenti, registra un record nuovo usando un `INSERT`.

- Report: Per i report ho unito le logiche di SQL (`JOIN` e `SUM` per incrociare e sommare i dati) con quelle di Python. Nel report mensile, il codice confronta il totale speso con il budget prefissato, avvisando eventualmente l'utente se è stato rispettato,"IN BUDGET", o se è stato superato, "SUPERAMENTO BUDGET".

---

### Funzionalità Extra: Investimenti

Ho deciso di aggiungere in autonomia una funzione extra dedicata agli Investimenti.

L'idea alla base è che, se a fine mese avanza una parte del budget, il software suggerisce all'utente di destinarne il 10% ai propri investimenti.
Se l'utente accetta, il sistema calcola la quota investita e la dichiara, mostrando il budget residuo aggiornato; se rifiuta, mostra semplicemente il totale dei soldi rimasti.

So che questa opzione si sarebbe potuta inserire aggiungendo una semplice categoria "Investimenti" tra le spese normali, ma voleva essere un meccanismo attivo di suggerimento al risparmio.



