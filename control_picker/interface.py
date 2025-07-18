import maya.cmds as cmds
from maya import OpenMayaUI as omui
import importlib
import os.path
from functools import partial

from control_picker.utils import qtpyside
PySide, wrapInstance = qtpyside.get_version()

from PySide.QtCore import Qt, QObject, SIGNAL
from PySide.QtGui import QIcon
from PySide.QtWidgets import (QWidget,
                              QVBoxLayout,
                              QHBoxLayout,
                              QGridLayout,
                              QPushButton,
                              QScrollArea,
                              QLabel,
                              QSizePolicy,
                              QLineEdit)

from control_picker.user_interface.pages import control_libary, sidebar, settings
from control_picker.script import remove, add, make_control

ui_pages = [control_libary, sidebar, settings]
scripts = [remove, add, make_control]

for module_list in [ui_pages, scripts]:
    for module in module_list:
        importlib.reload(module)

mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)


class Interface(QWidget):
    def __init__(self, *args, **kwargs):
        super(Interface, self).__init__(*args, **kwargs)
        UI_NAME = "Control Picker"

        self.check_existing_uis(UI_NAME=UI_NAME)
        self.setParent(mayaMainWindow)
        self.setWindowFlags(Qt.Window)
        self.initUI()
        self.set_style()
        self.setFixedWidth(620)
        self.setFixedHeight(400)
        self.setWindowTitle(UI_NAME)
        self.setObjectName(UI_NAME)

        self.connections()

    def initUI(self):
        # Base Layout
        self.verticle_layout = QVBoxLayout(self)
        self.verticle_layout.setContentsMargins(0,0,0,0)

        # Main Layout
        self.main_layout_widget = QWidget()
        self.main_layout = QHBoxLayout(self.main_layout_widget)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setStretch(1,100)
        self.verticle_layout.addWidget(self.main_layout_widget)

        # Sidebar Layout
        self.sidebar_widget = QWidget()
        self.sidebar_widget.setMaximumWidth(125)
        self.sidebar_layout = QVBoxLayout(self.sidebar_widget)
        # self.sidebar_layout.setContentsMargins(10,10,0,0)
        self.sidebar_layout.setSizeConstraint(QVBoxLayout.SetMinimumSize)
        self.sidebar_layout.setSpacing(10)

        self.sidebar_instance = sidebar.sidebar_ui(self, self.sidebar_layout)
        self.add_button, self.trash_button = self.sidebar_instance.return_objects()
        self.main_layout.addWidget(self.sidebar_widget)

        # Control Libary
        self.libary_widget = QWidget()
        self.libary_widget.setMaximumWidth(500)
        self.libary_layout = QVBoxLayout(self.libary_widget)
        self.libary_layout.setSizeConstraint(QVBoxLayout.SetMaximumSize)
        self.init_controllibary()
        self.main_layout.addWidget(self.libary_widget)

        # Settings array
        self.settings_layout_vert = QVBoxLayout()
        self.settings_layout_top = QHBoxLayout()
        self.settings_layout_botton = QHBoxLayout()
        self.libary_layout.addLayout(self.settings_layout_vert)
        self.settings_layout_vert.addLayout(self.settings_layout_top)
        self.settings_layout_vert.addLayout(self.settings_layout_botton)
        self.settings_instance = settings.settings_ui(self, self.libary_layout, self.settings_layout_top, self.settings_layout_botton)
        self.make_button, self.replace_button = self.settings_instance.return_widgets()

    
    def init_controllibary(self):
        settings_label = QLabel("Control Libary:")
        settings_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        settings_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 20px;
            }
        """)
        self.libary_layout.addWidget(settings_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        container_widget = QWidget()

        # Ensure the container widget expands horizontally
        container_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.scroll_area_layout = QGridLayout(container_widget)
        self.scroll_area_layout.setSpacing(5)

        # Remove margins and align to top left
        self.scroll_area_layout.setContentsMargins(8, 8, 0, 0)
        self.scroll_area_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.scroll_area.setWidget(container_widget)
        self.scroll_area.setWidgetResizable(True)
        # self.scroll_area.setContentsMargins(5,5,5,5)
        self.libary_layout.addWidget(self.scroll_area)
            
        self.control_libary_instance = control_libary.libary_ui(self, self.scroll_area_layout, self.libary_layout)
    
    def connections(self):
        QObject.connect(self.trash_button, SIGNAL("clicked()"), lambda: remove.remove_ctrl(button=self.control_libary_instance.return_selected(), layout=self.scroll_area_layout))
        QObject.connect(self.add_button, SIGNAL("clicked()"), lambda: partial(add.add_control(), self.control_libary_instance.refresh_libary()))
        QObject.connect(self.make_button, SIGNAL("clicked()"), lambda: make_control.make(button=self.control_libary_instance.return_selected(), sidebar_instance=self.sidebar_instance, settings_instance=self.settings_instance, make=True))
        QObject.connect(self.replace_button, SIGNAL("clicked()"), lambda: make_control.make(button=self.control_libary_instance.return_selected(), sidebar_instance=self.sidebar_instance, settings_instance=self.settings_instance, make=False))

    def set_style(self):
        stylesheet_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"user_interface","style","style.css")
        with open(stylesheet_path,"r") as file:
            stylesheet = file.read()
        self.setStyleSheet(stylesheet)

    def check_existing_uis(self, UI_NAME=None):
        if cmds.window(UI_NAME, exists=True):
            cmds.deleteUI(UI_NAME, window=True)


def start_interface():
    ui = Interface()
    ui.show()
    return ui
