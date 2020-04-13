

def polygonal_chain(xs,ys):
	def foo(number_of_points):
		i = 0 
		n = len(xs)
		if n < 2:
			return [],[]
		m = int(number_of_points/(n-1))
		lxs = []
		lys = []
		for i in range(n-1):
			if i == n-2:
				m = number_of_points - m*(n-2)
			for j in range(m):
				lxs.append(xs[i] + (j+1)/m * (xs[i+1] - xs[i]))
				lys.append(ys[i] + (j+1)/m * (ys[i+1] - ys[i]))
		return lxs,lys
	return foo


functionDict = {'polygonal_chain':polygonal_chain}

