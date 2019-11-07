# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'updatesequencedialog.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UpdateSequenceDialog(object):
    def setupUi(self, UpdateSequenceDialog):
        UpdateSequenceDialog.setObjectName("UpdateSequenceDialog")
        UpdateSequenceDialog.resize(685, 645)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(UpdateSequenceDialog.sizePolicy().hasHeightForWidth())
        UpdateSequenceDialog.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(UpdateSequenceDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(UpdateSequenceDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(UpdateSequenceDialog)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(UpdateSequenceDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(UpdateSequenceDialog)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 3, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.confirmButton = QtWidgets.QPushButton(UpdateSequenceDialog)
        self.confirmButton.setCheckable(True)
        self.confirmButton.setChecked(True)
        self.confirmButton.setObjectName("confirmButton")
        self.horizontalLayout.addWidget(self.confirmButton)
        self.cancelButton = QtWidgets.QPushButton(UpdateSequenceDialog)
        self.cancelButton.setCheckable(True)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.gridLayout.addLayout(self.horizontalLayout, 6, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(UpdateSequenceDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.textEditAA = QtWidgets.QTextEdit(UpdateSequenceDialog)
        self.textEditAA.setReadOnly(True)
        self.textEditAA.setObjectName("textEditAA")
        self.gridLayout.addWidget(self.textEditAA, 5, 0, 1, 1)

        self.retranslateUi(UpdateSequenceDialog)
        QtCore.QMetaObject.connectSlotsByName(UpdateSequenceDialog)

    def retranslateUi(self, UpdateSequenceDialog):
        _translate = QtCore.QCoreApplication.translate
        UpdateSequenceDialog.setWindowTitle(_translate("UpdateSequenceDialog", "Update Sequence"))
        self.label.setText(_translate("UpdateSequenceDialog", "Sequence:"))
        self.label_3.setText(_translate("UpdateSequenceDialog", "Translated Amino Acid sequence: (Using reading frame 0)"))
        self.confirmButton.setText(_translate("UpdateSequenceDialog", "Confirm"))
        self.cancelButton.setText(_translate("UpdateSequenceDialog", "Cancel"))
        self.label_2.setText(_translate("UpdateSequenceDialog", "Sequence Name:"))


