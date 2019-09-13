# B62_Projet_Oracle_TP3
## Objectif
Partitionnement des données l'aide de centroïdes (Centroid-based data clustering)
## Auteurs
Jean-Charles Bertrand

Jean-François Lessard

Danick Massicotte
## Options de ligne de commande
-c : clustering

-e : entraînement

-r : recherche

-t <taille> : taille de fenêtre. <taille> doit suivre -t, précédé d'un espace

-n <nombre>: nombre de mots à afficher par cluster (à la fin de l'exécution)

--nc <nombre> : nombre de centroïdes, une valeur entière

--mots <"mot1 mot2 mot3">: liste de <nombre> mots qui serviront de centroïdes initiaux

--enc <encodage> : encodage de fichier. <encodage> doit suivre --enc, précédé d'un espace.

--chemin <chemin> : chemin du corpus d'entrainement. <chemin> doit suivre --chemin, précédé d'un espace.

## Utilisation
Exemple de partionnement des données à l'aide de centroïdes (Méthode explicite):
```python
main.py -c -t 7 -n 10 --mots "mot1 mot2 mot3"
```
Exemple de partionnement des données à l'aide de centroïdes (Méthode aléatoire):
```python
main.py -c -t 7 -n 10 --nc 5
```
Exemple de ligne de commande pour l'entraînement d'un texte:
```python
main.py -e -t 7 --enc UTF-8 --chemin Y:\b62_projet_oracle_tp2\LeVentreDeParisUTF8.txt
```
Exemple de ligne de commande pour la recherche de résultats:
```python
main.py -r -t 7
```
## Base de données
La base de données SQLite est déjà intégrée au projet. Elle contient la matrice de cooccurrences
des mots des textes GerminalUTF8.txt, LesTroisMousquetairesUTF8.txt et LeVentreDeParis.txt.
Les tailles de fenêtre 5 à 8 lors de l'entraînement sont disponible dans la base de données...

##TEST code alternatif (tests hypothese)
Afin d'executer le code des hypothese sur la création de centroïdes, il faut modifier la fonction execute du clusterer. Des indication s'y trouvent. (essentiellement on met en commentaire et retire des commentaire la ligne de code correspondante


