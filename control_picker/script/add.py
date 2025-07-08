import maya.cmds as cmds
import maya.mel as mel
import os


class add_control():
    def __init__(self):
        self.load_dependencies()
        self.get_file_name()

    def load_dependencies(self):
        for plugin in ("AbcExport","AbcImport"):
            if not cmds.pluginInfo(plugin, query=True, loaded=True):
                cmds.loadPlugin(plugin)

    def export_alembic(self, file_name=None):
        if file_name:
            filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","libary",f"{file_name}.abc")
        else:
            return

        sel = cmds.ls(selection=True, long=True)
        if not sel:
            cmds.warning("No selection found")
            return

        current_frame = cmds.currentTime(query=True)

        orig_positions = {o: cmds.xform(o, q=True, t=True, ws=True) for o in sel}

        for o in sel:
            cmds.xform(o, ws=True, t=[0,0,0])

        roots = " ".join(f"-root {o}" for o in sel)
        job_str = f"-framerange {current_frame} {current_frame} -uvWrite -worldSpace {roots} -file \"{filepath}\""
        cmds.AbcExport(j=job_str)
        print(f"Exported to: {filepath}")

        for o, pos in orig_positions.items():
            cmds.xform(o, ws=True, t=pos)

    def get_file_name(self):
        result = cmds.promptDialog(
        title="ctrl_name",
        message="Name:",
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel',
        text='',
        backgroundColor=[0.1647,0.1804,0.1961])

        if result == 'OK':
            ctrl_name = cmds.promptDialog(query=True, text=True)
            ctrl_name.replace(" ","_")
            
            self.export_alembic(file_name=ctrl_name)


