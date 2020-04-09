# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gibsonalignmentdialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GibsonMSADialog(object):
    def setupUi(self, GibsonMSADialog):
        GibsonMSADialog.setObjectName("GibsonMSADialog")
        GibsonMSADialog.resize(1353, 683)
        self.gridLayout_3 = QtWidgets.QGridLayout(GibsonMSADialog)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.frame = QtWidgets.QFrame(GibsonMSADialog)
        self.frame.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.frame, 0, 0, 1, 1)
        self.frame_2 = QtWidgets.QFrame(GibsonMSADialog)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayoutFragment = QtWidgets.QGridLayout()
        self.gridLayoutFragment.setObjectName("gridLayoutFragment")
        self.gridLayout_5.addLayout(self.gridLayoutFragment, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.frame_2, 1, 0, 1, 1)
        self.frame_3 = QtWidgets.QFrame(GibsonMSADialog)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(1124, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 0, 1, 1)
        self.cancelButton = QtWidgets.QPushButton(self.frame_3)
        self.cancelButton.setAutoDefault(False)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout_2.addWidget(self.cancelButton, 0, 1, 1, 1)
        self.confirmButton = QtWidgets.QPushButton(self.frame_3)
        self.confirmButton.setCheckable(True)
        self.confirmButton.setChecked(True)
        self.confirmButton.setAutoDefault(False)
        self.confirmButton.setDefault(True)
        self.confirmButton.setObjectName("confirmButton")
        self.gridLayout_2.addWidget(self.confirmButton, 0, 2, 1, 1)
        self.gridLayout_3.addWidget(self.frame_3, 2, 0, 1, 1)

        self.retranslateUi(GibsonMSADialog)
        QtCore.QMetaObject.connectSlotsByName(GibsonMSADialog)

    def retranslateUi(self, GibsonMSADialog):
        _translate = QtCore.QCoreApplication.translate
        GibsonMSADialog.setWindowTitle(_translate("GibsonMSADialog", "Review and Confirm all fragments"))
        self.label.setText(_translate("GibsonMSADialog", "Gibson Clone Fragments Preview"))
        self.cancelButton.setText(_translate("GibsonMSADialog", "Cancel"))
        self.confirmButton.setText(_translate("GibsonMSADialog", "Confirm"))
