####################################################################################################################
#	IMPORTS
####################################################################################################################

import operator
import copy
import pandas as pd
import numpy as np
import re



####################################################################################################################
#	STRUCTURES
####################################################################################################################

class Multigraph:

	def __init__(self, n, m, vertices, edges):
		
		self.n = n # number of vertices
		self.m = m # number of edges
		self.vertices = vertices # list of strings
		self.edges = edges # list of tuples: (u, v, t, lambda)

	def transform_to_graph(self, verbose=False):
		"""
		Returns a simple graph.
		"""

		newVertices = {} # {original_vertex : list of new vertices}
		newEdges = []

		for vertex in self.vertices:
			newVertices[vertex] = []

		for source, dest, t, weight in self.edges :

			# vOUT(sommet multiGraphe) = liste de doublets (v, t) avec v = sommet multiGraphe et t = poids (date) de l'arc sortant de v
			u = (source, t)
			if u not in newVertices[source]:
				newVertices[source].append(u)

			# vIN(sommet multiGraphe) = liste de doublets (v, t) avec v = sommet multiGraphe et t = poids (date) de l'arc entrant de v + lambda
			v = (dest, t + weight)
			if v not in newVertices[dest]:
				newVertices[dest].append(v)

			e = (u, v, weight)
			newEdges.append(e)

		for v in newVertices.keys(): # v: name of original vertex

			# vertices are sorted by t
			newVertices[v].sort(key = operator.itemgetter(1), reverse = False)

			# arcs with weight = 0 are created between vertices with the same name
			to_visit = newVertices[v]
			for i in range(len(to_visit)-1):
				e = (to_visit[i], to_visit[i+1], 0)
				newEdges.append(e)

		return Graph(self.n, self.m, newVertices, newEdges, verbose)

	def afficheMultigraphe(self):
		print("\nMultigraph de " + str(self.n) + " sommets et " + str(self.m) + " arcs :")
		print("\tListe de sommets : " + str(self.vertices) )
		print("\tListe d'arcs : " + str(self.edges) + "\n" )

#-------------------------------------------------------------------------------------------------------------------

class Graph:

	def __init__(self, n, m, vertices, edges, verbose=False):
		
		self.n = n # number of vertices
		self.m = m # number of edges
		self.vertices = vertices # dictionary with key: original vertex, and value: list of new vertices (name, time) sorted by time
		self.edges = edges # list of tuples (u, v, weight), with u and v: tuples (name, time)
		self.adjacency_list = self.__obtain_adjacency_list(vertices, edges, verbose) # dictionary

	def __obtain_adjacency_list(self, vertices, edges, verbose=False):
		"""
		Returns an adjacency list (dictionary).
		"""

		# Construction de adjacency_list[key=source][val=destination, poids] (dictionnaire)
		adjacency_list = {}

		# Initialisation
		for l in vertices.values():
			for s in l:
				adjacency_list[s] = []

		for source, dest, weight in edges :
			adjacency_list[source].append((dest, weight))

		if verbose:
			print("\nListe d'adjacence :", adjacency_list)

		return adjacency_list

	def BFS(self, x, y, interval, verbose=False):
		"""
		Returns the <<<<<arbre couvrant>>>>>> from x to y.

		y : liste de destinations
		"""

		traceback = {} # Dictionnaire clé = successeur du pere (fils) : value = pere

		racine = None
		for v in self.vertices[x]:
			if v[1] >= interval[0]:
				racine = v # sommet source contenant l'etiquette x et la plus petite date
				break
		
		if racine == None:
			print("Aucun arbre couvrant possible entre x et y dans l'intervalle selectionné")
			return None

		print(racine)
		destinations = self.vertices[y] # liste des destinations contenant l'etiquette y
		print(destinations)

		f = [racine]	# Initialisation de la file avec le sommet source x
		sommetsVisites = [racine] # Initialisation de la liste de sommets dejà visités avec le sommet source x
		traceback[racine] = None

		while (len(f) > 0):
			print("\nNouvelle ite - etat file :", f)
			sommetATraiter = f.pop(0)
			print("Sommet à traiter :", sommetATraiter)
			if sommetATraiter in self.adjacency_list.keys():
				for successeur, _ in self.adjacency_list[sommetATraiter]:
					print("\tSuccesseur :", successeur)
					if successeur not in sommetsVisites:
						sommetsVisites.append(successeur)
						print("Sommets visites =", sommetsVisites)
						f.append(successeur)
						traceback[(successeur)] = sommetATraiter

		#if len(sommetsVisites) != len(sommetsFermes):
			#return "Erreur algorithme BFS"
		print("traceback :", traceback)
		return traceback	



####################################################################################################################
#	OUTILS
####################################################################################################################

def acquisitionMultigraphe(nomFichier):
	"""
	Méthode permettant d'acquérir un multigraphe G (modelisation : structure Multigraph) depuis un fichier texte
	
	nomFichier : chaine de caractéres representant un fichier texte d'extension .txt
	"""
	lignes = []
	vertices = []
	edges = []
	
	try:
		with open(nomFichier, 'r') as fichier:
			lignes = fichier.readlines()
	except:
		print("Erreur : fichier non trouvé")
		return None
	
	
	n = int(lignes[0])
	m = int(lignes[1])
	
	for i in range(2, len(lignes)):
		r = re.compile("^[(][\w]*[,][\w]*[,][0-9]*[,][0-9]*[)]\n*$")
		if r.match(lignes[i]) is not None:
			# format d'un arc : (source, dest, int(time), int(weight))
			e = lignes[i].split("(")[1].split(")")[0].split(",")
			edges.append((e[0], e[1], int(e[2]), int(e[3])))
			print((e[0], e[1], int(e[2]), int(e[3])))
		else :
			vertices.append(lignes[i].split("\n")[0])

	if len(vertices) != n or len(edges) != m :
		return None
		
	return Multigraph(n, m, vertices, edges)

#-------------------------------------------------------------------------------------------------------------------

def transformationMultigrapheListeAdjacence(multiG, verbose = False):
	"""
	Méthode permettant de transformer un multigraphe G pondéré par le temps en un graphe G' classique (modelisation : liste d'adjacence)

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
	ensV.sort(key = operator.itemgetter(0, 1), reverse=False)

	# Construction de la liste d'adjacence listeAdj[key=source][val=destination, poids] (dictionnaire) du graphe G issu du multigraphe multiG
	ensE = []
	listeAdj = {}

	# Ajout des arcs du sommet source au sommet destination de poids 0
	ensV_copy = copy.deepcopy(ensV)
	prec = None
	while (len(ensV_copy) > 0):
		sommetEnsV = ensV_copy.pop(0)
		listeAdj[sommetEnsV] = []
		if (prec != None and prec[0] == sommetEnsV[0]) :
			ensE.append((prec,sommetEnsV, 0))
			listeAdj[prec].append((sommetEnsV, 0))

			if verbose :
				print("Ajout d'un arc de poids 0 entre ", prec, "et", sommetEnsV)

		prec = sommetEnsV

	# Ajout des arcs du sommet source au sommet destination de poids lambda
	for arc in multiG.edges :
		x = arc.split("(")[1].split(")")[0].split(",")
		source = (x[0], int(x[2]))
		dest = (x[1], int(x[2])+int(x[3]))
		ensE.append((source,dest,int(x[3])))
		listeAdj[source].append((dest, int(x[3])))

		if verbose :
			print("Ajout d'un arc de poids lambda entre ", source, "et", dest)

	if verbose :
		print("\nListe d'adjacence :", listeAdj)

	return listeAdj

#-------------------------------------------------------------------------------------------------------------------

def transformationMultigrapheMatAdjacence(multiG, verbose = False):
	"""
	Méthode permettant de transformer un multigraphe G pondéré par le temps en un graphe G' classique (modelisation : matrice d'adjacence)

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
	ensV.sort(key = operator.itemgetter(0, 1), reverse=False)

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
			ensE.append((prec,sommetEnsV, 0))

			if verbose :
				print("Ajout d'un arc de poids 0 entre ", prec, "et", sommetEnsV)

		prec = sommetEnsV

	# Ajout des arcs du sommet source au sommet destination de poids lambda
	for arc in multiG.edges :
		x = arc.split("(")[1].split(")")[0].split(",")
		source = (x[0], int(x[2]))
		dest = (x[1], int(x[2])+int(x[3]))
		matG[ensV.index(source)][ensV.index(dest)] = int(x[3])
		ensE.append((source,dest,int(x[3])))

		if verbose :
			print("Ajout d'un arc de poids lambda entre ", source, "et", dest)

	if verbose :
		affichageMatG(matG, ensV)
		print("\nListe des sommets :", ensV)
		print("\nListe des arcs :", ensE)

	return ensV, ensE, matG

#-------------------------------------------------------------------------------------------------------------------

def affichageMatG(matG, ensV):
	df = pd.DataFrame(matG, index = ensV, columns = ensV)
	print("\nMatrice d'adjacence rélative au graphe classique G' obtenu par transformation du multigraphe pondéré par le temps G")
	print("NB. Les symboles '-' qui figurent sont en réalité des -1 dans la matrice, ils servent seulement à favoriser la lisibilité\n")
	df[df==-1] = "-"
	print(df, "\n")

#-------------------------------------------------------------------------------------------------------------------

def traceback(x, y, verbose):

	fils = y
	pere = traceback[y]
	path = [y]
	while (pere != None):
		path.append(pere)
		fils = pere
		pere = traceback[fils]
	
	path.reverse()

	if verbose:
		print("\nRésultat BFS(x =", x, ", y =", y, ") :", path)


####################################################################################################################
#	CHEMINS
####################################################################################################################

def earliest_arrival(x, y, g, verbose=False): # <-------------------------- commnentaire à effacer : remplacer g par self ; interval gere par arbre couvrante
	"""
	Returns the path from x to y which arrives the earliest.

	lAdj : graphe G’=(V,E) traduisant un multigraphe pondéré par le temps
	x : sommet source dans le multigraphe pondéré par le temps
	y : sommet destination dans le multigraphe pondéré par le temps
	"""
	listeX = g.vertices[x].reverse()  # <-------------------------- est ce que cela est une bonne idee our eviter les doublons de passages par x1, x2, x3...?
	listeY = g.vertices[y]
	if verbose :
		print("Liste des noeuds contenant y dans leur étiquette triée par t croissant:", listeY)
		print("Liste des noeuds contenant x dans leur étiquette :", listeX)

	# Pour chaque sommet dans la liste l, vérifier s' il existe un chemin de x à y en remontant le sens des arcs de G’.
	# Pendant cette recherche, les noeuds rejoint par un arc de poids = 0 ne sont pas retenus dans la solution
	# L’algorithme s'arrête au premier chemin de x à y trouvé
	for sY in g.vertices[y]:
		for sX in g.vertices[x]:
			path = traceback(sX, sY, verbose)
			if path != None:
				if verbose:
					print("Chemin d’arrivée au plus tôt de x à y :", path)
				return path

	if verbose:
		print("Il n'existe aucun chemin de x à y")	
	return None

#-------------------------------------------------------------------------------------------------------------------

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

#-------------------------------------------------------------------------------------------------------------------

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

#-------------------------------------------------------------------------------------------------------------------

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

#-------------------------------------------------------------------------------------------------------------------








####################################################################################################################
#	TESTS DEBUG
####################################################################################################################

mg = acquisitionMultigraphe("multigrapheG1.txt")

if mg != None :
	mg.afficheMultigraphe()
print("------------------------------------------------------------------")

#transformationMultigrapheMatAdjacence(g, verbose = False)
#print("------------------------------------------------------------------")

#listeAdj = transformationMultigrapheListeAdjacence(g, verbose = False)
#print("------------------------------------------------------------------")

g = mg.transform_to_graph(True)
print(g.adjacency_list)
print("------------------------------------------------------------------")

g.BFS("a", "g", [3, 10], True)
#print("------------------------------------------------------------------")


#earliest_arrival('a', 'g', listeAdj, verbose = True)