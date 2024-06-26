# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'userepitopedialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UserEpitopeDialog(object):
    def setupUi(self, UserEpitopeDialog):
        UserEpitopeDialog.setObjectName("UserEpitopeDialog")
        UserEpitopeDialog.resize(896, 721)
        self.gridLayout_4 = QtWidgets.QGridLayout(UserEpitopeDialog)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_2 = QtWidgets.QLabel(UserEpitopeDialog)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_4.addWidget(self.label_2, 1, 0, 1, 1)
        self.frame = QtWidgets.QFrame(UserEpitopeDialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.frame, 0, 0, 1, 4)
        self.comboBox = QtWidgets.QComboBox(UserEpitopeDialog)
        self.comboBox.setMinimumSize(QtCore.QSize(100, 0))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout_4.addWidget(self.comboBox, 1, 1, 1, 1)
        self.toolBox = QtWidgets.QToolBox(UserEpitopeDialog)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.toolBox.setFont(font)
        self.toolBox.setObjectName("toolBox")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 872, 524))
        self.page.setObjectName("page")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.page)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButtonSaveGroup = QtWidgets.QPushButton(self.page)
        self.pushButtonSaveGroup.setObjectName("pushButtonSaveGroup")
        self.gridLayout_2.addWidget(self.pushButtonSaveGroup, 1, 2, 1, 1)
        self.tableWidgetGroup = QtWidgets.QTableWidget(self.page)
        self.tableWidgetGroup.setObjectName("tableWidgetGroup")
        self.tableWidgetGroup.setColumnCount(0)
        self.tableWidgetGroup.setRowCount(0)
        self.gridLayout_2.addWidget(self.tableWidgetGroup, 0, 0, 1, 3)
        spacerItem = QtWidgets.QSpacerItem(662, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.toolBox.addItem(self.page, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 872, 524))
        self.page_2.setObjectName("page_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.page_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButtonSaveResidue = QtWidgets.QPushButton(self.page_2)
        self.pushButtonSaveResidue.setObjectName("pushButtonSaveResidue")
        self.gridLayout_3.addWidget(self.pushButtonSaveResidue, 1, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(636, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 1, 0, 1, 1)
        self.tableWidgetResidue = QtWidgets.QTableWidget(self.page_2)
        self.tableWidgetResidue.setObjectName("tableWidgetResidue")
        self.tableWidgetResidue.setColumnCount(0)
        self.tableWidgetResidue.setRowCount(0)
        self.gridLayout_3.addWidget(self.tableWidgetResidue, 0, 0, 1, 2)
        self.toolBox.addItem(self.page_2, "")
        self.gridLayout_4.addWidget(self.toolBox, 2, 0, 1, 4)
        self.pushButtonRestore = QtWidgets.QPushButton(UserEpitopeDialog)
        self.pushButtonRestore.setObjectName("pushButtonRestore")
        self.gridLayout_4.addWidget(self.pushButtonRestore, 1, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(496, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem2, 1, 3, 1, 1)

        self.retranslateUi(UserEpitopeDialog)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(UserEpitopeDialog)

    def retranslateUi(self, UserEpitopeDialog):
        _translate = QtCore.QCoreApplication.translate
        UserEpitopeDialog.setWindowTitle(_translate("UserEpitopeDialog", "Dialog"))
        self.label_2.setText(_translate("UserEpitopeDialog", "Numbering template:"))
        self.label.setText(_translate("UserEpitopeDialog", "Set up epitope annotation"))
        self.comboBox.setItemText(0, _translate("UserEpitopeDialog", "H1"))
        self.comboBox.setItemText(1, _translate("UserEpitopeDialog", "H3"))
        self.pushButtonSaveGroup.setText(_translate("UserEpitopeDialog", "Save group setting"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), _translate("UserEpitopeDialog", "Annotating groups (Click to show/hide content):"))
        self.pushButtonSaveResidue.setText(_translate("UserEpitopeDialog", "Save residue annotation"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), _translate("UserEpitopeDialog", "Annotating residues (Click to show/hide content):"))
        self.pushButtonRestore.setText(_translate("UserEpitopeDialog", "Restore Default Setting"))
