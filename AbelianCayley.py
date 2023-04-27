import networkx as nx

def groupSum(s, t, group):
	assert type(group) is tuple, "group is not appropriate"
	for n in group:
		assert type(n) is int and n > 1, "a group entry is not appropriate"
	rank = len(group)
	assert type(s) is tuple and len(s) == rank and type(t) is tuple and len(t) == rank, "a group element is not a tuple of the correct length"
	for i in range(rank):
		assert type(s[i]) is int and 0 <= s[i] < group[i] and type(t[i]) is int and 0 <= t[i] < group[i], "a group element has an entry which is not appropriate"
	return tuple([(s[i]+t[i])%group[i] for i in range(rank)])

class AbelianCayley:
	
	def __init__(self, group, gens): # group is a tuple of positive integers (residues), group is a list of tuples of the same length where each is a proper residue. will generate a multigraph, so duplicates (up to sign) get counted twice
		assert type(group) is tuple, "group is not appropriate"
		for n in group:
			assert type(n) is int and n > 1, "a group modulus is not appropriate"
		self.rank = len(group)
		assert type(gens) is list or type(gens) is int, "gens is not appropriate"
		for s in gens:
			assert type(s) is tuple and len(s) == len(group), "a generator is not a tuple of the correct length"
			for i in range(self.rank):
				assert type(s[i]) is int and 0 <= s[i] < group[i], "a generator has an entry which is not appropriate"
		self.size = 1
		for n in group:
			self.size *= n
		V = [[n] for n in range(group[0])]
		for i in range(1, self.rank):
			W = []
			for t in V:
				for m in range(group[i]):
					W.append(t + [m])
			V = W
		V = [tuple(t) for t in V]
		self.deg = 2*len(gens)
		self.graph = nx.MultiGraph()
		for v in V:
			vString = str(v)
			for s in gens:
				w = groupSum(v, s, group)
				wString = str(w)
				self.graph.add_edge(vString, wString)

# G = AbelianCayley((2,5), [(1,1)])
# print(G.graph.number_of_edges())
