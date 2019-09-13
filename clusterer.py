
"""
------------------------------------------------------------------
File name:  clusterer.py
Creation:   14/02/19
Author:     Jean-Charles Bertrand
            Jean-François Lessard
            Danick Massicotte
------------------------------------------------------------------
Context:    Travail pratique 2 - B62-Projet Oracle
------------------------------------------------------------------
Brief:      Classe qui traite la création de centroides
------------------------------------------------------------------
"""


from DBManager import *
from analyzer import *
import random

import time
import pickle


class Clusterer:
    def __init__(self, windowSize, wordQty, clusterWordList, clusterQty, clusteringType):
        self.windowSize = windowSize
        self.wordQty = int(wordQty)
        self.clusterWordList = clusterWordList
        self.nbOfClusters = int(clusterQty)
        self.clusteringType = clusteringType
        self.dbManager = DBManager()
        self.mainWordDict = self.dbManager.selectDictionaryDB()
        self.isWindowValid = self.dbManager.isWindowValid(self.windowSize)
        self.analyzer = Analyzer(self.windowSize, self.mainWordDict)
        self.analyzer.fillMatrixSearch(self.dbManager.coocToDictWindow(self.windowSize))
        self.wordMatrix = self.analyzer.wordMatrix
        self.centroidArrayArray = [[]]

    def execute(self):
        if self.clusteringType == 'words':
            print("Liste de mots (centroides): {}. Taille de fenetre: {}".format(self.clusterWordList, self.windowSize))
            start = time.time()
            centroids, membership = self.clusterByName()
            end = time.time()

        elif self.clusteringType == 'random':
            print("\n{} centroides, generes aleatoirement. Taille de fenetre: {}\n".format(self.nbOfClusters, self.windowSize))
            start = time.time()
            
            
            centroids, membership = self.clusterByRandom()
            
            
            
            
            #AFIN DE TESTER LES METHODES ALTERNATIVES DE CREATION DES CENTROIDES
            #VEUILLEZ METTRE EN COMMENTAIRE LA LIGNE DU DESSUS (50) ET METTRE ACTIVE
            #L'UNE DES 3 LIGNES DESSOUS
            
            #centroids, membership = self.clusterFullRandomMethodeA()   #Methode A
            #centroids, membership = self.clusterFullRandomD()       #methode D
            #centroids, membership = self.clusterFullRandom()        #methode B
            #centroids, membership = self.hypothesisCluster()        #methode C
            end = time.time()
        else:
            print("Erreur inattendue!")
            
        self.printClusterResults(centroids, membership)
        print("Clustering complete en {} secondes.".format(end - start))
        
    def clusterByName(self):
        # Creation d'un Array qui contiendra les n mots-centroides
        centroidArray = np.zeros((self.nbOfClusters, len(self.wordMatrix)))

        # Remplissage de l'Array avec les mots-centroides
        for i in range(len(self.clusterWordList)):
            centroidArray[i] = self.wordMatrix[i]

        # Creation d'un Array qui contiendra a quel mot-centroide les mots du dictionnaire appartiennent
        prevMembership = np.zeros(len(self.mainWordDict))

        for i in range(len(self.mainWordDict)):
            # Mise en memoire des scores du mot du dictionnaire par rapport Ã  chaque mot-centroÃ¯de
            scoreList = []
            for j in range(self.nbOfClusters):
                score = self.analyzer.leastSquare(centroidArray[j], self.wordMatrix[i])
                scoreList.append(score)
            minScore = min(scoreList)
            minScoreIndex = scoreList.index(minScore)

            prevMembership[i] = minScoreIndex

            return self.clusterLoop(prevMembership)

    def clusterByRandom(self):
        prevMembership = np.random.randint(0, self.nbOfClusters, len(self.wordMatrix))
        #self.dumpPickle(prevMembership)
        #prevMembership = self.loadPickle()
        return self.clusterLoop(prevMembership)
    

    def hypothesisCluster(self):
        
        threshold = 2000   
        indexCluster1 = random.randrange(0, len(self.mainWordDict)) #on initie avec un cluster issue du hasard
        array_cluster = [[]]
        #print(indexCluster1)
        array_cluster[0] = self.wordMatrix[indexCluster1]
        #print("jjj")
        #print(array_cluster[0])
        
        for i in range(len(self.mainWordDict)):
            vector1 = [] 
            vector1 = self.wordMatrix[i]
            
            for z in range (len(array_cluster)):   #noter que l'array va grossir avec l'ajout de nouveaux cluster
                vector2 = array_cluster[z]
                #print(vector1)
                #print(vector2)
                score =  np.sum((vector1 - vector2)**2)
                #print(score)
                #print(score)
                if score < threshold:
                    break
                else:
                    if z == len(array_cluster)-1:
                        threshold *= 1.2
                        array_cluster.append(self.wordMatrix[i])
                        #print(z)
        #print("over here")
        #print(len(array_cluster))
        self.nbOfClusters = len(array_cluster)
        return self.clusterLoop(self.attributeMembership(array_cluster))
                    
        
        #2 methodes testées. Méthode A : (trouver max de toutes les 'colonnes' d'un point et application a tout
        # les positions pour randomization et Methode B max local pour une colonne
        # Methode A : mise en veilleuse ligne 136, 145, 146, 149
        
    def clusterFullRandomMethodeA(self):
        #maxValues = []
        topMax = 0
              
        maxValues = np.zeros(len(self.mainWordDict))
        self.centroidArrayArray = np.zeros((self.nbOfClusters, len(self.mainWordDict)))
        #on va chercher les valeurs maximales pour chaque mot (en terme de coocurences max)
        for i in range(len(self.mainWordDict)):
            for j in range(len(self.mainWordDict)):
                if topMax  < self.wordMatrix[i][j]:
                    topMax = self.wordMatrix[i][j]
                    
                        
        #on utilise les valeurs max en plafond pour fonction aléatoire, X centreoides créer selon qte cluster requise
        
       # maxValues.fill(topMax)
        
        for i in range(self.nbOfClusters):
            for j in range(len(self.mainWordDict)):
                self.centroidArrayArray[i][j] = random.randrange(topMax)-1
       
        return self.clusterLoop(self.attributeMembership(self.centroidArrayArray))
    
    def clusterFullRandom(self):
        maxValues = []
        maxValues = np.zeros(len(self.mainWordDict))
        self.centroidArrayArray = np.zeros((self.nbOfClusters, len(self.mainWordDict)))
        #on va chercher les valeurs maximales pour chaque mot (en terme de coocurences max)
        for i in range(len(self.mainWordDict)):
            for j in range(len(self.mainWordDict)):
                if maxValues[i] < self.wordMatrix[i][j]:
                    maxValues[i] = self.wordMatrix[i][j]
        #on utilise les valeurs max en plafond pour fonction aléatoire, X centreoides créer selon qte cluster requise
        
               
        for i in range(self.nbOfClusters):
            for j in range(len(maxValues)):
                self.centroidArrayArray[i][j] = random.randrange(maxValues[j]+1)-1
       
        return self.clusterLoop(self.attributeMembership(self.centroidArrayArray))
    
    def clusterFullRandomD(self):
        totalZeroPrevalence = 0
        
        
        #CODE D'ANALYSE DU NOMBRE DE 0 PRESENT DANS LES VECTEURS 
        
        
        #qty1000 =[]
       # qty1000 = np.zeros(50)
        #nbrZero = []
        #nbrZero = np.zeros(len(self.mainWordDict))
       # for i in range(len(self.mainWordDict)):
          #  for j in range(len(self.mainWordDict)):
              #  if 0 == self.wordMatrix[i][j]:
                 #   nbrZero[i] +=1
            #if nbrZero[i] > 10000:
                #totalZeroPrevalence +=1
        
        
        #for i in range(len(self.mainWordDict)):
           # value = int (nbrZero[i] / 1000)
           # qty1000[value] +=1 
        
        #print(totalZeroPrevalence)
       # print(qty1000)
        
        
        
        maxValues = []
        maxValues = np.zeros(len(self.mainWordDict))
        self.centroidArrayArray = np.zeros((self.nbOfClusters, len(self.mainWordDict)))
        #on va chercher les valeurs maximales pour chaque mot (en terme de coocurences max)
        for i in range(len(self.mainWordDict)):
            for j in range(len(self.mainWordDict)):
                if maxValues[i] < self.wordMatrix[i][j]:
                    maxValues[i] = self.wordMatrix[i][j]
        #on utilise les valeurs max en plafond pour fonction aléatoire, X centreoides créer selon qte cluster requise
        
               
        for i in range(self.nbOfClusters):
            for j in range(len(maxValues)):
                randomvalue = random.randrange(100)
                if randomvalue < 90:
                    pass
                elif randomvalue < 98:  
                    self.centroidArrayArray[i][j] = random.randrange(15)
                else:
                    self.centroidArrayArray[i][j] = random.randrange(maxValues[j]+1)-1
       
        return self.clusterLoop(self.attributeMembership(self.centroidArrayArray))


    def dumpPickle(self, list):
        fpath = "Y:\_Oracle_TP\\b62_projet_oracle_tp2\Resultats\Tests Danick\\rsltPickle"
        f = open(fpath, 'wb')
        pickle.dump(list, f)
        f.close()
        
    def loadPickle(self):
        fpath = "Y:\_Oracle_TP\\b62_projet_oracle_tp2\Resultats\Tests Danick\\rsltPickle"
        f = open(fpath, 'rb')
        
        return pickle.load(f)

                    
    def clusterLoop(self, membershipList):
        
        done = False
        loops = 0
        prevMembership = membershipList

        # Comptage et affichage des mots appartenants aux centroides
        for i in range(self.nbOfClusters):
            counter = 0
            for j in range(len(self.wordMatrix)):
                if prevMembership[j] == i:
                    counter += 1
            print("Il y a {} point(s) (mots) regroupe(s) autour du centroide no {}".format(counter, i))
        
        while not done:
            loops += 1
            centroids, counter = self.calculateCentroids(prevMembership)
            newMembership = self.attributeMembership(centroids)
            
            changesList = np.equal(prevMembership, newMembership)
            changesSum = np.sum(changesList)
            changesTotal = len(self.wordMatrix) - changesSum

            print()
            print("="*60)
            print("Iteration {} terminee. {} changements de centroides.\n".format(loops, changesTotal))

            if changesTotal == 0:
                for i in range(self.nbOfClusters):
                    print("Il y a {} point(s) (mots) regroupe(s) autour du centroide no {}".format(counter[i], i))
                
                print()
                print("=" * 60)
                
                return centroids, prevMembership
                # done = True
                
            else:
                prevMembership = newMembership

                # Comptage et affichage des mots appartenants aux centroides
                for i in range(self.nbOfClusters):
                    print("Il y a {} point(s) (mots) regroupe(s) autour du centroide no {}".format(counter[i], i))
                
    def printClusterResults(self, centroides, membership):

        # Creation de la liste de listes qui contiendra les mots et leurs scores dans leur centroides respectifs
        list = []
        for i in range(self.nbOfClusters):
            list.append([])

        for word, i in self.mainWordDict.items():
            iCluster = int(membership[i])
            score = self.analyzer.leastSquare(self.wordMatrix[i], centroides[iCluster])
            list[iCluster].append((word, score))
        
        i = 0    
        for cluster in list:
            cluster = self.analyzer.sortResults(cluster, 0)
            print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print("Groupe: {}\n".format(i))
            
            for t in cluster[:10]:
                word, score = t
                print("{} --> {}".format(word, score))
            i += 1
        
        print()
        print("=" * 60)

    def calculateCentroids(self, membership):
        centroids = np.zeros((self.nbOfClusters, len(self.wordMatrix)))
        counter = np.zeros((self.nbOfClusters))
        #print("membership len")
        #print(len(membership))
        
        for i in range(len(self.wordMatrix)):
            n = int(membership[i])
            #print(i)
            #print(self.wordMatrix[i])
            #print(n)
            centroids[n] += self.wordMatrix[i]
            counter[n] += 1
            
        for i in range(len(centroids)):
            if counter[i] > 0:
                centroids[i] = centroids[i] / counter[i]
                
        return centroids, counter
    
    def attributeMembership(self, centroids):
        
        membership = np.zeros((len(self.wordMatrix)))
        
        for i in range(len(self.wordMatrix)):
            temp = {}
            
            for n in range(len(centroids)):
                temp[n] = self.analyzer.leastSquare(self.wordMatrix[i], centroids[n])
                
            membership[i] = min(temp, key=temp.get)
            
        return membership
