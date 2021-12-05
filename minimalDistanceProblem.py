from itertools import combinations

from multigraph import Multigraph 
from graph import Graph

#from gurobi_type4 import shortest_PL as pl


# -------- Minimal Distance Problem (with graph transformation) -------- #

class MinimalDistanceProblem():

	def __init__(self, g, x, y, interval):

		self.g = g
		self.x = x
		self.y = y
		self.interval = interval # closed interval
		self.visited_tree = g.BFS(x, y, interval) # contains best predecessors
		self.backwards_visited_tree = g.BFS(x, y, interval, backwards=True)

	def traceback(self, x_list, specific_y, visited_tree, backwards=False, verbose=False):
		"""
		Static method.
		Uses visited_tree to find the shortest path between specific_x and specific_y.
		x_list: list of possible sources
		specific_y: (original_vertex_label, time)
		visited_tree: dictionary containing best predecessors
		backwards: True if returned path should go from y to x
		"""

		# if specific_x == None or specific_y == None:
		# 	return []
		
		if specific_y not in visited_tree.keys():
			print("La destination n'était pas atteignable à partir de x.")
			return []

		if not(bool(visited_tree)):
			print("L'arbre couvrant est ")
			return []

		child = specific_y
		parent = visited_tree[child]
		path = [specific_y]

		while (parent != None):
			
			path.append(parent)
			if parent in x_list: # a path was found
				break

			child = parent
			parent = visited_tree[child]
		
		if parent == None: # reached the root without finding a path
			return []

		if not(backwards):
			path.reverse()

		if verbose:
			print("\nRésultat traceback(x =", specific_x, ", y =", specific_y, ") :", path)

		return path

	def earliest_arrival(self, verbose=False):
		"""
		Returns a path from x to y which arrives the earliest.

		"""

		if self.x == self.y:
			return [x]

		x_list = self.g.vertices[self.x]
		y_list = self.g.vertices[self.y]

		if verbose:
			print("Liste des noeuds contenant y dans leur étiquette triée par t croissant:", y_list)
			print("Liste des noeuds contenant x dans leur étiquette :", x_list)

		# Pour chaque sommet dans la liste y_list, vérifier s' il existe un chemin de x à y en remontant le sens des arcs de G’.
		# L’algorithme s'arrête au premier chemin de x à y trouvé

		for specific_y in y_list:
			path = self.traceback(x_list, specific_y, self.visited_tree) # specific_y est le sommet contenant y dans l'etiquette pas encore testé avec t minimale
			if len(path) > 0:
				if verbose:
					print("Chemin d’arrivée au plus tôt de x à y :", path)
				return path

		if verbose:
			print("Il n'existe aucun chemin de x à y.")	
		return []

	def latest_departure(self, verbose=False):
		"""
		Returns a path from x to y which leaves the latest.

		"""
		
		if self.x == self.y:
			return [x]

		x_list = self.g.vertices[self.x]
		y_list = self.g.vertices[self.y]
		
		for specific_x in reversed(x_list): # x triés par ordre décroissant
			path = self.traceback(y_list, specific_x, self.backwards_visited_tree, backwards=True) # specific_y est le sommet contenant y dans l'etiquette pas encore testé avec t minimale
			if len(path) > 0:
				if verbose:
					print("Chemin de départ au plus tard de x à y :", path)
				return path

		if verbose:
			print("Il n'existe aucun chemin de x à y.")
		return []

	def fastest(self, verbose=False):

		if self.x == self.y:
			return [x]
		
		x_list = self.g.vertices[self.x]
		y_list = self.g.vertices[self.y]

		combinations = [(x,y) for x in x_list for y in y_list]
		combinations.sort(key=lambda tup: tup[1][1]-tup[0][1]) # sorts in place by duration: t(y) - t(x)

		# Removes t(y) - t(x) <= 0 as they are impossible
		while combinations[0][1][1] - combinations[0][0][1] <= 0:
			combinations.pop(0)

		for c in combinations:
			for specific_x, specific_y in combinations:
				path = self.traceback([specific_x], specific_y, self.visited_tree) # specific_y est le sommet contenant y dans l'etiquette pas encore testé avec t minimale
			if len(path) > 0:
				if verbose:
					print("Chemin de plus courte durée :", path)
				return path

		if verbose:
			print("Il n'existe aucun chemin de x à y.")	
		return []

		return path

	def shortest(self):
		"""
		Returns a path from x to y for which the sum of the arc weights is minimal.

		"""

		visited_tree, specific_y = self.g.Dijkstra(self.x, self.y, self.interval)


		label, time = specific_y
		if label != self.y:
			return []

		return self.traceback(self.g.vertices[self.x], specific_y, visited_tree)

	#def shortest_gurobi(self):
	#	res = pl(self.adjacency_list)
	#	# boucler pour enterpreter le resultat


	def show_visited_tree(self, visited_tree, title = "Visited tree"):
		""" G : un dictionnaire representant un graphe { sommet s : sommets adjacents à s}
		    titre : titre du graphe à afficher, 'G' par defaut
		"""

		newG = nx.DiGraph()
		vertices = list(visited_tree.keys())
		newG.add_nodes_from(vertices)

		for successor in self.visited_tree.keys():
			if self.visited_tree[successor] == None:
				continue
			else:
				newG.add_edge(self.visited_tree[successor], successor)

		plt.title(title)
		nx.draw(newG, with_labels=True, node_size=1500, node_color="skyblue")

		toPdot = nx.drawing.nx_pydot.to_pydot
		pdot = toPdot(newG)
		pdot.write_png("VisitedTree.png")

		plt.show()