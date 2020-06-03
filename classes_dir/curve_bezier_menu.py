import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from classes_dir.extra_menu import ExtraMenu

class BezierCurveMenu(ExtraMenu):
    def __init__(self):
        super().__init__()

        self.activeCurve = None
        self.canvas = None

        self.entryDegree = Gtk.Entry()
        self.entryDegree.set_max_length(2)
        self.entryDegree.set_width_chars(3)
        self.pack_start(self.entryDegree,False,False,0)

        image1 = Gtk.Image()
        image1.set_from_file('data/degree_up.png')
        image2 = Gtk.Image()
        image2.set_from_file('data/degree_down.png')

        self.degreeUpButton = Gtk.Button()
        self.degreeUpButton.set_image(image1)
        self.pack_start(self.degreeUpButton,False,False,0)

        self.entryK = Gtk.Entry()
        self.entryK.set_max_length(2)
        self.entryK.set_width_chars(3)
        self.entryK.set_text('0')
        self.pack_start(self.entryK,False,False,0)

        self.entryL = Gtk.Entry()
        self.entryL.set_max_length(2)
        self.entryL.set_width_chars(3)
        self.entryL.set_text('0')
        self.pack_start(self.entryL,False,False,0)

        self.degreeDownButton = Gtk.Button()
        self.degreeDownButton.set_image(image2)
        self.pack_start(self.degreeDownButton,False,False,0)

        #self.bttns.append((self.entryDegree,self.degree_up_clicked,'activate'))
        #self.bttns.append((self.degreeDownButton,self.degree_down_clicked,'clicked'))
        #self.bttns.append((self.degreeUpButton,self.degree_up_clicked,'clicked'))

        self.degreeDownButton.connect('clicked',self.degree_down_clicked)
        self.degreeUpButton.connect('clicked',self.degree_up_clicked)

    def get_entryDegree_text(self):
        return self.entryDegree.get_text()

    def get_entryK_text(self):
        return self.entryK.get_text()

    def get_entryL_text(self):
        return self.entryL.get_text()

    def set_entryDegree_text(self,text):
        return self.entryDegree.set_text(text)

    def degree_up_clicked(self,widget):
        if self.activeCurve != None:
            try:
                d = int(self.get_entryDegree_text())
                self.activeCurve.degree_up(d)
                self.canvas.draw_idle()
            except:
                return   

    def degree_down_clicked(self,widget):
        if self.activeCurve != None:
            try:
                d = int(self.get_entryDegree_text())
                k = int(self.get_entryK_text())
                l = int(self.get_entryL_text())
                self.activeCurve.degree_down(d,k,l)
                self.canvas.draw_idle()
            except:
                return    

    def activate(self,activeCurve,canvas,set_active_widget):
        self.activeCurve = activeCurve
        self.canvas = canvas
        if activeCurve != None:
            self.set_entryDegree_text(str(activeCurve.numberOfPoints))
            self.degree_up = activeCurve.degree_up