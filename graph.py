class Graph:

	def __init__(self, n, m, vertices, edges):
		
		self.n = n # number of vertices
		self.m = m # number of edges
		self.vertices = vertices # dictionary with key: original vertex, and value: list of new vertices (name, time) sorted by time
		self.edges = edges # list of tuples (u, v, weight), with u and v: tuples (name, time)
		self.adjacency_list = self.__obtain_adjacency_list(vertices, edges) # dictionary with key: source, and value: list[(dest, weight)]

	def __obtain_adjacency_list(self, vertices, edges, verbose=False):
		"""
		Returns an adjacency list (dictionary).
		"""

		print(vertices)
		# Construction de adjacency_list[key=source][val=destination, poids] (dictionnaire)
		adjacency_list = {}

		# Initialisation
		for v_list in vertices.values():
			for vertex in v_list:
				adjacency_list[vertex] = []

		for source, dest, weight in edges :
			adjacency_list[source].append((dest, weight))

		if verbose:
			print("\nListe d'adjacence :", adjacency_list)

		return adjacency_list

	def BFS(self, x, y, interval, verbose=False):
		"""
		Returns the visited tree between x and y.

		Assumption: no cycles in the graph.
		"""

		visited_tree = {} # key: successor of the parent (child), value : parent

		t_alpha, t_omega = interval
		x_list = self.vertices[x]
		y_list = self.vertices[y].copy()

		if x_list[-1][1] < t_alpha or x_list[0][1] > t_omega or y_list[-1][1] < t_alpha or y_list[0][1] > t_omega:
			print("Aucun trajet possible entre x et y dans l'intervalle selectionné")
			return visited_tree # commentaire à retirer: je retourne un dict vide pour pas poser de problèmes dans les algos suivants, on retournera un chemin vide comme il n'y a aucun chemin possible

		root = None
		for vertex, time in x_list:
			if time >= t_alpha:
				root = (vertex, time) # sommet source contenant l'etiquette x et la plus petite date
				break
		print("Racine:", root)

		# To allow early exit [Optional (worth it if total nb of vertices >> len(path to y))]
		for vertex, time in y_list:
			if time < t_alpha or time > t_omega:
				y_list.remove((vertex, time))
		
		queue = [root]	# Initialisation de la file avec le sommet source x
		visited_tree[root] = None

		while (len(queue) > 0 and len(y_list) > 0): # complexity of len() in python : O(1), in other languages use counter to optimise
			print("\nNouvelle ite - etat file :", queue)
			current_v = queue.pop(0)
			print("Sommet à traiter :", current_v)
			if current_v in self.adjacency_list.keys(): # Erreur impossible ? et si possible la détecter plus tôt ?
				for successor, weight in self.adjacency_list[current_v]:
					print("\tSuccesseur :", successor)
					if successor not in visited_tree:
						queue.append(successor)
						visited_tree[successor] = current_v

						label, time = successor
						if label == y:
							y_list.remove(successor) # to allow early exit

		print("visited_tree :", visited_tree)

		return visited_tree

	def Dijkstra(self, x, y):
		"""
		"""

		pass