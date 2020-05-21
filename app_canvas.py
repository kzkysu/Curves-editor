import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio,GLib

from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

from matplotlib import axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class AppCanvas():
    def __init__(self):
        self.curvesCounter = 0
        self.activeCurve = None
        self.pointOfRotation = None
        self.getScaleWidget = None
        self.getAngleWidget = None 

        fig = plt.figure(figsize=[9, 6], dpi=100,)
        self.ax = fig.add_subplot()
        #plt.axis([0,300,0,200],'scaled')
        plt.axis([0,300,0,200])

        self.canvas = FigureCanvas(fig)

    def get_canvas(self):
        return self.canvas

    def get_ax(self):
        return self.ax

    def set_activeCurve(self,activeCurve):
        self.activeCurve = activeCurve

    def set_getScaleWidget(self,getScaleWidget):
        self.getScaleWidget = getScaleWidget

    def set_getAngleWidget(self,getAngleWidget):
        self.getAngleWidget = getAngleWidget
    
    def pick_curve(self,event):
        lineName = event.artist.get_label()
        if lineName == self.activeCurve.linePlot.get_label():
            self.drag_curve_active = self.canvas.mpl_connect('motion_notify_event', self.drag_curve)
            self.drop_curve_active = self.canvas.mpl_connect('button_release_event', self.drop_curve)
            self.mouseX = event.mouseevent.xdata
            self.mouseY = event.mouseevent.ydata
            self.activeCurve.set_working_accurancy()

    def drop_curve(self,event):
        if self.drag_curve_active != None:
            if event.inaxes != None:
                self.activeCurve.move_curve(event.xdata-self.mouseX,event.ydata-self.mouseY)
            self.canvas.mpl_disconnect(self.drag_curve_active)
            self.canvas.mpl_disconnect(self.drop_curve_active)
            self.activeCurve.set_normal_accurancy()
            self.canvas.draw_idle()
            self.drag_curve_active = None
            self.drop_curve_active = None
    
    def drag_curve(self,event):
        if event.inaxes != None:
            self.activeCurve.move_curve(event.xdata-self.mouseX,event.ydata-self.mouseY)
            self.mouseX = event.xdata
            self.mouseY = event.ydata
            self.canvas.draw_idle()

    def resize_curve(self,event):
        scale = self.getScaleWidget.get_scale_value()
        self.getScaleWidget.reset_scale_value()
        if self.activeCurve != None:
            self.activeCurve.resize_curve(scale/100.0)
        self.canvas.draw_idle()

    def change_line_width(self,event):
        scale = self.getScaleWidget.get_scale_value()
        self.getScaleWidget.reset_scale_value()
        if self.activeCurve != None:
            self.activeCurve.change_line_width(scale/100.0)
        self.canvas.draw_idle()

    def change_curve(self,event):
        scale = self.getScaleWidget.get_scale_value()
        self.getScaleWidget.reset_scale_value()
        if self.activeCurve != None:
            self.activeCurve.resize_curve(scale/100.0)
        self.canvas.draw_idle()

    def rotate_curve(self,event):
        angle = self.getAngleWidget.get_entry_text()
        if self.pointOfRotation != None:
            s = self.pointOfRotation[0].get_xdata()[0]
            t = self.pointOfRotation[0].get_ydata()[0]
        else:
            s,t = 0,0
        try:
            if self.activeCurve != None and int(angle) < 360 and int(angle) > -360:
                angle = int(angle)
                if angle < 0:
                    angle += 360
            self.activeCurve.rotate_curve(angle,s,t)
            self.canvas.draw_idle()
        except:
            pass

    def add_point_of_rotation(self,event):
        self.delete_point_of_rotation()
        self.pointOfRotation = self.ax.plot([event.xdata],[event.ydata],'ko')
        self.canvas.draw_idle()


    def delete_point_of_rotation(self):
        if self.pointOfRotation != None :
            self.pointOfRotation[0].remove()
            del self.pointOfRotation
            self.pointOfRotation = None
            self.canvas.draw_idle()

    def select_point(self,event):
        lineName = event.artist.get_label()
        if lineName == self.activeCurve.pointsPlot.get_label():
            self.activeCurve.activate_point(event.mouseevent.xdata,event.mouseevent.ydata)
            self.canvas.draw_idle()

    def delete_point(self,event):
        lineName = event.artist.get_label()
        if lineName == self.activeCurve.pointsPlot.get_label():
            self.activeCurve.delete_point(event.mouseevent.xdata,event.mouseevent.ydata)
            self.canvas.draw_idle()

    def add_point(self,event):
        if self.activeCurve != None and event.inaxes != None:
            self.activeCurve.add_point(event.xdata,event.ydata)
            self.canvas.draw_idle()

    def pick_point(self,event):
        self.drag_point_active = self.canvas.mpl_connect('motion_notify_event', self.drag_point)
        self.activeCurve.set_working_accurancy()

    def drop_point(self,event):
        self.canvas.mpl_disconnect(self.drag_point_active)
        if self.activeCurve != None:
            self.activeCurve.disactivate_point()
            self.activeCurve.set_normal_accurancy()
            self.canvas.draw_idle()

    def drag_point(self,event):
        if event.inaxes != None:
            self.activeCurve.move_point(event.xdata,event.ydata)
            self.canvas.draw_idle()