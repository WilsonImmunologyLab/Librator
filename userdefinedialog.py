# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'userdefinedialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UserDefineDialog(object):
    def setupUi(self, UserDefineDialog):
        UserDefineDialog.setObjectName("UserDefineDialog")
        UserDefineDialog.resize(601, 332)
        self.gridLayout_2 = QtWidgets.QGridLayout(UserDefineDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButtonCancel = QtWidgets.QPushButton(UserDefineDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.gridLayout_2.addWidget(self.pushButtonCancel, 4, 2, 1, 1)
        self.pushButtonSave = QtWidgets.QPushButton(UserDefineDialog)
        self.pushButtonSave.setDefault(True)
        self.pushButtonSave.setObjectName("pushButtonSave")
        self.gridLayout_2.addWidget(self.pushButtonSave, 4, 1, 1, 1)
        self.frame_3 = QtWidgets.QFrame(UserDefineDialog)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        self.label_2.setObjectName("label_2")
        self.gridLayout_4.addWidget(self.label_2, 0, 0, 1, 1)
        self.lineEditH1 = QtWidgets.QLineEdit(self.frame_3)
        self.lineEditH1.setObjectName("lineEditH1")
        self.gridLayout_4.addWidget(self.lineEditH1, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        self.label_3.setObjectName("label_3")
        self.gridLayout_4.addWidget(self.label_3, 1, 0, 1, 1)
        self.lineEditH3 = QtWidgets.QLineEdit(self.frame_3)
        self.lineEditH3.setObjectName("lineEditH3")
        self.gridLayout_4.addWidget(self.lineEditH3, 1, 1, 1, 1)
        self.gridLayout_2.addWidget(self.frame_3, 2, 0, 1, 3)
        self.frame_2 = QtWidgets.QFrame(UserDefineDialog)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_4 = QtWidgets.QLabel(self.frame_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 1, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.frame_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 2, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame_2, 1, 0, 1, 3)
        self.frame = QtWidgets.QFrame(UserDefineDialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 3)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 3, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 4, 0, 1, 1)

        self.retranslateUi(UserDefineDialog)
        QtCore.QMetaObject.connectSlotsByName(UserDefineDialog)

    def retranslateUi(self, UserDefineDialog):
        _translate = QtCore.QCoreApplication.translate
        UserDefineDialog.setWindowTitle(_translate("UserDefineDialog", "Dialog"))
        self.pushButtonCancel.setText(_translate("UserDefineDialog", "Cancel"))
        self.pushButtonSave.setText(_translate("UserDefineDialog", "Save"))
        self.label_2.setText(_translate("UserDefineDialog", "H1 epitopes:"))
        self.label_3.setText(_translate("UserDefineDialog", "H3 epitopes:"))
        self.label_4.setText(_translate("UserDefineDialog", "Note: your epitopes can not be redudant with LateralPatch sites!"))
        self.label_5.setText(_translate("UserDefineDialog", "H3 LateralPatch:119,129,165,166,169,171,173"))
        self.label_6.setText(_translate("UserDefineDialog", "H1 LateralPatch:121,131,168,169,172,174,176"))
        self.label.setText(_translate("UserDefineDialog", "Define your own epitopes"))
