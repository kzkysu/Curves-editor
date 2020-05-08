import matplotlib.pyplot as plt
import math as m
import json

class Curve:
    counter = 0
    curveType = None
    def __init__(self,pointsPlot,linePlot):
        self.name = "Curve " + str(Curve.counter)
        self.accurancy = 10000
        self.workingAccurancy = 100
        self.currentAccurancy = self.accurancy
        Curve.counter += 1
        self.linePlot = linePlot[0]
        self.pointsPlot = pointsPlot[0]
        self.texts = []
        self.points = [list(),list()]
        self.numberOfPoints = 0
        self.activePoint = None
        self.funcY = None
        self.color = None
        self.width = None
        self.pointsVisible = True
        self.numbersVisible = False
        self.visible = True 

    def load_from_file(self,path):
        try:
            with open(path,'r') as ifile:
                data = json.load(ifile)
            self.name = data['name']
            self.accurancy = data['accurancy']
            self.points = {'xs': data['pointsxs'],'ys': data['pointsys']}
            Curve.curveType = data['type']
            self.numberOfPoints = len(self.points[0])
            self.color = data['color']
            self.width = data['width']
            self.texts = []
            for i in range(self.numberOfPoints):
                self.texts.append(plt.text(self.points[0][i],self.points[1][i],i.__str__()))
                self.texts[i].set_visible(self.numbersVisible)
            self.update_plots_extended()

        except:
            print("Failed reading curve from file: " + path )

    '''def change_type(self,curveType):
        self.curveType = curveType
        self.update_plots_extended()'''

    def get_points_label(self):
        return self.pointsPlot.get_label()

    def calculate_function(self):
        pass

    def update_plots_extended(self):
        self.pointsPlot.set_data(self.points[0],self.points[1])
        self.funcY = self.calculate_function()
        lxs,lys = self.funcY(self.currentAccurancy)
        self.linePlot.set_data(lxs,lys)

    def update_plots(self,lxs,lys):
        self.pointsPlot.set_data(self.points[0],self.points[1])
        self.linePlot.set_data(lxs,lys)

    def update_numbers(self,startNumber):
        n = len(self.points[0])
        for i in range(startNumber,n):
            self.texts[i].set_text(i+1)

    def paste_curve_settings(self,toCurve):
        toCurve.accurancy = self.accurancy
        toCurve.workingAccurancy = self.workingAccurancy
        #toCurve.color = self.color
        toCurve.width = self.width

    def add_point(self,x,y):
        self.numberOfPoints += 1

        self.points[0].append(x)
        self.points[1].append(y)
        self.texts.append(plt.text(self.points[0][-1],self.points[1][-1],self.numberOfPoints.__str__()))
        self.texts[-1].set_visible(self.numbersVisible)

        self.update_plots_extended()

    def delete_point(self,x,y):
        i = self.find_point(x,y,self.points[0],self.points[1])
        del self.points[0][i]
        del self.points[1][i]
        self.texts[i].remove()
        del self.texts[i]

        self.numberOfPoints -= 1

        self.update_numbers(i)

        self.update_plots_extended()

    def activate_point(self,x,y):
        self.activePoint = self.find_point(x,y,self.points[0],self.points[1])

    def disactivate_point(self):
        self.activePoint = None

    def move_point(self,x,y):
        if self.activePoint != None:
            self.points[0][self.activePoint] = x
            self.points[1][self.activePoint] = y
            self.texts[self.activePoint].set_position((x,y))
            self.update_plots_extended()

    def move_curve(self,x,y):
        for i in range(self.numberOfPoints):
            self.points[0][i] += x
            self.points[1][i] += y
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

        xf,yf = self.points[0][0],self.points[1][0]

        for i in range(self.numberOfPoints-1):
            self.points[0][i+1],self.points[1][i+1]  = self.scale_point(xf,yf,self.points[0][i+1],self.points[1][i+1],scale)
            self.texts[i].set_position((self.points[0][i+1],self.points[1][i+1]))

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
            self.points[0][i],self.points[1][i]  = self.rotate_points(self.points[0][i],self.points[1][i],angle,s,t)
            self.texts[i].set_position((self.points[0][i],self.points[1][i]))

        for i in range(self.accurancy):
            linex[i], liney[i] = self.rotate_points(linex[i],liney[i],angle,s,t)

        self.update_plots(linex,liney)

    def split_curve(self,newCurve,xs1,ys1,xs2,ys2,x,y):
        n = len(xs1)-1

        self.points[0] = xs1
        self.points[1] = ys1
        self.numberOfPoints = len(xs1)

        newCurve.texts = self.texts[n:]
        self.texts = self.texts[:n]
        self.texts.append(plt.text(x,y,self.numberOfPoints.__str__()))
        self.texts[-1].set_visible(self.numbersVisible)
        self.update_plots_extended()

        self.paste_curve_settings(newCurve)
        newCurve.points[0] = xs2
        newCurve.points[1] = ys2
        newCurve.numberOfPoints = len(xs2)

        newCurve.texts = [plt.text(x,y,'1')] + newCurve.texts
        newCurve.texts[0].set_visible(self.numbersVisible)
        newCurve.update_numbers(1)
        newCurve.update_plots_extended()


    def find_point(self,x,y,xs,ys):
        minDistance = 100000000000000
        pointer = -1
        n = len(xs)
        for i in range(n):
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
        data['type'] = Curve.curveType
        data['accurancy'] = self.accurancy
        data['color'] = self.color
        data['pointsxs'] = self.points[0]
        data['pointsys'] = self.points[1]

        with open(path,'w') as ofile:
            json.dump(data,ofile)

    def hide_points(self):
        self.pointsPlot.set_visible(False)
        self.pointsVisible = False

    def show_points(self):
        if self.visible:
            self.pointsPlot.set_visible(True)
            self.pointsVisible = True

    def hide_curve(self):
        self.pointsPlot.set_visible(False)
        self.linePlot.set_visible(False)
        self.hide_numbers(temp=True)
        self.visible = False

    def show_curve(self):
        self.pointsPlot.set_visible(self.pointsVisible)
        self.linePlot.set_visible(True)
        if self.numbersVisible:
            self.show_numbers(force=True)
        self.visible = True

    def show_numbers(self,force=False):
        if self.visible and ( not self.numbersVisible or force ):
            for i in range(self.numberOfPoints):
                self.texts[i].set_visible(True)
            self.numbersVisible = True

    def hide_numbers(self,temp=False):
        if self.numbersVisible:
            for i in range(self.numberOfPoints):
                self.texts[i].set_visible(False)
            self.numbersVisible = temp

    def set_working_accurancy(self):
        self.currentAccurancy = self.workingAccurancy

    def set_normal_accurancy(self):
        self.currentAccurancy = self.accurancy
        self.update_plots_extended()

    def regular_nodes(self,n):
        ts = []
        for i in range(n):
            ts.append(i/(n-1))

        return ts

    def chebyshev_nodes(self,n):
        ts = []
        for k in range(n):
            ts.append(m.cos(m.pi*(k + 0.5)/n))

        return ts
