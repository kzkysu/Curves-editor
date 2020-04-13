import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio,GLib

from matplotlib import axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class EditPointsMenu(Gtk.HBox):
    def __init__(self,appCanvas,activeCurve,curves):
        super().__init__()

        self.appCanvas = appCanvas
        self.canvas = appCanvas.get_canvas()
        self.activeCurve = activeCurve
        self.curves = curves

        self.activeMenuButton = None

        self.addPointButton = Gtk.ToggleButton(label="Add point")
        self.addPointButton.connect("toggled", self.on_add_point_button_toggled)
        self.pack_start(self.addPointButton,False,False,0)

        self.deletePointButton = Gtk.ToggleButton(label="Delete point")
        self.deletePointButton.connect("toggled", self.on_delete_point_button_toggled)
        self.pack_start(self.deletePointButton,False,False,0)

        self.movePointButton = Gtk.ToggleButton(label="Move point")
        self.movePointButton.connect("toggled", self.on_move_point_button_toggled)
        self.pack_start(self.movePointButton,False,False,0)

    def update_active_curve(self,activeCurve):
        self.activeCurve = activeCurve

    def destroy_menu(self):
        self.addPointButton.set_active(False)
        self.deletePointButton.set_active(False)
        self.movePointButton.set_active(False)
        self.destroy()

    def set_active_widget(self,widget):
        if self.activeMenuButton != None and self.activeMenuButton != widget:
            self.activeMenuButton.set_active(False)
        self.activeMenuButton = widget

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
