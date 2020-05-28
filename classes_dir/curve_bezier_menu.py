import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from classes_dir.extra_menu import ExtraMenu

class BezierCurveMenu(ExtraMenu):
    def __init__(self):
        super().__init__()

        self.change_degree = None
        self.activeCurve = None

        self.entry = Gtk.Entry()
        self.entry.set_max_length(2)
        self.entry.set_width_chars(3)
        self.pack_start(self.entry,False,False,0)

        self.degreeUpButton = Gtk.Button("Change degree")
        self.pack_start(self.degreeUpButton,False,False,0)

        self.bttns.append((self.entry,self.change_degree_clicked,'activate'))
        self.bttns.append((self.degreeUpButton,self.change_degree_clicked,'clicked'))

    def get_entry_text(self):
        return self.entry.get_text()

    def set_entry_text(self,text):
        return self.entry.set_text(text)

    def change_degree_clicked(self,widget,canvas):
        if self.activeCurve != None:
            try:
                d = int(self.get_entry_text())
            except:
                return    
            self.activeCurve.change_degree(d)

    def activate(self,activeCurve):
        self.activeCurve = activeCurve
        if activeCurve != None:
            self.set_entry_text(str(activeCurve.numberOfPoints))
            self.change_degree = activeCurve.change_degree