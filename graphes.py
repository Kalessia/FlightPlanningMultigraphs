import sys 

# -------- UTILS -------- #

def readstr(): return sys.stdin.readline().strip()
def readint(): return int(readstr())
def readints(): return list(map(int, readstr().split()))

def parse():
	
	n = readint()
	m = readint()
	vertices = [readstr() for _ in range(n)]
	edges = [readints() for _ in range(m)]

	return Multigraph(n, m, vertices, edges)

# -------- MULTIGRAPH -------- #

class Multigraph:

	def __init__(self, n, m, vertices, edges):
		
		self.n = n # number of vertices
		self.m = m # number of edges
		self.vertices = vertices # list of strings
		self.edges = edges # list of tuples: (u, v, t, lambda)

	def earliest_arrival(x, y, interval):
		"""
		Returns the path from x to y which arrives the earliest.

		"""

		path = []

		return path

	def latest_departure(x, y, interval):
		"""
		Returns the path from x to y which arrives the earliest.

		"""
		
		path = []

		return path

	def fastest(x, y, interval):
		
		path = []

		return path

	def shortest(x, y, interval):
		
		path = []

		return path

def main():

	g = parse()

	x = readint()
	y = readint()
	interval = readints() # tuple: (start, end)

	type1 = g.earliest_arrival(x, y, interval)
	type2 = g.latest_departure(x, y, interval)
	type3 = g.fastest(x, y, interval)
	type4 = g.shortest(x, y, interval)

