import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class CurveWidget(Gtk.Box):
    def __init__(self,curve,radioButton,counter):
        self.curve = curve
        super(CurveWidget,self).__init__()
       
        self.radioButton = Gtk.RadioButton.new_from_widget(radioButton)
        self.toggleButton = Gtk.ToggleButton(label="Curve " + str(counter))

        self.pack_start(self.radioButton,False,False,0)
        self.pack_start(self.toggleButton,False,False,5)

    def get_curve(self):
        return self.curve
    def get_radioButton(self):
        return self.radioButton
    def get_toggleButton(self):
        return self.toggleButton