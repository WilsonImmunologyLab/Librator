# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'deletedialog.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_deleteDialog(object):
    def setupUi(self, deleteDialog):
        deleteDialog.setObjectName("deleteDialog")
        deleteDialog.resize(991, 682)
        self.label = QtWidgets.QLabel(deleteDialog)
        self.label.setGeometry(QtCore.QRect(30, 30, 301, 16))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayoutWidget = QtWidgets.QWidget(deleteDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 630, 931, 32))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.deleteButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.deleteButton.setCheckable(True)
        self.deleteButton.setChecked(True)
        self.deleteButton.setObjectName("deleteButton")
        self.horizontalLayout.addWidget(self.deleteButton)
        self.cancelButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.listWidget = QtWidgets.QListWidget(deleteDialog)
        self.listWidget.setGeometry(QtCore.QRect(30, 70, 931, 541))
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listWidget.setObjectName("listWidget")

        self.retranslateUi(deleteDialog)
        QtCore.QMetaObject.connectSlotsByName(deleteDialog)

    def retranslateUi(self, deleteDialog):
        _translate = QtCore.QCoreApplication.translate
        deleteDialog.setWindowTitle(_translate("deleteDialog", "Dialog"))
        self.label.setText(_translate("deleteDialog", "Please confirm the delete list:"))
        self.deleteButton.setText(_translate("deleteDialog", "Delete"))
        self.cancelButton.setText(_translate("deleteDialog", "Cancel"))
        self.listWidget.setSortingEnabled(True)


