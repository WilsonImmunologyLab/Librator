# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aa_or_nt.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_aantDialog(object):
    def setupUi(self, aantDialog):
        aantDialog.setObjectName("aantDialog")
        aantDialog.resize(430, 84)
        self.gridLayout = QtWidgets.QGridLayout(aantDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(aantDialog)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)
        self.pushButtonAA = QtWidgets.QPushButton(aantDialog)
        self.pushButtonAA.setObjectName("pushButtonAA")
        self.gridLayout.addWidget(self.pushButtonAA, 1, 0, 1, 1)
        self.pushButtonNT = QtWidgets.QPushButton(aantDialog)
        self.pushButtonNT.setObjectName("pushButtonNT")
        self.gridLayout.addWidget(self.pushButtonNT, 1, 1, 1, 1)
        self.pushButtonCancel = QtWidgets.QPushButton(aantDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.gridLayout.addWidget(self.pushButtonCancel, 1, 2, 1, 1)

        self.retranslateUi(aantDialog)
        QtCore.QMetaObject.connectSlotsByName(aantDialog)

    def retranslateUi(self, aantDialog):
        _translate = QtCore.QCoreApplication.translate
        aantDialog.setWindowTitle(_translate("aantDialog", "Dialog"))
        self.label.setText(_translate("aantDialog", "Please choose sequence type:"))
        self.pushButtonAA.setText(_translate("aantDialog", "Amino Acid"))
        self.pushButtonNT.setText(_translate("aantDialog", "Nucleotide"))
        self.pushButtonCancel.setText(_translate("aantDialog", "Cancel"))
