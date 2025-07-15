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
        self.ctrl_match()

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

        self.ctrl_name = QLineEdit("ctrl_name")
        self.ctrl_name.setObjectName("ctrl_name")
        self.ctrl_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # ctrl_name.setContentMargins(0,5,5,0)

        self.layout_top.addWidget(ctrl_label)
        self.layout_top.addWidget(self.ctrl_name)

    def ctrl_axis(self):
        rotation_orders = ['xyz','yzx','zxy','xzy','yxz','zyx']
        axis_label = QLabel("AXIS:")
        axis_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 10px;
            }
        """)
        
        self.axis_combobox = QComboBox()
        self.axis_combobox.setObjectName("axis_combobo")
        self.axis_combobox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.axis_combobox.addItems(rotation_orders)
        self.axis_combobox.setFixedWidth(50)

        self.layout_top.addWidget(axis_label)
        self.layout_top.addWidget(self.axis_combobox)

    def ctrl_match(self):
        match_label = QLabel("MATCH:")
        match_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 10px;
            }
        """)
        self.match_checkbox = QCheckBox()
        self.match_checkbox.setChecked(True)

        layout_hoz = QHBoxLayout()
        layout_hoz.addWidget(match_label)
        layout_hoz.addWidget(self.match_checkbox)
        layout_hoz.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.layout_top.addLayout(layout_hoz)

    def build_on_heirachy(self):
        heirachy_label = QLabel("CHAIN:")
        heirachy_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 10px;
            }
        """)
        self.chain_checkbox = QCheckBox()

        layout_hoz = QHBoxLayout()
        layout_hoz.addWidget(heirachy_label)
        layout_hoz.addWidget(self.chain_checkbox)
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
        self.constrain_checkbox = QCheckBox()

        layout_hoz = QHBoxLayout()
        layout_hoz.addWidget(constrain_label)
        layout_hoz.addWidget(self.constrain_checkbox)
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
        self.layout_bottom.addWidget(self.make_button)


    def return_widgets(self):
        return self.make_button, self.replace_button
