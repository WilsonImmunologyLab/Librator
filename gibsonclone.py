# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gibsonclone.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_gibsoncloneDialog(object):
    def setupUi(self, gibsoncloneDialog):
        gibsoncloneDialog.setObjectName("gibsoncloneDialog")
        gibsoncloneDialog.resize(688, 641)
        self.label = QtWidgets.QLabel(gibsoncloneDialog)
        self.label.setGeometry(QtCore.QRect(120, 20, 451, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(gibsoncloneDialog)
        self.label_2.setGeometry(QtCore.QRect(50, 60, 131, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(gibsoncloneDialog)
        self.label_3.setGeometry(QtCore.QRect(50, 270, 581, 21))
        self.label_3.setObjectName("label_3")
        self.jointUP = QtWidgets.QTextEdit(gibsoncloneDialog)
        self.jointUP.setGeometry(QtCore.QRect(50, 300, 581, 51))
        self.jointUP.setObjectName("jointUP")
        self.jointDOWN = QtWidgets.QTextEdit(gibsoncloneDialog)
        self.jointDOWN.setGeometry(QtCore.QRect(50, 390, 581, 51))
        self.jointDOWN.setObjectName("jointDOWN")
        self.label_4 = QtWidgets.QLabel(gibsoncloneDialog)
        self.label_4.setGeometry(QtCore.QRect(50, 520, 581, 21))
        self.label_4.setObjectName("label_4")
        self.outpath = QtWidgets.QLineEdit(gibsoncloneDialog)
        self.outpath.setGeometry(QtCore.QRect(50, 550, 491, 31))
        self.outpath.setObjectName("outpath")
        self.browse = QtWidgets.QPushButton(gibsoncloneDialog)
        self.browse.setGeometry(QtCore.QRect(540, 550, 91, 31))
        self.browse.setObjectName("browse")
        self.horizontalLayoutWidget = QtWidgets.QWidget(gibsoncloneDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(50, 590, 581, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.yes = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.yes.setDefault(True)
        self.yes.setObjectName("yes")
        self.horizontalLayout.addWidget(self.yes)
        self.cancel = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.cancel.setObjectName("cancel")
        self.horizontalLayout.addWidget(self.cancel)
        self.label_5 = QtWidgets.QLabel(gibsoncloneDialog)
        self.label_5.setGeometry(QtCore.QRect(50, 360, 581, 21))
        self.label_5.setObjectName("label_5")
        self.selection = QtWidgets.QListWidget(gibsoncloneDialog)
        self.selection.setGeometry(QtCore.QRect(50, 80, 581, 181))
        self.selection.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.selection.setObjectName("selection")
        self.label_6 = QtWidgets.QLabel(gibsoncloneDialog)
        self.label_6.setGeometry(QtCore.QRect(50, 450, 581, 21))
        self.label_6.setObjectName("label_6")
        self.dbpath = QtWidgets.QLineEdit(gibsoncloneDialog)
        self.dbpath.setGeometry(QtCore.QRect(50, 480, 411, 31))
        self.dbpath.setObjectName("dbpath")
        self.browseDB = QtWidgets.QPushButton(gibsoncloneDialog)
        self.browseDB.setGeometry(QtCore.QRect(540, 480, 91, 31))
        self.browseDB.setObjectName("browseDB")
        self.createDB = QtWidgets.QPushButton(gibsoncloneDialog)
        self.createDB.setGeometry(QtCore.QRect(460, 480, 91, 31))
        self.createDB.setObjectName("createDB")

        self.retranslateUi(gibsoncloneDialog)
        QtCore.QMetaObject.connectSlotsByName(gibsoncloneDialog)

    def retranslateUi(self, gibsoncloneDialog):
        _translate = QtCore.QCoreApplication.translate
        gibsoncloneDialog.setWindowTitle(_translate("gibsoncloneDialog", "Gibson Clone Fragments Design"))
        self.label.setText(_translate("gibsoncloneDialog", "Welcome to Gibson Clone Fragment Desgin page!"))
        self.label_2.setText(_translate("gibsoncloneDialog", "Your selections:"))
        self.label_3.setText(_translate("gibsoncloneDialog", "Joint region for upstream end  (Gibson cloning into the vector):"))
        self.label_4.setText(_translate("gibsoncloneDialog", "Gibson clone fragments files output path:"))
        self.browse.setText(_translate("gibsoncloneDialog", "Browse"))
        self.yes.setText(_translate("gibsoncloneDialog", "Generate Fragments"))
        self.cancel.setText(_translate("gibsoncloneDialog", "Cancel"))
        self.label_5.setText(_translate("gibsoncloneDialog", "Joint region for 3\' end  (instead of transmembrane region):"))
        self.label_6.setText(_translate("gibsoncloneDialog", "Fragments Database:"))
        self.browseDB.setText(_translate("gibsoncloneDialog", "Browse"))
        self.createDB.setText(_translate("gibsoncloneDialog", "Create"))


