import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio,GLib
#from gi.repository import GObject
#from gi.repository import GdkX11

from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

from matplotlib import axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from curve import Curve
from curves_editor_widget import CurveWidget,GetAngleWidget,getScaleWidget
from app_canvas import AppCanvas
from edit_curve_menu import EditCurveMenu
from edit_points_menu import EditPointsMenu

class MainWindow(Gtk.ApplicationWindow):
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
        self.editCurveMenu = None
        self.editPointsMenu = None

        self.set_icon_from_file("data/icon.png")

        mainVBox = Gtk.VBox()
        self.add(mainVBox)

        self.editorGrid = Gtk.Grid()
        self.editorGrid.set_row_spacing(6)
        self.editorGrid.set_column_spacing(5)
        mainVBox.pack_start(self.editorGrid,False,False,0)

        mainOptionsHBox = Gtk.HBox()
        #mainVBox.pack_start(mainOptionsHBox,False,False,0)
        self.editorGrid.attach(mainOptionsHBox,0,0,1,2)

        selectCurveButton = Gtk.ToggleButton(label="Select curve")
        selectCurveButton.connect("toggled", self.on_select_curve_button_toggled)
        mainOptionsHBox.pack_start(selectCurveButton,False,False,0)

        editCurveButton = Gtk.ToggleButton(label="Edit curve")
        editCurveButton.connect("toggled", self.on_edit_curve_button_toggled)
        mainOptionsHBox.pack_start(editCurveButton,False,False,0)

        editPointsButton = Gtk.ToggleButton(label="Edit points")
        editPointsButton.connect("toggled", self.on_edit_points_button_toggled)
        mainOptionsHBox.pack_start(editPointsButton,False,False,0)

        addCurveButton = Gtk.Button(label="Add curve")
        addCurveButton.connect("clicked", self.add_curve)
        mainOptionsHBox.pack_start(addCurveButton,False,False,0)

        deleteCurveButton = Gtk.Button(label="Delete active curve")
        deleteCurveButton.connect("clicked", self.delete_curve)
        mainOptionsHBox.pack_start(deleteCurveButton,False,False,0)

        addPointButton = Gtk.ToggleButton(label="Add point")
        addPointButton.connect("toggled", self.on_add_point_button_toggled)
        #self.editorGrid.attach(addPointButton,1,1,1,1)

        selectPointButton = Gtk.ToggleButton(label="Delete point")
        selectPointButton.connect("toggled", self.on_delete_point_button_toggled)
        #self.editorGrid.attach(selectPointButton,2,1,1,1)

        movePointButton = Gtk.ToggleButton(label="Move point")
        movePointButton.connect("toggled", self.on_move_point_button_toggled)
        #self.editorGrid.attach(movePointButton,3,1,1,1)
        
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

        self.appCanvas = AppCanvas()
        self.canvas = self.appCanvas.get_canvas()
        sw.add(self.canvas)

        self.ax = self.appCanvas.get_ax()

        self.show_all()

    def on_click(self,event):
        event.artist.remove()
        self.canvas.draw_idle()
        print("yupi")

    def set_active_widget(self,widget):
        if self.activeMenuButton != None and self.activeMenuButton != widget:
            self.activeMenuButton.set_active(False)
        self.activeMenuButton = widget

    def set_active_curve_from_button(self,widget):
        if widget.get_active():
            self.activeCurveWidget = widget.get_parent()
            self.set_active_curve()

    def set_active_curve(self):
        self.activeCurve = self.activeCurveWidget.get_curve()
        self.appCanvas.set_activeCurve(self.activeCurve)
        if self.editCurveMenu != None:
            self.editCurveMenu.update_active_curve(self.activeCurve)
        if self.editPointsMenu != None:
            self.editPointsMenu.update_active_curve(self.activeCurve)
        
    def on_select_curve_button_toggled(self,widget):
        if widget.get_active() == True:
            self.set_active_widget(widget)
            self.select_curve_active = self.canvas.mpl_connect('pick_event', self.select_curve)
        else:
            self.canvas.mpl_disconnect(self.select_curve_active)

    def on_edit_curve_button_toggled(self,widget):
        if widget.get_active() == True:
            self.set_active_widget(widget)
            self.editCurveMenu = EditCurveMenu(self.appCanvas,self.activeCurve,self.curves)
            self.editorGrid.attach(self.editCurveMenu,0,2,1,3)
            self.show_all()
        else:
            self.editCurveMenu.destroy_menu()
            self.editCurveMenu = None
            self.show_all()

    def on_edit_points_button_toggled(self,widget):
        if widget.get_active() == True:
            self.set_active_widget(widget)
            self.editPointsMenu = EditPointsMenu(self.appCanvas,self.activeCurve,self.curves)
            self.editorGrid.attach(self.editPointsMenu,0,2,1,3)
            self.show_all()
        else:
            self.editPointsMenu.destroy_menu()
            self.editPointsMenu = None
            self.show_all()
 
    def on_add_point_button_toggled(self,widget):
        if widget.get_active() == True:
            self.set_active_widget(widget)
            self.add_point_active = self.canvas.mpl_connect('button_press_event', self.appCanvas.add_point)
        else:
            self.canvas.mpl_disconnect(self.add_point_active)
    
    def on_delete_point_button_toggled(self,widget):
        if widget.get_active() == True:
            self.set_active_widget(widget)
            self.delete_point_active = self.canvas.mpl_connect('pick_event', self.appCanvas.delete_point)
        else:
            self.canvas.mpl_disconnect(self.delete_point_active)  
            

    def on_move_point_button_toggled(self,widget):
        if widget.get_active() == True:
            self.set_active_widget(widget)
            self.select_point_active = self.canvas.mpl_connect('pick_event', self.appCanvas.select_point)
            self.pick_point_active = self.canvas.mpl_connect('button_press_event', self.appCanvas.pick_point)
            self.drop_point_active = self.canvas.mpl_connect('button_release_event', self.appCanvas.drop_point)
        else:
            self.canvas.mpl_disconnect(self.select_point_active)
            self.canvas.mpl_disconnect(self.pick_point_active)
            self.canvas.mpl_disconnect(self.drop_point_active)

    def add_curve(self,event):
        newCurve = Curve(self.ax.plot([],[],'o',picker=5,label="points" + str(self.curvesCounter)),
            self.ax.plot([],[],picker=5,label="line" + str(self.curvesCounter)),'polygonal_chain')
        newCurveWidget = CurveWidget(newCurve,self.radioButton,self.curvesCounter,self.set_active_curve_from_button)

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
            self.activeCurve = self.activeCurveWidget.get_curve()
            self.appCanvas.set_activeCurve(self.activeCurve)

    def delete_curve(self,event):
        if self.activeCurve != None:
            self.curves[self.activeCurve.get_points_label()] = None
            self.activeCurve.delete_curve()
            self.activeCurveWidget.destroy()
            self.activeCurve = None
            self.appCanvas.set_activeCurve(self.activeCurve)
            self.activeCurveWidget = None

            self.canvas.draw_idle()
