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

	print("Calcul des chemins minimaux...")
	# type1 = g.earliest_arrival(x, y, interval)
	# type2 = g.latest_departure(x, y, interval)
	# type3 = g.fastest(x, y, interval)
	# type4 = g.shortest(x, y, interval)

main()