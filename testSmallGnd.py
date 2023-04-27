from ErdosRenyi import ndErdosRenyi
from miscCombo import combinations
from walk import trackSignedWalk
import networkx as nx
import matplotlib.pyplot as plt
from numpy import log
import numpy as np


# for a Gnd, is it the case that all balanced functions have lambda^t vanishing?

n = 12
d = 3
t = 100

trials = 1

def plusMinus1(n, S):
	l = [1 for _ in range(n)]
	for s in S:
		l[s] = -1
	return np.array(l)
balanced = [plusMinus1(n, S) for S in combinations(n,n//2)]
# print(balanced[:5])

for _ in range(trials):
	G = ndErdosRenyi(n, d)
	G.announce()
	evals = nx.laplacian_spectrum(G.graph)
	print(evals)
	gl = (evals[1]-evals[0])/d
	if nx.is_connected(G.graph):
		for f in balanced:
			plt.plot(log(trackSignedWalk(G, f, t)),color='k')
		plt.plot([i*log(gl) for i in range(t+1)],color='r')
		plt.xlabel('t')
		plt.ylabel('log | 1 . (AD)^t . 1 |')
		plt.show()
		plt.close()
