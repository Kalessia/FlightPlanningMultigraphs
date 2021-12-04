class Graph:

	def __init__(self, n, m, vertices, edges):
		
		self.n = n # number of vertices
		self.m = m # number of edges
		self.vertices = vertices # dictionary with key: original vertex, and value: list of new vertices (name, time) sorted by time
		self.edges = edges # list of tuples (u, v, weight), with u and v: tuples (name, time)
		self.adjacency_list, self.backwards_adjacency_list = self.__obtain_adjacency_list(vertices, edges) # dictionary with key: source, and value: list[(dest, weight)]

	def __obtain_adjacency_list(self, vertices, edges, verbose=False):
		"""
		Static method (doesn't depend on the attributes of the calling graph).
		Returns an adjacency list (dictionary).
		"""

		# Construction du dictionnaire adjacency_list[key=source][val=destination, poids]
		adjacency_list = {}
		backwards_adjacency_list = {}

		# Initialisation
		for v_list in vertices.values():
			for vertex in v_list:
				adjacency_list[vertex] = []
				backwards_adjacency_list[vertex] = []

		for source, dest, weight in edges :
			adjacency_list[source].append((dest, weight))
			backwards_adjacency_list[dest].append((source, weight))

		if verbose:
			print("Liste d'adjacence :", adjacency_list)
			print("Liste d'adjacence inversée :", backwards_adjacency_list)

		return adjacency_list, backwards_adjacency_list

	def __str__(self):

		return "\nGraph: \n\nVertices: "+str(self.vertices)+"\n\nEdges: "+str(self.edges)+"\n\nAdjacency List: "+str(self.adjacency_list)

	def BFS(self, x, y, interval, backwards=False, verbose=False):
		"""
		Returns the visited tree between x and y.

		Assumption: no cycles in the graph.
		"""

		if backwards:
			adjacency_list = self.backwards_adjacency_list
		else:
			adjacency_list = self.adjacency_list

		visited_tree = {} # key: successor of the parent (child), value : parent

		t_alpha, t_omega = interval
		x_list = self.vertices[x]
		y_list = self.vertices[y].copy()

		if x_list[-1][1] < t_alpha or x_list[0][1] > t_omega or y_list[-1][1] < t_alpha or y_list[0][1] > t_omega:
			print("Aucun trajet possible entre x et y dans l'intervalle selectionné.")
			return visited_tree # commentaire à retirer: je retourne un dict vide pour pas poser de problèmes dans les algos suivants, on retournera un chemin vide comme il n'y a aucun chemin possible

		root = None

		if backwards:
			for vertex, time in reversed(x_list): 
				if time <= t_omega:
					root = (vertex, time) # sommet source contenant l'etiquette x et la plus petite date
					break
		else:
			for vertex, time in x_list: 
				if time >= t_alpha:
					root = (vertex, time) # sommet source contenant l'etiquette x et la plus petite date
					break
		if verbose:
			print("[BFS] Racine:", root)

		# To allow early exit [Optional (worth it if total nb of vertices >> len(path to y))]
		for vertex, time in y_list:
			if time < t_alpha or time > t_omega:
				y_list.remove((vertex, time))
		
		queue = [root]	# Initialisation de la file avec le sommet source x
		visited_tree[root] = None

		while (len(queue) > 0 and len(y_list) > 0): # complexity of len() in python : O(1), in other languages use counter to optimise
			current_v = queue.pop(0)
			if verbose:
				print("\n[BFS] Etat de la file :", queue)
				print("[BFS] Sommet à traiter :", current_v)
			if current_v in self.adjacency_list.keys(): # Erreur impossible ? et si possible la détecter plus tôt ?
				for successor, weight in adjacency_list[current_v]:
					if verbose:
						print("\tSuccesseur :", successor)
					if successor not in visited_tree:
						queue.append(successor)
						visited_tree[successor] = current_v

						label, time = successor
						if label == y:
							y_list.remove(successor) # to allow early exit

		print("\n[BFS] visited_tree :", visited_tree, "\n")

		return visited_tree

	def Dijkstra(self, x, y):
		"""
		"""

		pass