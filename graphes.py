import sys
import operator
import re

# -------- UTILS -------- #

def readstr(): return sys.stdin.readline().strip()
def readint(): return int(readstr())
def readEdge():
	source, dest, time, weight = re.split("(|,|)", readstr())
	return (source, dest, int(time), int(weight))
def readInterval():
	t_alpha, t_omega = re.split("(|,|)", readstr())
	return (int(t_alpha), int(t_omega))

def parseMultigraph():
	
	n = readint()
	m = readint()
	vertices = [readstr() for _ in range(n)]
	edges = [readEdge() for _ in range(m)]

	return Multigraph(n, m, vertices, edges)

# -------- GRAPH -------- #

class Graph:

	def __init__(self, n, m, vertices, edges):
		
		self.n = n # number of vertices
		self.m = m # number of edges
		self.vertices = vertices # dictionary with key: original vertex, and value: list of new vertices (name, time) sorted by time
		self.edges = edges # list of tuples (u, v, weight), with u and v: tuples (name, time)
		self.adjacency_list = self.__obtain_adjacency_list(edges) # dictionary

	def __obtain_adjacency_list(self, vertices, edges, verbose=False):
		"""
		Returns an adjacency list (dictionary).
		"""

		# Construction de adjacency_list[key=source][val=destination, poids] (dictionnaire)
		adjacency_list = {}

		# Initialisation
		for vertex in vertices:
			adjacency_list[vertex] = []

		for source, dest, weight in edges :
			adjacency_list[source].append((dest, weight))

		if verbose:
			print("\nListe d'adjacence :", adjacency_list)

		return adjacency_list

	def BFS(self, x, y, verbose=False):
		"""
		Returns the shortest path from x to y.
		"""

		traceback = {} # Dictionnaire clé = successeur du pere (fils) : value = pere
		f = [x]	# Initialisation de la file avec le sommet source x
		sommetsVisites = [x] # Initialisation de la liste de sommets dejà visités avec le sommet source x
		traceback[x] = None

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

		if len(sommetsVisites) != len(self.adjacency_list):
			return "Erreur algorithme BFS"

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

		return path	

	def Dijkstra(self, x, y):
		"""
		"""

		pass

	def earliest_arrival(self, x, y, interval):
		"""
		Returns the path from x to y which arrives the earliest.

		"""

		path = []

		destinations = self.vertices[y] # liste des nouveaux sommets qui avaient pour sommet original y

		for v in destinations:
			BFS() # BFS partant de la fin


		return path

	def latest_departure(self, x, y, interval):
		"""
		Returns the path from x to y which leaves the latest.

		"""
		
		path = []

		return path

	def fastest(self, x, y, interval):
		
		path = []

		return path

	def shortest(self, x, y, interval):
		
		path = []

		return path

# -------- MULTIGRAPH -------- #

class Multigraph:

	def __init__(self, n, m, vertices, edges):
		
		self.n = n # number of vertices
		self.m = m # number of edges
		self.vertices = vertices # list of strings
		self.edges = edges # list of tuples: (u, v, t, lambda)

	def transform_to_graph(self):
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

		return Graph(self.n, self.m, newVertices, newEdges)

def main():

	# Rajouter tous les tests nécessaires pour éviter les erreurs

	mg = parseMultigraph()

	if mg == None:
		return

	x = readint()
	y = readint()
	interval = readints() # tuple: (start, end)

	g = mg.transform_to_graph()

	type1 = g.earliest_arrival(x, y, interval)
	type2 = g.latest_departure(x, y, interval)
	type3 = g.fastest(x, y, interval)
	type4 = g.shortest(x, y, interval)

