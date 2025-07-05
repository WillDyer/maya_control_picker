from importlib import reload
import sys
import os

dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dir_path)

import control_picker.interface as interface
reload(interface)
from control_picker.interface import start_interface
