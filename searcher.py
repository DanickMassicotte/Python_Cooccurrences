# -*- coding: utf-8 -*-
"""
------------------------------------------------------------------
File name:  searcher.py
Creation:   14/02/19
Author:     Jean-Charles Bertrand
            Jean-François Lessard
            Danick Massicotte
------------------------------------------------------------------
Context:    Travail pratique 2 - B62-Projet Oracle
------------------------------------------------------------------
Brief:      Classe qui traite la fonction recherche
------------------------------------------------------------------
"""

from DBManager import *
from analyzer import *
import time


class Searcher:
    def __init__(self, windowSize):
        self.windowSize = windowSize
        self.dbManager = DBManager()
        self.dictionary = self.dbManager.selectDictionaryDB()
        self.isWindowValid = self.dbManager.isWindowValid(self.windowSize)
        self.analyzer = Analyzer(self.windowSize, self.dictionary)
        self.analyzer.fillMatrixSearch(self.dbManager.coocToDictWindow(self.windowSize))
        
    # ==================================================================
    #
    # Fonction principale du Searcher; recherche une liste de synonymes
    # à un mot passé en paramètre selon une fenêtre de mot précisée
    # 
    # ==================================================================    
    def execute(self):
        while True:
            print("Entrez un mot, le nombre de synonymes que vous voulez et la méthode de calcul,")
            print("i.e. produit scalaire: 0, least squares: 1, cityblock: 2\n")
            userInput = input("Tapez q pour quitter\n\n")
            
            if userInput.lower() != 'q':
                try:
                    # Séparation de la liste d'arguments entrés par l'utilisateur
                    userInputList = userInput.split()
                    searchedWord = userInputList[0]
                    nbOfSynonyms = int(userInputList[1])
                    algoType = int(userInputList[2])
                    sortOrderDesc = False
                    
                    print("\nRecherche en cours...\n")
                    start = time.time()

                    # Choix de la méthode de calcul selon les paramètres de l'utilisateur
                    if searchedWord in self.dictionary:
                        if algoType == 0:
                            algo = self.analyzer.dotProduct
                            sortOrderDesc = True

                        elif algoType == 1:
                            algo = self.analyzer.leastSquare
                            
                        elif algoType == 2:
                            algo = self.analyzer.cityBlock
                            
                        else:
                            print("Erreur!: Veuillez entrer un numéro d'algorithme valide! (0, 1 ou 2)\n")
                            continue

                        # Calcul des cooccurrences et affichage des résultats édités
                        resultsList = self.analyzer.process(searchedWord, algo, self.dictionary)
                        end = time.time()
                        
                        self.analyzer.printResults(nbOfSynonyms, self.analyzer.sortResults(resultsList, sortOrderDesc))
                        
                        print("Recherche effectuée en {} secondes\n".format(end-start))
                    else:
                        print("Erreur!: Mot introuvable!\n")
                except IndexError:
                    print("Erreur!: Nombre d'arguments invalide!\n")
            else:
                break
