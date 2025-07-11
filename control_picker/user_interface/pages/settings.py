import importlib

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
                              QComboBox,
                              QCheckBox,
                              QSpacerItem)


class settings_ui(QWidget):
    def __init__(self, interface_class, libary_layout, layout_top, layout_bottom):
        super().__init__()
        
        self.interface_class = interface_class
        self.libary_layout = libary_layout
        self.layout_top = layout_top
        self.layout_bottom = layout_bottom

        self.ctrl_name()
        self.ctrl_axis()
        self.ctrl_side()

        self.build_on_heirachy()
        self.constrain()
        self.replace_control()
        self.make_control()

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

        self.layout_top.addWidget(ctrl_label)
        self.layout_top.addWidget(ctrl_name)

    def ctrl_axis(self):
        rotation_orders = ['xyz','yzx','zxy','xzy','yxz','zyx']
        axis_label = QLabel("AXIS:")
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

        self.layout_top.addWidget(axis_label)
        self.layout_top.addWidget(axis_combobox)

    def ctrl_side(self):
        rig_side = ['L','C','R']
        side_label = QLabel("SIDE:")
        side_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 10px;
            }
        """)
        self.layout_top.addWidget(side_label)

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

        self.layout_top.addLayout(self.horizontal)

    def build_on_heirachy(self):
        heirachy_label = QLabel("CHAIN:")
        heirachy_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 10px;
            }
        """)
        checkbox = QCheckBox()

        layout_hoz = QHBoxLayout()
        layout_hoz.addWidget(heirachy_label)
        layout_hoz.addWidget(checkbox)
        layout_hoz.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.layout_bottom.addLayout(layout_hoz)

    def constrain(self):
        constrain_label = QLabel("CONSTRAIN:")
        constrain_label.setStyleSheet("""
                                      QLabel {
                                          font-weight: bold;
                                          font-size: 10px;
                                          }
                                      """)
        checkbox = QCheckBox()

        layout_hoz = QHBoxLayout()
        layout_hoz.addWidget(constrain_label)
        layout_hoz.addWidget(checkbox)
        layout_hoz.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.layout_bottom.addLayout(layout_hoz)

    def replace_control(self):
        self.replace_button = QPushButton("Replace Control")
        self.replace_button.setStyleSheet("""
                                QPushButton {
                                    background-color: #8952e0;
                                }
                                QPushButton:hover {
                                    background-color: #9160E0;
                                }
                                QPushButton:pressed {
                                    background-color: #966ADD;
                                    }
                            """)

        self.replace_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # self.replace_button.setFixedWidth(200)

        # spacer = QSpacerItem(40,0,QSizePolicy.Expanding, QSizePolicy.Minimum)
        # self.layout_bottom.addItem(spacer)

        self.layout_bottom.addWidget(self.replace_button)

    def make_control(self):
        self.make_button = QPushButton("Make Control")
        self.make_button.setStyleSheet("""
                                QPushButton {
                                    background-color: #8952e0;
                                }
                                QPushButton:hover {
                                    background-color: #9160E0;
                                }
                                QPushButton:pressed {
                                    background-color: #966ADD;
                                    }
                            """)

        self.make_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # self.make_button.setFixedWidth(200)

        # spacer = QSpacerItem(40,0,QSizePolicy.Expanding, QSizePolicy.Minimum)
        # self.layout_bottom.addItem(spacer)

        self.layout_bottom.addWidget(self.make_button)


    def return_widgets(self):
        return self.make_button
