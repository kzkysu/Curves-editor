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

        self.set_icon_from_file("data/icon.png")

        mainVBox = Gtk.VBox()
        self.add(mainVBox)

        self.editorGrid = Gtk.Grid()
        self.editorGrid.set_row_spacing(3)
        self.editorGrid.set_column_spacing(5)
        mainVBox.pack_start(self.editorGrid,False,False,0)

        selectCurveButton = Gtk.ToggleButton(label="Select curve")
        selectCurveButton.connect("toggled", self.on_select_curve_button_toggled)
        self.editorGrid.add(selectCurveButton)

        addCurveButton = Gtk.Button(label="Add curve")
        addCurveButton.connect("clicked", self.add_curve)
        self.editorGrid.attach(addCurveButton,1,0,1,1)

        deleteCurveButton = Gtk.Button(label="Delete active curve")
        deleteCurveButton.connect("clicked", self.delete_curve)
        self.editorGrid.attach(deleteCurveButton,2,0,1,1)

        moveCurveButton = Gtk.ToggleButton(label = "Move curve")
        moveCurveButton.connect("toggled", self.on_move_curve_button_toggled)
        self.editorGrid.attach(moveCurveButton,3,0,1,1)

        resizeCurveButton = Gtk.ToggleButton(label = "Resize curve")
        resizeCurveButton.connect("toggled", self.on_resize_curve_button_toggled)
        self.editorGrid.attach(resizeCurveButton,4,0,1,1)

        rotateCurveButton = Gtk.ToggleButton(label = "Rotate curve")
        rotateCurveButton.connect("toggled", self.on_rotate_curve_button_toggled)
        self.editorGrid.attach(rotateCurveButton,5,0,1,1)

        addPointButton = Gtk.ToggleButton(label="Add point")
        addPointButton.connect("toggled", self.on_add_point_button_toggled)
        self.editorGrid.attach(addPointButton,1,1,1,1)

        selectPointButton = Gtk.ToggleButton(label="Delete point")
        selectPointButton.connect("toggled", self.on_delete_point_button_toggled)
        self.editorGrid.attach(selectPointButton,2,1,1,1)

        movePointButton = Gtk.ToggleButton(label="Move point")
        movePointButton.connect("toggled", self.on_move_point_button_toggled)
        self.editorGrid.attach(movePointButton,3,1,1,1)
        
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

        #self.show_plot()
        #self.canvas = FigureCanvas(self.fig)
        #self.canvas.set_size_request(900,600)
        self.appCanvas = AppCanvas(self.getScaleWidget,self.getAngleWidget)
        self.canvas = self.app_canvas.get_canvas()
        sw.add(self.canvas)

        self.show_all()

    def on_click(self,event):
        event.artist.remove()
        self.canvas.draw_idle()
        print("yupi")


    def show_plot(self):
        self.fig = plt.figure(figsize=[9, 6], dpi=100,)
        self.ax = self.fig.add_subplot()
        plt.axis([0,300,0,200])
        plt.axis('scaled')


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

    def on_move_curve_button_toggled(self,widget):
        if widget.get_active() == True:
            self.pick_curve_active = self.fig.canvas.mpl_connect('pick_event', self.pick_curve)
            self.drop_curve_active = self.fig.canvas.mpl_connect('button_release_event', self.drop_curve)
            if self.activeMenuButton != None and self.activeMenuButton != widget:
                self.activeMenuButton.set_active(False)
            self.activeMenuButton = widget
        else:
            self.fig.canvas.mpl_disconnect(self.pick_curve_active)
            self.fig.canvas.mpl_disconnect(self.drop_curve_active)

    def on_resize_curve_button_toggled(self,widget):
        if widget.get_active() == True:
            if self.activeMenuButton != None and self.activeMenuButton != widget:
                self.activeMenuButton.set_active(False)
            self.activeMenuButton = widget
            self.getScaleWidget = getScaleWidget(self.resize_curve)
            self.editorGrid.add(self.getScaleWidget)
            self.show_all()
        else:
            self.getScaleWidget.destroy()
            self.show_all()

    def on_rotate_curve_button_toggled(self,widget):
        if widget.get_active() == True:
            if self.activeMenuButton != None and self.activeMenuButton != widget:
                self.activeMenuButton.set_active(False)
            self.activeMenuButton = widget

            self.getAngleWidget = GetAngleWidget(self.rotate_curve,self.on_add_point_of_rotation_button_toggled)
            self.editorGrid.add(self.getAngleWidget)
            self.show_all()
        else:
            if(self.pointOfRotation != None): self.fig.canvas.mpl_disconnect(self.add_point_of_rotation_active)
            self.delete_point_of_rotation()
            self.getAngleWidget.destroy()
            self.show_all()

    def on_add_point_of_rotation_button_toggled(self,widget):
        if widget.get_active() == True:
            self.add_point_of_rotation_active = self.fig.canvas.mpl_connect('button_press_event', self.add_point_of_rotation)
        else:
            self.fig.canvas.mpl_disconnect(self.add_point_of_rotation_active)
            self.delete_point_of_rotation()
            self.canvas.draw_idle()
 
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

    def add_curve(self,event):
        newCurve = Curve(self.ax.plot([],[],'o',picker=5,label="points" + str(self.curvesCounter)),
            self.ax.plot([],[],picker=5,label="line" + str(self.curvesCounter)),'polygonal_chain')
        newCurveWidget = CurveWidget(newCurve,self.radioButton,self.curvesCounter,self.set_active_curve)

        self.activeCurve = newCurve
        self.activeCurveWidget = newCurveWidget

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

    def delete_curve(self,event):
        if self.activeCurve != None:
            self.curves[self.activeCurve.get_points_label()] = None
            self.activeCurve.delete_curve()
            self.activeCurveWidget.destroy()
            self.activeCurve = None
            self.activeCurveWidget = None

            self.canvas.draw_idle()

    def pick_curve(self,event):
        lineName = event.artist.get_label()
        if self.curves[lineName] == self.activeCurveWidget:
            self.drag_curve_active = self.fig.canvas.mpl_connect('motion_notify_event', self.drag_curve)
            self.mouseX = event.mouseevent.xdata
            self.mouseY = event.mouseevent.ydata

    def drop_curve(self,event):
        if self.drag_curve_active != None:
            self.activeCurve.move_curve(event.xdata-self.mouseX,event.ydata-self.mouseY)
            self.canvas.draw_idle()
            self.fig.canvas.mpl_disconnect(self.drag_curve_active)
    
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
        if( self.pointOfRotation != None ):
            self.pointOfRotation[0].remove()
            del self.pointOfRotation
            self.pointOfRotation = None
            self.canvas.draw_idle()

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
        
