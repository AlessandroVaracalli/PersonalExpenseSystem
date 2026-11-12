-- database.sql

CREATE TABLE IF NOT EXISTS Categorie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS Spese (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_spesa DATE NOT NULL,
    importo DECIMAL(10, 2) NOT NULL
    descrizione TEXT,
    categoria_id INTEGER NOT NULL,
    FOREIGN KEY (categoria_id) REFERENCES Categorie(id)
);

CREATE TABLE IF NOT EXISTS Budget (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mese VARCHAR(7) NOT NULL, -- Formato YYYY-MM
    importo DECIMAL(10, 2) NOT NULL CHECK(importo > 0),
    categoria_id INTEGER NOT NULL,
    UNIQUE(mese, categoria_id),
    FOREIGN KEY (categoria_id) REFERENCES Categorie(id)
);


INSERT INTO Categorie (nome) VALUES ('Alimentari');
INSERT INTO Categorie (nome) VALUES ('Trasporti');
INSERT INTO Categorie (nome) VALUES ('Investimenti');

INSERT INTO Spese (data_spesa, importo, descrizione, categoria_id) 
VALUES ('2025-01-15', 25.00, 'Pranzo', 1);
INSERT INTO Spese (data_spesa, importo, descrizione, categoria_id) 
VALUES ('2025-01-20', 120.00, 'Abbonamento treno', 2);

INSERT INTO Budget (mese, importo, categoria_id) VALUES ('2025-01', 300.00, 1);