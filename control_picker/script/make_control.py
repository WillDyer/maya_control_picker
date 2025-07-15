import maya.cmds as cmds
import os
from importlib import reload

from control_picker.utils import OPM
reload(OPM)

class make():
    def __init__(self, button, sidebar_instance, settings_instance, make):
        self.sidebar_instance = sidebar_instance
        self.settings_instance = settings_instance

        self.load_dependencies()
        button_name = self.return_qobject(button)

        if button_name:
            if make:
                if self.settings_instance.chain_checkbox.isChecked():
                    control_list = self.chain(file_name=button_name)
                else:
                    control_list = self.import_ctrl(file_name=button_name)
                    if self.settings_instance.match_checkbox.isChecked():
                        self.match(control=control_list)
                    if self.settings_instance.constrain_checkbox.isChecked():
                        self.constrain(joint=cmds.ls(sl=True)[0], control=control_list)
            else:
                self.init_change(button_name)

    def load_dependencies(self):
        for plugin in ("AbcExport","AbcImport"):
            if not cmds.pluginInfo(plugin, query=True, loaded=True):
                cmds.loadPlugin(plugin)
    
    def return_qobject(self, button):
        if button:
            name = button.objectName()
            button_name = name.replace("button_","")
            button_name = button_name.lower()
            return button_name
        else:
            cmds.warning("No selection made")
            return None

    def import_ctrl(self, file_name=None):
        if file_name:
            filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","libary",f"{file_name}.abc")
        else:
            cmds.warning("Failed to get file path for libary.")
            return
        
        scene_before = set(cmds.ls(long=True))

        cmds.AbcImport(filepath, mode="import")
        
        scene_after = set(cmds.ls(long=True))
        control = list(scene_after - scene_before)
        control = [obj for obj in control if "Shape" not in obj]
        
        for item in control:
            self.set_colour(item)
            self.axis(item)
            
            # self.set_name(item) # update name last
        return control

    def set_colour(self, item):
        rgb_colour = self.sidebar_instance.return_colour()

        cmds.setAttr(f"{item}.overrideEnabled", True)
        cmds.setAttr(f"{item}.overrideRGBColors", True)
            
        colour = [c / 255.0 for c in rgb_colour]
        cmds.setAttr(f"{item}.overrideColorR", colour[0])
        cmds.setAttr(f"{item}.overrideColorG", colour[1])
        cmds.setAttr(f"{item}.overrideColorB", colour[2])

    def set_name(self, item):
        cmds.rename(item, self.settings_instance.ctrl_name.text())
    
    def axis(self, item):
        cmds.setAttr(f"{item}.rotateOrder", self.settings_instance.axis_combobox.currentIndex())

    def match(self, control):
        for item in control:
            if cmds.ls(sl=True):
                cmds.matchTransform(item, cmds.ls(sl=True)[0])
                OPM.offsetParentMatrix(ctrl=item)
            else:
                cmds.warning("Skipping match transform no selection found")

    def chain(self, file_name):
        last_item = None
        controls = []
        joint_chain = cmds.listRelatives(cmds.ls(sl=True)[0], ad=True, type="joint") + cmds.ls(sl=True)
        joint_chain.reverse()
        for i, joint in enumerate(joint_chain):
            control_list = []
            control = self.import_ctrl(file_name=file_name)
            
            for item in control:
                cmds.matchTransform(item, joint)
                if i >= 1:
                    item = cmds.parent(item, last_item, a=True)[0]
                    control_list.append(item)
                    controls.append(control_list)
                last_item = item
                OPM.offsetParentMatrix(ctrl=item)

            if self.settings_instance.constrain_checkbox.isChecked():
                self.constrain(joint=joint, control=control_list)

        return controls

    def constrain(self, joint, control):
        for item in control:
            cmds.parentConstraint(control, joint, mo=True, name=f"pConst_{control}")

    def init_change(self, button_name):
        def change_control(selected):
            for item in selected:
                target = cmds.listRelatives(item, shapes=True, fullPath=True)
                control_list = self.import_ctrl(file_name=button_name)
                if target:
                    old_shapes = target + control_list
                    for control in control_list:
                        shape = cmds.listRelatives(control, shapes=True, fullPath=True)
                        cmds.parent(shape, item, shape=True, relative=True)
                    cmds.delete(old_shapes)
                else:
                    cmds.warning("No target shape found to replace")

        selected = cmds.ls(sl=True)
        for control in selected:
            if self.settings_instance.chain_checkbox.isChecked():
                chain = cmds.listRelatives(control, ad=True, type="transform") + [control]
                chain.reverse()
                print(chain)
                change_control(selected=chain)
            else:
                change_control(selected=[control])

