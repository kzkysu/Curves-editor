import matplotlib.pyplot as plt
import numerical_algorithm as num
import math as m

class Curve:
    counter = 0
    def __init__(self,pointsPlot,linePlot,curveType):
        self.name = "Curve " + str(Curve.counter)
        Curve.counter += 1
        self.linePlot = linePlot[0]
        self.pointsPlot = pointsPlot[0]
        self.points = {'xs':[],'ys':[]}
        self.curveType = curveType
        self.numberOfPoints = 0
        self.activePoint = None

    def get_points_label(self):
        return self.pointsPlot.get_label()

    def add_point(self,x,y):
        self.numberOfPoints += 1

        self.points['xs'].append(x)
        self.points['ys'].append(y)

        self.update_plots()

    def delete_point(self,x,y):
        i = self.find_point(x,y)
        del self.points['xs'][i]
        del self.points['ys'][i]

        self.numberOfPoints -= 1

        self.update_plots()

    def activate_point(self,x,y):
        self.activePoint = self.find_point(x,y)

    def disactivate_point(self):
        self.activePoint = None

    def move_point(self,x,y):
        if self.activePoint != None:
            self.points['xs'][self.activePoint] = x
            self.points['ys'][self.activePoint] = y
            self.update_plots()

    def move_curve(self,x,y):
        x /= 2
        y /= 2
        for i in range(self.numberOfPoints):
            self.points['xs'][i] += x
        for i in range(self.numberOfPoints):
            self.points['ys'][i] += y

        linex = self.linePlot.get_xdata()
        liney = self.linePlot.get_ydata()

        for i in range(self.numberOfPoints):
            linex[i] += x
        for i in range(self.numberOfPoints):
            liney[i] += y

        self.pointsPlot.set_data(self.points['xs'],self.points['ys'])
        self.linePlot.set_data(linex,liney)

    def rotate_points(self,x,y,angle):
        return x*m.cos(angle) - y*m.sin(angle), x*m.sin(angle) + y*m.cos(angle)


    def rotate_curve(self,angle):
        angle = m.radians(angle)

        linex = self.linePlot.get_xdata()
        liney = self.linePlot.get_ydata()

        for i in range(self.numberOfPoints):
            self.points['xs'][i],self.points['ys'][i]  = self.rotate_points(self.points['xs'][i],self.points['ys'][i],angle)

        for i in range(self.numberOfPoints):
            linex[i], liney[i] = self.rotate_points(linex[i],liney[i],angle)

        self.pointsPlot.set_data(self.points['xs'],self.points['ys'])
        self.linePlot.set_data(linex,liney)


    def update_plots(self):
        self.pointsPlot.set_data(self.points['xs'],self.points['ys'])
        self.linePlot.set_data(num.functionDict[self.curveType](self.points['xs'],self.points['ys']))

    def find_point(self,x,y):
        minDistance = 100000000000000
        pointer = -1
        xs = self.points['xs']
        ys = self.points['ys']
        for i in range(self.numberOfPoints):
            if (x-xs[i])**2 + (y-ys[i])**2 < minDistance:
                minDistance = (x-xs[i])**2 + (y-ys[i])**2
                pointer = i
        return pointer

    def delete_curve(self):
        self.linePlot.remove()
        del self.linePlot
        self.pointsPlot.remove()
        del self.pointsPlot


