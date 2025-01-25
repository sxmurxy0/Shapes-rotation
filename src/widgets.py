from matplotlib.backends.backend_qtagg import NavigationToolbar2QT, FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QComboBox
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize
from os import path

class DisplayWidget(QWidget):
    def __init__(self, rotator):
        super().__init__()
        self.setObjectName('display_widget')
        self.setFixedSize(730, 500)
        self.setWindowTitle('Поворот фигур')
        self.setWindowIcon(QIcon(QPixmap('assets/display_icon.png')))
        self.setStyleSheet('#display_widget { background-color: white; }')
        self.rotator = rotator

        self.canvas = FigureCanvas(self.rotator.figure)
        self.canvas.setGeometry(0, 0, self.width(), self.height())
        self.canvas.setParent(self)
        self.toolbar = NavigationToolbar(self.canvas, self.canvas, self.rotator)

class NavigationToolbar(NavigationToolbar2QT):
    def __init__(self, canvas, parent, rotator):
        self.toolitems = (
            ('Reset', 'Reset original state', 'trashbin', 'reset_state'),
            (None, None, None, None),
            ('Back', 'Back to previous view', 'back', 'back'),
            ('Forward', 'Forward to next view', 'forward', 'forward'),
            (None, None, None, None),
            ('Pan', 'Pan a plot', 'position', 'pan'),
            (None, None, None, None),
            ('Settings', 'Open settings', 'settings', 'open_settings'),
            (None, None, None, None),
            ('Rotate', 'Rotate shape', 'play', 'rotate_shape')
        )
        super().__init__(canvas, parent)
        self.setIconSize(QSize(20, 20))
        self.setFixedWidth(parent.width())
        self.set_message = lambda s: None
        self.rotator = rotator
    
    def reset_state(self):
        self.rotator.reset_state()

    def open_settings(self):
        self.rotator.settings_widget.show()
    
    def rotate_shape(self):
        self.rotator.rotate_shape()
    
    def _icon(self, name):
        local_path = 'assets/' + name
        return QIcon(QPixmap(local_path)) if path.exists(local_path) else super()._icon(name)

class SettingsWidget(QWidget):
    def __init__(self, parent, rotator):
        super().__init__(parent, Qt.WindowType.Window)
        self.setObjectName('settings_widget')
        self.setFixedSize(312, 105)
        self.setWindowTitle('Параметры')
        self.setWindowIcon(QIcon(QPixmap('assets/settings_icon.png')))
        self.setStyleSheet('#settings_widget { background-color: white; }')
        self.rotator = rotator

        self.initial_pos_x = QLineEdit(self)
        self.initial_pos_y = QLineEdit(self)
        self.initial_pos_z = QLineEdit(self)
        for line_edit, data in [(self.initial_pos_x, (50, 'X')), (self.initial_pos_y, (134, 'Y')), (self.initial_pos_z, (218, 'Z'))]:
            line_edit.setGeometry(data[0], 10, 75, 21)
            line_edit.setPlaceholderText(data[1])
            line_edit.textChanged.connect(self.rotator.update_shape)

        self.rotation_axis_x = QLineEdit(self)
        self.rotation_axis_y = QLineEdit(self)
        self.rotation_axis_z = QLineEdit(self)
        for line_edit, data in [(self.rotation_axis_x, (50, 'I')), (self.rotation_axis_y, (134, 'J')), (self.rotation_axis_z, (218, 'K'))]:
            line_edit.setGeometry(data[0], 40, 75, 21)
            line_edit.setPlaceholderText(data[1])
            line_edit.textChanged.connect(self.rotator.update_rotation_axis)

        for data in [(10, 'assets/position.png'), (40, 'assets/direction.png'), (70, 'assets/rotation.png')]:
            label = QLabel(self)
            label.setGeometry(20, data[0], 20, 20)
            label.setPixmap(QPixmap(data[1]))
            label.setScaledContents(True)

        self.rotation_angel = QLineEdit(self)
        self.rotation_angel.setGeometry(50, 70, 75, 21)
        self.rotation_angel.setPlaceholderText('Угол')

        shape_label = QLabel(self)
        shape_label.setGeometry(134, 70, 20, 20)
        shape_label.setPixmap(QPixmap('assets/shape.png'))
        shape_label.setScaledContents(True)

        self.shape_size = QLineEdit(self)
        self.shape_size.setGeometry(162, 70, 47, 21)
        self.shape_size.setPlaceholderText('Размер')
        self.shape_size.textChanged.connect(self.rotator.update_shape)

        self.shape_selection = QComboBox(self)
        self.shape_selection.setGeometry(218, 70, 75, 21)
        self.shape_selection.currentIndexChanged.connect(self.rotator.reset_state)