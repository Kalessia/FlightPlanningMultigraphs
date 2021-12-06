####################################################################################################################
#	IMPORTS
####################################################################################################################

import operator
import copy
from numpy.lib.type_check import _nan_to_num_dispatcher
import pandas as pd
import numpy as np
import re
from IPython.display import Image


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

	def printMultigraphe(self):
		print("\nMultigraph de " + str(self.n) + " sommets et " + str(self.m) + " arcs :")
		print("\tListe de sommets : " + str(self.vertices) )
		print("\tListe d'arcs : " + str(self.edges) + "\n" )



	# Méthode permettant d'afficher à l'écran un multigraphe orienté et, éventuellement, un titre
	def showMultigraphe(self, title = "Multi"):
		""" G : un dictionnaire representant un graphe { sommet s : sommets adjacents à s}
		    titre : titre du graphe à afficher, 'G' par defaut
		"""

		newG = nx.MultiGraph()
		newG.add_nodes_from(self.vertices)

		for source, dest, t, w in self.edges:
			newG.add_edge(source, dest, weight=t)

		plt.title(title)
		pos = nx.circular_layout(newG)
		e_labels = nx.get_edge_attributes(newG, 'weight')
		nx.draw_networkx_edge_labels(newG, pos=pos, edge_labels=e_labels)
		nx.draw(newG, with_labels=True, node_size=1500, pos=pos)

		toPdot = nx.drawing.nx_pydot.to_pydot
		pdot = toPdot(newG)
		pdot.write_png("Multigraph.png")

		plt.show()




#-------------------------------------------------------------------------------------------------------------------

class Graph:

	def __init__(self, n, m, vertices, edges, verbose=False):
		
		self.n = n # number of vertices
		self.m = m # number of edges
		self.vertices = vertices # dictionary with key: original vertex, and value: list of new vertices (name, time) sorted by time
		self.edges = edges # list of tuples (u, v, weight), with u and v: tuples (name, time)
		self.adjacency_list = self.__obtain_adjacency_list(vertices, edges, verbose) # dictionary
		self.arbreCouvrante = None

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

		arbreCouvrante = {} # Dictionnaire clé = successeur du pere (fils) : value = pere

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
		arbreCouvrante[racine] = None

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
						arbreCouvrante[(successeur)] = sommetATraiter

		#if len(sommetsVisites) != len(sommetsFermes):
			#return "Erreur algorithme BFS"
		print("arbreCouvrante :", arbreCouvrante)
		self.arbreCouvrante = arbreCouvrante # dictionnaire
		return arbreCouvrante


	# Méthode permettant d'afficher à l'écran un graphe orienté et, éventuellement, un titre
	def showGraphe(self, titre = "G"):
		# """ G : un dictionnaire representant un graphe { sommet s : sommets adjacents à s}
		#     titre : titre du graphe à afficher, 'G' par defaut
		# """
		newG = nx.DiGraph()
		listeSommetsG = list(self.adjacency_list.keys())
		newG.add_nodes_from(listeSommetsG)

		for source in listeSommetsG:
			for dest , w in self.adjacency_list[source]:
				newG.add_edge(source, dest, weight=w)

		plt.title(titre)
		pos = nx.circular_layout(newG)
		e_labels = nx.get_edge_attributes(newG,'weight')
		nx.draw_networkx_edge_labels(newG, pos=pos, edge_labels=e_labels)
		nx.draw(newG, with_labels=True, node_size=1500, pos=pos)

		toPdot = nx.drawing.nx_pydot.to_pydot
		pdot = toPdot(newG)
		pdot.write_png("Graphe.png")

		plt.show()   




	def showGrapheCouvrant(self, titre = "G Couvrant"):
		# """ G : un dictionnaire representant un graphe { sommet s : sommets adjacents à s}
		#     titre : titre du graphe à afficher, 'G' par defaut
		# """
		newG = nx.DiGraph()
		listeSommetsG = list(self.arbreCouvrante.keys())
		newG.add_nodes_from(listeSommetsG)

		for successeur in self.arbreCouvrante.keys():
			if self.arbreCouvrante[successeur] == None:
				continue
			else:
				newG.add_edge(self.arbreCouvrante[successeur], successeur)

		plt.title(titre)
		nx.draw(newG, with_labels=True, node_size=1500, node_color="skyblue")

		toPdot = nx.drawing.nx_pydot.to_pydot
		pdot = toPdot(newG)
		pdot.write_png("Multigraphe.png")

		plt.show()   


	def traceback(self, sX, sY, verbose):

		print("test traceback : sX, sY", sX, sY)
		if sX == None or sY == None:
			return None
		
		if sX not in g.arbreCouvrante.keys() or sY not in g.arbreCouvrante.keys() :
			return None

		if sX == sY:
			if verbose:
				print("\nRésultat traceback(x =", sX, ", y =", sY, ") :", [sX])
			return [sX]

		fils = sY
		pere = self.arbreCouvrante[sY]
		path = [sY]
		while (pere != None or pere != sX):
			path.append(pere)
			print ("test : pere, fils, path :", pere, fils, path)
			fils = pere
			pere = self.arbreCouvrante[fils]
		
		path.reverse()

		if pere != sX:
			return None

		if verbose:
			print("\nRésultat traceback(x =", sX, ", y =", sY, ") :", path)

		return path




# def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):

#     '''
#     From Joel's answer at https://stackoverflow.com/a/29597209/2966723 

#     If the graph is a tree this will return the positions to plot this in a 
#     hierarchical layout.

#     G: the graph (must be a tree)

#     root: the root node of current branch 
#     - if the tree is directed and this is not given, the root will be found and used
#     - if the tree is directed and this is given, then the positions will be just for the descendants of this node.
#     - if the tree is undirected and not given, then a random choice will be used.

#     width: horizontal space allocated for this branch - avoids overlap with other branches

#     vert_gap: gap between levels of hierarchy

#     vert_loc: vertical location of root

#     xcenter: horizontal location of root
#     '''
#     if not nx.is_tree(G):
#         raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

#     if root is None:
#         if isinstance(G, nx.DiGraph):
#             root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
#         else:
#             root = random.choice(list(G.nodes))

#     def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
#         '''
#         see hierarchy_pos docstring for most arguments

#         pos: a dict saying where all nodes go if they have been assigned
#         parent: parent of this branch. - only affects it if non-directed

#         '''

#         if pos is None:
#             pos = {root:(xcenter,vert_loc)}
#         else:
#             pos[root] = (xcenter, vert_loc)
#         children = list(G.neighbors(root))
#         if not isinstance(G, nx.DiGraph) and parent is not None:
#             children.remove(parent)  
#         if len(children)!=0:
#             dx = width/len(children) 
#             nextx = xcenter - width/2 - dx/2
#             for child in children:
#                 nextx += dx
#                 pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap, 
#                                     vert_loc = vert_loc-vert_gap, xcenter=nextx,
#                                     pos=pos, parent = root)
#         return pos


#     return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)


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



####################################################################################################################
#	CHEMINS
####################################################################################################################

def earliest_arrival(x, y, g, verbose=False): # <-------------------------- commnentaire à effacer : remplacer g par self ; interval gere par arbre couvrante
	"""
	Returns the path from x to y which arrives the earliest.

	x : sommet source dans le multigraphe pondéré par le temps
	y : sommet destination dans le multigraphe pondéré par le temps
	"""
	listeX = list(reversed(g.vertices[x]))  # <-------------------------- est ce que cela est une bonne idee our eviter les doublons de passages par x1, x2, x3...?
	listeY = g.vertices[y]

	if verbose :
		print("Liste des noeuds contenant y dans leur étiquette triée par t croissant:", listeY)
		print("Liste des noeuds contenant x dans leur étiquette :", listeX)

	# Pour chaque sommet dans la liste listeY, vérifier s' il existe un chemin de x à y en remontant le sens des arcs de G’.
	# L’algorithme s'arrête au premier chemin de x à y trouvé
	sX = None
	sY = None
	for sY in listeY:
		for sX in listeX:
			path = g.traceback(sX, sY, verbose) # sX est une liste de noeuds, sY est le sommet contenant y dans l'etiquette pas encore testé avec t minimale
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


####################################################################################################################
#	AFFICHAGE COURBES et GRAPHES
####################################################################################################################

import networkx as nx
import matplotlib.pyplot as plt
import time
import datetime



#------------------------------------------------------------------------------------------------------

# Méthode permettant d'afficher un graphique de comparaison des performances ("temps de calcul" et "qualité des Solutions") de l'algorithme choisi
def plotPerformances(maxN, maxM, maxInterval_dates, nbTests, nbIterations, x, y, interval, verbose = False, save = False):
	"""
	"""
	
	ordonnee_tGlobal = []  # liste des temps de calcul moyen, vue globale sur le programme
	ordonnee_tInit = []  # liste des temps de calcul moyen, vue sur l'initialisation (transformation en graphe + calcul d'arbre couvrant)
	ordonnee_tType1 = []  # liste des temps de calcul moyen, vue sur l'algorithme de type1
	ordonnee_tType2 = []  # liste des temps de calcul moyen, vue sur l'algorithme de type2
	ordonnee_tType3 = []  # liste des temps de calcul moyen, vue sur l'algorithme de type3
	ordonnee_tType4 = []  # liste des temps de calcul moyen, vue sur l'algorithme de type4
	 
	abscisse_n = []
	abscisse_m = []
	abscisse_interval_dates = []


	for nb in range(nbTests):

		n = int(maxN/nbTests*nb)
		m = int(maxM/nbTests*nb)
		interval_dates = [ int(maxInterval_dates[0]/nbTests*nb), int(maxInterval_dates[1]/nbTests*nb) ]

		abscisse_n.append(n)
		abscisse_m.append(m)
		abscisse_interval_dates.append(interval_dates)

		# Méthode permettant de générer des graphes aléatoires
		init_tStart = time.time() # init = initialisation programme = transformation en graphe + calcul d'arbre couvrant
		mg = randomMultigraphe(n, m, probM, interval_dates)
		g = mg.transform_to_graph()
		g.BFS(x, y, interval)
		init_tEnd = time.time()
		ordonnee_tInit.append(init_tEnd - init_tStart)

		tGlobal = []
		tInit = []
		tType1 = []
		tType2 = []
		tType3 = []
		tType4 = []


		for ite in range(nbIterations):

			global_tStart = time.time() # global = temps d'execution du programme entier = initialisation + calcul chemins
			
			type1_tStart = time.time()
			g.earliest_arrival()
			type1_tEnd = time.time()

			type2_tStart = time.time()
			g.latest_departure(x, y, interval)
			type2_tEnd = time.time()

			type3_tStart = time.time()
			g.fastest(x, y, interval)
			type3_tEnd = time.time()

			type4_tStart = time.time()
			g.shortest(x, y, interval)
			type4_tEnd = time.time()

			global_tEnd = time.time()

			tGlobal.append(global_tEnd - global_tStart)
			tInit.append(init_tEnd - init_tStart)
			tType1.append(type1_tEnd - type1_tStart)
			tType2.append(type2_tEnd - type2_tStart)
			tType3.append(type3_tEnd - type3_tStart)
			tType4.append(type4_tEnd - type4_tStart)

			if verbose:
				print("Temps d'executions rélatifs à l'itération n.", ite, "\n\ttGlobal :", tGlobal, "\n\ttInit :", tInit, "\n\ttType1 :", tType1, "\n\ttType2 :", tType2, "\n\ttType3 :", tType3, "\n\ttType4 :", tType4)

		ordonnee_tGlobal.append( (sum(tGlobal)/len(tGlobal)) )
		ordonnee_tType1.append( (sum(tType1)/len(tType1)) )
		ordonnee_tType2.append( (sum(tType2)/len(tType2)) )
		ordonnee_tType3.append( (sum(tType3)/len(tType3)) )
		ordonnee_tType4.append( (sum(tType4)/len(tType4)) )

	if verbose:
		print("Temps d'executions moyens rélatifs au test n.", nb, "\n\tordonnee_tGlobal :", ordonnee_tGlobal, "\n\tordonnee_tInit :", ordonnee_tInit, "\n\tordonnee_tType1 :", ordonnee_tType1, "\n\tordonnee_tType2 :", ordonnee_tType2, "\n\tordonnee_tType3 :", ordonnee_tType3, "\n\tordonnee_tType4 :", ordonnee_tType4)
	
	
	#Affichage graphique
	plt.figure(figsize = (10, 10))
	plt.suptitle("Performances")
	plt.rc('xtick', labelsize=10)    # fontsize of the tick labels
	
	# Construction et affichage du tracé "temps de calcul"
	plt.subplot(3, 1, 1)
	plt.title("Analyse du temps de calcul en fonction du nombre de sommets n")
	plt.xlabel("n") # nombre de sommets du graphe G
	plt.ylabel("t(n)") # temps de calcul en fonction du nombre de sommets du graphe G
	plt.plot(abscisse_n, ordonnee_tGlobal, color = 'blue')
	plt.plot(abscisse_n, ordonnee_tInit, color = 'red')
	plt.plot(abscisse_n, ordonnee_tType1, color = 'green')
	plt.plot(abscisse_n, ordonnee_tType2, color = 'yellow')
	plt.plot(abscisse_n, ordonnee_tType3, color = 'black')
	plt.plot(abscisse_n, ordonnee_tType4, color = 'pink')
	
	plt.subplot(3, 1, 2)
	plt.title("Analyse du temps de calcul en fonction du nombre d'arcs m")
	plt.xlabel("m") # nombre d'arcs du graphe G
	plt.ylabel("t(m)") # temps de calcul en fonction du nombre d'arcs du graphe G
	plt.plot(abscisse_m, ordonnee_tGlobal, color = 'blue')
	plt.plot(abscisse_m, ordonnee_tInit, color = 'red')
	plt.plot(abscisse_m, ordonnee_tType1, color = 'green')
	plt.plot(abscisse_m, ordonnee_tType2, color = 'yellow')
	plt.plot(abscisse_m, ordonnee_tType3, color = 'black')
	plt.plot(abscisse_m, ordonnee_tType4, color = 'pink')
	
	plt.subplot(3, 1, 3)
	plt.title("Analyse du temps de calcul en fonction de l'intervalle de dates choisies interval_dates")
	plt.xlabel("interval_dates") # nombre de sommets du graphe G
	plt.ylabel("t(interval_dates)") # temps de calcul en fonction de l'interval de dates choisies du graphe G
	plt.plot(abscisse_interval_dates, ordonnee_tGlobal, color = 'blue')
	plt.plot(abscisse_interval_dates, ordonnee_tInit, color = 'red')
	plt.plot(abscisse_interval_dates, ordonnee_tType1, color = 'green')
	plt.plot(abscisse_interval_dates, ordonnee_tType2, color = 'yellow')
	plt.plot(abscisse_interval_dates, ordonnee_tType3, color = 'black')
	plt.plot(abscisse_interval_dates, ordonnee_tType4, color = 'pink')
	
	# Sauvegarde du tracé
	if (save):
		plt.savefig("TestResults/" + str(datetime.date.today()) + str(datetime.datetime.now().strftime("_%H_%M_%S")) + ".jpeg", transparent = True)
	
	plt.show()







import random
import scipy.stats as st
from math import floor, ceil 

def randomMultigraphe(n, m, interval_dates):
	"""
	"""
	if n == 0 or m < n:
		return None

	vertices = ["s"+str(i) for i in range(n)]
	
	arcsADistribuer = m
	edges = []
	z = random.randint(1, int(np.log(n)) + 1) # nombre de feuilles (sommets finaux sans successeurs) souhaitées ; fonction logarithme népérien
	l = random.randint(1, int((n % m)) + 1) # lambda
	k = z*3 + 1 # nombre de arcs supplementaires que on réserve pour les sommets racine et feuilles

	# Parametrisation de truncnorm( (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd )
	borneInf = interval_dates[0] # low
	borneSup = interval_dates[1] # upp
	ecartType = int(interval_dates[1]/5) # sd
	# la moyenne mean vaut l'index du sommet en cours de traitement

	for i in range(m):

		if arcsADistribuer < 1:
			break

		# On attribue les premieres n-1 arcs pour rélier tous les sommets, tel que tout sommet est rélié à au moins un autre sommet
		if (i < n):
			print("on rentre car i =", i)
			source = vertices[i]
			nbSuccesseursSource = random.randint(1, int(((n % m))/2) + 1)
			if ( (i + nbSuccesseursSource) > n ):
				print("en effet:", i + nbSuccesseursSource, ">", n, "donc", n - i - 1 )
				nbSuccesseursSource = n - i - 1
			for j in range(1, nbSuccesseursSource):
				dest = vertices[i+j]
				#date = st.skewnorm.rvs(3, i, 5)
				#date = int(st.truncnorm.rvs( (borneInf - int(source[1])) / ecartType, (borneSup - int(source[1])) / ecartType, loc=int(source[1]), scale=ecartType ) )
				date = random.randint(borneInf, borneSup + 1)
				edges.append((source, dest, date, l))	# format arc : (source : str, dest : str, date : int, lambda l : int)
				arcsADistribuer -= 1
				print(i, "apres 1 :", arcsADistribuer)
				if arcsADistribuer == 0:
					break
				

		# On s'assure de réserver les derniers arcs à distribuer pour les sommets racine et feuilles
		elif (arcsADistribuer < k):
			print("k =", k)
			x = arcsADistribuer # <--------------------------- ne surtout pas effacer ce passage XD
			for j in range(floor(x/2)): # floor : partie entière inférieure
				print("test arcsADistribuer", arcsADistribuer)
				print("test repartition", floor(arcsADistribuer/2), ceil(arcsADistribuer/2))
				source = vertices[0] # racine
				dest = random.choice(vertices[1:z+2]) # choix parmi les premiers z sommets sauf la racine
				print("ja", j)
				#date = st.skewnorm.rvs(3, i, 5)
				#date = int( st.truncnorm.rvs( (borneInf - int(source[1])) / ecartType, (borneSup - int(source[1])) / ecartType, loc=int(source[1]), scale=ecartType ) )
				date = random.randint(borneInf, borneSup + 1)
				edges.append((source, dest, date, l))
				arcsADistribuer -= 1
				print(i, "apres 2a :", arcsADistribuer)

			for j in range(ceil(x/2)): # floor : partie entière superièure
				print("sono dentro b, j vale", j)
				print("sono dentro b, ceil", ceil(arcsADistribuer/2))
				source = random.choice(vertices[:-z*3+1]) # choix parmi les z*3 derniers sommets
				dest = random.choice(vertices[vertices.index(source)+1:])
				print("jb", j)
				#date = st.skewnorm.rvs(3, i, 5)
				#date = int( st.truncnorm.rvs( (borneInf - int(source[1])) / ecartType, (borneSup - int(source[1])) / ecartType, loc=int(source[1]), scale=ecartType ) )
				date = random.randint(borneInf, borneSup + 1)
				edges.append((source, dest, date, l))
				arcsADistribuer -= 1
				print(i, "apres 2b :", arcsADistribuer)

			break

		# Si les 2 cas précedents sont réspectés, le reste des arcs est distribué aléatoirement
		else:
			source = random.choice(vertices[:-z]) # tous les valeurs sauf le derniers z sommets (feuilles)
			dest = random.choice(vertices[vertices.index(source)+1:]) # tous les valeurs sauf le premier sommet (racine)
			#date = st.skewnorm.rvs(3, i, 5)
			#date = int( st.truncnorm.rvs(borneInf - int(source[1])) / ecartType, (borneSup - int(source[1])) / ecartType, loc=int(source[1]), scale=ecartType )
			date = random.randint(borneInf, borneSup + 1)
			edges.append((source, dest, date, l))	# format arc : (source : str, dest : str, date : int, lambda l : int)
			arcsADistribuer -= 1
			print(i, "apres 3 :", arcsADistribuer)


	print("len(vertices :", len(vertices), ", n :", n, ", len(edges) :", len(edges), ", m :", m)

	if len(vertices) != n or len(edges) != m :
		return None

	# Si i<n, alors il y a probablement des sommets non réliés par des arcs au multigraphe.
	# On rajoute la quantité minimale d'arcs à partir de ces sommets vers des successeurs pour ne pas faire planter la simulation.
	if (i < n) :
		print("on a i <n car i = ", i)
		nbSuccesseursSource = n-i
		for j in range(nbSuccesseursSource):
			source = vertices[i-1]
			dest = random.choice(vertices[vertices.index(source)+1:]) # tous les valeurs sauf le premier sommet (racine)
			#date = st.skewnorm.rvs(3, i, 5)
			#date = int(st.truncnorm.rvs( (borneInf - int(source[1])) / ecartType, (borneSup - int(source[1])) / ecartType, loc=int(source[1]), scale=ecartType ) )
			date = random.randint(borneInf, borneSup + 1)
			edges.append((source, dest, date, l))	# format arc : (source : str, dest : str, date : int, lambda l : int)
			print(i, "apres 7 :")


	return Multigraph(n, m, vertices, edges)


####################################################################################################################
#	TESTS DEBUG
####################################################################################################################

# mg = acquisitionMultigraphe("multigrapheG1.txt")

# if mg != None :
# 	mg.printMultigraphe()
# print("------------------------------------------------------------------")

#transformationMultigrapheMatAdjacence(g, verbose = False)
#print("------------------------------------------------------------------")

#listeAdj = transformationMultigrapheListeAdjacence(g, verbose = False)
#print("------------------------------------------------------------------")

# g = mg.transform_to_graph(True)
#print(g.adjacency_list)
#print("------------------------------------------------------------------")

# g.BFS("a", "g", [0, 10], True)
#print("------------------------------------------------------------------")

#g.showGraphe(titre = "graphe issu du multigraphe")
#print("------------------------------------------------------------------")

#g.showGrapheCouvrant(titre = "G Couvrant xxx")
#print("------------------------------------------------------------------")

#earliest_arrival('a', 'g', g, verbose = True)
#print("------------------------------------------------------------------")

#plotPerformances(10, 10, [1, 30], 15, 2, 'a', 'g', [2, 10], verbose = False, save = False)
#print("------------------------------------------------------------------")

rmg = randomMultigraphe(10, 20, [2,7])
if rmg != None :
	rmg.printMultigraphe()

rmg.showMultigraphe()
print("------------------------------------------------------------------")