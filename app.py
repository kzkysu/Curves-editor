import os
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio,GLib

from app_window import MainWindow
import animation_maker as anim

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
        self.add_gio_action('export',self.export_to_png)
        self.add_gio_action('exportanimation',self.make_gif)
        self.add_gio_action('hidepointsall',self.on_hidepointsall_clicked)
        self.add_gio_action('showpointsall',self.on_showpointsall_clicked)
        self.add_gio_action('showpoints',self.on_showpoints_clicked)
        self.add_gio_action('hidepoints',self.on_hidepoints_clicked)
        self.add_gio_action('shownumbers',self.on_shownumbers_clicked)
        self.add_gio_action('hidenumbers',self.on_hidenumbers_clicked)
        self.add_gio_action('showhull',self.on_showhull_clicked)
        self.add_gio_action('hidehull',self.on_hidehull_clicked)
        '''self.add_gio_action('setbackground',self.load_background)
        self.add_gio_action('setwhitebackground',self.set_white_background)'''

        '''hidePointsAction = Gio.SimpleAction.new_stateful("hidepoints", None,
                                           GLib.Variant.new_boolean(False))
        hidePointsAction.connect("change-state", self.on_hidepoints_toggled)
        self.add_action(hidePointsAction)

        showNumbersAction = Gio.SimpleAction.new_stateful("shownumbers", None,
                                           GLib.Variant.new_boolean(False))
        showNumbersAction.connect("change-state", self.on_shownumbers_toggled)
        self.add_action(showNumbersAction)'''


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

    def load_background(self,action,userData):
        dialog = Gtk.FileChooserDialog(title="Please choose a background image", parent=self.window,
            action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

        dialog.set_current_folder(os.getcwd() + "/data")

        fileFilter = Gtk.FileFilter()
        fileFilter.add_pattern("*.png")
        dialog.add_filter(fileFilter)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            path = dialog.get_filename()
            self.window.set_background_image(path)
            
        dialog.destroy()

    def set_white_background(self,action,userData):
        path = os.getcwd() + "/data/white_background.png"
        self.window.set_background_image(path)

    def export_to_png(self,action,userData):
        dialog = Gtk.FileChooserDialog(title="Please choose a file", parent=self.window,
            action=Gtk.FileChooserAction.SAVE)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE_AS, Gtk.ResponseType.OK)

        dialog.set_current_name("newfigure.png")
        dialog.set_do_overwrite_confirmation(True)
        dialog.set_current_folder(os.getcwd() + "/saved_figures")

        fileFilter = Gtk.FileFilter()
        fileFilter.add_pattern("*.png")
        dialog.add_filter(fileFilter)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            path = dialog.get_filename()
            self.window.save_fig_to_png(path)
            
        dialog.destroy()

    '''def on_hidepoints_toggled(self,action,value):
        action.set_state(value)
        if value.get_boolean():
            self.window.hide_points()
        else:
            self.window.show_points()
    
    def on_shownumbers_toggled(self,action,value):
        action.set_state(value)
        if value.get_boolean():
            self.window.show_numbers()
        else:
            self.window.hide_numbers()'''
    def on_hidepointsall_clicked(self,action,value):
        self.window.hide_points_all()

    def on_showpointsall_clicked(self,action,value):
        self.window.show_points_all()

    def on_showpoints_clicked(self,action,value):
        self.window.show_points()

    def on_hidepoints_clicked(self,action,value):
        self.window.hide_points()
    
    def on_shownumbers_clicked(self,action,value):
        self.window.show_numbers()

    def on_hidenumbers_clicked(self,action,value):
        self.window.hide_numbers()

    def on_showhull_clicked(self,action,value):
        self.window.show_hull()

    def on_hidehull_clicked(self,action,value):
        self.window.hide_hull()

    def on_change_active_curve(self,points_visible):
        if points_visible:
            pass

    def make_gif(self,action,userData):
        anim.make_gif_dialog(self.window,action,userData)


if __name__ == "__main__":
    app = App()
    app.run(sys.argv)