"""
------------------------------------------------------------------
File name:  main.py
Creation:   14/02/19
Author:     Jean-Charles Bertrand
            Jean-François Lessard
            Danick Massicotte
------------------------------------------------------------------
Context:    Travail pratique 2 - B62-Projet Oracle
------------------------------------------------------------------
Brief:      Logiciel qui permet de trouver des mots
            sémantiquement semblables à l'aide de
            l'apprentissage machine
------------------------------------------------------------------
"""

import sys
import getopt
from trainer import Trainer
from searcher import Searcher
from clusterer import Clusterer
from DBManager import DBManager


def main():

    # Lecture des arguments passés en ligne de commandes
    try:
        opts, args = getopt.getopt(sys.argv[1:], "et:rcn:s", ["enc=", "chemin=", "nc=", "mots="])
    except getopt.GetoptError as err:
        print(err)
        sys.exit()

    task = None
    clusterWordList = []

    # Mise en mémoire des aruments passés en ligne de commandes
    for opt, arg in opts:
        if opt == '-e':
            task = 'training'
        elif opt == '-t':
            if arg.isnumeric():
                windowSize = arg
            else:
                print("Erreur! Taille de la fenêtre!")
                sys.exit(1)
        elif opt == '-r':
            task = 'search'
        elif opt == '-c':
            task = 'clustering'
        elif opt == '-n':
            if arg.isnumeric():
                wordQty = arg
            else:
                print("Erreur! Nombre de mots à afficher par centroïdes!")
                sys.exit(1)
        elif opt == '-s':
            task = 'table'
        elif opt == '--enc':
            fileEncoding = arg
        elif opt == '--chemin':
            filePath = arg
        elif opt == '--nc':
            if arg.isnumeric():
                clusteringType = 'random'
                clusterQty = arg
            else:
                print("Erreur! Nombre de centroïdes à afficher!")
                sys.exit(1)
        elif opt == '--mots':
            clusteringType = 'words'
            clusterWordList = arg.split(" ")
            clusterQty = len(clusterWordList)

    if task == 'training':
        trainer = Trainer(filePath, fileEncoding, windowSize)
        trainer.execute()

    elif task == 'search':
        try:
            searcher = Searcher(windowSize)
            if searcher.isWindowValid:
                searcher.execute()
            else:
                print("Aucune donnée pour la taille de fenêtre {}".format(windowSize))
        except:
            print("Erreur! Base de données inexistante!")
            
    elif task == 'clustering':
        clusterer = Clusterer(windowSize, wordQty, clusterWordList, clusterQty, clusteringType)

        if clusterer.isWindowValid:
            clusterer.execute()
        else:
            print("Aucune donnée pour la taille de fenêtre {}".format(windowSize))

    elif task == 'table':
        db = DBManager()
        print("Création de Dictionnaire_Commun")
        db.createTableDict()
        print("Création de Cooccurrences")
        db.createTableCooc()
        print("Fermeture de la connexion")
        db.closeConnection()

    else:
        print("Erreur! Arguments -e, -r ou -c introuvables")
        sys.exit()

    print("\nFin du programme")

    return 0

    
if __name__ == '__main__':
    sys.exit(main())
