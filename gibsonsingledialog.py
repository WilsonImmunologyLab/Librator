# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gibsonsingledialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GibsonSingleDialog(object):
    def setupUi(self, GibsonSingleDialog):
        GibsonSingleDialog.setObjectName("GibsonSingleDialog")
        GibsonSingleDialog.resize(1118, 819)
        self.gridLayout_10 = QtWidgets.QGridLayout(GibsonSingleDialog)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.groupBox = QtWidgets.QGroupBox(GibsonSingleDialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.frame_4 = QtWidgets.QFrame(self.groupBox)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame_4)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_5 = QtWidgets.QLabel(self.frame_4)
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 0, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.frame_4)
        self.label_6.setObjectName("label_6")
        self.gridLayout_4.addWidget(self.label_6, 0, 2, 1, 1)
        self.jointUP = QtWidgets.QLineEdit(self.frame_4)
        self.jointUP.setObjectName("jointUP")
        self.gridLayout_4.addWidget(self.jointUP, 0, 1, 1, 1)
        self.jointDOWN = QtWidgets.QLineEdit(self.frame_4)
        self.jointDOWN.setObjectName("jointDOWN")
        self.gridLayout_4.addWidget(self.jointDOWN, 0, 3, 1, 1)
        self.gridLayout_5.addWidget(self.frame_4, 0, 0, 1, 2)
        self.frame_3 = QtWidgets.QFrame(self.groupBox)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.pushButtonBrowse = QtWidgets.QPushButton(self.frame_3)
        self.pushButtonBrowse.setObjectName("pushButtonBrowse")
        self.gridLayout_6.addWidget(self.pushButtonBrowse, 0, 2, 1, 1)
        self.outpath = QtWidgets.QLineEdit(self.frame_3)
        self.outpath.setObjectName("outpath")
        self.gridLayout_6.addWidget(self.outpath, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        self.label_3.setObjectName("label_3")
        self.gridLayout_6.addWidget(self.label_3, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.frame_3, 1, 0, 1, 2)
        self.gridLayout_10.addWidget(self.groupBox, 3, 0, 1, 3)
        self.pushButtonCancel = QtWidgets.QPushButton(GibsonSingleDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.gridLayout_10.addWidget(self.pushButtonCancel, 4, 1, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.textEdit = QtWidgets.QTextEdit(GibsonSingleDialog)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout_2.addWidget(self.textEdit)
        self.pushButtonGenerate = QtWidgets.QPushButton(GibsonSingleDialog)
        self.pushButtonGenerate.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButtonGenerate.setObjectName("pushButtonGenerate")
        self.horizontalLayout_2.addWidget(self.pushButtonGenerate)
        self.gridLayout_10.addLayout(self.horizontalLayout_2, 2, 0, 1, 3)
        self.pushButtonConfirm = QtWidgets.QPushButton(GibsonSingleDialog)
        self.pushButtonConfirm.setAutoDefault(False)
        self.pushButtonConfirm.setDefault(True)
        self.pushButtonConfirm.setObjectName("pushButtonConfirm")
        self.gridLayout_10.addWidget(self.pushButtonConfirm, 4, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(915, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_10.addItem(spacerItem, 4, 0, 1, 1)
        self.frame = QtWidgets.QFrame(GibsonSingleDialog)
        self.frame.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.gridLayout_10.addWidget(self.frame, 0, 0, 1, 3)
        self.frame_2 = QtWidgets.QFrame(GibsonSingleDialog)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 200))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setMaximumSize(QtCore.QSize(300, 16777215))
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 2)
        self.frame_5 = QtWidgets.QFrame(self.frame_2)
        self.frame_5.setMinimumSize(QtCore.QSize(0, 200))
        self.frame_5.setMaximumSize(QtCore.QSize(16777215, 200))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_5)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayoutSeq = QtWidgets.QGridLayout()
        self.gridLayoutSeq.setObjectName("gridLayoutSeq")
        self.gridLayout_2.addLayout(self.gridLayoutSeq, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.frame_5, 1, 0, 1, 5)
        self.clear = QtWidgets.QPushButton(self.frame_2)
        self.clear.setObjectName("clear")
        self.gridLayout_3.addWidget(self.clear, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(628, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 2, 1, 1, 2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.spinBoxStart = QtWidgets.QSpinBox(self.frame_2)
        self.spinBoxStart.setMinimumSize(QtCore.QSize(80, 0))
        self.spinBoxStart.setMaximum(9999)
        self.spinBoxStart.setObjectName("spinBoxStart")
        self.horizontalLayout_3.addWidget(self.spinBoxStart)
        self.spinBoxEnd = QtWidgets.QSpinBox(self.frame_2)
        self.spinBoxEnd.setMinimumSize(QtCore.QSize(80, 0))
        self.spinBoxEnd.setMaximum(9999)
        self.spinBoxEnd.setObjectName("spinBoxEnd")
        self.horizontalLayout_3.addWidget(self.spinBoxEnd)
        self.gridLayout_3.addLayout(self.horizontalLayout_3, 2, 3, 1, 1)
        self.pushButtonAdd = QtWidgets.QPushButton(self.frame_2)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.gridLayout_3.addWidget(self.pushButtonAdd, 2, 4, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.frame_2)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout_3.addWidget(self.comboBox, 0, 2, 1, 3)
        self.gridLayout_10.addWidget(self.frame_2, 1, 0, 1, 3)

        self.retranslateUi(GibsonSingleDialog)
        QtCore.QMetaObject.connectSlotsByName(GibsonSingleDialog)

    def retranslateUi(self, GibsonSingleDialog):
        _translate = QtCore.QCoreApplication.translate
        GibsonSingleDialog.setWindowTitle(_translate("GibsonSingleDialog", "Gibson Clone fragments design"))
        self.groupBox.setTitle(_translate("GibsonSingleDialog", "Settings"))
        self.label_5.setText(_translate("GibsonSingleDialog", "Upstream Connector "))
        self.label_6.setText(_translate("GibsonSingleDialog", "Downstream Connector "))
        self.pushButtonBrowse.setText(_translate("GibsonSingleDialog", "Browse"))
        self.label_3.setText(_translate("GibsonSingleDialog", "Output Path"))
        self.pushButtonCancel.setText(_translate("GibsonSingleDialog", "Cancel"))
        self.pushButtonGenerate.setText(_translate("GibsonSingleDialog", "Preview Gibson Clone Fragments"))
        self.pushButtonConfirm.setText(_translate("GibsonSingleDialog", "Confirm"))
        self.label_2.setText(_translate("GibsonSingleDialog", "Design Gibson Clone fragments for your sequence"))
        self.label.setText(_translate("GibsonSingleDialog", "Choose your target sequence:"))
        self.clear.setText(_translate("GibsonSingleDialog", "Clear"))
        self.pushButtonAdd.setText(_translate("GibsonSingleDialog", "Add Joint"))
