# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'updatesequencedialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
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
        self.label_2 = QtWidgets.QLabel(UpdateSequenceDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(UpdateSequenceDialog)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.searchBtn = QtWidgets.QCommandLinkButton(UpdateSequenceDialog)
        self.searchBtn.setMaximumSize(QtCore.QSize(80, 16777215))
        self.searchBtn.setObjectName("searchBtn")
        self.horizontalLayout_3.addWidget(self.searchBtn)
        self.SearchText = QtWidgets.QLineEdit(UpdateSequenceDialog)
        self.SearchText.setMaximumSize(QtCore.QSize(250, 16777215))
        self.SearchText.setObjectName("SearchText")
        self.horizontalLayout_3.addWidget(self.SearchText)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_5 = QtWidgets.QLabel(UpdateSequenceDialog)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.RFstart = QtWidgets.QSpinBox(UpdateSequenceDialog)
        self.RFstart.setMinimumSize(QtCore.QSize(40, 0))
        self.RFstart.setMinimum(1)
        self.RFstart.setMaximum(5000)
        self.RFstart.setObjectName("RFstart")
        self.horizontalLayout_2.addWidget(self.RFstart)
        self.label_6 = QtWidgets.QLabel(UpdateSequenceDialog)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.RFend = QtWidgets.QSpinBox(UpdateSequenceDialog)
        self.RFend.setMinimumSize(QtCore.QSize(40, 0))
        self.RFend.setMinimum(0)
        self.RFend.setMaximum(5000)
        self.RFend.setProperty("value", 5000)
        self.RFend.setObjectName("RFend")
        self.horizontalLayout_2.addWidget(self.RFend)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(UpdateSequenceDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(UpdateSequenceDialog)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 4, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(UpdateSequenceDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 2)
        self.textEditAA = QtWidgets.QTextEdit(UpdateSequenceDialog)
        self.textEditAA.setReadOnly(True)
        self.textEditAA.setObjectName("textEditAA")
        self.gridLayout.addWidget(self.textEditAA, 6, 0, 1, 2)
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
        self.gridLayout.addLayout(self.horizontalLayout, 7, 0, 1, 1)

        self.retranslateUi(UpdateSequenceDialog)
        QtCore.QMetaObject.connectSlotsByName(UpdateSequenceDialog)

    def retranslateUi(self, UpdateSequenceDialog):
        _translate = QtCore.QCoreApplication.translate
        UpdateSequenceDialog.setWindowTitle(_translate("UpdateSequenceDialog", "Update Sequence"))
        self.label_2.setText(_translate("UpdateSequenceDialog", "Sequence Name:"))
        self.searchBtn.setText(_translate("UpdateSequenceDialog", "Search"))
        self.label_5.setText(_translate("UpdateSequenceDialog", "Coding Region From:"))
        self.label_6.setText(_translate("UpdateSequenceDialog", "To:"))
        self.label.setText(_translate("UpdateSequenceDialog", "Sequence:"))
        self.label_3.setText(_translate("UpdateSequenceDialog", "Translated Amino Acid sequence: (Using current reading frame)"))
        self.confirmButton.setText(_translate("UpdateSequenceDialog", "Confirm"))
        self.cancelButton.setText(_translate("UpdateSequenceDialog", "Cancel"))
