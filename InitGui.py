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
  import DraftSnap
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
    self.frameList=["frameIt","insertSection","FrameLineManager","FrameBranchManager","spinSect","reverseBeam","shiftBeam","pivotBeam","levelBeam","alignEdge","rotJoin","alignFlange","stretchBeam","extend","adjustFrameAngle"]
    self.appendToolbar("frameTools",self.frameList)
    Log ('Loading Frame tools: done\n')
    import CPipe
    self.pypeList=["insertPipe","insertElbow","insertReduct","insertCap","insertValve","insertFlange","insertUbolt","insertPypeLine","insertBranch","insertTank","insertRoute","breakPipe","mateEdges","flat","extend2intersection","extend1intersection","laydown","raiseup","attach2tube","point2point","insertAnyz","joinPype"]
    self.appendToolbar("pipeTools",self.pypeList)
    Log ('Loading Pipe tools: done\n')
    menu1 = ["Frame tools"]
    menu2 = ["Pype tools"]
    menu3 = ["Utils"]
    self.appendMenu(menu1,self.frameList)
    self.appendMenu(menu2,self.pypeList)    
    self.appendMenu(menu3,self.utilsList)

  def ContextMenu(self, recipient):
    self.appendContextMenu('Frames', self.frameList)
    self.appendContextMenu('Pypes', self.pypeList)
    self.appendContextMenu('Utils', self.utilsList)

  def Activated(self):
    if hasattr(FreeCADGui,"draftToolBar"):
      FreeCADGui.draftToolBar.Activated()
    if hasattr(FreeCADGui,"Snapper"):
      FreeCADGui.Snapper.show()
    FreeCAD.__activePypeLine__=None
    FreeCAD.__activeFrameLine__=None
    Msg("Created variables in FreeCAD module:\n")
    Msg("__activePypeLine__\n")
    Msg("__activeFrameLine__\n")

  def Deactivated(self):
    del FreeCAD.__activePypeLine__
    del FreeCAD.__activeFrameLine__
    Msg("dodo deactivated()\n")
    Msg("Deleted variables in FreeCAD module:\n")
    Msg("__activePypeLine__\n")
    Msg("__activeFrameLine__\n")

Gui.addWorkbench(dodo)
