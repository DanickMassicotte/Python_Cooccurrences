"""
------------------------------------------------------------------
File name:  trainer.py
Creation:   02/04/19
Author:     Jean-Charles Bertrand
            Jean-François Lessard
            Danick Massicotte
------------------------------------------------------------------
Context:    Travail pratique 2 - B62-Projet Oracle
------------------------------------------------------------------
Brief:      Outils d'analyse de texte
------------------------------------------------------------------
"""

from analyzer import Analyzer
from DBManager import DBManager
from reader import Reader


class Trainer:

    def __init__(self, filePath, fileEncoding, windowSize):
        self.filePath = filePath
        self.fileEncoding = fileEncoding
        self.windowSize = int(windowSize)
        self.dbmanager = DBManager()

    def execute(self):

        # Création de la table DICTIONNAIRE_COMMUN s'il y a lieu
        #if self.dbmanager.tableDictExists():
        dbDict = self.dbmanager.selectDictionaryDB()  # Recherche des mots déjà présents dans le dict de la BD
        #print("DBDICT: {}".format(len(dbDict)))
        #else:
        #self.dbmanager.createTableDict()
        #dbDict = {}

        # Valeur de l'ID du dernier mot du dictionnaire de la BD
        maxDictIndex = len(dbDict)

        # Lecture du contenu du fichier texte et construction du dictionnaire de mots
        reader = Reader(self.filePath, self.fileEncoding, maxDictIndex, dbDict)

        # Création de la table COOCCURRENCES s'il y a lieu
        if not self.dbmanager.tableCoocExists():
            self.dbmanager.createTableCooc()

        analyzer = Analyzer(self.windowSize, reader.mainDict, reader.mainText)

        # Analyse du texte et création d'un dictionnaire de cooccurrences
        analyzer.extractText()
        
        # Sauvegarde des mots du texte dans le dictionnaire de la base de données
        self.dbmanager.insertDictionaryDB(reader.mainDict, maxDictIndex)

        # Insertion ou mise à jour des cooccurrences dans la base de données
        self.dbmanager.insertScoresDB(analyzer.newCoocDict)

        # Fermeture de la connection à la base de données
        self.dbmanager.closeConnection()
