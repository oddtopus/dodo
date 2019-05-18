# Copyright (C) 2018 oddtopus (www.github.com/oddtopus/dodo)
# Following code is derived from
# PieMenu widget for FreeCAD
#
# Copyright (C) 2016, 2017 triplus @ FreeCAD
# Copyright (C) 2015,2016 looo @ FreeCAD
# Copyright (C) 2015 microelly <microelly2@freecadbuch.de>

import math
import platform
import FreeCAD, FreeCADGui
from PySide import QtCore
from PySide import QtGui

# definition of style
styleButton = ("""
    QToolButton {
        background-color: lightGray;
        border: 1px outset silver;
    }

    QToolButton:disabled {
        background-color: darkGray;
    }

    QToolButton:hover {
        background-color: lightBlue;
    }

    QToolButton:checked {
        background-color: lightGreen;
    }

    QToolButton::menu-indicator {
        subcontrol-origin: padding;
        subcontrol-position: center center;
    }

    """)
styleMenuClose = ("""
    QToolButton {
        background-color: rgba(60,60,60,235);
        border: 1px solid #1e1e1e;
    }

    QToolButton::menu-indicator {
        subcontrol-origin: padding;
        subcontrol-position: center center;
    }

    """)
styleContainer = ("QMenu{background: transparent}")
# styleCombo = ("""
    # QComboBox {
        # background: transparent;
        # border: 1px solid transparent;
    # }

    # """)
# styleQuickMenu = ("padding: 5px")
iconClose = QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_DialogCloseButton)
def radiusSize(buttonSize):
    radius = str(buttonSize / 2)
    return "QToolButton {border-radius: " + radius + "px}"
def iconSize(buttonSize):
    icon = buttonSize# / 3 * 2
    return icon

# definition of widgets 
def closeButton(buttonSize=50):
    icon = iconSize(buttonSize)
    radius = radiusSize(buttonSize)
    button = QtGui.QToolButton()
    button.setProperty("ButtonX", 0)
    button.setProperty("ButtonY", 0)
    button.setGeometry(0, 0, buttonSize, buttonSize)
    button.setIconSize(QtCore.QSize(icon, icon))
    button.setIcon(iconClose)
    button.setStyleSheet(styleMenuClose + radius)
    button.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    def onButton():
        PieMenuInstance.hide()
    button.clicked.connect(onButton)
    return button

# main classes
class HoverButton(QtGui.QToolButton):
    def __init__(self, parent=None):
        super(HoverButton, self).__init__()
    def enterEvent(self, event):
        paramGet = FreeCAD.ParamGet("User parameter:BaseApp/PieMenu")
        mode = paramGet.GetString("TriggerMode")
        if self.defaultAction().isEnabled() and mode == "Hover":
            PieMenuInstance.hide()
            self.defaultAction().trigger()
        else:
            pass
    def mouseReleaseEvent(self, event):
        paramGet = FreeCAD.ParamGet("User parameter:BaseApp/PieMenu")
        mode = paramGet.GetString("TriggerMode")
        if self.defaultAction().isEnabled():
            PieMenuInstance.hide()
            self.defaultAction().trigger()
        else:
            pass

class PieMenu:
    def __init__(self):
        self.radius = 100
        self.buttons = []
        self.buttonSize = 32
        self.menu = QtGui.QMenu(mw)
        self.menuSize = 0
        self.menu.setStyleSheet(styleContainer)
        self.menu.setWindowFlags(self.menu.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.menu.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        if compositingManager:
            pass
        else:
            self.menu.setAttribute(QtCore.Qt.WA_PaintOnScreen)
    def add_commands(self, commands):
        paramGet = FreeCAD.ParamGet("User parameter:BaseApp/PieMenu")
        for i in self.buttons:
            i.deleteLater()
        self.buttons = []
        if len(commands) == 0:
            commandNumber = 1
        else:
            commandNumber = len(commands)
        valueRadius = 100
        valueButton = 50
        self.radius = valueRadius
        self.buttonSize = valueButton
        if commandNumber == 1:
            angle = 0
            buttonSize = self.buttonSize
        else:
            angle = 2 * math.pi / commandNumber
            buttonRadius = math.sin(angle / 2) * self.radius
            buttonSize = math.trunc(2 * buttonRadius / math.sqrt(2))
        angleStart = 3 * math.pi / 2 - angle
        if buttonSize > self.buttonSize:
            buttonSize = self.buttonSize
        else:
            pass
        radius = radiusSize(buttonSize)
        icon = iconSize(buttonSize)
        if windowShadow:
            pass
        else:
            self.menuSize = valueRadius * 2 + buttonSize + 4
            if self.menuSize < 90:
                self.menuSize = 90
            else:
                pass
            self.menu.setMinimumWidth(self.menuSize)
            self.menu.setMinimumHeight(self.menuSize)
        num = 1
        for i in commands:
            button = HoverButton()
            button.setParent(self.menu)
            button.setAttribute(QtCore.Qt.WA_Hover)
            button.setStyleSheet(styleButton + radius)
            button.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            button.setDefaultAction(commands[commands.index(i)])
            button.setGeometry(0, 0, buttonSize, buttonSize)
            button.setIconSize(QtCore.QSize(icon, icon))
            button.setProperty("ButtonX", self.radius *
                               (math.cos(angle * num + angleStart)))
            button.setProperty("ButtonY", self.radius *
                               (math.sin(angle * num + angleStart)))
            self.buttons.append(button)
            num = num + 1
        buttonClose = closeButton()
        buttonClose.setParent(self.menu)
        self.buttons.append(buttonClose)
        if compositingManager:
            pass
        else:
            for i in self.buttons:
                i.setAttribute(QtCore.Qt.WA_PaintOnScreen)
    def hide(self):
        for i in self.buttons:
            i.hide()
        self.menu.hide()
    def showAtMouse(self):
        actionDict=dict([(a.objectName(),a) for a in FreeCADGui.getMainWindow().findChildren(QtGui.QAction)])
        try: actions.pop('')
        except:pass
        commands=[actionDict[n] for n in toolList if n in actionDict]
        self.add_commands(commands)
        if self.menu.isVisible():
            self.hide()
        else:
            if windowShadow:
                pos = mw.mapFromGlobal(QtGui.QCursor.pos())
                self.menu.popup(QtCore.QPoint(mw.pos()))
                self.menu.setGeometry(mw.geometry())
                for i in self.buttons:
                    i.move(i.property("ButtonX") + pos.x() - i.width() / 2,
                           i.property("ButtonY") + pos.y() - i.height() / 2)
                    i.setVisible(True)
                for i in self.buttons:
                    i.repaint()
            else:
                pos = QtGui.QCursor.pos()
                for i in self.buttons:
                    i.move(i.property("ButtonX") + (self.menuSize - i.size().width()) / 2,
                           i.property("ButtonY") + (self.menuSize - i.size().height()) / 2)
                    i.setVisible(True)
                self.menu.popup(QtCore.QPoint(pos.x() - self.menuSize / 2, pos.y() - self.menuSize / 2))

# main
mw = FreeCADGui.getMainWindow()
toolList=["insertPipe","insertElbow","insertReduct","insertCap","insertValve","insertFlange","insertUbolt"]
compositingManager = True
if QtCore.qVersion() < "5":
    windowShadow = False
else:
    windowShadow = True
if platform.system() == "Linux":
    try:
        if QtGui.QX11Info.isCompositingManagerRunning():
            windowShadow = True
        else:
            compositingManager = False
    except AttributeError:
        windowShadow = True
if platform.system() == "Windows":
    windowShadow = True
PieMenuInstance = PieMenu()
FreeCAD.__dodoPMact__ = QtGui.QAction(mw)
FreeCAD.__dodoPMact__.setObjectName("PieTest")
FreeCAD.__dodoPMact__.setShortcut(QtGui.QKeySequence("Z"))
FreeCAD.__dodoPMact__.triggered.connect(PieMenuInstance.showAtMouse)
mw.addAction(FreeCAD.__dodoPMact__)

