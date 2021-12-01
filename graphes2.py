import operator
import copy
import pandas as pd
import numpy as np
import re

# -------- MULTIGRAPH -------- #

class Multigraph:

	def __init__(self, n, m, vertices, edges):
		
		self.n = n # number of vertices
		self.m = m # number of edges
		self.vertices = vertices # list of strings
		self.edges = edges # list of tuples: (u, v, t, lambda)

	def afficheMultigraphe(self):
		print("\nMultigraph de " + str(self.n) + " sommets et " + str(self.m) + " arcs :")
		print("\tListe de sommets : " + str(self.vertices) )
		print("\tListe d'arcs : " + str(self.edges) + "\n" )


def acquisitionMultigraphe(nomFichier):
	"""
	Méthode permettant d'acquérir un multigraphe G (modelisation : structure Multigraph) depuis un fichier texte
	
	nomFichier : chaine de caractéres representant un fichier texte d'extension .txt
	"""
	lignes = []
	vertices = []
	edges = []
	
	with open(nomFichier, 'r') as fichier:
		lignes = fichier.readlines()
		
	n = int(lignes[0])
	m = int(lignes[1])
	
	for i in range(2, len(lignes)):
		r = re.compile("^[(][\w]*[,][\w]*[,][0-9]*[,][0-9]*[)]\n*$")
		if r.match(lignes[i]) is not None:
			edges.append(lignes[i].split("\n")[0])
		else :
			vertices.append(lignes[i].split("\n")[0])

	if len(vertices) != n or len(edges) != m :
		return None
		
	return Multigraph(n, m, vertices, edges)




def transformationMultigraphe(multiG, verbose = False):
	"""
	Méthode permettant de transformer un multigraphe G pondéré par le temps en un graphe G' classique

	multiG : multigraphe pondéré par le temps, structure Multigraph
	verbose : mettre à True pour visualiser le détail du déroulement de cet algorithme
	"""
	vIN = []
	vOUT = []
	for arc in multiG.edges :
		x = arc.split("(")[1].split(")")[0].split(",")

		# vIN(sommet multiGraphe) = liste de doublets (v, t) avec v = sommet multiGraphe et t = poids (date) de l'arc entrant de v + lambda
		newSommet = (x[1], int(x[2])+int(x[3]))
		if newSommet not in vIN:
			vIN.append(newSommet)

		# vOUT(sommet multiGraphe) = liste de doublets (v, t) avec v = sommet multiGraphe et t = poids (date) de l'arc sortant de v
		newSommet = (x[0], int(x[2]))
		if newSommet not in vOUT:
			vOUT.append(newSommet)

	# ensV = union des ensembles vIN et vOUT
	ensV = vIN + vOUT
	# print("TEST env original ", ensV)
	ensV.sort(key = operator.itemgetter(0, 1), reverse=False)
	# print("TEST ensV sorted =" , ensV)

	# Construction de la matrice d'adjacence matG[source][destination] du graphe G issu du multigraphe multiG
	# Initialisation de toutes les cases à -1 qui signifie "aucun arc entre les sommets"
	matG = np.full((len(ensV), len(ensV)), -1)

	ensE = []
	# Ajout des arcs du sommet source au sommet destination de poids 0
	ensV_copy = copy.deepcopy(ensV)
	prec = None
	while (len(ensV_copy) > 0):
		sommetEnsV = ensV_copy.pop(0)
		if (prec != None and prec[0] == sommetEnsV[0]) :
			indexSource = ensV.index(prec)
			indexDest = ensV.index(sommetEnsV)
			matG[indexSource][indexDest] = 0
			ensE.append(prec,sommetEnsV)

			if verbose :
				print("Ajout d'un arc de poids 0 entre ", prec, "et", sommetEnsV)

		prec = sommetEnsV


	# Ajout des arcs du sommet source au sommet destination de poids lambda
	for arc in multiG.edges :
		x = arc.split("(")[1].split(")")[0].split(",")
		source = (x[0], int(x[2]))
		dest = (x[1], int(x[2])+int(x[3]))
		matG[ensV.index(source)][ensV.index(dest)] = int(x[3])
		ensE.append(source,dest)

		if verbose :
			print("Ajout d'un arc de poids lambda entre ", source, "et", dest)

	if verbose :
		affichageMatG(matG, ensV)

	return ensV, ensE, matG


def affichageMatG(matG, ensV):
	df = pd.DataFrame(matG, index = ensV, columns = ensV)
	print("\nMatrice d'adjacence rélative au graphe classique G' obtenu par transformation du multigraphe pondéré par le temps G")
	print("NB. Les symboles '-' qui figurent sont en réalité des -1 dans la matrice, ils servent seulement à favoriser la lisibilité\n")
	df[df==-1] = "-"
	print(df, "\n")


def existeChemin(indiceSourceX, indiceDestY, matG):
	return


def earliest_arrival(x, y, matG, ensV, verbose = False):
	"""
	Returns the path from x to y which arrives the earliest.

	matG : graphe G’=(V,E) traduisant un multigraphe pondéré par le temps
	ensV : liste de sommets de G' (doublets)
	x : sommet source dans le multigraphe pondéré par le temps
	y : sommet destination dans le multigraphe pondéré par le temps
	"""

	# Instanciation d'une liste listeY avec les noeuds contenant y dans leur étiquette classés par ordre de t croissant
	listeY = []
	listeX = []
	for sommet in ensV:
		if sommet[1] == y :
			listeY.append(sommet)
		if sommet[0] == x :
			listeX.append(ensV.index(sommet))

	listeY.sort(key = operator.itemgetter(1), reverse=False)

	if verbose :
		print("listeY = liste des noeuds contenant y dans leur étiquette triée par t croissant:", listeY)
		print("listeX = liste des noeuds contenant x dans leur étiquette :", listeX)

	# pour chaque sommet dans la liste l, vérifier s' il existe un chemin de x à y en remontant le sens des arcs de G’.
	# Pendant cette recherche, les noeuds rejoint par un arc de poids = 0 ne sont pas retenus dans la solution
	# L’algorithme s'arrête au premier chemin de x à y trouvé
	for s1 in listeY:
		for s2 in listeX :
			path = existeChemin(s2, [ensV.index(s1)], matG)
			if path != None :

				if verbose:
					print("Chemin d’arrivée au plus tôt de x à y :", path)

				return path

	if verbose:
		print("Il n'existe aucun chemin de x à y")
	
	return None
	

def latest_departure(x, y, matG, verbose):
	"""
	x : sommet source dans le multigraphe pondéré par le temps
	y : sommet destination dans le multigraphe pondéré par le temps
	"""
	# Algorithme II : chemin de départ au plus tard
	# Entrée : un graphe G’=(V,E) traduisant un multigraphe pondéré par le temps, une source x, une destination y
	# Déroulement :
	# instancier une liste L avec les noeuds contenant x dans leur étiquette classés par ordre de t décroissant
	# pour chaque sommet dans la liste L, vérifier s' il existe un chemin de x à y en suivant le sens des arcs de G’. Pendant cette recherche, les noeuds rejoint par un arc de poids = 0 ne sont pas retenus dans la solution
	# l’algorithme s'arrête au premier chemin de x à y trouvé
	# Sortie : si il existe un chemin de x à y, alors ceci est un chemin de départ au plus tard de x à y ; sinon, il n’existe pas de chemin de x à y.
	path = []

	return path

def fastest(x, y, matG, verbose):
	"""
	x : sommet source dans le multigraphe pondéré par le temps
	y : sommet destination dans le multigraphe pondéré par le temps
	"""
	# Algorithme III : chemin le plus rapide
	# Entrée : un graphe G’=(V,E) traduisant un multigraphe pondéré par le temps, une source x, une destination y
	# Déroulement :
	# instancier une liste L avec des doublets (noeudX, noeudY), dont noeudX est le noeud contenant x dans son étiquette et noeudY est le noeud contenant y dans son étiquette, classés par ordre de [ t(y) - t(x) ] croissant
	# supprimer de G’ les arcs de poids = 0 adjacents aux noeudX et noeudY. Cela permet d’imposer que la première et la dernière arête empruntées par tout chemin possible aient un poids > 0.
	# pour chaque doublet dans la liste L, vérifier s' il existe un chemin de noeudX à noeudY en suivant le sens des arcs de G’. Pendant cette recherche, les noeuds rejoint par un arc de poids = 0 ne sont pas retenus dans la solution
	# l’algorithme s'arrête au premier chemin de x à y trouvé
	# Sortie : si il existe un chemin de noeudX  à noeudY, alors ceci est le chemin le plus rapide de x à y ; sinon, il n’existe pas de chemin de x à y.

	path = []

	return path

def shortest(x, y, matG, verbose):
	"""
	x : sommet source dans le multigraphe pondéré par le temps
	y : sommet destination dans le multigraphe pondéré par le temps
	"""
	# Algorithme IV : plus court chemin
	# Entrée : un graphe G’=(V,E) traduisant un multigraphe pondéré par le temps, une source x, une destination y
	# Déroulement :
	# déterminer noeudX = le noeud contenant x dans son étiquette avec t minimal.
	# calculer un chemin de coût minimal dans G’ qui part du noeudX et termine dans un nœud contenant y dans son étiquette. Pour cela, mémoriser la somme des poids des arcs pour chaque chemin trouvé, et retourner le chemin ayant la plus petite valeur de somme. Pendant cette recherche, les noeuds rejoint par un arc de poids = 0 ne sont pas retenus dans la solution
	# Sortie : si il existe un chemin de x à y, alors ceci est un plus court chemin de x à y ; sinon, il n’existe pas de chemin de x à y.
	path = []

	return path









#-----------------------------------------------------------

g = acquisitionMultigraphe("multigrapheG1.txt")

if g != None :
	g.afficheMultigraphe()

transformationMultigraphe(g, True)