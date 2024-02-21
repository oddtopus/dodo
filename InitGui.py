#****************************************************************************
#*                                                                          *
#*   Dodo Workbench:                                                        *
#*       substitute of flamingo for Py3 / Qt5                               *
#*   Copyright (c) 2019 Riccardo Treu LGPL                                  *
#*                                                                          *
#*   This program is free software; you can redistribute it and/or modify   *
#*   it under the terms of the GNU Lesser General Public License (LGPL)     *
#*   as published by the Free Software Foundation; either version 2 of      *
#*   the License, or (at your option) any later version.                    *
#*   for detail see the LICENCE text file.                                  *
#*                                                                          *
#*   This program is distributed in the hope that it will be useful,        *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of         *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          *
#*   GNU Library General Public License for more details.                   *
#*                                                                          *
#*   You should have received a copy of the GNU Library General Public      *
#*   License along with this program; if not, write to the Free Software    *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307   *
#*   USA                                                                    *
#*                                                                          *
#****************************************************************************

class dodo ( Workbench ):
  try:
      import DraftSnap
  except Exception:
      import draftguitools.gui_snapper as DraftSnap
      print('flag') # patch
  if not hasattr(FreeCADGui, "Snapper"):
      FreeCADGui.Snapper = DraftSnap.Snapper()
      print('flag2') # patch

  import sys, FreeCAD
  v=sys.version_info[0]
  if v<3: FreeCAD.Console.PrintWarning('Dodo is written for Py3 and Qt5\n You may experience mis-behaviuors\n')
  Icon = '''
/* XPM */
static char * dodo1_xpm[] = {
"98 98 2 1",
" 	c None",
".	c #000000",
"                                                                                                  ",
"                                                                                                  ",
"                                                                                                  ",
"                                                                                                  ",
"                                                                                                  ",
"                                                                                                  ",
"                                                                                                  ",
"                                                                  ....                            ",
"                                                               ........                           ",
"                                                             ...........                          ",
"                                                           .............                          ",
"                                                          ...............                         ",
"                                                         .................                        ",
"                                                        .....................                     ",
"                                                       .........................                  ",
"                                                       .............................              ",
"                                                      ................................            ",
"                                                      ................................            ",
"                                                      .................................           ",
"                                                      ..................................          ",
"                                                      ..................................          ",
"                                                      ..................................          ",
"                                                      ..................................          ",
"                                                      ..................................          ",
"                                                       .................................          ",
"                                                       ..........         ..............          ",
"                 ......                                 .........           ........              ",
"            ............                                ..........           ......               ",
"          ................                              ..........                                ",
"         .................                               ..........                               ",
"         .................          .......               ..........                              ",
"        ..................     .................          ...........                             ",
"        ..................   .....................         ...........                            ",
"        ...........................................        ............                           ",
"        .............................................       .............                         ",
"        ..............................................       .............                        ",
"       ................................................      ..............                       ",
"       .................................................     ...............                      ",
"      .................................................... .................                      ",
"      .......................................................................                     ",
"       ......................................................................                     ",
"          ....................................................................                    ",
"              ................................................................                    ",
"               ...............................................................                    ",
"               ................................................................                   ",
"               ................................................................                   ",
"              ................................................................                    ",
"              ................................................................                    ",
"             .................................................................                    ",
"            ..................................................................                    ",
"            .................................................................                     ",
"           ..................................................................                     ",
"           ..................................................................                     ",
"          ..................................................................                      ",
"         ...................................................................                      ",
"         ...................................................................                      ",
"         ...................................................................                      ",
"           ................................................................                       ",
"            ...............................................................                       ",
"            ..............................................................                        ",
"             .............................................................                        ",
"              ............................................................                        ",
"               ..........................................................                         ",
"                .........................................................                         ",
"                 .......................................................                          ",
"                 ......................................................                           ",
"                   ...................................................                            ",
"                    ..................................................                            ",
"                     ...............................................                              ",
"                      .............................................                               ",
"                        ..........................................                                ",
"                         ........................................                                 ",
"                           ....................................                                   ",
"                            ................................                                      ",
"                             ............................                                         ",
"                             .........................                                            ",
"                              ....................                                                ",
"                              ....   ............                                                 ",
"                              ...            ...      ..                                          ",
"                              ...            ...    ....                                          ",
"                              ...            ................                                     ",
"                              ...       .... .................                                    ",
"                              ...        ..................                                       ",
"                              ...      ..   ........                                              ",
"                              ...    ....      .....                                              ",
"                        ....  ..........         .......                                          ",
"                          ...................        ....                                         ",
"                           ..................           .                                         ",
"                               .... .......                                                       ",
"                                ......                                                            ",
"                                 ......                                                           ",
"                                    .....                                                         ",
"                                       ..                                                         ",
"                                                                                                  ",
"                                                                                                  ",
"                                                                                                  ",
"                                                                                                  ",
"                                                                                                  "};
'''
  MenuText = "Dodo WB"
  ToolTip = "Dodo workbench \n(substitute of flamingo for Py3/Qt5)"
  def Initialize(self):
    import CUtils
    self.utilsList=["selectSolids","queryModel","moveWorkPlane","offsetWorkPlane","rotateWorkPlane","hackedL","moveHandle","dpCalc"]
    self.appendToolbar("Utils",self.utilsList)
    Log ('Loading Utils: done\n')
    
    import CFrame
    from cut_list.cut_list_commands import cutListCommand      
 
    self.frameList=["frameIt",
                    "FrameBranchManager",
                    "insertSection",
                    "spinSect",
                    "reverseBeam",
                    "shiftBeam",
                    "pivotBeam",
                    "levelBeam",
                    "alignEdge",
                    "rotJoin",
                    "alignFlange",
                    "stretchBeam",
                    "extend",
                    "adjustFrameAngle",
                    "insertPath",
                    "Create Cut List"]
    
    self.appendToolbar("frameTools",self.frameList)
    
    Log ('Loading Frame tools: done\n')
    import CPipe
    self.pypeList=["insertPipe","insertElbow","insertReduct","insertCap","insertValve","insertFlange","insertUbolt","insertPypeLine","insertBranch","insertTank","insertRoute","breakPipe","mateEdges","flat","extend2intersection","extend1intersection","makeHeader","laydown","raiseup","attach2tube","point2point","insertAnyz"]#,"joinPype"]
    from dodoPM import toolList
    self.qm=toolList # ["pipeQM","elbowQM","reductQM"]
    self.appendToolbar("pipeTools",self.pypeList)
    Log ('Loading Pipe tools: done\n')
    self.appendMenu(["Frame tools"],self.frameList)
    self.appendMenu(["Pype tools"],self.pypeList)    
    self.appendMenu(["Utils"],self.utilsList)
    self.appendMenu(["QkMenus"], self.qm)

  def ContextMenu(self, recipient):
    self.appendContextMenu('Frames', self.frameList)
    self.appendContextMenu('Pypes', self.pypeList)
    self.appendContextMenu('Utils', self.utilsList)

  def Activated(self):
    # if hasattr(FreeCADGui,"draftToolBar"):	#patch
      # FreeCADGui.draftToolBar.Activated()		#patch
    # if hasattr(FreeCADGui,"Snapper"):			#patch
      # FreeCADGui.Snapper.show()				#patchm
    FreeCAD.__activePypeLine__=None
    FreeCAD.__activeFrameLine__=None
    Msg("Created variables in FreeCAD module:\n")
    Msg("__activePypeLine__\n")
    Msg("__activeFrameLine__\n")
    try:
      import dodoPM
      Msg("__dodoPMact__ \n")
      FreeCAD.Console.PrintMessage(FreeCAD.__dodoPMact__.objectName()+' \'s shortcut = '+FreeCAD.__dodoPMact__.shortcuts()[0].toString()+'\n\t****\n')
    except:
      FreeCAD.Console.PrintError('dodoPM not loaded \n')

  def Deactivated(self):
    del FreeCAD.__activePypeLine__
    Msg("__activePypeLine__ variable deleted\n")
    del FreeCAD.__activeFrameLine__
    Msg("__activeFrameLine__ variable deleted\n")
    # mw=FreeCADGui.getMainWindow()
    # mw.removeAction(FreeCAD.__dodoPMact__)
    # Msg("dodoPM shortcut removed\n")
    # del FreeCAD.__dodoPMact__
    # Msg("__dodoPMact__ variable deleted\n")
    # Msg("dodo deactivated()\n")
 
Gui.addWorkbench(dodo)
