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
        deleteDialog.resize(703, 601)
        self.gridLayout_2 = QtWidgets.QGridLayout(deleteDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.deleteButton = QtWidgets.QPushButton(deleteDialog)
        self.deleteButton.setCheckable(True)
        self.deleteButton.setChecked(True)
        self.deleteButton.setObjectName("deleteButton")
        self.horizontalLayout.addWidget(self.deleteButton)
        self.cancelButton = QtWidgets.QPushButton(deleteDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(deleteDialog)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.listWidget = QtWidgets.QListWidget(deleteDialog)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout.addWidget(self.listWidget, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(deleteDialog)
        QtCore.QMetaObject.connectSlotsByName(deleteDialog)

    def retranslateUi(self, deleteDialog):
        _translate = QtCore.QCoreApplication.translate
        deleteDialog.setWindowTitle(_translate("deleteDialog", "Dialog"))
        self.deleteButton.setText(_translate("deleteDialog", "Delete"))
        self.cancelButton.setText(_translate("deleteDialog", "Cancel"))
        self.label.setText(_translate("deleteDialog", "Please confirm the delete list:"))
        self.listWidget.setSortingEnabled(True)

