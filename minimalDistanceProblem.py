from itertools import combinations
from gurobipy import *
import numpy as np
import pandas as pd

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
		
		self.visited_tree = g.BFS(x, y, interval, verbose=True) # contains best predecessors
		self.backwards_visited_tree = g.BFS(y, x, interval, backwards=True)
		
		self.root = self.find_root()
		self.backwards_root = self.find_root(backwards=True)

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
			print("L'arbre couvrant est vide.")
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
			print("Racine atteinte sans trouver de chemin.")
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

		# TODO: A DEBUGGER !!

		if self.x == self.y:
			return [x]
		
		x_list = self.g.vertices[self.x]
		y_list = self.g.vertices[self.y]

		combinations = [(x,y) for x in x_list for y in y_list]
		combinations.sort(key=lambda tup: tup[1][1]-tup[0][1]) # sorts in place by duration: t(y) - t(x)

		# Removes t(y) - t(x) <= 0 as they are impossible
		while combinations[0][1][1] - combinations[0][0][1] <= 0:
			combinations.pop(0)

		print("fastest combinations: ", combinations)

		for c in combinations:
			specific_x, specific_y = c
			path = self.traceback([specific_x], specific_y, self.visited_tree) # specific_y est le sommet contenant y dans l'etiquette pas encore testé avec t minimale
			if len(path) > 0:
				if verbose:
					print("Chemin de plus courte durée :", path)
				return path

		if verbose:
			print("Il n'existe aucun chemin de x à y.")	
			return []

		return path

	def fastest_slow(self, verbose=False):

		if self.x == self.y:
			return [x]
	
		x_list = self.g.vertices[self.x]
		y_list = self.g.vertices[self.y]

		combinations = [(x,y) for x in x_list for y in y_list]
		combinations.sort(key=lambda tup: tup[1][1]-tup[0][1]) # sorts in place by duration: t(y) - t(x)

		# Removes t(y) - t(x) <= 0 as they are impossible
		while combinations[0][1][1] - combinations[0][0][1] <= 0:
			combinations.pop(0)

		print("fastest combinations: ", combinations)

		for c in combinations:
			specific_x, specific_y = c

			visited_tree = self.g.BFS_fastest(specific_x, specific_y, self.interval)
			path = self.traceback([specific_x], specific_y, visited_tree) # specific_y est le sommet contenant y dans l'etiquette pas encore testé avec t minimale
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

		visited_tree, specific_y = self.g.Dijkstra(self.x, self.y, self.interval, verbose=True)

		label, time = specific_y
		if label != self.y:
			return []

		return self.traceback(self.g.vertices[self.x], specific_y, visited_tree)

	def shortest_LP(self, verbose=False):

		nbcont = self.g.n
		nbvar = self.g.m
		print("nbcont: ", nbcont, ", nbvar: ", nbvar)

		vertices = [v for v_list in self.g.vertices.values() for v in v_list]
		edges = self.g.edges

		coefficients = []
		variables = [str(e) for e in edges]
		constraint_names = [str(v) for v in vertices]

		constraints = np.zeros((nbcont, nbvar), dtype=int)
		constraints = pd.DataFrame(constraints, constraint_names, variables)

		for i in range(nbvar):
			e = edges[i]
			source, dest, weight = e
			coefficients.append(weight)

		adjacency_list = self.g.adjacency_list
		backwards_adjacency_list = self.g.backwards_adjacency_list

		source_index = -1
		dest_index = -1

		# limit solution within interval
		specific_x = self.root
		specific_y = self.backwards_root

		print("test: ", specific_x, specific_y)

		for i in range(nbcont):

			vertice = vertices[i]
			
			if vertice == specific_x:
				source_index = i

			elif vertice == specific_y:
				dest_index = i

			for prev, weight in backwards_adjacency_list[vertice]: # -1 for all entering arcs
				constraints[str((prev, vertice, weight))][str(vertice)] = -1
			for succ, weight in adjacency_list[vertice]: # 1 for all exiting arcs
				constraints[str((vertice, succ, weight))][str(vertice)] = 1

		constraints = constraints.values.tolist()
		# print("Constraints:", constraints)

		lines = range(nbcont)
		columns = range(nbvar)

		# Second membre
		b = [0 for _ in range(nbcont)]
		b[source_index] = 1
		b[dest_index] = -1

		m = Model("mogplex")     

		# Déclaration des variables de décision
		x = []
		for i in columns:
			x.append(m.addVar(vtype=GRB.BINARY, lb=0, name=variables[i]))

		# Maj du modèle pour intégrer les nouvelles variables
		m.update()

		obj = LinExpr();
		obj = 0
		for j in columns:
			obj += coefficients[j] * x[j]

		# Définition de l'objectif
		m.setObjective(obj, GRB.MINIMIZE)

		# Définition des contraintes
		for i in lines:
			m.addConstr(quicksum(constraints[i][j]*x[j] for j in columns) <= b[i], "Contrainte%d" % i)

		# Résolution
		m.optimize()

		if verbose:
			print("")
			print('Solution optimale:')
			for j in columns:
				print(variables[j], '=', x[j].x)
			print("")
			print('Valeur de la fonction objectif :', m.objVal)

		path = []

		for j in columns:
			if x[j].x == 1.0:
				path.append(edges[j])

		path.sort(key = lambda tup: tup[0][1])
		return path

	def reduce_problem(self):

		t_alpha, t_omega = self.interval
		x_list = self.vertices[x]
		y_list = self.vertices[y].copy()

		if x_list[-1][1] < t_alpha or x_list[0][1] > t_omega or y_list[-1][1] < t_alpha or y_list[0][1] > t_omega:
			print("[reduce_problem] Aucun trajet possible entre x et y dans l'intervalle selectionné.")
			raise NoPathError

		# To allow early exit in BFS [Optional (worth it if total nb of vertices >> len(path to y))]
		for vertex, time in y_list:
			if time < t_alpha or time > t_omega:
				y_list.remove((vertex, time)) # Keeps (y, t) only if t is within interval
		
		return y_list

	def find_root(self, backwards=False, verbose=False):

		t_alpha, t_omega = self.interval

		root = None

		if backwards:
			for vertex, time in reversed(self.g.vertices[self.y]): 
				if time <= t_omega:
					root = (vertex, time) # root: vertex labeled with x which has the latest time
					break
		else:
			for vertex, time in self.g.vertices[self.x]: 
				if time >= t_alpha:
					root = (vertex, time) # root: vertex labeled with x which has the earliest time
					break
		
		if verbose:
			print("[find_root] Racine:", root)

		return root

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