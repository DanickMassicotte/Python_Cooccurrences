"""
------------------------------------------------------------------
File name:  reader.py
Creation:   14/02/19
Author:     Jean-Charles Bertrand
            Jean-François Lessard
            Dannick Massicotte
------------------------------------------------------------------
Context:    Travail pratique 2 - B62-Projet Oracle
------------------------------------------------------------------
Brief:      Classe qui traite un fichier texte passé en paramètre
------------------------------------------------------------------
"""

import re
import time


class Reader:
    
    def __init__(self, filePath, fileEncoding, maxDictIndex, dbDict):
        self.filePath = filePath
        self.fileEncoding = fileEncoding
        self.dictIndex = maxDictIndex
        self.text = ""
        self.mainText = []
        self.mainDict = dbDict
        self.extract()
    
    def extract(self):
        try:
            with open(self.filePath, 'r', encoding=self.fileEncoding) as file:
                print("Traitement du fichier: {} en cours...".format(self.filePath))
                self.text = file.read().lower()

            for eachWord in self.getWords():
                self.mainText.append(eachWord)  # Ajout de chaque mot à une liste qui contiendra le texte

                # Remplissage du dictionnaire de mot
                if eachWord not in self.mainDict:
                    self.mainDict[eachWord] = self.dictIndex
                    self.dictIndex += 1
        except:
            print("Erreur à l'ouverture du fichier texte: {}".format(self.filePath))

    def getWords(self):
        return re.findall('\w+|[!?]+', self.text)
