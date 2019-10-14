# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bin_path_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_binPathDialog(object):
    def setupUi(self, binPathDialog):
        binPathDialog.setObjectName("binPathDialog")
        binPathDialog.resize(717, 204)
        self.binPath = QtWidgets.QLineEdit(binPathDialog)
        self.binPath.setGeometry(QtCore.QRect(40, 90, 531, 31))
        self.binPath.setObjectName("binPath")
        self.pushButton = QtWidgets.QPushButton(binPathDialog)
        self.pushButton.setGeometry(QtCore.QRect(580, 90, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(binPathDialog)
        self.label.setGeometry(QtCore.QRect(50, 30, 441, 16))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(binPathDialog)
        self.label_2.setGeometry(QtCore.QRect(50, 60, 441, 16))
        self.label_2.setObjectName("label_2")
        self.horizontalLayoutWidget = QtWidgets.QWidget(binPathDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(40, 150, 651, 32))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.yes = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.yes.setDefault(True)
        self.yes.setObjectName("yes")
        self.horizontalLayout.addWidget(self.yes)
        self.no = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.no.setObjectName("no")
        self.horizontalLayout.addWidget(self.no)

        self.retranslateUi(binPathDialog)
        QtCore.QMetaObject.connectSlotsByName(binPathDialog)

    def retranslateUi(self, binPathDialog):
        _translate = QtCore.QCoreApplication.translate
        binPathDialog.setWindowTitle(_translate("binPathDialog", "Dialog"))
        self.pushButton.setText(_translate("binPathDialog", "Browse"))
        self.label.setText(_translate("binPathDialog", "Your current bin path is:"))
        self.label_2.setText(_translate("binPathDialog", "You can set bin path by typing or click button to browse:"))
        self.yes.setText(_translate("binPathDialog", "Confirm"))
        self.no.setText(_translate("binPathDialog", "Cancel"))


