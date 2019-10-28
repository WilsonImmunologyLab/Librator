# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fusiondialog.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_fusionDialog(object):
    def setupUi(self, fusionDialog):
        fusionDialog.setObjectName("fusionDialog")
        fusionDialog.resize(708, 586)
        self.horizontalLayoutWidget = QtWidgets.QWidget(fusionDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 539, 651, 32))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.confirmButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.confirmButton.setDefault(True)
        self.confirmButton.setObjectName("confirmButton")
        self.horizontalLayout.addWidget(self.confirmButton)
        self.cancelButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.selection = QtWidgets.QListWidget(fusionDialog)
        self.selection.setGeometry(QtCore.QRect(30, 110, 651, 181))
        self.selection.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.selection.setObjectName("selection")
        self.label = QtWidgets.QLabel(fusionDialog)
        self.label.setGeometry(QtCore.QRect(30, 80, 391, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(fusionDialog)
        self.label_2.setGeometry(QtCore.QRect(30, 310, 391, 21))
        self.label_2.setObjectName("label_2")
        self.basename = QtWidgets.QLineEdit(fusionDialog)
        self.basename.setGeometry(QtCore.QRect(30, 340, 651, 31))
        self.basename.setReadOnly(True)
        self.basename.setObjectName("basename")
        self.showButton = QtWidgets.QPushButton(fusionDialog)
        self.showButton.setGeometry(QtCore.QRect(432, 410, 251, 71))
        self.showButton.setObjectName("showButton")
        self.label_3 = QtWidgets.QLabel(fusionDialog)
        self.label_3.setGeometry(QtCore.QRect(30, 390, 391, 21))
        self.label_3.setObjectName("label_3")
        self.startBase = QtWidgets.QLineEdit(fusionDialog)
        self.startBase.setGeometry(QtCore.QRect(30, 420, 161, 31))
        self.startBase.setObjectName("startBase")
        self.endBase = QtWidgets.QLineEdit(fusionDialog)
        self.endBase.setGeometry(QtCore.QRect(240, 420, 161, 31))
        self.endBase.setObjectName("endBase")
        self.startDonor = QtWidgets.QLineEdit(fusionDialog)
        self.startDonor.setGeometry(QtCore.QRect(30, 490, 161, 31))
        self.startDonor.setObjectName("startDonor")
        self.endDonor = QtWidgets.QLineEdit(fusionDialog)
        self.endDonor.setGeometry(QtCore.QRect(240, 490, 161, 31))
        self.endDonor.setObjectName("endDonor")
        self.label_4 = QtWidgets.QLabel(fusionDialog)
        self.label_4.setGeometry(QtCore.QRect(30, 460, 391, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(fusionDialog)
        self.label_5.setGeometry(QtCore.QRect(210, 420, 31, 21))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(fusionDialog)
        self.label_6.setGeometry(QtCore.QRect(210, 490, 31, 21))
        self.label_6.setObjectName("label_6")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(fusionDialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(440, 490, 241, 41))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.dna = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.dna.setChecked(False)
        self.dna.setAutoExclusive(False)
        self.dna.setObjectName("dna")
        self.horizontalLayout_2.addWidget(self.dna)
        self.aa = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.aa.setChecked(True)
        self.aa.setAutoExclusive(False)
        self.aa.setObjectName("aa")
        self.horizontalLayout_2.addWidget(self.aa)
        self.ba = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.ba.setChecked(True)
        self.ba.setAutoExclusive(False)
        self.ba.setObjectName("ba")
        self.horizontalLayout_2.addWidget(self.ba)
        self.label_7 = QtWidgets.QLabel(fusionDialog)
        self.label_7.setGeometry(QtCore.QRect(30, 20, 651, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")

        self.retranslateUi(fusionDialog)
        QtCore.QMetaObject.connectSlotsByName(fusionDialog)

    def retranslateUi(self, fusionDialog):
        _translate = QtCore.QCoreApplication.translate
        fusionDialog.setWindowTitle(_translate("fusionDialog", "Sequence Fusion across subtypes"))
        self.confirmButton.setText(_translate("fusionDialog", "Confirm"))
        self.cancelButton.setText(_translate("fusionDialog", "Cancel"))
        self.label.setText(_translate("fusionDialog", "Select donor sequence from the following list:"))
        self.label_2.setText(_translate("fusionDialog", "Current Base sequence:"))
        self.showButton.setText(_translate("fusionDialog", "Show Alignment"))
        self.label_3.setText(_translate("fusionDialog", "Replaced region on base sequence:"))
        self.label_4.setText(_translate("fusionDialog", "Donor region on donor sequence:"))
        self.label_5.setText(_translate("fusionDialog", "to"))
        self.label_6.setText(_translate("fusionDialog", "to"))
        self.dna.setText(_translate("fusionDialog", "DNA"))
        self.aa.setText(_translate("fusionDialog", "AA"))
        self.ba.setText(_translate("fusionDialog", "BA"))
        self.label_7.setText(_translate("fusionDialog", "Design your HA sequence across subtypes using SequenceFusion function"))


