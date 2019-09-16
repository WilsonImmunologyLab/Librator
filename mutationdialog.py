# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mutationdialog.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MutationDialog(object):
    def setupUi(self, MutationDialog):
        MutationDialog.setObjectName("MutationDialog")
        MutationDialog.resize(538, 390)
        self.addMutation = QtWidgets.QPushButton(MutationDialog)
        self.addMutation.setGeometry(QtCore.QRect(30, 320, 301, 31))
        self.addMutation.setDefault(True)
        self.addMutation.setObjectName("addMutation")
        self.Title = QtWidgets.QLabel(MutationDialog)
        self.Title.setGeometry(QtCore.QRect(40, 20, 421, 31))
        self.Title.setObjectName("Title")
        self.CurSeq = QtWidgets.QLabel(MutationDialog)
        self.CurSeq.setGeometry(QtCore.QRect(40, 60, 421, 31))
        self.CurSeq.setObjectName("CurSeq")
        self.cancel = QtWidgets.QPushButton(MutationDialog)
        self.cancel.setGeometry(QtCore.QRect(360, 320, 121, 31))
        self.cancel.setObjectName("cancel")
        self.labelSeqName = QtWidgets.QLabel(MutationDialog)
        self.labelSeqName.setGeometry(QtCore.QRect(40, 280, 101, 16))
        self.labelSeqName.setObjectName("labelSeqName")
        self.tabWidget = QtWidgets.QTabWidget(MutationDialog)
        self.tabWidget.setGeometry(QtCore.QRect(40, 100, 471, 151))
        self.tabWidget.setObjectName("tabWidget")
        self.OriPos = QtWidgets.QWidget()
        self.OriPos.setObjectName("OriPos")
        self.Mutation = QtWidgets.QLineEdit(self.OriPos)
        self.Mutation.setGeometry(QtCore.QRect(120, 40, 311, 31))
        self.Mutation.setObjectName("Mutation")
        self.labelpos = QtWidgets.QLabel(self.OriPos)
        self.labelpos.setGeometry(QtCore.QRect(20, 50, 101, 16))
        self.labelpos.setObjectName("labelpos")
        self.tabWidget.addTab(self.OriPos, "")
        self.H1H3pos = QtWidgets.QWidget()
        self.H1H3pos.setObjectName("H1H3pos")
        self.labelHA1 = QtWidgets.QLabel(self.H1H3pos)
        self.labelHA1.setGeometry(QtCore.QRect(10, 30, 101, 16))
        self.labelHA1.setObjectName("labelHA1")
        self.labelHA2 = QtWidgets.QLabel(self.H1H3pos)
        self.labelHA2.setGeometry(QtCore.QRect(10, 80, 101, 16))
        self.labelHA2.setObjectName("labelHA2")
        self.HA2mutation = QtWidgets.QLineEdit(self.H1H3pos)
        self.HA2mutation.setGeometry(QtCore.QRect(120, 70, 311, 31))
        self.HA2mutation.setObjectName("HA2mutation")
        self.HA1mutation = QtWidgets.QLineEdit(self.H1H3pos)
        self.HA1mutation.setGeometry(QtCore.QRect(120, 20, 311, 31))
        self.HA1mutation.setObjectName("HA1mutation")
        self.tabWidget.addTab(self.H1H3pos, "")
        self.SeqName = QtWidgets.QLineEdit(MutationDialog)
        self.SeqName.setGeometry(QtCore.QRect(160, 270, 311, 31))
        self.SeqName.setObjectName("SeqName")

        self.retranslateUi(MutationDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MutationDialog)

    def retranslateUi(self, MutationDialog):
        _translate = QtCore.QCoreApplication.translate
        MutationDialog.setWindowTitle(_translate("MutationDialog", "Generate mutated sequence"))
        self.addMutation.setText(_translate("MutationDialog", "Create new sequence with your mutations"))
        self.Title.setText(_translate("MutationDialog", "Please type your mutations below: e.g. R98Y, K141E"))
        self.CurSeq.setText(_translate("MutationDialog", "Current Sequence: "))
        self.cancel.setText(_translate("MutationDialog", "Cancel"))
        self.labelSeqName.setText(_translate("MutationDialog", "New SEQ Name"))
        self.labelpos.setText(_translate("MutationDialog", "Mutations"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.OriPos), _translate("MutationDialog", "Original Position"))
        self.labelHA1.setText(_translate("MutationDialog", "HA1 mutations"))
        self.labelHA2.setText(_translate("MutationDialog", "HA2 mutations"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.H1H3pos), _translate("MutationDialog", "H1/H3 Numbering"))


