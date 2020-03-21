import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import GdkX11

from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

from matplotlib import axes
from matplotlib.figure import Figure
from numpy import arange, pi, random, linspace
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

from curve import Curve
from curve_widget import CurveWidget


class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.set_title("Curves and surfaces editor")
        self.set_size_request(1200, 680)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.connect("destroy", Gtk.main_quit)
        self.curvesCounter = 0
        self.curves = {}
        self.radioButton = Gtk.RadioButton()
        self.activeCurve = None
        self.activeCurveWidget = None
        self.activeMenuButton = None

        mainVBox = Gtk.VBox()
        self.add(mainVBox)

        editorGrid = Gtk.Grid()
        mainVBox.pack_start(editorGrid,False,False,0)

        addCurveButton = Gtk.Button(label="Add curve")
        addCurveButton.connect("clicked", self.add_curve)
        editorGrid.add(addCurveButton)

        selectCurveButton = Gtk.ToggleButton(label="Select curve")
        selectCurveButton.connect("toggled", self.on_select_curve_button_toggled)
        editorGrid.attach(selectCurveButton,1,0,1,1)

        addPointButton = Gtk.ToggleButton(label="Add point")
        addPointButton.connect("toggled", self.on_add_point_button_toggled)
        editorGrid.attach(addPointButton,0,1,1,1)

        selectPointButton = Gtk.ToggleButton(label="Delete point")
        selectPointButton.connect("toggled", self.on_delete_point_button_toggled)
        editorGrid.attach(selectPointButton,2,1,1,1)

        movePointButton = Gtk.ToggleButton(label="Move point")
        movePointButton.connect("toggled", self.on_move_point_button_toggled)
        editorGrid.attach(movePointButton,1,1,1,1)
        
        mainHBox = Gtk.HBox()
        mainVBox.pack_end(mainHBox,True,True,0)

        sw = Gtk.ScrolledWindow()
        mainHBox.pack_start(sw,True,True,0)

        curvesList = Gtk.ScrolledWindow()
        curvesList.set_size_request(140,0)
        self.curvesVBox = Gtk.VBox()
        self.curvesVBox.set_size_request(140,0)
        mainHBox.pack_end(curvesList,False,True,20)
        curvesList.add(self.curvesVBox)

        self.show_plot()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.set_size_request(900,600)
        sw.add(self.canvas)

        self.show_all()

    def on_click(self,event):
        event.artist.remove()
        self.canvas.draw_idle()
        print("yupi")


    def show_plot(self):
        self.fig = plt.figure(figsize=[9, 6], dpi=100,)
        self.ax = self.fig.add_subplot()
        plt.axis([0,300,0,100],'scaled')

    def add_curve(self,event):
        newCurve = Curve(self.ax.plot([],[],'o',picker=5,label="points" + str(self.curvesCounter)),
            self.ax.plot([],[],picker=5,label="line" + str(self.curvesCounter)),'polygonal_chain')
        newCurveWidget = CurveWidget(newCurve,self.radioButton,self.curvesCounter)
        newCurveWidget.get_radioButton().set_active(True)
        newCurveWidget.get_radioButton().connect("toggled",self.set_active_curve)

        self.activeCurve = newCurve
        self.activeCurveWidget = newCurveWidget

        self.curvesVBox.pack_start(newCurveWidget,True,False,0)
        self.curves["points" + str(self.curvesCounter)] = newCurveWidget
        self.curves["line" + str(self.curvesCounter)] = newCurveWidget
        self.curvesCounter += 1
        self.show_all()

    def set_active_curve(self,widget):
        if widget.get_active():
            self.activeCurveWidget = widget.get_parent()
            self.activeCurve = self.activeCurveWidget.get_curve()
        
    def on_select_curve_button_toggled(self,widget):
        if widget.get_active() == True:
            self.select_curve_active = self.fig.canvas.mpl_connect('pick_event', self.select_curve)
            if self.activeMenuButton != None:
                self.activeMenuButton.set_active(False)
            self.activeMenuButton = widget
        else:
            self.fig.canvas.mpl_disconnect(self.select_curve_active)
 
    def on_add_point_button_toggled(self,widget):
        if widget.get_active() == True:
            self.add_point_active = self.fig.canvas.mpl_connect('button_press_event', self.add_point)
            if self.activeMenuButton != None and self.activeMenuButton != widget:
                self.activeMenuButton.set_active(False)
            self.activeMenuButton = widget
        else:
            self.fig.canvas.mpl_disconnect(self.add_point_active)
    
    def on_delete_point_button_toggled(self,widget):
        if widget.get_active() == True:
            self.delete_point_active = self.fig.canvas.mpl_connect('pick_event', self.delete_point)
            if self.activeMenuButton != None and self.activeMenuButton != widget:
                self.activeMenuButton.set_active(False)
            self.activeMenuButton = widget
        else:
            self.fig.canvas.mpl_disconnect(self.delete_point_active)
        

    def on_move_point_button_toggled(self,widget):
        if widget.get_active() == True:
            self.select_point_active = self.fig.canvas.mpl_connect('pick_event', self.select_point)
            self.pick_point_active = self.fig.canvas.mpl_connect('button_press_event', self.pick_point)
            self.drop_point_active = self.fig.canvas.mpl_connect('button_release_event', self.drop_point)
            if self.activeMenuButton != None and self.activeMenuButton != widget:
                self.activeMenuButton.set_active(False)
            self.activeMenuButton = widget
        else:
            self.fig.canvas.mpl_disconnect(self.select_point_active)
            self.fig.canvas.mpl_disconnect(self.pick_point_active)
            self.fig.canvas.mpl_disconnect(self.drop_point_active)
    

    def select_curve(self,event):
        lineName = event.artist.get_label()
        if 'line' in lineName:
            self.activeCurveWidget = self.curves[lineName]
            self.activeCurveWidget.get_radioButton().set_active(True)
            self.activeCurve = self.activeCurveWidget.get_curve()

    def select_point(self,event):
        lineName = event.artist.get_label()
        if 'points' in lineName and self.curves[lineName].get_curve().name == self.activeCurve.name:
            self.curves[lineName].get_curve().activate_point(event.mouseevent.xdata,event.mouseevent.ydata)
            self.canvas.draw_idle()

    def delete_point(self,event):
        lineName = event.artist.get_label()
        if 'points' in lineName and self.curves[lineName].get_curve().name == self.activeCurve.name:
            self.curves[lineName].get_curve().delete_point(event.mouseevent.xdata,event.mouseevent.ydata)
            self.canvas.draw_idle()

    def add_point(self,event):
        if self.activeCurve != None and event.inaxes != None:
            self.activeCurve.add_point(event.xdata,event.ydata)
            self.canvas.draw_idle()

    def pick_point(self,event):
        self.drag_point_active = self.fig.canvas.mpl_connect('motion_notify_event', self.drag_point)

    def drop_point(self,event):
        self.fig.canvas.mpl_disconnect(self.drag_point_active)
        if self.activeCurve != None:
            self.activeCurve.disactivate_point()

    def drag_point(self,event):
        if event.inaxes != None:
            self.activeCurve.move_point(event.xdata,event.ydata)
            self.canvas.draw_idle()
        

nw = MainWindow()
Gtk.main()
