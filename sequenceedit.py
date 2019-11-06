# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sequenceedit.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SequenceEditDialog(object):
    def setupUi(self, SequenceEditDialog):
        SequenceEditDialog.setObjectName("SequenceEditDialog")
        SequenceEditDialog.resize(736, 534)
        self.gridLayout = QtWidgets.QGridLayout(SequenceEditDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.BaseSeqLabel = QtWidgets.QLabel(SequenceEditDialog)
        self.BaseSeqLabel.setObjectName("BaseSeqLabel")
        self.gridLayout.addWidget(self.BaseSeqLabel, 0, 0, 1, 1)
        self.BaseSeqName = QtWidgets.QLabel(SequenceEditDialog)
        self.BaseSeqName.setObjectName("BaseSeqName")
        self.gridLayout.addWidget(self.BaseSeqName, 0, 1, 1, 1)
        self.ModeLabel = QtWidgets.QLabel(SequenceEditDialog)
        self.ModeLabel.setObjectName("ModeLabel")
        self.gridLayout.addWidget(self.ModeLabel, 1, 0, 1, 2)
        self.ModeTab = QtWidgets.QTabWidget(SequenceEditDialog)
        self.ModeTab.setObjectName("ModeTab")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_tab1 = QtWidgets.QLabel(self.tab)
        self.label_tab1.setObjectName("label_tab1")
        self.gridLayout_2.addWidget(self.label_tab1, 0, 0, 1, 1)
        self.DonorList_tab1 = QtWidgets.QListWidget(self.tab)
        self.DonorList_tab1.setObjectName("DonorList_tab1")
        self.gridLayout_2.addWidget(self.DonorList_tab1, 1, 0, 1, 1)
        self.ModeTab.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_tab2 = QtWidgets.QLabel(self.tab_2)
        self.label_tab2.setObjectName("label_tab2")
        self.gridLayout_3.addWidget(self.label_tab2, 0, 0, 1, 1)
        self.DonorList_tab2 = QtWidgets.QListWidget(self.tab_2)
        self.DonorList_tab2.setObjectName("DonorList_tab2")
        self.gridLayout_3.addWidget(self.DonorList_tab2, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.radioButton_all = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_all.setChecked(True)
        self.radioButton_all.setObjectName("radioButton_all")
        self.horizontalLayout_2.addWidget(self.radioButton_all)
        self.radioButton_single = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_single.setObjectName("radioButton_single")
        self.horizontalLayout_2.addWidget(self.radioButton_single)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.ModeTab.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.ModeTab, 2, 0, 1, 2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.GenerateSeq = QtWidgets.QPushButton(SequenceEditDialog)
        self.GenerateSeq.setDefault(True)
        self.GenerateSeq.setObjectName("GenerateSeq")
        self.horizontalLayout.addWidget(self.GenerateSeq)
        self.Cancel = QtWidgets.QPushButton(SequenceEditDialog)
        self.Cancel.setAutoDefault(True)
        self.Cancel.setObjectName("Cancel")
        self.horizontalLayout.addWidget(self.Cancel)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 2)

        self.retranslateUi(SequenceEditDialog)
        self.ModeTab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(SequenceEditDialog)

    def retranslateUi(self, SequenceEditDialog):
        _translate = QtCore.QCoreApplication.translate
        SequenceEditDialog.setWindowTitle(_translate("SequenceEditDialog", "Edit Sequences"))
        self.BaseSeqLabel.setText(_translate("SequenceEditDialog", "Base Sequence"))
        self.BaseSeqName.setText(_translate("SequenceEditDialog", "Base Sequence"))
        self.ModeLabel.setText(_translate("SequenceEditDialog", "Please choose sequence editing mode:"))
        self.label_tab1.setText(_translate("SequenceEditDialog", "Please select donor sequences, multiple selection is allowed"))
        self.ModeTab.setTabText(self.ModeTab.indexOf(self.tab), _translate("SequenceEditDialog", "Base Biased"))
        self.label_tab2.setText(_translate("SequenceEditDialog", "Please select donor sequence, only single selection allowed"))
        self.radioButton_all.setText(_translate("SequenceEditDialog", "All possible combinations"))
        self.radioButton_single.setText(_translate("SequenceEditDialog", "Only single muitations"))
        self.ModeTab.setTabText(self.ModeTab.indexOf(self.tab_2), _translate("SequenceEditDialog", "Cocktail"))
        self.GenerateSeq.setText(_translate("SequenceEditDialog", "Genearate Sequences"))
        self.Cancel.setText(_translate("SequenceEditDialog", "Cancel"))


