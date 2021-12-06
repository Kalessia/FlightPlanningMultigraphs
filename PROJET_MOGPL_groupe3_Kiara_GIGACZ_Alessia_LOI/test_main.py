from multigraph import Multigraph 
from graph import Graph
from minimalDistanceProblem import MinimalDistanceProblem
from utils import *

# -------- MAIN -------- #

def main():

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
		type3 = p.fastest()
		print("Chemin de type III (Chemin le plus rapide) :", type3)
		type4 = p.shortest()
		print("Chemin de type IV (Chemin le plus court) :", type4)
		type4_gurobi = p.shortest_LP()
		#print("Chemin de type IV (Chemin le plus court) calculé avec PL :", type4_gurobi)

	except NoPathError:
		"Sortie anticipée du programme car aucun chemin possible."

main()