import matplotlib.colors
import matplotlib.pyplot as plt
import math as m
import json

class Curve:
    counter = 0
    curveType = None
    extraMenu = None
    extraPointsMenu = None
    def __init__(self,linePlot,pointsPlot,convexHull):
        self.name = "Curve " + str(Curve.counter)
        self.accurancy = 10000
        self.workingAccurancy = 200
        self.currentAccurancy = self.accurancy
        Curve.counter += 1
        self.linePlot = linePlot[0]
        self.pointsPlot = pointsPlot[0]
        self.convexHull = convexHull[0]
        self.convexHull.set_visible(False)
        self.texts = []
        self.points = [list(),list()]
        self.numberOfPoints = 0
        self.activePoint = None
        self.color = self.linePlot.get_color()
        self.width = self.linePlot.get_linewidth()
        self.pointsVisible = True
        self.numbersVisible = False
        self.hullVisible = False
        self.visible = True 

    @staticmethod
    def load_curves_data_from_file(path):
        try:
            with open(path,'r') as ifile:
                data = json.load(ifile)
        except:
            print("Failed reading curve from file: " + path )
        return data

    @staticmethod
    def get_curve_type_from_data(data):
        try:
            return data['type']
        except:
            print("The data from file is not valid.")
            return None
        

    def set_curve_data(self,data):
        try:
            self.name = data['name']
            self.accurancy = data['accurancy']
            self.points[0] =  data['pointsxs']
            self.points[1] =  data['pointsys']
            self.numberOfPoints = len(self.points[0])
            self.color = data['color']
            self.linePlot.set_color(self.color)
            self.width = data['width']
            self.linePlot.set_linewidth(self.width)
            self.set_numbers()
            self.update_plots_extended()
        except:
            print("The data from file is not valid.")
    

    '''def change_type(self,curveType):
        self.curveType = curveType
        self.update_plots_extended()'''

    def get_points_label(self):
        return self.pointsPlot.get_label()

    def calculate_function(self):
        pass

    def update_plots_extended(self,flag=None):
        self.pointsPlot.set_data(self.points[0],self.points[1])
        newhull = self.find_convex_hull(self.points[0],self.points[1])
        self.convexHull.set_data(newhull[0],newhull[1])
        self.calculate_function(flag)
        lxs,lys = self.funcY()
        self.linePlot.set_data(lxs,lys)

    def update_plots(self,lxs,lys,cxs,cys):
        self.pointsPlot.set_data(self.points[0],self.points[1])
        self.linePlot.set_data(lxs,lys)
        self.convexHull.set_data(cxs,cys)


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

        self.update_plots_extended(flag="added_point")

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


        for i in range(len(linex)):
            linex[i] += x
            liney[i] += y

        cxs,cys = self.convexHull.get_data()

        n = len(cxs)
        for i in range(n):
            cxs[i] += x
            cys[i] += y

        self.update_plots(linex,liney,cxs,cys)

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
            self.texts[i+1].set_position((self.points[0][i+1],self.points[1][i+1]))

        for i in range(len(linex)-1):
            linex[i+1], liney[i+1] = self.scale_point(xf,yf,linex[i+1],liney[i+1],scale)

        cxs,cys = self.convexHull.get_data()

        n = len(cxs)
        for i in range(n):
            cxs[i],cys[i] = self.scale_point(xf,yf,cxs[i],cys[i],scale)

        self.update_plots(linex,liney,cxs,cys)


    def rotate_points(self,x,y,angle,s,t):
        return (x-s)*m.cos(angle) - (y-t)*m.sin(angle) + s, (x-s)*m.sin(angle) + (y-t)*m.cos(angle) + t

    def rotate_curve(self,angle,s,t):
        angle = m.radians(angle)

        linex = self.linePlot.get_xdata()
        liney = self.linePlot.get_ydata()

        for i in range(self.numberOfPoints):
            self.points[0][i],self.points[1][i]  = self.rotate_points(self.points[0][i],self.points[1][i],angle,s,t)
            self.texts[i].set_position((self.points[0][i],self.points[1][i]))

        for i in range(len(linex)):
            linex[i], liney[i] = self.rotate_points(linex[i],liney[i],angle,s,t)

        cxs,cys = self.convexHull.get_data()

        n = len(cxs)
        for i in range(n):
            cxs[i],cys[i] = self.rotate_points(cxs[i],cys[i],angle,s,t)

        self.update_plots(linex,liney,cxs,cys)

    def set_numbers(self):
        n = len(self.texts)
        for i in range(n):
            self.texts[-1].remove()
            del self.texts[-1]
        for i in range(self.numberOfPoints):
            self.texts.append(plt.text(self.points[0][i],self.points[1][i],(i+1).__str__()))
            self.texts[i].set_visible(self.numbersVisible)


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

    def join_curve(self,toJoin):
        print("This option is not available for this curves class.")


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
        self.convexHull.remove()
        del self.convexHull

    def save_to_file(self,path,data={}):
        data['name'] = self.name
        data['width'] = self.width
        data['type'] = self.curveType
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

    def hide_hull(self):
        self.convexHull.set_visible(False)
        self.hullVisible = False

    def show_hull(self):
        if self.visible:
            self.convexHull.set_visible(True)
            self.hullVisible = True

    def hide_curve(self):
        self.pointsPlot.set_visible(False)
        self.linePlot.set_visible(False)
        self.convexHull.set_visible(False)
        self.hide_numbers(temp=True)
        self.visible = False

    def show_curve(self):
        self.pointsPlot.set_visible(self.pointsVisible)
        self.linePlot.set_visible(True)
        self.convexHull.set_visible(self.hullVisible)
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
        self.update_plots_extended(flag='change_accurancy')
        
    def regular_nodes(self,n):
        ts = []
        for i in range(n):
            ts.append(i/(n-1))
        return ts

    def chebyshev_nodes(self,n):
        ts = []
        for k in range(1,n+1):
            ts.append(0.5 + 0.5*m.cos(m.pi*(2*k -1)/(2*n)))
        return ts

    @staticmethod
    def at_right(ax,ay,bx,by,cx,cy):
        return (cx-bx)*(ay-by) - (ax-bx)*(cy-by) < 0

    @staticmethod
    def pseudoangle(x,y):
        if x != 0 or y != 0:
            return x / (x**2 + y**2)**(1/2)
        return 2

    @staticmethod
    def find_convex_hull(xs,ys):
        minid = 0
        aux = []
        n = len(xs)
        stack = [[],[]]
        if n<3:
            return stack
        for i in range(n):
            if ys[i] < ys[minid] or (ys[i] == ys[minid] and xs[i] > xs[minid]):
                minid = i

        sx = xs[minid]
        sy = ys[minid]
        for i in range(n):
            xs[i] -= sx
            ys[i] -= sy
            aux.append((Curve.pseudoangle(xs[i],ys[i]),i))
        
        aux.sort(reverse=True)

        aux.append(aux[0])

        stack[0].append(xs[aux[0][1]])
        stack[1].append(ys[aux[0][1]])
        stack[0].append(xs[aux[1][1]])
        stack[1].append(ys[aux[1][1]])

        i = 2
        while i < n+1:
            j = aux[i][1]
            while len(stack[0]) > 1 and Curve.at_right(xs[j],ys[j],stack[0][-2],stack[1][-2],stack[0][-1],stack[1][-1]):
                del stack[0][-1]
                del stack[1][-1]
            stack[0].append(xs[j])
            stack[1].append(ys[j])
            i += 1

        for i in range(n):
            xs[i] += sx
            ys[i] += sy

        n = len(stack[0])
        for i in range(n):
            stack[0][i] += sx
            stack[1][i] += sy

        return stack

    def change_line_color(self,r,g,b):
        color = matplotlib.colors.to_hex((r,g,b))
        self.color = color
        self.linePlot.set_color(color)

    def change_line_width(self,scale):
        width = self.linePlot.get_linewidth()
        self.width = width*scale
        self.linePlot.set_linewidth(width*scale)
