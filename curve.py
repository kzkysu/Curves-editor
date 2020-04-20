import matplotlib.pyplot as plt
import numerical_algorithm as num
import math as m
import json

class Curve:
    counter = 0
    def __init__(self,pointsPlot,linePlot,curveType):
        self.name = "Curve " + str(Curve.counter)
        self.accurancy = 10000
        self.workingAccurancy = 1000
        self.currentAccurancy = self.accurancy
        Curve.counter += 1
        self.linePlot = linePlot[0]
        self.pointsPlot = pointsPlot[0]
        self.texts = []
        self.points = {'xs':[],'ys':[]}
        self.curveType = curveType
        self.numberOfPoints = 0
        self.activePoint = None
        self.funcY = None
        self.color = None
        self.width = None
        self.pointsVisible = True
        self.numbersVisble = False

    def load_from_file(self,path):
        try:
            with open(path,'r') as ifile:
                data = json.load(ifile)
            self.name = data['name']
            self.accurancy = data['accurancy']
            self.points = {'xs': data['pointsxs'],'ys': data['pointsys']}
            self.curveType = data['type']
            self.numberOfPoints = len(self.points['xs'])
            self.color = data['color']
            self.width = data['width']
            self.texts = []
            for i in self.numberOfPoints:
                self.texts.append(points['xs'][i],points['ys'][i])
            self.update_plots_extended()

        except:
            print("Failed reading curve from file: " + path )

    def change_type(self,curveType):
        self.curveType = curveType
        self.update_plots_extended()

    def get_points_label(self):
        return self.pointsPlot.get_label()

    def update_plots_extended(self):
        self.pointsPlot.set_data(self.points['xs'],self.points['ys'])
        self.funcY = num.functionDict[self.curveType](self.points['xs'],self.points['ys'])
        lxs,lys = self.funcY(self.accurancy)
        self.linePlot.set_data(lxs,lys)

    def update_plots(self,lxs,lys):
        self.pointsPlot.set_data(self.points['xs'],self.points['ys'])
        self.linePlot.set_data(lxs,lys)

    def add_point(self,x,y):
        self.numberOfPoints += 1

        self.points['xs'].append(x)
        self.points['ys'].append(y)
        self.texts.append(plt.text(self.points['xs'][-1],self.points['ys'][-1],self.numberOfPoints.__str__()))
        self.texts[-1].set_visible(self.numbersVisble)

        self.update_plots_extended()

    def delete_point(self,x,y):
        i = self.find_point(x,y)
        del self.points['xs'][i]
        del self.points['ys'][i]
        self.texts[i].remove()
        del self.texts[i]

        for j in range(i,self.numberOfPoints-1):
            self.texts[j].set_text(j+1)

        self.numberOfPoints -= 1

        self.update_plots_extended()

    def activate_point(self,x,y):
        self.activePoint = self.find_point(x,y)

    def disactivate_point(self):
        self.activePoint = None

    def move_point(self,x,y):
        if self.activePoint != None:
            self.points['xs'][self.activePoint] = x
            self.points['ys'][self.activePoint] = y
            self.texts[self.activePoint].set_position((x,y))
            self.update_plots_extended()

    def move_curve(self,x,y):
        for i in range(self.numberOfPoints):
            self.points['xs'][i] += x
            self.points['ys'][i] += y
        for i in range(self.numberOfPoints):
            oldx, oldy = self.texts[i].get_position()
            self.texts[i].set_position((oldx+x,oldy+y))

        linex = self.linePlot.get_xdata()
        liney = self.linePlot.get_ydata()


        for i in range(self.accurancy):
            linex[i] += x
        for i in range(self.accurancy):
            liney[i] += y

        self.update_plots(linex,liney)

    def scale_point(self,xf,yf,x,y,scale):
        x = xf + (x-xf)*scale
        y = yf + (y-yf)*scale
        return x,y

    def resize_curve(self,scale):
        linex = self.linePlot.get_xdata()
        liney = self.linePlot.get_ydata()

        xf,yf = self.points['xs'][0],self.points['ys'][0]

        for i in range(self.numberOfPoints-1):
            self.points['xs'][i+1],self.points['ys'][i+1]  = self.scale_point(xf,yf,self.points['xs'][i+1],self.points['ys'][i+1],scale)
            self.texts[i].set_position((self.points['xs'][i+1],self.points['ys'][i+1]))

        for i in range(self.accurancy-1):
            linex[i+1], liney[i+1] = self.scale_point(xf,yf,linex[i+1],liney[i+1],scale)

        self.update_plots(linex,liney)

    def rotate_points(self,x,y,angle,s,t):
        return (x-s)*m.cos(angle) - (y-t)*m.sin(angle) + s, (x-s)*m.sin(angle) + (y-t)*m.cos(angle) + t


    def rotate_curve(self,angle,s,t):
        angle = m.radians(angle)

        linex = self.linePlot.get_xdata()
        liney = self.linePlot.get_ydata()

        for i in range(self.numberOfPoints):
            self.points['xs'][i],self.points['ys'][i]  = self.rotate_points(self.points['xs'][i],self.points['ys'][i],angle,s,t)
            self.texts[i].set_position((self.points['xs'][i],self.points['ys'][i]))

        for i in range(self.accurancy):
            linex[i], liney[i] = self.rotate_points(linex[i],liney[i],angle,s,t)

        self.update_plots(linex,liney)

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
        for i in range(self.numberOfPoints):
            self.texts[i].remove()
        del self.texts
        self.linePlot.remove()
        del self.linePlot
        self.pointsPlot.remove()
        del self.pointsPlot

    def save_to_file(self,path):
        data = {}
        data['name'] = self.name
        data['width'] = self.width
        data['type'] = self.curveType
        data['accurancy'] = self.accurancy
        data['color'] = self.color
        data['pointsxs'] = self.points['xs']
        data['pointsys'] = self.points['ys']

        with open(path,'w') as ofile:
            json.dump(data,ofile)

    def hide_points(self):
        self.pointsPlot.set_visible(False)
        self.pointsVisible = False

    def show_points(self):
        self.pointsPlot.set_visible(True)
        self.pointsVisible = True

    def hide_curve(self):
        self.pointsPlot.set_visible(False)
        self.linePlot.set_visible(False)

    def show_curve(self):
        self.pointsPlot.set_visible(self.pointsVisible)
        self.linePlot.set_visible(True)

    def show_numbers(self):
        for i in range(self.numberOfPoints):
            self.texts[i].set_visible(True)
        self.numbersVisble = True

    def hide_numbers(self):
        for i in range(self.numberOfPoints):
            self.texts[i].set_visible(False)
        self.numbersVisble = False

    def set_working_accurancy(self):
        self.currentAccurancy = self.workingAccurancy

    def set_normal_accurancy(self):
        self.currentAccurancy = self.accurancy
