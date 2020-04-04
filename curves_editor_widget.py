import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class CurveWidget(Gtk.Box):
    def __init__(self,curve,radioButton,counter,radio_toggled_function):
        self.curve = curve
        super(CurveWidget,self).__init__()
       
        self.radioButton = Gtk.RadioButton.new_from_widget(radioButton)
        self.toggleButton = Gtk.ToggleButton(label="Curve " + str(counter))

        self.radioButton.set_active(True)
        self.radioButton.connect("toggled",radio_toggled_function)

        self.pack_start(self.radioButton,False,False,0)
        self.pack_start(self.toggleButton,False,False,5)

    def get_curve(self):
        return self.curve
    def get_radioButton(self):
        return self.radioButton
    def get_toggleButton(self):
        return self.toggleButton

class GetAngleWidget(Gtk.Box):
    def __init__(self,apply_function,add_point_function):
        super(GetAngleWidget,self).__init__()

        self.addPointButton =  Gtk.ToggleButton(label="Add point of rotation")
        self.entry = Gtk.Entry()
        self.applyButton = Gtk.Button(label="Apply")

        self.addPointButton.connect("toggled",add_point_function)
        self.applyButton.connect("clicked",apply_function)
        self.entry.connect("activate",apply_function)

        self.pack_start(self.addPointButton,False,False,0)
        self.pack_start(self.entry,False,False,0)
        self.pack_start(self.applyButton,False,False,0)

    def get_addPointButton(self):
        return self.addPointButton

    def get_entry(self):
        return self.entry

    def get_applyButton(self):
        return self.applyButton
