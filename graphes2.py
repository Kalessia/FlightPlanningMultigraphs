####################################################################################################################
#	IMPORTS
####################################################################################################################

import operator
import copy
from numpy.lib.type_check import _nan_to_num_dispatcher
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

	# Méthode permettant d'afficher à l'écran un graphe non orienté et, éventuellement, un titre
	def showGraphe(self, titre = "G"):
		# """ G : un dictionnaire representant un graphe { sommet s : sommets adjacents à s}
		#     titre : titre du graphe à afficher, 'G' par defaut
		# """
		newG = nx.DiGraph()
		listeSommetsG = list(self.adjacency_list.keys())
		newG.add_nodes_from(listeSommetsG)

		listeW = []
		for source in listeSommetsG:
			for dest , w in self.adjacency_list[source]:
				newG.add_edge(source, dest, weight=w)
				listeW.append(w)

		plt.title(titre)
		pos = nx.circular_layout(newG)
		e_labels = nx.get_edge_attributes(newG,'weight')
		nx.draw_networkx_edge_labels(newG, pos=pos, edge_labels=e_labels)
		nx.draw(newG, with_labels=True, node_size=1500, pos=pos)

		plt.show()   




#showGrapheCouvrant(g, titre = "G Couvrant")	



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




def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):

    '''
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723 

    If the graph is a tree this will return the positions to plot this in a 
    hierarchical layout.

    G: the graph (must be a tree)

    root: the root node of current branch 
    - if the tree is directed and this is not given, the root will be found and used
    - if the tree is directed and this is given, then the positions will be just for the descendants of this node.
    - if the tree is undirected and not given, then a random choice will be used.

    width: horizontal space allocated for this branch - avoids overlap with other branches

    vert_gap: gap between levels of hierarchy

    vert_loc: vertical location of root

    xcenter: horizontal location of root
    '''
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
        '''
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        '''

        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)  
        if len(children)!=0:
            dx = width/len(children) 
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap, 
                                    vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                    pos=pos, parent = root)
        return pos


    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)


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
def plotPerformances(p, nbIterations, secondesMaxAutorises, mode, verbose = False, save = False):
    """ p : la probabilité qu'une arete entre 2 sommets soit crée, p E ]0,1[
        nbIterations : nombre d'éxecutions de l'algorithme, dans le but d'en déduir une performance moyenne
        secondesMaxAutorises : temps maximum autorisé pour l'éxecution de l'algorithme
        nbNoeuds : nombre de nodes allant etre créées au maximum dans le graphe
        mode : valeur déterminant l'algorithme allant etre utilisé
        verbose : "True" pour afficher le détail des itérations
        save : "True" pour enregistrer le tracé en format jpg
    """
    # Calcul de la taille nMaxAGlouton pour l'algorithme (G)
    # nMax : taille jusqu'à laquelle l'algorithme tourne rapidement, i.e temps G(nMax,p) < secondesMaxAutorises
    nMax = 0
    t = 0
    while t < secondesMaxAutorises :
        nMax += 1
        
        # Méthode permettant de générer des graphes aléatoires
        G = randomGraphe(nMax, p)

        t1 = time.time()

        # Selection du mode (algorithme allant etre utilisé)
        if (mode == 1) :
            res = algoCouplage(G)
        elif (mode == 2) :
            res = algoGlouton(G)
        elif (mode == 3) :
            res = branchement(G)
        elif (mode == 4) :
            res = branchementBornesCouplage(G)
        elif (mode == 5) :
            res = branchementOptimiseCouplage(G)
        elif (mode == 6) :
            res = branchementOptimiseCouplage_uDegreMax(G)
        else :
            print("Aucun mode ne correspond à la valeur passée en paramètre. Veuillez choisir une autre valeur de mode.")
            return

        t2 = time.time()
        t = t2-t1

    if verbose :
        print("nMax = ", nMax, "\n")

    y1 = []  # axe des ordonnées : liste des temps de calcul moyen, pour l'algorithme sélectionné(G)
    y2 = []  # axe des ordonnées : liste des tailles des couplages (nombre de sommets) moyen, pour l'algorithme sélectionné(G)
    y3 = []  # axe des ordonnées : liste du nombre de noeuds générés pour l'algorithme de branchement (G)
    x = []   # axe des abscisses : liste de "nombre de sommets" {1/10 nbIterations, 2/10 nbIterations, ... , nbIterations}
    
    # Pour chaque 1/10 de nMax
    for i in range(1, 11) :

        tabTemps = []
        moyTemps = 0
        resAlgo = []
        moyQualiteSolutions = 0
        tabNoeudsGeneneres = []
        moyNbNoeudsGeneres = 0
        nbNoeuds = 0
        

        # Pour chacune des nbIterations démandées en paramètre
        for ite in range(nbIterations):

            # Méthode permettant de générer des graphes aléatoires
            G = randomGraphe(int(nMax * (i / 10)), p)

            # Execution et recueil statistiques de l'algorithme (G)
            t1 = time.time()

            # Variable res et noeud permettant de stocker le résultat de l'algorithme et le nombre de noeuds générés
            
            # Selection du mode (algorithme allant etre utilisé)
            if (mode == 1) :
                res = algoCouplage(G)
            elif (mode == 2) :
                res = algoGlouton(G)
            elif (mode == 3) :
                res, nbNoeuds = branchement(G)
            elif (mode == 4) :
                res, nbNoeuds = branchementBornesCouplage(G)
            elif (mode == 5) :
                res, nbNoeuds = branchementOptimiseCouplage(G)
            elif (mode == 6) :
                res, nbNoeuds = branchementOptimiseCouplage_uDegreMax(G)
            else :
                print("Aucun mode ne correspond à la valeur passée en paramètre. Veuillez choisir une autre valeur de mode.")
                return

            t2 = time.time()
            t = t2-t1

            tabTemps.append(t) # temps de calcul de l'algorithme pour l'itération courante
            resAlgo.append(len(res)) # qualité des solutions pour l'itération courante
            if (mode > 2) : # Dans le cas ou on utilise un algorithme de branchement
                tabNoeudsGeneneres.append(nbNoeuds)

            if verbose : 
                print("x = ", i, "/10 nMax, iteration n.", ite+1, ":", "\n\t\ttabTemps =", tabTemps, "\n\t\tresAlgo =", resAlgo, "\n")

        # Calcul et stockage du temps d'execution moyen et de la qualité des solutions moyenne par rapport aux 'nbIterations' éxecutions
        moyTemps = sum(tabTemps)/len(tabTemps)
        moyQualiteSolutions = int(sum(resAlgo)/len(resAlgo))
        if (mode > 2) :
            moyNbNoeudsGeneres = int(sum(tabNoeudsGeneneres)/len(tabNoeudsGeneneres))
        

        y1.append(moyTemps)
        y2.append(moyQualiteSolutions)
        if (mode > 2) :
            y3.append(moyNbNoeudsGeneres)
        x.append(int(nMax * (i / 10)))

        if verbose : 
            print("\nx = ", i, "/10 nMax (" + str(int(nbIterations * i/10)) + ") : moyTemps =", moyTemps, "moyQualiteSolutions =", moyQualiteSolutions)
            print("----------------------------------------------------------------------------------------------\n")

    # Selection du nom de l'algorithme
    if (mode == 1) :
        nomAlgo = "algo_Couplage"
    elif (mode == 2) :
        nomAlgo = "algo_Glouton"
    elif (mode == 3) :
        nomAlgo = "branchement"
    elif (mode == 4) :
        nomAlgo = "branchement_Bornes_Couplage"
    elif (mode == 5) :
        nomAlgo = "branchement_Optimise_Couplage"
    elif (mode == 6) :
        nomAlgo = "branchement_Optimise_Couplage_uDegreMax"
    else :
        print("Aucun mode ne correspond à la valeur passée en paramètre. Veuillez choisir une autre valeur de mode.")
        return

    # Affichage graphique
    plt.figure(figsize = (10, 10))
    plt.suptitle("Performances de l'algorithme " + nomAlgo + " avec nMax =" + str(nMax) + " nodes dans le graphe et p = " + str(p) + "\n", color = 'black', size = 10)
    plt.rc('xtick', labelsize=10)    # fontsize of the tick labels

    # Construction et affichage du tracé "temps de calcul"
    plt.subplot(3, 1, 1)
    plt.title("Analyse du temps de calcul en fonction du nombre de sommets n")
    plt.xlabel("n") # nombre de sommets du graphe G
    plt.ylabel("t(n)") # temps de calcul en fonction du nombre de sommets du graphe G
    plt.plot(x, y1, color = 'blue')

    # Construction et affichage du tracé "qualité des solutions"
    plt.subplot(3, 1, 2)
    plt.title("Analyse de la qualité des solutions en fonction du nombre de sommets n")
    plt.xlabel("n") # nombre de sommets du graphe G
    plt.ylabel("q(n)") # qualité des solutions (taille du couplage) en fonction du nombre de sommets du graphe G
    plt.plot(x, y2, color = 'green')

    if (mode > 2) : # Construction et affichage du tracé "nombre de noeuds générés"
        plt.subplot(3, 1, 3)
        plt.title("Nombre de noeuds générés dans l'algorithme de branchement en fonction du nombre de sommets n")
        plt.xlabel("n") # nombre de sommets du graphe G
        plt.ylabel("c(n)") # nombre de noeuds crées durant le branchement en fonction du nombre de sommets du graphe G
        plt.plot(x, y3, color = 'red')

    # Sauvegarde du tracé
    if (save) :
        plt.savefig("TestResults/" + nomAlgo + "_p=" + str(p) + "_" + str(datetime.date.today()) + str(datetime.datetime.now().strftime("_%H_%M_%S")) + ".jpeg", transparent = True)

    plt.show()

#------------------------------------------------------------------------------------------------------

# Méthode permettant d'afficher le rapport d'approximation de algoCouplage et algoGlouton
def plotRapportApproximation(nMax, p, mode, verbose = False, save = False):
    """ nMax : nombre de noeuds maximale pour le graphe
        p : la probabilité qu'une arete entre 2 sommets soit crée, p E ]0,1[
        mode : valeur déterminant l'algorithme allant etre utilisé, 1 = algoCouplage ; 2 = algoGlouton
        verbose : "True" pour afficher le détail des itérations
        save : "True" pour enregistrer le tracé en format jpg
    """
    y = []   # axe des ordonnées : rapport d'approximation des algorithmes couplage et glouton
    x = []   # axe des abscisses : liste de "nombre de sommets" {1/10 nbIterations, 2/10 nbIterations, ... , nbIterations}
    
    # Pour chaque 1/10 de nMax
    for i in range(1, 11) :

        r = -1
        res = -1

        # Méthode permettant de générer des graphes aléatoires
        G = randomGraphe(int(nMax * (i / 10)), p)

        # Calcul du rapport d'approximation r
        # mode : 1 = algoCouplage ; 2 = algoGlouton
        if (mode == 1) :
            res = len(algoCouplage(G))
        elif (mode == 2) :
            res = len(algoGlouton(G))
        else :
            print("Aucun mode ne correspond à la valeur passée en paramètre. Veuillez choisir une autre valeur de mode.")
            return

        opt = len(branchement(G))

        if opt != 0 :
            r = res/opt
        
        y.append(r)
        x.append(int(nMax * (i / 10)))

        if verbose : 
            print("\nx = ", i, "/10 nMax\n\t\tRapport d'approximation :", r, "\n")
            print("----------------------------------------------------------------------------------------------\n")


    # Affichage graphique
    plt.figure(figsize = (10, 10))
    if (mode == 1) :
        plt.title("Rapport d'approximation de l'algorithme algoCouplage en f(n) avec nMax =" + str(nMax) + " nodes dans le graphe et p = " + str(p) + "\n", color = 'black', size = 15)
    if (mode == 2) :
        plt.title("Rapport d'approximation de l'algorithme algoGlouton en f(n) avec nMax =" + str(nMax) + " nodes dans le graphe et p = " + str(p) + "\n", color = 'black', size = 15)
    plt.rc('xtick', labelsize=10)    # fontsize of the tick labels

    # Construction et affichage du tracé
    plt.xlabel("n") # nombre de sommets du graphe G
    plt.ylabel("r") # rapport d'approximation
    plt.axis([0, nMax, 0, r+1])
    plt.plot(x, y, color = 'blue')

    # Sauvegarde du tracé
    if (save) :
        plt.savefig("TestResults/rapportApproximation_p=" + str(p) + "_" + str(datetime.date.today()) + str(datetime.datetime.now().strftime("_%H_%M_%S")) + ".jpeg", transparent = True)

    plt.show()






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
#print(g.adjacency_list)
#print("------------------------------------------------------------------")

#g.BFS("a", "g", [0, 10], True)
#print("------------------------------------------------------------------")

#earliest_arrival('a', 'g', g, verbose = True)
#print("------------------------------------------------------------------")

g.showGraphe(titre = "graphe issu du multigraphe")
#print("------------------------------------------------------------------")

#showGrapheCouvrant(g, titre = "G Couvrant")
#print("------------------------------------------------------------------")


