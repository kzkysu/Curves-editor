import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio,GLib

from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

from matplotlib import axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import classes

from curves_editor_widget import CurveWidget,GetAngleWidget,getScaleWidget,CurvesTypesComboBox
from app_canvas import AppCanvas
from points_menu import PointsMenu
from curve_menu import CurveMenu

class MainWindow(Gtk.ApplicationWindow):
    curveTypes = classes.curveTypes

    def __init__(self,application=None):
        super(MainWindow,self).__init__(application=application)
        self.set_title("Curves and surfaces editor")
        self.set_size_request(1200, 700)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.curvesCounter = 0
        self.curves = {}
        self.radioButton = Gtk.RadioButton()
        self.activeCurve = None
        self.activeCurveWidget = None
        self.activeMenuButton = None
        self.pointOfRotation = None
        self.getAngleWidget = None
        self.getScaleWidget = None
        #self.editCurveMenu = None
        #self.editPointsMenu = None
        self.pointsVisible = True
        self.numbersVisible = False
        self.hullVisible = False
        self.activeToggleButton = []

        self.set_icon_from_file("data/icon.png")

        mainVBox = Gtk.VBox()
        self.add(mainVBox)

        self.editorGrid = Gtk.Grid()
        self.editorGrid.set_row_spacing(6)
        self.editorGrid.set_column_spacing(5)
        self.editorGrid.set_row_homogeneous(True)
        mainVBox.pack_start(self.editorGrid,False,False,0)

        mainOptionsHBox = Gtk.HBox()
        mainOptionsHBox.set_spacing(3)
        self.editorGrid.attach(mainOptionsHBox,0,0,1,2)

        addCurveBox = Gtk.Box()
        mainOptionsHBox.pack_start(addCurveBox,False,False,0)

        addCurveButton = Gtk.Button(label="Add curve")
        addCurveButton.connect("clicked", self.add_curve_clicked)
        addCurveBox.pack_start(addCurveButton,False,False,0)

        self.chooseTypeComboBox = CurvesTypesComboBox(list(MainWindow.curveTypes.keys()))
        addCurveBox.pack_start(self.chooseTypeComboBox,False,False,0)

        self.extraBox = Gtk.Box()
        mainOptionsHBox.pack_start(self.extraBox,False,False,0)

        self.emptyHBox = Gtk.HBox()
        self.editorGrid.attach(self.emptyHBox,0,2,1,4)
        
        mainHBox = Gtk.HBox()
        mainVBox.pack_end(mainHBox,True,True,0)

        canvasHBox = Gtk.HBox()
        mainHBox.pack_start(canvasHBox,True,True,0)
        
        sw = Gtk.ScrolledWindow()
       
        curvesList = Gtk.ScrolledWindow()
        curvesList.set_size_request(140,0)
        self.curvesVBox = Gtk.VBox()
        self.curvesVBox.set_size_request(140,0)
        mainHBox.pack_end(curvesList,False,True,20)
        curvesList.add(self.curvesVBox)

        self.appCanvas = AppCanvas()
        self.canvas = self.appCanvas.get_canvas()
        sw.add(self.canvas)

        self.editCurveMenu = CurveMenu(self.appCanvas,self.activeCurve,self.curves,self.activeToggleButton,self.extraBox)
        self.editorGrid.attach(self.editCurveMenu,0,2,1,2)

        self.editCurveMenu.basicMenu.selectCurveButton.connect("toggled", self.on_select_curve_button_toggled)
        self.editCurveMenu.basicMenu.splitCurveButton.connect("toggled", self.on_split_curve_button_toggled)
        self.editCurveMenu.basicMenu.deleteCurveButton.connect("clicked", self.delete_curve)

        self.pointsMenu = PointsMenu(self.appCanvas,self.activeCurve,self.curves,self.activeToggleButton)

        canvasHBox.pack_start(self.pointsMenu,False,False,0)
        canvasHBox.pack_start(sw,True,True,0)


        self.ax = self.appCanvas.get_ax()

        self.show_all()

    def on_click(self,event):
        event.artist.remove()
        self.canvas.draw_idle()
        print("yupi")

    def set_active_widget(self,widget):
        if self.activeToggleButton != []:
            if self.activeToggleButton[0] != widget:
                self.activeToggleButton[0].set_active(False)
            self.activeToggleButton[0] = widget
        else:
            self.activeToggleButton.append(widget)

    def set_active_curve_from_button(self,widget):
        if widget.get_active():
            self.activeCurveWidget = widget.get_parent()
            self.set_active_curve()

    def set_active_curve(self):
        self.activeCurve = self.activeCurveWidget.get_curve()
        self.chooseTypeComboBox.set_current_type(self.activeCurve.curveType)

        if self.pointsVisible:
            self.activeCurve.show_points()
        else:
            self.activeCurve.hide_points()
        if self.numbersVisible:
            self.activeCurve.show_numbers()
        else:
            self.activeCurve.hide_numbers()
        
        self.appCanvas.set_activeCurve(self.activeCurve)

        if self.editCurveMenu != None:
            self.editCurveMenu.update_active_curve(self.activeCurve)
        self.pointsMenu.update_active_curve(self.activeCurve)
        
    def on_select_curve_button_toggled(self,widget):
        if widget.get_active() == True:
            self.set_active_widget(widget)
            self.select_curve_active = self.canvas.mpl_connect('pick_event', self.select_curve)
        else:
            self.canvas.mpl_disconnect(self.select_curve_active)
        
    def on_split_curve_button_toggled(self,widget):
        if widget.get_active() == True:
            self.set_active_widget(widget)
            self.split_curve_active = self.canvas.mpl_connect('pick_event', self.split_curve)
        else:
            self.canvas.mpl_disconnect(self.split_curve_active)

    def add_curve_clicked(self,event):
        self.add_curve(MainWindow.curveTypes[self.chooseTypeComboBox.get_current_type()])

    def add_curve(self,CurveClass):
        newCurve = CurveClass(self.ax.plot([],[],picker=5,label="line" + str(self.curvesCounter)),
            self.ax.plot([],[],'o',picker=5,label="points" + str(self.curvesCounter)),
            self.ax.plot([],[],'--'))
        newCurveWidget = CurveWidget(newCurve,self.radioButton,self.curvesCounter,self.set_active_curve_from_button,self.canvas)
        
        self.activeCurveWidget = newCurveWidget
        self.set_active_curve()

        self.curvesVBox.pack_start(newCurveWidget,True,False,0)
        self.curves["points" + str(self.curvesCounter)] = newCurveWidget
        self.curves["line" + str(self.curvesCounter)] = newCurveWidget
        self.curvesCounter += 1
        self.show_all()
    
    def select_curve(self,event):
        lineName = event.artist.get_label()
        if 'line' in lineName:
            self.activeCurveWidget = self.curves[lineName]
            self.activeCurveWidget.get_radioButton().set_active(True)
            self.set_active_curve()

    def delete_curve(self,event):
        if self.activeCurve != None:
            self.curves[self.activeCurve.get_points_label()] = None
            self.activeCurve.delete_curve()
            self.activeCurveWidget.destroy()
            self.activeCurve = None
            self.appCanvas.set_activeCurve(self.activeCurve)
            self.activeCurveWidget = None

            self.canvas.draw_idle()

    def split_curve(self,event):
        lineName = event.artist.get_label()
        if self.activeCurve != None and lineName == self.activeCurve.linePlot.get_label():
            oldCurve = self.activeCurve
            self.add_curve(self.curveTypes[self.activeCurve.curveType])
            oldCurve.calculate_split(event.mouseevent.xdata,event.mouseevent.ydata,self.activeCurve)
            self.canvas.draw_idle()

    def save_active_curve(self,path):
        if self.activeCurve != None:
            self.activeCurve.save_to_file(path)

    def load_curve(self,path):
        data = classes.Curve.load_curves_data_from_file(path)
        curveType = classes.curveTypes[classes.Curve.get_curve_type_from_data(data)]
        if curveType != None:
            self.add_curve(curveType)
            self.activeCurve.set_curve_data(data)
            self.canvas.draw_idle()

    def save_fig_to_png(self,path):
        plt.axis('off')
        plt.savefig(path,format='png')
        plt.axis('on')

    def change_curve_type(self,widget):
        if self.activeCurve != None:
            self.activeCurve.change_type(widget.get_active_text())

    def hide_points(self):
        if self.activeCurve != None:
            self.activeCurve.hide_points()
            self.canvas.draw_idle()
            self.pointsVisible = False

    def show_points(self):
        if self.activeCurve != None:
            self.activeCurve.show_points()
            self.canvas.draw_idle()
            self.pointsVisible = True

    def show_numbers(self):
        if self.activeCurve != None:
            self.activeCurve.show_numbers()
            self.canvas.draw_idle()
            self.numbersVisible = True

    def hide_numbers(self):
        if self.activeCurve != None:
            self.activeCurve.hide_numbers()
            self.canvas.draw_idle()
            self.numbersVisible = False

    def show_hull(self):
        if self.activeCurve != None:
            self.activeCurve.show_hull()
            self.canvas.draw_idle()
            self.hullVisible = True

    def hide_hull(self):
        if self.activeCurve != None:
            self.activeCurve.hide_hull()
            self.canvas.draw_idle()
            self.hullVisible = False

    def hide_points_all(self):
        for key in self.curves:
            self.curves[key].get_curve().hide_points()
        self.canvas.draw_idle()
    
    def show_points_all(self):
        for key in self.curves:
            self.curves[key].get_curve().show_points()
        self.canvas.draw_idle()