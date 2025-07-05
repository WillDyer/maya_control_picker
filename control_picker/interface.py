import maya.cmds as cmds
from maya import OpenMayaUI as omui
import importlib
import os.path

from control_picker.utils import qtpyside
PySide, wrapInstance = qtpyside.get_version()

from PySide.QtCore import Qt
from Pyside.QtGui import QIcon
from PySide.QtWidgets import (QWidget,
                              QVBoxLayout,
                              QHBoxLayout,
                              QPushButton,
                              QScrollArea,
                              QLabel,
                              QSizePolicy,
                              QLineEdit)

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
        self.setFixedWidth(600)
        self.setFixedHeight(700)
        self.setWindowTitle(UI_NAME)
        self.setObjectName(UI_NAME)

    def initUI(self):
        # Main Layout
        self.main_layout_widget = QWidget()

    def check_existing_uis(self, UI_NAME=None):
        if cmds.window(UI_NAME, exists=True):
            cmds.deleteUI(UI_NAME, window=True)


def start_interface():
    ui = Interface()
    ui.show()
    return ui
