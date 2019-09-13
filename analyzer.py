"""
------------------------------------------------------------------
File name:  analyzer.py
Creation:   14/02/19
Author:     Jean-Charles Bertrand
            Jean-François Lessard
            Danick Massicotte
------------------------------------------------------------------
Context:    Travail pratique 2 - B62-Projet Oracle
------------------------------------------------------------------
Brief:      Outils d'analyse de texte
------------------------------------------------------------------
"""

import numpy as np
import stopWords


class Analyzer:
    
    def __init__(self, windowSize, mainWordDict, mainText = None):
        self.mainWordDict = mainWordDict
        self.mainText = mainText
        self.windowSize = int(windowSize)
        self.midWindow = self.windowSize // 2
        self.wordMatrix = np.zeros((len(self.mainWordDict), len(self.mainWordDict)))
        self.newCoocDict = {}

    # FONCTION OBSOLÈTE - Remplie la matrice de cooccurence en utilisant la fenêtre
    def fillMatrix(self):
        mainTextSize = len(self.mainText)   # Le nombre de mots dans la liste de mots du texte

        # Pour tous les mots dans la liste de mots du texte moins la longueur de la fenêtre
        # pour éviter de dépasser l'index
        for i in range(mainTextSize-self.windowSize):
            # Index du mot au milieu de la fenêtre
            middleWordIndex = self.mainWordDict[self.mainText[i+self.midWindow]]

            # Pour toute la largeur de la fenêtre
            for j in range(self.windowSize):
                if j == self.midWindow:
                    continue
                else:
                    comparedWordIndex = self.mainWordDict[self.mainText[i+j]]
                    self.wordMatrix[middleWordIndex][comparedWordIndex] += 1

    # ================================================================
    #
    # Remplie la matrice de cooccurrences selon un dictionnaire passé
    # en paramètre pour le Searcher.
    # 
    # ================================================================    
    def fillMatrixSearch(self, dictionary):

        #print("Remplissage de la matrice en cours...")
        for id_1, id_2 in dictionary:
            a = int(id_1)
            b = int(id_2)
            self.wordMatrix[a][b] = dictionary[(id_1, id_2)]
            self.wordMatrix[b][a] = dictionary[(id_1, id_2)]

        #print("Matrice remplie.")

    # ================================================================
    #
    # Analyse le texte et crée un dictionnaire de tuple contenant
    # le nombre de cooccurrences pour chaque combinaison mots/fenetre
    # ex: (mot1, mot2, tailleFenetre: nbCooccurrences)
    #
    # ================================================================
    def extractText(self):

        mainTextSize = len(self.mainText)  # Le nombre de mots dans la liste de mots du texte

        # Pour tous les mots dans la liste de mots du texte moins la longueur de la fenêtre
        # pour éviter de dépasser l'index
        for i in range(mainTextSize - self.windowSize):
            # Index du mot au milieu de la fenêtre
            middleWordIndex = self.mainWordDict[self.mainText[i + self.midWindow]]

            # Pour toute la largeur de la fenêtre
            for j in range(self.windowSize):
                if j == self.midWindow:
                    continue
                else:
                    comparedWordIndex = self.mainWordDict[self.mainText[i + j]]

                # Ajouts au dictionnaire de tuples
                if middleWordIndex > comparedWordIndex:
                    t = (middleWordIndex, comparedWordIndex, self.windowSize) 
                    if t not in self.newCoocDict:
                        self.newCoocDict[t] = 0
                    self.newCoocDict[t] += 1

    # ================================================================
    # Algorithme produit scalaire
    # ================================================================
    def dotProduct(self, vector1, vector2):
        return np.dot(vector1, vector2)

    # ================================================================
    # Algorithme least-squares
    # ================================================================
    def leastSquare(self, vector1, vector2):
        return np.sum((vector1 - vector2)**2)

    # ================================================================
    # Algorithme city-block
    # ================================================================
    def cityBlock(self, vector1, vector2):
        return np.sum(np.abs(vector1 - vector2))

    # ================================================================
    #
    # Recherche des meilleurs résultats selon le mot et l'algorithme
    # passés en paramètres.
    #
    # ================================================================
    def process(self, searchedWord, algo, dictionary={}):
        if len(dictionary) == 0:
            dictionary = self.reader.mainDict

        searchedWordIndex = int(dictionary[searchedWord])  # Recherche de l'index du mot sélectionné

        resultList = []

        for mot, index in dictionary.items():
            if mot == searchedWord or mot in stopWords.stopWords:
                continue
            else:
                result = algo(self.wordMatrix[searchedWordIndex], self.wordMatrix[index])
                resultList.append((mot, result))

        return resultList

    def sortResults(self, resultsList, sortOrderDesc):
        if sortOrderDesc:
            return sorted(resultsList, key=lambda kv: kv[1], reverse=True)
        else:
            return sorted(resultsList, key=lambda kv: kv[1])

    def printResults(self, nbOfSynonyms, resultsList):
        print("Résultats:\n")
        for i in range(nbOfSynonyms):
            print(resultsList[i])
        print()
