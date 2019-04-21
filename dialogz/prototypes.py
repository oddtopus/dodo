from PySide import QtCore, QtGui, QtWidgets # or PyQt5 ?

class protoPypeForm(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("protoPypeForm")
        Dialog.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.currentRatingLab = QtWidgets.QLabel(Dialog)
        self.currentRatingLab.setObjectName("currentRatingLab")
        self.gridLayout.addWidget(self.currentRatingLab, 0, 0, 1, 1)
        self.combo = QtWidgets.QComboBox(Dialog)
        self.combo.setObjectName("combo")
        self.gridLayout.addWidget(self.combo, 0, 1, 1, 1)
        self.sizeList = QtWidgets.QListWidget(Dialog)
        self.sizeList.setObjectName("sizeList")
        self.gridLayout.addWidget(self.sizeList, 1, 0, 2, 1)
        self.ratingList = QtWidgets.QListWidget(Dialog)
        self.ratingList.setObjectName("ratingList")
        self.gridLayout.addWidget(self.ratingList, 1, 1, 1, 1)
        self.btn1 = QtWidgets.QPushButton(Dialog)
        self.btn1.setObjectName("btn1")
        self.gridLayout.addWidget(self.btn1, 2, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.currentRatingLab.setText(_translate("Dialog", "Rating: "))
        self.btn1.setText(_translate("Dialog", "Insert"))

