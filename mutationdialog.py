# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mutationdialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MutationDialog(object):
    def setupUi(self, MutationDialog):
        MutationDialog.setObjectName("MutationDialog")
        MutationDialog.resize(882, 785)
        self.gridLayout_3 = QtWidgets.QGridLayout(MutationDialog)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(MutationDialog)
        self.tabWidget.setMaximumSize(QtCore.QSize(16777215, 120))
        self.tabWidget.setObjectName("tabWidget")
        self.OriPos = QtWidgets.QWidget()
        self.OriPos.setObjectName("OriPos")
        self.gridLayout = QtWidgets.QGridLayout(self.OriPos)
        self.gridLayout.setObjectName("gridLayout")
        self.labelpos = QtWidgets.QLabel(self.OriPos)
        self.labelpos.setObjectName("labelpos")
        self.gridLayout.addWidget(self.labelpos, 0, 0, 1, 1)
        self.Mutation = QtWidgets.QLineEdit(self.OriPos)
        self.Mutation.setObjectName("Mutation")
        self.gridLayout.addWidget(self.Mutation, 0, 1, 1, 1)
        self.tabWidget.addTab(self.OriPos, "")
        self.H1H3pos = QtWidgets.QWidget()
        self.H1H3pos.setObjectName("H1H3pos")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.H1H3pos)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.labelHA1 = QtWidgets.QLabel(self.H1H3pos)
        self.labelHA1.setObjectName("labelHA1")
        self.gridLayout_2.addWidget(self.labelHA1, 0, 0, 1, 1)
        self.HA1mutation = QtWidgets.QLineEdit(self.H1H3pos)
        self.HA1mutation.setObjectName("HA1mutation")
        self.gridLayout_2.addWidget(self.HA1mutation, 0, 1, 1, 1)
        self.labelHA2 = QtWidgets.QLabel(self.H1H3pos)
        self.labelHA2.setObjectName("labelHA2")
        self.gridLayout_2.addWidget(self.labelHA2, 1, 0, 1, 1)
        self.HA2mutation = QtWidgets.QLineEdit(self.H1H3pos)
        self.HA2mutation.setObjectName("HA2mutation")
        self.gridLayout_2.addWidget(self.HA2mutation, 1, 1, 1, 1)
        self.tabWidget.addTab(self.H1H3pos, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.labelHA1_2 = QtWidgets.QLabel(self.tab)
        self.labelHA1_2.setObjectName("labelHA1_2")
        self.gridLayout_4.addWidget(self.labelHA1_2, 0, 0, 1, 1)
        self.HA1mutationH3 = QtWidgets.QLineEdit(self.tab)
        self.HA1mutationH3.setObjectName("HA1mutationH3")
        self.gridLayout_4.addWidget(self.HA1mutationH3, 0, 1, 1, 1)
        self.labelHA2_2 = QtWidgets.QLabel(self.tab)
        self.labelHA2_2.setObjectName("labelHA2_2")
        self.gridLayout_4.addWidget(self.labelHA2_2, 1, 0, 1, 1)
        self.HA2mutationH3 = QtWidgets.QLineEdit(self.tab)
        self.HA2mutationH3.setObjectName("HA2mutationH3")
        self.gridLayout_4.addWidget(self.HA2mutationH3, 1, 1, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.gridLayout_3.addWidget(self.tabWidget, 3, 0, 1, 2)
        self.SeqName = QtWidgets.QLineEdit(MutationDialog)
        self.SeqName.setObjectName("SeqName")
        self.gridLayout_3.addWidget(self.SeqName, 5, 1, 1, 1)
        self.CurSeq = QtWidgets.QLabel(MutationDialog)
        self.CurSeq.setText("")
        self.CurSeq.setObjectName("CurSeq")
        self.gridLayout_3.addWidget(self.CurSeq, 2, 1, 1, 1)
        self.labelSeqName = QtWidgets.QLabel(MutationDialog)
        self.labelSeqName.setObjectName("labelSeqName")
        self.gridLayout_3.addWidget(self.labelSeqName, 5, 0, 1, 1)
        self.label = QtWidgets.QLabel(MutationDialog)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 1, 0, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(MutationDialog)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_3.addWidget(self.textEdit, 8, 0, 1, 2)
        self.Title = QtWidgets.QLabel(MutationDialog)
        self.Title.setObjectName("Title")
        self.gridLayout_3.addWidget(self.Title, 0, 0, 1, 2)
        self.CurSeqLab = QtWidgets.QLabel(MutationDialog)
        self.CurSeqLab.setObjectName("CurSeqLab")
        self.gridLayout_3.addWidget(self.CurSeqLab, 2, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.radioSingle = QtWidgets.QRadioButton(MutationDialog)
        self.radioSingle.setChecked(True)
        self.radioSingle.setObjectName("radioSingle")
        self.horizontalLayout_2.addWidget(self.radioSingle)
        self.radioAll = QtWidgets.QRadioButton(MutationDialog)
        self.radioAll.setObjectName("radioAll")
        self.horizontalLayout_2.addWidget(self.radioAll)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 6, 0, 1, 2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.addMutation = QtWidgets.QPushButton(MutationDialog)
        self.addMutation.setDefault(True)
        self.addMutation.setObjectName("addMutation")
        self.horizontalLayout.addWidget(self.addMutation)
        self.cancel = QtWidgets.QPushButton(MutationDialog)
        self.cancel.setObjectName("cancel")
        self.horizontalLayout.addWidget(self.cancel)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout_3.addLayout(self.horizontalLayout, 9, 0, 1, 1)

        self.retranslateUi(MutationDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MutationDialog)

    def retranslateUi(self, MutationDialog):
        _translate = QtCore.QCoreApplication.translate
        MutationDialog.setWindowTitle(_translate("MutationDialog", "Generate mutated sequence"))
        self.labelpos.setText(_translate("MutationDialog", "Mutations"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.OriPos), _translate("MutationDialog", "Original Position"))
        self.labelHA1.setText(_translate("MutationDialog", "HA1 mutations"))
        self.labelHA2.setText(_translate("MutationDialog", "HA2 mutations"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.H1H3pos), _translate("MutationDialog", "H1 Numbering"))
        self.labelHA1_2.setText(_translate("MutationDialog", "HA1 mutations"))
        self.labelHA2_2.setText(_translate("MutationDialog", "HA2 mutations"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MutationDialog", "H3 Numbering"))
        self.labelSeqName.setText(_translate("MutationDialog", "New SEQ Name"))
        self.label.setText(_translate("MutationDialog", "You can use \"X\" to represent any Amino acids: e.g. X102M"))
        self.Title.setText(_translate("MutationDialog", "Please type your mutations below: e.g. R98Y, K141E"))
        self.CurSeqLab.setText(_translate("MutationDialog", "Current Sequence: "))
        self.radioSingle.setText(_translate("MutationDialog", "Single Sequence with all mutations"))
        self.radioAll.setText(_translate("MutationDialog", "Sequences with each single mutation"))
        self.addMutation.setText(_translate("MutationDialog", "Genearate Sequence "))
        self.cancel.setText(_translate("MutationDialog", "Cancel"))
