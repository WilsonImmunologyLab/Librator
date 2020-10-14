# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fastaorseqdialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FastaOrSeqDialog(object):
    def setupUi(self, FastaOrSeqDialog):
        FastaOrSeqDialog.setObjectName("FastaOrSeqDialog")
        FastaOrSeqDialog.resize(518, 91)
        self.gridLayout = QtWidgets.QGridLayout(FastaOrSeqDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(FastaOrSeqDialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)
        self.pushButtonFasta = QtWidgets.QPushButton(FastaOrSeqDialog)
        self.pushButtonFasta.setDefault(True)
        self.pushButtonFasta.setObjectName("pushButtonFasta")
        self.gridLayout.addWidget(self.pushButtonFasta, 1, 0, 1, 1)
        self.pushButtonSEQ = QtWidgets.QPushButton(FastaOrSeqDialog)
        self.pushButtonSEQ.setObjectName("pushButtonSEQ")
        self.gridLayout.addWidget(self.pushButtonSEQ, 1, 1, 1, 1)
        self.pushButtonCancel = QtWidgets.QPushButton(FastaOrSeqDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.gridLayout.addWidget(self.pushButtonCancel, 1, 2, 1, 1)

        self.retranslateUi(FastaOrSeqDialog)
        QtCore.QMetaObject.connectSlotsByName(FastaOrSeqDialog)

    def retranslateUi(self, FastaOrSeqDialog):
        _translate = QtCore.QCoreApplication.translate
        FastaOrSeqDialog.setWindowTitle(_translate("FastaOrSeqDialog", "Dialog"))
        self.label.setText(_translate("FastaOrSeqDialog", "Please choose the input format:"))
        self.pushButtonFasta.setText(_translate("FastaOrSeqDialog", "Fasta"))
        self.pushButtonSEQ.setText(_translate("FastaOrSeqDialog", "SEQ"))
        self.pushButtonCancel.setText(_translate("FastaOrSeqDialog", "Cancel"))
