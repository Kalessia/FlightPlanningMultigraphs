class Graph:

	def __init__(self, n, m, vertices, edges):
		
		self.n = n # number of vertices
		self.m = m # number of edges
		self.vertices = vertices # dictionary with key: original vertex, and value: list of new vertices (name, time) sorted by time
		self.edges = edges # list of tuples (u, v, weight), with u and v: tuples (name, time)
		self.adjacency_list = self.__obtain_adjacency_list(vertices, edges) # dictionary

	def __obtain_adjacency_list(self, vertices, edges, verbose=False):
		"""
		Returns an adjacency list (dictionary).
		"""

		print(vertices)
		# Construction de adjacency_list[key=source][val=destination, poids] (dictionnaire)
		adjacency_list = {}

		# Initialisation
		for vertex in vertices:
			adjacency_list[vertex] = []

		for (source, weight), dest, weight in edges :
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