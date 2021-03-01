# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'codon_optimize_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CodonDialog(object):
    def setupUi(self, CodonDialog):
        CodonDialog.setObjectName("CodonDialog")
        CodonDialog.resize(933, 734)
        self.gridLayout = QtWidgets.QGridLayout(CodonDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.comboBoxSpecies = QtWidgets.QComboBox(CodonDialog)
        self.comboBoxSpecies.setMinimumSize(QtCore.QSize(150, 0))
        self.comboBoxSpecies.setObjectName("comboBoxSpecies")
        self.gridLayout.addWidget(self.comboBoxSpecies, 1, 4, 1, 1)
        self.pushButtonHighlight = QtWidgets.QPushButton(CodonDialog)
        self.pushButtonHighlight.setMaximumSize(QtCore.QSize(16777215, 30))
        self.pushButtonHighlight.setObjectName("pushButtonHighlight")
        self.gridLayout.addWidget(self.pushButtonHighlight, 8, 5, 1, 1)
        self.label_6 = QtWidgets.QLabel(CodonDialog)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 2)
        self.textEditSeqOpt = QtWidgets.QTextEdit(CodonDialog)
        self.textEditSeqOpt.setObjectName("textEditSeqOpt")
        self.gridLayout.addWidget(self.textEditSeqOpt, 9, 0, 3, 8)
        self.label_3 = QtWidgets.QLabel(CodonDialog)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 8, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(CodonDialog)
        self.label_2.setMaximumSize(QtCore.QSize(80, 30))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 8, 3, 1, 1)
        self.label_7 = QtWidgets.QLabel(CodonDialog)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 1, 3, 1, 1)
        self.lcdNumberGCOri = QtWidgets.QLCDNumber(CodonDialog)
        self.lcdNumberGCOri.setMaximumSize(QtCore.QSize(80, 30))
        self.lcdNumberGCOri.setObjectName("lcdNumberGCOri")
        self.gridLayout.addWidget(self.lcdNumberGCOri, 3, 4, 1, 1)
        self.pushButtonSave = QtWidgets.QPushButton(CodonDialog)
        self.pushButtonSave.setMaximumSize(QtCore.QSize(80, 16777215))
        self.pushButtonSave.setObjectName("pushButtonSave")
        self.gridLayout.addWidget(self.pushButtonSave, 1, 7, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(CodonDialog)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 13, 0, 1, 8)
        self.pushButtonManualEdit = QtWidgets.QPushButton(CodonDialog)
        self.pushButtonManualEdit.setMaximumSize(QtCore.QSize(200, 16777215))
        self.pushButtonManualEdit.setObjectName("pushButtonManualEdit")
        self.gridLayout.addWidget(self.pushButtonManualEdit, 12, 0, 1, 1)
        self.frame = QtWidgets.QFrame(CodonDialog)
        self.frame.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_5 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 8)
        self.label = QtWidgets.QLabel(CodonDialog)
        self.label.setMaximumSize(QtCore.QSize(80, 30))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 3, 1, 1)
        self.textEditSeqOri = QtWidgets.QTextEdit(CodonDialog)
        self.textEditSeqOri.setObjectName("textEditSeqOri")
        self.gridLayout.addWidget(self.textEditSeqOri, 4, 0, 3, 8)
        self.pushButtonRun = QtWidgets.QPushButton(CodonDialog)
        self.pushButtonRun.setMaximumSize(QtCore.QSize(80, 16777215))
        self.pushButtonRun.setObjectName("pushButtonRun")
        self.gridLayout.addWidget(self.pushButtonRun, 1, 6, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 5, 1, 1)
        self.line_2 = QtWidgets.QFrame(CodonDialog)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 2, 0, 1, 8)
        self.lcdNumberGCOpt = QtWidgets.QLCDNumber(CodonDialog)
        self.lcdNumberGCOpt.setMaximumSize(QtCore.QSize(80, 30))
        self.lcdNumberGCOpt.setObjectName("lcdNumberGCOpt")
        self.gridLayout.addWidget(self.lcdNumberGCOpt, 8, 4, 1, 1)
        self.comboBoxSeqName = QtWidgets.QComboBox(CodonDialog)
        self.comboBoxSeqName.setMinimumSize(QtCore.QSize(200, 0))
        self.comboBoxSeqName.setObjectName("comboBoxSeqName")
        self.gridLayout.addWidget(self.comboBoxSeqName, 1, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(CodonDialog)
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.lineEditPattern = QtWidgets.QLineEdit(CodonDialog)
        self.lineEditPattern.setObjectName("lineEditPattern")
        self.gridLayout.addWidget(self.lineEditPattern, 8, 6, 1, 2)

        self.retranslateUi(CodonDialog)
        QtCore.QMetaObject.connectSlotsByName(CodonDialog)

    def retranslateUi(self, CodonDialog):
        _translate = QtCore.QCoreApplication.translate
        CodonDialog.setWindowTitle(_translate("CodonDialog", "Dialog"))
        self.pushButtonHighlight.setText(_translate("CodonDialog", "Highlight Pattern"))
        self.label_6.setText(_translate("CodonDialog", "Target Sequence"))
        self.label_3.setText(_translate("CodonDialog", "Optimized Sequence (NT)"))
        self.label_2.setText(_translate("CodonDialog", "GC %"))
        self.label_7.setText(_translate("CodonDialog", "Species"))
        self.pushButtonSave.setText(_translate("CodonDialog", "Save"))
        self.pushButtonManualEdit.setText(_translate("CodonDialog", "Manual Edit"))
        self.label_5.setText(_translate("CodonDialog", "Codon optimization"))
        self.label.setText(_translate("CodonDialog", "GC %"))
        self.pushButtonRun.setText(_translate("CodonDialog", "Run"))
        self.label_4.setText(_translate("CodonDialog", "Original Sequence (NT)"))
