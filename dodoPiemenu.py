from __future__ import division
import FreeCADGui as Gui
from PySide import QtCore, QtGui
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
                [r * np.cos(phi[i]), r * np.sin(phi[i])],
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
        return r2, angle + (angle < 0) * 2 * np.pi

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


if __name__ == "__main__":
    def part_design(): Gui.activateWorkbench("PartDesignWorkbench")
    def part(): Gui.activateWorkbench("PartWorkbench")
    def draft(): Gui.activateWorkbench("DraftWorkbench")
    def arch(): Gui.activateWorkbench("ArchWorkbench")
    def fem(): Gui.activateWorkbench("FemWorkbench")
    def sketch(): Gui.activateWorkbench("SketcherWorkbench")
    def draw(): Gui.activateWorkbench("DrawingWorkbench")
    def mesh(): Gui.activateWorkbench("MeshWorkbench")

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
    view = Gui.ActiveDocument.ActiveView
    view.addEventCallback("SoKeyboardEvent", a.showAtMouse)

