import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class PointsVBox(Gtk.VBox):
    def __init__(self):
        super().__init__()
        self.set_size_request(40,100)

        image1 = Gtk.Image()
        image1.set_from_file('data/add_point.png')
        image2 = Gtk.Image()
        image2.set_from_file('data/delete_point.png')
        image3 = Gtk.Image()
        image3.set_from_file('data/move_point.png')

        self.addPointButton = Gtk.ToggleButton()
        self.addPointButton.set_image(image1)
        self.pack_start(self.addPointButton,False,False,0)

        self.deletePointButton = Gtk.ToggleButton()
        self.deletePointButton.set_image(image2)
        self.pack_start(self.deletePointButton,False,False,0)

        self.movePointButton = Gtk.ToggleButton()
        self.movePointButton.set_image(image3)
        self.pack_start(self.movePointButton,False,False,0)


class PointsMenu(Gtk.HBox):
    def __init__(self,appCanvas,activeCurve,curves,activeToggleButton):
        super().__init__()

        self.appCanvas = appCanvas
        self.canvas = appCanvas.get_canvas()
        self.activeCurve = activeCurve
        self.curves = curves

        self.activeToggleButton = activeToggleButton

        self.basicMenu = PointsVBox()
        self.add(self.basicMenu)

        self.basicMenu.addPointButton.connect("toggled", self.on_add_point_button_toggled)
        self.basicMenu.deletePointButton.connect("toggled", self.on_delete_point_button_toggled)
        self.basicMenu.movePointButton.connect("toggled", self.on_move_point_button_toggled)

    def update_active_curve(self,activeCurve):
        self.activeCurve = activeCurve

    def destroy_menu(self):
        self.basicMenu.addPointButton.set_active(False)
        self.basicMenu.deletePointButton.set_active(False)
        self.basicMenu.movePointButton.set_active(False)
        self.destroy()

    def set_active_widget(self,widget):
        if self.activeToggleButton != []:
            if self.activeToggleButton[0] != widget:
                self.activeToggleButton[0].set_active(False)
                self.activeToggleButton[0] = widget
        else:
            self.activeToggleButton.append(widget)

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


