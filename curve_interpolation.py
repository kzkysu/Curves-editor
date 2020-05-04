import matplotlib.pyplot as plt
import curve

class PolynomialInterpolation(curve.Curve):
    curveType = 'polynomial interpolation'
    def __init__(self,pointsPlot,linePlot):
        super().__init__(pointsPlot,linePlot)

    def interpolate(self,xs,ys):
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

    def calculate_function(self):
        def foo(numberOfPoints):
            i = 0 
            n = len(self.points[0])
            if n < 2:
                return [],[]
            lxs = []
            lys = []
            ts = []
            for i in range(n):
                ts.append(i/(n-1))

            Lnx = self.interpolate(ts,self.points[0])
            Lny = self.interpolate(ts,self.points[1])
            for i in range(numberOfPoints):
                lxs.append(Lnx(i/(numberOfPoints-1)))
                lys.append(Lny(i/(numberOfPoints-1)))
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