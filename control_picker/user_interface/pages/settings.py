from control_picker.utils import qtpyside
PySide, wrapInstance = qtpyside.get_version()

from PySide.QtCore import Qt, QObject, SIGNAL
from PySide.QtWidgets import (QWidget,
                              QHBoxLayout,
                              QVBoxLayout,
                              QPushButton,
                              QLabel,
                              QButtonGroup,
                              QLineEdit,
                              QSizePolicy,
                              QComboBox)

class settings_ui(QWidget):
    def __init__(self, interface_class, libary_layout, layout):
        super().__init__()
        
        self.interface_class = interface_class
        self.libary_layout = libary_layout
        self.layout = layout

        self.ctrl_name()
        self.ctrl_axis()
        self.ctrl_side()

    def ctrl_name(self):
        ctrl_label = QLabel("NAME:")
        ctrl_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 10px;
            }
        """)

        ctrl_name = QLineEdit("ctrl_name")
        ctrl_name.setObjectName("ctrl_name")
        ctrl_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # ctrl_name.setContentMargins(0,5,5,0)

        self.layout.addWidget(ctrl_label)
        self.layout.addWidget(ctrl_name)

    def ctrl_axis(self):
        rotation_orders = ['xyz','yzx','zxy','xzy','yxz','zyx']
        axis_label = QLabel("NAME:")
        axis_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 10px;
            }
        """)
        
        axis_combobox = QComboBox()
        axis_combobox.setObjectName("axis_combobo")
        axis_combobox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        axis_combobox.addItems(rotation_orders)
        axis_combobox.setFixedWidth(50)

        self.layout.addWidget(axis_label)
        self.layout.addWidget(axis_combobox)

    def ctrl_side(self):
        rig_side = ['L','C','R']
        side_label = QLabel("SIDE:")
        side_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 10px;
            }
        """)
        self.layout.addWidget(side_label)

        self.horizontal = QHBoxLayout()
        self.horizontal.setSpacing(3)

        self.button_group = QButtonGroup(self.interface_class)
        self.button_group.setExclusive(True)
        
        for x in rig_side:
            side_button = QPushButton(x)
            side_button.setObjectName(f"button_side_{x}")
            side_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            side_button.setFixedWidth(25)
            side_button.setCheckable(True)
            side_button.setStyleSheet("""
                                      QPushButton {
                                          font-weight: bold;
                                          }
                                      """)
            
            self.button_group.addButton(side_button)
            self.horizontal.addWidget(side_button)

            if x == "C":
                side_button.setChecked(True)

        self.layout.addLayout(self.horizontal)
