# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'idmutationdialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_IdMutationDialog(object):
    def setupUi(self, IdMutationDialog):
        IdMutationDialog.setObjectName("IdMutationDialog")
        IdMutationDialog.resize(1007, 698)
        self.gridLayout_2 = QtWidgets.QGridLayout(IdMutationDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(IdMutationDialog)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.comboBoxTemplate = QtWidgets.QComboBox(IdMutationDialog)
        self.comboBoxTemplate.setObjectName("comboBoxTemplate")
        self.gridLayout_2.addWidget(self.comboBoxTemplate, 0, 1, 1, 3)
        self.label_2 = QtWidgets.QLabel(IdMutationDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.comboBoxTarget = QtWidgets.QComboBox(IdMutationDialog)
        self.comboBoxTarget.setObjectName("comboBoxTarget")
        self.gridLayout_2.addWidget(self.comboBoxTarget, 1, 1, 1, 3)
        self.groupBoxHTML = QtWidgets.QGroupBox(IdMutationDialog)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.groupBoxHTML.setFont(font)
        self.groupBoxHTML.setObjectName("groupBoxHTML")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBoxHTML)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayoutHTML = QtWidgets.QGridLayout()
        self.gridLayoutHTML.setObjectName("gridLayoutHTML")
        self.gridLayout_4.addLayout(self.gridLayoutHTML, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBoxHTML, 2, 0, 1, 4)
        self.textEdit = QtWidgets.QTextEdit(IdMutationDialog)
        self.textEdit.setMaximumSize(QtCore.QSize(16777215, 100))
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_2.addWidget(self.textEdit, 4, 0, 1, 4)
        self.pushButtonConfirm = QtWidgets.QPushButton(IdMutationDialog)
        self.pushButtonConfirm.setDefault(True)
        self.pushButtonConfirm.setFlat(False)
        self.pushButtonConfirm.setObjectName("pushButtonConfirm")
        self.gridLayout_2.addWidget(self.pushButtonConfirm, 5, 2, 1, 1)
        self.pushButtonCancel = QtWidgets.QPushButton(IdMutationDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.gridLayout_2.addWidget(self.pushButtonCancel, 5, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 5, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(IdMutationDialog)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 3, 0, 1, 3)

        self.retranslateUi(IdMutationDialog)
        QtCore.QMetaObject.connectSlotsByName(IdMutationDialog)

    def retranslateUi(self, IdMutationDialog):
        _translate = QtCore.QCoreApplication.translate
        IdMutationDialog.setWindowTitle(_translate("IdMutationDialog", "Dialog"))
        self.label.setText(_translate("IdMutationDialog", "Template Sequence"))
        self.label_2.setText(_translate("IdMutationDialog", "Target Sequence"))
        self.groupBoxHTML.setTitle(_translate("IdMutationDialog", "Sequence Alignment"))
        self.pushButtonConfirm.setText(_translate("IdMutationDialog", "Confirm"))
        self.pushButtonCancel.setText(_translate("IdMutationDialog", "Cancel"))
        self.label_3.setText(_translate("IdMutationDialog", "Mutations between current template and target sequences:"))
