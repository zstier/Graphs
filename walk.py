import numpy as np
from numpy import log, abs
import networkx as nx
from ErdosRenyi import npErdosRenyi, ndErdosRenyi
import matplotlib.pyplot as plt

def runSignedWalk(G, f, t): # G is anything with .graph returning a nx object, f is a function
	assert type(f) == np.ndarray, "f not a numpy array"
	assert G.size == len(f), "f not a signing of G"
	assert type(t) == int and t >= 0, "t is not appropriate"
	
	A = nx.adjacency_matrix(G.graph)/G.deg
	n = len(f)
	v = np.ones(n)/n
	for _ in range(t):
		A @ (f * runSignedWalk(G, f, t))
	return v

def trackSignedWalk(G, f, t): # G is anything with .graph returning a nx object, f is a function
	assert type(f) == np.ndarray, "f not a numpy array"
	assert G.size == len(f), "f not a signing of G"
	assert type(t) == int and t >= 0, "t is not appropriate"
	
	A = nx.adjacency_matrix(G.graph)/G.deg
	n = len(f)
	ones = np.ones(n)
	v = ones/n
	values = []
	for _ in range(t+1):
		values.append(abs(ones@v))
		v = A @ (f * v)
	return values

"""
G = ndErdosRenyi(512, 9)
G.announce()
f = np.array([2*(i%2)-1 for i in range(512)])

plt.plot(log(trackSignedWalk(G, f, 50)),color='tab:purple')
plt.show()
plt.close()
"""
