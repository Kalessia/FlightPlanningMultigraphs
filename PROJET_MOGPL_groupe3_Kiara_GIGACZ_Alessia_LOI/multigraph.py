import datetime
import operator
import networkx as nx
from graph import Graph
import matplotlib.pyplot as plt


class Multigraph:

	def __init__(self, n, m, vertices, edges, verbose=False):
		
		self.n = n # number of vertices
		self.m = m # number of edges
		self.vertices = vertices # list of strings
		self.edges = edges # list of tuples: (u, v, t, lambda)

	def __str__(self):

		return "\nMultigraph with "+str(self.n)+" vertices and "+str(self.m)+" edges:\n\nVertices: "+str(self.vertices)+"\n\nEdges: "+str(self.edges)+"\n"

	def printMultigraphe(self):
		print("\nMultigraph de " + str(self.n) + " sommets et " + str(self.m) + " arcs :")
		print("\tListe de sommets : " + str(self.vertices) )
		print("\tListe d'arcs : " + str(self.edges) + "\n" )

	def transform_to_graph(self, verbose=False):
		"""
		Returns a simple graph.
		"""

		newVertices = {} # {original_vertex : list of new vertices}
		newEdges = []
		newN = 0

		for vertex in self.vertices:
			newVertices[vertex] = []

		for source, dest, t, weight in self.edges :

			# vOUT(sommet multiGraphe) = liste de doublets (v, t) avec v = sommet multiGraphe et t = poids (date) de l'arc sortant de v
			u = (source, t)
			if u not in newVertices[source]:
				newVertices[source].append(u)
				newN += 1

			# vIN(sommet multiGraphe) = liste de doublets (v, t) avec v = sommet multiGraphe et t = poids (date) de l'arc entrant de v + lambda
			v = (dest, t + weight)
			if v not in newVertices[dest]:
				newVertices[dest].append(v)
				newN += 1

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

		return Graph(newN, len(newEdges), newVertices, newEdges)

	# Méthode permettant d'afficher à l'écran un multigraphe orienté et, éventuellement, un titre
	def show(self, title = "Multigraphe pondere par le temps"):
		""" G : un dictionnaire representant un graphe { sommet s : sommets adjacents à s}
		    titre : titre du graphe à afficher, 'G' par defaut
		"""

		newG = nx.MultiDiGraph()
		newG.add_nodes_from(self.vertices)

		for source, dest, t, w in self.edges:
			newG.add_edge(source, dest, weight=t)

		plt.title(title)
		pos = nx.circular_layout(newG)

		dict_labels = {}
		e_labels = nx.get_edge_attributes(newG, 'weight')
		for u, v, w in e_labels:
			dict_labels[(u,v)] = w

		nx.draw_networkx_edge_labels(newG, pos=pos, edge_labels=dict_labels)
		nx.draw(newG, with_labels=True, node_size=1500, pos=pos)

		toPdot = nx.drawing.nx_pydot.to_pydot
		pdot = toPdot(newG)
		pdot.write_png("Visualisation_multigraphes/Multigraph/" + str(datetime.date.today()) + str(datetime.datetime.now().strftime("_%H_%M_%S")) + ".jpeg", transparent = True)

		plt.show()
		