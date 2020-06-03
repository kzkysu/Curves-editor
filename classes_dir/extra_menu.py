import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ExtraMenu(Gtk.Box):
    def __init__(self):
        super().__init__()

    def activate(self,activeCurve,canvas,set_active_widget):
        pass
