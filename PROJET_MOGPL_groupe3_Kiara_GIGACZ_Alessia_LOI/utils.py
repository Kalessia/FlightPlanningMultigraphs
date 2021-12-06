import sys
import re

from multigraph import Multigraph 
from minimalDistanceProblem import MinimalDistanceProblem

# -------- UTILS -------- #

def read_str(): return sys.stdin.readline().strip()

def read_int(): return int(read_str())

def read_edge():
	source, dest, time, weight = re.findall(r"\w+", read_str())
	return (source, dest, int(time), int(weight))

def read_interval():
	t_alpha, t_omega = re.findall(r"\w+", read_str())
	return (int(t_alpha), int(t_omega))

def parse_multigraph(safety=True):
	
	print("Veuillez entrer les données du graphe.")

	try:
		n = read_int()
		m = read_int()
		vertices = [read_str() for _ in range(n)]
		edges = [read_edge() for _ in range(m)] # catch error if not enough lines

		if safety:
			if len(vertices) != n or len(edges) != m:
				raise ValueError

	except ValueError:
		raise InputError("multigraphe") from None

	return Multigraph(n, m, vertices, edges)

def parse_problem(mg, g, safety=True):
	"""
	Reads x, y, and interval from stdin.
	safety: if True, performs extra tests. Deactivate when certain that the input is correct.
	"""

	try:
		print("Veuillez entrer le sommet de départ : ")
		x = read_str() 
		print("Veuillez entrer le sommet d'arrivée : ")
		y = read_str()
		print("Veuillez entrer l'intervalle dans lequel le trajet est effectué : ")
		interval = read_interval() # tuple: (start, end)
	except ValueError:
		raise InputError("problème") from None

	if safety:

		if not(x in mg.vertices):
			raise NoPathError("Le sommet de départ n'est pas dans le graphe.")
		if not(y in mg.vertices):
			raise NoPathError("Le sommet d'arrivée n'est pas dans le graphe.")
		if x == y:
			raise NoPathError("Le sommet de départ et le sommet d'arrivée sont égaux.")
		
	return MinimalDistanceProblem(g, x, y, interval)
	
	# for i in range(2, len(lignes)):
	# 	r = re.compile("^[(][\w]*[,][\w]*[,][0-9]*[,][0-9]*[)]\n*$")
	# 	if r.match(lignes[i]) is not None:
	# 		# format d'un arc : (source, dest, int(time), int(weight))
	# 		e = lignes[i].split("(")[1].split(")")[0].split(",")
	# 		edges.append((e[0], e[1], int(e[2]), int(e[3])))
	# 		print((e[0], e[1], int(e[2]), int(e[3])))
	# 	else :
	# 		vertices.append(lignes[i].split("\n")[0])

# -------- ERRORS -------- #

class Error(Exception):
	"""Base class for exceptions in this module."""
	pass

class InputError(Error):

	def __init__(self, format_type):
		self.format_type = format_type

	def __str__(self):
		return "Format de "+self.format_type+" non respecté, veuillez vérifier vos données."

class NoPathError(Error):
	pass
