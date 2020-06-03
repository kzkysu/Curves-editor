from classes_dir.curve import Curve
from classes_dir.curve_bezier_menu import BezierCurveMenu
import math as mth
import numpy as np

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

    def update_plots_extended(self,flag=None):
        super().update_plots_extended(flag=flag)
        Bezier.extraMenu.set_entryDegree_text(str(self.numberOfPoints))

    def degree_up(self,d):
        if d <= self.numberOfPoints:
            return
        else:
            d = d - self.numberOfPoints
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

    @staticmethod
    def operator_delta(r,cs,i):
        dc = 0
        nr = 1
        for j in range(r):
            dc += nr * (-1)**j * cs[i+r-j]
            nr *= (r-j)/(j+1)
        return dc

    @staticmethod
    def newt(n,k):
        return mth.factorial(n)/mth.factorial(k)/mth.factorial(n-k)

    def degree_down(self,d,k,l):
        if d >= self.numberOfPoints or k+l > self.numberOfPoints:
            print("Wrong arguments for degree down.")
            return
        else:
            d = d - self.numberOfPoints
        xs = []
        ys = []
        p1 = self.points[0]
        p2 = self.points[1]

        n = self.numberOfPoints-1
        m = n-d
        self.numberOfPoints += d 

        r1 = np.zeros(m+1)
        r2 = np.zeros(m+1)
        r1t = np.zeros(m+1)
        r2t = np.zeros(m+1)

        nn = 1
        nm = 1
        nh = 1
        for i in range(k):
            r1sum = 0
            r2sum = 0
            r1sumt = 0
            r2sumt = 0

            for h in range(i):
                r1sum += (-1)**(i+h)*nh*r1[h]
                r2sum += (-1)**(i+h)*nh*r2[h]
                r1sumt += (-1)**(i+h)*Bezier.newt(i,h)*r1t[h]
                r2sumt += (-1)**(i+h)*Bezier.newt(i,h)*r2t[h]
                nh *= (i-h)/(h+1)

            r1[i]= nn/nm * Bezier.operator_delta(i,p1,0) - r1sum
            r2[i]= nn/nm * Bezier.operator_delta(i,p2,0) - r2sum
            r1t[i]= Bezier.newt(n,i)/Bezier.newt(m,i) * Bezier.operator_delta(i,p1,0) - r1sumt
            r2t[i]= Bezier.newt(n,i)/Bezier.newt(m,i) * Bezier.operator_delta(i,p2,0) - r2sumt
            nn *= (n-i)/(i+1)
            nm *= (m-i)/(i+1)

        nn = 1
        nm = 1
        nh = 1
        for i in range(l):
            r1sum = 0
            r2sum = 0
            for h in range(i):
                r1sum += (-1)**i*nh*r1[m-i+h]
                r2sum += (-1)**i*nh*r2[m-i+h]
                nh *= (i-h)/(h+1)

            r1[m-i]= (-1)**i * nn/nm * Bezier.operator_delta(i,p1,n-i) - r1sum
            r2[m-i]= (-1)**i * nn/nm * Bezier.operator_delta(i,p2,n-i) - r2sum
            nn *= (n-i)/(i+1)
            nm *= (m-i)/(i+1)

        print(r1,r1t)

        
        '''self.points[0] = xs
        self.points[1] = ys
        self.set_numbers()
        self.update_plots_extended()'''