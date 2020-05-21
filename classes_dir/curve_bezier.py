from classes_dir.curve import Curve


class Bezier(Curve):
    curveType = 'Bezier'
    def __init__(self,pointsPlot,linePlot,convexHull):
        super().__init__(pointsPlot,linePlot,convexHull)

    def de_Casteljou(self,p,t):
        n = len(p)
        w = []
        w.append(p)
        for k in range(n-1):
            w.append([])
            for i in range(n-k-1):
                w[k+1].append( (1-t)*w[k][i] + t*w[k][i+1] )
        return w

    def calculate_function(self):
        def foo(numberOfPoints):
            n = len(self.points[0])
            if n<2:
                return [],[]

            lxs = []
            lys = []

            for i in range(numberOfPoints):
               x = i/(numberOfPoints-1)
               lxs.append(self.de_Casteljou(self.points[0],x)[-1][0])
               lys.append(self.de_Casteljou(self.points[1],x)[-1][0])
            return lxs,lys
        return foo

    def calculate_split(self,x,y,newCurve):
        pass
