import FreeCAD
import FreeCADGui
import os
from . import cut_list_ui
from . import cut_list_creation
from . import RESOURCE_PATH


class cutListCommand:
    toolbarName = 'Cut List'
    commandName = 'Create Cut List'

    def GetResources(self):
        Icon = os.path.join(RESOURCE_PATH, "cut_list_icon.svg")
        return {'MenuText': self.commandName,
                'ToolTip': "Create a new Cut List from Dodo Beams",
                'Pixmap': Icon
                }

    def Activated(self):

        cut_list_ui.openCutListDialog()

    def IsActive(self):
        """If there is no active document we can't do anything."""
        return not FreeCAD.ActiveDocument is None



FreeCADGui.addCommand(cutListCommand.commandName, cutListCommand())
