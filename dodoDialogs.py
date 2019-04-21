from PySide.QtCore import *
from PySide.QtGui import *
from sys import platform
from os.path import join, dirname, abspath
from os import listdir
import FreeCAD, FreeCADGui, csv

class protoTypeDialog(object): 
  'prototype for dialogs.ui with callback function'
  def __init__(self,dialog='anyFile.ui'):
    dialogPath=join(dirname(abspath(__file__)),"dialogz",dialog)
    self.form=FreeCADGui.PySideUic.loadUi(dialogPath)
    ### new shortcuts procedure
    self.mw = FreeCADGui.getMainWindow()
    for act in self.mw.findChildren(QAction):
      if act.objectName() in ["actionX", "actionS"]:
        self.mw.removeAction(act)
    self.actionX = QAction(self.mw)
    self.actionX.setObjectName("actionX") # define X action
    self.actionX.setShortcut(QKeySequence("X"))
    self.actionX.triggered.connect(self.accept)
    self.mw.addAction(self.actionX)
    self.actionS = QAction(self.mw)
    self.actionS.setObjectName("actionS") # define S action
    self.actionS.setShortcut(QKeySequence("S"))
    self.actionS.triggered.connect(self.selectAction)
    self.mw.addAction(self.actionS)
    FreeCAD.Console.PrintMessage('"%s" to select; "%s" to execute\n' %(self.actionX.shortcuts()[0].toString(),self.actionS.shortcuts()[0].toString()))
    try:
      self.view=FreeCADGui.activeDocument().activeView()
      self.call=self.view.addEventCallback("SoMouseButtonEvent", self.action) # SoKeyboardEvents replaced by QAction'
    except:
      FreeCAD.Console.PrintError('No view available.\n')
  def action(self,arg):
    'Defines functions executed by the callback self.call when "SoMouseButtonEvent"'
    # SoKeyboardEvents replaced by QAction':
    CtrlAltShift=[arg['CtrlDown'],arg['AltDown'],arg['ShiftDown']]
    if arg['Button']=='BUTTON1' and arg['State']=='DOWN': self.mouseActionB1(CtrlAltShift)
    elif arg['Button']=='BUTTON2' and arg['State']=='DOWN': self.mouseActionB2(CtrlAltShift)
    elif arg['Button']=='BUTTON3' and arg['State']=='DOWN': self.mouseActionB3(CtrlAltShift)
  def selectAction(self):
    'MUST be redefined in the child class'
    print('"selectAction" performed')
    pass
  def mouseActionB1(self,CtrlAltShift):
    'MUST be redefined in the child class'
    pass
  def mouseActionB2(self,CtrlAltShift):
    'MUST be redefined in the child class'
    pass
  def mouseActionB3(self,CtrlAltShift):
    'MUST be redefined in the child class'
    pass
  def reject(self):
    'CAN be redefined to remove other attributes, such as arrow()s or label()s'
    self.mw.removeAction(self.actionX)
    self.mw.removeAction(self.actionS)
    FreeCAD.Console.PrintMessage('Actions "%s" and "%s" removed\n' %(self.actionX.objectName(),self.actionS.objectName()))
    try: self.view.removeEventCallback('SoMouseButtonEvent',self.call)
    except: pass
    FreeCADGui.Control.closeDialog()
    if FreeCAD.ActiveDocument: FreeCAD.ActiveDocument.recompute()

class protoPypeForm(QDialog): 
  'prototype dialog for insert pFeatures'
  def __init__(self,winTitle='Title', PType='Pipe', PRating='SCH-STD', icon='dodo.svg'):
    '''
    __init__(self,winTitle='Title', PType='Pipe', PRating='SCH-STD')
      winTitle: the window's title
      PType: the pipeFeature type
      PRating: the pipeFeature pressure rating class
    It lookups in the directory ./tablez the file PType+"_"+PRating+".csv",
    imports it's content in a list of dictionaries -> .pipeDictList and
    shows a summary in the QListWidget -> .sizeList
    Also create a property -> PRatingsList with the list of available PRatings for the 
    selected PType.   
    '''
    super(protoPypeForm,self).__init__()
    self.move(QPoint(100,250))
    self.PType=PType
    self.PRating=PRating
    self.setWindowFlags(Qt.WindowStaysOnTopHint)
    self.setWindowTitle(winTitle)
    iconPath=join(dirname(abspath(__file__)),"iconz",icon)
    from PySide.QtGui import QIcon
    Icon=QIcon()
    Icon.addFile(iconPath)
    self.setWindowIcon(Icon) 
    self.mainHL=QHBoxLayout()
    self.setLayout(self.mainHL)
    self.firstCol=QWidget()
    self.firstCol.setLayout(QVBoxLayout())
    self.mainHL.addWidget(self.firstCol)
    self.currentRatingLab=QLabel('Rating: '+self.PRating)
    self.firstCol.layout().addWidget(self.currentRatingLab)
    self.sizeList=QListWidget()
    self.firstCol.layout().addWidget(self.sizeList)
    self.pipeDictList=[]
    self.fileList=listdir(join(dirname(abspath(__file__)),"tablez"))
    self.fillSizes()
    self.PRatingsList=[s.lstrip(PType+"_").rstrip(".csv") for s in self.fileList if s.startswith(PType) and s.endswith('.csv')]
    self.secondCol=QWidget()
    self.secondCol.setLayout(QVBoxLayout())
    self.combo=QComboBox()
    self.combo.addItem('<none>')
    try:
      self.combo.addItems([o.Label for o in FreeCAD.activeDocument().Objects if hasattr(o,'PType') and o.PType=='PypeLine'])
    except:
      None
    self.combo.currentIndexChanged.connect(self.setCurrentPL)
    if FreeCAD.__activePypeLine__ and FreeCAD.__activePypeLine__ in [self.combo.itemText(i) for i in range(self.combo.count())]:
      self.combo.setCurrentIndex(self.combo.findText(FreeCAD.__activePypeLine__))
    self.secondCol.layout().addWidget(self.combo)
    self.ratingList=QListWidget()
    self.ratingList.addItems(self.PRatingsList)
    self.ratingList.itemClicked.connect(self.changeRating)
    self.ratingList.setCurrentRow(0)
    self.secondCol.layout().addWidget(self.ratingList)
    self.btn1=QPushButton('Insert')
    self.secondCol.layout().addWidget(self.btn1)
    self.mainHL.addWidget(self.secondCol)
    self.resize(350,350)
    self.mainHL.setContentsMargins(0,0,0,0)
  def setCurrentPL(self,PLName=None):
    if self.combo.currentText() not in ['<none>','<new>']:
      FreeCAD.__activePypeLine__= self.combo.currentText()
    else:
      FreeCAD.__activePypeLine__=None
  def fillSizes(self):
    self.sizeList.clear()
    for fileName in self.fileList:
      if fileName==self.PType+'_'+self.PRating+'.csv':
        f=open(join(dirname(abspath(__file__)),"tablez",fileName),'r')
        reader=csv.DictReader(f,delimiter=';')
        self.pipeDictList=[DNx for DNx in reader]
        f.close()
        for row in self.pipeDictList:
          s=row['PSize']
          if 'OD' in row.keys():
            s+=" - "+row['OD']
          if 'thk' in row.keys():
            s+="x"+row['thk']
          self.sizeList.addItem(s)
        break
  def changeRating(self,item):
    self.PRating=item.text()
    self.currentRatingLab.setText('Rating: '+self.PRating)
    self.fillSizes()
  def findDN(self,DN):
    result=None
    for row in self.pipeDictList:
      if row['PSize']==DN:
        result=row
        break
    return result

# Following code is derived from
# PieMenu widget for FreeCAD
#
# Copyright (C) 2016, 2017 triplus @ FreeCAD
# Copyright (C) 2015,2016 looo @ FreeCAD
# Copyright (C) 2015 microelly <microelly2@freecadbuch.de>
#
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
#
# Attribution:
# http://forum.freecadweb.org/
# http://www.freecadweb.org/wiki/index.php?title=Code_snippets


from PySide import QtCore, QtGui
from math import pi, cos, sin
import numpy as np

class PieButton(QtGui.QGraphicsEllipseItem):
    def __init__(self, pos=[0, 0], angle_range=(0, 1), size=[50, 50], view=None, parent=None):
        super(PieButton, self).__init__(None, scene=parent)
        self.view = view
        self.angle_range = angle_range
        self.setRect(pos[0] - size[0] / 2, pos[1] - size[1] / 2, size[0], size[1])
        self.setBrush(QtGui.QBrush(QtCore.Qt.blue))
        self.setAcceptHoverEvents(True)
        self.command = None
        self.hoover = False
    def setHoover(self, value):
        if not self.hoover == value:
            self.hoover = value
            if value:
                self.setBrush(QtGui.QBrush(QtCore.Qt.red))
                self.view.setText(self.command[0])
            else:
                self.setBrush(QtGui.QBrush(QtCore.Qt.blue))

class PieView(QtGui.QGraphicsView):
    def __init__(self, key, commands, parent=None):
        super(PieView, self).__init__(parent)
        self.key = key
        self.setWindowFlags(QtCore.Qt.Widget | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet("QGraphicsView {border-style: none; background: transparent;}" )
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scene = QtGui.QGraphicsScene(self)
        self.scene.setSceneRect(-200, -200, 400, 400)
        self.setScene(self.scene)
        self.center = [0, 0]
        self.buttons = []
        self.label = QtGui.QGraphicsSimpleTextItem("")
        self.scene.addItem(self.label)
        self.add_commands(commands)

    def setText(self, text):
        self.label.setText(text)
        self.label.update()
        self.label.setPos(-self.label.sceneBoundingRect().width() / 2, 0)
    def add_commands(self, commands):
        num = len(commands)
        r = 100
        a = 70
        pie_phi = np.linspace(0, np.pi * 2, num + 1)
        phi = [(p + pie_phi[i + 1]) / 2 for i, p in enumerate(pie_phi[:-1])]
        for i, command in enumerate(commands):
            button = PieButton(
                [r * cos(phi[i]), r * sin(phi[i])],
                [pie_phi[i], pie_phi[i + 1]],
                [a, a], self, self.scene)
            button.command = command
            self.scene.addItem(button)
            self.buttons.append(button)
    def mouseMoveEvent(self, event):
        r2, angle = self.polarCoordinates
        hoover = False
        for item in self.buttons:
            if (item.angle_range[0] < angle and
                angle < item.angle_range[1] and
                r2 > 1000):
                item.setHoover(True)
                hoover = True
            else:
                item.setHoover(False)
        if not hoover:
            self.setText("")
    @property
    def polarCoordinates(self):
        pos = QtGui.QCursor.pos() - self.center
        r2 = pos.x() ** 2 + pos.y() ** 2
        angle = np.arctan2(pos.y(), pos.x())
        return r2, angle + (angle < 0) * 2 * pi
    def showAtMouse(self, event):
        if event["Key"] == self.key:
            self.show()
            self.center = QtGui.QCursor.pos()
            self.move(self.center.x()-(self.width()/2), self.center.y()-(self.height()/2))
    def keyReleaseEvent(self, event):
        super(PieView, self).keyReleaseEvent(event)
        if event.key() == QtGui.QKeySequence(self.key):
            if not event.isAutoRepeat():
                for item in self.scene.items():
                    if hasattr(item, "hoover"):
                        if item.hoover:
                            item.command[1]()
                self.hide()

def startPieMenu():
  if __name__ == "__main__":
    def part_design(): FreeCADGui.activateWorkbench("PartDesignWorkbench")
    def part(): FreeCADGui.activateWorkbench("PartWorkbench")
    def draft(): FreeCADGui.activateWorkbench("DraftWorkbench")
    def arch(): FreeCADGui.activateWorkbench("ArchWorkbench")
    def fem(): FreeCADGui.activateWorkbench("FemWorkbench")
    def sketch(): FreeCADGui.activateWorkbench("SketcherWorkbench")
    def draw(): FreeCADGui.activateWorkbench("DrawingWorkbench")
    def mesh(): FreeCADGui.activateWorkbench("MeshWorkbench")
    command_list = [
        ["PartDesign", part_design],
        ["Part", part],
        ["Draft", draft],
        ["Arch", arch],
        ["Fem", fem],
        ["sketch", sketch],
        ["draw", draw],
        ["mesh", mesh]]
    a = PieView("a", command_list)
    view = FreeCADGui.ActiveDocument.ActiveView
    view.addEventCallback("SoKeyboardEvent", a.showAtMouse)

