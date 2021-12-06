import heapq
import networkx as nx
import matplotlib.pyplot as plt


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

		adjacency_list = {}
		backwards_adjacency_list = {}

		# Initialisation
		for v_list in vertices.values():
			for vertex in v_list:
				adjacency_list[vertex] = []
				backwards_adjacency_list[vertex] = []
		
		# adjacency_list[key=source][val=(destination, weight)]
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

		x: vertex in original (multi)graph
		y: vertex in original (multi)graph
		backwards: True if building tree from destination (x: destination, y: source)
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
			print("[BFS] Aucun trajet possible entre x et y dans l'intervalle selectionné.")
			return visited_tree 

		root = None

		if backwards:
			for vertex, time in reversed(x_list): 
				if time <= t_omega:
					root = (vertex, time) # root: vertex labeled with x which has the latest time
					break
		else:
			for vertex, time in x_list: 
				if time >= t_alpha:
					root = (vertex, time) # root: vertex labeled with x which has the earliest time
					break
		if verbose:
			print("[BFS] Racine:", root)

		# To allow early exit [Optional (worth it if total nb of vertices >> len(path to y))]
		for vertex, time in y_list:
			if time < t_alpha or time > t_omega:
				y_list.remove((vertex, time)) # Keeps (y, t) only if t is within interval
		
		queue = [root]
		visited_tree[root] = None

		while (len(queue) > 0 and len(y_list) > 0): # complexity of len() in python : O(1), in other languages use counter to optimise
			current_v = queue.pop(0)
			if verbose:
				print("\n[BFS] Etat de la file :", queue)
				print("[BFS] Sommet à traiter :", current_v)
			if current_v in self.adjacency_list.keys():
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

	def Dijkstra(self, x, y, interval, verbose=False):
		"""
		"""

		visited_tree = {} # key: successor of the parent (child), value : parent

		t_alpha, t_omega = interval
		x_list = self.vertices[x]
		y_list = self.vertices[y].copy()

		if x_list[-1][1] < t_alpha or x_list[0][1] > t_omega or y_list[-1][1] < t_alpha or y_list[0][1] > t_omega:
			print("Aucun trajet possible entre x et y dans l'intervalle selectionné.")
			return visited_tree, ("null", -1)

		root = None

		for vertex, time in x_list: 
			if time >= t_alpha:
				root = (vertex, time) # root: vertex labeled with x which has the earliest time
				break

		if verbose:
			print("[Dijkstra] Racine:", root)

		priorityQ = [(0, root)]
		visited_tree[root] = None
		cost_so_far = {}
		cost_so_far[root] = 0

		while (len(priorityQ) > 0 and len(y_list) > 0): # complexity of len() in python : O(1), in other languages use counter to optimise
			
			time, label = heapq.heappop(priorityQ)
			current_v = label
			if verbose:
				print("\n[Dijkstra] Etat de la file :", priorityQ)
				print("[Dijkstra] Sommet à traiter :", current_v)
			if current_v in self.adjacency_list.keys():
				for successor, weight in self.adjacency_list[current_v]:
					new_cost = cost_so_far[current_v] + weight
					if verbose:
						print("\tSuccesseur :", successor)
					if successor not in visited_tree or new_cost < cost_so_far[successor]:
						cost_so_far[successor] = new_cost
						heapq.heappush(priorityQ, (new_cost, successor))
						visited_tree[successor] = current_v

						label, time = successor
						if label == y:
							print("\n[Dijkstra] visited_tree :", visited_tree, "\n")
							return visited_tree, successor

		print("\n[Dijkstra] visited_tree :", visited_tree, "\n")

		return visited_tree, successor


	# Méthode permettant d'afficher à l'écran un graphe orienté et, éventuellement, un titre
	def show(self, title = "Graph"):
		""" G : un dictionnaire representant un graphe { sommet s : sommets adjacents à s}
		    titre : titre du graphe à afficher, 'G' par defaut
		"""

		newG = nx.DiGraph()
		vertices = list(self.adjacency_list.keys())
		newG.add_nodes_from(vertices)

		for source in vertices:
			for dest, w in self.adjacency_list[source]:
				newG.add_edge(source, dest, weight=w)

		plt.title(title)
		pos = nx.circular_layout(newG)
		e_labels = nx.get_edge_attributes(newG, 'weight')
		nx.draw_networkx_edge_labels(newG, pos=pos, edge_labels=e_labels)
		nx.draw(newG, with_labels=True, node_size=1500, pos=pos)

		toPdot = nx.drawing.nx_pydot.to_pydot
		pdot = toPdot(newG)
		pdot.write_png("Graph.png")

		plt.show()