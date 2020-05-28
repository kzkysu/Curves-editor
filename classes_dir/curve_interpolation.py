import matplotlib.pyplot as plt
from classes_dir.curve import Curve

class PolynomialInterpolation(Curve):
    curveType = 'Polynomial'
    def __init__(self,pointsPlot,linePlot,convexHull):
        super().__init__(pointsPlot,linePlot,convexHull)
        self.a = None

    def interpolate(self,xs,ys,w,t):
        n = len(xs)
        for i in range(n):
            if xs[i]==t:
                return ys[i]
        s1 = 0
        for i in range(n):
            s1 += w[i]/(t-xs[i])*ys[i]
        s2=0
        for i in range(n):
            s2 += w[i]/(t-xs[i])

        return s1/s2

    def Warner(self,xs):
        n = len(xs)-1 
        a = [[1]]
        for i in range(n+1):
            a[0].append(0)
        for i in range(1,n+1):
            a.append([])
            for j in range(i):
                a[i].append(a[i-1][j]/(xs[i]-xs[j]))
                a[j+1].append(a[j][i]-a[i][j])
        return a

    def funcY(self):
        i = 0 
        n = len(self.points[0])
        if n < 2:
            return [],[]
        lxs = []
        lys = []
        ts = self.chebyshev_nodes(n)
        #ts = self.regular_nodes(n)

        b = ts[0]
        e = ts[-1]
        for i in range(self.currentAccurancy):
            lxs.append(self.interpolate(ts,self.points[0],self.a[-1],b + (e-b)*i/(self.currentAccurancy-1)))
            lys.append(self.interpolate(ts,self.points[1],self.a[-1],b + (e-b)*i/(self.currentAccurancy-1)))
        return lxs,lys

    def calculate_function(self,flag):
        if flag != 'change_accurancy':
            n = len(self.points[0])
            ts = self.chebyshev_nodes(n)
            self.a = a = self.Warner(ts)

    def calculate_split(self,x,y,newCurve):
        linex = self.linePlot.get_xdata()
        liney = self.linePlot.get_ydata()
        np = self.find_point(x,y,linex,liney)
        xs = self.points[0]
        ys = self.points[1]
        x=linex[np]
        y=liney[np]

        n = len(self.points[0])
        m = len(linex)

        interval = (m + n-2)//(n-1)
        splitPoint = np//interval
        xs1 = xs[:splitPoint+1] + [x]
        xs2 = [x] + xs[splitPoint+1:]
        ys1 = ys[:splitPoint+1] + [y]
        ys2 = [y] + ys[splitPoint+1:]
        self.split_curve(newCurve,xs1,ys1,xs2,ys2,x,y)
