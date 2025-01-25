from PyQt6.QtWidgets import QApplication
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation as Animation
from widgets import DisplayWidget, SettingsWidget
from shapes import ShapesProvider
from quaternions import Quaternion
from renderers import Renderer

class Rotator(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.figure = Figure(dpi = 70)
        self.axes = Axes3D(self.figure)
        self.figure.add_axes(self.axes)
      
        self.shapes_provider = ShapesProvider()
        self.renderer = Renderer(self.axes)
        self.display_widget = DisplayWidget(self)
        self.settings_widget = SettingsWidget(self.display_widget, self)

        self.frames_count = 45
        self.rotating = False
        self.angle = 0
        self.animation = None
        self.shape_name = None
        self.shape_data = None
        self.axis = None
        self.shape_artist = None
        self.rotation_axis_artist = None

    def init(self):
        self.axes.set_xlim(-4, 4)
        self.axes.set_ylim(-4, 4)
        self.axes.set_zlim(-4, 4)

        self.block_signals(True)
        self.settings_widget.initial_pos_x.setText('0')
        self.settings_widget.initial_pos_y.setText('0')
        self.settings_widget.initial_pos_z.setText('0')

        self.settings_widget.rotation_axis_x.setText('1')
        self.settings_widget.rotation_axis_y.setText('1')
        self.settings_widget.rotation_axis_z.setText('1')

        self.settings_widget.rotation_angel.setText('90')
        self.settings_widget.shape_size.setText('5')
        self.block_signals(False)
        
        shapes = self.shapes_provider.shapes_names()
        for shape in shapes:
            self.settings_widget.shape_selection.addItem(shape)
        
        self.display_widget.show()

    def get_initial_pos(self):
        try:
            x = float(self.settings_widget.initial_pos_x.text())
            y = float(self.settings_widget.initial_pos_y.text())
            z = float(self.settings_widget.initial_pos_z.text())
            return (x, y, z)
        except Exception: return None

    def get_rotation_axis(self):
        try:
            x = float(self.settings_widget.rotation_axis_x.text())
            y = float(self.settings_widget.rotation_axis_y.text())
            z = float(self.settings_widget.rotation_axis_z.text())
            return (x, y, z)
        except Exception: return None
    
    def get_rotation_angle(self):
        try:
            return float(self.settings_widget.rotation_angel.text())
        except Exception: return None
    
    def get_size(self):
        try:
            return float(self.settings_widget.shape_size.text())
        except Exception: return None
    
    def block_signals(self, state):
        settings = self.settings_widget
        for widget in (settings.initial_pos_x, settings.initial_pos_y, settings.initial_pos_z, settings.shape_size):
            widget.blockSignals(state)

    def block_major_settings(self, state):
        settings = self.settings_widget
        for widget in (settings.initial_pos_x, settings.initial_pos_y, settings.initial_pos_z, settings.shape_size):
            widget.setEnabled(not state)
    
    def block_minor_settings(self, state):
        settings = self.settings_widget
        for widget in (settings.rotation_axis_x, settings.rotation_axis_y, settings.rotation_axis_z, settings.rotation_angel, settings.shape_selection):
            widget.setEnabled(not state)
    
    def reset_state(self):
        if self.rotating: return
        self.block_major_settings(False)
        self.display_widget.toolbar.home()
        self.update_shape()

    def update_shape(self):
        if self.shape_artist:
            self.shape_artist.remove()
            self.shape_artist = None
        
        if not self.rotating:
            initial_pos = self.get_initial_pos()
            size = self.get_size()
            self.shape_name = None
            self.shape_data = None
            if initial_pos and size and size > 0:
                self.shape_name = self.settings_widget.shape_selection.currentText()
                self.shape_data = self.shapes_provider.build_shape(self.shape_name, initial_pos, size)
                self.shape_artist = self.renderer.render_shape(self.shape_data)
        else:
            self.shape_artist = self.renderer.render_shape(self.shape_data)
        self.figure.canvas.draw_idle()

    def update_rotation_axis(self):
        if self.rotation_axis_artist:
            for line in self.rotation_axis_artist: line.remove()
            self.rotation_axis_artist = None
        
        self.axis = self.get_rotation_axis()
        if self.axis:
            self.rotation_axis_artist = self.renderer.render_polyline([(0, 0, 0), self.axis], linestyle = 'dashed', linewidth = 4)
        self.figure.canvas.draw_idle()
    
    def update_rotating(self, frame):
        q1 = Quaternion.rotation_quaternion(self.axis, self.angle / (self.frames_count + 1))
        q2 = q1.inverse()
        vertices = [(q1 * Quaternion(0, vertex[0], vertex[1], vertex[2]) * q2).to_vector() 
            for vertex in self.shape_data.vertices()]
        self.shape_data.set_vertices(vertices)
        self.update_shape()
        if frame == self.frames_count - 1:
            self.block_minor_settings(False)
            self.rotating = False
    
    def rotate_shape(self):
        if self.rotating: return
        self.angle = self.get_rotation_angle()
        if not self.shape_data or not self.axis or not self.angle: return
        self.rotating = True
        self.block_minor_settings(True)
        self.block_major_settings(True)
        self.animation = Animation(self.figure, self.update_rotating, frames = self.frames_count, interval = 10, repeat = False)
        self.figure.canvas.draw_idle()