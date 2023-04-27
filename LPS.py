import numpy as np
from numpy import sqrt
import networkx as nx
from miscNT import legendre, tonelli
from primefac import isprime
import pickle
from os.path import exists
# import os

def jacobi4(p):
	if exists("LPS/Jacobi4/" + str(p) + ".p"):
		return pickle.load(open("LPS/Jacobi4/" + str(p) + ".p", "rb"))
	else:
		A = [] # list of quadruples
		for a in range(1, int(sqrt(p))+1, 2): # look for odd a
			rb = int(sqrt(p-a**2))
			fb = rb % 2
			for b in range(-rb+fb, rb+1, 2): # look for even b which are not too large
				rc = int(sqrt(p-a**2-b**2))
				fc = rc % 2
				for c in range(-rc+fc, rc+1, 2): # look for even c which are not too large
					d = int(sqrt(p-a**2-b**2-c**2))
					if a**2 + b**2 + c**2 + d**2 == p: # see if (a,b,c,d) is viable
						A.append((a,b,c,d))
						if d != 0:
							A.append((a,b,c,-d))
		pickle.dump(A, open("LPS/Jacobi4/" + str(p) + ".p", "wb"))
		return A

# print(jacobi4(17))

class LPS:
	
	def __init__(self, p, q):
		# variables: seed; size; deg; graph
		# assert p in smallPrimes and q in smallPrimes
		assert type(p) is int and type(q) is int and p > 2 and q > 2 and p%4 == 1 and q%4 == 1 and isprime(p) and isprime(q), "p or q is not appropriate"
		
		if exists("LPS/Graphs/" + str(p) + "," + str(q) + ".p"):
			G = pickle.load(open("LPS/Graphs/" + str(p) + "," + str(q) + ".p", "rb"))
			self.size = G.size
			self.deg = G.deg
			self.graph = G.graph
		else:
			self.size = (q-1)*q*(q+1)/2
			self.deg = p+1
			
			iota = tonelli(-1, q)
			sqrtpinv = tonelli(pow(p,-1,q), q)
			pquadruples = jacobi4(p)
			# "standard form" for PSL2(Fq): flatten ((a,b),(c,d)) where a < q//2 and if a = 0 then b < q//2
			S = [((sqrtpinv * (a+b*iota)) % q, (sqrtpinv * (c+d*iota)) % q, (sqrtpinv * (-c+d*iota)) % q, (sqrtpinv * (a-b*iota)) % q) for (a,b,c,d) in pquadruples] # generating set, as elements of PSL2(Fq)
			V = [] # vertex set of X^p,q
			for b in range(1,1+q//2): # a = 0
				c = pow(-b,-1,q)
				for d in range(q):
					V.append((0,b,c,d))
			for a in range(1,1+q//2): # a > 0
				for b in range(q):
					for c in range(q):
						d = (1+b*c)*pow(a,-1,q) % q
						V.append((a,b,c,d))
			
			def qmul(X,Y): # multiply tuples (flattened 2x2 mats) mod q and use the standard form
				(a,b,c,d),(e,f,g,h) = X,Y
				(i,j,k,l) = ((a*e+b*g) % q, (a*f+b*h) % q, (c*e+d*g) % q, (c*f+d*h) % q)
				if i == 0:
					if j > q//2:
						return (0, -j % q, -k % q, -l % q)
					return (0, j, k, l)
				if i > q//2:
					return (-i % q, -j % q, -k % q, -l % q)
				return (i, j, k, l)
			
			self.graph = nx.Graph()
			for v in V:
				vString = str(v)
				for s in S:
					# sString = str(s)
					w = qmul(v, s)
					wString = str(w)
					self.graph.add_edge(vString, wString)
			pickle.dump(self, open("LPS/Graphs/" + str(p) + "," + str(q) + ".p", "wb"))

G = LPS(5,29)
print(G.graph.number_of_edges())
