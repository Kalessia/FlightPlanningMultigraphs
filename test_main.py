from multigraph import Multigraph 
from graph import Graph
from minimalDistanceProblem import MinimalDistanceProblem
from utils import *

###################### A RETIRERRRRRRRRRRRRRRRRRRRRRRRRRRRRR !!!!!!!!!!!!!!!!!!!!!!! JUSTE POUR TESTER #############""

from datetime import datetime
from math import floor
from pathlib import Path
import random

def generateGraph(nbNodes, p, lbdarange=None, t_max = 3):
	"""
	Randomly generates a multigraph

	:param nbNodes: Number of nodes the multigraph should have
	:param p: Probability of a node being linked to a subsequent node
	:param lbdarange: Possible lambda values for each arc
	:param t_max: Random variance for the date between two nodes
	:return: A randomly generated multigraph
	"""
	if lbdarange is None:
		lbdarange = [1]

	nodes = [str(i) for i in range(nbNodes)]
	arcs = set()
	for i in range(nbNodes):
		for j in range(i + 1, nbNodes):
			if random.random() < p:
				variance = [i + floor(random.uniform(0.9,1.2) * j) for i in range(0, t_max)]
				random_t = 1 + floor(random.random() * i) + random.choice(variance)
				arcs.add(f'({i},{j},{random_t},{random.choice(lbdarange)})')
	lines = [str(nbNodes), str(len(arcs))]
	lines.extend(nodes)
	lines.extend(arcs)

	newFilePath = ''
	try:
		Path('graphsInput').mkdir(parents=True, exist_ok=True)
		newFilePath = f'graphsInput/multigraph-generated-{int(datetime.now().timestamp())}.mug'
		with open(newFilePath, 'w') as f:
			f.write('\n'.join(lines))
		print(f'Successfully saved file at: {newFilePath}')
	except (IOError, OSError) as e:
		print('An error occured while saving the file: ' + e)

	return newFilePath

# -------- MAIN -------- #

def main():

	generateGraph(10, 0.5)

	try:

		mg = parse_multigraph()
		print(mg)
		print("Le graph a été parsé sans erreur.")

		print("Graphe en cours de transformation...")
		g = mg.transform_to_graph()
		print(g)

		p = parse_problem(mg, g, safety=True)

		if p.visited_tree == {} or p.backwards_visited_tree == {}:
			raise NoPathError

		print("Calcul des chemins minimaux...")
		type1 = p.earliest_arrival()
		print("Chemin de type I (Arrivée le plus tôt) :", type1)
		if type1 == []:
			raise NoPathError
		type2 = p.latest_departure()
		print("Chemin de type II (Départ le plus tard) :", type2)
		type3 = p.fastest_slow()
		print("Chemin de type III (Chemin le plus rapide) :", type3)
		type4 = p.shortest()
		print("Chemin de type IV (Chemin le plus court) :", type4)
		type4_gurobi = p.shortest_LP(verbose=True)
		print("Chemin de type IV (Chemin le plus court) calculé avec PL :", type4_gurobi)

	except NoPathError:
		"Sortie anticipée du programme car aucun chemin possible."

main()