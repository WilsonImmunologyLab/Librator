# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gibsonclone.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_gibsoncloneDialog(object):
    def setupUi(self, gibsoncloneDialog):
        gibsoncloneDialog.setObjectName("gibsoncloneDialog")
        gibsoncloneDialog.resize(718, 974)
        self.gridLayout_6 = QtWidgets.QGridLayout(gibsoncloneDialog)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label = QtWidgets.QLabel(gibsoncloneDialog)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_6.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(gibsoncloneDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout_6.addWidget(self.label_2, 1, 0, 1, 1)
        self.selection = QtWidgets.QListWidget(gibsoncloneDialog)
        self.selection.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.selection.setObjectName("selection")
        self.gridLayout_6.addWidget(self.selection, 2, 0, 1, 3)
        self.label_3 = QtWidgets.QLabel(gibsoncloneDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout_6.addWidget(self.label_3, 3, 0, 1, 1)
        self.jointUP = QtWidgets.QTextEdit(gibsoncloneDialog)
        self.jointUP.setMaximumSize(QtCore.QSize(16777215, 30))
        self.jointUP.setObjectName("jointUP")
        self.gridLayout_6.addWidget(self.jointUP, 4, 0, 1, 3)
        self.label_5 = QtWidgets.QLabel(gibsoncloneDialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout_6.addWidget(self.label_5, 5, 0, 1, 1)
        self.jointDOWN = QtWidgets.QTextEdit(gibsoncloneDialog)
        self.jointDOWN.setMaximumSize(QtCore.QSize(16777215, 30))
        self.jointDOWN.setObjectName("jointDOWN")
        self.gridLayout_6.addWidget(self.jointDOWN, 6, 0, 1, 3)
        self.label_6 = QtWidgets.QLabel(gibsoncloneDialog)
        self.label_6.setObjectName("label_6")
        self.gridLayout_6.addWidget(self.label_6, 7, 0, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(gibsoncloneDialog)
        self.tabWidget.setMaximumSize(QtCore.QSize(16777215, 120))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.dbpath = QtWidgets.QLineEdit(self.tab)
        self.dbpath.setObjectName("dbpath")
        self.gridLayout_2.addWidget(self.dbpath, 0, 0, 1, 1)
        self.createDB = QtWidgets.QPushButton(self.tab)
        self.createDB.setObjectName("createDB")
        self.gridLayout_2.addWidget(self.createDB, 0, 1, 1, 1)
        self.browseDB = QtWidgets.QPushButton(self.tab)
        self.browseDB.setObjectName("browseDB")
        self.gridLayout_2.addWidget(self.browseDB, 0, 2, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_9 = QtWidgets.QLabel(self.tab_2)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 0, 5, 1, 1)
        self.DBnameinput = QtWidgets.QLineEdit(self.tab_2)
        self.DBnameinput.setObjectName("DBnameinput")
        self.gridLayout_3.addWidget(self.DBnameinput, 0, 6, 1, 1)
        self.Userinput = QtWidgets.QLineEdit(self.tab_2)
        self.Userinput.setObjectName("Userinput")
        self.gridLayout_3.addWidget(self.Userinput, 1, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.tab_2)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 1, 0, 1, 1)
        self.Portinput = QtWidgets.QLineEdit(self.tab_2)
        self.Portinput.setObjectName("Portinput")
        self.gridLayout_3.addWidget(self.Portinput, 0, 3, 1, 2)
        self.label_10 = QtWidgets.QLabel(self.tab_2)
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 1, 2, 1, 2)
        self.label_7 = QtWidgets.QLabel(self.tab_2)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)
        self.Passinput = QtWidgets.QLineEdit(self.tab_2)
        self.Passinput.setObjectName("Passinput")
        self.gridLayout_3.addWidget(self.Passinput, 1, 4, 1, 3)
        self.label_11 = QtWidgets.QLabel(self.tab_2)
        self.label_11.setObjectName("label_11")
        self.gridLayout_3.addWidget(self.label_11, 0, 2, 1, 1)
        self.IPinput = QtWidgets.QLineEdit(self.tab_2)
        self.IPinput.setObjectName("IPinput")
        self.gridLayout_3.addWidget(self.IPinput, 0, 1, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout_6.addWidget(self.tabWidget, 8, 0, 1, 3)
        self.label_4 = QtWidgets.QLabel(gibsoncloneDialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout_6.addWidget(self.label_4, 9, 0, 1, 1)
        self.outpath = QtWidgets.QLineEdit(gibsoncloneDialog)
        self.outpath.setObjectName("outpath")
        self.gridLayout_6.addWidget(self.outpath, 10, 0, 1, 2)
        self.browse = QtWidgets.QPushButton(gibsoncloneDialog)
        self.browse.setObjectName("browse")
        self.gridLayout_6.addWidget(self.browse, 10, 2, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(gibsoncloneDialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.radioButtonH1 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButtonH1.setChecked(True)
        self.radioButtonH1.setObjectName("radioButtonH1")
        self.gridLayout_5.addWidget(self.radioButtonH1, 0, 0, 1, 1)
        self.radioButtonH3 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButtonH3.setObjectName("radioButtonH3")
        self.gridLayout_5.addWidget(self.radioButtonH3, 0, 1, 1, 1)
        self.radioButtonNA = QtWidgets.QRadioButton(self.groupBox)
        self.radioButtonNA.setObjectName("radioButtonNA")
        self.gridLayout_5.addWidget(self.radioButtonNA, 0, 2, 1, 1)
        self.gridLayout_6.addWidget(self.groupBox, 11, 0, 1, 3)
        self.groupBox_2 = QtWidgets.QGroupBox(gibsoncloneDialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.radioButtonDefault = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButtonDefault.setChecked(True)
        self.radioButtonDefault.setObjectName("radioButtonDefault")
        self.gridLayout_4.addWidget(self.radioButtonDefault, 0, 0, 1, 1)
        self.radioButtonUser = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButtonUser.setObjectName("radioButtonUser")
        self.gridLayout_4.addWidget(self.radioButtonUser, 0, 1, 1, 1)
        self.gridLayout_6.addWidget(self.groupBox_2, 12, 0, 1, 3)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.F2_start = QtWidgets.QLineEdit(gibsoncloneDialog)
        self.F2_start.setReadOnly(True)
        self.F2_start.setObjectName("F2_start")
        self.gridLayout.addWidget(self.F2_start, 0, 5, 1, 1)
        self.F1_end = QtWidgets.QLineEdit(gibsoncloneDialog)
        self.F1_end.setReadOnly(True)
        self.F1_end.setObjectName("F1_end")
        self.gridLayout.addWidget(self.F1_end, 0, 3, 1, 1)
        self.label_18 = QtWidgets.QLabel(gibsoncloneDialog)
        self.label_18.setObjectName("label_18")
        self.gridLayout.addWidget(self.label_18, 2, 2, 1, 1)
        self.label_14 = QtWidgets.QLabel(gibsoncloneDialog)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 2, 0, 1, 1)
        self.label_19 = QtWidgets.QLabel(gibsoncloneDialog)
        self.label_19.setObjectName("label_19")
        self.gridLayout.addWidget(self.label_19, 0, 6, 1, 1)
        self.F3_start = QtWidgets.QLineEdit(gibsoncloneDialog)
        self.F3_start.setReadOnly(True)
        self.F3_start.setObjectName("F3_start")
        self.gridLayout.addWidget(self.F3_start, 2, 1, 1, 1)
        self.F4_start = QtWidgets.QLineEdit(gibsoncloneDialog)
        self.F4_start.setReadOnly(True)
        self.F4_start.setObjectName("F4_start")
        self.gridLayout.addWidget(self.F4_start, 2, 5, 1, 1)
        self.label_16 = QtWidgets.QLabel(gibsoncloneDialog)
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 2, 4, 1, 1)
        self.F1_start = QtWidgets.QLineEdit(gibsoncloneDialog)
        self.F1_start.setReadOnly(True)
        self.F1_start.setObjectName("F1_start")
        self.gridLayout.addWidget(self.F1_start, 0, 1, 1, 1)
        self.label_17 = QtWidgets.QLabel(gibsoncloneDialog)
        self.label_17.setObjectName("label_17")
        self.gridLayout.addWidget(self.label_17, 0, 2, 1, 1)
        self.label_20 = QtWidgets.QLabel(gibsoncloneDialog)
        self.label_20.setObjectName("label_20")
        self.gridLayout.addWidget(self.label_20, 2, 6, 1, 1)
        self.label_13 = QtWidgets.QLabel(gibsoncloneDialog)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 0, 0, 1, 1)
        self.label_15 = QtWidgets.QLabel(gibsoncloneDialog)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 0, 4, 1, 1)
        self.F3_end = QtWidgets.QLineEdit(gibsoncloneDialog)
        self.F3_end.setReadOnly(True)
        self.F3_end.setObjectName("F3_end")
        self.gridLayout.addWidget(self.F3_end, 2, 3, 1, 1)
        self.F2_end = QtWidgets.QLineEdit(gibsoncloneDialog)
        self.F2_end.setReadOnly(True)
        self.F2_end.setObjectName("F2_end")
        self.gridLayout.addWidget(self.F2_end, 0, 7, 1, 1)
        self.F4_end = QtWidgets.QLineEdit(gibsoncloneDialog)
        self.F4_end.setReadOnly(True)
        self.F4_end.setObjectName("F4_end")
        self.gridLayout.addWidget(self.F4_end, 2, 7, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout, 13, 0, 1, 3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.yes = QtWidgets.QPushButton(gibsoncloneDialog)
        self.yes.setDefault(True)
        self.yes.setObjectName("yes")
        self.horizontalLayout.addWidget(self.yes)
        self.cancel = QtWidgets.QPushButton(gibsoncloneDialog)
        self.cancel.setObjectName("cancel")
        self.horizontalLayout.addWidget(self.cancel)
        self.gridLayout_6.addLayout(self.horizontalLayout, 14, 1, 1, 2)

        self.retranslateUi(gibsoncloneDialog)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(gibsoncloneDialog)

    def retranslateUi(self, gibsoncloneDialog):
        _translate = QtCore.QCoreApplication.translate
        gibsoncloneDialog.setWindowTitle(_translate("gibsoncloneDialog", "Gibson Clone Fragments Design"))
        self.label.setText(_translate("gibsoncloneDialog", "Welcome to Gibson Clone Fragment Desgin page!"))
        self.label_2.setText(_translate("gibsoncloneDialog", "Your selections:"))
        self.label_3.setText(_translate("gibsoncloneDialog", "Joint region for upstream end  (Gibson cloning into the vector):"))
        self.label_5.setText(_translate("gibsoncloneDialog", "Joint region for 3\' end  (instead of transmembrane region):"))
        self.label_6.setText(_translate("gibsoncloneDialog", "Fragments Database:"))
        self.createDB.setText(_translate("gibsoncloneDialog", "Create"))
        self.browseDB.setText(_translate("gibsoncloneDialog", "Browse"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("gibsoncloneDialog", "Loacl DB"))
        self.label_9.setText(_translate("gibsoncloneDialog", "DB name"))
        self.label_8.setText(_translate("gibsoncloneDialog", "User Name"))
        self.label_10.setText(_translate("gibsoncloneDialog", "Password"))
        self.label_7.setText(_translate("gibsoncloneDialog", "Server IP"))
        self.label_11.setText(_translate("gibsoncloneDialog", "Port"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("gibsoncloneDialog", "Remote DB"))
        self.label_4.setText(_translate("gibsoncloneDialog", "Gibson clone fragments files output path:"))
        self.browse.setText(_translate("gibsoncloneDialog", "Browse"))
        self.groupBox.setTitle(_translate("gibsoncloneDialog", "Subtype"))
        self.radioButtonH1.setText(_translate("gibsoncloneDialog", "H1/Group1"))
        self.radioButtonH3.setText(_translate("gibsoncloneDialog", "H3/Group2"))
        self.radioButtonNA.setText(_translate("gibsoncloneDialog", "NA"))
        self.groupBox_2.setTitle(_translate("gibsoncloneDialog", "Joint Region Design"))
        self.radioButtonDefault.setText(_translate("gibsoncloneDialog", "Default"))
        self.radioButtonUser.setText(_translate("gibsoncloneDialog", "User Defined"))
        self.label_18.setText(_translate("gibsoncloneDialog", "to"))
        self.label_14.setText(_translate("gibsoncloneDialog", "Fragment 3"))
        self.label_19.setText(_translate("gibsoncloneDialog", "to"))
        self.label_16.setText(_translate("gibsoncloneDialog", "Fragment 4"))
        self.label_17.setText(_translate("gibsoncloneDialog", "to"))
        self.label_20.setText(_translate("gibsoncloneDialog", "to"))
        self.label_13.setText(_translate("gibsoncloneDialog", "Fragment 1"))
        self.label_15.setText(_translate("gibsoncloneDialog", "Fragment 2"))
        self.yes.setText(_translate("gibsoncloneDialog", "Generate Fragments"))
        self.cancel.setText(_translate("gibsoncloneDialog", "Cancel"))
