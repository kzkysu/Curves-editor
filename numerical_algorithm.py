
def polygonal_chain(xs,ys):
	def foo(numberOfPoints):
		i = 0 
		n = len(xs)
		if n < 2:
			return [],[]
		m = int(numberOfPoints/(n-1))
		lxs = []
		lys = []
		for i in range(n-1):
			if i == n-2:
				m = numberOfPoints - m*(n-2)
			for j in range(m):
				lxs.append(xs[i] + (j+1)/m * (xs[i+1] - xs[i]))
				lys.append(ys[i] + (j+1)/m * (ys[i+1] - ys[i]))
		return lxs,lys
	return foo

def interpolate(xs,ys):
	def foo(t):
		n = len(xs)-1 
		for i in range(n+1):
			if xs[i]==t:
				return ys[i]
		a = [[1]]
		for i in range(n+1):
			a[0].append(0)
		n = len(xs)-1 
		for i in range(1,n+1):
			a.append([])
			for j in range(i):
				a[i].append(a[i-1][j]/(xs[i]-xs[j]))
				a[j+1].append(a[j][i]-a[i][j])
		n = len(xs)
		s1 = 0
		for i in range(n):
			s1 += a[n-1][i]/(t-xs[i])*ys[i]
		s2=0
		for i in range(n):
			s2 += a[n-1][i]/(t-xs[i])

		return s1/s2
	return foo

def polynomial_interpolation(xs,ys):
	def foo(numberOfPoints):
		i = 0 
		n = len(xs)
		if n < 2:
			return [],[]
		lxs = []
		lys = []
		ts = []
		for i in range(n):
			ts.append(i/(n-1))

		Lnx = interpolate(ts,xs)
		Lny = interpolate(ts,ys)
		for i in range(numberOfPoints):
			lxs.append(Lnx(i/(numberOfPoints-1)))
			lys.append(Lny(i/(numberOfPoints-1)))
		return lxs,lys
	return foo

	
def polynomial_interpolation_split(xs,ys,dxs,dys,np):
	pass



functionDict = {'polygonal_chain':polygonal_chain,
				'polynomial_interpolation':polynomial_interpolation}

def get_curves_types():
	return functionDict.keys()

