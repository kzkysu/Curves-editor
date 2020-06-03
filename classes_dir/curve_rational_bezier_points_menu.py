import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from classes_dir.extra_menu import ExtraMenu

class RationalBezierPointsMenu(ExtraMenu):
    def __init__(self):
        super().__init__()

        self.activeCurve = None
        self.activePoint = None
        self.canvas = None
        self.set_active_widget = None
        self.set_orientation(Gtk.Orientation.VERTICAL)

        image1 = Gtk.Image()
        image1.set_from_file('data/choose_point.png')
        image2 = Gtk.Image()
        image2.set_from_file('data/change_weight.png')

        self.choosePointButton = Gtk.ToggleButton()
        self.choosePointButton.connect("toggled",self.choose_point_toggled)
        self.choosePointButton.set_image(image1)
        self.pack_start(self.choosePointButton,False,False,0)

        self.entryActivePoint = Gtk.Entry()
        self.entryActivePoint.set_max_length(2)
        self.entryActivePoint.set_width_chars(3)
        self.pack_start(self.entryActivePoint,False,False,0)

        self.entryWeight = Gtk.Entry()
        self.entryWeight.set_max_length(2)
        self.entryWeight.set_width_chars(3)
        self.pack_start(self.entryWeight,False,False,0)

        self.changeWeightButton = Gtk.Button()
        self.changeWeightButton.connect("clicked",self.change_weight)
        self.changeWeightButton.set_image(image2)
        self.pack_start(self.changeWeightButton,False,False,0)


    def get_entryActivePoint_text(self):
        return self.entryActivePoint.get_text()

    def get_entryWeight_text(self):
        return self.entryWeight.get_text()

    def set_entryActivePoint_text(self,text):
        return self.entryActivePoint.set_text(text)

    def set_entryWeight_text(self,text):
        return self.entryWeight.set_text(text)

    def activate(self,activeCurve,canvas,set_active_widget):
        self.activeCurve = activeCurve
        self.canvas = canvas
        self.set_active_widget = set_active_widget

    def choose_point_toggled(self,widget):
        if widget.get_active():
            self.set_active_widget(widget)
            self.choose_point_active = self.canvas.mpl_connect('pick_event', self.activate_point)
        else:
            self.activePoint = None
            self.activeCurve.activePoint = None
            self.canvas.mpl_disconnect(self.choose_point_active)
            self.set_entryActivePoint_text('')
            self.set_entryWeight_text('')

    def activate_point(self,event):
        self.activeCurve.activate_point(event.mouseevent.xdata,event.mouseevent.ydata)
        self.activePoint = self.activeCurve.activePoint
        self.set_entryActivePoint_text(str(self.activePoint + 1))
        self.set_entryWeight_text(str(self.activeCurve.get_weight(self.activePoint)))

    def change_weight(self,widget):
        try:
            if self.activePoint != None and self.activePoint != int(self.get_entryActivePoint_text())-1:
                self.activePoint = int(self.get_entryActivePoint_text())-1
                self.activeCurve.activePoint = int(self.get_entryActivePoint_text())-1
        except:
            print("Wrong points number.")

        try:
            if self.activePoint != None:
                wgh = float(self.get_entryWeight_text())
                if self.activeCurve.get_weight(self.activePoint) != wgh:
                    self.activeCurve.set_weight(self.activePoint,wgh)
                    self.canvas.draw_idle()
        except:
            print("Wrong weight.")
