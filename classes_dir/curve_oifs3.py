import matplotlib.pyplot as plt
from classes_dir.curve import Curve
import numpy as np

class OIFS3(Curve):
    curveType = 'OIFS3'
    def __init__(self,pointsPlot,linePlot,convexHull):
        super().__init__(pointsPlot,linePlot,convexHull)

    def interpolate(self,xs,ys):
        n = len(xs)

        d = np.zeros(n)
        h = np.zeros(n+1)
        l = np.zeros(n)

        for k in range(1,n):
            h[k] = xs[k]-xs[k-1]
        h[n] = h[1]

        for k in range(1,n-1):
            d[k] = 6/(h[k]+h[k+1])*((ys[k+1]-ys[k])/h[k+1] - (ys[k]-ys[k-1])/h[k])
        d[n-1] = 6/(h[n-1]+h[n])*((ys[1]-ys[n-1])/h[n] - (ys[n-1]-ys[n-2])/h[n-1])
        
        for k in range(1,n):
            l[k] = h[k]/(h[k]+h[k+1])

        p = np.zeros(n)
        q = np.zeros(n)
        s = np.zeros(n)
        s[0] = 1
        u = np.zeros(n)

        for k in range(1,n-1):
            p[k] = l[k]*q[k-1] + 2.0
            q[k] = (l[k]-1.0)/p[k]
            s[k] = -l[k]*s[k-1]/p[k]
            u[k] = (d[k]-l[k]*u[k-1])/p[k]

        t = np.zeros(n)
        t[n-1]=1
        v = np.zeros(n)

        for k in range(n-2,0,-1):
            t[k] = q[k]*t[k+1] + s[k]
            v[k] = q[k]*v[k+1] + u[k]

        m = np.zeros(n+1)
        m[n-1] = (d[n-1]-(1-l[n-1])*v[1] - l[n-1]*v[n-2])/(2+(1-l[n-1])*t[1]+l[n-1]*t[n-2])
        m[0] = m[n-1]
        for k in range(n-2, 0,-1):
            m[k] = v[k] + t[k]*m[k+1]
        m[n] = m[1]
        return m,h


    def calculate_function(self):
        def foo(numberOfPoints):
            n = len(self.points[0])
            if n<2:
                return [],[]
            ts = self.regular_nodes(n)
            mx,hx = self.interpolate(ts,self.points[0])
            my,hy = self.interpolate(ts,self.points[1])
            lxs = []
            lys = []

            k = 1
            xs = self.points[0]
            ys = self.points[1]
            for i in range(numberOfPoints):
                x = i/(numberOfPoints-1)
                if x > ts[k]:
                    k += 1
                sx = (1/hx[k])*(1/6*mx[k-1]*(ts[k]-x)**3
                 + (1/6)*mx[k]*(x - ts[k-1])**3 
                 + (xs[k-1] - (1/6)*mx[k-1]*hx[k]**2)*(ts[k]-x)
                 + (xs[k]- (1/6)*mx[k]*hx[k]**2)*(x-ts[k-1]))
                sy = (1/hy[k])*(1/6*my[k-1]*(ts[k]-x)**3
                 + (1/6)*my[k]*(x - ts[k-1])**3 
                 + (ys[k-1] - (1/6)*my[k-1]*hy[k]**2)*(ts[k]-x)
                 + (ys[k]- (1/6)*my[k]*hy[k]**2)*(x-ts[k-1])) 
                lxs.append(sx)
                lys.append(sy)
            return lxs,lys
        return foo

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
