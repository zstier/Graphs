

def combinations(n, r): # adapted from geeksforgeeks.com
	data = list(range(r))
	ans = []
	def combinationUtil(arr, n, r, index, data, i):
		if(index == r):
			"""
			for j in range(r):
				print(data[j], end = " ")
			print(" ")
			"""
			ans.append([j for j in data])
			return

		if(i >= n):
			return

		data[index] = arr[i]
		combinationUtil(arr, n, r, index + 1, data, i + 1)
		
		combinationUtil(arr, n, r, index, data, i + 1)
		
	combinationUtil(range(n), n, r, 0, data, 0)
	return ans
