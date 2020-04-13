import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio,GLib

from app_window import MainWindow

with open("data/menu.xml",'r') as menufile:
    MENU_XML = menufile.read()

class App(Gtk.Application):
    def __init__(self):
        super().__init__()
        self.window = None
    def do_startup(self):
        Gtk.Application.do_startup(self)
        builder = Gtk.Builder.new_from_string(MENU_XML, -1)
        self.set_menubar(builder.get_object("view-menu"))

    def do_activate(self):
        if not self.window:
            self.window = MainWindow(application=self)

        self.window.present()

    def do_command_line(self, command_line):
        self.activate()
        return 0

if __name__ == "__main__":
    app = App()
    app.run(sys.argv)