import matplotlib.pyplot as plt
import numerical_algorithm as num

class Curve:
    counter = 0
    def __init__(self,pointsPlot,linePlot,curveType):
        self.name = "Curve " + str(Curve.counter)
        Curve.counter += 1
        self.linePlot = linePlot
        self.pointsPlot = pointsPlot
        self.points = {'xs':[],'ys':[]}
        self.curveType = curveType
        self.numberOfPoints = 0
        self.activePoint = None

    def add_point(self,x,y):
        self.numberOfPoints += 1

        self.points['xs'].append(x)
        self.points['ys'].append(y)

        self.update_plots()

    def delete_point(self,x,y):
        self.numberOfPoints -= 1

        i = self.find_point(x,y)
        del self.points['xs'][i]
        del self.points['ys'][i]

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

    def update_plots(self):
        self.pointsPlot[0].set_data(self.points['xs'],self.points['ys'])
        self.linePlot[0].set_data(num.functionDict[self.curveType](self.points['xs'],self.points['ys']))

    def find_point(self,x,y):
        minDistance = 100000000000000
        pointer = -1
        xs = self.points['xs']
        ys = self.points['ys']
        for i in range(self.numberOfPoints + 1):
            if (x-xs[i])**2 + (y-ys[i])**2 < minDistance:
                minDistance = (x-xs[i])**2 + (y-ys[i])**2
                pointer = i
        return pointer


