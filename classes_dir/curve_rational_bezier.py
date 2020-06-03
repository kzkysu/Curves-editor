from classes_dir.curve import Curve
from classes_dir.curve_rational_bezier_points_menu import RationalBezierPointsMenu
import math as mth
import numpy as np

class RationalBezier(Curve):
    curveType = 'RationalBezier'
    extraPointsMenu = RationalBezierPointsMenu()

    def __init__(self,pointsPlot,linePlot,convexHull):
        super().__init__(pointsPlot,linePlot,convexHull)
        self.calculatedAccurancy = None
        self.wg = [1,1]
        self.ws = None
        self.wgs = None

    def de_Casteljou(self,p,r,t):
        n = len(p)
        w = []
        g = []
        w.append(p)
        g.append(r)
        for k in range(n-1):
            w.append([])
            g.append([])
            for i in range(n-k-1):
                g[k+1].append( (1-t)*g[k][i] + t*g[k][i+1] )
                w[k+1].append( (1-t)*g[k][i]/g[k+1][i]*w[k][i] + t*g[k][i+1]/g[k+1][i]*w[k][i+1] )
        return w,g

    def de_Casteljou_step(self,w,g,t):
        n = len(w)
        w.append([])
        g.append([])

        for i in range(n):
            g[i+1].append( (1-t)*g[i][-2] + t*g[i][-1] )
            w[i+1].append( (1-t)*g[i][-2]/g[i+1][-1]*w[i][-2] + t*g[i][-1]/g[i+1][-1]*w[i][-1] )

        return w,g


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
            self.wg.append(1)
            
            for i in range(numberOfPoints):
                x = i/(numberOfPoints-1)
                self.ws[0][i],self.wgs[0][i]=self.de_Casteljou_step(self.ws[0][i],self.wgs[0][i],x)
                self.ws[1][i],self.wgs[1][i]=self.de_Casteljou_step(self.ws[1][i],self.wgs[1][i],x)

        else:
            if n<2:
                return
            numberOfPoints = self.currentAccurancy

            self.ws = [[],[]]
            self.wgs = [[],[]]

            for i in range(numberOfPoints):
                x = i/(numberOfPoints-1)

                aws,ags = self.de_Casteljou(self.points[0],self.wg,x)
                self.ws[0].append(aws)
                self.wgs[0].append(ags)

                aws,ags = self.de_Casteljou(self.points[1],self.wg,x)
                self.ws[1].append(aws)
                self.wgs[1].append(ags)

    def calculate_split(self,x,y,newCurve):
        pass

    def split_curve(self,newCurve,xs1,ys1,xs2,ys2,x,y):
        pass

    def change_weight(self,wgh):
        if self.activePoint != None:
            self.wg = wgh
        self.update_plot_extended()

    def get_weight(self,i):
        return self.wg[i]

    def set_weight(self,i,x):
        self.wg[i] = x
        self.update_plots_extended()