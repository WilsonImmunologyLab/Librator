# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'base_path_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_basePathDialog(object):
    def setupUi(self, basePathDialog):
        basePathDialog.setObjectName("basePathDialog")
        basePathDialog.resize(728, 197)
        self.label = QtWidgets.QLabel(basePathDialog)
        self.label.setGeometry(QtCore.QRect(40, 20, 441, 16))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(basePathDialog)
        self.label_2.setGeometry(QtCore.QRect(40, 50, 441, 16))
        self.label_2.setObjectName("label_2")
        self.basePath = QtWidgets.QLineEdit(basePathDialog)
        self.basePath.setGeometry(QtCore.QRect(40, 80, 531, 31))
        self.basePath.setObjectName("basePath")
        self.pushButton = QtWidgets.QPushButton(basePathDialog)
        self.pushButton.setGeometry(QtCore.QRect(590, 80, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayoutWidget = QtWidgets.QWidget(basePathDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(40, 130, 661, 32))
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

        self.retranslateUi(basePathDialog)
        QtCore.QMetaObject.connectSlotsByName(basePathDialog)

    def retranslateUi(self, basePathDialog):
        _translate = QtCore.QCoreApplication.translate
        basePathDialog.setWindowTitle(_translate("basePathDialog", "Dialog"))
        self.label.setText(_translate("basePathDialog", "Your current base path is:"))
        self.label_2.setText(_translate("basePathDialog", "You can set bin path by typing or click button to browse:"))
        self.pushButton.setText(_translate("basePathDialog", "Browse"))
        self.yes.setText(_translate("basePathDialog", "Confirm"))
        self.no.setText(_translate("basePathDialog", "Cancel"))


