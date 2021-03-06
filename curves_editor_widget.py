import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class CurveWidget(Gtk.Box):
    def __init__(self,curve,radioButton,counter,radio_toggled_function,canvas):
        self.curve = curve
        self.canvas = canvas
        super().__init__()
       
        self.radioButton = Gtk.RadioButton.new_from_widget(radioButton)
        self.toggleButton = Gtk.ToggleButton(label=self.curve.curveType + ' ' + str(counter))

        self.radioButton.set_active(True)
        self.radioButton.connect("toggled",radio_toggled_function)

        self.toggleButton.set_active(True)
        self.toggleButton.connect("toggled",self.on_button_toggled)

        self.pack_start(self.radioButton,False,False,0)
        self.pack_start(self.toggleButton,False,False,5)

    def get_curve(self):
        return self.curve
    def get_radioButton(self):
        return self.radioButton
    def get_toggleButton(self):
        return self.toggleButton

    def on_button_toggled(self,widget):
        if widget.get_active():
            self.curve.show_curve()
            self.canvas.draw_idle()
        else:
            self.curve.hide_curve()
            self.canvas.draw_idle()

class CurvesTypesComboBox(Gtk.ComboBoxText):

    def __init__(self,curveTypes):
        super().__init__()
        for curveType in curveTypes:
            self.append(curveType,curveType)

        self.set_active_id(curveTypes[0])

    def set_current_type(self,curveType):
        self.set_active_id(curveType)

    def get_current_type(self):
        return self.get_active_text()

    
class GetAngleWidget(Gtk.Box):
    def __init__(self,apply_function,add_point_function):
        super().__init__()

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

    def get_entry_text(self):
        return self.entry.get_text()

    def get_applyButton(self):
        return self.applyButton

class getScaleWidget(Gtk.Grid):
    def __init__(self,apply_function):
        super().__init__()

        self.scale = Gtk.Scale(orientation = Gtk.Orientation(0),adjustment=Gtk.Adjustment(100,25,200,5,10,0))
        self.scale.set_size_request(300,10)
        self.scale.set_value_pos(Gtk.PositionType.RIGHT)
        self.scale.set_digits(0)

        self.applyButton = Gtk.Button(label="Apply")
        self.applyButton.connect("clicked",apply_function)

        self.attach(self.scale,0,0,3,1)
        self.attach(self.applyButton,3,0,1,1)

        self.set_column_spacing(20)

    def get_scale_value(self):
        return self.scale.get_value()

    def reset_scale_value(self):
        self.scale.set_value(100)
    
class AnimationModeBox(Gtk.Box):
    def __init__(self,path,frameName,savefig):
        super().__init__()
        self.n = 0
        self.frameName = frameName
        self.path = path
        self.savefig = savefig
        frameButton = Gtk.Button("Frame")
        self.add(frameButton)
        frameButton.connect("clicked",self.make_frame)

    def make_frame(self,widget):
        self.savefig(self.path + '/' + self.frameName + '_' + str(self.n))
        self.n += 1


