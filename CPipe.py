#(c) 2019 R. T. LGPL: part of dodo w.b. for FreeCAD

__title__="pypeTools toolbar"
__author__="oddtopus"
__url__="github.com/oddtopus/dodo"
__license__="LGPL 3"

# import FreeCAD modules
import FreeCAD, FreeCADGui,inspect, os

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
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","pipe.svg"),'MenuText':'Insert a tube','ToolTip':'Insert a tube'}

class insertElbow: 
  def Activated (self):
    import pForms,FreeCAD
    elbForm=pForms.insertElbowForm()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","elbow.svg"),'MenuText':'Insert a curve','ToolTip':'Insert a curve'}

class insertReduct: 
  def Activated (self):
    import pForms
    pipeFormObj=pForms.insertReductForm()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","reduct.svg"),'MenuText':'Insert a reduction','ToolTip':'Insert a reduction'}

class insertCap: 
  def Activated (self):
    import pForms
    pipeFormObj=pForms.insertCapForm()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","cap.svg"),'MenuText':'Insert a cap','ToolTip':'Insert a cap'}

class insertFlange:
  def Activated (self):
    import pForms
    pipeFormObj=pForms.insertFlangeForm()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","flange.svg"),'MenuText':'Insert a flange','ToolTip':'Insert a flange'}

class insertUbolt:
  def Activated (self):
    import pForms
    pipeFormObj=pForms.insertUboltForm()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","clamp.svg"),'MenuText':'Insert a U-bolt','ToolTip':'Insert a U-bolt'}

class insertPypeLine:
  def Activated (self):
    import pForms
    pipeFormObj=pForms.insertPypeLineForm()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","pypeline.svg"),'MenuText':'PypeLine Manager','ToolTip':'Open PypeLine Manager'}

class insertBranch:
  def Activated (self):
    import pForms
    #pCmd.makeBranch()
    pipeFormObj=pForms.insertBranchForm()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","branch.svg"),'MenuText':'Insert a branch','ToolTip':'Insert a PypeBranch'}

class breakPipe:
  def Activated (self):
    import pForms
    pipeFormObj=pForms.breakForm()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","break.svg"),'MenuText':'Break the pipe','ToolTip':'Break one pipe at point and insert gap'}

class mateEdges:
  def Activated (self):
    import pCmd
    FreeCAD.activeDocument().openTransaction('Mate')
    pCmd.alignTheTube()
    FreeCAD.activeDocument().commitTransaction()
    FreeCAD.activeDocument().recompute()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","mate.svg"),'Accel':"M,E",'MenuText':'Mate pipes edges','ToolTip':'Mate two terminations through their edges'}

class flat:  
  def Activated (self):
    import pCmd
    pCmd.flatten()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","flat.svg"),'MenuText':'Fit one elbow','ToolTip':'Place the elbow between two pipes or beams'}

class extend2intersection:
  def Activated (self):
    import pCmd
    FreeCAD.activeDocument().openTransaction('Xtend2int')
    pCmd.extendTheTubes2intersection()
    FreeCAD.activeDocument().recompute()
    FreeCAD.activeDocument().commitTransaction()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","intersect.svg"),'MenuText':'Extends pipes to intersection','ToolTip':'Extends pipes to intersection'}

class extend1intersection:
  def Activated (self):
    import pCmd
    FreeCAD.activeDocument().openTransaction('Xtend1int')
    pCmd.extendTheTubes2intersection(both=False)
    FreeCAD.activeDocument().recompute()
    FreeCAD.activeDocument().commitTransaction()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","intersect1.svg"),'MenuText':'Extends pipe to intersection','ToolTip':'Extends pipe to intersection'}

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
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","laydown.svg"),'MenuText':'Lay-down the pipe','ToolTip':'Lay-down the pipe on the support plane'}

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
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","raiseup.svg"),'MenuText':'Raise-up the support','ToolTip':'Raise the support to the pipe'}

class joinPype:
  '''
  
  '''
  def Activated(self):
    import FreeCAD, FreeCADGui, pForms #pObservers
    # s=pObservers.joinObserver()
    FreeCADGui.Control.showDialog(pForms.joinForm()) #.Selection.addObserver(s)
    
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","join.svg"),'MenuText':'Join pypes','ToolTip':'Select the part-pype and the port'} 

class insertValve:
  def Activated (self):
    import pForms
    #pipeFormObj=pForms.insertValveForm()
    #FreeCADGui.Control.showDialog(pForms.insertValveForm()) 
    pipeFormObj=pForms.insertValveForm()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","valve.svg"),'MenuText':'Insert a valve','ToolTip':'Insert a valve'}

class attach2tube:
  def Activated (self):
    import pCmd
    FreeCAD.activeDocument().openTransaction('Attach to tube')
    pCmd.attachToTube()
    FreeCAD.activeDocument().recompute()
    FreeCAD.activeDocument().commitTransaction()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","attach.svg"),'MenuText':'Attach  to tube','ToolTip':'Attach one pype to the nearest port of selected pipe'}

class point2point:

  def Activated(self):
    import pForms
    form = pForms.point2pointPipe()

  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","point2point.svg"),'MenuText':'draw a tube point-to-point','ToolTip':'Click on subsequent points.'}
    
class insertAnyz:
  '''
  Dialog to insert any object saved as .STEP, .IGES or .BREP in folder ../Mod/dodo/shapez or subfolders.
  '''
  def Activated(self):
    import anyShapez
    FreeCADGui.Control.showDialog(anyShapez.shapezDialog()) 
    
  def GetResources(self):
    return{'MenuText':'Insert any shape','ToolTip':'Insert a STEP, IGES or BREP'}

class insertTank:
  def Activated(self):
    import FreeCADGui, pForms
    FreeCADGui.Control.showDialog(pForms.insertTankForm())
    
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","tank.svg"),'MenuText':'Insert a tank','ToolTip':'Create tank and nozzles'} 

class insertRoute:
  def Activated(self):
    import FreeCADGui, pForms
    FreeCADGui.Control.showDialog(pForms.insertRouteForm())
    
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","route.svg"),'MenuText':'Insert a pipe route','ToolTip':'Create a sketch attached to a circular edge'} 

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

### QkMenus ###
class pipeQM:
  def Activated(self):
    import dodoPM
    #dodoPM.pqm.updatePL()
    dodoPM.pqm.show()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","pipe.svg"),'MenuText':'QM for pipes'} 
addCommand('pipeQM',pipeQM())

class elbowQM():
  def Activated (self):
    import dodoPM
    #dodoPM.eqm.updatePL()
    dodoPM.eqm.show()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","elbow.svg"),'MenuText':'QM for elbows'} 
addCommand('elbowQM',elbowQM())

class flangeQM():
  def Activated (self):
    import dodoPM
    #dodoPM.fqm.updatePL()
    dodoPM.fqm.show()
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"iconz","flange.svg"),'MenuText':'QM for flanges'} 
addCommand('flangeQM',flangeQM())

