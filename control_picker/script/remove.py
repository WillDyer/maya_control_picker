import maya.cmds as cmds
import os

from control_picker.utils import qtpyside
PySide, wrapInstance = qtpyside.get_version()

from PySide.QtCore import Qt, QObject, SIGNAL, QSize
from PySide.QtGui import QIcon
from PySide.QtWidgets import (QWidget,
                              QHBoxLayout,
                              QVBoxLayout,
                              QPushButton,
                              QLabel,
                              QSizePolicy,
                              QColorDialog)

class remove_ctrl():
    def __init__(self, button=None, layout=None):
        self.layout = layout
        self.remove_button(button)

    def return_qobject(self, button):
        name = button.objectName()
        button_name = name.replace("button_","")
        button_name = button_name.lower()
        return button_name

    def remove_button(self, button):
        result = cmds.confirmDialog(
                title="Confirm Removal",
                message="Do you really want to remove this control?",
                button=["Yes","No"],
                defaultButton="Yes",
                cancelButton="No",
                dismissString="No"
                )
        if button:
            if result == "Yes":
                self.delete_file(button)
            else:
                cmds.warning("Cancelled choice")

    def delete_file(self, button):
        file = self.return_qobject(button)
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","libary",f"{file}.abc")
        print(file_path)

        if os.path.exists(file_path):
            os.remove(file_path)
            print("file removed")
            button.deleteLater()
        else:
            cmds.warning("No file found")
