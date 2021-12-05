import sys
import re

from multigraph import Multigraph 

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
	
	try:
		n = readint()
		m = readint()
		vertices = [readstr() for _ in range(n)]
		edges = [readEdge() for _ in range(m)] # catch error if not enough lines
	except ValueError:
		print("Format d'entrée non respecté, veuillez vérifier vos données.")

	return Multigraph(n, m, vertices, edges)