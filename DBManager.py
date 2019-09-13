"""
------------------------------------------------------------------
File name:  DBManager.py
Creation:   19/03/19
Author:     Jean-Charles Bertrand
            Jean-François Lessard
            Danick Massicotte
------------------------------------------------------------------
Context:    Travail pratique 2 - B62-Projet Oracle
------------------------------------------------------------------
Brief:      Outils de connexion à la base de données Oracle
------------------------------------------------------------------
"""

import sqlite3
from sqlite3 import Error
import cx_Oracle
from constants import *


class DBManager:
    def __init__(self):
        #self.dsn = cx_Oracle.makedsn(LOGIN_HOSTNAME, LOGIN_PORT, LOGIN_SID)
        #self.user = LOGIN_USERNAME + '/' + LOGIN_PASSWORD + '@' + self.dsn
        #self.connection = cx_Oracle.connect(self.user)
        self.connection = self.createConnection()
        self.cursor = self.connection.cursor()
        
    # ============================================================
    #
    # Connexion à la base de données SQLite. Créé la base de 
    # données si elle n'existe pas.
    # 
    # ============================================================
    def createConnection(self):
        #print("Connection à la base de donnée...")
        conn = None
        
        try:
            conn = sqlite3.connect(DB_FILE)
            
        except Error as e:
            print("Erreur de connexion à SQLite: ", e)
            
        return conn

    # ============================================================
    #
    # Ferme les connexions à la base de données
    # 
    # ============================================================
    def closeConnection(self):
        self.cursor.close()
        self.connection.close()
    
    # ============================================================
    #
    # Insère un dictionnaire de mots dans la base de données; le
    # dictionnaire doit être (mot, index).
    #
    # ============================================================ 
    def insertDictionaryDB(self, dictionary, dbMaxID):
        l = []
        
        for key, value in dictionary.items():
            if value >= dbMaxID:     # Si l'ID du mot ne figure pas déjà dans le dictionnaire
                l.append((value, key))
            
        self.cursor.executemany(REQ_INSERT_DICT, l)
        self.connection.commit()
        print("{} mots insérés dans la base de données.".format(len(l)))

    # ============================================================
    #
    # Fonction retournant tous les mots de la base de données sous
    # forme de dictionnaire.
    #
    # ============================================================
    def selectDictionaryDB(self):
        #print("Récupération des mots de la BD dans un dictionnaire en cours...")
        wordDict = {}
        
        self.cursor.execute(REQ_SELECT_DICT)

        for id, word in self.cursor.fetchall():
            wordDict[word] = id

        #print("Récupération terminée.")
        return wordDict

    # ==============================================================================
    #
    # Fonction retournant tous les mots de la base de données sous forme de liste.
    #
    # ==============================================================================
    def getDictList(self):
        wordList = []

        self.cursor.execute(REQ_SELECT_DICT)

        for tup in self.cursor.fetchall():
            wordList.append(tup[1])

        return wordList

    # ==============================================================================
    #
    # Fonction qui met à jour la table COOCCURRENCES de la base de données
    #
    # ==============================================================================
    def insertScoresDB(self, newCoocDict):

        # Création d'un dictionnaire contenant toutes les cooccurrences existantes dans la BD
        coocDict = self.coocToDict()

        insertList = []
        updateList = []

        for (id_word1, id_word2, window), score in newCoocDict.items():
            if (id_word1, id_word2, window) in coocDict:
                updateList.append((score + coocDict[(id_word1, id_word2, window)], id_word1, id_word2, window))
            else:
                insertList.append((id_word1, id_word2, window, score))

        self.cursor.executemany(REQ_INSERT_SCORES, insertList)
        self.cursor.executemany(REQ_UPDATE_SCORES, updateList)
        self.connection.commit()

    # ==============================================================================
    #
    # Fonction qui retourne un dictionnaires de tuple (id_mot1, id_mot2, fenetre)
    # de toutes les cooccurrences présentes dans la base de données.
    #
    # ==============================================================================
    def coocToDict(self):
        coocDict = {}

        self.cursor.execute(REQ_SELECT_ALL_WORDS_COOC)

        for id_mot1, id_mot2, fenetre, resultat in self.cursor.fetchall():
            coocDict[(id_mot1, id_mot2, fenetre)] = resultat

        return coocDict
    
    # =====================================================================
    #
    # Fonction qui retourne un dictionnaire de tuple (id_mot1, id_mot2) de
    # toutes les cooccurrences présentes dans la base de données selon une 
    # fenêtre de mots utilisée à l'entrainement.
    # 
    # =====================================================================
    def coocToDictWindow(self, window):
        coocDict = {}
        l = []
        l.append(window)

        self.cursor.execute(REQ_SELECT_COOC_WINDOW, l)
        
        for id_mot1, id_mot2, resultat in self.cursor.fetchall():
            coocDict[(id_mot1, id_mot2)] = resultat

        return coocDict

    # ==============================================================================
    #
    # Création de la table DICTIONNAIRE_COMMUN dans la base de données
    #
    # ==============================================================================
    def createTableDict(self):
        self.cursor.execute(REQ_CREATE_DICT)
        
    # ==============================================================================
    #
    # Création de la table COOCCURENCES dans la base de données
    #
    # ==============================================================================
    def createTableCooc(self):
        self.cursor.execute(REQ_CREATE_COOC)
        #self.cursor.execute(REQ_ALTER_COOC1)
        #self.cursor.execute(REQ_ALTER_COOC2)

    # ==============================================================================
    #
    # Fonction retournant 1 si la table DICTIONNAIRE_COMMUN existe. Retourne 0 sinon
    #
    # ==============================================================================
    def tableDictExists(self):
        self.cursor.execute(REQ_TABLE_DICT_EXIST_SQLITE)
        return self.cursor.fetchone()[0]

    # ==============================================================================
    #
    # Fonction retournant 1 si la table COOCCURRENCES existe. Retourne 0 sinon
    #
    # ==============================================================================
    def tableCoocExists(self):
        self.cursor.execute(REQ_TABLE_COOC_EXIST_SQLITE)
        return self.cursor.fetchone()[0]
    
    # ==============================================================================
    #
    # Fonction retournant l'index le plus élevé de la table DICTIONNAIRE_COMMUN
    #
    # ==============================================================================
    def getDictMaxID(self):
        self.cursor.execute(REQ_GET_MAX_DICT_ID)
        return self.cursor.fetchone()[0]

    # ===================================================================================
    #
    # Fonction retournant 1 si la taille de fenêtre existe dans la BD. Retourne 0 sinon
    #
    # ===================================================================================
    def isWindowValid(self, windowSize):
        #print("Vérification de la validité de la taille de fenêtre en cours...")
        self.cursor.execute(REQ_SELECT_WINDOW_SIZE, windowSize)
        return self.cursor.fetchone()[0]



