#(c) 2019 R. T. LGPL: part of dodo w.b. for FreeCAD

__title__="pypeTools toolbar"
__author__="oddtopus"
__url__="github.com/oddtopus/dodo"
__license__="LGPL 3"

# import FreeCAD modules
import FreeCAD, FreeCADGui,inspect, os
from PySide.QtCore import QT_TRANSLATE_NOOP
from DraftGui import translate
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
  #print(name+":\n"+str(source))

def updatesPL(dialogqm):
  if FreeCAD.activeDocument():
    pypelines=[o.Label for o in FreeCAD.activeDocument().Objects if hasattr(o,'PType') and o.PType=='PypeLine']
  else:
    pypelines=[]
  if pypelines: # updates pypelines in combo
    dialogqm.QM.comboPL.clear()
    dialogqm.QM.comboPL.addItems(pypelines)

#---------------------------------------------------------------------------
# The command classes
#---------------------------------------------------------------------------

class insertPipe:
  def Activated (self):
    import pForms
    pipForm=pForms.insertPipeForm()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "iconz","pipe.svg"),
    'MenuText':QT_TRANSLATE_NOOP('insertPipe','Insert a tube'),
    'ToolTip':QT_TRANSLATE_NOOP('insertPipe','Insert a tube')}

class insertElbow:
  def Activated (self):
    import pForms,FreeCAD
    elbForm=pForms.insertElbowForm()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "iconz","elbow.svg"),
    'MenuText':QT_TRANSLATE_NOOP('insertElbow','Insert a curve'),
    'ToolTip':QT_TRANSLATE_NOOP('insertElbow','Insert a curve')}

class insertReduct:
  def Activated (self):
    import pForms
    pipeFormObj=pForms.insertReductForm()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "iconz","reduct.svg"),
    'MenuText':QT_TRANSLATE_NOOP('insertReduct','Insert a reduction'),
    'ToolTip':QT_TRANSLATE_NOOP('insertReduct','Insert a reduction')}

class insertCap:
  def Activated (self):
    import pForms
    pipeFormObj=pForms.insertCapForm()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "iconz","cap.svg"),
    'MenuText':QT_TRANSLATE_NOOP('insertCap','Insert a cap'),
    'ToolTip':QT_TRANSLATE_NOOP('insertCap','Insert a cap')}

class insertFlange:
  def Activated (self):
    import pForms
    pipeFormObj=pForms.insertFlangeForm()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "iconz","flange.svg"),
    'MenuText':QT_TRANSLATE_NOOP('insertFlange','Insert a flange'),
    'ToolTip':QT_TRANSLATE_NOOP('insertFlange','Insert a flange')}

class insertUbolt:
  def Activated (self):
    import pForms
    pipeFormObj=pForms.insertUboltForm()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "iconz","clamp.svg"),
    'MenuText':QT_TRANSLATE_NOOP('insertUbolt','Insert a U-bolt'),
    'ToolTip':QT_TRANSLATE_NOOP('insertUbolt','Insert a U-bolt')}

class insertPypeLine:
  def Activated (self):
    import pForms
    pipeFormObj=pForms.insertPypeLineForm()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "iconz","pypeline.svg"),
    'MenuText':QT_TRANSLATE_NOOP('insertPypeLine','PypeLine Manager'),
    'ToolTip':QT_TRANSLATE_NOOP('insertPypeLine','Open PypeLine Manager')}

class insertBranch:
  def Activated (self):
    import pForms
    #pCmd.makeBranch()
    pipeFormObj=pForms.insertBranchForm()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "iconz","branch.svg"),
    'MenuText':QT_TRANSLATE_NOOP('insertBranch','Insert a branch'),
    'ToolTip':QT_TRANSLATE_NOOP('insertBranch','Insert a PypeBranch')}

class breakPipe:
  def Activated (self):
    import pForms
    pipeFormObj=pForms.breakForm()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "iconz","break.svg"),
    'MenuText':QT_TRANSLATE_NOOP('breakPipe','Break the pipe'),
    'ToolTip':QT_TRANSLATE_NOOP('breakPipe','Break one pipe at point and insert gap')}

class mateEdges:
  def Activated (self):
    import pCmd
    FreeCAD.activeDocument().openTransaction('Mate')
    pCmd.alignTheTube()
    FreeCAD.activeDocument().commitTransaction()
    FreeCAD.activeDocument().recompute()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "iconz","mate.svg"),
    'Accel':"M,E",
    'MenuText':QT_TRANSLATE_NOOP('mateEdges','Mate pipes edges'),
    'ToolTip':QT_TRANSLATE_NOOP('mateEdges','Mate two terminations through their edges')}

class flat:
  def Activated (self):
    import pCmd
    pCmd.flatten()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "iconz","flat.svg"),
    'MenuText':QT_TRANSLATE_NOOP('flat','Fit one elbow'),
    'ToolTip':QT_TRANSLATE_NOOP('flat','Place the elbow between two pipes or beams')}

class extend2intersection:
  def Activated (self):
    import pCmd
    FreeCAD.activeDocument().openTransaction('Xtend2int')
    pCmd.extendTheTubes2intersection()
    FreeCAD.activeDocument().recompute()
    FreeCAD.activeDocument().commitTransaction()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "iconz","intersect.svg"),
    'MenuText':QT_TRANSLATE_NOOP('extend2intersection','Extends pipes to intersection'),
    'ToolTip':QT_TRANSLATE_NOOP('extend2intersection','Extends pipes to intersection')}

class extend1intersection:
  def Activated (self):
    import pCmd
    FreeCAD.activeDocument().openTransaction('Xtend1int')
    pCmd.extendTheTubes2intersection(both=False)
    FreeCAD.activeDocument().recompute()
    FreeCAD.activeDocument().commitTransaction()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "iconz","intersect1.svg"),
    'MenuText':QT_TRANSLATE_NOOP('extend1intersection','Extends pipe to intersection'),
    'ToolTip':QT_TRANSLATE_NOOP('extend1intersection','Extends pipe to intersection')}

class laydown:
  def Activated (self):
    import pCmd, fCmd
    from Part import Plane
    refFace=[f for f in fCmd.faces() if type(f.Surface)==Plane][0]
    FreeCAD.activeDocument().openTransaction('Lay-down the pipe')
    for b in fCmd.beams():
      if pCmd.isPipe(b):
        pCmd.laydownTheTube(b,refFace)
    FreeCAD.activeDocument().recompute()
    FreeCAD.activeDocument().commitTransaction()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "iconz","laydown.svg"),
    'MenuText':QT_TRANSLATE_NOOP('laydown','Lay-down the pipe'),
    'ToolTip':QT_TRANSLATE_NOOP('laydown','Lay-down the pipe on the support plane')}

class raiseup:
  def Activated (self):
    import pCmd, fCmd
    from Part import Plane
    selex=FreeCADGui.Selection.getSelectionEx()
    for sx in selex:
      sxFaces=[f for f in fCmd.faces([sx]) if type(f.Surface)==Plane]
      if len(sxFaces)>0:
        refFace=sxFaces[0]
        support=sx.Object
    FreeCAD.activeDocument().openTransaction('Raise-up the support')
    for b in fCmd.beams():
      if pCmd.isPipe(b):
        pCmd.laydownTheTube(b,refFace,support)
        break
    FreeCAD.activeDocument().recompute()
    FreeCAD.activeDocument().commitTransaction()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "iconz","raiseup.svg"),
    'MenuText':QT_TRANSLATE_NOOP('raiseup','Raise-up the support'),
    'ToolTip':QT_TRANSLATE_NOOP('raiseup','Raise the support to the pipe')}

class joinPype:
  '''

  '''
  def Activated(self):
    import FreeCAD, FreeCADGui, pForms #pObservers
    # s=pObservers.joinObserver()
    FreeCADGui.Control.showDialog(pForms.joinForm()) #.Selection.addObserver(s)

  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "iconz","join.svg"),
    'MenuText':QT_TRANSLATE_NOOP('joinPype','Join pypes'),
    'ToolTip':QT_TRANSLATE_NOOP('joinPype','Select the part-pype and the port')}

class insertValve:
  def Activated (self):
    import pForms
    #pipeFormObj=pForms.insertValveForm()
    #FreeCADGui.Control.showDialog(pForms.insertValveForm())
    pipeFormObj=pForms.insertValveForm()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "iconz","valve.svg"),
    'MenuText':QT_TRANSLATE_NOOP('insertValve','Insert a valve'),
    'ToolTip':QT_TRANSLATE_NOOP('insertValve','Insert a valve')}

class attach2tube:
  def Activated (self):
    import pCmd
    FreeCAD.activeDocument().openTransaction('Attach to tube')
    pCmd.attachToTube()
    FreeCAD.activeDocument().recompute()
    FreeCAD.activeDocument().commitTransaction()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "iconz","attach.svg"),
    'MenuText':QT_TRANSLATE_NOOP('attach2tube','Attach  to tube'),
    'ToolTip':QT_TRANSLATE_NOOP('attach2tube','Attach one pype to the nearest port of selected pipe')}

class point2point:

  def Activated(self):
    import pForms
    form = pForms.point2pointPipe()

  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "iconz","point2point.svg"),
    'MenuText':QT_TRANSLATE_NOOP('point2point','draw a tube point-to-point'),
    'ToolTip':QT_TRANSLATE_NOOP('point2point','Click on subsequent points.')}

class insertAnyz:
  '''
  Dialog to insert any object saved as .STEP, .IGES or .BREP in folder ../Mod/dodo/shapez or subfolders.
  '''
  def Activated(self):
    import anyShapez
    FreeCADGui.Control.showDialog(anyShapez.shapezDialog())

  def GetResources(self):
    return{'MenuText':QT_TRANSLATE_NOOP('insertAnyz','Insert any shape'),
    'ToolTip':QT_TRANSLATE_NOOP('insertAnyz','Insert a STEP, IGES or BREP')}

class insertTank:
  def Activated(self):
    import FreeCADGui, pForms
    FreeCADGui.Control.showDialog(pForms.insertTankForm())

  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "iconz","tank.svg"),
    'MenuText':QT_TRANSLATE_NOOP('insertTank','Insert a tank'),
    'ToolTip':QT_TRANSLATE_NOOP('insertTank','Create tank and nozzles')}

class insertRoute:
  def Activated(self):
    import FreeCADGui, pForms
    FreeCADGui.Control.showDialog(pForms.insertRouteForm())

  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "iconz","route.svg"),
    'MenuText':QT_TRANSLATE_NOOP('insertRoute','Insert a pipe route'),
    'ToolTip':QT_TRANSLATE_NOOP('insertRoute','Create a sketch attached to a circular edge')}

class makeHeader:
  def Activated (self):
    import pCmd
    FreeCAD.activeDocument().openTransaction('Connect to header')
    pCmd.header()
    FreeCAD.activeDocument().recompute()
    FreeCAD.activeDocument().commitTransaction()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "iconz","header.svg"),
    'MenuText':QT_TRANSLATE_NOOP('makeHeader', 'Connect to header'),
    'ToolTip':QT_TRANSLATE_NOOP('makeHeader', 'Connect branches to one header pipe\nBranches and header\'s axes must be ortho')}

#---------------------------------------------------------------------------
# Adds the commands to the FreeCAD command manager
#---------------------------------------------------------------------------
addCommand('insertPipe',insertPipe())
addCommand('insertElbow',insertElbow())
addCommand('insertReduct',insertReduct())
addCommand('insertCap',insertCap())
addCommand('insertValve',insertValve())
addCommand('insertFlange',insertFlange())
addCommand('insertUbolt',insertUbolt())
addCommand('insertPypeLine',insertPypeLine())
addCommand('insertBranch',insertBranch())
addCommand('insertTank',insertTank())
addCommand('insertRoute',insertRoute())
addCommand('breakPipe',breakPipe())
addCommand('mateEdges',mateEdges())
addCommand('joinPype',joinPype())
addCommand('attach2tube',attach2tube())
addCommand('flat',flat())
addCommand('extend2intersection',extend2intersection())
addCommand('extend1intersection',extend1intersection())
addCommand('laydown',laydown())
addCommand('raiseup',raiseup())
addCommand('point2point',point2point())
addCommand('insertAnyz',insertAnyz())
addCommand('makeHeader',makeHeader())

### QkMenus ###
class pipeQM:
  def Activated(self):
    import dodoPM
    #dodoPM.pqm.updatePL()
    dodoPM.pqm.show()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "iconz","pipe.svg"),
    'MenuText':QT_TRANSLATE_NOOP('pipeQM','QM for pipes')}
addCommand('pipeQM',pipeQM())

class elbowQM():
  def Activated (self):
    import dodoPM
    dodoPM.eqm.show()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "iconz","elbow.svg"),
    'MenuText':QT_TRANSLATE_NOOP('elbowQM','QM for elbows')}
addCommand('elbowQM',elbowQM())

class flangeQM():
  def Activated (self):
    import dodoPM
    dodoPM.fqm.show()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "iconz","flange.svg"),
    'MenuText':QT_TRANSLATE_NOOP('flangeQM','QM for flanges')}
addCommand('flangeQM',flangeQM())

class valveQM():
  def Activated (self):
    import dodoPM
    dodoPM.vqm.show()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "iconz","valve.svg"),
    'MenuText':QT_TRANSLATE_NOOP('valveQM','QM for valves')}
addCommand('valveQM',valveQM())

class capQM():
  def Activated (self):
    import dodoPM
    dodoPM.cqm.show()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "iconz","cap.svg"),
    'MenuText':QT_TRANSLATE_NOOP('capQM','QM for caps')}
addCommand('capQM',capQM())
