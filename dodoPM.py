# Following code is derived from
# PieMenu widget for FreeCAD
#
# Copyright (C) 2016, 2017 triplus @ FreeCAD
# Copyright (C) 2015,2016 looo @ FreeCAD
# Copyright (C) 2015 microelly <microelly2@freecadbuch.de>

import math
import operator
import platform
import FreeCAD, FreeCADGui
from PySide import QtCore
from PySide import QtGui
# sign = {
    # "<": operator.lt,
    # "<=": operator.le,
    # "==": operator.eq,
    # "!=": operator.ne,
    # ">": operator.gt,
    # ">=": operator.ge,
    # }

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
styleCombo = ("""
    QComboBox {
        background: transparent;
        border: 1px solid transparent;
    }

    """)
styleQuickMenu = ("padding: 5px")
iconClose = QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_DialogCloseButton)
def radiusSize(buttonSize):
    radius = str(buttonSize / 2)
    return "QToolButton {border-radius: " + radius + "px}"
def iconSize(buttonSize):
    icon = buttonSize / 3 * 2
    return icon

# definition of widgets (commented those used in unused dialogs)
def closeButton(buttonSize=32):
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

def getActionList():
    actions = {}
    duplicates = []
    for i in mw.findChildren(QtGui.QAction):
        if i.objectName() is not None:
            if i.objectName() != "" and i.icon():
                if i.objectName() in actions:
                    if i.objectName() not in duplicates:
                        duplicates.append(i.objectName())
                    else:
                        pass
                else:
                    actions[i.objectName()] = i
            else:
                pass
        else:
            pass
    for d in duplicates:
        del actions[d]
    return actions

def updateCommands():
    toolList=["insertPipe","insertElbow","insertReduct","insertCap","insertValve","insertFlange","insertUbolt"]
    commands = []
    actionList = getActionList()
    for i in toolList:
        if i in actionList:
            commands.append(actionList[i])
        else:
            pass
    PieMenuInstance.add_commands(commands, False)

def getGroup(mode=0):
    paramGet = FreeCAD.ParamGet("User parameter:BaseApp/PieMenu")
    paramIndexGet = FreeCAD.ParamGet("User parameter:BaseApp/PieMenu/Index")
    indexList = paramIndexGet.GetString("IndexList")
    if mode == 2:
        try:
            text = paramGet.GetString("ContextPie").decode("UTF-8")
        except AttributeError:
            text = paramGet.GetString("ContextPie")
    elif mode == 1:
        try:
            text = paramGet.GetString("CurrentPie").decode("UTF-8")
        except AttributeError:
            text = paramGet.GetString("CurrentPie")
    else:
        text = cBox.currentText()
    if indexList:
        indexList = indexList.split(".,.")
        temp = []
        for i in indexList:
            temp.append(int(i))
        indexList = temp
    else:
        indexList = []
    group = None
    for i in indexList:
        a = str(i)
        try:
            pie = paramIndexGet.GetString(a).decode("UTF-8")
        except AttributeError:
            pie = paramIndexGet.GetString(a)
        if pie == text:
            group = paramIndexGet.GetGroup(a)
        else:
            pass
    if group:
        pass
    else:
        if 0 in indexList:
            group = paramIndexGet.GetGroup("0")
        else:
            setDefaultPie()
            updateCommands()
            group = paramIndexGet.GetGroup("0")
    return group

def setDefaultPie():
    paramGet = FreeCAD.ParamGet("User parameter:BaseApp/PieMenu")
    paramIndexGet = FreeCAD.ParamGet("User parameter:BaseApp/PieMenu/Index")
    indexList = paramIndexGet.GetString("IndexList")
    defaultTools = ["Std_ViewTop",
                    "Std_New",
                    "Std_ViewRight",
                    "Std_BoxSelection",
                    "Std_ViewBottom",
                    "Std_ViewAxo",
                    "Std_ViewLeft",
                    "Std_ViewScreenShot"]
    if indexList:
        indexList = indexList.split(".,.")
        temp = []
        for i in indexList:
            temp.append(int(i))
        indexList = temp
    else:
        indexList = []
    if 0 in indexList:
        pass
    else:
        indexList.append(0)
        temp = []
        for i in indexList:
            temp.append(str(i))
        indexList = temp
        paramIndexGet.SetString("0", "Default")
        paramIndexGet.SetString("IndexList", ".,.".join(indexList))
        group = paramIndexGet.GetGroup("0")
        group.SetString("ToolList", ".,.".join(defaultTools))
    paramGet.SetBool("ToolBar", False)
    paramGet.SetString("CurrentPie", "Default")
    group = getGroup(mode=1)
    group.SetInt("Radius", 100)
    group.SetInt("Button", 32)

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
    def add_commands(self, commands, context=False):
        paramGet = FreeCAD.ParamGet("User parameter:BaseApp/PieMenu")
        for i in self.buttons:
            i.deleteLater()
        self.buttons = []
        if context:
            group = getGroup(mode=2)
        else:
            group = getGroup(mode=1)
        if len(commands) == 0:
            commandNumber = 1
        else:
            commandNumber = len(commands)
        valueRadius = group.GetInt("Radius")
        valueButton = group.GetInt("Button")
        if paramGet.GetBool("ToolBar"):
            valueRadius = 100
            valueButton = 32
        if valueRadius:
            self.radius = valueRadius
        else:
            self.radius = 100
        if valueButton:
            self.buttonSize = valueButton
        else:
            self.buttonSize = 32
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
        updateCommands()
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
FreeCAD.__dodoPMact__.setShortcut(QtGui.QKeySequence("Ctrl+Q"))
FreeCAD.__dodoPMact__.triggered.connect(PieMenuInstance.showAtMouse)
mw.addAction(FreeCAD.__dodoPMact__)

