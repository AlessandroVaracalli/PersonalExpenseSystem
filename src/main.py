import sqlite3
import sys

def connetti_db():
    conn = sqlite3.connect('spese.db')
    return conn

def esegui_script_iniziale(conn):
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS Categorie (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100) UNIQUE NOT NULL
        );
        CREATE TABLE IF NOT EXISTS Spese (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_spesa DATE NOT NULL,
            importo DECIMAL(10, 2) NOT NULL CHECK(importo > 0),
            descrizione TEXT,
            categoria_id INTEGER NOT NULL,
            FOREIGN KEY (categoria_id) REFERENCES Categorie(id)
        );
        CREATE TABLE IF NOT EXISTS Budget (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mese VARCHAR(7) NOT NULL,
            importo DECIMAL(10, 2) NOT NULL CHECK(importo > 0),
            categoria_id INTEGER NOT NULL,
            UNIQUE(mese, categoria_id),
            FOREIGN KEY (categoria_id) REFERENCES Categorie(id)
        );
    """)
    conn.commit()

def ottieni_id_categoria(conn, nome_categoria):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Categorie WHERE nome = ?", (nome_categoria,))
    risultato = cursor.fetchone()
    
    if risultato:
        return risultato[0]
    else:
        return None

def gestisci_categorie(conn):
    nome = input("Inserisci il nome della categoria: ").strip()
    if not nome:
        print("Errore: il nome della categoria non può essere vuoto.")
        return
    
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Categorie WHERE nome = ?", (nome,))
    if cursor.fetchone():
        print("La categoria esiste già.")
    else:
        cursor.execute("INSERT INTO Categorie (nome) VALUES (?)", (nome,))
        conn.commit()
        print("Categoria inserita correttamente.")

def inserisci_spesa(conn):
    data = input("Inserisci la data (YYYY-MM-DD): ").strip()
    importo_str = input("Inserisci l'importo: ").strip()
    
    if importo_str.replace('.', '', 1).isdigit():
        importo = float(importo_str)
    else:
        print("Inserire un importo valido.")
        return

    if importo <= 0:
        print("L'importo deve essere maggiore di zero.")
        return
            
    nome_categoria = input("Inserisci il nome della categoria: ").strip()
    categoria_id = ottieni_id_categoria(conn, nome_categoria)
    
    if not categoria_id:
        print("La categoria non esiste.")
        return
        
    descrizione = input("Inserisci una descrizione (facoltativa): ").strip()
    
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Spese (data_spesa, importo, descrizione, categoria_id) VALUES (?, ?, ?, ?)",
                   (data, importo, descrizione, categoria_id))
    conn.commit()
    print("Spesa inserita correttamente.")

def definisci_budget(conn):
    mese = input("Inserisci il mese (YYYY-MM): ").strip()
    nome_categoria = input("Inserisci il nome della categoria: ").strip()
    importo_str = input("Inserisci l'importo del budget: ").strip()
    
    if importo_str.replace('.', '', 1).isdigit():
        importo = float(importo_str)
    else:
        print("Inserire un valore numerico.")
        return
        
    if importo <= 0:
        print("Inserire un budget valido.")
        return

            
    categoria_id = ottieni_id_categoria(conn, nome_categoria)
    if not categoria_id:
        print("La categoria non esiste.")
        return
        
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM Budget WHERE mese = ? AND categoria_id = ?", (mese, categoria_id))
    risultato = cursor.fetchone()
    
    if risultato:
        cursor.execute("UPDATE Budget SET importo = ? WHERE mese = ? AND categoria_id = ?", 
                       (importo, mese, categoria_id))
    else:
        cursor.execute("INSERT INTO Budget (mese, importo, categoria_id) VALUES (?, ?, ?)", 
                       (mese, importo, categoria_id))
        
    conn.commit()
    print("Budget mensile salvato.")

def visualizza_report(conn):
    while True:
        print("\n--- Menu dei Report ---")
        print("1. Totale spese per categoria")
        print("2. Spese mensili vs budget")
        print("3. Elenco completo delle spese ordinate per data")
        print("4. Ritorna al menu principale")
        
        scelta = input("Inserisci la tua scelta: ").strip()
        cursor = conn.cursor()
        
        if scelta == '1':
            cursor.execute("""
                SELECT C.nome, SUM(S.importo) 
                FROM Spese S JOIN Categorie C ON S.categoria_id = C.id 
                GROUP BY C.nome
            """)
            print("\nCategoria\t\tTotale Speso")
            for riga in cursor.fetchall():
                print(f"{riga[0]}\t\t{riga[1]:.2f}")
                
        elif scelta == '2':
            mese_ricerca = input("Inserisci il mese (YYYY-MM) per il report: ").strip()
            
            cursor.execute("SELECT categoria_id, importo FROM Budget WHERE mese = ?", (mese_ricerca,))
            budgets = cursor.fetchall()
            
            if not budgets:
                print("Nessun budget trovato per questo mese.")
            else:
                for b in budgets:
                    categoria_id = b[0]
                    budget_importo = b[1]
                    
                    cursor.execute("SELECT nome FROM Categorie WHERE id = ?", (categoria_id,))
                    riga_cat = cursor.fetchone()
                    if riga_cat:
                        nome_categoria = riga_cat[0]
                    else:
                        nome_categoria = "Sconosciuta"
                    
                    mese_like = mese_ricerca + "-%" 
                    cursor.execute("""
                        SELECT SUM(importo) FROM Spese 
                        WHERE categoria_id = ? AND data_spesa LIKE ?
                    """, (categoria_id, mese_like))
                    
                    riga_spesa = cursor.fetchone()
                    if riga_spesa and riga_spesa[0] is not None:
                        speso = float(riga_spesa[0])
                    else:
                        speso = 0.0
                        
                    if speso > budget_importo:
                        stato = "SUPERAMENTO BUDGET"
                    else:
                        stato = "IN BUDGET"
                        
                    print(f"\nMese: {mese_ricerca}")
                    print(f"Categoria: {nome_categoria}")
                    print(f"Budget: {budget_importo:.2f}")
                    print(f"Speso: {speso:.2f}")
                    print(f"Stato: {stato}")
                    
        elif scelta == '3':
            cursor.execute("""
                SELECT S.data_spesa, C.nome, S.importo, S.descrizione 
                FROM Spese S JOIN Categorie C ON S.categoria_id = C.id 
                ORDER BY S.data_spesa ASC
            """)
            print("\nData\t\tCategoria\tImporto\tDescrizione")
            for riga in cursor.fetchall():
                print(f"{riga[0]}\t{riga[1]}\t{riga[2]:.2f}\t{riga[3]}")
                
        elif scelta == '4':
            break
        else:
            print("Scelta non valida.")

# Funzione aggiunta in autonomia: sezione per valutare un investimento in base al budget residuo del mese
def gestisci_investimenti(conn):
    print("\n--- Menù Investimenti ---")
    mese_ricerca = input("Inserisci il mese (YYYY-MM) per controllare il budget: ").strip()
    cursor = conn.cursor()
    
    cursor.execute("SELECT SUM(importo) FROM Budget WHERE mese = ?", (mese_ricerca,))
    riga_budget = cursor.fetchone()
    
    if riga_budget and riga_budget[0] is not None:
        totale_budget = float(riga_budget[0])
    else:
        totale_budget = 0.0
        
    mese_like = mese_ricerca + "-%"
    cursor.execute("SELECT SUM(importo) FROM Spese WHERE data_spesa LIKE ?", (mese_like,))
    riga_spesa = cursor.fetchone()
    
    if riga_spesa and riga_spesa[0] is not None:
        totale_speso = float(riga_spesa[0])
    else:
        totale_speso = 0.0
        
    rimanenza = totale_budget - totale_speso
    
    if rimanenza > 0:
        print(f"\nTi rimangono {rimanenza:.2f} euro per questo mese.")
        scelta = input("Vuoi utilizzare il 10% per investimenti? (s/n): ").strip().lower()
        
        if scelta == 's' or scelta == 'si':
            investimento = rimanenza * 0.10
            budget_residuo = rimanenza - investimento
            print(f"Ottimo! {investimento:.2f} euro vanno in investimenti.")
            print(f"Ti rimangono {budget_residuo:.2f} euro di budget.")
        else:
            print(f"\nNessun investimento effettuato. Ti rimangono {rimanenza:.2f} euro di budget mensile.")
            
    else:
        print(f"\nIl budget mensile è a {rimanenza:.2f} euro.")
        print("Budget finito. Non è rimasto nulla da investire.")

def menu_principale():
    conn = connetti_db()
    esegui_script_iniziale(conn)
    
    print("Benvenuto nel Sistema di Gestione delle Spese Personali e del Budget!")
    
    while True:
        print("\nSISTEMA SPESE PERSONALI")
        print("1. Gestione Categorie")
        print("2. Inserisci Spesa")
        print("3. Definisci Budget Mensile")
        print("4. Visualizza Report")
        print("5. Investimenti")
        print("6. Esci")
        
        scelta = input("Inserisci la tua scelta: ").strip()
        
        if scelta == '1':
            gestisci_categorie(conn)
        elif scelta == '2':
            inserisci_spesa(conn)
        elif scelta == '3':
            definisci_budget(conn)
        elif scelta == '4':
            visualizza_report(conn)
        elif scelta == '5':
            gestisci_investimenti(conn)
        elif scelta == '6':
            print("Uscita dal programma.")
            conn.close()
            sys.exit(0)
        else:
            print("Scelta non valida. Riprovare.")

if __name__ == "__main__":
    menu_principale()