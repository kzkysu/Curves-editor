import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio,GLib

from matplotlib import axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from curves_editor_widget import GetAngleWidget,getScaleWidget


class EditCurveMenu(Gtk.HBox):
    def __init__(self,appCanvas,activeCurve,curves):
        super().__init__()

        self.appCanvas = appCanvas
        self.canvas = appCanvas.get_canvas()
        self.activeCurve = activeCurve
        self.curves = curves

        self.activeMenuButton = None
        self.pointOfRotation = None
        self.getAngleWidget = None
        self.getScaleWidget = None

        self.moveCurveButton = Gtk.ToggleButton(label = "Move curve")
        self.moveCurveButton.connect("toggled", self.on_move_curve_button_toggled)
        self.pack_start(self.moveCurveButton,False,False,0)

        self.resizeCurveButton = Gtk.ToggleButton(label = "Resize curve")
        self.resizeCurveButton.connect("toggled", self.on_resize_curve_button_toggled)
        self.pack_start(self.resizeCurveButton,False,False,0)

        self.rotateCurveButton = Gtk.ToggleButton(label = "Rotate curve")
        self.rotateCurveButton.connect("toggled", self.on_rotate_curve_button_toggled)
        self.pack_start(self.rotateCurveButton,False,False,0)

        self.splitCurveButton = Gtk.ToggleButton(label = "Split curve")
        self.pack_start(self.splitCurveButton,False,False,0)

    def update_active_curve(self,activeCurve):
        self.activeCurve = activeCurve

    def destroy_menu(self):
        self.appCanvas.delete_point_of_rotation()
        self.moveCurveButton.set_active(False)
        self.resizeCurveButton.set_active(False)
        self.rotateCurveButton.set_active(False)
        self.destroy()

    def set_active_widget(self,widget):
        if self.activeMenuButton != None and self.activeMenuButton != widget:
            self.activeMenuButton.set_active(False)
        self.activeMenuButton = widget

    def on_move_curve_button_toggled(self,widget):
        if widget.get_active() == True:
            self.set_active_widget(widget)
            self.pick_curve_active = self.canvas.mpl_connect('pick_event', self.appCanvas.pick_curve)
        else:
            self.canvas.mpl_disconnect(self.pick_curve_active)

    def on_resize_curve_button_toggled(self,widget):
        if widget.get_active() == True:
            self.set_active_widget(widget)
            self.getScaleWidget = getScaleWidget(self.appCanvas.resize_curve)
            self.appCanvas.set_getScaleWidget(self.getScaleWidget)
            self.add(self.getScaleWidget)
            self.show_all()
        else:
            self.getScaleWidget.destroy()
            self.getScaleWidget = None
            self.show_all()

    def on_rotate_curve_button_toggled(self,widget):
        if widget.get_active() == True:
            self.set_active_widget(widget)

            self.getAngleWidget = GetAngleWidget(self.appCanvas.rotate_curve,self.on_add_point_of_rotation_button_toggled)
            self.appCanvas.set_getAngleWidget(self.getAngleWidget)
            self.add(self.getAngleWidget)
            self.show_all()
        else:
            try:
                self.canvas.mpl_disconnect(self.add_point_of_rotation_active)
            except:
                pass
            self.appCanvas.delete_point_of_rotation()
            self.getAngleWidget.destroy()
            self.show_all()

    def on_add_point_of_rotation_button_toggled(self,widget):
        if widget.get_active() == True:
            self.add_point_of_rotation_active = self.canvas.mpl_connect('button_press_event', self.appCanvas.add_point_of_rotation)
        else:
            self.canvas.mpl_disconnect(self.add_point_of_rotation_active)
            self.appCanvas.delete_point_of_rotation()
            self.canvas.draw_idle()