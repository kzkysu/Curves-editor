from classes_dir.curve import Curve
from classes_dir.curve_bezier_menu import BezierCurveMenu
import math as mth

class Bezier(Curve):
    curveType = 'Bezier'
    extraMenu = BezierCurveMenu()
    def __init__(self,pointsPlot,linePlot,convexHull):
        super().__init__(pointsPlot,linePlot,convexHull)
        self.calculatedAccurancy = None
        self.ws = None

    def de_Casteljou(self,p,t):
        n = len(p)
        w = []
        w.append(p)
        for k in range(n-1):
            w.append([])
            for i in range(n-k-1):
                w[k+1].append( (1-t)*w[k][i] + t*w[k][i+1] )
        return w

    def de_Casteljou_step(self,w,t):
        n = len(w)
        w.append([])

        for i in range(n):
            w[i+1].append( (1-t)*w[i][-2] + t*w[i][-1] )

        return w


    def funcY(self):
        n = len(self.points[0])
        if n<2:
            return [],[]

        numberOfPoints = self.currentAccurancy
        lxs = []
        lys = []

        for i in range(numberOfPoints):
            x = i/(numberOfPoints-1)
            lxs.append(self.ws[0][i][-1][0])
            lys.append(self.ws[1][i][-1][0])
        return lxs,lys

    def calculate_function(self,flag):
        n = len(self.points[0])
        if flag == 'added_point' and n>2:
            numberOfPoints = self.currentAccurancy
            
            for i in range(numberOfPoints):
                x = i/(numberOfPoints-1)
                self.ws[0][i]=self.de_Casteljou_step(self.ws[0][i],x)
                self.ws[1][i]=self.de_Casteljou_step(self.ws[1][i],x)

        else:
            if n<2:
                return
            numberOfPoints = self.currentAccurancy

            self.ws = [[],[]]

            for i in range(numberOfPoints):
                x = i/(numberOfPoints-1)
                self.ws[0].append(self.de_Casteljou(self.points[0],x))
                self.ws[1].append(self.de_Casteljou(self.points[1],x))

    def calculate_split(self,x,y,newCurve):
        n = len(self.points[0])
        xs1 = []
        ys1 = []
        xs2 = []
        ys2 = []

        np = self.find_point(x,y,self.linePlot.get_xdata(),self.linePlot.get_ydata())
        numberOfPoints = self.currentAccurancy

        w1 = self.de_Casteljou(self.points[0],np/(numberOfPoints-1))
        w2 = self.de_Casteljou(self.points[1],np/(numberOfPoints-1))

        for i in range(n):
            xs1.append(w1[i][0])
            xs2.append(w1[i][-1])
            ys1.append(w2[i][0])
            ys2.append(w2[i][-1])

        self.split_curve(newCurve,xs1,ys1,xs2,ys2,x,y)

    def split_curve(self,newCurve,xs1,ys1,xs2,ys2,x,y):
        n = len(xs1)-1

        self.points[0] = xs1
        self.points[1] = ys1
        self.numberOfPoints = len(xs1)

        self.set_numbers()
        self.update_plots_extended()

        self.paste_curve_settings(newCurve)
        newCurve.points[0] = xs2
        newCurve.points[1] = ys2
        newCurve.numberOfPoints = len(xs2)

        newCurve.set_numbers()
        newCurve.update_plots_extended()

    def change_degree(self,d):
        if d > self.numberOfPoints:
            self.degree_up(d-self.numberOfPoints)

    def update_plots_extended(self,flag=None):
        super().update_plots_extended(flag=flag)
        Bezier.extraMenu.set_entry_text(str(self.numberOfPoints))

    def degree_up(self,d):
        xs = []
        ys = []

        n = self.numberOfPoints-1
        self.numberOfPoints += d

        df = mth.factorial(d)
        dn = mth.factorial(n)
        nd = 1

        for i in range(self.numberOfPoints):
            w1 = 0
            w2 = 0
            nk = 1
            if d > i:
                dk = df/mth.factorial(i)/mth.factorial(d-i)
            else:
                dk = 1
            if i-d > 0:
                nk = dn/mth.factorial(i-d)/mth.factorial(n-i+d)
            for k in range(max(0,i-d),min(n+1,i+1)):
                w1 += self.points[0][k]*nk*dk
                w2 += self.points[1][k]*nk*dk
                nk *= (n-k)/(k+1)
                if d-i+k+1 > 0:
                    dk *= (i-k)/(d-i+k+1)
                else:
                    dk = 1
            xs.append(w1/nd)
            ys.append(w2/nd)
            nd *= (n+d-i)/(i+1)
        
        self.points[0] = xs
        self.points[1] = ys
        self.set_numbers()
        self.update_plots_extended()