import numpy as np
import networkx as nx
import time

def matching(n):
	assert type(n) is int and n > 0 and n%2 == 0, "n is not appropriate" # n must be even int
	
	pos = 0
	edges = 0 # edges matched so far
	M = [] # matching to output
	vertices = list(range(n))
	while vertices != []:
		i = 0
		j = np.random.randint(1, n - 2*edges)
		M.append((vertices[i],vertices[j]))
		vertices.pop(j)
		vertices.pop(i)
		edges += 1
	return M

# print(matching(10))

class ndErdosRenyi:
	
	def __init__(self, n, d, seed = -1):
		# variables: seed; size; deg; graph
		assert type(n) is int and type(d) is int and n > 0 and d > 0 and n%2 == 0, "n or d is not appropriate" # only even n for now
		
		self.size = n
		self.deg = d
		
		self.seed = seed
		if self.seed == -1:
			self.seed = int(time.time())
		np.random.seed(self.seed)
		
		self.graph = nx.MultiGraph()
		for _ in range(self.deg):
			self.graph.add_edges_from(matching(self.size))
	
	def announce(self):
		print("SEED =", self.seed)
		
# G = ndErdosRenyi(16, 4, 0)
# print(nx.adjacency_matrix(G.graph).todense())

# class npErdosRenyi:
class npErdosRenyi:
	
	def __init__(self, n, p, seed = -1):
		# variables: seed; size; deg; graph; adj mat, bool; adj dict, bool; sparse rep, bool
		assert type(n) is int and type(p) is float and n > 0 and p > 0, "n or p is not appropriate" # only even n for now
		
		self.size = n
		self.prob = p
		
		self.seed = seed
		if self.seed == -1:
			self.seed = int(time.time())
		np.random.seed(self.seed)
		
		self.graph = nx.Graph()
		for i in range(self.size):
			for j in range(i+1,self.size):
				q = np.random.random()
				if q < p:
					self.graph.add_edge(i,j)
	
	def announce(self):
		print("SEED =", self.seed)

# G = npErdosRenyi(20, 0.1, 0)
# print(nx.adjacency_matrix(G.graph).todense())
