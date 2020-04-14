import os
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

        self.add_gio_action('saveas',self.save_file_as)
        self.add_gio_action('load',self.load_json)

    def do_activate(self):
        if not self.window:
            self.window = MainWindow(application=self)

        self.window.present()

    def add_gio_action(self, name, callback):
            action = Gio.SimpleAction.new(name, None)
            action.connect('activate', callback)
            self.add_action(action)

    def save_file_as(self,action,userData):
        dialog = Gtk.FileChooserDialog(title="Please choose a file", parent=self.window,
            action=Gtk.FileChooserAction.SAVE)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE_AS, Gtk.ResponseType.OK)

        dialog.set_current_name("newcurve.json")
        dialog.set_do_overwrite_confirmation(True)
        dialog.set_current_folder(os.getcwd() + "/saved_curves")

        fileFilter = Gtk.FileFilter()
        fileFilter.add_pattern("*.json")
        dialog.add_filter(fileFilter)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            path = dialog.get_filename()
            self.window.save_active_curve(path)
            
        dialog.destroy()

    def load_json(self,action,userData):
        dialog = Gtk.FileChooserDialog(title="Please choose a file", parent=self.window,
            action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

        dialog.set_current_folder(os.getcwd() + "/saved_curves")

        fileFilter = Gtk.FileFilter()
        fileFilter.add_pattern("*.json")
        dialog.add_filter(fileFilter)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            path = dialog.get_filename()
            self.window.load_curve(path)
            
        dialog.destroy()


if __name__ == "__main__":
    app = App()
    app.run(sys.argv)