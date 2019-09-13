"""
------------------------------------------------------------------
File name:  constants.py
Creation:   21/03/19
Author:     Jean-Charles Bertrand
            Jean-François Lessard
            Danick Massicotte
------------------------------------------------------------------
Context:    Travail pratique 2 - B62-Projet Oracle
------------------------------------------------------------------
Brief:      Constantes relatives à la connexion à la base de
            données et aux commandes pour les requêtes
------------------------------------------------------------------
"""

# ============================================================
# Constantes de login
# ============================================================


LOGIN_USERNAME = "e0582846"
LOGIN_PASSWORD = "bnmj5648"

LOGIN_HOSTNAME = "delta"
LOGIN_PORT = 1521
LOGIN_SID = "decinfo"

# ============================================================
# Constantes pour SQLite
# ============================================================
DB_FILE = "cooccurrencesDB.db"

# ============================================================
# Constantes pour les requêtes SQL
# ============================================================

# Commandes CREATE TABLE
REQ_CREATE_DICT = "CREATE TABLE IF NOT EXISTS dictionnaire_commun ( " \
                    "id	        INTEGER, " \
                    "mot        TEXT    NOT NULL, " \
                    "CONSTRAINT pk_dictcom_id PRIMARY KEY(id), " \
                    "CONSTRAINT uc_dictcom_mot UNIQUE(mot))"
                    
REQ_CREATE_COOC = "CREATE TABLE IF NOT EXISTS cooccurrences ( " \
                    "id_mot1		INTEGER		NOT NULL, " \
                    "id_mot2		INTEGER		NOT NULL, " \
                    "fenetre		INTEGER		NOT NULL, " \
                    "resultat	    INTEGER		NOT NULL, " \
                    "CONSTRAINT pk_cooccurrences	PRIMARY KEY(id_mot1, id_mot2, fenetre), " \
                    "FOREIGN KEY (id_mot1) REFERENCES dictionnaire_commun(id), " \
                    "FOREIGN KEY (id_mot2) REFERENCES dictionnaire_commun(id))"
                    
#REQ_ALTER_COOC1 = "ALTER TABLE cooccurrences " \
#                  "ADD CONSTRAINT fk_dictcom_cooccurrences_mot1 " \
#                    "FOREIGN KEY (id_mot1) " \
#                    "REFERENCES dictionnaire_commun(id)"
                    
#REQ_ALTER_COOC2 = "ALTER TABLE cooccurrences " \
#                  "ADD CONSTRAINT fk_dictcom_cooccurrences_mot2 " \
#                    "FOREIGN KEY (id_mot2) " \
#                    "REFERENCES dictionnaire_commun(id)"
                    
                    
# Commandes SELECT
REQ_SELECT_DICT = "SELECT * FROM dictionnaire_commun"
REQ_SELECT_ALL_WORDS_COOC = "SELECT * FROM cooccurrences"
REQ_SELECT_COOC_WINDOW = "SELECT id_mot1, id_mot2, resultat FROM cooccurrences WHERE fenetre = :1"
REQ_TABLE_DICT_EXIST = "SELECT count(*) count FROM user_tables where table_name = 'DICTIONNAIRE_COMMUN'"
REQ_TABLE_COOC_EXIST = "SELECT count(*) count FROM user_tables where table_name = 'COOCCURRENCES'"
REQ_TABLE_DICT_EXIST_SQLITE = "SELECT count(*) FROM sqlite_master where type='table' AND name='DICTIONNAIRE_COMMUN'"
REQ_TABLE_COOC_EXIST_SQLITE = "SELECT count(*) FROM sqlite_master where type='table' AND name='COOCCURRENCES'"
REQ_GET_MAX_DICT_ID = "SELECT MAX(id) FROM DICTIONNAIRE_COMMUN"
REQ_SELECT_WINDOW_SIZE = "SELECT count(*) FROM cooccurrences WHERE fenetre = :1"

# Commandes INSERT
REQ_INSERT_DICT = "INSERT INTO dictionnaire_commun(id, mot) VALUES(:1, :2)"
REQ_INSERT_SCORES = "INSERT INTO cooccurrences(id_mot1, id_mot2, fenetre, resultat) VALUES(:1, :2, :3, :4)"

# Commandes UPDATE
REQ_UPDATE_SCORES = "UPDATE cooccurrences SET resultat = :1 WHERE id_mot1 = :2 AND id_mot2 = :3 AND fenetre = :4"
