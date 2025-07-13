import maya.cmds as cmds
import os


class make():
    def __init__(self, button, sidebar_instance, settings_instance):
        self.sidebar_instance = sidebar_instance
        self.settings_instance = settings_instance

        self.load_dependencies()
        self.return_qobject(button)

    def load_dependencies(self):
        for plugin in ("AbcExport","AbcImport"):
            if not cmds.pluginInfo(plugin, query=True, loaded=True):
                cmds.loadPlugin(plugin)
    
    def return_qobject(self, button):
        if button:
            name = button.objectName()
            button_name = name.replace("button_","")
            button_name = button_name.lower()
            self.import_ctrl(file_name=button_name)
        else:
            cmds.warning("No selection made")

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

        self.set_colour(control)
        self.set_name(control)

    def set_colour(self, control):
        for item in control:
            rgb_colour = self.sidebar_instance.return_colour()

            cmds.setAttr(f"{item}.overrideEnabled", True)
            cmds.setAttr(f"{item}.overrideRGBColors", True)
            
            colour = [c / 255.0 for c in rgb_colour]
            cmds.setAttr(f"{item}.overrideColorR", colour[0])
            cmds.setAttr(f"{item}.overrideColorG", colour[1])
            cmds.setAttr(f"{item}.overrideColorB", colour[2])

    def set_name(self, control):
        for item in control:
            cmds.rename()
        
