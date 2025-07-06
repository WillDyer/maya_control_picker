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

        self.add_buttons()

    def add_buttons(self):
        maximum_row = 4
        row_index = -1
        column_index = 0

        self.button_group = QButtonGroup(self.interface_class)
        self.button_group.setExclusive(True)

        for x in range(25):
            row_index += 1

            button = QPushButton(f"{x}")
            button.setCheckable(True)
            button.setFixedSize(100,100)
            button.setObjectName(f"button_{x}")

            self.button_group.addButton(button)
            
            if row_index == maximum_row:
                row_index = 0
                column_index += 1

            print(f"row_index: {row_index}, column_index: {column_index}")
            self.scroll_area_layout.addWidget(button,column_index, row_index)
