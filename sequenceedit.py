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
        self.ModeTab = QtWidgets.QTabWidget(SequenceEditDialog)
        self.ModeTab.setGeometry(QtCore.QRect(40, 100, 631, 341))
        self.ModeTab.setObjectName("ModeTab")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.DonorList_tab1 = QtWidgets.QListWidget(self.tab)
        self.DonorList_tab1.setGeometry(QtCore.QRect(10, 40, 611, 271))
        self.DonorList_tab1.setObjectName("DonorList_tab1")
        self.label_tab1 = QtWidgets.QLabel(self.tab)
        self.label_tab1.setGeometry(QtCore.QRect(10, 10, 581, 16))
        self.label_tab1.setObjectName("label_tab1")
        self.ModeTab.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label_tab2 = QtWidgets.QLabel(self.tab_2)
        self.label_tab2.setGeometry(QtCore.QRect(10, 10, 581, 16))
        self.label_tab2.setObjectName("label_tab2")
        self.DonorList_tab2 = QtWidgets.QListWidget(self.tab_2)
        self.DonorList_tab2.setGeometry(QtCore.QRect(10, 40, 611, 221))
        self.DonorList_tab2.setObjectName("DonorList_tab2")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.tab_2)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 270, 611, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.radioButton_all = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_all.setChecked(True)
        self.radioButton_all.setObjectName("radioButton_all")
        self.horizontalLayout_2.addWidget(self.radioButton_all)
        self.radioButton_single = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_single.setObjectName("radioButton_single")
        self.horizontalLayout_2.addWidget(self.radioButton_single)
        self.ModeTab.addTab(self.tab_2, "")
        self.BaseSeqLabel = QtWidgets.QLabel(SequenceEditDialog)
        self.BaseSeqLabel.setGeometry(QtCore.QRect(50, 30, 101, 16))
        self.BaseSeqLabel.setObjectName("BaseSeqLabel")
        self.ModeLabel = QtWidgets.QLabel(SequenceEditDialog)
        self.ModeLabel.setGeometry(QtCore.QRect(50, 70, 261, 16))
        self.ModeLabel.setObjectName("ModeLabel")
        self.horizontalLayoutWidget = QtWidgets.QWidget(SequenceEditDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(40, 460, 631, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.GenerateSeq = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.GenerateSeq.setDefault(True)
        self.GenerateSeq.setObjectName("GenerateSeq")
        self.horizontalLayout.addWidget(self.GenerateSeq)
        self.Cancel = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.Cancel.setAutoDefault(True)
        self.Cancel.setObjectName("Cancel")
        self.horizontalLayout.addWidget(self.Cancel)
        self.BaseSeqName = QtWidgets.QLabel(SequenceEditDialog)
        self.BaseSeqName.setGeometry(QtCore.QRect(170, 30, 511, 16))
        self.BaseSeqName.setObjectName("BaseSeqName")

        self.retranslateUi(SequenceEditDialog)
        self.ModeTab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(SequenceEditDialog)

    def retranslateUi(self, SequenceEditDialog):
        _translate = QtCore.QCoreApplication.translate
        SequenceEditDialog.setWindowTitle(_translate("SequenceEditDialog", "Edit Sequences"))
        self.label_tab1.setText(_translate("SequenceEditDialog", "Please select donor sequences, multiple selection is allowed"))
        self.ModeTab.setTabText(self.ModeTab.indexOf(self.tab), _translate("SequenceEditDialog", "Base Biased"))
        self.label_tab2.setText(_translate("SequenceEditDialog", "Please select donor sequence, only single selection allowed"))
        self.radioButton_all.setText(_translate("SequenceEditDialog", "All possible combinations"))
        self.radioButton_single.setText(_translate("SequenceEditDialog", "Only single muitations"))
        self.ModeTab.setTabText(self.ModeTab.indexOf(self.tab_2), _translate("SequenceEditDialog", "Cocktail"))
        self.BaseSeqLabel.setText(_translate("SequenceEditDialog", "Base Sequence"))
        self.ModeLabel.setText(_translate("SequenceEditDialog", "Please choose sequence editing mode:"))
        self.GenerateSeq.setText(_translate("SequenceEditDialog", "Genearate Sequences"))
        self.Cancel.setText(_translate("SequenceEditDialog", "Cancel"))
        self.BaseSeqName.setText(_translate("SequenceEditDialog", "Base Sequence"))


