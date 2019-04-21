from PySide.QtCore import *
from PySide.QtGui import *
from sys import platform
from os.path import join, dirname, abspath
import FreeCAD, FreeCADGui

class prototypeDialog(QDialog): 
  'prototype for dialogs.ui with callback function'
  def __init__(self,dialog='anyFile.ui'):
    super(prototypeDialog,self).__init__()
    dialogPath=join(dirname(abspath(__file__)),"dialogz",dialog)
    FreeCAD.Console.PrintMessage(dialogPath+"\n")
    self.form=FreeCADGui.PySideUic.loadUi(dialogPath)
    FreeCAD.Console.PrintMessage(dialogPath+" loaded\n")
    ### new shortcuts procedure
    mw = FreeCADGui.getMainWindow()
    for act in mw.findChildren(QtGui.QAction):
      if act.objectName() in ["actionX", "actionS"]:
        mw.removeAction(act)
    actionKey = QAction(mw)
    actionKey.setObjectName("actionX") # define X action
    actionKey.setShortcut(QKeySequence("Alt+X"))
    actionKey.triggered.connect(self.accept)
    mw.addAction(actionKey)
    actionKey.setObjectName("actionS") # define S action
    actionKey.setShortcut(QKeySequence("Alt+S"))
    actionKey.triggered.connect(self.selectAction)
    mw.addAction(actionKey)
    FreeCAD.Console.PrintMessage('"Alt+S" to select\n"Alt+X" to execute\n')
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
    mw = FreeCADGui.getMainWindow()
    for act in mw.findChildren(QtGui.QAction):
      if act.objectName() in ["actionX", "actionS"]:
        mw.removeAction(act)
    try: self.view.removeEventCallback('SoMouseButtonEvent',self.call)
    except: pass
    FreeCADGui.Control.closeDialog()
    if FreeCAD.ActiveDocument: FreeCAD.ActiveDocument.recompute()

class protopypeForm(QDialog): #, prototypes.protoPypeForm):
  'prototype dialog for insert pFeatures'
  def __init__(self,winTitle='Title', PType='Pipe', PRating='SCH-STD', icon='flamingo.svg'):
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
    super(protopypeForm,self).__init__()
    self.initUI() #added 20190331
    #self.setupUi()
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

