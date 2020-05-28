import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from curves_editor_widget import GetAngleWidget,getScaleWidget

class CurveHBox(Gtk.HBox):
    def __init__(self):
        super().__init__()
        self.set_size_request(200,30)

        image1 = Gtk.Image()
        image1.set_from_file('data/select_curve.png')
        image2 = Gtk.Image()
        image2.set_from_file('data/move_curve.png')
        image3 = Gtk.Image()
        image3.set_from_file('data/resize_curve.png')
        image4 = Gtk.Image()
        image4.set_from_file('data/rotate_curve.png')
        image5 = Gtk.Image()
        image5.set_from_file('data/split_curve.png')
        image6 = Gtk.Image()
        image6.set_from_file('data/delete_curve.png')
        image7 = Gtk.Image()
        image7.set_from_file('data/choose_color2.png')
        image8 = Gtk.Image()
        image8.set_from_file('data/choose_width.png')

        self.selectCurveButton = Gtk.ToggleButton()
        self.selectCurveButton.set_image(image1)
        self.pack_start(self.selectCurveButton,False,False,0)

        self.moveCurveButton = Gtk.ToggleButton()
        self.moveCurveButton.set_image(image2)
        self.pack_start(self.moveCurveButton,False,False,0)

        self.resizeCurveButton = Gtk.ToggleButton()
        self.resizeCurveButton.set_image(image3)
        self.pack_start(self.resizeCurveButton,False,False,0)

        self.rotateCurveButton = Gtk.ToggleButton()
        self.rotateCurveButton.set_image(image4)
        self.pack_start(self.rotateCurveButton,False,False,0)

        self.splitCurveButton = Gtk.ToggleButton()
        self.splitCurveButton.set_image(image5)
        self.pack_start(self.splitCurveButton,False,False,0)

        self.deleteCurveButton = Gtk.Button()
        self.deleteCurveButton.set_image(image6)
        self.pack_start(self.deleteCurveButton,False,False,0)

        self.chooseColorButton = Gtk.Button()
        self.chooseColorButton.set_image(image7)
        self.pack_start(self.chooseColorButton,False,False,0)

        self.changeWidthButton = Gtk.ToggleButton()
        self.changeWidthButton.set_image(image8)
        self.pack_start(self.changeWidthButton,False,False,0)

class CurveMenu(Gtk.VBox):
    def __init__(self,appCanvas,activeCurve,curves,activeToggleButton,extraBox):
        super().__init__()

        self.appCanvas = appCanvas
        self.canvas = appCanvas.get_canvas()
        self.activeCurve = activeCurve
        self.curves = curves

        self.activeMenuButton = None
        self.pointOfRotation = None
        self.getAngleWidget = None
        self.getScaleWidget = None
        self.extraMenu = None

        self.extraBox = extraBox
        self.mainHBox = Gtk.HBox()
        self.add(self.mainHBox)
        self.activeToggleButton = activeToggleButton

        self.basicMenu = CurveHBox()
        self.mainHBox.add(self.basicMenu)

        self.basicMenu.moveCurveButton.connect("toggled", self.on_move_curve_button_toggled)
        self.basicMenu.resizeCurveButton.connect("toggled", self.on_resize_curve_button_toggled)
        self.basicMenu.rotateCurveButton.connect("toggled", self.on_rotate_curve_button_toggled)
        self.basicMenu.chooseColorButton.connect("clicked", self.on_choose_color_button_clicked)
        self.basicMenu.changeWidthButton.connect("toggled", self.on_change_width_button_toggled)


    def update_active_curve(self,activeCurve):
        if self.extraMenu != None:
            self.mainHBox.remove(self.extraMenu)
            self.extraMenu = None

        self.activeCurve = activeCurve

        if activeCurve != None and activeCurve.__class__.extraMenu != None:
            self.extraMenu = activeCurve.__class__.extraMenu
            self.extraMenu.activate(activeCurve)
            self.mainHBox.add(self.extraMenu)
            for b in self.extraMenu.bttns:
                btn,f,action = b
                btn.connect(action,lambda widget: self.on_button_clicked_template(widget,f))

        self.show_all()


    def destroy_menu(self):
        self.appCanvas.delete_point_of_rotation()
        self.basicMenu.moveCurveButton.set_active(False)
        self.basicMenu.resizeCurveButton.set_active(False)
        self.basicMenu.rotateCurveButton.set_active(False)
        self.basicMenu.rotateCurveButton.set_active(False)
        self.destroy()

    def set_active_widget(self,widget):
        if self.activeToggleButton != []:
            if self.activeToggleButton[0] != widget:
                self.activeToggleButton[0].set_active(False)
                self.activeToggleButton[0] = widget
        else:
            self.activeToggleButton.append(widget)

    def on_move_curve_button_toggled(self,widget):
        if widget.get_active() == True:
            self.set_active_widget(widget)
            self.pick_curve_active = self.canvas.mpl_connect('pick_event', self.appCanvas.pick_curve)
        else:
            self.canvas.mpl_disconnect(self.pick_curve_active)

    def on_resize_curve_button_toggled(self,widget):
        if widget.get_active() == True:
            self.set_active_widget(widget)
            self.getScaleWidget = getScaleWidget(self.appCanvas.resize_curve)
            self.appCanvas.set_getScaleWidget(self.getScaleWidget)
            self.extraBox.add(self.getScaleWidget)
            self.extraBox.show_all()
        else:
            self.getScaleWidget.destroy()
            self.getScaleWidget = None
            self.extraBox.show_all()

    def on_rotate_curve_button_toggled(self,widget):
        if widget.get_active() == True:
            self.set_active_widget(widget)

            self.getAngleWidget = GetAngleWidget(self.appCanvas.rotate_curve,self.on_add_point_of_rotation_button_toggled)
            self.appCanvas.set_getAngleWidget(self.getAngleWidget)
            self.extraBox.add(self.getAngleWidget)
            self.extraBox.show_all()
        else:
            try:
                self.canvas.mpl_disconnect(self.add_point_of_rotation_active)
            except:
                pass
            self.appCanvas.delete_point_of_rotation()
            self.getAngleWidget.destroy()
            self.extraBox.show_all()

    def on_add_point_of_rotation_button_toggled(self,widget):
        if widget.get_active() == True:
            self.add_point_of_rotation_active = self.canvas.mpl_connect('button_press_event', self.appCanvas.add_point_of_rotation)
        else:
            self.canvas.mpl_disconnect(self.add_point_of_rotation_active)
            self.appCanvas.delete_point_of_rotation()
            self.canvas.draw_idle()

    def on_choose_color_button_clicked(self,widget):
        colorChooserDialog = Gtk.ColorChooserDialog()
        stat = colorChooserDialog.run()
        col = colorChooserDialog.get_rgba()
        self.activeCurve.change_line_color(col.red,col.green,col.blue)
        colorChooserDialog.destroy()

    def on_change_width_button_toggled(self,widget):
        if widget.get_active() == True:
            self.set_active_widget(widget)
            self.getScaleWidget = getScaleWidget(self.appCanvas.change_line_width)
            self.appCanvas.set_getScaleWidget(self.getScaleWidget)
            self.extraBox.add(self.getScaleWidget)
            self.extraBox.show_all()
        else:
            self.getScaleWidget.destroy()
            self.getScaleWidget = None
            self.extraBox.show_all()

    def on_button_toggled_template(self,widget,f):
        if widget.get_active() == True:
            f(widget,self.canvas)
            self.canvas.draw_idle()
        else:
            self.canvas.draw_idle()

    def on_button_clicked_template(self,widget,f):
            f(widget,self.canvas)
            self.canvas.draw_idle()
