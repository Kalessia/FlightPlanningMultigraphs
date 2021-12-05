from multigraph import Multigraph 
from graph import Graph
from minimalDistanceProblem import MinimalDistanceProblem
from utils import *

# -------- MAIN -------- #

def main():

	# TODO: Rajouter tous les tests nécessaires pour éviter les erreurs

	print("Veuillez entrer les données du graphe.")
	mg = parseMultigraph()

	if mg == None:
		print("Erreur ")
		return

	print("Le graph a été parsé sans erreur.")

	print("Veuillez entrer le sommet de départ : ")
	x = readstr() # test si sommet n'existe pas
	print("Veuillez entrer le sommet d'arrivée : ")
	y = readstr()
	print("Veuillez entrer l'intervalle dans lequel le trajet est effectué : ")
	interval = readInterval() # tuple: (start, end)

	print("Graphe en cours de transformation...")
	g = mg.transform_to_graph()
	print(g)

	p = MinimalDistanceProblem(g, x, y, interval)
	if p.visited_tree == {} or p.backwards_visited_tree == {}:
		print("Aucun chemin existe pour les ")

	print("Calcul des chemins minimaux...")
	type1 = p.earliest_arrival()
	print("Chemin de type I (Arrivée le plus tôt) :", type1)
	type2 = p.latest_departure()
	print("Chemin de type II (Départ le plus tard) :", type2)
	type3 = p.fastest()
	print("Chemin de type III (Chemin le plus rapide) :", type3)
	type4 = p.shortest()
	print("Chemin de type IV (Chemin le plus court) :", type4)
	#type4_gurobi = p.shortest_gurobi()
	#print("Chemin de type IV (Chemin le plus court) calculé avec PL :", type4_gurobi)

main()