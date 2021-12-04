import sys
import re

from multigraph import Multigraph 
from graph import Graph

# -------- UTILS -------- #

def readstr(): return sys.stdin.readline().strip()

def readint(): return int(readstr())

def readEdge():
	source, dest, time, weight = re.findall(r"\w+", readstr())
	return (source, dest, int(time), int(weight))

def readInterval():
	t_alpha, t_omega = re.findall(r"\w+", readstr())
	return (int(t_alpha), int(t_omega))

def parseMultigraph():
	
	n = readint()
	m = readint()
	vertices = [readstr() for _ in range(n)]
	edges = [readEdge() for _ in range(m)]

	return Multigraph(n, m, vertices, edges)

# -------- Minimal Distance Problem (with graph transformation) -------- #

class MinimalDistanceProblem():

	def __init__(self, g, x, y, interval):

		self.g = g
		self.x = x
		self.y = y
		self.interval = interval # closed interval
		self.visited_tree = g.BFS(x, y, interval) # contains best predecessors

	def traceback(self, x_list, specific_y, verbose=False):
		"""
		Uses visited_tree to find the shortest path between specific_x and specific_y.
		specific_x: (original_vertex_label, time)
		specific_y: (original_vertex_label, time)
		"""

		print("test traceback : sX, sY", x_list, specific_y)
		# if specific_x == None or specific_y == None:
		# 	return []
		
		# if specific_x not in self.visited_tree.keys() or specific_y not in self.visited_tree.keys():
		# 	return []

		if not(bool(self.visited_tree)):
			return []

		child = specific_y
		parent = self.visited_tree[child]
		path = [specific_y]

		while (parent != None):
			path.append(parent)

			if parent in x_list: 
				break

			print ("test : parent, child, path :", parent, child, path)
			child = parent
			parent = self.visited_tree[child]
		
		if parent == None:
			return []

		path.reverse()

		if verbose:
			print("\nRésultat traceback(x =", specific_x, ", y =", specific_y, ") :", path)

		return path

	def earliest_arrival(self, verbose=False):
		"""
		Returns the path from x to y which arrives the earliest.

		"""

		if self.x == self.y:
			return [x]

		x_list = self.g.vertices[self.x]
		y_list = self.g.vertices[self.y]

		if verbose :
			print("Liste des noeuds contenant y dans leur étiquette triée par t croissant:", y_list)
			print("Liste des noeuds contenant x dans leur étiquette :", x_list)

		# Pour chaque sommet dans la liste y_list, vérifier s' il existe un chemin de x à y en remontant le sens des arcs de G’.
		# L’algorithme s'arrête au premier chemin de x à y trouvé

		for specific_y in reversed(y_list):
			path = self.traceback(x_list, specific_y) # specific_y est le sommet contenant y dans l'etiquette pas encore testé avec t minimale
			if path != None:
				if verbose:
					print("Chemin d’arrivée au plus tôt de x à y :", path)
				return path

		if verbose:
			print("Il n'existe aucun chemin de x à y")	
		return None

	def latest_departure(self):
		"""
		Returns the path from x to y which leaves the latest.

		"""
		
		path = []

		return path

	def fastest(self):
		
		path = []

		return path

	def shortest(self):
		
		path = []

		return path

# -------- MAIN -------- #

def main():

	# TODO: Rajouter tous les tests nécessaires pour éviter les erreurs

	print("Veuillez entrer les données du graphe.")
	mg = parseMultigraph()

	if mg == None:
		return

	print("Le graph a été parsé sans erreur.")

	print("Veuillez entrer le sommet de départ : ")
	x = readstr()
	print("Veuillez entrer le sommet d'arrivée : ")
	y = readstr()
	print("Veuillez entrer l'intervalle dans lequel le trajet est effectué : ")
	interval = readInterval() # tuple: (start, end)

	print("Graphe en cours de transformation...")
	g = mg.transform_to_graph()

	p = MinimalDistanceProblem(g, x, y, interval)

	print("Calcul des chemins minimaux...")
	type1 = p.earliest_arrival()
	print("Chemin de type I :", type1)
	# type2 = g.latest_departure(x, y, interval)
	# type3 = g.fastest(x, y, interval)
	# type4 = g.shortest(x, y, interval)

main()