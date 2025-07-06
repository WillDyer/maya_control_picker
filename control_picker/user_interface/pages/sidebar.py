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

class sidebar_ui(QWidget):
    def __init__(self, interface_class, sidebar_layout):
        super().__init__()

        self.interface_class = interface_class
        self.sidebar_layout = sidebar_layout
        
        self.add_buttons()
        self.colour_button()

    def add_buttons(self):
        module_label = QLabel("SETTINGS:")
        module_label.setFixedSize(125,25)
        module_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 20px;
            }
        """)
        self.sidebar_layout.addWidget(module_label)

        button_dict = {
                "add": {"tool_tip": "Add selected control to libary"},
                "trash": {"tool_tip": "Delete selected control from Libary"}
                }

        for button_name in button_dict.keys():
            icon = QIcon(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","icons",f"{button_name}.svg"))

            button = QPushButton()
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setIcon(icon)
            button.setIconSize(QSize(64,64))
            button.setToolTip(button_dict[button_name]["tool_tip"])
            button.setObjectName(f"button_{button_name}")
            self.sidebar_layout.addWidget(button)

    def colour_button(self):
        colour_widget = QWidget()
        colour_widget.setContentsMargins(0,0,0,0)
        verticle_layout = QVBoxLayout(colour_widget)
        verticle_layout.setContentsMargins(0,5,5,0)
        verticle_layout.setSpacing(5)
        horizontal_layout = QHBoxLayout()
        horizontal_layout.setContentsMargins(0,0,0,0)
        horizontal_layout.setSpacing(2)

        module_label = QLabel("Colour:")
        module_label.setFixedSize(125,25)
        module_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 20px;
            }
        """)

        self.colour_dict = {
                "L_button": {"red": "255", "green": "0", "blue": "0"}, #[255, 0, 0],
                "C_button": {"red": "255", "green": "255", "blue": "0"}, #[255, 255, 0],
                "R_button": {"red": "0", "green": "0", "blue": "255"} # [0, 0, 255]
            }

        colour_button = QPushButton()
        colour_button.setObjectName("colour_button")
        colour_button.setStyleSheet(f"background-color: rgb({self.colour_dict['C_button']['red']},{self.colour_dict['C_button']['green']},{self.colour_dict['C_button']['blue']});")
        
        L_button = QPushButton("L")
        L_button.setObjectName("L_button")
        C_button = QPushButton("C")
        C_button.setObjectName("C_button")
        R_button = QPushButton("R")
        R_button.setObjectName("R_button")
        
        verticle_layout.addWidget(module_label)
        verticle_layout.addWidget(colour_button)
        horizontal_layout.addWidget(L_button)
        horizontal_layout.addWidget(C_button)
        horizontal_layout.addWidget(R_button)
        verticle_layout.addLayout(horizontal_layout)

        self.sidebar_layout.addWidget(colour_widget)
        
        QObject.connect(colour_button, SIGNAL("clicked()"), lambda: self.set_colour(colour_button))
        QObject.connect(L_button, SIGNAL("clicked()"), lambda: self.set_colour_preset(L_button, colour_button))
        QObject.connect(C_button, SIGNAL("clicked()"), lambda: self.set_colour_preset(C_button, colour_button))
        QObject.connect(R_button, SIGNAL("clicked()"), lambda: self.set_colour_preset(R_button, colour_button))

    def set_colour(self, button):
        colour = self.get_colour()
        if colour:
            button.setStyleSheet(f"background-color: rgb({colour['red']}, {colour['green']}, {colour['blue']});")
            colour_dict = {"red": colour['red'],
                           "green": colour['green'],
                           "blue": colour['blue']}

    def get_colour(self):
        colour = QColorDialog.getColor()
        if colour.isValid():
            red = colour.red()
            green = colour.green()
            blue = colour.blue()
            return {"red":red, "green":green, "blue":blue}
        else:
            return None

    def set_colour_preset(self, button, colour_button):
        colour_button.setStyleSheet(f"background-color: rgb({self.colour_dict[button.objectName()]['red']}, {self.colour_dict[button.objectName()]['green']}, {self.colour_dict[button.objectName()]['blue']});")

