#(c) 2019 R. T. LGPL: part of dodo w.b. for FreeCAD

__license__="LGPL 3"

import FreeCAD,FreeCADGui
import fCmd, dodoDialogs
from PySide.QtCore import *
from PySide.QtGui import *
from os.path import join, dirname, abspath
from sys import platform

class fillForm(dodoDialogs.protoTypeDialog):
  'dialog for fillFrame()'
  def __init__(self):
    super(fillForm,self).__init__('fillframe.ui')
    self.beam=None
    self.form.btn1.clicked.connect(self.selectAction)
  def accept(self):
    if self.beam!=None and len(fCmd.edges())>0:
      FreeCAD.activeDocument().openTransaction('Fill frame')
      if self.form.radio1.isChecked():
        fCmd.placeTheBeam(self.beam,frameCmd.edges()[0])
      else:
        for edge in fCmd.edges():
          struct=FreeCAD.activeDocument().copyObject(self.beam,True)
          fCmd.placeTheBeam(struct,edge)
        FreeCAD.activeDocument().recompute()
      FreeCAD.ActiveDocument.recompute()
      FreeCAD.activeDocument().commitTransaction()
  def selectAction(self):
    if len(fCmd.beams())>0:
      self.beam=fCmd.beams()[0]
      self.form.label.setText(self.beam.Label+':'+self.beam.Profile)
      FreeCADGui.Selection.removeSelection(self.beam)

class extendForm(dodoDialogs.protoTypeDialog):
  'dialog for fCmd.extendTheBeam()'
  def __init__(self):
    super(extendForm,self).__init__('extend.ui')
    selex = FreeCADGui.Selection.getSelectionEx()
    self.form.btn1.clicked.connect(self.selectAction)
    if len(selex):
      self.target=selex[0].SubObjects[0]
      self.form.label.setText(selex[0].Object.Label+':'+self.target.ShapeType)
      FreeCADGui.Selection.removeSelection(selex[0].Object)
    else:
      self.target=None
  def selectAction(self):
    selex = FreeCADGui.Selection.getSelectionEx()
    if len(selex[0].SubObjects)>0 and hasattr(selex[0].SubObjects[0],'ShapeType'):
      self.target=selex[0].SubObjects[0]
      self.form.label.setText(selex[0].Object.Label+':'+self.target.ShapeType)
      FreeCADGui.Selection.clearSelection()
  def accept(self):            # extend
    if self.target!=None and len(fCmd.beams())>0:
      FreeCAD.activeDocument().openTransaction('Extend beam')
      for beam in fCmd.beams():
        fCmd.extendTheBeam(beam,self.target)
      FreeCAD.activeDocument().recompute()
      FreeCAD.activeDocument().commitTransaction()
      
class stretchForm(dodoDialogs.protoTypeDialog):
  '''dialog for stretchTheBeam()
    [Get Length] measures the min. distance of the selected objects or
      the length of the selected edge or
      the Height of the selected beam
    [ Stretch ] changes the Height of the selected beams
  '''
  def __init__(self):
    self.L=None
    super(stretchForm,self).__init__('beamstretch.ui')
    self.form.edit1.setValidator(QDoubleValidator())
    self.form.edit1.editingFinished.connect(self.edit12L)
    self.form.btn1.clicked.connect(self.selectAction)
    self.form.slider.setMinimum(-100)
    self.form.slider.setMaximum(100)
    self.form.slider.setValue(0)
    self.form.slider.valueChanged.connect(self.changeL)
    self.labTail=None
  def edit12L(self):
    if self.form.edit1.text():
      self.L=float(self.form.edit1.text())
      self.form.slider.setValue(0)
  def changeL(self):
    if self.L:
      ext=self.L*(1+self.form.slider.value()/100.0)
      self.form.edit1.setText("%.3f" %ext)
  def selectAction(self):
    if self.labTail:
      self.labTail.removeLabel()
      self.labTail=None
    self.L=fCmd.getDistance()
    if self.L:
      self.form.edit1.setText("%.3f"%self.L)
    elif fCmd.beams():
      beam=fCmd.beams()[0]
      self.L=float(beam.Height)
      self.form.edit1.setText("%.3f"%self.L)
    else:
      self.form.edit1.setText('') 
    self.form.slider.setValue(0)
    self.writeTail()
  def writeTail(self):
    if fCmd.beams():
      beam=fCmd.beams()[0]
      from uCmd import label3D
      self.labTail=label3D(pl=beam.Placement, text='____TAIL')
  def accept(self):
    if self.labTail:
      self.labTail.removeLabel()
      self.labTail=None
    self.L=fCmd.getDistance()
    if self.form.edit1.text():
      length=float(self.form.edit1.text())
      FreeCAD.activeDocument().openTransaction('Stretch beam')
      for beam in fCmd.beams():
        delta=float(beam.Height)-length
        fCmd.stretchTheBeam(beam,length)
        if self.form.tail.isChecked():
          disp=fCmd.beamAx(beam).multiply(delta)
          beam.Placement.move(disp)
        elif self.form.both.isChecked():
          disp=fCmd.beamAx(beam).multiply(delta/2.0)
          beam.Placement.move(disp)
      FreeCAD.activeDocument().recompute()
      FreeCAD.activeDocument().commitTransaction()
  def reject(self): # redefined to remove label from the scene
    if self.labTail:
      self.labTail.removeLabel()
    super(stretchForm,self).reject()

class translateForm(dodoDialogs.protoTypeDialog):   
  'dialog for moving blocks'
  def __init__(self):
    super(translateForm,self).__init__("beamshift.ui")
    for e in [self.form.edit1,self.form.edit2,self.form.edit3,self.form.edit4,self.form.edit5]:
      e.setValidator(QDoubleValidator())
    self.form.btn1.clicked.connect(self.selectAction)
    self.arrow=None
  def getDistance(self):
    self.deleteArrow()
    roundDigits=3
    shapes=[y for x in FreeCADGui.Selection.getSelectionEx() for y in x.SubObjects if hasattr(y,'ShapeType')][:2]
    if len(shapes)>1:    # if at least 2 shapes selected....
      base,target=shapes[:2]
      disp=None
      if base.ShapeType==target.ShapeType=='Vertex':
        disp=target.Point-base.Point
      elif base.ShapeType==target.ShapeType=='Edge':
        if base.curvatureAt(0):
          P1=base.centerOfCurvatureAt(0)
        else:
          P1=base.CenterOfMass
        if target.curvatureAt(0):
          P2=target.centerOfCurvatureAt(0)
        else:
          P2=target.CenterOfMass
        disp=P2-P1
      elif set([base.ShapeType,target.ShapeType])=={'Vertex','Edge'}:
        P=list()
        i=0
        for o in [base,target]:
          if o.ShapeType=='Vertex':
            P.append(o.Point)
          elif o.curvatureAt(0):
            P.append(o.centerOfCurvatureAt(0))
          else:
            return
          i+=1
        disp=P[1]-P[0]
      elif base.ShapeType=='Vertex' and target.ShapeType=='Face':
        disp=fCmd.intersectionPlane(base.Point,target.normalAt(0,0),target)-base.Point
      elif base.ShapeType=='Face' and target.ShapeType=='Vertex':
        disp=target.Point-fCmd.intersectionPlane(target.Point,base.normalAt(0,0),base)
        disp=P[1]-P[0]
      if disp!=None:
        self.form.edit4.setText(str(disp.Length))
        self.form.edit5.setText('1')
        disp.normalize()
        dx,dy,dz=list(disp)
        self.form.edit1.setText(str(round(dx,roundDigits)))
        self.form.edit2.setText(str(round(dy,roundDigits)))
        self.form.edit3.setText(str(round(dz,roundDigits)))
        FreeCADGui.Selection.clearSelection()
  def getLength(self):
    roundDigits=3
    if len(fCmd.edges())>0:
      edge=fCmd.edges()[0]
      self.form.edit4.setText(str(edge.Length))
      self.form.edit5.setText('1')
      dx,dy,dz=list(edge.tangentAt(0))
      self.form.edit1.setText(str(round(dx,roundDigits)))
      self.form.edit2.setText(str(round(dy,roundDigits)))
      self.form.edit3.setText(str(round(dz,roundDigits)))
      FreeCADGui.Selection.clearSelection()
      self.deleteArrow()
      from uCmd import arrow
      where=FreeCAD.Placement()
      where.Base=edge.valueAt(0)
      where.Rotation=FreeCAD.Rotation(FreeCAD.Vector(0,0,1),edge.tangentAt(0))
      size=[edge.Length/20.0,edge.Length/10.0,edge.Length/20.0]
      self.arrow=arrow(pl=where,scale=size,offset=edge.Length/2.0)
  def selectAction(self):
    shapes=[y for x in FreeCADGui.Selection.getSelectionEx() for y in x.SubObjects if hasattr(y,'ShapeType')][:2]
    if len(shapes)>1:
      self.getDistance()
    elif len(fCmd.edges())>0:
      self.getLength()
  def accept(self):           # translate
    self.deleteArrow()
    scale=float(self.form.edit4.text())/float(self.form.edit5.text())
    disp=FreeCAD.Vector(float(self.form.edit1.text())*self.form.cbX.isChecked(),float(self.form.edit2.text())*self.form.cbY.isChecked(),float(self.form.edit3.text())*self.form.cbZ.isChecked()).scale(scale,scale,scale)
    FreeCAD.activeDocument().openTransaction('Translate')    
    if self.form.radio2.isChecked():
      for o in set(FreeCADGui.Selection.getSelection()):
        FreeCAD.activeDocument().copyObject(o,True)
    for o in set(FreeCADGui.Selection.getSelection()):
      o.Placement.move(disp)
    FreeCAD.activeDocument().recompute()
    FreeCAD.activeDocument().commitTransaction()    
  def deleteArrow(self):
    if self.arrow: self.arrow.closeArrow() #FreeCADGui.ActiveDocument.ActiveView.getSceneGraph().removeChild(self.arrow.node)
    self.arrow=None
  def reject(self): # redefined to remove arrow from scene
    self.deleteArrow()
    super(translateForm,self).reject()

class alignForm(dodoDialogs.protoTypeDialog):   
  'dialog to flush faces'
  def __init__(self):
    super(alignForm,self).__init__('align.ui')
    self.faceRef=None
    self.selectAction()
    self.form.btn1.clicked.connect(self.selectAction)
    self.form.btnXY.clicked.connect(lambda: self.refPlane(FreeCAD.Vector(0,0,1)))
    self.form.btnXZ.clicked.connect(lambda: self.refPlane(FreeCAD.Vector(0,1,0)))
    self.form.btnYZ.clicked.connect(lambda: self.refPlane(FreeCAD.Vector(1,0,0)))
    self.form.X.setValidator(QDoubleValidator())
    self.form.btnNorm.clicked.connect(lambda: self.refPlane(FreeCAD.Vector(float(self.form.X.text()),float(self.form.Y.text()),float(self.form.Z.text()))))
    self.form.Y.setValidator(QDoubleValidator())
    self.form.Z.setValidator(QDoubleValidator())
  def selectAction(self):
    if fCmd.faces():
      a=[(o,fCmd.faces([o])[0]) for o in FreeCADGui.Selection.getSelectionEx() if frameCmd.faces([o])][0]
      self.faceRef=a[1]
      self.form.label.setText(a[0].Object.Label+':Face')
      FreeCADGui.Selection.clearSelection()
  def refPlane(self,norm):
    self.faceRef=norm
    if norm==FreeCAD.Vector(0,0,1):
      self.form.label.setText('plane XY')
    elif norm==FreeCAD.Vector(0,1,0):
      self.form.label.setText('plane XZ')
    elif norm==FreeCAD.Vector(1,0,0):
      self.form.label.setText('plane YZ')
    else:
      self.form.label.setText('normal: X=%.2f Y=%.2f Z=%.2f' %(norm.x,norm.y,norm.z))
    for edit in [self.form.X, self.form.Y, self.form.Z]:
      edit.clear()
  def accept(self):
    faces=fCmd.faces()
    objs=FreeCADGui.Selection.getSelection() #beams=fCmd.beams()
    if len(faces)==len(objs)>0 and self.faceRef:
      FreeCAD.activeDocument().openTransaction('AlignFlange')
      for i in range(len(objs)):
        fCmd.rotTheBeam(objs[i],self.faceRef,faces[i])
      FreeCAD.activeDocument().recompute()
      FreeCAD.activeDocument().commitTransaction()
    
class rotateAroundForm(dodoDialogs.protoTypeDialog):
  '''
  Dialog for rotateTheBeamAround().
  It allows to rotate one object around one edge or the axis of a circular edge (or one principal axis.)
  '''
  def __init__(self):
    super(rotateAroundForm,self).__init__('rotAround.ui')
    self.form.edit1.setValidator(QDoubleValidator())
    self.form.btn1.clicked.connect(self.selectAction)
    self.form.btn2.clicked.connect(self.reverse)
    self.form.btnX.clicked.connect(lambda: self.getPrincipalAx('X'))
    self.form.btnY.clicked.connect(lambda: self.getPrincipalAx('Y'))
    self.form.btnZ.clicked.connect(lambda: self.getPrincipalAx('Z'))
    self.form.dial.valueChanged.connect(lambda: self.form.edit1.setText(str(self.form.dial.value())))
    self.form.edit1.editingFinished.connect(lambda: self.form.dial.setValue(int(self.form.edit1.text())))
    self.Axis=None
    self.arrow=None
    self.selectAction()
  def accept(self, ang=None):
    if not ang:
      ang=float(self.form.edit1.text())
    self.deleteArrow()
    objects=FreeCADGui.Selection.getSelection()
    if objects and self.Axis:
      FreeCAD.ActiveDocument.openTransaction('rotateTheBeamAround')
      for o in objects:
        if self.form.copyCB.isChecked():
          FreeCAD.activeDocument().copyObject(o,True)
        fCmd.rotateTheBeamAround(o,self.Axis,ang)
      FreeCAD.ActiveDocument.commitTransaction()
  def reverse(self):
    ang=float(self.form.edit1.text())*-1
    self.form.edit1.setText('%.0f'%ang)
    self.form.dial.setValue(int(self.form.edit1.text()))
    self.accept(ang*2)
  def getPrincipalAx(self, ax='Z'):
    self.deleteArrow()
    from Part import Edge,Line
    O=FreeCAD.Vector()
    l=Line(O,FreeCAD.Vector(0,0,1000))
    if ax=='X':
      l=Line(O,FreeCAD.Vector(1000,0,0))
    elif ax=='Y':
      l=Line(O,FreeCAD.Vector(0,1000,0))
    self.Axis=Edge(l)
    self.form.lab1.setText("Principal: "+ax)
  def selectAction(self):
    edged = [objex for objex in FreeCADGui.Selection.getSelectionEx() if fCmd.edges([objex])]
    if edged:
      self.Axis=fCmd.edges([edged[0]])[0]
      self.deleteArrow()
      from uCmd import arrow
      where=FreeCAD.Placement()
      where.Base=self.Axis.valueAt(self.Axis.LastParameter)
      where.Rotation=FreeCAD.Rotation(FreeCAD.Vector(0,0,1),self.Axis.tangentAt(self.Axis.LastParameter))
      size=[self.Axis.Length/20.0,self.Axis.Length/10.0,self.Axis.Length/20.0]
      self.arrow=arrow(pl=where,scale=size,offset=self.Axis.Length/10.0)
      if self.Axis.curvatureAt(0):
        O=self.Axis.centerOfCurvatureAt(0)
        n=self.Axis.tangentAt(0).cross(self.Axis.normalAt(0))
        from Part import Edge, Line
        self.Axis=(Edge(Line(FreeCAD.Vector(O),FreeCAD.Vector(O+n))))
      self.form.lab1.setText(edged[0].Object.Label+": edge")
  def deleteArrow(self):
    if self.arrow: self.arrow.closeArrow()
    self.arrow=None
  def reject(self): # redefined to remove arrow from scene
    self.deleteArrow()
    super(rotateAroundForm,self).reject()
