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

    def Horner(self,p,t):
        n = len(p)-1
        
        if t <= 0.5:
            y = p[-1]
            x=t/(1-t)
            for i in range(n):
                y *= x*(i+1)/(n-i)
                y += p[n-i-1]
            return y*(1-t)**n
        else:
            y= p[0]
            x=(1-t)/t
            for i in range(n):
                y *= x*(i+1)/(n-i)
                y += p[i+1]
            return y*t**n

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

        if self.ws != None:
            for i in range(numberOfPoints):
                x = i/(numberOfPoints-1)
                lxs.append(self.ws[0][i][-1][0])
                lys.append(self.ws[1][i][-1][0])

        else:
            for i in range(numberOfPoints):
                x = i/(numberOfPoints-1)
                lxs.append(self.Horner(self.points[0],x))
                lys.append(self.Horner(self.points[1],x))

        return lxs,lys

    def calculate_function(self,flag):
        n = len(self.points[0])
        if flag == 'added_point' and n>2:
            if self.ws != None:
                #print("Casteljou step")
                numberOfPoints = self.currentAccurancy
                
                for i in range(numberOfPoints):
                    x = i/(numberOfPoints-1)
                    self.ws[0][i]=self.de_Casteljou_step(self.ws[0][i],x)
                    self.ws[1][i]=self.de_Casteljou_step(self.ws[1][i],x)
            else:
                #print("Casteljou")
                numberOfPoints = self.currentAccurancy
                self.ws = [[],[]]

                for i in range(numberOfPoints):
                    x = i/(numberOfPoints-1)
                    self.ws[0].append(self.de_Casteljou(self.points[0],x))
                    self.ws[1].append(self.de_Casteljou(self.points[1],x))

        else:
            if n<2:
                return
            #print("Horner")
            self.ws = None
 


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

        self.split_curve(newCurve,xs1,ys1,xs2,ys2)

    def split_curve(self,newCurve,xs1,ys1,xs2,ys2):
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

    def align_curve(self,newFX,newFY):
        if self.numberOfPoints > 0:
            x = newFX - self.points[0][0]
            y = newFY - self.points[1][0]
            self.move_curve(x,y)

    def join_curve(self,toJoin):
        n = self.numberOfPoints
        m = toJoin.numberOfPoints
        if n > 1 and m > 1:
            toJoin.align_curve(self.points[0][-1],self.points[1][-1])

            toJoin.points[0][1] = ((m+n-2)*self.points[0][-1] - (n-1)*self.points[0][-2])/(m-1)
            toJoin.points[1][1] = ((m+n-2)*self.points[1][-1] - (n-1)*self.points[1][-2])/(m-1)

            for i in range(1,m):
                self.points[0].append(toJoin.points[0][i])
                self.points[1].append(toJoin.points[1][i])

            self.numberOfPoints = n+m-1
            self.set_numbers()
            self.update_plots_extended()
        else:
            print("Both curves must have at least two points.")

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

    def degree_down(self,d):
        if d >= self.numberOfPoints:
            print("Wrong arguments for degree down.")
            return

        n = self.numberOfPoints
        for i in range(n-d):
            self.degree_step_down()
        #print(self.points[0])

        self.set_numbers()
        self.update_plots_extended()


    def degree_step_down(self):
        n = self.numberOfPoints-1
        if n > 2:
            p1 = self.points[0]
            p2 = self.points[1]
            m = int(n/2)+1
            r = m-1+(n%2)

            w1i = np.zeros(m)
            w2i = np.zeros(m)
            w1ii = np.zeros(m)
            w2ii = np.zeros(m)

            w1i[0] = p1[0]
            w2i[0] = p2[0]

            w1ii[r-1] = p1[n]
            w2ii[r-1] = p2[n]

            for k in range(1,m):
                w1i[k] = (1+k/(n-k))*p1[k] - k/(n-k)*w1i[k-1]
                w2i[k] = (1+k/(n-k))*p2[k] - k/(n-k)*w2i[k-1]
                w1ii[r-k-1] = (n/(n-k))*p1[n-k] + (1 - n/(n-k))*w1ii[r-k]
                w2ii[r-k-1] = (n/(n-k))*p2[n-k] + (1 - n/(n-k))*w2ii[r-k]

            w1ii[0] = (w1ii[0] + w1i[m-1])/2
            w2ii[0] = (w2ii[0] + w2i[m-1])/2

        p1 = []
        p2 = []
        for i in range(r-(n%2)):
            p1.append(w1i[i])
            p2.append(w2i[i])
        for i in range(r):
            p1.append(w1ii[i])
            p2.append(w2ii[i])

        self.points[0] = p1
        self.points[1] = p2
        self.numberOfPoints = n

    ''' @staticmethod
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

    @staticmethod
    def pochhammer(c,i):
        p = 1
        while i > 0:
            p *= c
            c += 1
            i -= 1
        return p

    def degree_down_todo(self,d,k,l):
        if d >= self.numberOfPoints or k+l > self.numberOfPoints:
            print("Wrong arguments for degree down.")
            print(d,k+l,self.numberOfPoints)
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

        print("halo?")

        v1t = np.zeros(n-l-k+1)
        v2t = np.zeros(n-l-k+1) 
        for i in range(k,n-l+1):
            v1t[i-k] = Bezier.pochhammer(2*l+1,m-l-i)*Bezier.pochhammer(2*k+1,i-k)
            v2t[i-k] = v1t[i-k]
            s1 = Bezier.newt(n,i)
            s2 = s1
            s1 *= p1[i]
            s2 *= p2[i]
            for h in range(k):
                if h > i or h > m or n-m < i-h:
                    break
                s1 -= Bezier.newt(n-m,i-h)*Bezier.newt(m,h)*r1[h]
                s2 -= Bezier.newt(n-m,i-h)*Bezier.newt(m,h)*r2[h]
            for h in range(m-l+1,m+1):
                if h > i or h > m or n-m < i-h:
                    break
                s1 -= Bezier.newt(n-m,i-h)*Bezier.newt(m,h)*r1[h]
                s2 -= Bezier.newt(n-m,i-h)*Bezier.newt(m,h)*r2[h]
            v1t[i-k]*=s1
            v2t[i-k]*=s2

        print(r1,v1t)'''

        
'''self.points[0] = xs
        self.points[1] = ys
        self.set_numbers()
        self.update_plots_extended()'''