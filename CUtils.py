#(c) 2019 R. T. LGPL: part of dodo w.b. for FreeCAD

__license__="LGPL 3"

# import FreeCAD modules
import FreeCAD, FreeCADGui,inspect , os

# helper -------------------------------------------------------------------
# FreeCAD TemplatePyMod module  
# (c) 2007 Juergen Riegel LGPL

def addCommand(name,cmdObject):
	(list,num) = inspect.getsourcelines(cmdObject.Activated)
	pos = 0
	# check for indentation
	while(list[1][pos] == ' ' or list[1][pos] == '\t'):
		pos += 1
	source = ""
	for i in range(len(list)-1):
		source += list[i+1][pos:]
	FreeCADGui.addCommand(name,cmdObject,source)

#---------------------------------------------------------------------------
# The command classes
#---------------------------------------------------------------------------

class queryModel:

  def Activated(self):
    import FreeCAD, FreeCADGui, uForms
    form = uForms.QueryForm(FreeCADGui.Selection)

  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","query.svg"),'Accel':"Q,M",'MenuText':'query the model','ToolTip':'Click objects to print infos'}
    
class moveWorkPlane:
  '''
  Tool to set the DraftWorkingPlane according existing geometry of 
  the model.
  The normal of plane is set:
  * 1st according the selected face,
  * then according the plane defined by a curved edge,
  * at last according the plane defined by two straight edges.
  The origin is set:
  * 1st according the selected vertex,
  * then according the center of curvature of a curved edge,
  * at last according the intersection of two straight edges.
  '''
  def Activated(self):
    import uCmd
    uCmd.setWP()

  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","grid.svg"),'Accel':"A,W",'MenuText':'align Workplane','ToolTip':'Moves and rotates the drafting workplane with points, edges and faces'}
    
class rotateWorkPlane:

  def Activated(self):
    import FreeCAD, FreeCADGui, uForms
    form = uForms.rotWPForm()

  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","rotWP.svg"),'Accel':"R,W",'MenuText':'rotate Workplane','ToolTip':'Spin the Draft working plane about one of its axes'}
    
class offsetWorkPlane:

  def Activated(self):
    if hasattr(FreeCAD,'DraftWorkingPlane') and hasattr(FreeCADGui,'Snapper'):
      import uCmd
      s=FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft").GetInt("gridSize")
      sc=[float(x*s) for x in [1,1,.2]]
      arrow =uCmd.arrow(FreeCAD.DraftWorkingPlane.getPlacement(),scale=sc,offset=s)
      from PySide.QtGui import QInputDialog as qid
      offset=qid.getInt(None,'Offset Work Plane','Offset: ')
      if offset[1]>0:
        uCmd.offsetWP(offset[0])
      #FreeCADGui.ActiveDocument.ActiveView.getSceneGraph().removeChild(arrow.node)
      arrow.closeArrow()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","offsetWP.svg"),'Accel':"O,W",'MenuText':'offset Workplane','ToolTip':'Shifts the WP alongg its normal.'}
    
class hackedL:

  def Activated(self):
    import uCmd
    form = uCmd.hackedLine()

  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","hackedL.svg"),'Accel':"H,L",'MenuText':'draw a DWire','ToolTip':'WP is re-positioned at each point. Possible to spin and offset it.'}
    
class moveHandle:

  def Activated(self):
    import uCmd
    FreeCADGui.Control.showDialog(uCmd.handleDialog())
    #form = uCmd.handleDialog()

  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","moveHandle.svg"),'Accel':"M,H",'MenuText':'Move objects','ToolTip':'Move quickly objects inside viewport'}
    
class dpCalc:

  def Activated(self):
    import uForms
    FreeCADGui.Control.showDialog(uForms.dpCalcDialog())

  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","delta.svg"),'MenuText':'Pressure loss calculator','ToolTip':'Calculate pressure loss in "pypes" using ChEDL libraries.\n See __doc__ of the module for further information.'}

class selectSolids:

  def Activated(self):
    from fCmd import getSolids
    if FreeCADGui.Selection.getSelection(): allDoc=False
    else: allDoc=True
    getSolids(allDoc)

  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","solids.svg"),'MenuText':'Select solids','ToolTip':'Grab all solids or those partially selected\n to export in .step format'}

#---------------------------------------------------------------------------
# Adds the commands to the FreeCAD command manager
#---------------------------------------------------------------------------
addCommand('queryModel',queryModel()) 
addCommand('moveWorkPlane',moveWorkPlane()) 
addCommand('rotateWorkPlane',rotateWorkPlane())
addCommand('offsetWorkPlane',offsetWorkPlane())
addCommand('hackedL',hackedL())
addCommand('moveHandle',moveHandle())
addCommand('dpCalc',dpCalc())
addCommand('selectSolids',selectSolids())
