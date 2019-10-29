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
        self.textEdit = QtWidgets.QTextEdit(UpdateSequenceDialog)
        self.textEdit.setGeometry(QtCore.QRect(40, 130, 611, 451))
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(UpdateSequenceDialog)
        self.label.setGeometry(QtCore.QRect(40, 90, 59, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(UpdateSequenceDialog)
        self.label_2.setGeometry(QtCore.QRect(40, 20, 141, 16))
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(UpdateSequenceDialog)
        self.lineEdit.setGeometry(QtCore.QRect(40, 50, 611, 31))
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayoutWidget = QtWidgets.QWidget(UpdateSequenceDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(40, 590, 611, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.confirmButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.confirmButton.setCheckable(True)
        self.confirmButton.setChecked(True)
        self.confirmButton.setObjectName("confirmButton")
        self.horizontalLayout.addWidget(self.confirmButton)
        self.cancelButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.cancelButton.setCheckable(True)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)

        self.retranslateUi(UpdateSequenceDialog)
        QtCore.QMetaObject.connectSlotsByName(UpdateSequenceDialog)

    def retranslateUi(self, UpdateSequenceDialog):
        _translate = QtCore.QCoreApplication.translate
        UpdateSequenceDialog.setWindowTitle(_translate("UpdateSequenceDialog", "Update Sequence"))
        self.label.setText(_translate("UpdateSequenceDialog", "Sequence:"))
        self.label_2.setText(_translate("UpdateSequenceDialog", "Sequence Name:"))
        self.confirmButton.setText(_translate("UpdateSequenceDialog", "Confirm"))
        self.cancelButton.setText(_translate("UpdateSequenceDialog", "Cancel"))


