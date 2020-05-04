import matplotlib.pyplot as plt
from curve import Curve

class PolygonalChain(Curve):
    curveType = 'polygonal chain'
    def __init__(self,pointsPlot,linePlot):
        super().__init__(pointsPlot,linePlot)

    def calculate_function(self):
        def foo(numberOfPoints):
            i = 0 
            n = len(self.points[0])
            if n < 2:
                return [],[]
            m = int(numberOfPoints/(n-1))
            lxs = []
            lys = []
            for i in range(n-1):
                if i == n-2:
                    m = numberOfPoints - m*(n-2)
                for j in range(m):
                    lxs.append(self.points[0][i] + (j+1)/m * (self.points[0][i+1] - self.points[0][i]))
                    lys.append(self.points[1][i] + (j+1)/m * (self.points[1][i+1] - self.points[1][i]))
            return lxs,lys
        return foo

    def calculate_split(self,x,y,newCurve):
        linex = self.linePlot.get_xdata()
        liney = self.linePlot.get_ydata()
        np = self.find_point(x,y,linex,liney)
        x = linex[np]
        y = liney[np]
        xs = self.points[0]
        ys = self.points[1]

        n = len(self.points[0])
        m = len(linex)

        interval = (m + n-2)//(n-1)
        splitPoint = np//interval
        xs1 = xs[:splitPoint+1] + [x]
        xs2 = [x] + xs[splitPoint+1:]
        ys1 = ys[:splitPoint+1] + [y]
        ys2 = [y] + ys[splitPoint+1:]
        self.split_curve(newCurve,xs1,ys1,xs2,ys2,x,y)
    