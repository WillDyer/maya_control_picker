import maya.cmds as cmds
import os


class make():
    def __init__(self, button):
        print("running make")
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
        
        cmds.AbcImport(filepath, mode="import")
        
