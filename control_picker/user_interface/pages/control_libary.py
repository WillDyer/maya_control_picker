import os
import string

from control_picker.utils import qtpyside
PySide, wrapInstance = qtpyside.get_version()

from PySide.QtCore import Qt, QObject, SIGNAL
from PySide.QtWidgets import (QWidget,
                              QHBoxLayout,
                              QVBoxLayout,
                              QPushButton,
                              QLabel,
                              QButtonGroup)


class libary_ui(QWidget):
    def __init__(self, interface_class, scroll_area_layout, layout):
        super().__init__()
        
        self.interface_class = interface_class
        self.scroll_area_layout = scroll_area_layout
        self.layout = layout
        self.button = None
        self.button_group = QButtonGroup(self.interface_class)
        self.button_group.setExclusive(True)
        self.existing_buttons = set()


        self.add_buttons()

    def add_buttons(self):
        maximum_row = 4
        row_index = -1
        column_index = 0

        files = [".".join(f.split(".")[:-1]) for f in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'libary'))]
        try: files.remove("")
        except ValueError: pass
        files = [f for f in files if f not in ["__init__"]]

        for x in files:
            if x in self.existing_buttons:
                continue

            row_index += 1
            button_name = x.replace("_","")
            button_name = string.capwords(button_name)

            button = QPushButton(f"{button_name}")
            button.setCheckable(True)
            button.setFixedSize(100,100)
            button.setObjectName(f"button_{button_name}")

            self.button_group.addButton(button)
            self.existing_buttons.add(x)
            
            if row_index == maximum_row:
                row_index = 0
                column_index += 1

            print(f"row_index: {row_index}, column_index: {column_index}")
            self.scroll_area_layout.addWidget(button,column_index, row_index)
            
            QObject.connect(button, SIGNAL("clicked()"), lambda b=button: self.hold_selected(b))

    def refresh_libary(self):
        for i in reversed(range(self.scroll_area_layout.count())):
            item = self.scroll_area_layout.takeAt(i)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.existing_buttons.clear()
        self.add_buttons()

    def hold_selected(self, button):
        print(f"selected button: {button}")
        self.button = button

    def return_selected(self):
        if self.button:
            return self.button
        else:
            return None
