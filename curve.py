import matplotlib.pyplot as plt
import numerical_algorithm as num

class Curve:
    counter = 0
    def __init__(self,pointsPlot,linePlot):
        self.name = "Curve " + str(Curve.counter)
        Curve.counter += 1
        self.linePlot = linePlot
        self.pointsPlot = pointsPlot
        self.numberOfPoints = 0

    def add_point(self,x,y):
        self.numberOfPoints += 1

        xs = list(self.pointsPlot[0].get_xdata())
        ys = list(self.pointsPlot[0].get_ydata())

        xs.append(x)
        ys.append(y)

        self.pointsPlot[0].set_data(xs,ys)
        self.linePlot[0].set_data(num.polygonal_chain(xs,ys))

    def delete_point(self,x,y):
        self.numberOfPoints -= 1

        xs = list(self.pointsPlot[0].get_xdata())
        ys = list(self.pointsPlot[0].get_ydata())

        i = self.find_point(x,y,xs,ys)
        del xs[i]
        del ys[i]

        self.pointsPlot[0].set_data(xs,ys)
        self.linePlot[0].set_data(num.polygonal_chain(xs,ys))


    def find_point(self,x,y,xs,ys):
        minDistance = 100000000000000
        pointer = -1
        for i in range(self.numberOfPoints):
            if (x-xs[i])**2 + (y-ys[i])**2 < minDistance:
                minDistance = (x-xs[i])**2 + (y-ys[i])**2
                pointer = i
        return pointer


