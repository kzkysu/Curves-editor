import os
import sys
import gi
import re
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio,GLib
import imageio

def make_gif_dialog(parent,action,userData):
        dialog = Gtk.FileChooserDialog(title="Please choose a directory to make gif", parent=parent,
            action=Gtk.FileChooserAction.SELECT_FOLDER)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

        #dialog.set_current_name("newgif.gif")
        dialog.set_do_overwrite_confirmation(True)
        dialog.set_current_folder(os.getcwd() + "/animation")

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            path = dialog.get_filename()
            make_gif(path)
            
        dialog.destroy()

def make_gif(path):
    name = path.split('/')[-1]
    #print(name)
    filenames = os.listdir(path)
    filenames.sort(key=natural_keys)
    try:
        with imageio.get_writer(os.getcwd() + "/gifs/" + name + ".gif", mode='I') as writer:
            for filename in filenames:
                print(filename)
                image = imageio.imread(path + "/" +filename)
                writer.append_data(image)
    except:
        print("Error during making gif.")


def atoi(text):
    return int(text) if text.isdigit() else text
def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)',text) ]
