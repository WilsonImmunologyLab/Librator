# Librator by Patrick Wilson
from PyQt5.QtCore import pyqtSlot, QTimer, QDateTime, Qt, QSortFilterProxyModel, QModelIndex, QEventLoop, pyqtSignal,\
	QEventLoop, QUrl, QSize
from PyQt5 import QtWidgets, QtPrintSupport, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtGui import QTextCursor, QFont, QPixmap, QTextCharFormat, QBrush, QColor, QCursor
from LibratorSQL import creatnewDB, enterData, RunSQL, UpdateField, deleterecords, RunInsertion, creatnewFragmentDB,\
	CopyDatatoDB2, RunMYSQL, RunMYSQLInsertion
from PyQt5.QtWebEngineWidgets import QWebEngineView
from pyecharts.charts import Bar, Pie, Line, Page, Grid
from pyecharts import options as opts

from HA_numbering_function import HA_numbering_Jesse
from itertools import combinations
from collections import Counter
from subprocess import call, Popen, PIPE
from platform import system
import os, sys, re, time, string, sip, csv
import pandas as pd
import numpy as np
import shutil

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
matplotlib.rcParams["font.sans-serif"] = ["Times New Roman"]
matplotlib.rcParams["font.size"] = 6
import seaborn as sns

from MainLibrator_UI import Ui_MainLibrator
from mutationdialog import Ui_MutationDialog
from sequenceedit import Ui_SequenceEditDialog
from gibsonclone import Ui_gibsoncloneDialog
from base_path_dialog import Ui_basePathDialog
from fusiondialog import Ui_fusionDialog
from updatesequencedialog import Ui_UpdateSequenceDialog
from deletedialog import Ui_deleteDialog
from treedialog import Ui_treeDialog
from gibsonalignmentdialog import Ui_GibsonMSADialog
from jointdialog import Ui_JointDialog
from htmldialog import Ui_htmlDialog

from LibDialogues import openFile, openFiles, newFile, saveFile, questionMessage, informationMessage, setItem, setText
from VgenesTextEdit import VGenesTextMain
from ui_VGenesTextEdit import ui_TextEditor
import LibratorSeq

global BaseSeq
BaseSeq = ''


global MoveNotChange
MoveNotChange = False
global SeqMove
SeqMove = False
global H1Numbering
global H3Numbering
global NumberingMap
H1Numbering = {}
H3Numbering = {}
NumberingMap = {}

global VGenesTextWindows
VGenesTextWindows = {}

global GLMsg
GLMsg = False

global DataIs
DataIs = []

global DBFilename
DBFilename = 'none'

# read configure information from file. If no conf file, initial conf path
global conf_file, ldb_file, joint_file
conf_file = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), '..', 'Resources', 'Conf', 'path_setting.txt')
ldb_file = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), '..', 'Resources', 'Conf', 'ldb_setting.txt')
joint_file = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), '..', 'Resources', 'Conf', 'joint_setting.txt')

global working_prefix
global temp_folder
global muscle_path
global clustal_path
global pymol_path
global raxml_path
global figtree_path
global fragmentdb_path

working_prefix = os.path.dirname(os.path.realpath(sys.argv[0])) + '/'
temp_folder = os.path.join(working_prefix, '..', 'Resources', 'Temp')

if os.path.exists(conf_file):   # if conf exist, read conf info from file
	file_handle = open(conf_file, 'r')
	settings = file_handle.readlines()
	muscle_path =  settings[0].strip('\n')
	clustal_path =  settings[1].strip('\n')
	pymol_path =  settings[2].strip('\n')
	raxml_path =  settings[3].strip('\n')
	figtree_path =  settings[4].strip('\n')
	file_handle.close()
	del settings
else:                           # if conf does not exist, initial conf info and write to file
	muscle_path = os.path.join(working_prefix, '..', 'Resources', 'Tools', 'muscle')
	clustal_path = os.path.join(working_prefix, '..', 'Resources', 'Tools', 'clustalo')
	pymol_path = '/usr/local/bin/pymol'
	raxml_path = os.path.join(working_prefix, '..', 'Resources', 'Tools', 'raxml')
	figtree_path = '/Applications/FigTree.app/Contents/MacOS/universalJavaApplicationStub'

	file_handle = open(conf_file, 'w')
	file_handle.write(muscle_path + '\n')
	file_handle.write(clustal_path + '\n')
	file_handle.write(pymol_path + '\n')
	file_handle.write(raxml_path + '\n')
	file_handle.write(figtree_path)
	file_handle.close()

if os.path.exists(ldb_file):   # if conf exist, read conf info from file
	file_handle = open(ldb_file, 'r')
	settings = file_handle.readlines()
	if len(settings) > 0:
		fragmentdb_path = settings[0].strip('\n')
	else:
		fragmentdb_path = ''
	file_handle.close()
else:
	fragmentdb_path = ''
	file_handle = open(ldb_file, 'w')
	file_handle.write(fragmentdb_path)
	file_handle.close()

global joint_up
global joint_down

if os.path.exists(joint_file):   # if conf exist, read conf info from file
	file_handle = open(joint_file, 'r')
	settings = file_handle.readlines()
	joint_up = settings[0].strip('\n')
	joint_down = settings[1].strip('\n')
	file_handle.close()
else:
	joint_up = "TCCACTCCCAGGTCCAACTGCACCTCGGTTCTATCGATTGAATTC"
	joint_down = "GGGTCCGGATACATACCAGAGGCCCCGCGAGATGG"
	file_handle = open(joint_file, 'w')
	file_handle.write(joint_up + '\n')
	file_handle.write(joint_down)
	file_handle.close()

class MyFigure(FigureCanvas):
    def __init__(self,width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(MyFigure,self).__init__(self.fig)
        self.axes = self.fig.add_subplot(111)

class ResizeWidget(QWebEngineView):
	resizeSignal = pyqtSignal(int,int)
	def __init__(self,parent=None):
		super(ResizeWidget,self).__init__()
		self.id = 0
		self.h = 0
		self.w = 0

	def resizeEvent(self, evt):
		#w = evt.oldSize().width()
		#h = evt.oldSize().height()
		#print(f' size before :{w,h}')
		w = evt.size().width()
		h = evt.size().height()
		self.h = h
		self.w = w
		print(f' size now :{w, h, self.id}')
		self.resizeSignal.emit(w,h)

class jointDialog(QtWidgets.QDialog):
	def __init__(self):
		super(jointDialog, self).__init__()
		self.ui = Ui_JointDialog()
		self.ui.setupUi(self)

		global H1_start, H1_end, H3_start, H3_end, NA_start, NA_end
		global H3_start_user, H3_end_user, H1_start_user, H1_end_user, NA_end_user, NA_start_user
		global H1_Gibson_file, H3_Gibson_file, NA_Gibson_file

		self.ui.H1_F1_S.setText(str(H1_start[0]))
		self.ui.H1_F2_S.setText(str(H1_start[1]))
		self.ui.H1_F3_S.setText(str(H1_start[2]))
		self.ui.H1_F4_S.setText(str(H1_start[3]))
		self.ui.H1_F1_E.setText(str(H1_end[0]))
		self.ui.H1_F2_E.setText(str(H1_end[1]))
		self.ui.H1_F3_E.setText(str(H1_end[2]))
		self.ui.H1_F4_E.setText(str(H1_end[3]))

		self.ui.H3_F1_S.setText(str(H3_start[0]))
		self.ui.H3_F2_S.setText(str(H3_start[1]))
		self.ui.H3_F3_S.setText(str(H3_start[2]))
		self.ui.H3_F4_S.setText(str(H3_start[3]))
		self.ui.H3_F1_E.setText(str(H3_end[0]))
		self.ui.H3_F2_E.setText(str(H3_end[1]))
		self.ui.H3_F3_E.setText(str(H3_end[2]))
		self.ui.H3_F4_E.setText(str(H3_end[3]))

		self.ui.NA_F1_S.setText(str(NA_start[0]))
		self.ui.NA_F2_S.setText(str(NA_start[1]))
		self.ui.NA_F3_S.setText(str(NA_start[2]))
		self.ui.NA_F1_E.setText(str(NA_end[0]))
		self.ui.NA_F2_E.setText(str(NA_end[1]))
		self.ui.NA_F3_E.setText(str(NA_end[2]))

		self.ui.saveButton.clicked.connect(self.accept)
		self.ui.cancelButton.clicked.connect(self.reject)
		self.ui.exitButton.clicked.connect(self.reject)

	def accept(self):
		global H1_start, H1_end, H3_start, H3_end, NA_start, NA_end
		global H3_start_user, H3_end_user, H1_start_user, H1_end_user, NA_end_user, NA_start_user
		global H1_Gibson_file, H3_Gibson_file, NA_Gibson_file

		if self.ui.H1_F1_SU.text() != '' and self.ui.H1_F1_EU.text() != '' and self.ui.H1_F2_SU.text() != '' and self.ui.H1_F2_EU.text() != '' and self.ui.H1_F3_SU.text() != '' and self.ui.H1_F3_EU.text() != '' and self.ui.H1_F4_SU.text() != '' and self.ui.H1_F4_EU.text() != '':
			H1_start_user = [int(self.ui.H1_F1_SU.text()), int(self.ui.H1_F2_SU.text()),
			                 int(self.ui.H1_F3_SU.text()), int(self.ui.H1_F4_SU.text())]
			H1_end_user = [int(self.ui.H1_F1_EU.text()), int(self.ui.H1_F2_EU.text()),
			               int(self.ui.H1_F3_EU.text()), int(self.ui.H1_F4_EU.text())]

			file_handle = open(H1_Gibson_file, 'w')
			text = ','.join(list(map(str, H1_start_user))) + '\n' + ','.join(list(map(str, H1_end_user)))
			file_handle.write(text)
			file_handle.close()

		if self.ui.H3_F1_SU.text() != '' and self.ui.H3_F1_EU.text() != '' and self.ui.H3_F2_SU.text() != '' and self.ui.H3_F2_EU.text() != '' and self.ui.H3_F3_SU.text() != '' and self.ui.H3_F3_EU.text() != '' and self.ui.H3_F4_SU.text() != '' and self.ui.H3_F4_EU.text() != '':
			H3_start_user = [int(self.ui.H3_F1_SU.text()), int(self.ui.H3_F2_SU.text()),
			                 int(self.ui.H3_F3_SU.text()), int(self.ui.H3_F4_SU.text())]
			H3_end_user = [int(self.ui.H3_F1_EU.text()), int(self.ui.H3_F2_EU.text()),
			               int(self.ui.H3_F3_EU.text()), int(self.ui.H3_F4_EU.text())]

			file_handle = open(H3_Gibson_file, 'w')
			text = ','.join(list(map(str, H3_start_user))) + '\n' + ','.join(list(map(str, H3_end_user)))
			file_handle.write(text)
			file_handle.close()

		if self.ui.NA_F1_SU.text() != '' and self.ui.NA_F1_EU.text() != '' and self.ui.NA_F2_SU.text() != '' and self.ui.NA_F2_EU.text() != '' and self.ui.NA_F3_SU.text() != '' and self.ui.NA_F3_EU.text() != '':
			NA_start_user = [int(self.ui.NA_F1_SU.text()), int(self.ui.NA_F2_SU.text()),
			                 int(self.ui.NA_F3_SU.text())]
			NA_end_user = [int(self.ui.NA_F1_EU.text()), int(self.ui.NA_F2_EU.text()),
			               int(self.ui.NA_F3_EU.text())]

			file_handle = open(NA_Gibson_file, 'w')
			text = ','.join(list(map(str, NA_start_user))) + '\n' + ','.join(list(map(str, NA_end_user)))
			file_handle.write(text)
			file_handle.close()

		self.close()

class treeDialog(QtWidgets.QDialog):
	treeSignal = pyqtSignal(list, str)
	def __init__(self):
		super(treeDialog, self).__init__()
		self.ui = Ui_treeDialog()
		self.ui.setupUi(self)

		self.ui.confirmButton.clicked.connect(self.accept)
		self.ui.cancelButton.clicked.connect(self.reject)

		self.ui.nameList.itemSelectionChanged.connect(self.highlightSeq)
		self.ui.startBox.valueChanged.connect(self.highlightRegion)
		self.ui.endBox.valueChanged.connect(self.highlightRegion)
		#self.ui.showButton.clicked.connect(self.highlightRegion)
		self.ui.seqEdit.cursorPositionChanged.connect(self.ruler)

	def ruler(self):
		cursor = self.ui.seqEdit.textCursor()
		StartP = cursor.selectionStart()
		EndP = cursor.selectionEnd()

		text = self.ui.seqEdit.toPlainText()
		tmp = re.findall(r"\n", text)
		LenSeq = int(len(text)/len(tmp)) - 1

		row_length = LenSeq + 1
		StartP = int(StartP%row_length)
		EndP = int(EndP % row_length)

		if StartP == EndP:
			lblText = 'Sequence: position = ' + str(EndP) + ' of ' + str(LenSeq) + ' BP'
		else:
			lblText = 'Sequence: ' + str(StartP + 1) + ' to ' + str(EndP) + ' (' + str(
				EndP - StartP) + ' bases) ' ' selected of ' + str(LenSeq) + ' BP'

		self.ui.lbl.setText(lblText)

	def highlightSeq(self):
		sel_seq = []
		for item in self.ui.nameList.selectedItems():
			sel_seq.append(item.text())

		color = []
		seq_len = len(self.seqs[0]) + 1
		for i in range(0,len(self.names)):
			if self.names[i] in sel_seq:
				color.append('7')
			else:
				color.append('0')
		self.DecorateSeq(color, seq_len)

	def highlightRegion(self):
		seq_len = len(self.seqs[0]) + 1
		start = self.ui.startBox.value()
		end = self.ui.endBox.value()

		if end > seq_len:
			end = seq_len
			self.ui.endBox.setValue(end)
		if start > seq_len:
			start = seq_len - 1
			self.ui.startBox.setValue(start)

		if start != 0 and end != 0:
			if end > start:
				num_len = len(self.seqs)
				self.DecorateRegion(start, end, seq_len, num_len)

	def accept(self):
		start = self.ui.startBox.value()
		end = self.ui.endBox.value()

		if start > end:
			self.ui.endBox.setValue(0)
			self.ui.startBox.setValue(0)
			Msg = 'Start posotion should be smaller than end position!'
			QMessageBox.warning(self, 'Warning', Msg, QMessageBox.Ok, QMessageBox.Ok)
			return

		if start == 0 and end == 0:
			end = 5000
		else:
			start = start - 1

		seq_list = []
		for i in range(0,len(self.names)):
			seq = self.seqs[i]
			seq = seq[start:end]
			seq_list.append([self.names[i],seq])

		self.treeSignal.emit(seq_list, self.path)
		self.close()

	def DecorateRegion(self, start, end, seq_len, num_len):
		cursor = self.ui.seqEdit.textCursor()
		CurPos = 0

		# Setup the desired format for matches
		format = QTextCharFormat()
		start = start - 1
		for i in range(0,num_len):  # QColor is RGB: 0-255, 0-255, 0-255
			if start > 0:
				format.setForeground(QBrush(QColor("black")))
				cursor.setPosition(CurPos)
				cursor.setPosition(CurPos + start, QTextCursor.KeepAnchor)
				cursor.mergeCharFormat(format)

			format.setForeground(QBrush(QColor("red")))
			cursor.setPosition(CurPos + start)
			cursor.setPosition(CurPos + end, QTextCursor.KeepAnchor)
			cursor.mergeCharFormat(format)

			if end < seq_len:
				format.setForeground(QBrush(QColor("black")))
				cursor.setPosition(CurPos + end)
				cursor.setPosition(CurPos + seq_len, QTextCursor.KeepAnchor)
				cursor.mergeCharFormat(format)

			CurPos += seq_len

	def DecorateSeq(self, ColorMap, Len):
		cursor = self.ui.seqEdit.textCursor()
		CurPos = 0

		# Setup the desired format for matches
		format = QTextCharFormat()

		for valueIs in ColorMap:  # QColor is RGB: 0-255, 0-255, 0-255
			if valueIs == '0':
				format.setBackground(QBrush(QColor("white")))
			elif valueIs == '7':
				format.setBackground(QBrush(QColor("lightGray")))

			cursor.setPosition(CurPos)
			cursor.setPosition(CurPos + Len, QTextCursor.KeepAnchor)
			cursor.mergeCharFormat(format)

			CurPos += Len

class GibsonMSADialog(QtWidgets.QDialog):
	gibson_msa_Signal = pyqtSignal(object, int, list, str, list, str, int)
	def __init__(self):
		super(GibsonMSADialog, self).__init__()
		self.ui = Ui_GibsonMSADialog()
		self.ui.setupUi(self)

		self.ui.confirmButton.clicked.connect(self.accept)
		self.ui.cancelButton.clicked.connect(self.reject)

		#self.ui.nameList.clicked.connect(self.highlightSeq)
		self.ui.nameList.itemSelectionChanged.connect(self.highlightSeq)

		self.ui.radioNT.clicked.connect(self.switchSeq)
		self.ui.radioAA.clicked.connect(self.switchSeq)

	def accept(self):
		self.gibson_msa_Signal.emit(self.fragment_data, self.mode, self.db_file, self.out_dir, self.joint, self.subtype, self.num_frag)
		self.close()

	def highlightSeq(self):
		sel_seq = []
		for item in self.ui.nameList.selectedItems():
			sel_seq.append(item.text())

		color = []
		names = self.names
		num_names = len(names)
		for item in self.names:
			if item in sel_seq:
				color.append('7')
			else:
				color.append('0')
		if self.ui.radioAA.isChecked():
			self.DecorateAASeq(color, self.len)
		else:
			self.DecorateNTSeq(color)

	def switchSeq(self):
		fragment_data = self.fragment_data
		if self.ui.radioAA.isChecked():
			seq_names = fragment_data['Name'].tolist()
			F1_seqs = fragment_data['F_AA_1_origin'].tolist()
			F2_seqs = fragment_data['F_AA_2_origin'].tolist()
			F3_seqs = fragment_data['F_AA_3_origin'].tolist()

			F1_seq_text = '\n'.join(F1_seqs) + '\n'
			F2_seq_text = '\n'.join(F2_seqs) + '\n'
			F3_seq_text = '\n'.join(F3_seqs) + '\n'

			self.ui.seqEditF1.setText(F1_seq_text)
			self.ui.seqEditF2.setText(F2_seq_text)
			self.ui.seqEditF3.setText(F3_seq_text)

			# color text for F1, F2, F3, F4
			num_seq = len(seq_names)
			format = QTextCharFormat()
			format_hyphen = QTextCharFormat()
			format_hyphen.setBackground(QBrush(QColor("red")))
			format_hyphen.setForeground(QBrush(QColor("white")))

			# F1
			cursor1 = self.ui.seqEditF1.textCursor()
			len_f1 = len(F1_seqs[0])
			CurPos = 0
			for i in range(0, num_seq):
				format.setForeground(QBrush(QColor("red")))
				cursor1.setPosition(CurPos + len_f1 - 9)
				cursor1.setPosition(CurPos + len_f1, QTextCursor.KeepAnchor)
				cursor1.mergeCharFormat(format)
				CurPos += len_f1 + 1

			text = self.ui.seqEditF1.toPlainText()
			list = [i.start() for i in re.finditer('-',text)]
			if len(list) > 0:
				for pos in list:
					cursor1.setPosition(pos)
					cursor1.setPosition(pos + 1, QTextCursor.KeepAnchor)
					cursor1.mergeCharFormat(format_hyphen)
			# F2
			cursor2 = self.ui.seqEditF2.textCursor()
			len_f2 = len(F2_seqs[0])
			CurPos = 0
			for i in range(0, num_seq):
				format.setForeground(QBrush(QColor("red")))
				cursor2.setPosition(CurPos + 0)
				cursor2.setPosition(CurPos + 9, QTextCursor.KeepAnchor)
				cursor2.mergeCharFormat(format)

				cursor2.setPosition(CurPos + len_f2 - 9)
				cursor2.setPosition(CurPos + len_f2, QTextCursor.KeepAnchor)
				cursor2.mergeCharFormat(format)
				CurPos += len_f2 + 1

			text = self.ui.seqEditF2.toPlainText()
			list = [i.start() for i in re.finditer('-', text)]
			if len(list) > 0:
				for pos in list:
					cursor2.setPosition(pos)
					cursor2.setPosition(pos + 1, QTextCursor.KeepAnchor)
					cursor2.mergeCharFormat(format_hyphen)
			# F3
			cursor3 = self.ui.seqEditF3.textCursor()
			len_f3 = len(F3_seqs[0])
			CurPos = 0
			for i in range(0, num_seq):
				format.setForeground(QBrush(QColor("red")))
				cursor3.setPosition(CurPos + 0)
				cursor3.setPosition(CurPos + 9, QTextCursor.KeepAnchor)
				cursor3.mergeCharFormat(format)

				if self.num_frag == 4:
					cursor3.setPosition(CurPos + len_f3 - 9)
					cursor3.setPosition(CurPos + len_f3, QTextCursor.KeepAnchor)
					cursor3.mergeCharFormat(format)
				CurPos += len_f3 + 1

			text = self.ui.seqEditF3.toPlainText()
			list = [i.start() for i in re.finditer('-', text)]
			if len(list) > 0:
				for pos in list:
					cursor3.setPosition(pos)
					cursor3.setPosition(pos + 1, QTextCursor.KeepAnchor)
					cursor3.mergeCharFormat(format_hyphen)

			if self.num_frag == 4:
				F4_seqs = fragment_data['F_AA_4_origin'].tolist()
				F4_seq_text = '\n'.join(F4_seqs) + '\n'
				self.ui.seqEditF4.setText(F4_seq_text)
				# F4
				cursor4 = self.ui.seqEditF4.textCursor()
				len_f4 = len(F4_seqs[0])
				CurPos = 0
				for i in range(0, num_seq):
					format.setForeground(QBrush(QColor("red")))
					cursor4.setPosition(CurPos + 0)
					cursor4.setPosition(CurPos + 9, QTextCursor.KeepAnchor)
					cursor4.mergeCharFormat(format)
					CurPos += len_f4 + 1

				text = self.ui.seqEditF4.toPlainText()
				list = [i.start() for i in re.finditer('-', text)]
				if len(list) > 0:
					for pos in list:
						cursor4.setPosition(pos)
						cursor4.setPosition(pos + 1, QTextCursor.KeepAnchor)
						cursor4.mergeCharFormat(format_hyphen)

			self.ui.notice.setText('"-" in sequences will be removed before generating Fragments')
		else:
			joint_up_str = '\n' + self.joint[0]
			joint_down_str = self.joint[1] + '\n'

			seq_names = fragment_data['Name'].tolist()
			F1_seqs = fragment_data['F_NT_1'].tolist()
			F2_seqs = fragment_data['F_NT_2'].tolist()
			F3_seqs = fragment_data['F_NT_3'].tolist()

			F1_seq_text = self.joint[0] + joint_up_str.join(F1_seqs) + '\n'
			F2_seq_text = '\n'.join(F2_seqs) + '\n'
			if self.num_frag == 4:
				F3_seq_text = '\n'.join(F3_seqs) + '\n'
			else:
				F3_seq_text = joint_down_str.join(F3_seqs) + joint_down_str

			self.ui.seqEditF1.setText(F1_seq_text)
			self.ui.seqEditF2.setText(F2_seq_text)
			self.ui.seqEditF3.setText(F3_seq_text)

			# color text for F1, F2, F3, F4
			num_seq = len(seq_names)
			format = QTextCharFormat()

			# F1
			cursor1 = self.ui.seqEditF1.textCursor()
			CurPos = 0
			for i in range(0, num_seq):
				cur_len = len(self.joint[0]) + len(F1_seqs[i])
				format.setForeground(QBrush(QColor("red")))
				cursor1.setPosition(CurPos + 0)
				cursor1.setPosition(CurPos + len(self.joint[0]), QTextCursor.KeepAnchor)
				cursor1.mergeCharFormat(format)

				cursor1.setPosition(CurPos + cur_len - 25)
				cursor1.setPosition(CurPos + cur_len, QTextCursor.KeepAnchor)
				cursor1.mergeCharFormat(format)
				CurPos += cur_len + 1

			# F2
			cursor2 = self.ui.seqEditF2.textCursor()
			CurPos = 0
			for i in range(0, num_seq):
				cur_len = len(F2_seqs[i])
				format.setForeground(QBrush(QColor("red")))
				cursor2.setPosition(CurPos + 0)
				cursor2.setPosition(CurPos + 25, QTextCursor.KeepAnchor)
				cursor2.mergeCharFormat(format)

				cursor2.setPosition(CurPos + cur_len - 25)
				cursor2.setPosition(CurPos + cur_len, QTextCursor.KeepAnchor)
				cursor2.mergeCharFormat(format)
				CurPos += cur_len + 1

			# F3
			cursor3 = self.ui.seqEditF3.textCursor()
			CurPos = 0
			for i in range(0, num_seq):
				format.setForeground(QBrush(QColor("red")))
				cursor3.setPosition(CurPos + 0)
				cursor3.setPosition(CurPos + 25, QTextCursor.KeepAnchor)
				cursor3.mergeCharFormat(format)

				if self.num_frag == 4:
					cur_len = len(F3_seqs[i])
					cursor3.setPosition(CurPos + cur_len - 25)
				else:
					cur_len = len(F3_seqs[i]) + len(self.joint[1])
					cursor3.setPosition(CurPos + cur_len - len(self.joint[1]))
				cursor3.setPosition(CurPos + cur_len, QTextCursor.KeepAnchor)
				cursor3.mergeCharFormat(format)
				CurPos += cur_len + 1

			if self.num_frag == 4:
				F4_seqs = fragment_data['F_NT_4'].tolist()
				F4_seq_text = joint_down_str.join(F4_seqs) + joint_down_str
				self.ui.seqEditF4.setText(F4_seq_text)

				# F4
				cursor4 = self.ui.seqEditF4.textCursor()
				CurPos = 0
				for i in range(0, num_seq):
					cur_len = len(F4_seqs[i]) + len(self.joint[1])
					format.setForeground(QBrush(QColor("red")))
					cursor4.setPosition(CurPos + 0)
					cursor4.setPosition(CurPos + 25, QTextCursor.KeepAnchor)
					cursor4.mergeCharFormat(format)

					cursor4.setPosition(CurPos + cur_len - len(self.joint[1]))
					cursor4.setPosition(CurPos + cur_len, QTextCursor.KeepAnchor)
					cursor4.mergeCharFormat(format)
					CurPos += cur_len + 1

			self.ui.notice.setText('NT fragments have same AA sequence will be merged')

		self.highlightSeq()

	def DecorateNTSeq(self, ColorMap):
		format = QTextCharFormat()
		# F1
		cursor = self.ui.seqEditF1.textCursor()
		text = self.ui.seqEditF1.toPlainText()

		text_list = text.split('\n')
		CurPos = 0
		for i in range(0,len(ColorMap)):
			valueIs = ColorMap[i]

			if valueIs == '0':
				format.setBackground(QBrush(QColor("white")))
			elif valueIs == '7':
				format.setBackground(QBrush(QColor("lightGray")))

			cursor.setPosition(CurPos)
			cursor.setPosition(CurPos + len(text_list[i]), QTextCursor.KeepAnchor)
			cursor.mergeCharFormat(format)

			CurPos += len(text_list[i]) + 1
		# F2
		cursor = self.ui.seqEditF2.textCursor()
		text = self.ui.seqEditF2.toPlainText()

		text_list = text.split('\n')
		CurPos = 0
		for i in range(0, len(ColorMap)):
			valueIs = ColorMap[i]

			if valueIs == '0':
				format.setBackground(QBrush(QColor("white")))
			elif valueIs == '7':
				format.setBackground(QBrush(QColor("lightGray")))

			cursor.setPosition(CurPos)
			cursor.setPosition(CurPos + len(text_list[i]), QTextCursor.KeepAnchor)
			cursor.mergeCharFormat(format)

			CurPos += len(text_list[i]) + 1

		# F3
		cursor = self.ui.seqEditF3.textCursor()
		text = self.ui.seqEditF3.toPlainText()

		text_list = text.split('\n')
		CurPos = 0
		for i in range(0, len(ColorMap)):
			valueIs = ColorMap[i]

			if valueIs == '0':
				format.setBackground(QBrush(QColor("white")))
			elif valueIs == '7':
				format.setBackground(QBrush(QColor("lightGray")))

			cursor.setPosition(CurPos)
			cursor.setPosition(CurPos + len(text_list[i]), QTextCursor.KeepAnchor)
			cursor.mergeCharFormat(format)

			CurPos += len(text_list[i]) + 1

		if self.num_frag == 4:
			# F4
			cursor = self.ui.seqEditF4.textCursor()
			text = self.ui.seqEditF4.toPlainText()

			text_list = text.split('\n')
			CurPos = 0
			for i in range(0, len(ColorMap)):
				valueIs = ColorMap[i]

				if valueIs == '0':
					format.setBackground(QBrush(QColor("white")))
				elif valueIs == '7':
					format.setBackground(QBrush(QColor("lightGray")))

				cursor.setPosition(CurPos)
				cursor.setPosition(CurPos + len(text_list[i]), QTextCursor.KeepAnchor)
				cursor.mergeCharFormat(format)

				CurPos += len(text_list[i]) + 1

	def DecorateAASeq(self, ColorMap, Len):
		cursor1 = self.ui.seqEditF1.textCursor()
		cursor2 = self.ui.seqEditF2.textCursor()
		cursor3 = self.ui.seqEditF3.textCursor()
		cursor4 = self.ui.seqEditF4.textCursor()

		# Setup the desired format for matches
		format = QTextCharFormat()
		format_hyphen = QTextCharFormat()
		format_hyphen.setBackground(QBrush(QColor("red")))
		format_hyphen.setForeground(QBrush(QColor("white")))
		# F1
		CurPos = 0
		for valueIs in ColorMap:
			if valueIs == '0':
				format.setBackground(QBrush(QColor("white")))
			elif valueIs == '7':
				format.setBackground(QBrush(QColor("lightGray")))

			cursor1.setPosition(CurPos)
			cursor1.setPosition(CurPos + Len[0], QTextCursor.KeepAnchor)
			cursor1.mergeCharFormat(format)

			CurPos += Len[0] + 1

		text = self.ui.seqEditF1.toPlainText()
		list = [i.start() for i in re.finditer('-', text)]
		if len(list) > 0:
			for pos in list:
				cursor1.setPosition(pos)
				cursor1.setPosition(pos + 1, QTextCursor.KeepAnchor)
				cursor1.mergeCharFormat(format_hyphen)

		# F2
		CurPos = 0
		for valueIs in ColorMap:
			if valueIs == '0':
				format.setBackground(QBrush(QColor("white")))
			elif valueIs == '7':
				format.setBackground(QBrush(QColor("lightGray")))

			cursor2.setPosition(CurPos)
			cursor2.setPosition(CurPos + Len[1], QTextCursor.KeepAnchor)
			cursor2.mergeCharFormat(format)

			CurPos += Len[1] + 1

		text = self.ui.seqEditF2.toPlainText()
		list = [i.start() for i in re.finditer('-', text)]
		if len(list) > 0:
			for pos in list:
				cursor2.setPosition(pos)
				cursor2.setPosition(pos + 1, QTextCursor.KeepAnchor)
				cursor2.mergeCharFormat(format_hyphen)

		# F3
		CurPos = 0
		for valueIs in ColorMap:
			if valueIs == '0':
				format.setBackground(QBrush(QColor("white")))
			elif valueIs == '7':
				format.setBackground(QBrush(QColor("lightGray")))

			cursor3.setPosition(CurPos)
			cursor3.setPosition(CurPos + Len[2], QTextCursor.KeepAnchor)
			cursor3.mergeCharFormat(format)

			CurPos += Len[2] + 1

		text = self.ui.seqEditF3.toPlainText()
		list = [i.start() for i in re.finditer('-', text)]
		if len(list) > 0:
			for pos in list:
				cursor3.setPosition(pos)
				cursor3.setPosition(pos + 1, QTextCursor.KeepAnchor)
				cursor3.mergeCharFormat(format_hyphen)

		if self.num_frag == 4:
			# F4
			CurPos = 0
			for valueIs in ColorMap:
				if valueIs == '0':
					format.setBackground(QBrush(QColor("white")))
				elif valueIs == '7':
					format.setBackground(QBrush(QColor("lightGray")))

				cursor4.setPosition(CurPos)
				cursor4.setPosition(CurPos + Len[3], QTextCursor.KeepAnchor)
				cursor4.mergeCharFormat(format)

				CurPos += Len[3] + 1

			text = self.ui.seqEditF4.toPlainText()
			list = [i.start() for i in re.finditer('-', text)]
			if len(list) > 0:
				for pos in list:
					cursor4.setPosition(pos)
					cursor4.setPosition(pos + 1, QTextCursor.KeepAnchor)
					cursor4.mergeCharFormat(format_hyphen)

class deleteDialog(QtWidgets.QDialog):
	deleteSignal = pyqtSignal(list)
	def __init__(self):
		super(deleteDialog, self).__init__()
		self.ui = Ui_deleteDialog()
		self.ui.setupUi(self)

		self.ui.deleteButton.clicked.connect(self.accept)
		self.ui.cancelButton.clicked.connect(self.reject)

	def accept(self):
		selItems = self.ui.listWidget.selectedItems()
		del_list = []
		for item in selItems:
			del_list.append(item.text())

		self.deleteSignal.emit(del_list)

class updateSeqDialog(QtWidgets.QDialog):
	updateSignal = pyqtSignal(str, str)
	def __init__(self):
		super(updateSeqDialog, self).__init__()
		self.ui = Ui_UpdateSequenceDialog()
		self.ui.setupUi(self)

		self.ui.confirmButton.clicked.connect(self.accept)
		self.ui.cancelButton.clicked.connect(self.reject)
		self.ui.textEdit.textChanged.connect(self.updateAA)
		self.ui.searchBtn.clicked.connect(self.searchFun)
		self.ui.RFstart.valueChanged.connect(self.highRegion)
		self.ui.RFend.valueChanged.connect(self.highRegion)

	def searchFun(self):
		pattern = self.ui.SearchText.text().upper()
		self.markPattern(pattern)

	def highRegion(self):
		start = self.ui.RFstart.value() - 1
		end = self.ui.RFend.value() - 1
		if start < 0:
			start = 0
		if start < end:
			self.markRegion(start, end)
			self.updateAA()

	def accept(self):
		SeqName = self.ui.lineEdit.text()
		Seq = self.ui.textEdit.toPlainText()

		self.updateSignal.emit(SeqName,Seq)

	def updateAA(self):
		start = self.ui.RFstart.value() - 1
		end = self.ui.RFend.value() - 1
		if start < 0:
			start = 0
		text_nt = self.ui.textEdit.toPlainText()
		text_nt = text_nt[start:end]
		aa_seq = Translator(text_nt,0)
		aa_seq = aa_seq[0]

		self.ui.textEditAA.setText(aa_seq)

	def markRegion(self, start, end):
		text = self.ui.textEdit.toPlainText()
		if end > len(text):
			end = len(text)

		cursor = self.ui.textEdit.textCursor()
		format = QTextCharFormat()
		format.setBackground(QBrush(QColor("white")))
		cursor.setPosition(0)
		cursor.setPosition(len(text), QTextCursor.KeepAnchor)
		cursor.mergeCharFormat(format)

		format.setBackground(QBrush(QColor("lightGray")))
		cursor.setPosition(start)
		cursor.setPosition(end, QTextCursor.KeepAnchor)
		cursor.mergeCharFormat(format)

	def markPattern(self, pattern):
		text = self.ui.textEdit.toPlainText().upper()
		cursor = self.ui.textEdit.textCursor()
		format = QTextCharFormat()

		# reset all font color
		format.setForeground(QBrush(QColor("black")))
		cursor.setPosition(0)
		cursor.setPosition(len(text), QTextCursor.KeepAnchor)
		cursor.mergeCharFormat(format)

		# highlight pattern
		format.setForeground(QBrush(QColor("red")))
		pos_list = [i.start() for i in re.finditer(pattern, text)]
		if len(pos_list) > 0:
			for pos in pos_list:
				cursor.setPosition(pos)
				cursor.setPosition(pos + len(pattern), QTextCursor.KeepAnchor)
				cursor.mergeCharFormat(format)

class fusionDialog(QtWidgets.QDialog):
	fusionSignal = pyqtSignal(list, str, bool, bool, bool)
	fusionSeqSignal = pyqtSignal(str, str, int, int, int, int)
	def __init__(self):
		super(fusionDialog, self).__init__()
		self.ui = Ui_fusionDialog()
		self.ui.setupUi(self)

		self.ui.confirmButton.clicked.connect(self.accept)
		self.ui.cancelButton.clicked.connect(self.reject)
		#self.ui.showButton.clicked.connect(self.showalignment)
		self.ui.selection.itemSelectionChanged.connect(self.displaySeq)

		self.ui.startBase.valueChanged.connect(self.highlight)
		self.ui.endBase.valueChanged.connect(self.highlight)
		self.ui.startDonor.valueChanged.connect(self.highlight)
		self.ui.endDonor.valueChanged.connect(self.highlight)

		self.base_len = 0
		self.donor_len = 0

	def highlight(self):
		startBase = int(self.ui.startBase.text())
		endBase = int(self.ui.endBase.text())

		if startBase != 0 and endBase != 0:
			if endBase > self.base_len:
				endBase = self.base_len
				self.ui.endBase.setValue(endBase)
			if endBase > startBase:
				mut_info = range(startBase, endBase + 1)

				base = self.ui.basename.text()
				WhereState = 'SeqName = "' + base + '"'
				SQLStatement = 'SELECT SeqName, Sequence, Vfrom, VTo FROM LibDB WHERE ' + WhereState
				DataIn = RunSQL(DBFilename, SQLStatement)
				Sequence = DataIn[0][1]
				VFrom = int(DataIn[0][2]) - 1
				if VFrom == -1: VFrom = 0
				VTo = int(DataIn[0][3])
				Sequence = Sequence[VFrom:VTo]
				Sequence = Sequence.upper()
				AA_Sequence = Translator(Sequence, 0)
				AA_Sequence = AA_Sequence[0]

				HANumbering(AA_Sequence)
				Decorations = ['H3Num', 'H1Num', 'Muts']
				self.Decorate(Decorations, self.ui.textEditBase, mut_info)

		startDonor = int(self.ui.startDonor.text())
		endDonor = int(self.ui.endDonor.text())

		if startDonor != 0 and endDonor != 0:
			if endDonor > self.donor_len:
				endDonor = self.donor_len
				self.ui.endDonor.setValue(endDonor)
			if endDonor > startDonor:
				mut_info = range(startDonor, endDonor + 1)

				donor = self.ui.selection.selectedItems()
				if len(donor) > 0:
					donor = donor[0].text()
					WhereState = 'SeqName = "' + donor + '"'
					SQLStatement = 'SELECT SeqName, Sequence, Vfrom, VTo FROM LibDB WHERE ' + WhereState
					DataIn = RunSQL(DBFilename, SQLStatement)
					Sequence = DataIn[0][1]
					VFrom = int(DataIn[0][2]) - 1
					if VFrom == -1: VFrom = 0
					VTo = int(DataIn[0][3])
					Sequence = Sequence[VFrom:VTo]
					Sequence = Sequence.upper()
					AA_Sequence = Translator(Sequence, 0)
					AA_Sequence = AA_Sequence[0]

					HANumbering(AA_Sequence)
					Decorations = ['H3Num', 'H1Num', 'Muts']
					self.Decorate(Decorations, self.ui.textEditDonor, mut_info)

	def accept(self):
		# get sequence editing information
		del_start = self.ui.startBase.text()
		del_end = self.ui.endBase.text()
		add_start = self.ui.startDonor.text()
		add_end = self.ui.endDonor.text()

		# input check
		try:
			del_start = int(del_start)
			del_end = int(del_end)
			add_start = int(add_start)
			add_end = int(add_end)

		except ValueError:
			QMessageBox.warning(self, 'Warning', 'Please type integer numbers in all four inputs! Check your input!', QMessageBox.Ok,
			                    QMessageBox.Ok)
			return
		else:
			if del_start >= del_end or add_start >= add_end:
				QMessageBox.warning(self, 'Warning',
				                    'start position should be smaller than end position!', QMessageBox.Ok,
				                    QMessageBox.Ok)
				return

		listItems = self.ui.selection.selectedItems()
		donor_seq = ''
		if len(listItems) == 0:
			QMessageBox.warning(self, 'Warning', 'Please select sequence from active sequence panel!', QMessageBox.Ok,
			                    QMessageBox.Ok)
			return
		for item in listItems:
			eachItemIs = item.text()
			donor_seq = eachItemIs

		base_seq = self.ui.basename.text()

		self.fusionSeqSignal.emit(base_seq, donor_seq, del_start, del_end, add_start, add_end)

	def displaySeq(self):
		global DBFilename
		global H1Numbering
		global H3Numbering

		if self.ui.textEditBase.toPlainText() == '':
			# base sequence
			base = self.ui.basename.text()
			WhereState = 'SeqName = "' + base + '"'
			SQLStatement = 'SELECT SeqName, Sequence, Vfrom, VTo FROM LibDB WHERE ' + WhereState
			DataIn = RunSQL(DBFilename, SQLStatement)
			Sequence = DataIn[0][1]
			VFrom = int(DataIn[0][2]) - 1
			if VFrom == -1: VFrom = 0
			VTo = int(DataIn[0][3])
			Sequence = Sequence[VFrom:VTo]
			Sequence = Sequence.upper()
			AA_Sequence = Translator(Sequence, 0)
			AA_Sequence = AA_Sequence[0]

			HANumbering(AA_Sequence)
			Decorations = ['H3Num', 'H1Num','Muts']
			self.Decorate(Decorations, self.ui.textEditBase, 'none')

			self.ui.label_base.setText('Base Sequence: ' + base)
			self.base_len = len(AA_Sequence)

		# selected donor
		donor = self.ui.selection.selectedItems()
		if len(donor) > 0:
			donor = donor[0].text()
			WhereState = 'SeqName = "' + donor + '"'
			SQLStatement = 'SELECT SeqName, Sequence, Vfrom, VTo FROM LibDB WHERE ' + WhereState
			DataIn = RunSQL(DBFilename, SQLStatement)
			Sequence = DataIn[0][1]
			VFrom = int(DataIn[0][2]) - 1
			if VFrom == -1: VFrom = 0
			VTo = int(DataIn[0][3])
			Sequence = Sequence[VFrom:VTo]
			Sequence = Sequence.upper()
			AA_Sequence = Translator(Sequence, 0)
			AA_Sequence = AA_Sequence[0]

			HANumbering(AA_Sequence)
			Decorations = ['H3Num', 'H1Num','Muts']
			self.Decorate(Decorations, self.ui.textEditDonor, 'none')

			self.ui.label_donor.setText('Donor Sequence: ' + donor)
			self.donor_len = len(AA_Sequence)

			self.ui.startDonor.setDisabled(False)
			self.ui.endDonor.setDisabled(False)
			self.ui.startDonor.setValue(0)
			self.ui.endDonor.setValue(0)
		else:
			self.ui.textEditDonor.setText('')
			self.ui.startDonor.setValue(0)
			self.ui.endDonor.setValue(0)
			self.ui.startDonor.setDisabled(True)
			self.ui.endDonor.setDisabled(True)
			self.ui.label_donor.setText('Donor Sequence: ')



	def showalignment(self):
		global DBFilename
		# global DataIs
		# self.ui.cboActive.clear()
		AlignIn = []
		listItems = self.ui.selection.selectedItems()
		# if not listItems: return
		WhereState = ''
		NumSeqs = len(listItems)
		i = 1

		if len(listItems) == 0:
			QMessageBox.warning(self, 'Warning', 'Please select sequence from active sequence panel!', QMessageBox.Ok,
			                    QMessageBox.Ok)
			return

		# search selected sequence name
		for item in listItems:
			eachItemIs = item.text()
			WhereState += 'SeqName = "' + eachItemIs + '"'
			if NumSeqs > i:
				WhereState += ' OR '
			i += 1

		# search base sequence name
		basename = self.ui.basename.text()
		WhereState += ' OR ' + 'SeqName = "' + basename + '"'

		SQLStatement = 'SELECT SeqName, Sequence, Vfrom, VTo FROM LibDB WHERE ' + WhereState
		DataIn = RunSQL(DBFilename, SQLStatement)

		for item in DataIn:
			SeqName = item[0]
			Sequence = item[1]
			VFrom = int(item[2]) - 1
			if VFrom == -1: VFrom = 0

			VTo = int(item[3])
			Sequence = Sequence[VFrom:VTo]
			Sequence = Sequence.upper()
			EachIn = (SeqName, Sequence)
			AlignIn.append(EachIn)

		Notes = ''
		self.fusionSignal.emit(AlignIn,Notes, self.ui.dna.isChecked(), self.ui.aa.isChecked(), self.ui.ba.isChecked())

	def Decorate(self, Decorations, textEdit, mutation_info):
		AAColorMap = ''

		H3NumOn = False
		H1NumOn = False
		H3AgOn = False
		H1AgOn = False
		DomainsOn = False
		MutsOn = False
		DonRegOn = False
		AAColorMap = ''
		AASeq = ''
		NumLine = ''
		AAPosColorMap= ''
		rePos = ''
		LenResP = 0
		ResDownP=0

		for Decoration in Decorations:
			if Decoration == 'H3Num':
				H3NumOn = True

			if Decoration == 'H1Num':
				H1NumLine = ''
				H1NumOn = True

			if Decoration == 'Muts':
				MutsLine = ''
				MutsOn = True

		H3NumLine = ''
		H3ColorMap = ''

		H1NumLine = ''
		H1ColorMap = ''

		Key = ''
		KeyMap = ''
		HA2K = False
		TMK = False
		TrimK = False
		StopK = False
		# MakeItUp = ''
		ResT = ''
		InHA1 = False
		InHA2 = False
		NotLong = False
		ResDown = 0

		H3Key = ''
		H3KeyCMap = ''

		H1Key = ''
		H1KeyCMap = ''
		AAKey = 'Sequence elements:  HA1    HA2   stop   Transmembrane  Trimerization-Avitag-H6  Highlight Region \n'
		AAKeyC = '000000000000000000000000099999991111111888888888888888BBBBBBBBBBBBBBBBBBBBBBBBBEEEEEEEEEEEEEEEEEE\n'

		PosKey = ''
		PosKeyC = ''

		if H3NumOn == True:
			for pos in range(1, len(H3Numbering)):
				residue = H3Numbering[pos]
				AA = residue[1]
				AASeq += AA
				resPos = str(pos)

				tesResNP = pos / 5
				if resPos == 1:
					NumLine += str(pos)
					AAPosColorMap += '0'

				elif tesResNP.is_integer():  # is divisible by 5
					ResTP = str(pos)
					LenResP = len(ResTP)

					if NumberingMap['H3HA1end'] > (pos + LenResP + 1):
						ResDownP = LenResP
						NumLine += ResTP[LenResP - ResDownP]

						ResDownP -= 1
						AAPosColorMap += '0'
					else:
						NumLine += '.'
						AAPosColorMap += '0'
				else:
					if ResDownP != 0:
						NumLine += ResTP[LenResP - ResDownP]
						AAPosColorMap += '0'
						# H3ColorMap += '0'
						ResDownP -= 1
					else:
						NumLine += '.'
						AAPosColorMap += '0'

				region = residue[0]

				if region == 'HA1':
					NextC = '0'
					InHA1 = True
				elif region == 'HA2':
					InHA2 = True
					NextC = '9'
					HA2K = True
				elif region == 'TM':
					NextC = '8'
					TMK = True
				elif region == 'Trimer-Avitag-H6':
					NextC = 'B'
					TrimK = True
				else:
					NextC = '0'

				if AA == '*':
					NextC = '1'
					StopK = True
				AAColorMap += NextC

				res = residue[2]
				Ag = residue[4]

				if res != '-':
					# if res.is_integer():
					tesResN = res / 5
					if res == 1:
						H3NumLine += str(res)
						H3ColorMap += '5'

					elif tesResN.is_integer(): #is divisible by 5
						ResT = str(res)
						LenRes = len(ResT)
						if region == 'HA1':
							if NumberingMap['H3HA1end'] > (res + LenRes +1):
								ResDown = LenRes
								H3NumLine += ResT[LenRes - ResDown]
								if Ag == '-':
									H3ColorMap += '0'
								elif Ag == 'A':
									H3ColorMap += '6'
								elif Ag == 'B':
									H3ColorMap += '2'
								elif Ag == 'C':
									H3ColorMap += '7'
								elif Ag == 'D':
									H3ColorMap += '3'
								elif Ag == 'E':
									H3ColorMap += 'C'
								elif Ag == 'Stalk-MN':
									H3ColorMap += 'A'
								else:
									H3ColorMap += '0'

								ResDown -= 1
							else:
								H3NumLine += '.'
								if Ag == '-':
									H3ColorMap += '0'
								elif Ag == 'A':
									H3ColorMap += '6'
								elif Ag == 'B':
									H3ColorMap += '2'
								elif Ag == 'C':
									H3ColorMap += '7'
								elif Ag == 'D':
									H3ColorMap += '3'
								elif Ag == 'E':
									H3ColorMap += 'C'
								elif Ag == 'Stalk-MN':
									H3ColorMap += 'A'
								else:
									H3ColorMap += '0'

						elif region == 'HA2':
							if NumberingMap['H3HA2end'] > (res + LenRes + 1):
								ResDown = LenRes
								H3NumLine += ResT[LenRes - ResDown]
								if Ag == '-':
									H3ColorMap += '0'
								elif Ag == 'Stalk-MN':
									H3ColorMap += 'A'
								else:
									H3ColorMap += '0'

								ResDown -= 1
							else:
								H3NumLine += '.'
								if Ag == '-':
									H3ColorMap += '0'
								elif Ag == 'Stalk-MN':
									H3ColorMap += 'A'
								else:
									H3ColorMap += '0'

					else:
						if ResDown != 0:
							H3NumLine += ResT[LenRes - ResDown]
							if region == 'HA1':
								if Ag == '-':
									H3ColorMap += '0'
								elif Ag == 'A':
									H3ColorMap += '6'
								elif Ag == 'B':
									H3ColorMap += '2'
								elif Ag == 'C':
									H3ColorMap += '7'
								elif Ag == 'D':
									H3ColorMap += '3'
								elif Ag == 'E':
									H3ColorMap += 'C'
								elif Ag == 'Stalk-MN':
									H3ColorMap += 'A'
								else:
									H3ColorMap += '0'
							elif region == 'HA2':
								if Ag == '-':
									H3ColorMap += '0'
								elif Ag == 'Stalk-MN':
									H3ColorMap += 'A'
								else:
									H3ColorMap += '0'
							else:
								H3ColorMap += '0'

							# H3ColorMap += '0'
							ResDown -= 1
						else:
							H3NumLine += '.'
							if region == 'HA1':
								if Ag == '-':
									H3ColorMap += '0'
								elif Ag == 'A':
									H3ColorMap += '6'
								elif Ag == 'B':
									H3ColorMap += '2'
								elif Ag == 'C':
									H3ColorMap += '7'
								elif Ag == 'D':
									H3ColorMap += '3'
								elif Ag == 'E':
									H3ColorMap += 'C'
								elif Ag == 'Stalk-MN':
									H3ColorMap += 'A'
								else:
									H3ColorMap += '0'
							elif region == 'HA2':
								if Ag == '-':
									H3ColorMap += '0'
								elif Ag == 'Stalk-MN':
									H3ColorMap += 'A'
								else:
									H3ColorMap += '0'
							else:
								H3ColorMap += '0'
				else:

					H3NumLine += res
					H3ColorMap += '0'

			H3Key = 'H3 Antigenic Sites:  A    B    C    D    E   Stalk-MN \n'
			H3KeyCMap = '000000000000000000066666222227777733333CCCCCAAAAAAAAAA\n'

		if H1NumOn == True:
			ResDown = 0
			ResT = ''

			for pos in range(1, len(H1Numbering)):
				residue = H1Numbering[pos]

				region = residue[0]

				if H3NumOn == False:
					AA = residue[1]
					AASeq += AA
					resPos = str(pos)

					tesResNP = pos / 5
					if resPos == 1:
						NumLine += str(pos)
						AAPosColorMap += '0'

					elif tesResNP.is_integer():  # is divisible by 5
						ResTP = str(pos)
						LenResP = len(ResTP)

						if NumberingMap['H3HA1end'] > (pos + LenResP + 1):
							ResDownP = LenResP
							NumLine += ResTP[LenResP - ResDownP]
							ResDownP -= 1
							AAPosColorMap += '0'
						else:
							NumLine += '.'

							AAPosColorMap += '0'

					else:
						if ResDownP != 0:
							NumLine += ResTP[LenResP - ResDownP]
							AAPosColorMap += '0'
							# H3ColorMap += '0'
							ResDownP -= 1
						else:
							NumLine += '.'
							AAPosColorMap += '0'

					if region == 'HA1':
						NextC = '0'
						InHA1 = True
					elif region == 'HA2':
						InHA2 = True
						NextC = '9'
						HA2K = True
					elif region == 'TM':
						NextC = '8'
						TMK = True
					elif region == 'Trimer-Avitag-H6':
						NextC = 'B'
						TrimK = True
					else:
						NextC = '0'

					if AA == '*':
						NextC = '1'
						StopK = True

					AAColorMap += NextC


				res = residue[2]
				Ag = residue[4]

				if res != '-':
					# if res.is_integer():
					tesResN = res / 5
					if res == 1:
						H1NumLine += str(res)
						H1ColorMap += '5'

					elif tesResN.is_integer(): #is divisible by 5
						ResT = str(res)
						LenRes = len(ResT)
						if region == 'HA1':
							if NumberingMap['H1HA1end'] > (res + LenRes +1):
								ResDown = LenRes
								H1NumLine += ResT[LenRes - ResDown]
								if Ag == '-':
									H1ColorMap += '0'
								elif Ag == 'Cb':
									H1ColorMap += '7'
								elif Ag == 'Ca1':
									H1ColorMap += '2'
								elif Ag == 'Ca2':
									H1ColorMap += '4'
								elif Ag == 'Sa':
									H1ColorMap += '3'
								elif Ag == 'Sb':
									H1ColorMap += '6'
								else:
									H1ColorMap += '0'

								ResDown -= 1
							else:
								H1NumLine += '.'
								if Ag == '-':
									H1ColorMap += '0'
								elif Ag == 'Cb':
									H1ColorMap += '7'
								elif Ag == 'Ca1':
									H1ColorMap += '2'
								elif Ag == 'Ca2':
									H1ColorMap += '4'
								elif Ag == 'Sa':
									H1ColorMap += '3'
								elif Ag == 'Sb':
									H1ColorMap += '6'
								else:
									H1ColorMap += '0'

						elif region == 'HA2':
							if NumberingMap['H1HA2end'] > (res + LenRes + 1):
								ResDown = LenRes
								H1NumLine += ResT[LenRes - ResDown]
								if Ag == '-':
									H1ColorMap += '0'
								elif Ag == 'Stalk-MN':
									H1ColorMap += 'A'
								else:
									H1ColorMap += '0'

								ResDown -= 1
							else:
								H1NumLine += '.'
								if Ag == '-':
									H1ColorMap += '0'
								elif Ag == 'Stalk-MN':
									H1ColorMap += 'A'
								else:
									H1ColorMap += '0'

					else:
						if ResDown != 0:
							H1NumLine += ResT[LenRes - ResDown]
							if region == 'HA1':
								if Ag == '-':
									H1ColorMap += '0'
								elif Ag == 'Cb':
									H1ColorMap += '7'
								elif Ag == 'Ca1':
									H1ColorMap += '2'
								elif Ag == 'Ca2':
									H1ColorMap += '4'
								elif Ag == 'Sa':
									H1ColorMap += '3'
								elif Ag == 'Sb':
									H1ColorMap += '6'
								else:
									H1ColorMap += '0'
							elif region == 'HA2':
								if Ag == '-':
									H1ColorMap += '0'
								elif Ag == 'Stalk-MN':
									H1ColorMap += 'A'
								else:
									H1ColorMap += '0'
							else:
								H1ColorMap += '0'

							ResDown -= 1
						else:
							H1NumLine += '.'
							if region == 'HA1':
								if Ag == '-':
									H1ColorMap += '0'
								elif Ag == 'Cb':
									H1ColorMap += '7'
								elif Ag == 'Ca1':
									H1ColorMap += '2'
								elif Ag == 'Ca2':
									H1ColorMap += '4'
								elif Ag == 'Sa':
									H1ColorMap += '3'
								elif Ag == 'Sb':
									H1ColorMap += '6'
								else:
									H1ColorMap += '0'
							elif region == 'HA2':
								if Ag == '-':
									H1ColorMap += '0'
								elif Ag == 'Stalk-MN':
									H1ColorMap += 'A'
								else:
									H1ColorMap += '0'
							else:
								H1ColorMap += '0'
				else:

					H1NumLine += res
					H1ColorMap += '0'
			H1Key = 'H1 Antigenic Sites:  Ca1    Ca2    Cb    Sa    Sb   Stalk-MN \n'
			H1KeyCMap = '000000000000000000022222224444444777777333333666666AAAAAAAAAA\n'

		SeqName = ''
		LenSeqName = len(SeqName)

		Sequence = SeqName + '\n'
		ColorMap = ''
		for i in range(0,LenSeqName):
			ColorMap += '0'
		ColorMap += '\n'

		for i in range(0, len(AASeq), 60):
			AASeqSeg = AASeq[i:i + 60]
			AAColorSeg = AAColorMap[i:i + 60]
			NumLineSeg = NumLine[i:i + 60]
			AAPosColorSeg = AAPosColorMap[i:i + 60]

			if DonRegOn == True:
				if donor_info != 'none':
					donor_start, donor_end = donor_info.split('-')
					donor_start = int(donor_start) - 1
					donor_end = int(donor_end)

					cur_start = i
					cur_end = i + 60
					# case 1
					if cur_start > donor_end:
						pass
					# case 2
					if cur_start <= donor_end and cur_start >= donor_start and donor_end <= cur_end:
						cur_donor_start = 0
						cur_donor_end = donor_end - cur_start
						AAPosColorSeg = 'D'*cur_donor_end + AAPosColorSeg[cur_donor_end:]
					# case 3
					if cur_start <= donor_start and cur_end >= donor_end:
						cur_donor_start = donor_start - cur_start
						cur_donor_end = donor_end - cur_start
						AAPosColorSeg = AAPosColorSeg[:cur_donor_start] + 'D' * (cur_donor_end - cur_donor_start) +\
						                AAPosColorSeg[cur_donor_end:]
					# case 4
					if cur_end <= donor_end and cur_end >= donor_start and donor_start >= cur_start:
						cur_donor_start = donor_start - cur_start
						cur_donor_end = cur_end - cur_start
						AAPosColorSeg = AAPosColorSeg[:cur_donor_start] + 'D' * \
						                (cur_donor_end - cur_donor_start)
					# case 5
					if cur_start >= donor_start and cur_end <= donor_end:
						AAPosColorSeg = 'D' * 60
					# case 6
					if donor_start > cur_end:
						pass

			NumLineSeg = '    Position: ' + NumLineSeg + '\n'
			AAPosColorSeg = '00000000000000' + AAPosColorSeg + '\n'

			Sequence += NumLineSeg
			ColorMap += AAPosColorSeg

			if H3NumOn == True:
				H3NumSeg = 'H3-Numbering: ' + H3NumLine[i:i+60] + '\n'
				H3ColorSeg = '00000000000000' + H3ColorMap[i:i + 60] + '\n'
				Sequence += H3NumSeg
				ColorMap += H3ColorSeg

			if H1NumOn == True:
				H1NumSeg = 'H1-Numbering: ' + H1NumLine[i:i + 60] + '\n'
				H1ColorSeg = '00000000000000' + H1ColorMap[i:i + 60] + '\n'
				Sequence += H1NumSeg
				ColorMap += H1ColorSeg

			if MutsOn == True:
				cur_start = i
				cur_end = i + 60

				if mutation_info != "none":
					for x in mutation_info:
						mutation_pos = int(x) - 1

						if mutation_pos in range(cur_start, cur_end):
							AAColorSeg = list(AAColorSeg)
							AAColorSeg[mutation_pos - cur_start] = 'E'
							AAColorSeg = ''.join(AAColorSeg)

			AASeqSeg = '    Sequence: ' + AASeqSeg + '\n\n'
			AAColorSeg = '00000000000000' + AAColorSeg + '\n\n'

			Sequence += AASeqSeg
			ColorMap += AAColorSeg

		Sequence += ' \n'
		ColorMap += '0\n'


		Sequence += AAKey + H3Key + H1Key + PosKey
		ColorMap += AAKeyC + H3KeyCMap + H1KeyCMap + PosKeyC
		# Add note at begining that HA1 is black andHA2 is grey or
		textEdit.setText(Sequence)
		#return
		cursor = textEdit.textCursor()

		format = QTextCharFormat()
		format.setBackground(QBrush(QColor("white")))
		format.setForeground(QBrush(QColor("black")))

		cursor.setPosition(0)
		cursor.setPosition(len(ColorMap), QTextCursor.KeepAnchor)
		cursor.mergeCharFormat(format)

		# Setup the desired format for matches
		CurPos = 0
		for valueIs in ColorMap:  # QColor is RGB: 0-255, 0-255, 0-255
			if valueIs == '0':
				CurPos += 1
				continue
			elif valueIs == '1':
				format.setBackground(QBrush(QColor(255, 00, 0)))  # or 'red'
				format.setForeground(QBrush(QColor("black")))
			elif valueIs == '2':
				format.setBackground(QBrush(QColor("darkMagenta")))
				format.setForeground(QBrush(QColor("white")))
			elif valueIs == '3':
				format.setBackground(QBrush(QColor("darkred")))
				format.setForeground(QBrush(QColor("white")))
			elif valueIs == '3':
				format.setBackground(QBrush(QColor("Magenta")))
				format.setForeground(QBrush(QColor("black")))
			elif valueIs == '4':
				format.setBackground(QBrush(QColor("yellow")))
				format.setForeground(QBrush(QColor("black")))
			elif valueIs == '5':
				format.setBackground(QBrush(QColor("black")))
				format.setForeground(QBrush(QColor("white")))
			elif valueIs == '6':
				format.setBackground(QBrush(QColor("green")))
				format.setForeground(QBrush(QColor("white")))
			elif valueIs == '7':
				format.setBackground(QBrush(QColor("lightGray")))
				format.setForeground(QBrush(QColor("black")))
			elif valueIs == '8':
				format.setBackground(QBrush(QColor("yellow")))
				format.setForeground(QBrush(QColor("black")))
			elif valueIs == '9':
				format.setBackground(QBrush(QColor("lightGray")))
				format.setForeground(QBrush(QColor("black")))
			elif valueIs == '10':
				format.setBackground(QBrush(QColor("black")))
				format.setForeground(QBrush(QColor("white")))
			elif valueIs == 'A':
				format.setBackground(QBrush(QColor("darkBlue")))
				format.setForeground(QBrush(QColor("white")))
			elif valueIs == 'B':
				format.setBackground(QBrush(QColor("darkGreen")))
				format.setForeground(QBrush(QColor("white")))
			elif valueIs == 'C':
				format.setBackground(QBrush(QColor("blue")))
				format.setForeground(QBrush(QColor("yellow")))
			elif valueIs == 'D':
				format.setBackground(QBrush(QColor("Gray")))
				format.setForeground(QBrush(QColor("black")))
			elif valueIs == 'E':
				format.setBackground(QBrush(QColor("lightGray")))
				format.setForeground(QBrush(QColor("red")))

			cursor.setPosition(CurPos)
			cursor.setPosition(CurPos + 1, QTextCursor.KeepAnchor)
			cursor.mergeCharFormat(format)

			CurPos += 1

class basePathDialog(QtWidgets.QDialog):
	def __init__(self):
		super(basePathDialog, self).__init__()
		self.ui = Ui_basePathDialog()
		self.ui.setupUi(self)

		self.ui.browseMuscle.clicked.connect(self.browsemuscledir)
		self.ui.browseClustal.clicked.connect(self.browseclustaldir)
		self.ui.browsePymol.clicked.connect(self.browsepymoldir)
		self.ui.browseFigtree.clicked.connect(self.browsefigtreedir)
		self.ui.browseRaxml.clicked.connect(self.browseraxmldir)
		self.ui.browseFragmentDB.clicked.connect(self.browsesqlitedir)

		self.ui.yes.clicked.connect(self.accept)
		self.ui.no.clicked.connect(self.reject)

	def browsemuscledir(self):  # browse and select path
		out_dir = QFileDialog.getExistingDirectory(self, "select path", '~/')
		if out_dir == '':
			return
		self.ui.musclePath.setText(out_dir)
	def browseclustaldir(self):  # browse and select path
		out_dir = QFileDialog.getExistingDirectory(self, "select path", '~/')
		if out_dir == '':
			return
		self.ui.clustaloPath.setText(out_dir)
	def browsepymoldir(self):  # browse and select path
		out_dir = QFileDialog.getExistingDirectory(self, "select path", '~/')
		if out_dir == '':
			return
		self.ui.pymolPath.setText(out_dir)
	def browsefigtreedir(self):  # browse and select path
		out_dir = QFileDialog.getExistingDirectory(self, "select path", '~/')
		if out_dir == '':
			return
		self.ui.FigtreePath.setText(out_dir)
	def browseraxmldir(self):  # browse and select path
		out_dir = QFileDialog.getExistingDirectory(self, "select path", '~/')
		if out_dir == '':
			return
		self.ui.RaxmlPath.setText(out_dir)
	def browsesqlitedir(self):
		out_dir, _ = QFileDialog.getOpenFileName(self, "select existing fragment DB", temp_folder,
		                                         "Librator database Files (*.ldb);;All Files (*)")
		if out_dir == '':
			return
		self.ui.FragmentDB_path.setText(out_dir)

	def accept(self):  # redo accept method
		global working_prefix
		global temp_folder
		global pymol_path
		global muscle_path
		global clustal_path
		global figtree_path
		global raxml_path
		global fragmentdb_path
		global conf_file
		global ldb_file

		# check if muscle path exist or not
		if self.ui.musclePath.text() != '':
			if os.path.exists(self.ui.musclePath.text()):
				muscle_path = self.ui.musclePath.text()
			else:
				question = 'The path for muscle you typed seems not exist, do you still want to continue?'
				buttons = 'YN'
				answer = questionMessage(self, question, buttons)
				if answer == 'No':
					return
				else:
					muscle_path = self.ui.musclePath.text()

		# check if clustal omega path exist or not
		if self.ui.clustaloPath.text() != '':
			if os.path.exists(self.ui.clustaloPath.text()):
				clustal_path = self.ui.clustaloPath.text()
			else:
				question = 'The path for clustal omega you typed seems not exist, do you still want to continue?'
				buttons = 'YN'
				answer = questionMessage(self, question, buttons)
				if answer == 'No':
					return
				else:
					clustal_path = self.ui.clustaloPath.text()

		# check if PyMOL path exist or not
		if self.ui.pymolPath.text() != '':
			if os.path.exists(self.ui.pymolPath.text()):
				pymol_path = self.ui.pymolPath.text()
			else:
				question = 'The path for PyMOL you typed seems not exist, do you still want to continue?'
				buttons = 'YN'
				answer = questionMessage(self, question, buttons)
				if answer == 'No':
					return
				else:
					pymol_path = self.ui.pymolPath.text()

		# check if FigTree path exist or not
		if self.ui.FigtreePath.text() != '':
			if os.path.exists(self.ui.FigtreePath.text()):
				figtree_path = self.ui.FigtreePath.text()
			else:
				question = 'The path for FigTree you typed seems not exist, do you still want to continue?'
				buttons = 'YN'
				answer = questionMessage(self, question, buttons)
				if answer == 'No':
					return
				else:
					figtree_path = self.ui.FigtreePath.text()

		# check if RAxML path exist or not
		if self.ui.RaxmlPath.text() != '':
			if os.path.exists(self.ui.RaxmlPath.text()):
				raxml_path = self.ui.RaxmlPath.text()
			else:
				question = 'The path for RAxML you typed seems not exist, do you still want to continue?'
				buttons = 'YN'
				answer = questionMessage(self, question, buttons)
				if answer == 'No':
					return
				else:
					raxml_path = self.ui.RaxmlPath.text()

		# check if LDB path exist or not
		if self.ui.FragmentDB_path.text() != '':
			if os.path.exists(self.ui.FragmentDB_path.text()):
				fragmentdb_path = self.ui.FragmentDB_path.text()
			else:
				question = 'The path for local Fragment DB you typed seems not exist, do you still want to continue?'
				buttons = 'YN'
				answer = questionMessage(self, question, buttons)
				if answer == 'No':
					return
				else:
					fragmentdb_path = self.ui.FragmentDB_path.text()



		# save MYSQL setting
		# test if MySQL DB exists
		server_ip = self.ui.IPinput.text()
		server_port = self.ui.Portinput.text()
		db_name = self.ui.DBnameinput.text()
		db_user = self.ui.Userinput.text()
		db_pass = self.ui.Passinput.text()

		db_path = [server_ip, server_port, db_name, db_user, db_pass]
		SQLCommand = "SELECT * FROM Fragments LIMIT 1"
		try:
			fetch_results = RunMYSQL(db_path, SQLCommand)
		except:
			QMessageBox.warning(self, 'Warning', "Can not connect to the MySQL DB or No Fragments table in your DB!",
			                    QMessageBox.Ok, QMessageBox.Ok)
			return

		# save all changes to file
		file_handle = open(conf_file, 'w')
		file_handle.write(muscle_path + '\n')
		file_handle.write(clustal_path + '\n')
		file_handle.write(pymol_path + '\n')
		file_handle.write(raxml_path + '\n')
		file_handle.write(figtree_path)
		file_handle.close()

		file_handle = open(ldb_file, 'w')
		file_handle.write(fragmentdb_path)
		file_handle.close()

		mysql_setting_file = os.path.join(working_prefix, '..', 'Resources', 'Conf', 'mysql_setting.txt')
		file_handle = open(mysql_setting_file, 'w')
		my_info = self.ui.IPinput.text() + ',' + self.ui.Portinput.text() + ',' + self.ui.DBnameinput.text() + \
		          ',' + self.ui.Userinput.text() + ',' + self.ui.Passinput.text()
		file_handle.write(my_info)
		file_handle.close()

		self.close()

class MutationDialog(QtWidgets.QDialog):
	applySignal = pyqtSignal(str, str, str, str, str, str)  # user define signal
	def __init__(self):
		super(MutationDialog, self).__init__()
		self.ui = Ui_MutationDialog()
		self.ui.setupUi(self)

		self.ui.addMutation.clicked.connect(self.accept)
		self.ui.cancel.clicked.connect(self.reject)

		self.ui.radioAll.clicked.connect(self.disable_name)
		self.ui.radioSingle.clicked.connect(self.active_name)

		self.ui.Mutation.textChanged.connect(self.update_name)
		self.ui.HA1mutation.textChanged.connect(self.update_name)
		self.ui.HA2mutation.textChanged.connect(self.update_name)
		self.ui.tabWidget.currentChanged.connect(self.update_name)

	def disable_name(self):
		self.ui.SeqName.setDisabled(True)

	def active_name(self):
		self.ui.SeqName.setDisabled(False)

	def update_name(self):
		active_tab = self.ui.tabWidget.currentIndex()
		if self.ui.radioSingle.isChecked():
			if active_tab == 0:  # OriPos
				seq_name = self.ui.CurSeq.text()
				mu = self.ui.Mutation.text().upper()
				if mu != '':
					seq_name += '-' + mu
				self.ui.SeqName.setText(seq_name)
			else:
				seq_name = self.ui.CurSeq.text()
				mu1 = self.ui.HA1mutation.text().upper()
				mu2 = self.ui.HA2mutation.text().upper()
				if mu1 != '':
					mu1 += '(HA1)'
				if mu2 != '':
					mu2 += '(HA2)'

				if mu1 != '' or mu2 != '':
					seq_name += '-' + mu1 + mu2

				self.ui.SeqName.setText(seq_name)

	def accept(self):  # redo accept method
		# send signal
		active_tab = self.ui.tabWidget.currentIndex()
		seq_name = self.ui.SeqName.text()
		mutation = self.ui.Mutation.text().upper()
		mutation_ha1 = self.ui.HA1mutation.text().upper()
		mutation_ha2 = self.ui.HA2mutation.text().upper()
		template_name = self.ui.CurSeq.text()
		if self.ui.radioSingle.isChecked():
			mode = 'single'
		else:
			mode = 'screen'

		if seq_name in self.active_sequence and mode == 'single':
			QMessageBox.warning(self, 'Warning', 'The sequence name is already taken! Please make a unique name for '
												 'your Generated sequence!', QMessageBox.Ok, QMessageBox.Ok)
			return

		if active_tab == 0: 		# OriPos
			if mutation == "":
				QMessageBox.warning(self, 'Warning',
									'The mutation can not be blank!', QMessageBox.Ok, QMessageBox.Ok)
			else:
				self.applySignal.emit("OriPos", template_name, seq_name, mutation, "Nothing", mode)
		elif active_tab == 1:		# H1H3pos
			if (mutation_ha1 == "" and mutation_ha2 == ""):
				QMessageBox.warning(self, 'Warning',
									'The mutation can not be blank!', QMessageBox.Ok, QMessageBox.Ok)
			else:
				self.applySignal.emit("H1H3pos", template_name, seq_name, mutation_ha1, mutation_ha2, mode)

class gibsoncloneDialog(QtWidgets.QDialog):
	gibsonSignal = pyqtSignal(int, str, str, str, str, list, str, str)  # user define signal

	def __init__(self):
		super(gibsoncloneDialog, self).__init__()
		self.ui = Ui_gibsoncloneDialog()
		self.ui.setupUi(self)

		self.ui.yes.clicked.connect(self.accept)
		self.ui.cancel.clicked.connect(self.reject)
		self.ui.browse.clicked.connect(self.browse)
		self.ui.createDB.clicked.connect(self.new_db)
		self.ui.browseDB.clicked.connect(self.browse_db)
		self.ui.radioButtonH1.clicked.connect(self.setJoint)
		self.ui.radioButtonH3.clicked.connect(self.setJoint)
		self.ui.radioButtonNA.clicked.connect(self.setJoint)
		self.ui.radioButtonDefault.clicked.connect(self.setJoint)
		self.ui.radioButtonUser.clicked.connect(self.setJoint)
		self.ui.checkBoxAll.stateChanged.connect(self.checkAll)
	def checkAll(self):
		rows = self.ui.selectionTable.rowCount()
		if self.ui.checkBoxAll.isChecked():
			for row in range(rows):
				self.ui.selectionTable.cellWidget(row,0).setChecked(True)
		else:
			for row in range(rows):
				self.ui.selectionTable.cellWidget(row,0).setChecked(False)

	def browse(self):  # browse and select path
		global temp_folder
		out_dir = QFileDialog.getExistingDirectory(self, "select files", temp_folder)
		self.ui.outpath.setText(out_dir)

	def setJoint(self):
		global H1_start, H1_end, H3_start, H3_end, NA_start, NA_end
		global H3_start_user, H3_end_user, H1_start_user, H1_end_user, NA_end_user, NA_start_user

		if self.ui.radioButtonH1.isChecked() and self.ui.radioButtonDefault.isChecked():
			data_start = H1_start
			data_end = H1_end
		elif self.ui.radioButtonH3.isChecked() and self.ui.radioButtonDefault.isChecked():
			data_start = H3_start
			data_end = H3_end
		elif self.ui.radioButtonNA.isChecked() and self.ui.radioButtonDefault.isChecked():
			data_start = NA_start
			data_end = NA_end
		elif self.ui.radioButtonH1.isChecked() and self.ui.radioButtonUser.isChecked():
			data_start = H1_start_user
			data_end = H1_end_user
		elif self.ui.radioButtonH3.isChecked() and self.ui.radioButtonUser.isChecked():
			data_start = H3_start_user
			data_end = H3_end_user
		elif self.ui.radioButtonNA.isChecked() and self.ui.radioButtonUser.isChecked():
			data_start = NA_start_user
			data_end = NA_end_user


		if len(data_start) == 3:
			self.ui.F1_start.setText(str(data_start[0]))
			self.ui.F2_start.setText(str(data_start[1]))
			self.ui.F3_start.setText(str(data_start[2]))
			self.ui.F1_end.setText(str(data_end[0]))
			self.ui.F2_end.setText(str(data_end[1]))
			self.ui.F3_end.setText(str(data_end[2]))
			self.ui.F4_start.setText('')
			self.ui.F4_end.setText('')
			self.ui.F4_start.setDisabled(True)
			self.ui.F4_end.setDisabled(True)
		elif len(data_start) == 4:
			self.ui.F4_start.setDisabled(False)
			self.ui.F4_end.setDisabled(False)
			self.ui.F1_start.setText(str(data_start[0]))
			self.ui.F2_start.setText(str(data_start[1]))
			self.ui.F3_start.setText(str(data_start[2]))
			self.ui.F4_start.setText(str(data_start[3]))
			self.ui.F1_end.setText(str(data_end[0]))
			self.ui.F2_end.setText(str(data_end[1]))
			self.ui.F3_end.setText(str(data_end[2]))
			self.ui.F4_end.setText(str(data_end[3]))
		else:
			self.ui.F1_start.setText('')
			self.ui.F2_start.setText('')
			self.ui.F3_start.setText('')
			self.ui.F1_end.setText('')
			self.ui.F2_end.setText('')
			self.ui.F3_end.setText('')
			self.ui.F4_start.setText('')
			self.ui.F4_end.setText('')

	def browse_db(self):  # browse and select path
		global temp_folder
		out_dir, _ = QFileDialog.getOpenFileName(self, "select existing fragment DB", temp_folder,"Librator database Files (*.ldb);;All Files (*)")
		# check if this is the right DB
		if out_dir == '':
			return
		SQLStatement = 'SELECT * FROM Fragments ORDER BY Name DESC LIMIT 1 '
		try:
			DataIn = RunSQL(out_dir, SQLStatement)
		except:
			QMessageBox.warning(self, 'Warning', 'There is no Fragments table in the selected database!', QMessageBox.Ok,
			                    QMessageBox.Ok)
			return
		self.ui.dbpath.setText(out_dir)

	def new_db(self):
		options = QtWidgets.QFileDialog.Options()
		DBFilename, _ = QtWidgets.QFileDialog.getSaveFileName(self,
		                                                      "New Fragment Database",
		                                                      "New Fragment database",
		                                                      "Librator database Files (*.ldb);;All Files (*)",
		                                                      options=options)
		if DBFilename != 'none':
			creatnewFragmentDB(DBFilename)
			self.ui.dbpath.setText(DBFilename)


	def accept(self):  # redo accept method
		global working_prefix

		if self.ui.radioButtonH1.isChecked():
			subtype = 'H1'
		elif self.ui.radioButtonH3.isChecked():
			subtype = 'H3'
		elif self.ui.radioButtonNA.isChecked():
			subtype = 'NA'

		if self.ui.radioButtonDefault.isChecked():
			joint_plan = 'Default'
		elif self.ui.radioButtonUser.isChecked():
			joint_plan = 'User'

		active_tab = self.ui.tabWidget.currentIndex()
		if active_tab == 0:
			# send signal
			joint_up = self.ui.jointUP.toPlainText()
			joint_down = self.ui.jointDOWN.toPlainText()
			db_path = [self.ui.dbpath.text()]
			out_path = self.ui.outpath.text()

			if joint_up == "" or joint_down == "": 		# OriPos
				QMessageBox.warning(self, 'Warning',
										'The joint region can not be blank!', QMessageBox.Ok, QMessageBox.Ok)
			else:
				if out_path == "":
					QMessageBox.warning(self, 'Warning',
										'The output path can not be blank!', QMessageBox.Ok, QMessageBox.Ok)
				else:
					# get selected sequence name
					text = []
					row_table = self.ui.selectionTable.rowCount()
					for i in range(row_table):
						cur_check_box = self.ui.selectionTable.cellWidget(i, 0)
						if cur_check_box.isChecked():
							text.append(cur_check_box.text())
					if len(text) == 0:
						QMessageBox.warning(self, 'Warning',
						                    'Please select at least one sequence!', QMessageBox.Ok, QMessageBox.Ok)
						return
					text = '\n'.join(text)
					self.gibsonSignal.emit(0, text, joint_up, joint_down, out_path, db_path, subtype, joint_plan)
		elif active_tab == 1:
			# send signal
			joint_up = self.ui.jointUP.toPlainText()
			joint_down = self.ui.jointDOWN.toPlainText()
			out_path = self.ui.outpath.text()

			server_ip = self.ui.IPinput.text()
			server_port = self.ui.Portinput.text()
			db_name = self.ui.DBnameinput.text()
			db_user = self.ui.Userinput.text()
			db_pass = self.ui.Passinput.text()

			db_path = [server_ip, server_port, db_name, db_user, db_pass]

			if joint_up == "" or joint_down == "": 		# OriPos
				QMessageBox.warning(self, 'Warning',
										'The joint region can not be blank!', QMessageBox.Ok, QMessageBox.Ok)
				return

			if out_path == "":
				QMessageBox.warning(self, 'Warning',
									'The output path can not be blank!', QMessageBox.Ok, QMessageBox.Ok)
				return

			if server_ip == '' or db_name == '' or db_user == '' or db_pass == '':
				QMessageBox.warning(self, 'Warning',
				                    'The output path can not be blank!', QMessageBox.Ok, QMessageBox.Ok)
				return

			# get selected sequence name
			text = []
			row_table = self.ui.selectionTable.rowCount()
			for i in range(row_table):
				cur_check_box = self.ui.selectionTable.cellWidget(i, 0)
				if cur_check_box.isChecked():
					text.append(cur_check_box.text())
			if len(text) == 0:
				QMessageBox.warning(self, 'Warning',
				                    'Please select at least one sequence!', QMessageBox.Ok, QMessageBox.Ok)
				return
			text = '\n'.join(text)

			# save MYSQL setting
			mysql_setting_file = os.path.join(working_prefix, '..', 'Resources', 'Conf', 'mysql_setting.txt')
			file_handle = open(mysql_setting_file, 'w')
			my_info = self.ui.IPinput.text() + ',' + self.ui.Portinput.text() + ',' + self.ui.DBnameinput.text() + \
			          ',' + self.ui.Userinput.text() + ',' + self.ui.Passinput.text()
			file_handle.write(my_info)
			file_handle.close()

			self.gibsonSignal.emit(1, text, joint_up, joint_down, out_path, db_path, subtype, joint_plan)

class SequenceEditDialog(QtWidgets.QDialog):
	seqEditSignal = pyqtSignal(int, str, str, str)  # user define signal

	def __init__(self):
		super(SequenceEditDialog, self).__init__()
		self.ui = Ui_SequenceEditDialog()
		self.ui.setupUi(self)

		self.ui.GenerateSeq.clicked.connect(self.accept)
		self.ui.Cancel.clicked.connect(self.reject)

		self.ui.GenerateSeq.setToolTip('Generate Sequences!')
		self.ui.Cancel.setToolTip('Cancel!')

	def accept(self):  # redo accept method
		# send signal
		active_tab = self.ui.ModeTab.currentIndex()
		base_name = self.ui.BaseSeqName.text()

		if active_tab == 0: 		# Base biased
			donor_list = self.ui.DonorList_tab1.selectedItems()
			if len(donor_list) == 0:
				QMessageBox.warning(self, 'Warning', 'Please select at least one donor sequence!', QMessageBox.Ok,
									QMessageBox.Ok)
			else:
				text = [i.text() for i in list(donor_list)]
				text = '\t'.join(text)
				self.seqEditSignal.emit(0, base_name, text, "")
		elif active_tab == 1:		# Cocktail
			donor_list = self.ui.DonorList_tab2.selectedItems()
			if self.ui.radioButton_all.isChecked():
				mutation_schema = "all"
			else:
				mutation_schema = "single"
			if len(donor_list) == 0:
				QMessageBox.warning(self, 'Warning', 'Please select at least one donor sequence!', QMessageBox.Ok,
									QMessageBox.Ok)
			else:
				text = [i.text() for i in list(donor_list)]
				text = '\t'.join(text)

				WhereState = "SeqName = " + '"' + text + '"'
				SQLStatement = 'SELECT Role, Donor FROM LibDB WHERE ' + WhereState
				DataIn = RunSQL(DBFilename, SQLStatement)
				select_role = DataIn[0][0]
				select_donor = DataIn[0][1]
				if select_donor == "none":
					reply = QMessageBox.question(self, 'Information', 'Your selected sequence do not have a donor region, will use full HA as donor region, is it OK？',
												 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
					if reply == QMessageBox.Yes:
						self.seqEditSignal.emit(1, base_name, text, mutation_schema)

				else:
					self.seqEditSignal.emit(1, base_name, text, mutation_schema)
		#self.hide()

class VGenesTextMain(QtWidgets.QMainWindow, ui_TextEditor):
	vGeneSignal = pyqtSignal(str, str)
	def __init__(self, parent=None):
		QtWidgets.QMainWindow.__init__(self, parent)
		super(VGenesTextMain, self).__init__()
		self.setupUi()

		self.dnaAct.changed.connect(self.reformat)
		self.aaAct.changed.connect(self.reformat)
		self.baAct.changed.connect(self.reformat)

	def reformat(self):
		if self.type == 'RF':
			return
		DataIn = self.data
		Notes = self.note
		dnaCheck = self.dnaAct.isChecked()
		aaCheck = self.aaAct.isChecked()
		posCheck = self.baAct.isChecked()

		self.AlignSequencesSelf(DataIn, Notes, dnaCheck, aaCheck, posCheck)

	def AlignSequencesSelf(self, DataIn, Notes, dnaCheck, aaCheck, posCheck):
		# import tempfile
		import os
		TupData = ()
		DataSet = []
		QApplication.setOverrideCursor(Qt.WaitCursor)
		global GLMsg
		global working_prefix
		global clustal_path
		global temp_folder
		global VGenesTextWindows

		DataSet = DataIn

		# align selected sequences using ClustalOmega
		outfilename = ''
		try:
			if len(DataSet) == 1:
				time_stamp = str(int(time.time() * 100))
				outfilename = os.path.join(temp_folder, "out-" + time_stamp + ".fas")
				out_handle = open(outfilename, 'w')
				out_handle.write('>' + DataSet[0][0] + '\n')
				out_handle.write(DataSet[0][1])
				out_handle.close()
			else:
				if os.path.exists(clustal_path):
					outfilename = LibratorSeq.ClustalO(DataSet, 80, True, temp_folder, clustal_path)
				else:
					QMessageBox.warning(self, 'Warning',
					                    'The Clustal Omega does not exist! Check your path!', QMessageBox.Ok,
					                    QMessageBox.Ok)
					return

			lenName = 0
			longestName = 0
			alignmentText = ''
			ColorMap = ''
			germseq = ''
			germpeptide = ''

			each = ()
			all = []
			longestName = 10

			peptide = ''
			SeqName = ''
			StartAll = False

			# read alignment file, make alignment NT and AA sequences
			if os.path.isfile(outfilename):
				with open(outfilename, 'r') as currentfile:
					for line in currentfile:
						Readline = line.replace('\n', '').replace('\r', '').replace('-', '.')
						Readline = Readline.strip()
						if Readline[0] == '>':
							if StartAll == True:
								all.append(each)
							StartAll = True
							SeqName = Readline[1:] + ':'
							lenName = len(SeqName)
							if lenName > longestName:
								longestName = lenName + 2
						else:
							AASeq, ErMessage = LibratorSeq.Translator(Readline, 0)
							# Position, Amino Acid, H1-segment (HA1 or HA2), H1Number, A/California/4/2009-residue, H1-antigenic-region

							if DataIn == 'RF':
								AASeq2, ErMessage = LibratorSeq.Translator(Readline, 1)
								AASeq3, ErMessage = LibratorSeq.Translator(Readline, 2)
							peptide = ''
							if DataIn == 'RF':
								peptide2 = ''
								peptide3 = ''

							for res in AASeq:
								peptide += (' ' + res + ' ')

							if DataIn == 'RF':
								for res in AASeq2:
									peptide2 += (' ' + res + ' ')
								for res in AASeq3:
									peptide3 += (' ' + res + ' ')

							peptide = peptide[0:len(Readline)]

							if DataIn == 'RF':
								peptide = peptide[1:]
								peptide2 = peptide2[0:len(Readline)]

							if DataIn == 'RF':
								peptide3 = peptide3[0:len(Readline)]
								peptide3 = ' ' + peptide3

							if SeqName != 'Germline:':
								if DataIn == 'RF':
									each = (SeqName, Readline, peptide, peptide2, peptide3)
								else:
									each = (SeqName, Readline, peptide)
							else:
								germseq = Readline
								germpeptide = peptide
								StartAll = False
				if StartAll == True:
					all.append(each)
			else:
				return
		# todo add header that says what germline based on
		except:
			print('no')

		finally:
			if os.path.exists(outfilename):
				os.remove(outfilename)

		# generate consnesus sequences (AA and NT)
		if len(all) == 1:
			consensusDNA = all[0][1]
			consensusAA = all[0][2]
		else:
			firstOne = all[1]
			seqlen = len(firstOne[1])

			consensusDNA = ''
			tester = ''
			for i in range(0, seqlen - 1):
				tester = ''
				Cnuc = ''
				for item in all:
					seq = item[1]
					tester += seq[i]

				frequencies = [(c, tester.count(c)) for c in set(tester)]
				Cnuc = max(frequencies, key=lambda x: x[1])[0]
				consensusDNA += Cnuc

			consensusAA = ''
			firstOne = all[1]
			seqlen = len(firstOne[1])
			for i in range(0, seqlen - 1):
				tester = ''
				Caa = ''
				for item in all:
					seq = item[2]
					tester += seq[i]

				frequencies = [(c, tester.count(c)) for c in set(tester)]
				Caa = max(frequencies, key=lambda x: x[1])[0]
				consensusAA += Caa

		# align consensus AA sequence with template to generate H1 and H3 numbering
		if posCheck == True:
			compact_consensusAA = consensusAA.replace(' ', '')
			HANumbering(compact_consensusAA)

		header = 'VGenes multiple alignment using Clustal Omega. \n'
		ConName = 'Consensus: '

		if DataIn == 'RF': ConName = 'Sequence: '

		while len(ConName) < longestName:
			ConName += ' '

		AASpaces = ''
		while len(AASpaces) < longestName:
			AASpaces += ' '

		alignmentText = header
		ColorMap += '0' * (len(header) - 1) + '\n'
		i = 0
		endSeg = 0
		done = False
		ConAdd = True

		if dnaCheck == True:
			maxLen = len(consensusDNA)
		else:
			NewConAA = consensusAA.replace(' ', '')
			maxLen = len(NewConAA)

		# canAA = True
		while endSeg <= maxLen - 1:
			if i + 60 < maxLen:
				endSeg = i + 60
			else:
				endSeg = maxLen

			aa_start = int(i / 3 + 1)
			aa_end = int(endSeg / 3)
			if posCheck == True:
				rulerAA = 'Position(AA)' + AASpaces[12:] + MakeRuler(aa_start, aa_end, 5, 'aa')
				rulerNT = 'Position(NT)' + AASpaces[12:] + MakeRuler(i + 1, endSeg, 5, 'nt')
				if aaCheck == True and dnaCheck == True:
					rulerH1 = 'H1numbering' + AASpaces[11:]
					rulerH1Color = '0' * len(rulerH1)
					rulerH3 = 'H3numbering' + AASpaces[11:]
					rulerH3Color = '0' * len(rulerH3)

					# make H1 numbering
					space_from_last_pos = 0
					for x in range(aa_start, aa_end + 1):
						if H1Numbering[x][2] == '-':
							rulerH1 += ' ' * (1 - space_from_last_pos) + '- '
							space_from_last_pos = 0
							rulerH1Color += '000'
						else:
							if int(H1Numbering[x][2]) % 5 == 0:
								if len(str(H1Numbering[x][2])) == 1:
									rulerH1 += ' ' * (1 - space_from_last_pos) + str(H1Numbering[x][2]) + ' '
									space_from_last_pos = 0
								elif len(str(H1Numbering[x][2])) == 2:
									rulerH1 += ' ' * (1 - space_from_last_pos) + str(H1Numbering[x][2])
									space_from_last_pos = 0
								else:
									rulerH1 += ' ' * (1 - space_from_last_pos) + str(H1Numbering[x][2])
									space_from_last_pos = 1
							else:
								rulerH1 += ' ' * (1 - space_from_last_pos) + '. '
								space_from_last_pos = 0
							if H1Numbering[x][4] == "Cb":
								rulerH1Color += '777'
							elif H1Numbering[x][4] == "Ca1":
								rulerH1Color += '222'
							elif H1Numbering[x][4] == "Ca2":
								rulerH1Color += '444'
							elif H1Numbering[x][4] == "Sa":
								rulerH1Color += '333'
							elif H1Numbering[x][4] == "Sb":
								rulerH1Color += '666'
							elif H1Numbering[x][4] == "Stalk-MN":
								rulerH1Color += 'AAA'
							else:
								rulerH1Color += '000'
					if space_from_last_pos == 1:
						rulerH1Color += rulerH1Color[-1]

					# make H3 numbering
					space_from_last_pos = 0
					for x in range(aa_start, aa_end + 1):
						if H3Numbering[x][2] == '-':
							rulerH3 += ' ' * (1 - space_from_last_pos) + '- '
							space_from_last_pos = 0
							rulerH3Color += '000'
						else:
							if int(H3Numbering[x][2]) % 5 == 0:
								if len(str(H3Numbering[x][2])) == 1:
									rulerH3 += ' ' * (1 - space_from_last_pos) + str(H3Numbering[x][2]) + ' '
									space_from_last_pos = 0
								elif len(str(H3Numbering[x][2])) == 2:
									rulerH3 += ' ' * (1 - space_from_last_pos) + str(H3Numbering[x][2])
									space_from_last_pos = 0
								else:
									rulerH3 += ' ' * (1 - space_from_last_pos) + str(H3Numbering[x][2])
									space_from_last_pos = 1
							else:
								rulerH3 += ' ' * (1 - space_from_last_pos) + '. '
								space_from_last_pos = 0
							if H3Numbering[x][4] == "A":
								rulerH3Color += '666'
							elif H3Numbering[x][4] == "B":
								rulerH3Color += '222'
							elif H3Numbering[x][4] == "C":
								rulerH3Color += '777'
							elif H3Numbering[x][4] == "D":
								rulerH3Color += '333'
							elif H3Numbering[x][4] == "E":
								rulerH3Color += 'CCC'
							elif H3Numbering[x][4] == "Stalk-MN":
								rulerH3Color += 'AAA'
							else:
								rulerH3Color += '000'
					if space_from_last_pos == 1:
						rulerH3Color += rulerH3Color[-1]
				elif aaCheck == True and dnaCheck == False:
					aa_start = i + 1
					aa_end = endSeg

					rulerH1 = 'H1numbering' + AASpaces[11:]
					rulerH1Color = '0' * len(rulerH1)
					rulerH3 = 'H3numbering' + AASpaces[11:]
					rulerH3Color = '0' * len(rulerH3)

					# make H1 numbering
					space_from_last_pos = 0
					for x in range(aa_start, aa_end + 1):
						if H1Numbering[x][2] == '-':
							if space_from_last_pos == 2:
								rulerH1Color += '0'
								space_from_last_pos = space_from_last_pos - 1
							elif space_from_last_pos == 1:
								rulerH1Color += '0'
								space_from_last_pos = space_from_last_pos - 1
							else:
								rulerH1 += '-'
								rulerH1Color += '0'
						else:
							if int(H1Numbering[x][2]) % 5 == 0:
								if len(str(H1Numbering[x][2])) == 1:
									rulerH1 += str(H1Numbering[x][2])
									space_from_last_pos = 0
								elif len(str(H1Numbering[x][2])) == 2:
									rulerH1 += str(H1Numbering[x][2])
									space_from_last_pos = 1
								else:
									rulerH1 += str(H1Numbering[x][2])
									space_from_last_pos = 2
							else:
								if space_from_last_pos == 2:
									space_from_last_pos = space_from_last_pos - 1
								elif space_from_last_pos == 1:
									space_from_last_pos = space_from_last_pos - 1
								else:
									rulerH1 += '.'

							if H1Numbering[x][4] == "Cb":
								rulerH1Color += '7'
							elif H1Numbering[x][4] == "Ca1":
								rulerH1Color += '2'
							elif H1Numbering[x][4] == "Ca2":
								rulerH1Color += '4'
							elif H1Numbering[x][4] == "Sa":
								rulerH1Color += '3'
							elif H1Numbering[x][4] == "Sb":
								rulerH1Color += '6'
							elif H1Numbering[x][4] == "Stalk-MN":
								rulerH1Color += 'A'
							else:
								rulerH1Color += '0'
					if space_from_last_pos == 2:
						# rulerH1Color += rulerH1Color[-1] * 2
						rulerH1Color += '00'
					elif space_from_last_pos == 1:
						# rulerH1Color += rulerH1Color[-1]
						rulerH1Color += '0'

					# make H3 numbering
					space_from_last_pos = 0
					for x in range(aa_start, aa_end + 1):
						if H3Numbering[x][2] == '-':
							if space_from_last_pos == 2:
								space_from_last_pos = space_from_last_pos - 1
								rulerH3Color += '0'
							elif space_from_last_pos == 1:
								space_from_last_pos = space_from_last_pos - 1
								rulerH3Color += '0'
							else:
								rulerH3 += '-'
								rulerH3Color += '0'
						else:
							if int(H3Numbering[x][2]) % 5 == 0:
								if len(str(H3Numbering[x][2])) == 1:
									rulerH3 += str(H3Numbering[x][2])
									space_from_last_pos = 0
								elif len(str(H3Numbering[x][2])) == 2:
									rulerH3 += str(H3Numbering[x][2])
									space_from_last_pos = 1
								else:
									rulerH3 += str(H3Numbering[x][2])
									space_from_last_pos = 2
							else:
								if space_from_last_pos == 2:
									space_from_last_pos = space_from_last_pos - 1
								elif space_from_last_pos == 1:
									space_from_last_pos = space_from_last_pos - 1
								else:
									rulerH3 += '.'

							if H3Numbering[x][4] == "A":
								rulerH3Color += '6'
							elif H3Numbering[x][4] == "B":
								rulerH3Color += '2'
							elif H3Numbering[x][4] == "C":
								rulerH3Color += '7'
							elif H3Numbering[x][4] == "D":
								rulerH3Color += '3'
							elif H3Numbering[x][4] == "E":
								rulerH3Color += 'C'
							elif H3Numbering[x][4] == "Stalk-MN":
								rulerH3Color += 'A'
							else:
								rulerH3Color += '0'
					if space_from_last_pos == 2:
						# rulerH3Color += rulerH1Color[-1] * 2
						rulerH3Color += '00'
					elif space_from_last_pos == 1:
						# rulerH3Color += rulerH1Color[-1]
						rulerH3Color += '0'

			for seq in all:
				SeqName = seq[0]
				DNASeq = seq[1]
				AASeq = seq[2]
				if DataIn == 'RF':
					AASeq2 = seq[3]
					AASeq3 = seq[4]

				NewAA = AASeq.replace(' ', '')
				if DataIn == 'RF':
					NewAA2 = AASeq2.replace(' ', '')
					NewAA3 = AASeq3.replace(' ', '')

				while len(SeqName) < longestName:
					SeqName += ' '
				# todo can build num line even add CDR if align relative to germline instead just number as end
				toSpace = len(str(maxLen))
				endLabel = str(endSeg)
				while len(endLabel) < toSpace:
					endLabel += ' '
				endLabel = '  ' + endLabel

				if dnaCheck == True:

					ConSegDNA = consensusDNA[i:endSeg]
					DNASeqSeg = DNASeq[i:endSeg]
					ConSegDNA = ConSegDNA.upper()
					DNASeqSeg = DNASeqSeg.upper()

					DNAArt = ''
					for n in range(0, len(ConSegDNA)):
						if DNASeqSeg[n] == ConSegDNA[n]:
							if DataIn == 'RF':
								DNAArt += '-'
							else:
								char = DNASeqSeg[n]
								char = char.upper()
								# DNAArt += char
								DNAArt += '-'
						else:
							if DataIn == 'RF':
								DNAArt += DNASeqSeg[n]
							else:
								char = DNASeqSeg[n]
								char = char.lower()
								DNAArt += char

					ConSegDNA = ConName + ConSegDNA + endLabel
					DNASeqSeg = SeqName + DNAArt + endLabel
					if aaCheck == True:
						AArt = ''
						ConSegAA = consensusAA[i:endSeg]
						if DataIn == 'RF': ConSegAA2 = AASeq2[i:endSeg]
						if DataIn == 'RF': ConSegAA3 = AASeq3[i:endSeg]

						AASeqSeg = AASeq[i:endSeg]

						for n in range(0, len(ConSegAA)):
							if AASeqSeg[n] == ConSegAA[n]:
								AArt += ' '
							else:
								AArt += AASeqSeg[n]

						AASeqSeg = AASpaces + AArt  # + endLabel
						if DataIn == 'RF':
							ConSegAA = AASpaces + 'RF1: ' + ConSegAA
						else:
							ConSegAA = AASpaces + ConSegAA

						if DataIn == 'RF':
							ConSegAA2 = AASpaces + 'RF2: ' + ConSegAA2
							ConSegAA3 = AASpaces + 'RF3: ' + ConSegAA3

						if ConAdd == True:
							if posCheck == True:
								alignmentText += '\n' + rulerAA
								ColorMap += '\n' + '0' * len(rulerAA)
								alignmentText += '\n' + rulerH1
								ColorMap += '\n' + rulerH1Color
								alignmentText += '\n' + rulerH3
								ColorMap += '\n' + rulerH3Color

							alignmentText += '\n' + ConSegAA + '\n'
							ColorMap += '\n' + '0' * len(ConSegAA) + '\n'
							if DataIn == 'RF':
								alignmentText += '\n' + ConSegAA2 + '\n'
								alignmentText += '\n' + ConSegAA3 + '\n'
								alignmentText += '     ' + ConSegDNA + '\n'
							else:
								if posCheck == True:
									alignmentText += rulerNT + '\n'
									ColorMap += '0' * len(rulerNT) + '\n'

								alignmentText += ConSegDNA + '\n'
								ColorMap += '0' * len(ConSegDNA) + '\n'
							ConAdd = False
						if DataIn != 'RF':
							alignmentText += AASeqSeg + '\n'
							ColorMap += '0' * len(AASeqSeg) + '\n'
							alignmentText += DNASeqSeg + '\n'
							ColorMap += '0' * len(DNASeqSeg) + '\n'
					else:
						if ConAdd == True:
							if posCheck == True:
								alignmentText += '\n' + rulerNT
								ColorMap += '0' * len(rulerNT)
							alignmentText += '\n' + ConSegDNA + '\n'
							ColorMap += '\n' + '0' * len(ConSegDNA) + '\n'
							ConAdd = False
						if DataIn != 'RF':
							alignmentText += DNASeqSeg + '\n'
							ColorMap += '0' * len(DNASeqSeg) + '\n'
				else:
					if aaCheck == True:
						AArt = ''
						ConSegAA = NewConAA[i:endSeg]
						AASeqSeg = NewAA[i:endSeg]

						for n in range(0, len(ConSegAA)):
							if AASeqSeg[n] == ConSegAA[n]:
								AArt += '-'
							else:
								AArt += AASeqSeg[n]

						AASeqSeg = SeqName + AArt + endLabel
						ConSegAA = ConName + ConSegAA
						if ConAdd == True:
							if posCheck == True:
								alignmentText += '\n' + 'Position(AA)' + rulerNT[12:]
								ColorMap += '\n' + '0' * len(rulerNT)
								alignmentText += '\n' + rulerH1
								ColorMap += '\n' + rulerH1Color
								alignmentText += '\n' + rulerH3
								ColorMap += '\n' + rulerH3Color
							alignmentText += '\n' + ConSegAA + '\n'
							ColorMap += '\n' + '0' * len(ConSegAA) + '\n'
							ConAdd = False
						alignmentText += AASeqSeg + '\n'
						ColorMap += '0' * len(AASeqSeg) + '\n'

			i += 60
			ConAdd = True
			alignmentText += '\n'
			ColorMap += '\n'

		# legend text and color
		legend_text = 'H1 Antigenic Sites:  Ca1    Ca2    Cb    Sa    Sb   Stalk-MN \n' + \
		              'H3 Antigenic Sites:  A    B    C    D    E   Stalk-MN \n'
		legend_color = '000000000000000000022222224444444777777333333666666AAAAAAAAAA\n' + \
		               '000000000000000000066666222227777733333CCCCCAAAAAAAAAA\n'

		self.ShowVGenesTextEdit(alignmentText, ColorMap)

	# update current window content
	def ShowVGenesTextEdit(self, textToShow, ColorMap):
		self.textEdit.setText(textToShow)
		cursor = self.textEdit.textCursor()
		self.DecorateText(ColorMap, cursor)

	def DecorateText(self, ColorMap, cursor):
		# setup default color for all text
		format = QTextCharFormat()
		format.setBackground(QBrush(QColor("white")))
		format.setForeground(QBrush(QColor("black")))

		cursor.setPosition(0)
		cursor.setPosition(len(ColorMap), QTextCursor.KeepAnchor)
		cursor.mergeCharFormat(format)

		# Setup the desired format for matches
		CurPos = 0
		for valueIs in ColorMap:  #QColor is RGB: 0-255, 0-255, 0-255
			if valueIs == '0':
				CurPos += 1
				continue
			elif valueIs == '1':
				format.setBackground(QBrush(QColor(255,00,0))) #or 'red'
				format.setForeground(QBrush(QColor("black")))
			elif valueIs == '2':
				format.setBackground(QBrush(QColor("darkMagenta")))
				format.setForeground(QBrush(QColor("white")))
			elif valueIs == '3':
				format.setBackground(QBrush(QColor("darkred")))
				format.setForeground(QBrush(QColor("white")))
			elif valueIs == '3':
				format.setBackground(QBrush(QColor("Magenta")))
				format.setForeground(QBrush(QColor("black")))
			elif valueIs == '4':
				format.setBackground(QBrush(QColor("yellow")))
				format.setForeground(QBrush(QColor("black")))
			elif valueIs == '5':
				format.setBackground(QBrush(QColor("black")))
				format.setForeground(QBrush(QColor("white")))
			elif valueIs == '6':
				format.setBackground(QBrush(QColor("green")))
				format.setForeground(QBrush(QColor("white")))
			elif valueIs == '7':
				format.setBackground(QBrush(QColor("lightGray")))
				format.setForeground(QBrush(QColor("black")))
			elif valueIs == '8':
				format.setBackground(QBrush(QColor("yellow")))
				format.setForeground(QBrush(QColor("black")))
			elif valueIs == '9':
				format.setBackground(QBrush(QColor("lightGray")))
				format.setForeground(QBrush(QColor("black")))
			elif valueIs == '10':
				format.setBackground(QBrush(QColor("black")))
				format.setForeground(QBrush(QColor("white")))
			elif valueIs == 'A':
				format.setBackground(QBrush(QColor("darkBlue")))
				format.setForeground(QBrush(QColor("white")))
			elif valueIs == 'B':
				format.setBackground(QBrush(QColor("darkGreen")))
				format.setForeground(QBrush(QColor("white")))
			elif valueIs == 'C':
				format.setBackground(QBrush(QColor("blue")))
				format.setForeground(QBrush(QColor("yellow")))
			elif valueIs == 'D':
				format.setBackground(QBrush(QColor("Gray")))
				format.setForeground(QBrush(QColor("black")))
			elif valueIs == 'E':
				format.setBackground(QBrush(QColor("lightGray")))
				format.setForeground(QBrush(QColor("red")))


			cursor.setPosition(CurPos)
			cursor.setPosition(CurPos + 1, QTextCursor.KeepAnchor)
			cursor.mergeCharFormat(format)

			CurPos += 1

class htmlDialog(QtWidgets.QDialog):
	def __init__(self):
		super(htmlDialog, self).__init__()
		self.ui = Ui_htmlDialog()
		self.ui.setupUi(self)

class LibratorMain(QtWidgets.QMainWindow):
	def __init__(self):  # , parent=None):
		global VGenesTextWindows
	# def __init__(self, master=None):
		super(LibratorMain, self).__init__()  # parent)
		self.ui = Ui_MainLibrator()
		self.ui.setupUi(self)

		self.ui.listWidgetStrainsIn.itemClicked['QListWidgetItem*'].connect(self.ListItemChanged)
		self.ui.listWidgetStrainsIn.itemDoubleClicked.connect(self.removeSel)
		self.ui.listWidgetStrainsIn.itemSelectionChanged.connect(self.ListItemChanged)
		self.ui.cboRole.currentTextChanged['QString'].connect(self.RoleChanged)
		self.ui.cboForm.currentTextChanged['QString'].connect(self.FormChanged)
		self.ui.cboSubtype.currentTextChanged['QString'].connect(self.SubTypeChanged)
		self.ui.cboRecent.currentTextChanged['QString'].connect(self.OpenRecent)
		self.ui.cboReportOptions.currentTextChanged['QString'].connect(self.GenerateReport)
		self.ui.spnFrom.valueChanged['int'].connect(self.SeqFrom)
		self.ui.spnTo.valueChanged['int'].connect(self.SeqTo)
		self.ui.spnAlignFont.valueChanged['int'].connect(self.AlignFont)
		self.ui.txtDonorRegions.selectionChanged.connect(self.DonorRegionsDialog)
		self.ui.txtInsert_Base.selectionChanged.connect(self.MutationsDialog)
		self.ui.txtName.cursorPositionChanged.connect(self.EditSeqName)
		self.ui.tabWidget.currentChanged['int'].connect(self.FillAlignmentTab)
		self.ui.rdoDNA.clicked.connect(self.resetSearch)
		self.ui.rdoAA.clicked.connect(self.resetSearch)
		self.ui.SearchButton.clicked.connect(self.searchPattern)
		self.ui.browseFragmentDB.clicked.connect(self.determineFile)
		self.ui.connectFragmentDB.clicked.connect(self.connectDB)
		self.ui.FragmentTab.currentChanged['int'].connect(self.clearTable)
		self.ui.EditLock.clicked.connect(self.ChangeEditMode)
		self.ui.groupCombo.currentTextChanged.connect(self.rebuildTree)

		self.ui.cboRole.last_value = ''
		self.ui.cboForm.last_value = ''
		self.ui.cboSubtype.last_value = ''

		self.UpdateRecent()
		self.modalessMutationDialog = None
		self.modalessSeqEditDialog = None
		self.TextEdit = VGenesTextMain()
		self.modalessJointDialog = None

		self.fig = 0
		self.html = 0



		self.ui.HTMLview1 = ResizeWidget(self)
		self.ui.HTMLview1.id = 1
		grid_html1 = QGridLayout(self.ui.groupBoxHTML1)
		grid_html1.addWidget(self.ui.HTMLview1)

		self.ui.HTMLview2 = ResizeWidget(self)
		self.ui.HTMLview2.id = 2
		grid_html2 = QGridLayout(self.ui.groupBoxHTML2)
		grid_html2.addWidget(self.ui.HTMLview2)

		self.ui.comboBoxHANA_html = QComboBox()
		self.ui.comboBoxHANA_html.addItem("H1/Group1")
		self.ui.comboBoxHANA_html.addItem("H3/Group2")
		self.ui.comboBoxHANA_html.addItem("NA")
		self.ui.comboBoxHANA_html.currentIndexChanged.connect(self.reloadHTML)
		self.ui.comboBoxIndex_html = QComboBox()
		self.ui.comboBoxIndex_html.addItem("Percentage of Variation")
		self.ui.comboBoxIndex_html.addItem("Amino Acid Variation Index")
		self.ui.comboBoxIndex_html.currentIndexChanged.connect(self.reloadHTML)
		self.ui.HTMLview3 = ResizeWidget(self)
		self.ui.HTMLview3.id = 3
		grid_html3 = QGridLayout(self.ui.groupBoxHTML3)
		grid_html3.addWidget(self.ui.comboBoxHANA_html,1,0)
		grid_html3.addWidget(self.ui.comboBoxIndex_html,1,1)
		grid_html3.addWidget(self.ui.HTMLview3,2,0,10,0)

		self.ui.HTMLview1.resizeSignal.connect(self.resizeHTML)
		self.ui.HTMLview2.resizeSignal.connect(self.resizeHTML)
		self.ui.HTMLview3.resizeSignal.connect(self.resizeHTML)

	def ChangeEditMode(self):
		if self.ui.SeqTable.editTriggers() == QtWidgets.QAbstractItemView.NoEditTriggers:
			unlock_icon = QtGui.QIcon()
			unlock_icon.addPixmap(QtGui.QPixmap(":/PNG-Icons/unlocked.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.EditLock.setIcon(unlock_icon)
			self.ui.SeqTable.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
		else:
			lock_icon = QtGui.QIcon()
			lock_icon.addPixmap(QtGui.QPixmap(":/PNG-Icons/locked.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.EditLock.setIcon(lock_icon)
			self.ui.SeqTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

	def reloadHTML(self):
		if self.ui.HTMLview3.h != 0:
			######  plot stat for H1
			if self.ui.comboBoxHANA_html.currentIndex() == 0 and self.ui.comboBoxIndex_html.currentIndex() == 0:  # H1 + PCT
				# get data
				data_file = os.path.join(working_prefix, '..', 'Resources', 'Data', 'H1_PCT.csv')
				if os.path.exists(data_file):
					pass
				else:
					return

				csvFile = open(data_file, "r")
				reader = csv.reader(csvFile)
				data_array = []
				for item in reader:
					item = list(map(float, item))
					data_array.append(item)
				# generate local HTML
				line = (
					Line(init_opts=opts.InitOpts(width="900px", height="380px"))
						.add_xaxis(range(1, len(data_array[0]) + 1))
						.add_yaxis("Season H1", data_array[0], is_symbol_show=False)
						.add_yaxis("pdm09 H1", data_array[1], is_symbol_show=False)
						.set_global_opts(
						title_opts=opts.TitleOpts(title="Variations for H1(Pct)", subtitle="human H1"))
				)
			elif self.ui.comboBoxHANA_html.currentIndex() == 1 and self.ui.comboBoxIndex_html.currentIndex() == 0:  # H3 + PCT
				# get data
				data_file = os.path.join(working_prefix, '..', 'Resources', 'Data', 'H3_PCT.csv')
				if os.path.exists(data_file):
					pass
				else:
					return

				csvFile = open(data_file, "r")
				reader = csv.reader(csvFile)
				data_array = []
				for item in reader:
					item = list(map(float, item))
					data_array.append(item)
				# generate local HTML
				line = (
					Line(init_opts=opts.InitOpts(width="900px", height="380px"))
						.add_xaxis(range(1, len(data_array[0]) + 1))
						.add_yaxis("H3", data_array[0], is_symbol_show=False)
						.set_global_opts(
						title_opts=opts.TitleOpts(title="Variations for H3(Pct)", subtitle="human H3"))
				)
			elif self.ui.comboBoxHANA_html.currentIndex() == 2 and self.ui.comboBoxIndex_html.currentIndex() == 0:  # NA + PCT
				# get data
				data_file = os.path.join(working_prefix, '..', 'Resources', 'Data', 'NA_PCT.csv')
				if os.path.exists(data_file):
					pass
				else:
					return

				csvFile = open(data_file, "r")
				reader = csv.reader(csvFile)
				data_array = []
				for item in reader:
					item = list(map(float, item))
					data_array.append(item)
				# generate local HTML
				line = (
					Line(init_opts=opts.InitOpts(width="900px", height="380px"))
						.add_xaxis(range(1, len(data_array[0]) + 1))
						.add_yaxis("N1", data_array[0], is_symbol_show=False)
						.add_yaxis("N2", data_array[1], is_symbol_show=False)
						.add_yaxis("N3", data_array[2], is_symbol_show=False)
						.add_yaxis("N4", data_array[3], is_symbol_show=False)
						.add_yaxis("N5", data_array[4], is_symbol_show=False)
						.add_yaxis("N6", data_array[5], is_symbol_show=False)
						.add_yaxis("N7", data_array[6], is_symbol_show=False)
						.add_yaxis("N8", data_array[7], is_symbol_show=False)
						.add_yaxis("N9", data_array[8], is_symbol_show=False)
						.set_global_opts(
						title_opts=opts.TitleOpts(title="Variations for NA(Pct)", subtitle="human NA"))
				)
			elif self.ui.comboBoxHANA_html.currentIndex() == 0 and self.ui.comboBoxIndex_html.currentIndex() == 1:  # H1 + AAVI
				# get data
				data_file = os.path.join(working_prefix, '..', 'Resources', 'Data', 'H1_AAVI.csv')
				if os.path.exists(data_file):
					pass
				else:
					return

				csvFile = open(data_file, "r")
				reader = csv.reader(csvFile)
				data_array = []
				for item in reader:
					item = list(map(float, item))
					data_array.append(item)
				# generate local HTML
				line = (
					Line(init_opts=opts.InitOpts(width="900px", height="380px"))
						.add_xaxis(range(1, len(data_array[0]) + 1))
						.add_yaxis("Season H1", data_array[0], is_symbol_show=False)
						.add_yaxis("pdm09 H1", data_array[1], is_symbol_show=False)
						.set_global_opts(
						title_opts=opts.TitleOpts(title="Variations for H1(AAVI)", subtitle="human H1"))
				)
			elif self.ui.comboBoxHANA_html.currentIndex() == 1 and self.ui.comboBoxIndex_html.currentIndex() == 1:  # H3 + AAVI
				# get data
				data_file = os.path.join(working_prefix, '..', 'Resources', 'Data', 'H3_AAVI.csv')
				if os.path.exists(data_file):
					pass
				else:
					return

				csvFile = open(data_file, "r")
				reader = csv.reader(csvFile)
				data_array = []
				for item in reader:
					item = list(map(float, item))
					data_array.append(item)
				# generate local HTML
				line = (
					Line(init_opts=opts.InitOpts(width="900px", height="380px"))
						.add_xaxis(range(1, len(data_array[0]) + 1))
						.add_yaxis("H3", data_array[0], is_symbol_show=False)
						.set_global_opts(
						title_opts=opts.TitleOpts(title="Variations for H3(AAVI)", subtitle="human H3"))
				)
			elif self.ui.comboBoxHANA_html.currentIndex() == 2 and self.ui.comboBoxIndex_html.currentIndex() == 1:  # NA + AAVI
				# get data
				data_file = os.path.join(working_prefix, '..', 'Resources', 'Data', 'NA_AAVI.csv')
				if os.path.exists(data_file):
					pass
				else:
					return

				csvFile = open(data_file, "r")
				reader = csv.reader(csvFile)
				data_array = []
				for item in reader:
					item = list(map(float, item))
					data_array.append(item)
				# generate local HTML
				line = (
					Line(init_opts=opts.InitOpts(width="900px", height="380px"))
						.add_xaxis(range(1, len(data_array[0]) + 1))
						.add_yaxis("N1", data_array[0], is_symbol_show=False)
						.add_yaxis("N2", data_array[1], is_symbol_show=False)
						.add_yaxis("N3", data_array[2], is_symbol_show=False)
						.add_yaxis("N4", data_array[3], is_symbol_show=False)
						.add_yaxis("N5", data_array[4], is_symbol_show=False)
						.add_yaxis("N6", data_array[5], is_symbol_show=False)
						.add_yaxis("N7", data_array[6], is_symbol_show=False)
						.add_yaxis("N8", data_array[7], is_symbol_show=False)
						.add_yaxis("N9", data_array[8], is_symbol_show=False)
						.set_global_opts(
						title_opts=opts.TitleOpts(title="Variations for NA(AAVI)", subtitle="human NA"))
				)

			html_path = os.path.join(temp_folder, 'test3.html')
			line.render(path=html_path)
			# adjust the window size seting
			file_handle = open(html_path, 'r')
			lines = file_handle.readlines()
			file_handle.close()
			# edit js line
			js_line = '            <script type="text/javascript" src="' + \
			          os.path.join(working_prefix, '..', 'Resources', 'Js', 'echarts.min.js') + '"></script>'
			lines[5] = js_line
			# edit style line
			style_line = lines[9]
			style_pos = style_line.find('style')
			style_line = style_line[
			             0:style_pos] + 'style="position: fixed; top: 0px; left: 5%;width:90%; height:' + str(
				self.ui.HTMLview3.h - 20) + 'px;"></div>'
			lines[9] = style_line
			content = '\n'.join(lines)
			file_handle = open(html_path, 'w')
			file_handle.write(content)
			file_handle.close()
			# show local HTML
			self.ui.HTMLview3.load(QUrl('file://' + html_path))
			self.ui.HTMLview3.show()

	def clearTable(self):
		self.ui.tableWidget.setRowCount(0)
		self.ui.tableWidget.setColumnCount(0)

	def resizeHTML(self, w, h):
		if DBFilename == 'none':
			return
		h = h - 20
		sender = self.sender()
		a = sender.id
		if sender.id == 1:
			######  plot stat for subtype
			# get data
			SQLStatement = 'SELECT Subtype FROM LibDB'
			DataIn = RunSQL(DBFilename, SQLStatement)
			data = []
			for element in DataIn:
				data.append(element[0])
			result = Counter(data)
			labels = result.keys()
			values = result.values()
			# generate local HTML
			html_path = os.path.join(temp_folder, 'test1.html')
			pie = (
				Pie(init_opts=opts.InitOpts(width="380px", height="380px"))
					.add('', [list(z) for z in zip(labels, values)], radius=["40%", "75%"], )
					.set_global_opts(title_opts=opts.TitleOpts(title=""))
					.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
			)
			pie.render(path=html_path)
			# adjust the window size seting
			file_handle = open(html_path, 'r')
			lines = file_handle.readlines()
			file_handle.close()
			# edit js line
			js_line = '            <script type="text/javascript" src="' +\
			          os.path.join(working_prefix,'..','Resources','Js','echarts.min.js') + '"></script>'
			lines[5] = js_line
			#edit style line
			style_line = lines[9]
			style_pos = style_line.find('style')
			style_line = style_line[0:style_pos] + 'style="position: fixed; top: 0px; left: 5%;width:90%; height:' + str(h) + 'px;"></div>'
			lines[9] = style_line
			content = '\n'.join(lines)
			file_handle = open(html_path, 'w')
			file_handle.write(content)
			file_handle.close()
			# show local HTML
			self.ui.HTMLview1.load(QUrl('file://' + html_path))
			self.ui.HTMLview1.show()
		elif sender.id == 2:
			######  plot stat for Role
			# get data
			SQLStatement = 'SELECT Role FROM LibDB'
			DataIn = RunSQL(DBFilename, SQLStatement)
			data = []
			for element in DataIn:
				data.append(element[0])
			result = Counter(data)
			labels = result.keys()
			values = result.values()
			# generate local HTML
			html_path = os.path.join(temp_folder, 'test2.html')
			pie = (
				Pie(init_opts=opts.InitOpts(width="380px", height="380px"))
					.add('', [list(z) for z in zip(labels, values)], radius=["40%", "75%"], )
					.set_global_opts(title_opts=opts.TitleOpts(title=""))
					.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
			)
			pie.render(path=html_path)
			# adjust the window size seting
			file_handle = open(html_path, 'r')
			lines = file_handle.readlines()
			file_handle.close()
			# edit js line
			js_line = '            <script type="text/javascript" src="' + \
			          os.path.join(working_prefix, '..', 'Resources', 'Js', 'echarts.min.js') + '"></script>'
			lines[5] = js_line
			# edit style line
			style_line = lines[9]
			style_pos = style_line.find('style')
			style_line = style_line[
			             0:style_pos] + 'style="position: fixed; top: 0px; left: 5%;width:90%; height:' + str(
				h) + 'px;"></div>'
			lines[9] = style_line
			content = '\n'.join(lines)
			file_handle = open(html_path, 'w')
			file_handle.write(content)
			file_handle.close()
			# show local HTML
			self.ui.HTMLview2.load(QUrl('file://' + html_path))
			self.ui.HTMLview2.show()
		elif sender.id == 3:
			######  plot stat for H1
			# get data
			self.reloadHTML()

	def connectDB(self):
		SQLStatement = 'SELECT * FROM Fragments ORDER BY Name DESC'
		if self.ui.FragmentTab.currentIndex() == 0:     # connect to local sqLite DB
			F_db_name = self.ui.dbpath.text()
			try:
				DataIn = RunSQL(F_db_name, SQLStatement)
			except:
				Msg = 'Can not connect to the Fragment DB! Please chekc your input!'
				QMessageBox.warning(self, 'Warning', Msg, QMessageBox.Ok, QMessageBox.Ok)
				return
		else:                                           # connect to remote MySQL DB
			server_ip = self.ui.IPinput.text()
			server_port = self.ui.Portinput.text()
			db_name = self.ui.DBnameinput.text()
			db_user = self.ui.Userinput.text()
			db_pass = self.ui.Passinput.text()

			db_config = [server_ip, server_port, db_name, db_user, db_pass]
			try:
				DataIn = RunMYSQL(db_config, SQLStatement)
			except:
				Msg = 'Can not connect to the Fragment DB! Please chekc your input!'
				QMessageBox.warning(self, 'Warning', Msg, QMessageBox.Ok, QMessageBox.Ok)
				return

		num_row = len(DataIn)
		num_col = 9
		self.ui.tableWidget.setRowCount(num_row)
		self.ui.tableWidget.setColumnCount(num_col)

		horizontalHeader = ['Name', 'Segment', 'Fragment', 'Subtype', 'ID', 'Template', 'AA seq', 'NT seq', 'In stock']
		self.ui.tableWidget.setHorizontalHeaderLabels(horizontalHeader)
		self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
		self.ui.tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
		self.ui.tableWidget.horizontalHeader().setSectionResizeMode(1,QtWidgets.QHeaderView.Fixed)
		self.ui.tableWidget.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Fixed)
		self.ui.tableWidget.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Fixed)
		self.ui.tableWidget.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Fixed)
		self.ui.tableWidget.horizontalHeader().setSectionResizeMode(8, QtWidgets.QHeaderView.Fixed)
		self.ui.tableWidget.setColumnWidth(0, 100)
		self.ui.tableWidget.setColumnWidth(1, 60)
		self.ui.tableWidget.setColumnWidth(2, 60)
		self.ui.tableWidget.setColumnWidth(3, 60)
		self.ui.tableWidget.setColumnWidth(4, 50)
		self.ui.tableWidget.setColumnWidth(8, 60)

		for row_index in range(num_row):
			for col_index in range(num_col):
				if col_index != 8:
					self.ui.tableWidget.setItem(row_index, col_index, QTableWidgetItem(DataIn[row_index][col_index]))
				else:
					cell_comBox = QComboBox()
					cell_comBox.addItems(['Yes', 'No'])
					if DataIn[row_index][col_index] == 'yes':
						cell_comBox.setCurrentIndex(0)
					else:
						cell_comBox.setCurrentIndex(1)
					#cell_comBox.setStyleSheet('QComboBox{margin:3px}')
					cell_comBox.currentIndexChanged.connect(self.changeInStock)
					cell_comBox.name = DataIn[row_index][0]
					cell_comBox.ignore = 0
					self.ui.tableWidget.setCellWidget(row_index, col_index, cell_comBox)

		# show sort indicator
		self.ui.tableWidget.horizontalHeader().setSortIndicatorShown(True)
		# connect sort indicator to slot function
		self.ui.tableWidget.horizontalHeader().sectionClicked.connect(self.sortTable)

	def changeInStock(self):
		sender = self.sender()
		if sender.ignore != 0:
			return
		name = sender.name
		index = sender.currentText()

		question = 'Are you sure you want change instock status of ' + name + ' to ' + index + '?'
		buttons = 'YN'
		answer = questionMessage(self, question, buttons)
		if answer == 'No':
			sender.ignore = 1
			if index == 'Yes':
				sender.setCurrentIndex(1)
			else:
				sender.setCurrentIndex(0)
			sender.ignore = 0
			return
		else:
			SQLStatement = 'UPDATE Fragments SET `Instock`="' + index.lower() + '" WHERE `Name` = "' + name + '"'
			if self.ui.FragmentTab.currentIndex() == 0: #local DB
				F_db_name = self.ui.dbpath.text()
				RunInsertion(F_db_name, SQLStatement)
			else:   # remote DB
				server_ip = self.ui.IPinput.text()
				server_port = self.ui.Portinput.text()
				db_name = self.ui.DBnameinput.text()
				db_user = self.ui.Userinput.text()
				db_pass = self.ui.Passinput.text()

				db_config = [server_ip, server_port, db_name, db_user, db_pass]
				RunMYSQLInsertion(db_config, SQLStatement)

			Msg = 'Update successfully!'
			QMessageBox.information(self, 'information', Msg, QMessageBox.Ok,
			                        QMessageBox.Ok)

	def sortTable(self, index):
		self.ui.tableWidget.sortByColumn(index, self.ui.tableWidget.horizontalHeader().sortIndicatorOrder())

	def determineFile(self):
		global temp_folder
		out_dir, _ = QFileDialog.getOpenFileName(self, "select existing fragment DB", temp_folder,
		                                         "Librator database Files (*.ldb);;All Files (*)")
		if out_dir == '':
			return
		# check if this is the right DB
		SQLStatement = 'SELECT * FROM Fragments ORDER BY Name DESC LIMIT 1 '
		try:
			DataIn = RunSQL(out_dir, SQLStatement)
		except:
			QMessageBox.warning(self, 'Warning', 'There is no Fragments table in the selected database!',
			                    QMessageBox.Ok,
			                    QMessageBox.Ok)
			return
		self.ui.dbpath.setText(out_dir)

	def resetSearch(self):
		self.ui.txtSearch.setPlainText('')

		textNT = self.ui.textSeq.toPlainText()
		cursorNT = self.ui.textSeq.textCursor()
		textAA = self.ui.textAA.toPlainText()
		cursorAA = self.ui.textAA.textCursor()

		format = QTextCharFormat()
		format.setBackground(QBrush(QColor("white")))
		format.setForeground(QBrush(QColor("black")))

		cursorNT.setPosition(0)
		cursorNT.setPosition(len(textNT), QTextCursor.KeepAnchor)
		cursorNT.mergeCharFormat(format)

		cursorAA.setPosition(0)
		cursorAA.setPosition(len(textAA), QTextCursor.KeepAnchor)
		cursorAA.mergeCharFormat(format)

	def on_actionGibsonClone_Setting_triggered(self):
		global H1_start_user
		global H3_start_user
		global NA_start_user
		self.modalessJointDialog = None
		self.modalessJointDialog = jointDialog()

		a = H1_start_user
		b = H3_start_user
		c = NA_start_user

		if len(H1_start_user) > 0:
			self.modalessJointDialog.ui.H1_F1_SU.setText(str(H1_start_user[0]))
			self.modalessJointDialog.ui.H1_F2_SU.setText(str(H1_start_user[1]))
			self.modalessJointDialog.ui.H1_F3_SU.setText(str(H1_start_user[2]))
			self.modalessJointDialog.ui.H1_F4_SU.setText(str(H1_start_user[3]))
			self.modalessJointDialog.ui.H1_F1_EU.setText(str(H1_end_user[0]))
			self.modalessJointDialog.ui.H1_F2_EU.setText(str(H1_end_user[1]))
			self.modalessJointDialog.ui.H1_F3_EU.setText(str(H1_end_user[2]))
			self.modalessJointDialog.ui.H1_F4_EU.setText(str(H1_end_user[3]))

		if len(H3_start_user) > 0:
			self.modalessJointDialog.ui.H3_F1_SU.setText(str(H3_start_user[0]))
			self.modalessJointDialog.ui.H3_F2_SU.setText(str(H3_start_user[1]))
			self.modalessJointDialog.ui.H3_F3_SU.setText(str(H3_start_user[2]))
			self.modalessJointDialog.ui.H3_F4_SU.setText(str(H3_start_user[3]))
			self.modalessJointDialog.ui.H3_F1_EU.setText(str(H3_end_user[0]))
			self.modalessJointDialog.ui.H3_F2_EU.setText(str(H3_end_user[1]))
			self.modalessJointDialog.ui.H3_F3_EU.setText(str(H3_end_user[2]))
			self.modalessJointDialog.ui.H3_F4_EU.setText(str(H3_end_user[3]))

		if len(NA_start_user) > 0:
			self.modalessJointDialog.ui.NA_F1_SU.setText(str(NA_start_user[0]))
			self.modalessJointDialog.ui.NA_F2_SU.setText(str(NA_start_user[1]))
			self.modalessJointDialog.ui.NA_F3_SU.setText(str(NA_start_user[2]))
			self.modalessJointDialog.ui.NA_F1_EU.setText(str(NA_end_user[0]))
			self.modalessJointDialog.ui.NA_F2_EU.setText(str(NA_end_user[1]))
			self.modalessJointDialog.ui.NA_F3_EU.setText(str(NA_end_user[2]))

		self.modalessJointDialog.show()

	def searchPattern(self):
		pattern = self.ui.txtSearch.toPlainText().upper()

		if self.ui.rdoDNA.isChecked():
			text = self.ui.textSeq.toPlainText()
			cursor = self.ui.textSeq.textCursor()
		else:
			text = self.ui.textAA.toPlainText()
			cursor = self.ui.textAA.textCursor()

		format = QTextCharFormat()
		format.setBackground(QBrush(QColor("white")))
		format.setForeground(QBrush(QColor("black")))
		cursor.setPosition(0)
		cursor.setPosition(len(text), QTextCursor.KeepAnchor)
		cursor.mergeCharFormat(format)

		format.setBackground(QBrush(QColor("red")))
		format.setForeground(QBrush(QColor("white")))
		try:
			pos_list = [i.start() for i in re.finditer(pattern, text)]
			if len(pos_list) > 0:
				for pos in pos_list:
					cursor.setPosition(pos)
					cursor.setPosition(pos + len(pattern), QTextCursor.KeepAnchor)
					cursor.mergeCharFormat(format)
		except Exception:
			pass


	@pyqtSlot()
	def UpdateRecent(self):
		global working_prefix
		self.ui.cboRecent.clear()
		self.ui.cboRecent.addItem('Open previous')
		record_file = os.path.join(working_prefix, '..', 'Resources', 'Conf', 'db_record.txt')
		if os.path.isfile(record_file):
			with open(record_file, 'r') as currentFile:
				RecentFiles = currentFile.readlines()
			currentFile.close()
			if len(RecentFiles) != 0:
				RecentFiles = RecentFiles[0]
				RecentFiles = RecentFiles.split(',')
				for file in RecentFiles:
					if file != '':
						if os.path.isfile(file):
							self.ui.cboRecent.addItem(file)
						else:
							RecentFiles.remove(file)
				RecentFiles_str = ','.join(RecentFiles)
				with open(record_file, 'w') as currentFile:
					currentFile.write(RecentFiles_str)
				currentFile.close()

	@pyqtSlot()
	def on_actionIncrease_font_size_triggered(self):

		if self.ui.tabWidget.currentIndex() == 2:
			val = int(self.ui.spnAlignFont.value())
			val += 1
			self.ui.spnAlignFont.setValue(val)
		elif self.ui.tabWidget.currentIndex() == 1:
			FontIs = self.ui.txtAASeq.currentFont()
			font = QFont(FontIs)

			FontSize = int(font.pointSize())
			if FontSize < 36:
				FontSize += 1
			font.setPointSize(FontSize)
			font.setFamily("Courier New")

			# self.ui.txtDNASeq.setFont(font)
			self.ui.txtAASeq.setFont(font)

	@pyqtSlot()
	def on_actionClean_triggered(self):
		global temp_folder

		question = 'Clean all TEMP files?'
		buttons = 'YN'
		answer = questionMessage(self, question, buttons)
		if answer == 'No':
			return
		else:
			cmd = 'cd ' + temp_folder + '; rm -rf ' + temp_folder + '/*'
			try:
				os.system(cmd)
			except:
				QMessageBox.warning(self, 'Warning', 'Fail to clear TEMP folder!', QMessageBox.Ok,
				                    QMessageBox.Ok)
				return

	@pyqtSlot()
	def on_actionExport_triggered(self):
		global DataIs

		# read sequences from database
		AlignIn = []
		listItems = self.ui.listWidgetStrainsIn.selectedItems()

		WhereState = ''
		NumSeqs = len(listItems)
		i = 1

		if len(listItems) == 0:
			QMessageBox.warning(self, 'Warning', 'Please select sequence from active sequence panel!', QMessageBox.Ok,
			                    QMessageBox.Ok)
			return
		for item in listItems:
			eachItemIs = item.text()
			WhereState += 'SeqName = "' + eachItemIs + '"'
			if NumSeqs > i:
				WhereState += ' OR '

			i += 1

		SQLStatement = 'SELECT SeqName, Sequence, Vfrom, VTo FROM LibDB WHERE ' + WhereState
		DataIn = RunSQL(DBFilename, SQLStatement)

		for item in DataIn:
			SeqName = item[0]
			Sequence = item[1]
			VFrom = int(item[2]) - 1
			if VFrom == -1: VFrom = 0

			VTo = int(item[3])
			Sequence = Sequence[VFrom:VTo]
			Sequence = Sequence.upper()
			EachIn = (SeqName, Sequence)
			AlignIn.append(EachIn)

		# get output file
		options = QtWidgets.QFileDialog.Options()
		OUTFilename, _ = QtWidgets.QFileDialog.getSaveFileName(self,
		                                                      "output file",
		                                                      "output file",
		                                                      "Fasta Files (*.fasta);;All Files (*)",
		                                                      options=options)
		if OUTFilename != '':
			out_handle = open(OUTFilename, 'w')
			for element in AlignIn:
				out_handle.write('>' + element[0] + '\n')
				out_handle.write(element[1] + '\n')
			out_handle.close()


	@pyqtSlot()
	def on_actionDecrease_font_size_triggered(self):

		if self.ui.tabWidget.currentIndex() == 2:
			val = int(self.ui.spnAlignFont.value())
			val -= 1
			self.ui.spnAlignFont.setValue(val)
		elif self.ui.tabWidget.currentIndex() == 1:
			FontIs = self.ui.txtAASeq.currentFont()
			font = QFont(FontIs)

			FontSize = int(font.pointSize())
			if FontSize > 3:
				FontSize -= 1
			font.setPointSize(FontSize)
			font.setFamily("Courier New")

			# self.ui.txtDNASeq.setFont(font)
			self.ui.txtAASeq.setFont(font)
		# elif self.ui.tabWidget.currentIndex() == 1:
		# 	FontIs = self.ui.tableView.font()
		# 	font = QFont(FontIs)
		#
		# 	FontSize = int(font.pointSize())
		# 	if FontSize > 7:
		# 		FontSize -= 1
		# 	font.setPointSize(FontSize)
		# 	font.setFamily('Lucida Grande')
		#
		# 	self.ui.tableView.setFont(font)

	@pyqtSlot()
	def on_spnAlignFont_valueChanged(self, value):
		self.AlignFont()

	@pyqtSlot()
	def AlignFont(self):
		FontSize = int(self.ui.spnAlignFont.text())
		font = QFont()
		font.setFamily("Courier New")
		font.setPointSize(FontSize)

		self.ui.txtSeqAlignment.setFont(font)

	@pyqtSlot()
	def on_btnEditSequence_clicked(self):
		self.open_update_dialog()

	@pyqtSlot()
	def on_btnImportBase_clicked(self):
		# SeqIndex = self.ui.listStrain_Base.currentIndex()
		SeqImport = self.ui.cmbListBase.currentText()

		if SeqImport == 'New':
			SeqInfoPacket = []
			filename = openFile(self, 'FASTA')
			HA_Read = ReadFASTA(filename)

			if len(HA_Read) == 0:
				answer = informationMessage(self, 'Please select a FASTA file of a full length HA beginning at the first coding nucleotide', 'OK')
				return

			for item in HA_Read:
				HAName = item[0]
				HASeq = item[1]

			HAAA = Translator(HASeq.upper(),0)

			items = ('H1','H2','H3','H4','H5','H6','H7','H8','H9','H10','H11','H12','H13','H14','H15','H16','H17',
			         'H18','N1','N2','N3','N4','N5','N6','N7','N8','N9','N10','N11','B','Other')
			title = 'Choose infleunza subtype:'
			subtype = setItem(self, items, title)
			self.ui.cmbSubtypes_Base.setCurrentText(subtype)
			if subtype == "Cancel":
				subtype = 'none'
				return

			items = ('Full HA', 'Probe HA', "Full NA", "Probe NA", 'Other')
			title = 'Choose form of molecule:'
			form = setItem(self, items, title)
			self.ui.cmbForm_Base.setCurrentText(form)
			if subtype == "Cancel":
				form = 'none'
				return


			self.ui.textBaseSeq.setText(HASeq.upper())
			self.ui.textBaseAA.setText(HAAA[0])
			self.ui.textBaseSeqName.setText(HAName)
			blank = 'spaceholder'
			# SeqName text, Sequence text, SeqLen, SubType text, Form text,

			question = 'Would you like to enter the sequence into your database?'
			buttons = 'YN'
			answer = questionMessage(self, question, buttons)
			if answer == 'Yes':
				if DBFilename == 'none':
					items = ('New', 'Open', "Cancel")
					title = 'Choose an option'
					selection = setItem(self, items, title)
					self.ui.cmbSubtypes_Base.setCurrentText(subtype)
					if selection == "Cancel":
						return
					elif selection == 'New':
						self.on_action_New_triggered()
					elif selection == 'Open':
						self.on_action_Open_triggered()


				ItemIn = (HAName, HASeq, str(len(HASeq)), subtype, form, blank)
				SeqInfoPacket.append(ItemIn)

	@pyqtSlot()
	def on_btnReadingFrames_clicked(self):
		self.AlignSequencesRF('RF', 'none')

	@pyqtSlot()
	def on_textSeq_cursorPositionChanged(self):
		self.UpdatePositions()
	@pyqtSlot()
	def UpdatePositions(self):
		StartP, EndP, LenSeq = self.get_text_selection()

		cursor = self.ui.textSeq.textCursor()
		if StartP == EndP:
			lblText = 'DNA Sequence: position = ' + str(EndP) + ' of ' + str(LenSeq) + ' total nucleotides'
		else:
			lblText = 'DNA Sequence: ' + str(StartP + 1) + ' to ' + str(EndP + 1) + ' (' + str(
				EndP - StartP) + ' bases) ' ' selected of ' + str(LenSeq) + ' total nucleotides'

		self.ui.lblDNA.setText(lblText)

	# def ChangeListName(self):

	@pyqtSlot()
	def FindSeq(self, SeqFind):

		FindSeq = SeqFind
		if self.ui.rdoDNA.isChecked():
			Found = self.ui.textSeq.find(FindSeq)
			self.ui.textSeq.setFocus()
			# self.ui.textSeq.scroll(100,100)


		elif self.ui.rdoAA.isChecked():
			Found = self.ui.textAA.find(FindSeq)
			self.ui.textAA.setFocus()
		#
		# if Found == False:
		# 	# self.SeqButton('none')
		# 	Found = self.ui.txtAASeq.find(FindSeq)

		if Found == False:
			msg = SeqFind + ' could not be found.'
			buttons = 'OK'
			answer = informationMessage(self, msg, buttons)

		# self.UpdatePositions()

		return Found
	@pyqtSlot()
	def SeqButton(self, button):
		global JustMoved

		cursor = self.ui.textSeq.textCursor()
		AAcursor = self.ui.textAA.textCursor()
		StartSel = 0
		EndSel = 0

		cursor.setPosition(StartSel)
		cursor.setPosition(EndSel, QTextCursor.KeepAnchor)
		if StartSel != 0:
			AAStartSel = StartSel / 3
		else:
			AAStartSel = StartSel
		if EndSel != 0:
			AAEndSel = EndSel / 3
		else:
			AAEndSel = EndSel

		AAcursor.setPosition(AAStartSel)
		AAcursor.setPosition(AAEndSel, QTextCursor.KeepAnchor)


	@pyqtSlot()
	def get_text_selection(self):
		cursor = self.ui.textSeq.textCursor()
		DNAseq = self.ui.textSeq.toPlainText()
		lenSeq = len(DNAseq)
		return cursor.selectionStart(), cursor.selectionEnd(), lenSeq


	@pyqtSlot()
	def on_textAA_cursorPositionChanged(self):
		self.UpdatePositionsAA()

	@pyqtSlot()
	def UpdatePositionsAA(self):
		StartP, EndP, LenSeq = self.get_text_selectionAA()

		cursor = self.ui.textAA.textCursor()
		if StartP == EndP:
			lblText = 'Amino Acid Sequence: position = ' + str(EndP+1) + ' of ' + str(LenSeq+1) + ' total residues'


		else:
			lblText = 'Amino Acid Sequence: ' + str(StartP + 1) + ' to ' + str(EndP + 1) + ' (' + str(
				EndP - StartP) + ' bases) ' ' selected of ' + str(LenSeq) + ' total residues'


		self.ui.lblAA.setText(lblText)

	@pyqtSlot()
	def get_text_selectionAA(self):
		cursor = self.ui.textAA.textCursor()
		AAseq = self.ui.textAA.toPlainText()
		lenSeq = len(AAseq)
		return cursor.selectionStart(), cursor.selectionEnd(), lenSeq

	@pyqtSlot()
	def on_actionTree_triggered(self):
		global DataIs
		global DBFilename
		global temp_folder
		global raxml_path
		global figtree_path

		listItems = self.ui.listWidgetStrainsIn.selectedItems()
		# if not listItems: return
		WhereState = ''
		NumSeqs = len(listItems)
		i = 1
		if len(listItems) == 0:
			QMessageBox.warning(self, 'Warning', 'Please select sequence from active sequence panel!', QMessageBox.Ok,
			                    QMessageBox.Ok)
			return
		elif len(listItems) < 4:
			QMessageBox.warning(self, 'Warning', 'Please select at least 4 sequences from active sequence panel!',
			 					QMessageBox.Ok, QMessageBox.Ok)
			return
		elif len(listItems) > 100:
			QMessageBox.warning(self, 'Warning', 'Max sequence number is limited to 100!',
			                    QMessageBox.Ok, QMessageBox.Ok)
			return

		for item in listItems:
			eachItemIs = item.text()
			WhereState += 'SeqName = "' + eachItemIs + '"'
			if NumSeqs > i:
				WhereState += ' OR '
			i += 1

		SQLStatement = 'SELECT SeqName, Sequence, Vfrom, VTo FROM LibDB WHERE ' + WhereState
		DataIn = RunSQL(DBFilename, SQLStatement)

		# write sequences into file
		time_stamp = str(int(time.time() * 100))
		this_folder = os.path.join(temp_folder, time_stamp)
		cmd = 'mkdir ' + this_folder
		try:
			os.system(cmd)
		except:
			QMessageBox.warning(self, 'Warning', 'Fail to make temp folder! Check your path setting!', QMessageBox.Ok,
			                    QMessageBox.Ok)
			return

		aafilename = this_folder + "/input.fas"
		outfilename = this_folder + "/alignment.fas"
		treefilename = 'tree'
		out_handle = open(aafilename, 'w')

		for item in DataIn:
			SeqName = item[0]
			Sequence = item[1]
			VFrom = int(item[2]) - 1
			if VFrom == -1: VFrom = 0

			VTo = int(item[3])
			Sequence = Sequence[VFrom:VTo]
			Sequence = Sequence.upper()
			AAseq = Translator(Sequence,0)

			# parse seq name
			SeqName = re.sub(r'[^\w\d\/\>]','_', SeqName)
			SeqName = re.sub(r'_+', '_', SeqName)
			SeqName = SeqName.strip('_')

			out_handle.write('>' + SeqName + '\n')
			out_handle.write(AAseq[0] + '\n')
		out_handle.close()

		# alignment
		cmd = muscle_path
		cmd += " -in " + aafilename + " -out " + outfilename
		try:
			os.system(cmd)
		except:
			QMessageBox.warning(self, 'Warning', 'Fail to run muscle! Check your muscle path!', QMessageBox.Ok, QMessageBox.Ok)
			return

		# open dialog, review alignment
		seq_names = []
		seq_seqs = []
		tmp_seq = ''
		file_handle = open(outfilename, 'r')
		for line in file_handle:
			Readline = line.replace('\n', '').replace('\r', '')
			if len(Readline) > 0:
				if Readline[0] == '>':
					Readline = Readline.replace('>', '')
					seq_names.append(Readline)
					if tmp_seq != '':
						seq_seqs.append(tmp_seq)
						tmp_seq = ''
				else:
					tmp_seq += Readline
		seq_seqs.append(tmp_seq)

		self.open_tree_dialog(seq_names, seq_seqs, this_folder)


	@pyqtSlot()
	def on_actionNTTree_triggered(self):
		global DataIs
		global DBFilename
		global temp_folder
		global raxml_path
		global figtree_path

		listItems = self.ui.listWidgetStrainsIn.selectedItems()
		# if not listItems: return
		WhereState = ''
		NumSeqs = len(listItems)
		i = 1
		if len(listItems) == 0:
			QMessageBox.warning(self, 'Warning', 'Please select sequence from active sequence panel!', QMessageBox.Ok,
			                    QMessageBox.Ok)
			return
		elif len(listItems) < 4:
			QMessageBox.warning(self, 'Warning', 'Please select at least 4 sequences from active sequence panel!',
			                    QMessageBox.Ok, QMessageBox.Ok)
			return
		elif len(listItems) > 100:
			QMessageBox.warning(self, 'Warning', 'Max sequence number is limited to 100!',
			                    QMessageBox.Ok, QMessageBox.Ok)
			return

		for item in listItems:
			eachItemIs = item.text()
			WhereState += 'SeqName = "' + eachItemIs + '"'
			if NumSeqs > i:
				WhereState += ' OR '
			i += 1

		SQLStatement = 'SELECT SeqName, Sequence, Vfrom, VTo FROM LibDB WHERE ' + WhereState
		DataIn = RunSQL(DBFilename, SQLStatement)

		# write sequences into file
		time_stamp = str(int(time.time() * 100))
		this_folder = os.path.join(temp_folder, time_stamp)
		cmd = 'mkdir ' + this_folder
		try:
			os.system(cmd)
		except:
			QMessageBox.warning(self, 'Warning', 'Fail to make temp folder!', QMessageBox.Ok,
			                    QMessageBox.Ok)
			return

		aafilename = this_folder + "/input.fas"
		outfilename = this_folder + "/alignment.fas"
		treefilename = 'tree'
		out_handle = open(aafilename, 'w')

		for item in DataIn:
			SeqName = item[0]
			Sequence = item[1]

			# parse seq name
			SeqName = re.sub(r'[^\w\d\/\>]', '_', SeqName)
			SeqName = re.sub(r'_+', '_', SeqName)
			SeqName = SeqName.strip('_')

			out_handle.write('>' + SeqName + '\n')
			out_handle.write(Sequence + '\n')
		out_handle.close()

		# alignment
		cmd = muscle_path
		cmd += " -in " + aafilename + " -out " + outfilename
		try:
			os.system(cmd)
		except:
			QMessageBox.warning(self, 'Warning', 'Fail to run muscle! Check your muscle path!', QMessageBox.Ok,
			                    QMessageBox.Ok)
			return

		# open dialog, review alignment
		seq_names = []
		seq_seqs = []
		tmp_seq = ''
		file_handle = open(outfilename, 'r')
		for line in file_handle:
			Readline = line.replace('\n', '').replace('\r', '')
			if len(Readline) > 0:
				if Readline[0] == '>':
					Readline = Readline.replace('>', '')
					seq_names.append(Readline)
					if tmp_seq != '':
						seq_seqs.append(tmp_seq)
						tmp_seq = ''
				else:
					tmp_seq += Readline
		seq_seqs.append(tmp_seq)

		self.open_tree_dialog(seq_names, seq_seqs, this_folder)

	@pyqtSlot()
	def on_actionMultiple_Alignement_triggered(self):
		print('run 222 \n')
		global DataIs
		global DBFilename

		AlignIn = []
		listItems = self.ui.listWidgetStrainsIn.selectedItems()
		# if not listItems: return
		WhereState = ''
		NumSeqs = len(listItems)
		i = 1
		if len(listItems) == 0:
			QMessageBox.warning(self, 'Warning', 'Please select sequence from active sequence panel!', QMessageBox.Ok,
								QMessageBox.Ok)
			return
		for item in listItems:
			eachItemIs = item.text()
			WhereState += 'SeqName = "' + eachItemIs + '"'
			if NumSeqs > i:
				WhereState += ' OR '
			i += 1

		SQLStatement = 'SELECT SeqName, Sequence, Vfrom, VTo FROM LibDB WHERE ' + WhereState
		DataIn = RunSQL(DBFilename, SQLStatement)
		for item in DataIn:
			SeqName = item[0]
			Sequence = item[1]
			VFrom = int(item[2]) - 1
			if VFrom == -1: VFrom = 0

			VTo = int(item[3])
			Sequence = Sequence[VFrom:VTo]
			Sequence = Sequence.upper()
			EachIn = (SeqName, Sequence)
			AlignIn.append(EachIn)

		Notes = ''
		self.AlignSequences(AlignIn, Notes)

	@pyqtSlot()
	def on_actionAlignmentHTML_triggered(self):
		global VGenesTextWindows
		# load data
		AlignIn = []
		listItems = self.ui.listWidgetStrainsIn.selectedItems()

		WhereState = ''
		NumSeqs = len(listItems)
		i = 1
		if len(listItems) == 0:
			QMessageBox.warning(self, 'Warning', 'Please select sequence from active sequence panel!',
			                    QMessageBox.Ok,
			                    QMessageBox.Ok)
			return
		for item in listItems:
			eachItemIs = item.text()
			WhereState += 'SeqName = "' + eachItemIs + '"'
			if NumSeqs > i:
				WhereState += ' OR '
			i += 1

		SQLStatement = 'SELECT SeqName, Sequence, Vfrom, VTo FROM LibDB WHERE ' + WhereState
		DataIn = RunSQL(DBFilename, SQLStatement)

		for item in DataIn:
			SeqName = item[0]
			Sequence = item[1]
			VFrom = int(item[2]) - 1
			if VFrom == -1: VFrom = 0

			VTo = int(item[3])
			Sequence = Sequence[VFrom:VTo]
			Sequence = Sequence.upper()
			EachIn = (SeqName, Sequence)
			AlignIn.append(EachIn)
		# make HTML
		html_file = AlignSequencesHTML(AlignIn)
		# delete close window objects
		del_list = []
		for id, obj in VGenesTextWindows.items():
			if obj.isVisible() == False:
				del_list.append(id)
		for id in del_list:
			del_obj = VGenesTextWindows.pop(id)

		# display
		window_id = int(time.time() * 100)
		VGenesTextWindows[window_id] = htmlDialog()
		VGenesTextWindows[window_id].id = window_id
		layout = QGridLayout(VGenesTextWindows[window_id])
		view = QWebEngineView(self)
		view.load(QUrl("file://" + html_file))
		view.show()
		layout.addWidget(view)
		VGenesTextWindows[window_id].show()

	@pyqtSlot()
	def FillAlignmentTab(self):
		global DBFilename
		global temp_folder
		global working_prefix
		global MoveNotChange

		AlignIn = []
		EachIn = ()

		if self.ui.tabWidget.currentIndex() == 2:
			self.ui.actionAA.setChecked(True)
			self.ui.actionDNA.setChecked(True)
			self.ui.actionBA.setChecked(False)
			#self.ui.listWidgetStrainsIn.selectAll()
			listItems = self.ui.listWidgetStrainsIn.selectedItems()
			WhereState = ''
			NumSeqs = len(listItems)
			# if not listItems: do nothing
			if NumSeqs < 1:
				pass
			else:
				i = 1
				for item in listItems:

					eachItemIs = item.text()
					WhereState += 'SeqName = "' + eachItemIs + '"'
					if NumSeqs > i:
						WhereState += ' OR '
					i += 1

				SQLStatement = 'SELECT SeqName, Sequence, Vfrom, VTo FROM LibDB WHERE ' + WhereState
				DataIn = RunSQL(DBFilename, SQLStatement)

				for item in DataIn:
					SeqName = item[0]
					Sequence = item[1]
					VFrom = int(item[2])-1
					if VFrom == -1: VFrom = 0

					VTo = int(item[3])
					Sequence = Sequence[VFrom:VTo]
					Sequence = Sequence.upper()
					EachIn = (SeqName, Sequence)
					AlignIn.append(EachIn)

				Notes = 'Tab'
				self.AlignSequences(AlignIn, Notes)

		elif self.ui.tabWidget.currentIndex() == 1:
			#displays all info about the selected sequence
			selection = self.ui.listWidgetStrainsIn.selectedItems()
			if len(selection) == 0:
				return

			Subtype = self.ui.cboSubtype.currentText()


			self.ui.cboSubtype_2.setCurrentText(Subtype)
			if Subtype in Group2:
				self.ui.btnH1Num.setChecked(False)
				self.ui.btnH3Num.setChecked(True)
			elif Subtype in Group1:
				self.ui.btnH1Num.setChecked(True)
				self.ui.btnH3Num.setChecked(False)
			elif Subtype in GroupNA or Subtype == 'B' or Subtype == 'Other':
				self.ui.btnH1Num.setChecked(False)
				self.ui.btnH3Num.setChecked(False)
			else:
				self.ui.btnH1Num.setChecked(False)
				self.ui.btnH3Num.setChecked(False)

			self.CheckDecorations()

		elif self.ui.tabWidget.currentIndex() == 3:
			if self.ui.SeqTable.columnCount() > 0:
				self.ui.SeqTable.itemChanged.disconnect(self.EditTableItem)
			self.ui.SeqTable.setColumnCount(0)
			self.ui.SeqTable.setRowCount(0)

			if DBFilename != '' and DBFilename != 'none':
				SQLStatement = 'SELECT * FROM LibDB ORDER BY SeqName DESC'
				DataIn = RunSQL(DBFilename, SQLStatement)

				num_row = len(DataIn)
				num_col = 13
				self.ui.SeqTable.setRowCount(num_row)
				self.ui.SeqTable.setColumnCount(num_col)

				horizontalHeader = ['SeqName', 'Sequence', 'SeqLen', 'Subtype', 'Form', 'VFrom', 'VTo', 'Active',
				                    'Role','Donor','Mutations','ID','Base']
				self.ui.SeqTable.setHorizontalHeaderLabels(horizontalHeader)
				self.ui.SeqTable.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Fixed)
				self.ui.SeqTable.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Fixed)
				self.ui.SeqTable.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Fixed)
				self.ui.SeqTable.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Fixed)
				self.ui.SeqTable.horizontalHeader().setSectionResizeMode(6, QtWidgets.QHeaderView.Fixed)
				self.ui.SeqTable.horizontalHeader().setSectionResizeMode(7, QtWidgets.QHeaderView.Fixed)
				self.ui.SeqTable.horizontalHeader().setSectionResizeMode(8, QtWidgets.QHeaderView.Fixed)
				self.ui.SeqTable.horizontalHeader().setSectionResizeMode(11, QtWidgets.QHeaderView.Fixed)
				self.ui.SeqTable.setColumnWidth(2, 60)
				self.ui.SeqTable.setColumnWidth(3, 80)
				self.ui.SeqTable.setColumnWidth(4, 60)
				self.ui.SeqTable.setColumnWidth(5, 60)
				self.ui.SeqTable.setColumnWidth(6, 50)
				self.ui.SeqTable.setColumnWidth(7, 60)
				self.ui.SeqTable.setColumnWidth(8, 100)
				self.ui.SeqTable.setColumnWidth(11, 40)

				for row_index in range(num_row):
					for col_index in range(num_col):
						unit = QTableWidgetItem(DataIn[row_index][col_index])
						unit.last_name = DataIn[row_index][col_index]
						self.ui.SeqTable.setItem(row_index, col_index,unit)

				# show sort indicator
				self.ui.SeqTable.horizontalHeader().setSortIndicatorShown(True)
				# connect sort indicator to slot function
				self.ui.SeqTable.horizontalHeader().sectionClicked.connect(self.sortTable)
				self.ui.SeqTable.itemChanged.connect(self.EditTableItem)

		elif self.ui.tabWidget.currentIndex() == 4:
			if DBFilename == 'none':
				return
			#  plot stat for subtype
			# get data
			SQLStatement = 'SELECT Subtype FROM LibDB'
			DataIn = RunSQL(DBFilename, SQLStatement)

			data = []
			for element in DataIn:
				data.append(element[0])
			result = Counter(data)
			labels = result.keys()
			values = result.values()
			colors = sns.color_palette("hls", len(values))

			F = MyFigure(width=3, height=3, dpi=160)
			F.axes.pie(values, colors=colors, radius=1.0, pctdistance = 0.8,autopct='%1.1f%%',startangle=90)
			F.fig.legend(labels, title = 'Subtype')
			x = [1, 0, 0, 0]
			F.axes.pie(x, colors = 'w', radius=0.6)

			if self.fig == 0:
				gridlayout_fig1 = QGridLayout(self.ui.groupBox1)
			else:
				gridlayout_fig1 = self.ui.groupBox1.layout()
				for i in range(gridlayout_fig1.count()):
					gridlayout_fig1.itemAt(i).widget().deleteLater()
			gridlayout_fig1.addWidget(F,0,1)

			#  plot stat for Role
			# get data
			SQLStatement = 'SELECT Role FROM LibDB'
			DataIn = RunSQL(DBFilename, SQLStatement)

			data = []
			for element in DataIn:
				data.append(element[0])
			result = Counter(data)
			labels = result.keys()
			values = result.values()
			colors = sns.color_palette("hls", len(values))

			F = MyFigure(width=3, height=3, dpi=160)
			F.axes.pie(values,  colors=colors, radius=1.0, pctdistance = 0.8,autopct='%1.1f%%',startangle=90)
			F.fig.legend(labels, title = 'Role')
			x = [1, 0, 0, 0]
			F.axes.pie(x, colors='w', radius=0.6)

			if self.fig == 0:
				gridlayout_fig2 = QGridLayout(self.ui.groupBox2)
			else:
				gridlayout_fig2 = self.ui.groupBox2.layout()
				for i in range(gridlayout_fig2.count()):
					gridlayout_fig2.itemAt(i).widget().deleteLater()
			gridlayout_fig2.addWidget(F, 0, 1)

			#  plot stat for something
			# get data
			if self.fig == 0:
				self.ui.comboBoxHANA = QComboBox()
				self.ui.comboBoxHANA.addItem("H1/Group1")
				self.ui.comboBoxHANA.addItem("H3/Group2")
				self.ui.comboBoxHANA.addItem("NA")
				self.ui.comboBoxHANA.currentIndexChanged.connect(self.FigChange)

				self.ui.comboBoxIndex = QComboBox()
				self.ui.comboBoxIndex.addItem("Percentage of Variation")
				self.ui.comboBoxIndex.addItem("Amino Acid Variation Index")
				self.ui.comboBoxIndex.currentIndexChanged.connect(self.FigChange)

				self.Stat_fig()

				gridlayout_fig3 = QGridLayout(self.ui.groupBox3)
				gridlayout_fig3.addWidget(self.ui.comboBoxHANA, 1, 0)
				gridlayout_fig3.addWidget(self.ui.comboBoxIndex, 1, 1)
				gridlayout_fig3.addWidget(self.F, 2, 0, 10, 0)

				self.fig = 1
		elif self.ui.tabWidget.currentIndex() == 5:
			if DBFilename == 'none':
				return
			if self.ui.HTMLview1.h != 0:
				######  plot stat for subtype
				# get data
				SQLStatement = 'SELECT Subtype FROM LibDB'
				DataIn = RunSQL(DBFilename, SQLStatement)
				data = []
				for element in DataIn:
					data.append(element[0])
				result = Counter(data)
				labels = result.keys()
				values = result.values()
				# generate local HTML
				html_path = os.path.join(temp_folder, 'test1.html')
				pie = (
					Pie(init_opts=opts.InitOpts(width="380px",height="380px"))
					.add('', [list(z) for z in zip(labels, values)], radius=["40%", "75%"],)
					.set_global_opts(title_opts=opts.TitleOpts(title=""))
					.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
				)
				pie.render(path=html_path)
				# adjust the window size seting
				file_handle = open(html_path, 'r')
				lines = file_handle.readlines()
				file_handle.close()
				# edit js line
				js_line = '            <script type="text/javascript" src="' + \
				          os.path.join(working_prefix, '..', 'Resources', 'Js', 'echarts.min.js') + '"></script>'
				lines[5] = js_line
				# edit style line
				style_line = lines[9]
				style_pos = style_line.find('style')
				style_line = style_line[
				             0:style_pos] + 'style="position: fixed; top: 0px; left: 5%;width:90%; height:' + str(
					self.ui.HTMLview1.h - 20) + 'px;"></div>'
				lines[9] = style_line
				content = '\n'.join(lines)
				file_handle = open(html_path, 'w')
				file_handle.write(content)
				file_handle.close()
				# show local HTML
				self.ui.HTMLview1.load(QUrl('file://' + html_path))
				self.ui.HTMLview1.show()
			if self.ui.HTMLview2.h != 0:
				######  plot stat for Role
				# get data
				SQLStatement = 'SELECT Role FROM LibDB'
				DataIn = RunSQL(DBFilename, SQLStatement)
				data = []
				for element in DataIn:
					data.append(element[0])
				result = Counter(data)
				labels = result.keys()
				values = result.values()
				# generate local HTML
				html_path = os.path.join(temp_folder, 'test2.html')
				pie = (
					Pie(init_opts=opts.InitOpts(width="380px", height="380px"))
						.add('', [list(z) for z in zip(labels, values)], radius=["40%", "75%"],)
						.set_global_opts(title_opts=opts.TitleOpts(title=""))
						.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
				)
				pie.render(path=html_path)
				# adjust the window size seting
				file_handle = open(html_path, 'r')
				lines = file_handle.readlines()
				file_handle.close()
				# edit js line
				js_line = '            <script type="text/javascript" src="' + \
				          os.path.join(working_prefix, '..', 'Resources', 'Js', 'echarts.min.js') + '"></script>'
				lines[5] = js_line
				# edit style line
				style_line = lines[9]
				style_pos = style_line.find('style')
				style_line = style_line[
				             0:style_pos] + 'style="position: fixed; top: 0px; left: 5%;width:90%; height:' + str(
					self.ui.HTMLview2.h - 20) + 'px;"></div>'
				lines[9] = style_line
				content = '\n'.join(lines)
				file_handle = open(html_path, 'w')
				file_handle.write(content)
				file_handle.close()
				# show local HTML
				self.ui.HTMLview2.load(QUrl('file://' + html_path))
				self.ui.HTMLview2.show()
			if self.ui.HTMLview3.h != 0:
				######  plot stat for H1
				# get data
				data_file = os.path.join(working_prefix, '..', 'Resources', 'Data', 'H1_PCT.csv')
				if os.path.exists(data_file):
					pass
				else:
					return

				csvFile = open(data_file, "r")
				reader = csv.reader(csvFile)
				data_array = []
				for item in reader:
					item = list(map(float, item))
					data_array.append(item)
				# generate local HTML
				line = (
					Line(init_opts=opts.InitOpts(width="900px", height="380px"))
						.add_xaxis(range(1, len(data_array[0]) + 1))
						.add_yaxis("Season H1", data_array[0], is_symbol_show=False)
						.add_yaxis("pdm09 H1", data_array[1], is_symbol_show=False)
						.set_global_opts(title_opts=opts.TitleOpts(title="Pct of variations for H1", subtitle="seasonal/pdm09"))
				)
				html_path = os.path.join(temp_folder, 'test3.html')
				line.render(path=html_path)
				# adjust the window size seting
				file_handle = open(html_path, 'r')
				lines = file_handle.readlines()
				file_handle.close()
				# edit js line
				js_line = '            <script type="text/javascript" src="' + \
				          os.path.join(working_prefix, '..', 'Resources', 'Js', 'echarts.min.js') + '"></script>'
				lines[5] = js_line
				# edit style line
				style_line = lines[9]
				style_pos = style_line.find('style')
				style_line = style_line[
				             0:style_pos] + 'style="position: fixed; top: 0px; left: 5%;width:90%; height:' + str(
					self.ui.HTMLview3.h - 20) + 'px;"></div>'
				lines[9] = style_line
				content = '\n'.join(lines)
				file_handle = open(html_path, 'w')
				file_handle.write(content)
				file_handle.close()
				# show local HTML
				self.ui.HTMLview3.load(QUrl('file://' + html_path))
				self.ui.HTMLview3.show()
		elif self.ui.tabWidget.currentIndex() == 6:
			mysql_setting_file = os.path.join(working_prefix, '..', 'Resources', 'Conf', 'mysql_setting.txt')

			if os.path.exists(mysql_setting_file):
				my_open = open(mysql_setting_file, 'r')
				my_info = my_open.readlines()
				my_open.close()
				my_info = my_info[0]
			else:
				file_handle = open(mysql_setting_file, 'w')
				my_info = ',,,,'
				file_handle.write(my_info)
				file_handle.close()

			my_info = my_info.strip('\n')
			if my_info != '':
				Setting = my_info.split(',')

				self.ui.IPinput.setText(Setting[0])
				self.ui.Portinput.setText(Setting[1])
				self.ui.DBnameinput.setText(Setting[2])
				self.ui.Userinput.setText(Setting[3])
				self.ui.Passinput.setText(Setting[4])

			self.ui.dbpath.setText(fragmentdb_path)
		elif self.ui.tabWidget.currentIndex() == 7:
			# load data
			AlignIn = []
			listItems = self.ui.listWidgetStrainsIn.selectedItems()
			# if not listItems: return
			WhereState = ''
			NumSeqs = len(listItems)
			i = 1

			if len(listItems) == 0:
				layout = self.ui.MSAgroupBox.layout()
				if layout == None:
					layout = QGridLayout(self.ui.MSAgroupBox)
				else:
					for i in range(layout.count()):
						layout.removeWidget(layout.itemAt(i).widget())
				return

			for item in listItems:
				eachItemIs = item.text()
				WhereState += 'SeqName = "' + eachItemIs + '"'
				if NumSeqs > i:
					WhereState += ' OR '
				i += 1

			SQLStatement = 'SELECT SeqName, Sequence, Vfrom, VTo FROM LibDB WHERE ' + WhereState
			DataIn = RunSQL(DBFilename, SQLStatement)

			for item in DataIn:
				SeqName = item[0]
				Sequence = item[1]
				VFrom = int(item[2]) - 1
				if VFrom == -1: VFrom = 0

				VTo = int(item[3])
				Sequence = Sequence[VFrom:VTo]
				Sequence = Sequence.upper()
				EachIn = (SeqName, Sequence)
				AlignIn.append(EachIn)
			# make HTML
			html_file = AlignSequencesHTML(AlignIn)
			# display
			view = QWebEngineView()
			view.load(QUrl("file://" + html_file))
			view.show()

			layout = self.ui.MSAgroupBox.layout()
			if layout == None:
				layout = QGridLayout(self.ui.MSAgroupBox)
			else:
				for i in range(layout.count()):
					layout.removeWidget(layout.itemAt(i).widget())
			layout.addWidget(view)

	def EditTableItem(self,item):
		global MoveNotChange
		if MoveNotChange:
			return

		row = item.row()
		col = item.column()
		CurVal = item.text()

		horizontalHeader = ['SeqName', 'Sequence', 'SeqLen', 'Subtype', 'Form', 'VFrom', 'VTo', 'Active',
		                    'Role', 'Donor', 'Mutations', 'ID', 'Base']
		col_name = horizontalHeader[col]
		SeqName = self.ui.SeqTable.item(row, 0).text()
		if col == 0:    #  update sequence name
			SeqName = item.last_name
			try:
				self.UpdateSeq(SeqName, CurVal, col_name)
				item.last_name = CurVal
			except:
				MoveNotChange = True
				self.ui.SeqTable.item(row,col).setText(SeqName)
				MoveNotChange = False
				QMessageBox.warning(self, 'Warning',
				                    'The name:\n' + CurVal + '\nhas been taken! Please choose another name!',
				                    QMessageBox.Ok,
				                    QMessageBox.Ok)
		elif col == 3:
			sub_type_list = ['H1','H2','H3','H4','H5','H6','H7','H8','H9','H10','H11','H12','H13','H14','H15',
			                 'H16','H17','H18','N1','N2','N3','N4','N5','N6','N7','N8','N9','N10','N11','B','Other']
			if CurVal in sub_type_list:
				self.UpdateSeq(SeqName, CurVal, col_name)
				item.last_name = CurVal
			else:
				MoveNotChange = True
				item.setText(item.last_name)
				MoveNotChange = False
				QMessageBox.warning(self, 'Warning',
				                    'The subtype:\n' + CurVal + '\nis not a valid subtype!\n' + 'Please choose from \n' + '\n'.join(sub_type_list),
				                    QMessageBox.Ok,
				                    QMessageBox.Ok)

		elif col == 4:
			form_list = ['Full HA', 'Probe HA', 'Full NA', 'Probe NA', 'Other']
			if CurVal in form_list:
				self.UpdateSeq(SeqName, CurVal, col_name)
				item.last_name = CurVal
			else:
				MoveNotChange = True
				item.setText(item.last_name)
				MoveNotChange = False
				QMessageBox.warning(self, 'Warning',
				                    'The Form:\n' + CurVal + '\nis not a valid Form!\n' + 'Please choose from \n' + '\n'.join(form_list),
				                    QMessageBox.Ok,
				                    QMessageBox.Ok)
		elif col == 5:
			try:
				CurVal = int(CurVal)
				if CurVal > 0:
					self.UpdateSeq(SeqName, str(CurVal), col_name)
					item.last_name = str(CurVal)
			except:
				MoveNotChange = True
				item.setText(item.last_name)
				MoveNotChange = False
				QMessageBox.warning(self, 'Warning',
				                    'The value:\n' + str(CurVal) + '\nis not a valid int number!',
				                    QMessageBox.Ok,
				                    QMessageBox.Ok)
		elif col == 6:
			try:
				CurVal = int(CurVal)
				if CurVal > 0:
					self.UpdateSeq(SeqName, str(CurVal), col_name)
					item.last_name = str(CurVal)
			except:
				MoveNotChange = True
				item.setText(item.last_name)
				MoveNotChange = False
				QMessageBox.warning(self, 'Warning',
				                    'The value:\n' + str(CurVal) + '\nis not a valid int number!',
				                    QMessageBox.Ok,
				                    QMessageBox.Ok)
		elif col == 7:
			active_list = ['False', 'True']
			if CurVal in active_list:
				self.UpdateSeq(SeqName, CurVal, col_name)
				item.last_name = CurVal
			else:
				MoveNotChange = True
				item.setText(item.last_name)
				MoveNotChange = False
				QMessageBox.warning(self, 'Warning',
				                    'The value:\n' + CurVal + '\nis not valid!\n The value only can be True or False!',
				                    QMessageBox.Ok,
				                    QMessageBox.Ok)
		elif col == 8:
			role_list = ['Unassigned', 'Generated','Reference']
			if CurVal in role_list:
				self.UpdateSeq(SeqName, CurVal, col_name)
				item.last_name = CurVal
			elif CurVal == 'BaseSeq':
				MoveNotChange = True
				item.setText(item.last_name)
				MoveNotChange = False
				QMessageBox.warning(self, 'Warning',
				                    'You can not determine Base Sequence here! Please use Main tab!',
				                    QMessageBox.Ok,
				                    QMessageBox.Ok)
			else:
				MoveNotChange = True
				item.setText(item.last_name)
				MoveNotChange = False
				QMessageBox.warning(self, 'Warning',
				                    'The value:\n' + CurVal + '\nis not valid!\n The value only can be Unassigned, Generated or Reference!',
				                    QMessageBox.Ok,
				                    QMessageBox.Ok)
		else:
			self.UpdateSeq(SeqName, CurVal, col_name)

	def FigChange(self):
		sip.delete(self.F)
		self.Stat_fig()
		#self.ui.groupBox3.layout().itemAt(2).widget().deleteLater()
		self.ui.groupBox3.layout().addWidget(self.F, 2, 0, 10, 0)

	def Stat_fig(self):
		global H1_start, H1_end, H3_start, H3_end, NA_start, NA_end, working_prefix
		global H3_start_user, H3_end_user, H1_start_user, H1_end_user, NA_end_user, NA_start_user

		H1_joint = []
		for i in range(0,len(H1_start)-1):
			cur_joint = [H1_start[i+1], H1_end[i]]
			H1_joint.append(cur_joint)
		H3_joint = []
		for i in range(0, len(H3_start) - 1):
			cur_joint = [H3_start[i + 1], H3_end[i]]
			H3_joint.append(cur_joint)
		NA_joint = []
		for i in range(0,len(NA_start)-1):
			cur_joint = [NA_start[i+1], NA_end[i]]
			NA_joint.append(cur_joint)

		H1_joint_user = []
		if len(H1_start_user) == 4:
			for i in range(0, len(H1_start_user) - 1):
				cur_joint = [H1_start_user[i + 1], H1_end_user[i]]
				H1_joint_user.append(cur_joint)

		H3_joint_user = []
		if len(H3_start_user) == 4:
			for i in range(0, len(H3_start_user) - 1):
				cur_joint = [H3_start_user[i + 1], H3_end_user[i]]
				H3_joint_user.append(cur_joint)

		NA_joint_user = []
		if len(NA_start_user) == 3:
			for i in range(0, len(NA_start_user) - 1):
				cur_joint = [NA_start_user[i + 1], NA_end_user[i]]
				NA_joint_user.append(cur_joint)

		self.F = MyFigure(width=6, height=3, dpi=160)

		if self.ui.comboBoxHANA.currentIndex() == 0 and self.ui.comboBoxIndex.currentIndex() == 0:  # H1 + PCT
			data_file = os.path.join(working_prefix, '..', 'Resources', 'Data', 'H1_PCT.csv')
			if os.path.exists(data_file):
				pass
			else:
				return

			csvFile = open(data_file, "r")
			reader = csv.reader(csvFile)
			data_array = []
			for item in reader:
				item = list(map(float, item))
				data_array.append(item)

			colors = sns.color_palette("hls", 3)
			x = range(1, len(data_array[0]) + 1)
			self.F.axes.plot(x, data_array[0], color=colors[0], linewidth=1, label="Season H1")
			self.F.axes.plot(x, data_array[1], color=colors[1], linewidth=1, label="pdm09 H1")
			i = 0
			for joint in H1_joint:
				if i == 0:
					self.F.axes.plot([joint[0],joint[1]], [0.1,0.1], color='r', linewidth = 3, label="Joint region")
					i += 1
				else:
					self.F.axes.plot([joint[0], joint[1]], [0.1, 0.1], color='r', linewidth = 3)
			if len(H1_joint_user) > 0:
				i = 0
				for joint in H1_joint_user:
					if i == 0:
						self.F.axes.plot([joint[0], joint[1]], [0.2, 0.2], color='b', linewidth=3, label="Joint region (User)")
						i += 1
					else:
						self.F.axes.plot([joint[0], joint[1]], [0.2, 0.2], color='b', linewidth=3)

			self.F.fig.suptitle("Pct of variations for H1")
			self.F.fig.legend()
			self.F.axes.spines['top'].set_visible(False)
			self.F.axes.spines['right'].set_visible(False)
			self.F.axes.spines['bottom'].set_position(('data', 0))
			self.F.axes.spines['left'].set_position(('data', 0))
			self.F.axes.set_yticks([0,0.1,0.2,0.3,0.4,0.5,0.6])
			yticklabels=['','10%','20%','30%','40%','50%','60%']
			self.F.axes.set_yticklabels(yticklabels)
			self.F.fig.subplots_adjust(top = 0.95, bottom = 0.1, right = 0.98, left = 0.05, hspace = 0, wspace = 0)
		elif self.ui.comboBoxHANA.currentIndex() == 1 and self.ui.comboBoxIndex.currentIndex() == 0:  # H3 + PCT
			data_file = os.path.join(working_prefix, '..', 'Resources', 'Data', 'H3_PCT.csv')
			if os.path.exists(data_file):
				pass
			else:
				return

			csvFile = open(data_file, "r")
			reader = csv.reader(csvFile)
			data_array = []
			for item in reader:
				item = list(map(float, item))
				data_array.append(item)

			colors = sns.color_palette("hls", 3)
			x = range(1, len(data_array[0]) + 1)
			self.F.axes.plot(x, data_array[0], color=colors[0], linewidth=1, label="H3")
			i = 0
			for joint in H3_joint:
				if i == 0:
					self.F.axes.plot([joint[0],joint[1]], [0.1,0.1], color='r', linewidth = 3, label="Joint region")
					i += 1
				else:
					self.F.axes.plot([joint[0], joint[1]], [0.1, 0.1], color='r', linewidth = 3)
			if len(H3_joint_user) > 0:
				i = 0
				for joint in H3_joint_user:
					if i == 0:
						self.F.axes.plot([joint[0], joint[1]], [0.2, 0.2], color='b', linewidth=3, label="Joint region (User)")
						i += 1
					else:
						self.F.axes.plot([joint[0], joint[1]], [0.2, 0.2], color='b', linewidth=3)

			self.F.fig.suptitle("Pct of variations for H3")
			self.F.fig.legend()
			self.F.axes.spines['top'].set_visible(False)
			self.F.axes.spines['right'].set_visible(False)
			self.F.axes.spines['bottom'].set_position(('data', 0))
			self.F.axes.spines['left'].set_position(('data', 0))
			self.F.axes.set_yticks([0,0.1,0.2,0.3,0.4,0.5,0.6])
			yticklabels=['','10%','20%','30%','40%','50%','60%']
			self.F.axes.set_yticklabels(yticklabels)
			self.F.fig.subplots_adjust(top = 0.95, bottom = 0.1, right = 0.98, left = 0.05, hspace = 0, wspace = 0)
		elif self.ui.comboBoxHANA.currentIndex() == 2 and self.ui.comboBoxIndex.currentIndex() == 0:  # NA + PCT
			data_file = os.path.join(working_prefix, '..', 'Resources', 'Data', 'NA_PCT.csv')
			if os.path.exists(data_file):
				pass
			else:
				return

			csvFile = open(data_file, "r")
			reader = csv.reader(csvFile)
			data_array = []
			for item in reader:
				item = list(map(float, item))
				data_array.append(item)

			colors = sns.color_palette("hls", 9)
			x = range(1, len(data_array[0]) + 1)
			self.F.axes.plot(x, data_array[0], linewidth=1, color=colors[0], label="N1")
			self.F.axes.plot(x, data_array[1], linewidth=1, color=colors[1], label="N2")
			self.F.axes.plot(x, data_array[2], linewidth=1, color=colors[2], label="N3")
			self.F.axes.plot(x, data_array[3], linewidth=1, color=colors[3], label="N4")
			self.F.axes.plot(x, data_array[4], linewidth=1, color=colors[4], label="N5")
			self.F.axes.plot(x, data_array[5], linewidth=1, color=colors[5], label="N6")
			self.F.axes.plot(x, data_array[6], linewidth=1, color=colors[6], label="N7")
			self.F.axes.plot(x, data_array[7], linewidth=1, color=colors[7], label="N8")
			self.F.axes.plot(x, data_array[8], linewidth=1, color=colors[8], label="N9")
			i = 0
			for joint in NA_joint:
				if i == 0:
					self.F.axes.plot([joint[0], joint[1]], [0.1, 0.1], color='r', linewidth=3, label="Joint region")
					i += 1
				else:
					self.F.axes.plot([joint[0], joint[1]], [0.1, 0.1], color='r', linewidth=3)
			if len(NA_joint_user) > 0:
				i = 0
				for joint in NA_joint_user:
					if i == 0:
						self.F.axes.plot([joint[0], joint[1]], [0.2, 0.2], color='b', linewidth=3, label="Joint region (User)")
						i += 1
					else:
						self.F.axes.plot([joint[0], joint[1]], [0.2, 0.2], color='b', linewidth=3)

			self.F.fig.suptitle("Pct of variations for NA")
			self.F.fig.legend()
			self.F.axes.spines['top'].set_visible(False)
			self.F.axes.spines['right'].set_visible(False)
			self.F.axes.spines['bottom'].set_position(('data', 0))
			self.F.axes.spines['left'].set_position(('data', 0))
			self.F.axes.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
			yticklabels = ['', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%']
			self.F.axes.set_yticklabels(yticklabels)
			self.F.fig.subplots_adjust(top=0.95, bottom=0.1, right=0.98, left=0.05, hspace=0, wspace=0)

		elif self.ui.comboBoxHANA.currentIndex() == 0 and self.ui.comboBoxIndex.currentIndex() == 1:  # H1 + AAVI
			data_file = os.path.join(working_prefix, '..', 'Resources', 'Data', 'H1_AAVI.csv')
			if os.path.exists(data_file):
				pass
			else:
				return

			csvFile = open(data_file, "r")
			reader = csv.reader(csvFile)
			data_array = []
			for item in reader:
				item = list(map(float, item))
				data_array.append(item)

			colors = sns.color_palette("hls", 3)
			x = range(1, len(data_array[0]) + 1)
			self.F.axes.plot(x, data_array[0], color=colors[0], linewidth=1, label="Season H1")
			self.F.axes.plot(x, data_array[1], color=colors[1], linewidth=1, label="pdm09 H1")
			i = 0
			for joint in H1_joint:
				if i == 0:
					self.F.axes.plot([joint[0], joint[1]], [2.5, 2.5], color='r', linewidth=3, label="Joint region")
					i += 1
				else:
					self.F.axes.plot([joint[0], joint[1]], [2.5, 2.5], color='r', linewidth=3)
			if len(H1_joint_user) > 0:
				i = 0
				for joint in H1_joint_user:
					if i == 0:
						self.F.axes.plot([joint[0], joint[1]], [5, 5], color='b', linewidth=3, label="Joint region (User)")
						i += 1
					else:
						self.F.axes.plot([joint[0], joint[1]], [5, 5], color='b', linewidth=3)

			self.F.fig.suptitle("Amino Acid Variation Index for H1")
			self.F.fig.legend()
			self.F.axes.spines['top'].set_visible(False)
			self.F.axes.spines['right'].set_visible(False)
			self.F.axes.spines['bottom'].set_position(('data', 0))
			self.F.axes.spines['left'].set_position(('data', 0))
			self.F.fig.subplots_adjust(top=0.95, bottom=0.1, right=0.98, left=0.05, hspace=0, wspace=0)
		elif self.ui.comboBoxHANA.currentIndex() == 1 and self.ui.comboBoxIndex.currentIndex() == 1:  # H3 + AAVI
			data_file = os.path.join(working_prefix, '..', 'Resources', 'Data', 'H3_AAVI.csv')
			if os.path.exists(data_file):
				pass
			else:
				return

			csvFile = open(data_file, "r")
			reader = csv.reader(csvFile)
			data_array = []
			for item in reader:
				item = list(map(float, item))
				data_array.append(item)

			colors = sns.color_palette("hls", 3)
			x = range(1, len(data_array[0]) + 1)
			self.F.axes.plot(x, data_array[0], color=colors[0], linewidth=1, label="H3")
			i = 0
			for joint in H3_joint:
				if i == 0:
					self.F.axes.plot([joint[0],joint[1]], [5, 5], color='r', linewidth = 3, label="Joint region")
					i += 1
				else:
					self.F.axes.plot([joint[0], joint[1]], [5, 5], color='r', linewidth = 3)
			if len(H3_joint_user) > 0:
				i = 0
				for joint in H3_joint_user:
					if i == 0:
						self.F.axes.plot([joint[0], joint[1]], [10, 10], color='b', linewidth=3, label="Joint region (User)")
						i += 1
					else:
						self.F.axes.plot([joint[0], joint[1]], [10, 10], color='b', linewidth=3)

			self.F.fig.suptitle("Amino Acid Variation Index for H3")
			self.F.fig.legend()
			self.F.axes.spines['top'].set_visible(False)
			self.F.axes.spines['right'].set_visible(False)
			self.F.axes.spines['bottom'].set_position(('data', 0))
			self.F.axes.spines['left'].set_position(('data', 0))
			self.F.fig.subplots_adjust(top = 0.95, bottom = 0.1, right = 0.98, left = 0.05, hspace = 0, wspace = 0)
		elif self.ui.comboBoxHANA.currentIndex() == 2 and self.ui.comboBoxIndex.currentIndex() == 1:  # NA + AAVI
			data_file = os.path.join(working_prefix, '..', 'Resources', 'Data', 'NA_AAVI.csv')
			if os.path.exists(data_file):
				pass
			else:
				return

			csvFile = open(data_file, "r")
			reader = csv.reader(csvFile)
			data_array = []
			for item in reader:
				item = list(map(float, item))
				data_array.append(item)

			colors = sns.color_palette("hls", 9)
			x = range(1, len(data_array[0])+1)
			self.F.axes.plot(x, data_array[0], linewidth=1,  color=colors[0], label="N1")
			self.F.axes.plot(x, data_array[1], linewidth=1,  color=colors[1], label="N2")
			self.F.axes.plot(x, data_array[2], linewidth=1,  color=colors[2], label="N3")
			self.F.axes.plot(x, data_array[3], linewidth=1,  color=colors[3], label="N4")
			self.F.axes.plot(x, data_array[4], linewidth=1,  color=colors[4], label="N5")
			self.F.axes.plot(x, data_array[5], linewidth=1,  color=colors[5], label="N6")
			self.F.axes.plot(x, data_array[6], linewidth=1,  color=colors[6], label="N7")
			self.F.axes.plot(x, data_array[7], linewidth=1,  color=colors[7], label="N8")
			self.F.axes.plot(x, data_array[8], linewidth=1,  color=colors[8], label="N9")
			i = 0
			for joint in NA_joint:
				if i == 0:
					self.F.axes.plot([joint[0], joint[1]], [10, 10], color='r', linewidth=3, label="Joint region")
					i += 1
				else:
					self.F.axes.plot([joint[0], joint[1]], [10, 10], color='r', linewidth=3)
			if len(NA_joint_user) > 0:
				i = 0
				for joint in NA_joint_user:
					if i == 0:
						self.F.axes.plot([joint[0], joint[1]], [15, 15], color='b', linewidth=3, label="Joint region (User)")
						i += 1
					else:
						self.F.axes.plot([joint[0], joint[1]], [15, 15], color='b', linewidth=3)

			self.F.fig.suptitle("Amino Acid Variation Index for NA")
			self.F.fig.legend()
			self.F.axes.spines['top'].set_visible(False)
			self.F.axes.spines['right'].set_visible(False)
			self.F.axes.spines['bottom'].set_position(('data', 0))
			self.F.axes.spines['left'].set_position(('data', 0))
			self.F.fig.subplots_adjust(top=0.95, bottom=0.1, right=0.98, left=0.05, hspace=0, wspace=0)


	@pyqtSlot()
	def GenerateReport(self):
		RepOption = self.ui.cboReportOptions.currentText()
		if RepOption == 'Make Secreted Probe':
			self.MakeProbe()
		elif RepOption == 'Sequence Editing':
			self.sequence_editing()
		elif RepOption == 'Mutate Sequences':
			self.open_mutation_dialog()
		elif RepOption == 'Fusion Sequences':
			self.open_fusion_dialog()
		self.ui.cboReportOptions.setCurrentIndex(0)

	@pyqtSlot()
	def MakeProbe(self):
		global H1Numbering
		global H3Numbering

		TrimerBioH6 = 'GGTTCAGGCTACATTCCAGAGGCCCCGAGGGATGGTCAGGCATACGTGAGAAAGGACGGCGAATGGGTCCTGCTGAGCACGTTCTTGGGTAGTGGGTTGAATGATATCTTTGAGGCGCAAAAGATTGAGTGGCATGAAGGACACCACCATCATCATCATTGA'
		testAASeq, ErMessage = LibratorSeq.Translator(TrimerBioH6, 0)

		listItems = self.ui.listWidgetStrainsIn.selectedItems()
		# if not listItems: return
		WhereState = ''
		NumSeqs = len(listItems)
		# AASeqWas = self.ui.textAA.toPlainText()
		AASeq = ''

		if NumSeqs > 0:
			i = 1
			for item in listItems:

				eachItemIs = item.text()
				WhereState += 'SeqName = "' + eachItemIs + '"'
				if NumSeqs > i:
					WhereState += ' OR '

				i += 1

			SQLStatement = 'SELECT SeqName, Sequence, Vfrom, VTo, SubType FROM LibDB WHERE ' + WhereState  # SeqName = "327_Cl15_H1" OR SeqName = "327_Cl16_H1" OR SeqName = "327_Cl17_H1"'
			# Position: H3-segment (HA1 or HA2), Amino Acid, H3Number, A/Aichi/2/1968-residue, H3-antigenic-region
			DataIn = RunSQL(DBFilename, SQLStatement)

			for item in DataIn:
				SeqName = item[0]
				Sequence = item[1]
				SubType  = item[4]
				VFrom = int(item[2]) - 1
				if VFrom == -1: VFrom = 0

				VTo = int(item[3])-1
				Sequence = Sequence[VFrom:VTo]
				Sequence = Sequence.upper()
				AASeq, ErMessage = LibratorSeq.Translator(Sequence, 0)
				HANumbering(AASeq)
				NewAASeq = ''
				NewSeqName = ''
				SeqInfoPacket = []
				if SubType == 'H3N2':
					for i in range(1, len(H3Numbering)):
						residue = H3Numbering[i]
						region = residue[0]
						AA = residue[1]
						H3Num = residue[2]
						H3res = residue[3]
						H3Ag = residue[4]

						if region == 'TM':
							StartTrimer = (i * 3) -3
							FrontEnd = Sequence[:StartTrimer]
							NewSeq = FrontEnd + TrimerBioH6
							NewAASeq, ErMessage = LibratorSeq.Translator(NewSeq, 0)
							StopAT = NewAASeq.find('*')
							NewAASeq = NewAASeq[:StopAT+1]

							NewSeqName = SeqName + '-Probe'
							form = 'Probe'
							Active = 'True'
							Role = 'Unassigned'
							Donor = 'none'
							Mutations = 'Y98F,'
							VFrom = 1

							# todo add code to mutate Y98F or incorporate mutations automatically

							ItemIn = [NewSeqName, NewSeq, str(len(NewSeq)), SubType, form, VFrom, str(len(NewSeq)), Active, Role, Donor, Mutations, 0]
							SeqInfoPacket.clear()
							SeqInfoPacket.append(ItemIn)
							# if DBFilename == 'none':
							# 	self.on_action_New_triggered()
							# 	return
							NumEnterred = enterData(self, DBFilename, SeqInfoPacket)

							# self.HANumbering(AASeqWas) #changes Numbering back to original
							self.ui.listWidgetStrainsIn.setCurrentRow(0)
							self.PopulateCombos()
							return

	@pyqtSlot()
	def on_actionDelete_record_triggered(self):
		# fields = ['SeqName', 'ID']
		listToDelete = self.ui.listWidgetStrains.selectedItems()
		# RowsToDellete= self.ui.listWidgetStrains.item

		if len(listToDelete) != 0:
			for item in listToDelete:
				eachItemIs = item.text()
				# itemRow = item.row()
				# 'SELECT * FROM vgenesDB WHERE SeqName = '
				question = 'Are you certain you want to delete '+ eachItemIs + '?'
				buttons = 'YN'
				answer = questionMessage(self, question, buttons)

				if answer == 'Yes':
					SQLStatement = 'DELETE FROM LibDB WHERE SeqName = "' + eachItemIs + '"'  # LibratorSQL.MakeSQLStatement(self, fields, data[0])
					deleterecords(DBFilename,SQLStatement)

					self.ui.listWidgetStrains.setCurrentItem(item)
					delitem = self.ui.listWidgetStrains.currentRow()

					self.ui.listWidgetStrains.takeItem(delitem)

					self.ui.listWidgetStrainsIn.selectAll()
					ListActive = self.ui.listWidgetStrainsIn.selectedItems()
					for Initem in ListActive:
						if Initem.text() == eachItemIs:
							self.ui.listWidgetStrainsIn.setCurrentItem(Initem)
							delitemIn = self.ui.listWidgetStrainsIn.currentRow()
							self.ui.listWidgetStrainsIn.takeItem(delitemIn)



			# self.removeAll()
			# self.PopulateCombos()
			#
			#
			# ItemsList = self.ui.listWidgetStrainsIn.count()
			# if ItemsList >0:
			# 	self.ui.listWidgetStrainsIn.setCurrentRow(0)
			# 	self.ListItemChanged()
			# 	for item in DataIs:
			# 		FromV = int(item[5])-1
			# 		if FromV == -1: FromV = 0
			# 		ToV = int(item[6])-1
			#
			# 		HASeq = item[1]
			# 		HASeq = HASeq[FromV:ToV]
			#
			# 		AASeq = Translator(HASeq.upper(), 0)
			# 		AASeqIs = AASeq[0]
			# 	self.HANumbering(AASeqIs)

	@pyqtSlot()
	def on_btnH1Num_clicked(self):
		self.CheckDecorations()

	@pyqtSlot()
	def on_btnH3Num_clicked(self):
		self.CheckDecorations()

	@pyqtSlot()
	def on_btnH1Ag_clicked(self):
		self.CheckDecorations()

	@pyqtSlot()
	def on_btnH3Ag_clicked(self):
		self.CheckDecorations()

	@pyqtSlot()
	def on_btnMuts_clicked(self):
		self.CheckDecorations()

	@pyqtSlot()
	def on_btnDonReg_clicked(self):
		self.CheckDecorations()

	@pyqtSlot()
	def CheckDecorations(self):
		Subtype = self.ui.cboSubtype.currentText()
		Decorations = []
		Decorations.clear()

		if self.ui.btnH3Num.isChecked():
			Decorations.append('H3Num')
		if self.ui.btnH1Num.isChecked():
			Decorations.append('H1Num')
		if self.ui.btnMuts.isChecked():
			Decorations.append('Muts')
		if self.ui.btnDonReg.isChecked():
			Decorations.append('DonReg')
		if len(Decorations) == 0:
			Decorations.append('None')

		if Subtype in Group2 or Subtype in Group1:
			ItemsList = self.ui.listWidgetStrainsIn.count()
			AASeqIs = ''
			if ItemsList > 0:
				AASeqIs = self.ui.textAA.toPlainText()
				HANumbering(AASeqIs)
			else:
				return
			cursor = self.ui.txtAASeq.textCursor()
			self.Decorate(Decorations, cursor)
		elif Subtype in GroupNA or Subtype == 'B' or Subtype == 'Other':
			ItemsList = self.ui.listWidgetStrainsIn.count()
			AASeqIs = ''
			if ItemsList > 0:
				AASeqIs = self.ui.textAA.toPlainText()
			else:
				return
			cursor = self.ui.txtAASeq.textCursor()
			self.DecorateNoneHA(Decorations, cursor)

	@pyqtSlot()
	def DecorateSingle(self):
		global H1Numbering
		global H3Numbering

		AASeqIs = self.ui.textAA.toPlainText()
		HANumbering(AASeqIs)

		cursor = self.ui.txtAASeq.textCursor()
		H3NumOn = True
		H1NumOn = True
		MutsOn = True
		DonRegOn = True
		AAColorMap = ''
		AASeq = ''
		NumLine = ''
		AAPosColorMap = ''
		rePos = ''
		LenResP = 0
		ResDownP = 0

		H3NumLine = ''
		H3ColorMap = ''

		H1NumLine = ''
		H1ColorMap = ''

		Key = ''
		KeyMap = ''
		HA2K = False
		TMK = False
		TrimK = False
		StopK = False
		# MakeItUp = ''
		ResT = ''
		InHA1 = False
		InHA2 = False
		NotLong = False
		ResDown = 0

		H3Key = ''
		H3KeyCMap = ''

		H1Key = ''
		H1KeyCMap = ''
		AAKey = 'Sequence elements:  HA1    HA2   stop   Transmembrane  Trimerization-Avitag-H6  Mutations \n'
		AAKeyC = '000000000000000000000000099999991111111888888888888888BBBBBBBBBBBBBBBBBBBBBBBBBEEEEEEEEEEE\n'

		PosKey = 'Position:           Donor Region \n'
		PosKeyC = '0000000000000000000DDDDDDDDDDDDDD\n'

		if H3NumOn == True:
			for pos in range(1, len(H3Numbering)):
				residue = H3Numbering[pos]
				AA = residue[1]
				AASeq += AA
				resPos = str(pos)

				tesResNP = pos / 5
				if resPos == 1:
					NumLine += str(pos)
					AAPosColorMap += '0'

				elif tesResNP.is_integer():  # is divisible by 5
					ResTP = str(pos)
					LenResP = len(ResTP)

					if NumberingMap['H3HA1end'] > (pos + LenResP + 1):
						ResDownP = LenResP
						NumLine += ResTP[LenResP - ResDownP]

						ResDownP -= 1
						AAPosColorMap += '0'
					else:
						NumLine += '.'
						AAPosColorMap += '0'
				else:
					if ResDownP != 0:
						NumLine += ResTP[LenResP - ResDownP]
						AAPosColorMap += '0'
						# H3ColorMap += '0'
						ResDownP -= 1
					else:
						NumLine += '.'
						AAPosColorMap += '0'

				region = residue[0]

				if region == 'HA1':
					NextC = '0'
					InHA1 = True
				elif region == 'HA2':
					InHA2 = True
					NextC = '9'
					HA2K = True
				elif region == 'TM':
					NextC = '8'
					TMK = True
				elif region == 'Trimer-Avitag-H6':
					NextC = 'B'
					TrimK = True
				else:
					NextC = '0'

				if AA == '*':
					NextC = '1'
					StopK = True
				AAColorMap += NextC

				res = residue[2]
				Ag = residue[4]

				if res != '-':
					# if res.is_integer():
					tesResN = res / 5
					if res == 1:
						H3NumLine += str(res)
						H3ColorMap += '5'

					elif tesResN.is_integer():  # is divisible by 5
						ResT = str(res)
						LenRes = len(ResT)
						if region == 'HA1':
							if NumberingMap['H3HA1end'] > (res + LenRes + 1):
								ResDown = LenRes
								H3NumLine += ResT[LenRes - ResDown]
								if Ag == '-':
									H3ColorMap += '0'
								elif Ag == 'A':
									H3ColorMap += '6'
								elif Ag == 'B':
									H3ColorMap += '2'
								elif Ag == 'C':
									H3ColorMap += '7'
								elif Ag == 'D':
									H3ColorMap += '3'
								elif Ag == 'E':
									H3ColorMap += 'C'
								elif Ag == 'Stalk-MN':
									H3ColorMap += 'A'
								else:
									H3ColorMap += '0'

								ResDown -= 1
							else:
								H3NumLine += '.'
								if Ag == '-':
									H3ColorMap += '0'
								elif Ag == 'A':
									H3ColorMap += '6'
								elif Ag == 'B':
									H3ColorMap += '2'
								elif Ag == 'C':
									H3ColorMap += '7'
								elif Ag == 'D':
									H3ColorMap += '3'
								elif Ag == 'E':
									H3ColorMap += 'C'
								elif Ag == 'Stalk-MN':
									H3ColorMap += 'A'
								else:
									H3ColorMap += '0'

						elif region == 'HA2':
							if NumberingMap['H3HA2end'] > (res + LenRes + 1):
								ResDown = LenRes
								H3NumLine += ResT[LenRes - ResDown]
								if Ag == '-':
									H3ColorMap += '0'
								elif Ag == 'Stalk-MN':
									H3ColorMap += 'A'
								else:
									H3ColorMap += '0'

								ResDown -= 1
							else:
								H3NumLine += '.'
								if Ag == '-':
									H3ColorMap += '0'
								elif Ag == 'Stalk-MN':
									H3ColorMap += 'A'
								else:
									H3ColorMap += '0'

					else:
						if ResDown != 0:
							H3NumLine += ResT[LenRes - ResDown]
							if region == 'HA1':
								if Ag == '-':
									H3ColorMap += '0'
								elif Ag == 'A':
									H3ColorMap += '6'
								elif Ag == 'B':
									H3ColorMap += '2'
								elif Ag == 'C':
									H3ColorMap += '7'
								elif Ag == 'D':
									H3ColorMap += '3'
								elif Ag == 'E':
									H3ColorMap += 'C'
								elif Ag == 'Stalk-MN':
									H3ColorMap += 'A'
								else:
									H3ColorMap += '0'
							elif region == 'HA2':
								if Ag == '-':
									H3ColorMap += '0'
								elif Ag == 'Stalk-MN':
									H3ColorMap += 'A'
								else:
									H3ColorMap += '0'
							else:
								H3ColorMap += '0'

							# H3ColorMap += '0'
							ResDown -= 1
						else:
							H3NumLine += '.'
							if region == 'HA1':
								if Ag == '-':
									H3ColorMap += '0'
								elif Ag == 'A':
									H3ColorMap += '6'
								elif Ag == 'B':
									H3ColorMap += '2'
								elif Ag == 'C':
									H3ColorMap += '7'
								elif Ag == 'D':
									H3ColorMap += '3'
								elif Ag == 'E':
									H3ColorMap += 'C'
								elif Ag == 'Stalk-MN':
									H3ColorMap += 'A'
								else:
									H3ColorMap += '0'
							elif region == 'HA2':
								if Ag == '-':
									H3ColorMap += '0'
								elif Ag == 'Stalk-MN':
									H3ColorMap += 'A'
								else:
									H3ColorMap += '0'
							else:
								H3ColorMap += '0'
				else:

					H3NumLine += res
					H3ColorMap += '0'

			H3Key = 'H3 Antigenic Sites:  A    B    C    D    E   Stalk-MN \n'
			H3KeyCMap = '000000000000000000066666222227777733333CCCCCAAAAAAAAAA\n'

		if H1NumOn == True:
			ResDown = 0
			ResT = ''

			for pos in range(1, len(H1Numbering)):
				residue = H1Numbering[pos]

				region = residue[0]

				if H3NumOn == False:
					AA = residue[1]
					AASeq += AA
					resPos = str(pos)

					tesResNP = pos / 5
					if resPos == 1:
						NumLine += str(pos)
						AAPosColorMap += '0'

					elif tesResNP.is_integer():  # is divisible by 5
						ResTP = str(pos)
						LenResP = len(ResTP)

						if NumberingMap['H3HA1end'] > (pos + LenResP + 1):
							ResDownP = LenResP
							NumLine += ResTP[LenResP - ResDownP]
							ResDownP -= 1
							AAPosColorMap += '0'
						else:
							NumLine += '.'

							AAPosColorMap += '0'

					else:
						if ResDownP != 0:
							NumLine += ResTP[LenResP - ResDownP]
							AAPosColorMap += '0'
							# H3ColorMap += '0'
							ResDownP -= 1
						else:
							NumLine += '.'
							AAPosColorMap += '0'

					if region == 'HA1':
						NextC = '0'
						InHA1 = True
					elif region == 'HA2':
						InHA2 = True
						NextC = '9'
						HA2K = True
					elif region == 'TM':
						NextC = '8'
						TMK = True
					elif region == 'Trimer-Avitag-H6':
						NextC = 'B'
						TrimK = True
					else:
						NextC = '0'

					if AA == '*':
						NextC = '1'
						StopK = True

					AAColorMap += NextC

				res = residue[2]
				Ag = residue[4]

				if res != '-':
					# if res.is_integer():
					tesResN = res / 5
					if res == 1:
						H1NumLine += str(res)
						H1ColorMap += '5'

					elif tesResN.is_integer():  # is divisible by 5
						ResT = str(res)
						LenRes = len(ResT)
						if region == 'HA1':
							if NumberingMap['H1HA1end'] > (res + LenRes + 1):
								ResDown = LenRes
								H1NumLine += ResT[LenRes - ResDown]
								if Ag == '-':
									H1ColorMap += '0'
								elif Ag == 'Cb':
									H1ColorMap += '7'
								elif Ag == 'Ca1':
									H1ColorMap += '2'
								elif Ag == 'Ca2':
									H1ColorMap += '4'
								elif Ag == 'Sa':
									H1ColorMap += '3'
								elif Ag == 'Sb':
									H1ColorMap += '6'
								else:
									H1ColorMap += '0'

								ResDown -= 1
							else:
								H1NumLine += '.'
								if Ag == '-':
									H1ColorMap += '0'
								elif Ag == 'Cb':
									H1ColorMap += '7'
								elif Ag == 'Ca1':
									H1ColorMap += '2'
								elif Ag == 'Ca2':
									H1ColorMap += '4'
								elif Ag == 'Sa':
									H1ColorMap += '3'
								elif Ag == 'Sb':
									H1ColorMap += '6'
								else:
									H1ColorMap += '0'

						elif region == 'HA2':
							if NumberingMap['H1HA2end'] > (res + LenRes + 1):
								ResDown = LenRes
								H1NumLine += ResT[LenRes - ResDown]
								if Ag == '-':
									H1ColorMap += '0'
								elif Ag == 'Stalk-MN':
									H1ColorMap += 'A'
								else:
									H1ColorMap += '0'

								ResDown -= 1
							else:
								H1NumLine += '.'
								if Ag == '-':
									H1ColorMap += '0'
								elif Ag == 'Stalk-MN':
									H1ColorMap += 'A'
								else:
									H1ColorMap += '0'

					else:
						if ResDown != 0:
							H1NumLine += ResT[LenRes - ResDown]
							if region == 'HA1':
								if Ag == '-':
									H1ColorMap += '0'
								elif Ag == 'Cb':
									H1ColorMap += '7'
								elif Ag == 'Ca1':
									H1ColorMap += '2'
								elif Ag == 'Ca2':
									H1ColorMap += '4'
								elif Ag == 'Sa':
									H1ColorMap += '3'
								elif Ag == 'Sb':
									H1ColorMap += '6'
								else:
									H1ColorMap += '0'
							elif region == 'HA2':
								if Ag == '-':
									H1ColorMap += '0'
								elif Ag == 'Stalk-MN':
									H1ColorMap += 'A'
								else:
									H1ColorMap += '0'
							else:
								H1ColorMap += '0'

							ResDown -= 1
						else:
							H1NumLine += '.'
							if region == 'HA1':
								if Ag == '-':
									H1ColorMap += '0'
								elif Ag == 'Cb':
									H1ColorMap += '7'
								elif Ag == 'Ca1':
									H1ColorMap += '2'
								elif Ag == 'Ca2':
									H1ColorMap += '4'
								elif Ag == 'Sa':
									H1ColorMap += '3'
								elif Ag == 'Sb':
									H1ColorMap += '6'
								else:
									H1ColorMap += '0'
							elif region == 'HA2':
								if Ag == '-':
									H1ColorMap += '0'
								elif Ag == 'Stalk-MN':
									H1ColorMap += 'A'
								else:
									H1ColorMap += '0'
							else:
								H1ColorMap += '0'
				else:

					H1NumLine += res
					H1ColorMap += '0'
			H1Key = 'H1 Antigenic Sites:  Ca1    Ca2    Cb    Sa    Sb   Stalk-MN \n'
			H1KeyCMap = '000000000000000000022222224444444777777333333666666AAAAAAAAAA\n'

		SeqName = self.ui.txtSeqName2.toPlainText() + '\n'
		LenSeqName = len(SeqName)

		if DonRegOn == True or MutsOn == True:
			WhereState = "SeqName = " + '"' + self.ui.txtSeqName2.toPlainText() + '"'
			SQLStatement = 'SELECT `Donor`, `Mutations` FROM LibDB WHERE ' + WhereState
			DataIn = RunSQL(DBFilename, SQLStatement)
			donor_info = DataIn[0][0]
			mutation_info = DataIn[0][1]

		if H1NumOn == False and H3NumOn == False:
			for pos in range(1, len(H1Numbering)):
				residue = H1Numbering[pos]
				region = residue[0]

				AA = residue[1]
				AASeq += AA
				resPos = str(pos)

				tesResNP = pos / 5
				if resPos == 1:
					NumLine += str(pos)
					AAPosColorMap += '0'

				elif tesResNP.is_integer():  # is divisible by 5
					ResTP = str(pos)
					LenResP = len(ResTP)

					if NumberingMap['H3HA1end'] > (pos + LenResP + 1):
						ResDownP = LenResP
						NumLine += ResTP[LenResP - ResDownP]
						ResDownP -= 1
						AAPosColorMap += '0'
					else:
						NumLine += '.'

						AAPosColorMap += '0'

				else:
					if ResDownP != 0:
						NumLine += ResTP[LenResP - ResDownP]
						AAPosColorMap += '0'
						# H3ColorMap += '0'
						ResDownP -= 1
					else:
						NumLine += '.'
						AAPosColorMap += '0'

				if region == 'HA1':
					NextC = '0'
					InHA1 = True
				elif region == 'HA2':
					InHA2 = True
					NextC = '9'
					HA2K = True
				elif region == 'TM':
					NextC = '8'
					TMK = True
				elif region == 'Trimer-Avitag-H6':
					NextC = 'B'
					TrimK = True
				else:
					NextC = '0'

				if AA == '*':
					NextC = '1'
					StopK = True

				AAColorMap += NextC

		Sequence = SeqName + '\n'
		ColorMap = ''
		for i in range(0, LenSeqName):
			ColorMap += '0'
		ColorMap += '\n'

		if MutsOn == True:
			if mutation_info == "none":
				# QMessageBox.warning(self, 'Warning',
				#                     'No mutation information for this sequence!', QMessageBox.Ok, QMessageBox.Ok)
				pass
			else:
				mutation_info = mutation_info.rstrip(',')
				mutation_info = mutation_info.split(',')

		if DonRegOn == True:
			if donor_info == 'none':
				# QMessageBox.warning(self, 'Warning',
				#                     'No donor information for this sequence!', QMessageBox.Ok, QMessageBox.Ok)
				pass

		# NumLine += '.'
		# AAPosColorMap += '0'
		for i in range(0, len(AASeq), 60):
			AASeqSeg = AASeq[i:i + 60]
			AAColorSeg = AAColorMap[i:i + 60]
			NumLineSeg = NumLine[i:i + 60]
			AAPosColorSeg = AAPosColorMap[i:i + 60]

			if DonRegOn == True:
				if donor_info != 'none':
					donor_start, donor_end = donor_info.split('-')
					donor_start = int(donor_start) - 1
					donor_end = int(donor_end)

					cur_start = i
					cur_end = i + 60
					# case 1
					if cur_start > donor_end:
						pass
					# case 2
					if cur_start <= donor_end and cur_start >= donor_start and donor_end <= cur_end:
						cur_donor_start = 0
						cur_donor_end = donor_end - cur_start
						AAPosColorSeg = 'D' * cur_donor_end + AAPosColorSeg[cur_donor_end:]
					# case 3
					if cur_start <= donor_start and cur_end >= donor_end:
						cur_donor_start = donor_start - cur_start
						cur_donor_end = donor_end - cur_start
						AAPosColorSeg = AAPosColorSeg[:cur_donor_start] + 'D' * (cur_donor_end - cur_donor_start) + \
						                AAPosColorSeg[cur_donor_end:]
					# case 4
					if cur_end <= donor_end and cur_end >= donor_start and donor_start >= cur_start:
						cur_donor_start = donor_start - cur_start
						cur_donor_end = cur_end
						AAPosColorSeg = AAPosColorSeg[:cur_donor_start] + 'D' * \
						                (cur_donor_end - cur_donor_start)
					# case 5
					if cur_start >= donor_start and cur_end <= donor_end:
						AAPosColorSeg = 'D' * 60
					# case 6
					if donor_start > cur_end:
						pass

			NumLineSeg = '    Position: ' + NumLineSeg + '\n'
			AAPosColorSeg = '00000000000000' + AAPosColorSeg + '\n'

			Sequence += NumLineSeg
			ColorMap += AAPosColorSeg

			if H3NumOn == True:
				H3NumSeg = 'H3-Numbering: ' + H3NumLine[i:i + 60] + '\n'
				H3ColorSeg = '00000000000000' + H3ColorMap[i:i + 60] + '\n'
				Sequence += H3NumSeg
				ColorMap += H3ColorSeg

			if H1NumOn == True:
				H1NumSeg = 'H1-Numbering: ' + H1NumLine[i:i + 60] + '\n'
				H1ColorSeg = '00000000000000' + H1ColorMap[i:i + 60] + '\n'
				Sequence += H1NumSeg
				ColorMap += H1ColorSeg

			if MutsOn == True:
				cur_start = i
				cur_end = i + 60

				if mutation_info != "none":
					for x in mutation_info:
						mutation_pos = re.findall(r"\d+", x)
						mutation_pos = int(mutation_pos[0]) - 1

						if mutation_pos in range(cur_start, cur_end):
							AAColorSeg = list(AAColorSeg)
							AAColorSeg[mutation_pos - cur_start] = 'E'
							AAColorSeg = ''.join(AAColorSeg)

			AASeqSeg = '    Sequence: ' + AASeqSeg + '\n\n'
			AAColorSeg = '00000000000000' + AAColorSeg + '\n\n'

			Sequence += AASeqSeg
			ColorMap += AAColorSeg

		Sequence += ' \n'
		ColorMap += '0\n'

		legend_text = AAKey + H3Key + H1Key + PosKey
		legend_color = AAKeyC + H3KeyCMap + H1KeyCMap + PosKeyC
		# Add note at begining that HA1 is black andHA2 is grey or

		# create new window object
		window_id = int(time.time() * 100)
		VGenesTextWindows[window_id] = VGenesTextMain()
		VGenesTextWindows[window_id].id = window_id
		VGenesTextWindows[window_id].data = DataIn
		VGenesTextWindows[window_id].note = Notes
		VGenesTextWindows[window_id].type = 'Alignment'
		VGenesTextWindows[window_id].dnaAct.setChecked(self.ui.actionDNA.isChecked())
		VGenesTextWindows[window_id].aaAct.setChecked(self.ui.actionAA.isChecked())
		VGenesTextWindows[window_id].baAct.setChecked(self.ui.actionBA.isChecked())


		Style = 'aligned'
		self.ShowVGenesTextEdit(Sequence, Style, ColorMap, window_id)
		self.ShowVGenesTextEditLegend(legend_text, legend_color,window_id)

	@pyqtSlot()
	def DecorateNoneHA(self, Decorations, cursor):
		MutsOn = False
		DonRegOn = False
		AASeq = ''
		AAColorMap = ''
		AAPos = ''
		AAPosColorMap = ''

		for Decoration in Decorations:
			if Decoration == 'DonReg':
				DomainsLine = ''
				DonRegOn = True
			if Decoration == 'Muts':
				MutsLine = ''
				MutsOn = True

		AAKey = 'Sequence elements:  Mutations \n'
		AAKeyC = '0000000000000000000EEEEEEEEEEE\n'

		PosKey = 'Position:           Donor Region \n'
		PosKeyC = '0000000000000000000DDDDDDDDDDDDDD\n'

		SeqName = self.ui.txtSeqName2.toPlainText() + '\n'
		LenSeqName = len(SeqName)
		AASeq = self.ui.textAA.toPlainText()
		AAColorMap = '0' * len(AASeq)
		AAPos = MakeRuler(1, len(AASeq), 5, 'nt')
		AAPosColorMap = '0' * len(AAPos)

		if DonRegOn == True or MutsOn == True:
			WhereState = "SeqName = " + '"' + self.ui.txtSeqName2.toPlainText() + '"'
			SQLStatement = 'SELECT `Donor`, `Mutations` FROM LibDB WHERE ' + WhereState
			DataIn = RunSQL(DBFilename, SQLStatement)
			donor_info = DataIn[0][0]
			mutation_info = DataIn[0][1]

		Sequence = SeqName + '\n'
		ColorMap = ''
		ColorMap += '0' * LenSeqName + '\n'

		if MutsOn == True:
			if mutation_info == "none":
				pass
			else:
				mutation_info = mutation_info.rstrip(',')
				mutation_info = mutation_info.split(',')
		if DonRegOn == True:
			if donor_info == 'none':
				pass

		for i in range(0, len(AASeq), 60):
			AASeqSeg = AASeq[i:i + 60]
			AAColorSeg = AAColorMap[i:i + 60]
			AAPosSeg = AAPos[i:i + 60]
			AAPosColorSeg = AAPosColorMap[i:i + 60]

			if DonRegOn == True:
				if donor_info != 'none':
					donor_start, donor_end = donor_info.split('-')
					donor_start = int(donor_start) - 1
					donor_end = int(donor_end)

					cur_start = i
					cur_end = i + 60
					# case 1
					if cur_start > donor_end:
						pass
					# case 2
					if cur_start <= donor_end and cur_start >= donor_start and donor_end <= cur_end:
						cur_donor_start = 0
						cur_donor_end = donor_end - cur_start
						AAPosColorSeg = 'D' * cur_donor_end + AAPosColorSeg[cur_donor_end:]
					# case 3
					if cur_start <= donor_start and cur_end >= donor_end:
						cur_donor_start = donor_start - cur_start
						cur_donor_end = donor_end - cur_start
						AAPosColorSeg = AAPosColorSeg[:cur_donor_start] + 'D' * (cur_donor_end - cur_donor_start) + \
						                AAPosColorSeg[cur_donor_end:]
					# case 4
					if cur_end <= donor_end and cur_end >= donor_start and donor_start >= cur_start:
						cur_donor_start = donor_start - cur_start
						cur_donor_end = cur_end - cur_start
						AAPosColorSeg = AAPosColorSeg[:cur_donor_start] + 'D' * \
						                (cur_donor_end - cur_donor_start)
					# case 5
					if cur_start >= donor_start and cur_end <= donor_end:
						AAPosColorSeg = 'D' * 60
					# case 6
					if donor_start > cur_end:
						pass

			AAPosSeg = '    Position: ' + AAPosSeg + '\n'
			AAPosColorSeg = '00000000000000' + AAPosColorSeg + '\n'

			Sequence += AAPosSeg
			ColorMap += AAPosColorSeg

			if MutsOn == True:
				cur_start = i
				cur_end = i + 60

				if mutation_info != "none":
					for x in mutation_info:
						mutation_pos = re.findall(r"\d+", x)
						mutation_pos = int(mutation_pos[0]) - 1

						if mutation_pos in range(cur_start, cur_end):
							AAColorSeg = list(AAColorSeg)
							AAColorSeg[mutation_pos - cur_start] = 'E'
							AAColorSeg = ''.join(AAColorSeg)

			AASeqSeg = '    Sequence: ' + AASeqSeg + '\n\n'
			AAColorSeg = '00000000000000' + AAColorSeg + '\n\n'

			Sequence += AASeqSeg
			ColorMap += AAColorSeg

		Sequence += ' \n'
		ColorMap += '0\n'

		Sequence += AAKey + PosKey
		ColorMap += AAKeyC + PosKeyC
		# Add note at begining that HA1 is black andHA2 is grey or
		self.ui.txtAASeq.setText(Sequence)
		self.DecorateText(ColorMap, cursor)

	@pyqtSlot()
	def Decorate(self, Decorations, cursor):
		AAColorMap = ''

		H3NumOn = False
		H1NumOn = False
		H3AgOn = False
		H1AgOn = False
		DomainsOn = False
		MutsOn = False
		DonRegOn = False
		AAColorMap = ''
		AASeq = ''
		NumLine = ''
		AAPosColorMap= ''
		rePos = ''
		LenResP = 0
		ResDownP=0

		for Decoration in Decorations:
			if Decoration == 'None':
				continue
				# Setup the desired format for matches
				format = QTextCharFormat()
				format.setForeground(QBrush(QColor("black")))
				format.setBackground(QBrush(QColor("white")))
				format.setFontUnderline(False)
				cursor.setPosition(0)
				cursor.setPosition(len(self.ui.txtAASeq.toPlainText()), QTextCursor.KeepAnchor)
				cursor.mergeCharFormat(format)

				cursor.setPosition(0)

				for pos in range(1, len(H3Numbering)):
					residue = H3Numbering[pos]
					AA = residue[1]
					AASeq += AA
					resPos = str(pos)
					tesResNP = pos / 5
					if resPos == 1:
						NumLine += str(pos)
						AAPosColorMap += '0'
					elif tesResNP.is_integer():  # is divisible by 5
						ResTP = str(pos)
						LenResP = len(ResTP)
						if NumberingMap['H3HA1end'] > (pos + LenResP + 1):
							ResDownP = LenResP
							NumLine += ResTP[LenResP - ResDownP]
							ResDownP -= 1
							AAPosColorMap += '0'
						else:
							NumLine += '.'
							AAPosColorMap += '0'
					else:
						if ResDownP != 0:
							NumLine += ResTP[LenResP - ResDownP]
							AAPosColorMap += '0'
							# H3ColorMap += '0'
							ResDownP -= 1
						else:
							NumLine += '.'
							AAPosColorMap += '0'
					region = residue[0]
					if region == 'HA1':
						NextC = '0'
						InHA1 = True
					elif region == 'HA2':
						InHA2 = True
						NextC = '9'
						HA2K = True
					elif region == 'TM':
						NextC = '8'
						TMK = True
					elif region == 'Trimer-Avitag-H6':
						NextC = '7'
						TrimK = True
					else:
						NextC = '0'
					if AA == '*':
						NextC = '1'
						StopK = True
					AAColorMap += NextC
				break

			if Decoration == 'H3Num':
				H3NumOn = True

			if Decoration == 'H1Num':
				H1NumLine = ''
				H1NumOn = True

			if Decoration == 'H3Ag':
				H3AgLine = ''

				H3AgOn = True

			if Decoration == 'H1Ag':
				H1AgLine = ''
				H1AgOn = True

			if Decoration == 'DonReg':
				DomainsLine = ''
				DonRegOn = True

			if Decoration == 'Muts':
				MutsLine = ''
				MutsOn = True

		# need to build the alignment and colormap in conjunction where colormap has a
		# indicating what color that matches identically to the alignment character for
		# character

		# Tuple 1: Position(dict): H1-segment (HA1 or HA2), residue, H3or11Number, H# or H1-residue, H1-antigenic-region

		H3NumLine = ''
		H3ColorMap = ''

		H1NumLine = ''
		H1ColorMap = ''

		Key = ''
		KeyMap = ''
		HA2K = False
		TMK = False
		TrimK = False
		StopK = False
		# MakeItUp = ''
		ResT = ''
		InHA1 = False
		InHA2 = False
		NotLong = False
		ResDown = 0

		H3Key = ''
		H3KeyCMap = ''

		H1Key = ''
		H1KeyCMap = ''
		AAKey = 'Sequence elements:  HA1    HA2   stop   Transmembrane  Trimerization-Avitag-H6  Mutations \n'
		AAKeyC = '000000000000000000000000099999991111111888888888888888BBBBBBBBBBBBBBBBBBBBBBBBBEEEEEEEEEEE\n'

		PosKey =  'Position:           Donor Region \n'
		PosKeyC = '0000000000000000000DDDDDDDDDDDDDD\n'

		if H3NumOn == True:
			for pos in range(1, len(H3Numbering)):
				residue = H3Numbering[pos]
				AA = residue[1]
				AASeq += AA
				resPos = str(pos)

				tesResNP = pos / 5
				if resPos == 1:
					NumLine += str(pos)
					AAPosColorMap += '0'

				elif tesResNP.is_integer():  # is divisible by 5
					ResTP = str(pos)
					LenResP = len(ResTP)

					if NumberingMap['H3HA1end'] > (pos + LenResP + 1):
						ResDownP = LenResP
						NumLine += ResTP[LenResP - ResDownP]

						ResDownP -= 1
						AAPosColorMap += '0'
					else:
						NumLine += '.'
						AAPosColorMap += '0'
				else:
					if ResDownP != 0:
						NumLine += ResTP[LenResP - ResDownP]
						AAPosColorMap += '0'
						# H3ColorMap += '0'
						ResDownP -= 1
					else:
						NumLine += '.'
						AAPosColorMap += '0'

				region = residue[0]

				if region == 'HA1':
					NextC = '0'
					InHA1 = True
				elif region == 'HA2':
					InHA2 = True
					NextC = '9'
					HA2K = True
				elif region == 'TM':
					NextC = '8'
					TMK = True
				elif region == 'Trimer-Avitag-H6':
					NextC = 'B'
					TrimK = True
				else:
					NextC = '0'

				if AA == '*':
					NextC = '1'
					StopK = True
				AAColorMap += NextC

				res = residue[2]
				Ag = residue[4]

				if res != '-':
					# if res.is_integer():
					tesResN = res / 5
					if res == 1:
						H3NumLine += str(res)
						H3ColorMap += '5'

					elif tesResN.is_integer(): #is divisible by 5
						ResT = str(res)
						LenRes = len(ResT)
						if region == 'HA1':
							if NumberingMap['H3HA1end'] > (res + LenRes +1):
								ResDown = LenRes
								H3NumLine += ResT[LenRes - ResDown]
								if Ag == '-':
									H3ColorMap += '0'
								elif Ag == 'A':
									H3ColorMap += '6'
								elif Ag == 'B':
									H3ColorMap += '2'
								elif Ag == 'C':
									H3ColorMap += '7'
								elif Ag == 'D':
									H3ColorMap += '3'
								elif Ag == 'E':
									H3ColorMap += 'C'
								elif Ag == 'Stalk-MN':
									H3ColorMap += 'A'
								else:
									H3ColorMap += '0'

								ResDown -= 1
							else:
								H3NumLine += '.'
								if Ag == '-':
									H3ColorMap += '0'
								elif Ag == 'A':
									H3ColorMap += '6'
								elif Ag == 'B':
									H3ColorMap += '2'
								elif Ag == 'C':
									H3ColorMap += '7'
								elif Ag == 'D':
									H3ColorMap += '3'
								elif Ag == 'E':
									H3ColorMap += 'C'
								elif Ag == 'Stalk-MN':
									H3ColorMap += 'A'
								else:
									H3ColorMap += '0'

						elif region == 'HA2':
							if NumberingMap['H3HA2end'] > (res + LenRes + 1):
								ResDown = LenRes
								H3NumLine += ResT[LenRes - ResDown]
								if Ag == '-':
									H3ColorMap += '0'
								elif Ag == 'Stalk-MN':
									H3ColorMap += 'A'
								else:
									H3ColorMap += '0'

								ResDown -= 1
							else:
								H3NumLine += '.'
								if Ag == '-':
									H3ColorMap += '0'
								elif Ag == 'Stalk-MN':
									H3ColorMap += 'A'
								else:
									H3ColorMap += '0'

					else:
						if ResDown != 0:
							H3NumLine += ResT[LenRes - ResDown]
							if region == 'HA1':
								if Ag == '-':
									H3ColorMap += '0'
								elif Ag == 'A':
									H3ColorMap += '6'
								elif Ag == 'B':
									H3ColorMap += '2'
								elif Ag == 'C':
									H3ColorMap += '7'
								elif Ag == 'D':
									H3ColorMap += '3'
								elif Ag == 'E':
									H3ColorMap += 'C'
								elif Ag == 'Stalk-MN':
									H3ColorMap += 'A'
								else:
									H3ColorMap += '0'
							elif region == 'HA2':
								if Ag == '-':
									H3ColorMap += '0'
								elif Ag == 'Stalk-MN':
									H3ColorMap += 'A'
								else:
									H3ColorMap += '0'
							else:
								H3ColorMap += '0'

							# H3ColorMap += '0'
							ResDown -= 1
						else:
							H3NumLine += '.'
							if region == 'HA1':
								if Ag == '-':
									H3ColorMap += '0'
								elif Ag == 'A':
									H3ColorMap += '6'
								elif Ag == 'B':
									H3ColorMap += '2'
								elif Ag == 'C':
									H3ColorMap += '7'
								elif Ag == 'D':
									H3ColorMap += '3'
								elif Ag == 'E':
									H3ColorMap += 'C'
								elif Ag == 'Stalk-MN':
									H3ColorMap += 'A'
								else:
									H3ColorMap += '0'
							elif region == 'HA2':
								if Ag == '-':
									H3ColorMap += '0'
								elif Ag == 'Stalk-MN':
									H3ColorMap += 'A'
								else:
									H3ColorMap += '0'
							else:
								H3ColorMap += '0'
				else:

					H3NumLine += res
					H3ColorMap += '0'

			H3Key = 'H3 Antigenic Sites:  A    B    C    D    E   Stalk-MN \n'
			H3KeyCMap = '000000000000000000066666222227777733333CCCCCAAAAAAAAAA\n'

		if H1NumOn == True:
			ResDown = 0
			ResT = ''

			for pos in range(1, len(H1Numbering)):
				residue = H1Numbering[pos]

				region = residue[0]

				if H3NumOn == False:
					AA = residue[1]
					AASeq += AA
					resPos = str(pos)

					tesResNP = pos / 5
					if resPos == 1:
						NumLine += str(pos)
						AAPosColorMap += '0'

					elif tesResNP.is_integer():  # is divisible by 5
						ResTP = str(pos)
						LenResP = len(ResTP)

						if NumberingMap['H3HA1end'] > (pos + LenResP + 1):
							ResDownP = LenResP
							NumLine += ResTP[LenResP - ResDownP]
							ResDownP -= 1
							AAPosColorMap += '0'
						else:
							NumLine += '.'

							AAPosColorMap += '0'

					else:
						if ResDownP != 0:
							NumLine += ResTP[LenResP - ResDownP]
							AAPosColorMap += '0'
							# H3ColorMap += '0'
							ResDownP -= 1
						else:
							NumLine += '.'
							AAPosColorMap += '0'

					if region == 'HA1':
						NextC = '0'
						InHA1 = True
					elif region == 'HA2':
						InHA2 = True
						NextC = '9'
						HA2K = True
					elif region == 'TM':
						NextC = '8'
						TMK = True
					elif region == 'Trimer-Avitag-H6':
						NextC = 'B'
						TrimK = True
					else:
						NextC = '0'

					if AA == '*':
						NextC = '1'
						StopK = True

					AAColorMap += NextC


				res = residue[2]
				Ag = residue[4]

				if res != '-':
					# if res.is_integer():
					tesResN = res / 5
					if res == 1:
						H1NumLine += str(res)
						H1ColorMap += '5'

					elif tesResN.is_integer(): #is divisible by 5
						ResT = str(res)
						LenRes = len(ResT)
						if region == 'HA1':
							if NumberingMap['H1HA1end'] > (res + LenRes +1):
								ResDown = LenRes
								H1NumLine += ResT[LenRes - ResDown]
								if Ag == '-':
									H1ColorMap += '0'
								elif Ag == 'Cb':
									H1ColorMap += '7'
								elif Ag == 'Ca1':
									H1ColorMap += '2'
								elif Ag == 'Ca2':
									H1ColorMap += '4'
								elif Ag == 'Sa':
									H1ColorMap += '3'
								elif Ag == 'Sb':
									H1ColorMap += '6'
								else:
									H1ColorMap += '0'

								ResDown -= 1
							else:
								H1NumLine += '.'
								if Ag == '-':
									H1ColorMap += '0'
								elif Ag == 'Cb':
									H1ColorMap += '7'
								elif Ag == 'Ca1':
									H1ColorMap += '2'
								elif Ag == 'Ca2':
									H1ColorMap += '4'
								elif Ag == 'Sa':
									H1ColorMap += '3'
								elif Ag == 'Sb':
									H1ColorMap += '6'
								else:
									H1ColorMap += '0'

						elif region == 'HA2':
							if NumberingMap['H1HA2end'] > (res + LenRes + 1):
								ResDown = LenRes
								H1NumLine += ResT[LenRes - ResDown]
								if Ag == '-':
									H1ColorMap += '0'
								elif Ag == 'Stalk-MN':
									H1ColorMap += 'A'
								else:
									H1ColorMap += '0'

								ResDown -= 1
							else:
								H1NumLine += '.'
								if Ag == '-':
									H1ColorMap += '0'
								elif Ag == 'Stalk-MN':
									H1ColorMap += 'A'
								else:
									H1ColorMap += '0'

					else:
						if ResDown != 0:
							H1NumLine += ResT[LenRes - ResDown]
							if region == 'HA1':
								if Ag == '-':
									H1ColorMap += '0'
								elif Ag == 'Cb':
									H1ColorMap += '7'
								elif Ag == 'Ca1':
									H1ColorMap += '2'
								elif Ag == 'Ca2':
									H1ColorMap += '4'
								elif Ag == 'Sa':
									H1ColorMap += '3'
								elif Ag == 'Sb':
									H1ColorMap += '6'
								else:
									H1ColorMap += '0'
							elif region == 'HA2':
								if Ag == '-':
									H1ColorMap += '0'
								elif Ag == 'Stalk-MN':
									H1ColorMap += 'A'
								else:
									H1ColorMap += '0'
							else:
								H1ColorMap += '0'

							ResDown -= 1
						else:
							H1NumLine += '.'
							if region == 'HA1':
								if Ag == '-':
									H1ColorMap += '0'
								elif Ag == 'Cb':
									H1ColorMap += '7'
								elif Ag == 'Ca1':
									H1ColorMap += '2'
								elif Ag == 'Ca2':
									H1ColorMap += '4'
								elif Ag == 'Sa':
									H1ColorMap += '3'
								elif Ag == 'Sb':
									H1ColorMap += '6'
								else:
									H1ColorMap += '0'
							elif region == 'HA2':
								if Ag == '-':
									H1ColorMap += '0'
								elif Ag == 'Stalk-MN':
									H1ColorMap += 'A'
								else:
									H1ColorMap += '0'
							else:
								H1ColorMap += '0'
				else:

					H1NumLine += res
					H1ColorMap += '0'
			H1Key = 'H1 Antigenic Sites:  Ca1    Ca2    Cb    Sa    Sb   Stalk-MN \n'
			H1KeyCMap = '000000000000000000022222224444444777777333333666666AAAAAAAAAA\n'

		SeqName = self.ui.txtSeqName2.toPlainText() + '\n'
		LenSeqName = len(SeqName)

		if DonRegOn == True or MutsOn == True:
			WhereState = "SeqName = " + '"' + self.ui.txtSeqName2.toPlainText() + '"'
			SQLStatement = 'SELECT `Donor`, `Mutations` FROM LibDB WHERE ' + WhereState
			DataIn = RunSQL(DBFilename, SQLStatement)
			donor_info = DataIn[0][0]
			mutation_info = DataIn[0][1]

		if H1NumOn == False and H3NumOn == False:
			for pos in range(1, len(H1Numbering)):
				residue = H1Numbering[pos]
				region = residue[0]

				AA = residue[1]
				AASeq += AA
				resPos = str(pos)

				tesResNP = pos / 5
				if resPos == 1:
					NumLine += str(pos)
					AAPosColorMap += '0'

				elif tesResNP.is_integer():  # is divisible by 5
					ResTP = str(pos)
					LenResP = len(ResTP)

					if NumberingMap['H3HA1end'] > (pos + LenResP + 1):
						ResDownP = LenResP
						NumLine += ResTP[LenResP - ResDownP]
						ResDownP -= 1
						AAPosColorMap += '0'
					else:
						NumLine += '.'

						AAPosColorMap += '0'

				else:
					if ResDownP != 0:
						NumLine += ResTP[LenResP - ResDownP]
						AAPosColorMap += '0'
						# H3ColorMap += '0'
						ResDownP -= 1
					else:
						NumLine += '.'
						AAPosColorMap += '0'

				if region == 'HA1':
					NextC = '0'
					InHA1 = True
				elif region == 'HA2':
					InHA2 = True
					NextC = '9'
					HA2K = True
				elif region == 'TM':
					NextC = '8'
					TMK = True
				elif region == 'Trimer-Avitag-H6':
					NextC = 'B'
					TrimK = True
				else:
					NextC = '0'

				if AA == '*':
					NextC = '1'
					StopK = True

				AAColorMap += NextC


		Sequence = SeqName + '\n'
		ColorMap = ''
		for i in range(0,LenSeqName):
			ColorMap += '0'
		ColorMap += '\n'

		if MutsOn == True:
			if mutation_info == "none":
				# QMessageBox.warning(self, 'Warning',
				#                     'No mutation information for this sequence!', QMessageBox.Ok, QMessageBox.Ok)
				pass
			else:
				mutation_info = mutation_info.rstrip(',')
				mutation_info = mutation_info.split(',')

		if DonRegOn == True:
			if donor_info == 'none':
				# QMessageBox.warning(self, 'Warning',
				#                     'No donor information for this sequence!', QMessageBox.Ok, QMessageBox.Ok)
				pass

		# NumLine += '.'
		# AAPosColorMap += '0'
		for i in range(0, len(AASeq), 60):
			AASeqSeg = AASeq[i:i + 60]
			AAColorSeg = AAColorMap[i:i + 60]
			NumLineSeg = NumLine[i:i + 60]
			AAPosColorSeg = AAPosColorMap[i:i + 60]

			if DonRegOn == True:
				if donor_info != 'none':
					donor_start, donor_end = donor_info.split('-')
					donor_start = int(donor_start) - 1
					donor_end = int(donor_end)

					cur_start = i
					cur_end = i + 60
					# case 1
					if cur_start > donor_end:
						pass
					# case 2
					if cur_start <= donor_end and cur_start >= donor_start and donor_end <= cur_end:
						cur_donor_start = 0
						cur_donor_end = donor_end - cur_start
						AAPosColorSeg = 'D'*cur_donor_end + AAPosColorSeg[cur_donor_end:]
					# case 3
					if cur_start <= donor_start and cur_end >= donor_end:
						cur_donor_start = donor_start - cur_start
						cur_donor_end = donor_end - cur_start
						AAPosColorSeg = AAPosColorSeg[:cur_donor_start] + 'D' * (cur_donor_end - cur_donor_start) +\
						                AAPosColorSeg[cur_donor_end:]
					# case 4
					if cur_end <= donor_end and cur_end >= donor_start and donor_start >= cur_start:
						cur_donor_start = donor_start - cur_start
						cur_donor_end = cur_end - cur_start
						AAPosColorSeg = AAPosColorSeg[:cur_donor_start] + 'D' * \
						                (cur_donor_end - cur_donor_start)
					# case 5
					if cur_start >= donor_start and cur_end <= donor_end:
						AAPosColorSeg = 'D' * 60
					# case 6
					if donor_start > cur_end:
						pass

			NumLineSeg = '    Position: ' + NumLineSeg + '\n'
			AAPosColorSeg = '00000000000000' + AAPosColorSeg + '\n'

			Sequence += NumLineSeg
			ColorMap += AAPosColorSeg

			if H3NumOn == True:
				H3NumSeg = 'H3-Numbering: ' + H3NumLine[i:i+60] + '\n'
				H3ColorSeg = '00000000000000' + H3ColorMap[i:i + 60] + '\n'
				Sequence += H3NumSeg
				ColorMap += H3ColorSeg

			if H1NumOn == True:
				H1NumSeg = 'H1-Numbering: ' + H1NumLine[i:i + 60] + '\n'
				H1ColorSeg = '00000000000000' + H1ColorMap[i:i + 60] + '\n'
				Sequence += H1NumSeg
				ColorMap += H1ColorSeg

			if MutsOn == True:
				cur_start = i
				cur_end = i + 60

				if mutation_info != "none":
					for x in mutation_info:
						mutation_pos = re.findall(r"\d+",x)
						mutation_pos = int(mutation_pos[0]) - 1

						if mutation_pos in range(cur_start, cur_end):
							AAColorSeg = list(AAColorSeg)
							AAColorSeg[mutation_pos - cur_start] = 'E'
							AAColorSeg = ''.join(AAColorSeg)

			AASeqSeg = '    Sequence: ' + AASeqSeg + '\n\n'
			AAColorSeg = '00000000000000' + AAColorSeg + '\n\n'

			Sequence += AASeqSeg
			ColorMap += AAColorSeg

		Sequence += ' \n'
		ColorMap += '0\n'


		Sequence += AAKey + H3Key + H1Key + PosKey
		ColorMap += AAKeyC + H3KeyCMap + H1KeyCMap + PosKeyC
		# Add note at begining that HA1 is black andHA2 is grey or
		self.ui.txtAASeq.setText(Sequence)
		self.DecorateText(ColorMap, cursor)

	@pyqtSlot()
	def DecorateText(self, ColorMap, cursor):
		# setup default color for all text
		format = QTextCharFormat()
		format.setBackground(QBrush(QColor("white")))
		format.setForeground(QBrush(QColor("black")))

		cursor.setPosition(0)
		cursor.setPosition(len(ColorMap), QTextCursor.KeepAnchor)
		cursor.mergeCharFormat(format)

		# Setup the desired format for matches
		CurPos = 0
		for valueIs in ColorMap:  #QColor is RGB: 0-255, 0-255, 0-255
			if valueIs == '0':
				CurPos += 1
				continue
			elif valueIs == '1':
				format.setBackground(QBrush(QColor(255,00,0))) #or 'red'
				format.setForeground(QBrush(QColor("black")))
			elif valueIs == '2':
				format.setBackground(QBrush(QColor("darkMagenta")))
				format.setForeground(QBrush(QColor("white")))
			elif valueIs == '3':
				format.setBackground(QBrush(QColor("darkred")))
				format.setForeground(QBrush(QColor("white")))
			elif valueIs == '3':
				format.setBackground(QBrush(QColor("Magenta")))
				format.setForeground(QBrush(QColor("black")))
			elif valueIs == '4':
				format.setBackground(QBrush(QColor("yellow")))
				format.setForeground(QBrush(QColor("black")))
			elif valueIs == '5':
				format.setBackground(QBrush(QColor("black")))
				format.setForeground(QBrush(QColor("white")))
			elif valueIs == '6':
				format.setBackground(QBrush(QColor("green")))
				format.setForeground(QBrush(QColor("white")))
			elif valueIs == '7':
				format.setBackground(QBrush(QColor("lightGray")))
				format.setForeground(QBrush(QColor("black")))
			elif valueIs == '8':
				format.setBackground(QBrush(QColor("yellow")))
				format.setForeground(QBrush(QColor("black")))
			elif valueIs == '9':
				format.setBackground(QBrush(QColor("lightGray")))
				format.setForeground(QBrush(QColor("black")))
			elif valueIs == '10':
				format.setBackground(QBrush(QColor("black")))
				format.setForeground(QBrush(QColor("white")))
			elif valueIs == 'A':
				format.setBackground(QBrush(QColor("darkBlue")))
				format.setForeground(QBrush(QColor("white")))
			elif valueIs == 'B':
				format.setBackground(QBrush(QColor("darkGreen")))
				format.setForeground(QBrush(QColor("white")))
			elif valueIs == 'C':
				format.setBackground(QBrush(QColor("blue")))
				format.setForeground(QBrush(QColor("yellow")))
			elif valueIs == 'D':
				format.setBackground(QBrush(QColor("Gray")))
				format.setForeground(QBrush(QColor("black")))
			elif valueIs == 'E':
				format.setBackground(QBrush(QColor("lightGray")))
				format.setForeground(QBrush(QColor("red")))


			cursor.setPosition(CurPos)
			cursor.setPosition(CurPos + 1, QTextCursor.KeepAnchor)
			cursor.mergeCharFormat(format)

			CurPos += 1

	@pyqtSlot()
	def DecorateTextOld(self, ColorMap, cursor):
		# Setup the desired format for matches
		format = QTextCharFormat()
		CurPos = 0
		for valueIs in ColorMap:  # QColor is RGB: 0-255, 0-255, 0-255
			if valueIs == '0':
				format.setBackground(QBrush(QColor("white")))
				format.setForeground(QBrush(QColor("black")))
			elif valueIs == '1':
				format.setBackground(QBrush(QColor(255, 00, 0)))  # or 'red'
				format.setForeground(QBrush(QColor("black")))
			elif valueIs == '2':
				format.setBackground(QBrush(QColor("darkMagenta")))
				format.setForeground(QBrush(QColor("white")))
			elif valueIs == '3':
				format.setBackground(QBrush(QColor("darkred")))
				format.setForeground(QBrush(QColor("white")))
			elif valueIs == '3':
				format.setBackground(QBrush(QColor("Magenta")))
				format.setForeground(QBrush(QColor("black")))
			elif valueIs == '4':
				format.setBackground(QBrush(QColor("yellow")))
				format.setForeground(QBrush(QColor("black")))
			elif valueIs == '5':
				format.setBackground(QBrush(QColor("black")))
				format.setForeground(QBrush(QColor("white")))
			elif valueIs == '6':
				format.setBackground(QBrush(QColor("green")))
				format.setForeground(QBrush(QColor("white")))
			elif valueIs == '7':
				format.setBackground(QBrush(QColor("lightGray")))
				format.setForeground(QBrush(QColor("black")))
			elif valueIs == '8':
				format.setBackground(QBrush(QColor("yellow")))
				format.setForeground(QBrush(QColor("black")))
			elif valueIs == '9':
				format.setBackground(QBrush(QColor("lightGray")))
				format.setForeground(QBrush(QColor("black")))
			elif valueIs == '10':
				format.setBackground(QBrush(QColor("black")))
				format.setForeground(QBrush(QColor("white")))
			elif valueIs == 'A':
				format.setBackground(QBrush(QColor("darkBlue")))
				format.setForeground(QBrush(QColor("white")))
			elif valueIs == 'B':
				format.setBackground(QBrush(QColor("darkGreen")))
				format.setForeground(QBrush(QColor("white")))
			elif valueIs == 'C':
				format.setBackground(QBrush(QColor("blue")))
				format.setForeground(QBrush(QColor("yellow")))
			elif valueIs == 'D':
				format.setBackground(QBrush(QColor("Gray")))
				format.setForeground(QBrush(QColor("black")))
			elif valueIs == 'E':
				format.setBackground(QBrush(QColor("lightGray")))
				format.setForeground(QBrush(QColor("red")))

			cursor.setPosition(CurPos)
			cursor.setPosition(CurPos + 1, QTextCursor.KeepAnchor)
			cursor.mergeCharFormat(format)

			CurPos += 1

	def AlignSequencesFusion(self, DataIn, Notes, dnaCheck, aaCheck, posCheck):
		# import tempfile
		import os
		TupData = ()
		DataSet = []
		QApplication.setOverrideCursor(Qt.WaitCursor)
		global GLMsg
		global working_prefix
		global clustal_path
		global temp_folder
		global VGenesTextWindows

		DataSet = DataIn

		# align selected sequences using ClustalOmega
		outfilename = ''
		try:
			if len(DataSet) == 1:
				time_stamp = str(int(time.time() * 100))
				outfilename = os.path.join(temp_folder, "out-" + time_stamp + ".fas")
				out_handle = open(outfilename, 'w')
				out_handle.write('>' + DataSet[0][0] + '\n')
				out_handle.write(DataSet[0][1])
				out_handle.close()
			else:
				if os.path.exists(clustal_path):
					outfilename = LibratorSeq.ClustalO(DataSet, 80, True, temp_folder, clustal_path)
				else:
					QMessageBox.warning(self, 'Warning',
					                    'The Clustal Omega does not exist! Check your path!', QMessageBox.Ok,
					                    QMessageBox.Ok)
					return

			lenName = 0
			longestName = 0
			alignmentText = ''
			ColorMap = ''
			germseq = ''
			germpeptide = ''

			each = ()
			all = []
			longestName = 10

			peptide = ''
			SeqName = ''
			StartAll = False

			# read alignment file, make alignment NT and AA sequences
			if os.path.isfile(outfilename):
				with open(outfilename, 'r') as currentfile:
					for line in currentfile:
						Readline = line.replace('\n', '').replace('\r', '').replace('-', '.')
						Readline = Readline.strip()
						if Readline[0] == '>':
							if StartAll == True:
								all.append(each)
							StartAll = True
							SeqName = Readline[1:] + ':'
							lenName = len(SeqName)
							if lenName > longestName:
								longestName = lenName + 2
						else:
							AASeq, ErMessage = LibratorSeq.Translator(Readline, 0)
							# Position, Amino Acid, H1-segment (HA1 or HA2), H1Number, A/California/4/2009-residue, H1-antigenic-region

							if DataIn == 'RF':
								AASeq2, ErMessage = LibratorSeq.Translator(Readline, 1)
								AASeq3, ErMessage = LibratorSeq.Translator(Readline, 2)
							peptide = ''
							if DataIn == 'RF':
								peptide2 = ''
								peptide3 = ''

							for res in AASeq:
								peptide += (' ' + res + ' ')

							if DataIn == 'RF':
								for res in AASeq2:
									peptide2 += (' ' + res + ' ')
								for res in AASeq3:
									peptide3 += (' ' + res + ' ')

							peptide = peptide[0:len(Readline)]

							if DataIn == 'RF':
								peptide = peptide[1:]
								peptide2 = peptide2[0:len(Readline)]

							if DataIn == 'RF':
								peptide3 = peptide3[0:len(Readline)]
								peptide3 = ' ' + peptide3

							if SeqName != 'Germline:':
								if DataIn == 'RF':
									each = (SeqName, Readline, peptide, peptide2, peptide3)
								else:
									each = (SeqName, Readline, peptide)
							else:
								germseq = Readline
								germpeptide = peptide
								StartAll = False
				if StartAll == True:
					all.append(each)
			else:
				return
		# todo add header that says what germline based on
		except:
			print('no')

		finally:
			if os.path.exists(outfilename):
				os.remove(outfilename)

		# generate consnesus sequences (AA and NT)
		if len(all) == 1:
			consensusDNA = all[0][1]
			consensusAA = all[0][2]
		else:
			firstOne = all[1]
			seqlen = len(firstOne[1])

			consensusDNA = ''
			tester = ''
			for i in range(0, seqlen - 1):
				tester = ''
				Cnuc = ''
				for item in all:
					seq = item[1]
					tester += seq[i]

				frequencies = [(c, tester.count(c)) for c in set(tester)]
				Cnuc = max(frequencies, key=lambda x: x[1])[0]
				consensusDNA += Cnuc

			consensusAA = ''
			firstOne = all[1]
			seqlen = len(firstOne[1])
			for i in range(0, seqlen - 1):
				tester = ''
				Caa = ''
				for item in all:
					seq = item[2]
					tester += seq[i]

				frequencies = [(c, tester.count(c)) for c in set(tester)]
				Caa = max(frequencies, key=lambda x: x[1])[0]
				consensusAA += Caa

		# align consensus AA sequence with template to generate H1 and H3 numbering
		if posCheck == True:
			compact_consensusAA = consensusAA.replace(' ', '')
			HANumbering(compact_consensusAA)

		header = 'VGenes multiple alignment using Clustal Omega. \n'
		RFSeqName = self.ui.txtName.toPlainText()
		ConName = 'Consensus: '

		if DataIn == 'RF': ConName = 'Sequence: '

		while len(ConName) < longestName:
			ConName += ' '

		AASpaces = ''
		while len(AASpaces) < longestName:
			AASpaces += ' '

		alignmentText = header
		ColorMap += '0' * (len(header) - 1) + '\n'
		i = 0
		endSeg = 0
		done = False
		ConAdd = True

		if dnaCheck == True:
			maxLen = len(consensusDNA)
		else:
			NewConAA = consensusAA.replace(' ', '')
			maxLen = len(NewConAA)

		# canAA = True
		while endSeg <= maxLen - 1:
			if i + 60 < maxLen:
				endSeg = i + 60
			else:
				endSeg = maxLen

			aa_start = int(i / 3 + 1)
			aa_end = int(endSeg / 3)
			if posCheck == True:
				rulerAA = 'Position(AA)' + AASpaces[12:] + self.MakeRuler(aa_start, aa_end, 5, 'aa')
				rulerNT = 'Position(NT)' + AASpaces[12:] + self.MakeRuler(i + 1, endSeg, 5, 'nt')
				if aaCheck == True and dnaCheck == True:
					rulerH1 = 'H1numbering' + AASpaces[11:]
					rulerH1Color = '0' * len(rulerH1)
					rulerH3 = 'H3numbering' + AASpaces[11:]
					rulerH3Color = '0' * len(rulerH3)

					# make H1 numbering
					space_from_last_pos = 0
					for x in range(aa_start, aa_end + 1):
						if H1Numbering[x][2] == '-':
							rulerH1 += ' ' * (1 - space_from_last_pos) + '- '
							space_from_last_pos = 0
							rulerH1Color += '000'
						else:
							if int(H1Numbering[x][2]) % 5 == 0:
								if len(str(H1Numbering[x][2])) == 1:
									rulerH1 += ' ' * (1 - space_from_last_pos) + str(H1Numbering[x][2]) + ' '
									space_from_last_pos = 0
								elif len(str(H1Numbering[x][2])) == 2:
									rulerH1 += ' ' * (1 - space_from_last_pos) + str(H1Numbering[x][2])
									space_from_last_pos = 0
								else:
									rulerH1 += ' ' * (1 - space_from_last_pos) + str(H1Numbering[x][2])
									space_from_last_pos = 1
							else:
								rulerH1 += ' ' * (1 - space_from_last_pos) + '. '
								space_from_last_pos = 0
							if H1Numbering[x][4] == "Cb":
								rulerH1Color += '777'
							elif H1Numbering[x][4] == "Ca1":
								rulerH1Color += '222'
							elif H1Numbering[x][4] == "Ca2":
								rulerH1Color += '444'
							elif H1Numbering[x][4] == "Sa":
								rulerH1Color += '333'
							elif H1Numbering[x][4] == "Sb":
								rulerH1Color += '666'
							elif H1Numbering[x][4] == "Stalk-MN":
								rulerH1Color += 'AAA'
							else:
								rulerH1Color += '000'
					if space_from_last_pos == 1:
						rulerH1Color += rulerH1Color[-1]

					# make H3 numbering
					space_from_last_pos = 0
					for x in range(aa_start, aa_end + 1):
						if H3Numbering[x][2] == '-':
							rulerH3 += ' ' * (1 - space_from_last_pos) + '- '
							space_from_last_pos = 0
							rulerH3Color += '000'
						else:
							if int(H3Numbering[x][2]) % 5 == 0:
								if len(str(H3Numbering[x][2])) == 1:
									rulerH3 += ' ' * (1 - space_from_last_pos) + str(H3Numbering[x][2]) + ' '
									space_from_last_pos = 0
								elif len(str(H3Numbering[x][2])) == 2:
									rulerH3 += ' ' * (1 - space_from_last_pos) + str(H3Numbering[x][2])
									space_from_last_pos = 0
								else:
									rulerH3 += ' ' * (1 - space_from_last_pos) + str(H3Numbering[x][2])
									space_from_last_pos = 1
							else:
								rulerH3 += ' ' * (1 - space_from_last_pos) + '. '
								space_from_last_pos = 0
							if H3Numbering[x][4] == "A":
								rulerH3Color += '666'
							elif H3Numbering[x][4] == "B":
								rulerH3Color += '222'
							elif H3Numbering[x][4] == "C":
								rulerH3Color += '777'
							elif H3Numbering[x][4] == "D":
								rulerH3Color += '333'
							elif H3Numbering[x][4] == "E":
								rulerH3Color += 'CCC'
							elif H3Numbering[x][4] == "Stalk-MN":
								rulerH3Color += 'AAA'
							else:
								rulerH3Color += '000'
					if space_from_last_pos == 1:
						rulerH3Color += rulerH3Color[-1]
				elif aaCheck == True and dnaCheck == False:
					aa_start = i + 1
					aa_end = endSeg

					rulerH1 = 'H1numbering' + AASpaces[11:]
					rulerH1Color = '0' * len(rulerH1)
					rulerH3 = 'H3numbering' + AASpaces[11:]
					rulerH3Color = '0' * len(rulerH3)

					# make H1 numbering
					space_from_last_pos = 0
					for x in range(aa_start, aa_end + 1):
						if H1Numbering[x][2] == '-':
							if space_from_last_pos == 2:
								rulerH1Color += '0'
								space_from_last_pos = space_from_last_pos - 1
							elif space_from_last_pos == 1:
								rulerH1Color += '0'
								space_from_last_pos = space_from_last_pos - 1
							else:
								rulerH1 += '-'
								rulerH1Color += '0'
						else:
							if int(H1Numbering[x][2]) % 5 == 0:
								if len(str(H1Numbering[x][2])) == 1:
									rulerH1 += str(H1Numbering[x][2])
									space_from_last_pos = 0
								elif len(str(H1Numbering[x][2])) == 2:
									rulerH1 += str(H1Numbering[x][2])
									space_from_last_pos = 1
								else:
									rulerH1 += str(H1Numbering[x][2])
									space_from_last_pos = 2
							else:
								if space_from_last_pos == 2:
									space_from_last_pos = space_from_last_pos - 1
								elif space_from_last_pos == 1:
									space_from_last_pos = space_from_last_pos - 1
								else:
									rulerH1 += '.'

							if H1Numbering[x][4] == "Cb":
								rulerH1Color += '7'
							elif H1Numbering[x][4] == "Ca1":
								rulerH1Color += '2'
							elif H1Numbering[x][4] == "Ca2":
								rulerH1Color += '4'
							elif H1Numbering[x][4] == "Sa":
								rulerH1Color += '3'
							elif H1Numbering[x][4] == "Sb":
								rulerH1Color += '6'
							elif H1Numbering[x][4] == "Stalk-MN":
								rulerH1Color += 'A'
							else:
								rulerH1Color += '0'
					if space_from_last_pos == 2:
						# rulerH1Color += rulerH1Color[-1] * 2
						rulerH1Color += '00'
					elif space_from_last_pos == 1:
						# rulerH1Color += rulerH1Color[-1]
						rulerH1Color += '0'

					# make H3 numbering
					space_from_last_pos = 0
					for x in range(aa_start, aa_end + 1):
						if H3Numbering[x][2] == '-':
							if space_from_last_pos == 2:
								space_from_last_pos = space_from_last_pos - 1
								rulerH3Color += '0'
							elif space_from_last_pos == 1:
								space_from_last_pos = space_from_last_pos - 1
								rulerH3Color += '0'
							else:
								rulerH3 += '-'
								rulerH3Color += '0'
						else:
							if int(H3Numbering[x][2]) % 5 == 0:
								if len(str(H3Numbering[x][2])) == 1:
									rulerH3 += str(H3Numbering[x][2])
									space_from_last_pos = 0
								elif len(str(H3Numbering[x][2])) == 2:
									rulerH3 += str(H3Numbering[x][2])
									space_from_last_pos = 1
								else:
									rulerH3 += str(H3Numbering[x][2])
									space_from_last_pos = 2
							else:
								if space_from_last_pos == 2:
									space_from_last_pos = space_from_last_pos - 1
								elif space_from_last_pos == 1:
									space_from_last_pos = space_from_last_pos - 1
								else:
									rulerH3 += '.'

							if H3Numbering[x][4] == "A":
								rulerH3Color += '6'
							elif H3Numbering[x][4] == "B":
								rulerH3Color += '2'
							elif H3Numbering[x][4] == "C":
								rulerH3Color += '7'
							elif H3Numbering[x][4] == "D":
								rulerH3Color += '3'
							elif H3Numbering[x][4] == "E":
								rulerH3Color += 'C'
							elif H3Numbering[x][4] == "Stalk-MN":
								rulerH3Color += 'A'
							else:
								rulerH3Color += '0'
					if space_from_last_pos == 2:
						# rulerH3Color += rulerH1Color[-1] * 2
						rulerH3Color += '00'
					elif space_from_last_pos == 1:
						# rulerH3Color += rulerH1Color[-1]
						rulerH3Color += '0'

			for seq in all:
				SeqName = seq[0]
				DNASeq = seq[1]
				AASeq = seq[2]
				if DataIn == 'RF':
					AASeq2 = seq[3]
					AASeq3 = seq[4]

				NewAA = AASeq.replace(' ', '')
				if DataIn == 'RF':
					NewAA2 = AASeq2.replace(' ', '')
					NewAA3 = AASeq3.replace(' ', '')

				while len(SeqName) < longestName:
					SeqName += ' '
				# todo can build num line even add CDR if align relative to germline instead just number as end
				toSpace = len(str(maxLen))
				endLabel = str(endSeg)
				while len(endLabel) < toSpace:
					endLabel += ' '
				endLabel = '  ' + endLabel

				if dnaCheck == True:

					ConSegDNA = consensusDNA[i:endSeg]
					DNASeqSeg = DNASeq[i:endSeg]
					ConSegDNA = ConSegDNA.upper()
					DNASeqSeg = DNASeqSeg.upper()

					DNAArt = ''
					for n in range(0, len(ConSegDNA)):
						if DNASeqSeg[n] == ConSegDNA[n]:
							if DataIn == 'RF':
								DNAArt += '-'
							else:
								char = DNASeqSeg[n]
								char = char.upper()
								# DNAArt += char
								DNAArt += '-'
						else:
							if DataIn == 'RF':
								DNAArt += DNASeqSeg[n]
							else:
								char = DNASeqSeg[n]
								char = char.lower()
								DNAArt += char

					ConSegDNA = ConName + ConSegDNA + endLabel
					DNASeqSeg = SeqName + DNAArt + endLabel
					if aaCheck == True:
						AArt = ''
						ConSegAA = consensusAA[i:endSeg]
						if DataIn == 'RF': ConSegAA2 = AASeq2[i:endSeg]
						if DataIn == 'RF': ConSegAA3 = AASeq3[i:endSeg]

						AASeqSeg = AASeq[i:endSeg]

						for n in range(0, len(ConSegAA)):
							if AASeqSeg[n] == ConSegAA[n]:
								AArt += ' '
							else:
								AArt += AASeqSeg[n]

						AASeqSeg = AASpaces + AArt  # + endLabel
						if DataIn == 'RF':
							ConSegAA = AASpaces + 'RF1: ' + ConSegAA
						else:
							ConSegAA = AASpaces + ConSegAA

						if DataIn == 'RF':
							ConSegAA2 = AASpaces + 'RF2: ' + ConSegAA2
							ConSegAA3 = AASpaces + 'RF3: ' + ConSegAA3

						if ConAdd == True:
							if posCheck == True:
								alignmentText += '\n' + rulerAA
								ColorMap += '\n' + '0' * len(rulerAA)
								alignmentText += '\n' + rulerH1
								ColorMap += '\n' + rulerH1Color
								alignmentText += '\n' + rulerH3
								ColorMap += '\n' + rulerH3Color

							alignmentText += '\n' + ConSegAA + '\n'
							ColorMap += '\n' + '0' * len(ConSegAA) + '\n'
							if DataIn == 'RF':
								alignmentText += '\n' + ConSegAA2 + '\n'
								alignmentText += '\n' + ConSegAA3 + '\n'
								alignmentText += '     ' + ConSegDNA + '\n'
							else:
								if posCheck == True:
									alignmentText += rulerNT + '\n'
									ColorMap += '0' * len(rulerNT) + '\n'

								alignmentText += ConSegDNA + '\n'
								ColorMap += '0' * len(ConSegDNA) + '\n'
							ConAdd = False
						if DataIn != 'RF':
							alignmentText += AASeqSeg + '\n'
							ColorMap += '0' * len(AASeqSeg) + '\n'
							alignmentText += DNASeqSeg + '\n'
							ColorMap += '0' * len(DNASeqSeg) + '\n'
					else:
						if ConAdd == True:
							if posCheck == True:
								alignmentText += '\n' + rulerNT
								ColorMap += '0' * len(rulerNT)
							alignmentText += '\n' + ConSegDNA + '\n'
							ColorMap += '\n' + '0' * len(ConSegDNA) + '\n'
							ConAdd = False
						if DataIn != 'RF':
							alignmentText += DNASeqSeg + '\n'
							ColorMap += '0' * len(DNASeqSeg) + '\n'
				else:
					if aaCheck == True:
						AArt = ''
						ConSegAA = NewConAA[i:endSeg]
						AASeqSeg = NewAA[i:endSeg]

						for n in range(0, len(ConSegAA)):
							if AASeqSeg[n] == ConSegAA[n]:
								AArt += '-'
							else:
								AArt += AASeqSeg[n]

						AASeqSeg = SeqName + AArt + endLabel
						ConSegAA = ConName + ConSegAA
						if ConAdd == True:
							if posCheck == True:
								alignmentText += '\n' + 'Position(AA)' + rulerNT[12:]
								ColorMap += '\n' + '0' * len(rulerNT)
								alignmentText += '\n' + rulerH1
								ColorMap += '\n' + rulerH1Color
								alignmentText += '\n' + rulerH3
								ColorMap += '\n' + rulerH3Color
							alignmentText += '\n' + ConSegAA + '\n'
							ColorMap += '\n' + '0' * len(ConSegAA) + '\n'
							ConAdd = False
						alignmentText += AASeqSeg + '\n'
						ColorMap += '0' * len(AASeqSeg) + '\n'

			i += 60
			ConAdd = True
			alignmentText += '\n'
			ColorMap += '\n'

		Style = 'aligned'

		# legend text and color
		legend_text = 'H1 Antigenic Sites:  Ca1    Ca2    Cb    Sa    Sb   Stalk-MN \n' + \
		              'H3 Antigenic Sites:  A    B    C    D    E   Stalk-MN \n'
		legend_color = '000000000000000000022222224444444777777333333666666AAAAAAAAAA\n' + \
		               '000000000000000000066666222227777733333CCCCCAAAAAAAAAA\n'
		if Notes != 'Tab':
			window_id = int(time.time() * 100)
			VGenesTextWindows[window_id] = VGenesTextMain()
			VGenesTextWindows[window_id].id = window_id
			VGenesTextWindows[window_id].data = DataIn
			VGenesTextWindows[window_id].note = Notes
			VGenesTextWindows[window_id].type = 'Alignment'
			VGenesTextWindows[window_id].dnaAct.setChecked(dnaCheck)
			VGenesTextWindows[window_id].aaAct.setChecked(aaCheck)
			VGenesTextWindows[window_id].baAct.setChecked(posCheck)

			self.ShowVGenesTextEdit(alignmentText, Style, ColorMap, window_id)
			self.ShowVGenesTextEditLegend(legend_text, legend_color, window_id)
		else:
			self.ui.txtSeqAlignment.setText(alignmentText)

		QApplication.restoreOverrideCursor()

	@pyqtSlot()
	def AlignSequences(self, DataIn, Notes):
		# import tempfile
		import os
		TupData = ()
		DataSet = []
		QApplication.setOverrideCursor(Qt.WaitCursor)
		global GLMsg
		global working_prefix
		global clustal_path
		global temp_folder
		global VGenesTextWindows

		if self.ui.actionDNA.isChecked() == False and self.ui.actionAA.isChecked() == False:
			QMessageBox.warning(self, 'Warning', 'Neither DNA nor AA has been selected! Will generate DNA alignment!',
								QMessageBox.Ok, QMessageBox.Ok)
			self.ui.actionDNA.setChecked(True)

		if DataIn == 'RF':  #can use this part for reading frames
			fields = ['SeqName', 'Sequence']
			# checkedProjects, checkedGroups, checkedSubGroups, checkedkids = getTreeChecked()
			# SQLStatement = LibratorSQL.MakeSQLStatement(self, fields, data[0])
			#
			#
			# DataIs = VGenesSQL.RunSQL(DBFilename, SQLStatement)  # returns list of tuples where seqname is first

			# SeqName = self.ui.txtName.toPlainText()
			SeqName = 'Current'
			DNASeq = self.ui.textSeq.toPlainText()
			# GermSeq = DNASeq
			TupData  = (SeqName, DNASeq)
			DataSet.append(TupData)

			global GLMsg
			if len(DataSet) == 1:
				GLMsg = False
				self.ui.actionBA.setChecked(True)
				self.ui.actionAA.setChecked(True)
				GLMsg = True
				GermSeq = DNASeq
				Germline = ('Germline', GermSeq)
				DataSet.append(Germline)
			else:
				if self.ui.actionBA.isChecked() == True:
					GLMsg = True
					GermSeq = DNASeq
					Germline = ('Germline', GermSeq)
					DataSet.append(Germline)
		elif DataIn == 'edit':
			DataIn = 'none'
			# DataIs = []

			# SeqName = data[0]

			# DNAseq = self.ui.txtDNASeq.toPlainText()
			# Sequence = (SeqName, DNAseq)
			# DataSet.append(Sequence)


			if len(DataSet) == 1:
				GLMsg = False
				self.ui.actionBA.setChecked(True)
				self.ui.actionAA.setChecked(True)
				GLMsg = True
				GermSeq = self.ui.textSeq.toPlainText()
				Germline = ('Germline', GermSeq)
				DataSet.append(Germline)
		else:
			DataSet = DataIn

		# align selected sequences using ClustalOmega
		outfilename = ''
		try:
			if len(DataSet) == 1:
				time_stamp = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime())
				outfilename = os.path.join(temp_folder, "out-" + time_stamp + ".fas")
				out_handle = open(outfilename,'w')
				out_handle.write('>' + DataSet[0][0] + '\n')
				out_handle.write(DataSet[0][1])
				out_handle.close()
			else:
				if os.path.exists(clustal_path):
					outfilename = LibratorSeq.ClustalO(DataSet, 80, True, temp_folder, clustal_path)
				else:
					QMessageBox.warning(self, 'Warning',
					                    'The Clustal Omega does not exist! Check your path!', QMessageBox.Ok, QMessageBox.Ok)
					return

			lenName = 0
			longestName = 0
			alignmentText = ''
			ColorMap = ''
			germseq = ''
			germpeptide = ''

			each = ()
			all = []
			if self.ui.actionBA.isChecked() == False:
				longestName = 11
			else:
				longestName = 10

			peptide = ''
			SeqName = ''
			StartAll = False

			# read alignment file, make alignment NT and AA sequences
			if os.path.isfile(outfilename):
				with open(outfilename, 'r') as currentfile:
					for line in currentfile:
						Readline = line.replace('\n', '').replace('\r', '').replace('-', '.')
						Readline = Readline.strip()
						if Readline[0] == '>':
							if StartAll == True:
								all.append(each)
							StartAll = True
							SeqName = Readline[1:] + ':'
							lenName = len(SeqName)
							if lenName > longestName:
								longestName = lenName + 2
						else:
							AASeq, ErMessage = LibratorSeq.Translator(Readline, 0)
							#Position, Amino Acid, H1-segment (HA1 or HA2), H1Number, A/California/4/2009-residue, H1-antigenic-region

							if DataIn == 'RF':
								AASeq2, ErMessage = LibratorSeq.Translator(Readline, 1)
								AASeq3, ErMessage = LibratorSeq.Translator(Readline, 2)
							peptide = ''
							if DataIn == 'RF':
								peptide2 = ''
								peptide3 = ''

							for res in AASeq:
								peptide += (' ' + res + ' ')

							if DataIn == 'RF':
								for res in AASeq2:
									peptide2 += (' ' + res + ' ')
								for res in AASeq3:
									peptide3 += (' ' + res + ' ')

							peptide = peptide[0:len(Readline)]

							if DataIn == 'RF':
								peptide = peptide[1:]
								peptide2 = peptide2[0:len(Readline)]

							if DataIn == 'RF':
								peptide3 = peptide3[0:len(Readline)]
								peptide3 = ' ' + peptide3

							if SeqName != 'Germline:':
								if DataIn == 'RF':
									each = (SeqName, Readline, peptide, peptide2, peptide3)
								else:
									each = (SeqName, Readline, peptide)
							else:
								germseq = Readline
								germpeptide = peptide
								StartAll = False
				if StartAll == True:
					all.append(each)
			else:
				return
		# todo add header that says what germline based on
		except:
			print('no')

		finally:
			if os.path.exists(outfilename):
				os.remove(outfilename)

		# generate consnesus sequences (AA and NT)
		if len(all) == 1:
			consensusDNA = all[0][1]
			consensusAA = all[0][2]
		else:
			firstOne = all[1]
			seqlen = len(firstOne[1])

			consensusDNA = ''
			tester = ''
			for i in range(0, seqlen - 1):
				tester = ''
				Cnuc = ''
				for item in all:
					seq = item[1]
					tester += seq[i]

				frequencies = [(c, tester.count(c)) for c in set(tester)]
				Cnuc = max(frequencies, key=lambda x: x[1])[0]
				consensusDNA += Cnuc

			consensusAA = ''
			firstOne = all[1]
			seqlen = len(firstOne[1])
			for i in range(0, seqlen - 1):
				tester = ''
				Caa = ''
				for item in all:
					seq = item[2]
					tester += seq[i]

				frequencies = [(c, tester.count(c)) for c in set(tester)]
				Caa = max(frequencies, key=lambda x: x[1])[0]
				consensusAA += Caa

		# align consensus AA sequence with template to generate H1 and H3 numbering
		if self.ui.actionBA.isChecked() == True:
			compact_consensusAA = consensusAA.replace(' ', '')
			HANumbering(compact_consensusAA)

		header = 'VGenes multiple alignment using Clustal Omega. \n'
		RFSeqName = self.ui.txtName.toPlainText()
		ConName = 'Consensus: '

		if DataIn == 'RF': ConName = 'Sequence: '

		while len(ConName) < longestName:
			ConName += ' '

		AASpaces = ''
		while len(AASpaces) < longestName:
			AASpaces += ' '

		alignmentText = header
		ColorMap += '0' * (len(header) - 1) + '\n'
		i = 0
		endSeg = 0
		done = False
		ConAdd = True

		if self.ui.actionDNA.isChecked() == True:
			maxLen = len(consensusDNA)
		else:
			NewConAA = consensusAA.replace(' ', '')
			maxLen = len(NewConAA)

		# canAA = True
		while endSeg <= maxLen - 1:
			if i + 60 < maxLen:
				endSeg = i + 60
			else:
				endSeg = maxLen

			aa_start = int(i/3 + 1)
			aa_end = int(endSeg/3)
			if self.ui.actionBA.isChecked() == True:
				rulerAA = 'Position(AA)' + AASpaces[12:] + MakeRuler(aa_start, aa_end, 5, 'aa')
				rulerNT = 'Position(NT)' + AASpaces[12:] + MakeRuler(i + 1, endSeg, 5, 'nt')
				if self.ui.actionAA.isChecked() == True and self.ui.actionDNA.isChecked() == True:
					rulerH1 = 'H1numbering' + AASpaces[11:]
					rulerH1Color = '0' * len(rulerH1)
					rulerH3 = 'H3numbering' + AASpaces[11:]
					rulerH3Color = '0' * len(rulerH3)

					# make H1 numbering
					space_from_last_pos = 0
					for x in range(aa_start,aa_end + 1):
						if H1Numbering[x][2] == '-':
							rulerH1 += ' ' * (1 - space_from_last_pos) + '- '
							space_from_last_pos = 0
							rulerH1Color += '000'
						else:
							if int(H1Numbering[x][2])%5 == 0:
								if len(str(H1Numbering[x][2])) == 1:
									rulerH1 += ' ' * (1 - space_from_last_pos) + str(H1Numbering[x][2]) + ' '
									space_from_last_pos = 0
								elif len(str(H1Numbering[x][2])) == 2:
									rulerH1 += ' ' * (1 - space_from_last_pos) + str(H1Numbering[x][2])
									space_from_last_pos = 0
								else:
									rulerH1 += ' ' * (1 - space_from_last_pos) + str(H1Numbering[x][2])
									space_from_last_pos = 1
							else:
								rulerH1 += ' ' * (1 - space_from_last_pos) + '. '
								space_from_last_pos = 0
							if H1Numbering[x][4] == "Cb":
								rulerH1Color += '777'
							elif H1Numbering[x][4] == "Ca1":
								rulerH1Color += '222'
							elif H1Numbering[x][4] == "Ca2":
								rulerH1Color += '444'
							elif H1Numbering[x][4] == "Sa":
								rulerH1Color += '333'
							elif H1Numbering[x][4] == "Sb":
								rulerH1Color += '666'
							elif H1Numbering[x][4] == "Stalk-MN":
								rulerH1Color += 'AAA'
							else:
								rulerH1Color += '000'
					if space_from_last_pos == 1:
						rulerH1Color += rulerH1Color[-1]

					# make H3 numbering
					space_from_last_pos = 0
					for x in range(aa_start,aa_end + 1):
						if H3Numbering[x][2] == '-':
							rulerH3 += ' ' * (1 - space_from_last_pos) + '- '
							space_from_last_pos = 0
							rulerH3Color += '000'
						else:
							if int(H3Numbering[x][2])%5 == 0:
								if len(str(H3Numbering[x][2])) == 1:
									rulerH3 += ' ' * (1 - space_from_last_pos) + str(H3Numbering[x][2]) + ' '
									space_from_last_pos = 0
								elif len(str(H3Numbering[x][2])) == 2:
									rulerH3 += ' ' * (1 - space_from_last_pos) + str(H3Numbering[x][2])
									space_from_last_pos = 0
								else:
									rulerH3 += ' ' * (1 - space_from_last_pos) + str(H3Numbering[x][2])
									space_from_last_pos = 1
							else:
								rulerH3 += ' ' * (1 - space_from_last_pos) + '. '
								space_from_last_pos = 0
							if H3Numbering[x][4] == "A":
								rulerH3Color += '666'
							elif H3Numbering[x][4] == "B":
								rulerH3Color += '222'
							elif H3Numbering[x][4] == "C":
								rulerH3Color += '777'
							elif H3Numbering[x][4] == "D":
								rulerH3Color += '333'
							elif H3Numbering[x][4] == "E":
								rulerH3Color += 'CCC'
							elif H3Numbering[x][4] == "Stalk-MN":
								rulerH3Color += 'AAA'
							else:
								rulerH3Color += '000'
					if space_from_last_pos == 1:
						rulerH3Color += rulerH3Color[-1]
				elif self.ui.actionAA.isChecked() == True and self.ui.actionDNA.isChecked() == False:
					aa_start = i + 1
					aa_end = endSeg

					rulerH1 = 'H1numbering' + AASpaces[11:]
					rulerH1Color = '0' * len(rulerH1)
					rulerH3 = 'H3numbering' + AASpaces[11:]
					rulerH3Color = '0' * len(rulerH3)

					# make H1 numbering
					space_from_last_pos = 0
					for x in range(aa_start, aa_end + 1):
						if H1Numbering[x][2] == '-':
							if space_from_last_pos == 2:
								rulerH1Color += '0'
								space_from_last_pos = space_from_last_pos - 1
							elif space_from_last_pos == 1:
								rulerH1Color += '0'
								space_from_last_pos = space_from_last_pos - 1
							else:
								rulerH1 += '-'
								rulerH1Color += '0'
						else:
							if int(H1Numbering[x][2]) % 5 == 0:
								if len(str(H1Numbering[x][2])) == 1:
									rulerH1 += str(H1Numbering[x][2])
									space_from_last_pos = 0
								elif len(str(H1Numbering[x][2])) == 2:
									rulerH1 += str(H1Numbering[x][2])
									space_from_last_pos = 1
								else:
									rulerH1 += str(H1Numbering[x][2])
									space_from_last_pos = 2
							else:
								if space_from_last_pos == 2:
									space_from_last_pos = space_from_last_pos - 1
								elif space_from_last_pos == 1:
									space_from_last_pos = space_from_last_pos - 1
								else:
									rulerH1 += '.'

							if H1Numbering[x][4] == "Cb":
								rulerH1Color += '7'
							elif H1Numbering[x][4] == "Ca1":
								rulerH1Color += '2'
							elif H1Numbering[x][4] == "Ca2":
								rulerH1Color += '4'
							elif H1Numbering[x][4] == "Sa":
								rulerH1Color += '3'
							elif H1Numbering[x][4] == "Sb":
								rulerH1Color += '6'
							elif H1Numbering[x][4] == "Stalk-MN":
								rulerH1Color += 'A'
							else:
								rulerH1Color += '0'
					if space_from_last_pos == 2:
						#rulerH1Color += rulerH1Color[-1] * 2
						rulerH1Color += '00'
					elif space_from_last_pos == 1:
						#rulerH1Color += rulerH1Color[-1]
						rulerH1Color += '0'

					# make H3 numbering
					space_from_last_pos = 0
					for x in range(aa_start, aa_end + 1):
						if H3Numbering[x][2] == '-':
							if space_from_last_pos == 2:
								space_from_last_pos = space_from_last_pos - 1
								rulerH3Color += '0'
							elif space_from_last_pos == 1:
								space_from_last_pos = space_from_last_pos - 1
								rulerH3Color += '0'
							else:
								rulerH3 += '-'
								rulerH3Color += '0'
						else:
							if int(H3Numbering[x][2]) % 5 == 0:
								if len(str(H3Numbering[x][2])) == 1:
									rulerH3 += str(H3Numbering[x][2])
									space_from_last_pos = 0
								elif len(str(H3Numbering[x][2])) == 2:
									rulerH3 += str(H3Numbering[x][2])
									space_from_last_pos = 1
								else:
									rulerH3 += str(H3Numbering[x][2])
									space_from_last_pos = 2
							else:
								if space_from_last_pos == 2:
									space_from_last_pos = space_from_last_pos - 1
								elif space_from_last_pos == 1:
									space_from_last_pos = space_from_last_pos - 1
								else:
									rulerH3 += '.'

							if H3Numbering[x][4] == "A":
								rulerH3Color += '6'
							elif H3Numbering[x][4] == "B":
								rulerH3Color += '2'
							elif H3Numbering[x][4] == "C":
								rulerH3Color += '7'
							elif H3Numbering[x][4] == "D":
								rulerH3Color += '3'
							elif H3Numbering[x][4] == "E":
								rulerH3Color += 'C'
							elif H3Numbering[x][4] == "Stalk-MN":
								rulerH3Color += 'A'
							else:
								rulerH3Color += '0'
					if space_from_last_pos == 2:
						#rulerH3Color += rulerH1Color[-1] * 2
						rulerH3Color += '00'
					elif space_from_last_pos == 1:
						#rulerH3Color += rulerH1Color[-1]
						rulerH3Color += '0'

			for seq in all:
				SeqName = seq[0]
				DNASeq = seq[1]
				AASeq = seq[2]
				if DataIn == 'RF':
					AASeq2 = seq[3]
					AASeq3 = seq[4]

				NewAA = AASeq.replace(' ', '')
				if DataIn == 'RF':
					NewAA2 = AASeq2.replace(' ', '')
					NewAA3 = AASeq3.replace(' ', '')

				while len(SeqName) < longestName:
					SeqName += ' '
				# todo can build num line even add CDR if align relative to germline instead just number as end
				toSpace = len(str(maxLen))
				endLabel = str(endSeg)
				while len(endLabel) < toSpace:
					endLabel += ' '
				endLabel = '  ' + endLabel

				if self.ui.actionDNA.isChecked() == True:

					ConSegDNA = consensusDNA[i:endSeg]
					DNASeqSeg = DNASeq[i:endSeg]
					ConSegDNA = ConSegDNA.upper()
					DNASeqSeg = DNASeqSeg.upper()

					DNAArt = ''
					for n in range(0, len(ConSegDNA)):
						if DNASeqSeg[n] == ConSegDNA[n]:
							if DataIn == 'RF':
								DNAArt += '-'
							else:
								char = DNASeqSeg[n]
								char = char.upper()
								# DNAArt += char
								DNAArt += '-'
						else:
							if DataIn == 'RF':
								DNAArt += DNASeqSeg[n]
							else:
								char = DNASeqSeg[n]
								char = char.lower()
								DNAArt += char


					ConSegDNA = ConName + ConSegDNA + endLabel
					DNASeqSeg = SeqName + DNAArt + endLabel
					if self.ui.actionAA.isChecked() == True:
						AArt = ''
						ConSegAA = consensusAA[i:endSeg]
						if DataIn == 'RF': ConSegAA2 = AASeq2[i:endSeg]
						if DataIn == 'RF': ConSegAA3 = AASeq3[i:endSeg]

						AASeqSeg = AASeq[i:endSeg]

						for n in range(0, len(ConSegAA)):
							if AASeqSeg[n] == ConSegAA[n]:
								AArt += ' '
							else:
								AArt += AASeqSeg[n]

						AASeqSeg = AASpaces + AArt  # + endLabel
						if DataIn == 'RF':
							ConSegAA = AASpaces + 'RF1: ' + ConSegAA
						else:
							ConSegAA = AASpaces + ConSegAA

						if DataIn == 'RF':
							ConSegAA2 = AASpaces + 'RF2: ' +  ConSegAA2
							ConSegAA3 = AASpaces + 'RF3: ' + ConSegAA3

						if ConAdd == True:
							if self.ui.actionBA.isChecked() == True:
								alignmentText += '\n' + rulerAA
								ColorMap += '\n' + '0' * len(rulerAA)
								alignmentText += '\n' + rulerH1
								ColorMap += '\n' + rulerH1Color
								alignmentText += '\n' + rulerH3
								ColorMap += '\n' + rulerH3Color

							alignmentText += '\n' + ConSegAA + '\n'
							ColorMap += '\n' + '0' * len(ConSegAA) + '\n'
							if DataIn == 'RF':
								alignmentText += '\n' + ConSegAA2 + '\n'
								alignmentText += '\n' + ConSegAA3 + '\n'
								alignmentText += '     ' + ConSegDNA + '\n'
							else:
								if self.ui.actionBA.isChecked() == True:
									alignmentText += rulerNT + '\n'
									ColorMap += '0' * len(rulerNT) + '\n'

								alignmentText += ConSegDNA + '\n'
								ColorMap += '0' * len(ConSegDNA) + '\n'
							ConAdd = False
						if DataIn != 'RF':
							alignmentText += AASeqSeg + '\n'
							ColorMap += '0' * len(AASeqSeg) + '\n'
							alignmentText += DNASeqSeg + '\n'
							ColorMap += '0' * len(DNASeqSeg) + '\n'
					else:
						if ConAdd == True:
							if self.ui.actionBA.isChecked() == True:
								alignmentText += '\n' + rulerNT
								ColorMap += '0' * len(rulerNT)
							alignmentText += '\n' + ConSegDNA + '\n'
							ColorMap += '\n' + '0' * len(ConSegDNA) + '\n'
							ConAdd = False
						if DataIn != 'RF':
							alignmentText += DNASeqSeg + '\n'
							ColorMap += '0' * len(DNASeqSeg) + '\n'
				else:
					if self.ui.actionAA.isChecked() == True:
						AArt = ''
						ConSegAA = NewConAA[i:endSeg]
						AASeqSeg = NewAA[i:endSeg]

						for n in range(0, len(ConSegAA)):
							if AASeqSeg[n] == ConSegAA[n]:
								AArt += '-'
							else:
								AArt += AASeqSeg[n]

						AASeqSeg = SeqName + AArt + endLabel
						ConSegAA = ConName + ConSegAA
						if ConAdd == True:
							if self.ui.actionBA.isChecked() == True:
								alignmentText += '\n' + 'Position(AA)' + rulerNT[12:]
								ColorMap += '\n' + '0' * len(rulerNT)
								alignmentText += '\n' + rulerH1
								ColorMap += '\n' + rulerH1Color
								alignmentText += '\n' + rulerH3
								ColorMap += '\n' + rulerH3Color
							alignmentText += '\n' + ConSegAA + '\n'
							ColorMap += '\n' + '0' * len(ConSegAA) + '\n'
							ConAdd = False
						alignmentText += AASeqSeg + '\n'
						ColorMap += '0' * len(AASeqSeg) + '\n'

			i += 60
			ConAdd = True
			alignmentText += '\n'
			ColorMap += '\n'

		Style = 'aligned'

		# legend text and color
		legend_text = 'H1 Antigenic Sites:  Ca1    Ca2    Cb    Sa    Sb   Stalk-MN \n' + \
		              'H3 Antigenic Sites:  A    B    C    D    E   Stalk-MN \n'
		legend_color = '000000000000000000022222224444444777777333333666666AAAAAAAAAA\n' + \
		               '000000000000000000066666222227777733333CCCCCAAAAAAAAAA\n'
		if Notes != 'Tab':
			#window_id = int(time.time() * 100)
			#text_edit = VGenesTextMain()
			#text_edit.id = window_id
			#text_edit.vGeneSignal.connect(self.testXXXX)
			#text_edit.show()

			window_id = int(time.time() * 100)
			VGenesTextWindows[window_id] = VGenesTextMain()
			VGenesTextWindows[window_id].id = window_id
			VGenesTextWindows[window_id].data = DataIn
			VGenesTextWindows[window_id].note = Notes
			VGenesTextWindows[window_id].type = 'Alignment'
			VGenesTextWindows[window_id].dnaAct.setChecked(self.ui.actionDNA.isChecked())
			VGenesTextWindows[window_id].aaAct.setChecked(self.ui.actionAA.isChecked())
			VGenesTextWindows[window_id].baAct.setChecked(self.ui.actionBA.isChecked())

			self.ShowVGenesTextEdit(alignmentText, Style, ColorMap, window_id)
			self.ShowVGenesTextEditLegend(legend_text, legend_color, window_id)
		else:
			self.ui.txtSeqAlignment.setText(alignmentText)

		QApplication.restoreOverrideCursor()

	def MakeRuler(self, pos1, pos2, step, mode):
		ErrMsg = ""
		if len(str(pos2)) > step - 1:
			ErrMsg = "Please use larger step! Current step is too short!"

		# start to make ruler
		if mode == "aa":
			step_count = int(pos2) - int(pos1) + 1
			ruler = ' . ' * step_count

			for x in range(100):
				cur_pos = pos1 + x * step
				if cur_pos <= pos2:
					ruler = ruler[:x * 3 * step + 1] + str(cur_pos) + ruler[len(str(cur_pos)) + x * 3 * step + 1:]

		else:
			ruler = ''
			cur_pos = pos1
			step_count = 0
			space_left = 0
			while cur_pos <= pos2:
				if cur_pos == pos1 + step_count * step:
					ruler += str(cur_pos)
					space_left = len(str(cur_pos)) - 1
					cur_pos += 1
					step_count += 1
				else:
					if space_left > 0:
						space_left = space_left - 1
						cur_pos += 1
					else:
						ruler += '.'
						cur_pos += 1
		return ruler

	@pyqtSlot()
	def AlignSequencesRF(self, DataIn, Notes):
		# import tempfile
		import os
		TupData = ()
		DataSet = []
		QApplication.setOverrideCursor(Qt.WaitCursor)
		global GLMsg
		global working_prefix
		global clustal_path
		global temp_folder
		global VGenesTextWindows


		if DataIn == 'RF':  #can use this part for reading frames
			fields = ['SeqName', 'Sequence']
			# checkedProjects, checkedGroups, checkedSubGroups, checkedkids = getTreeChecked()
			# SQLStatement = LibratorSQL.MakeSQLStatement(self, fields, data[0])
			#
			#
			# DataIs = VGenesSQL.RunSQL(DBFilename, SQLStatement)  # returns list of tuples where seqname is first

			# SeqName = self.ui.txtName.toPlainText()
			SeqName = 'Current'
			DNASeq = self.ui.textSeq.toPlainText()
			# GermSeq = DNASeq
			TupData  = (SeqName, DNASeq)

			DataSet.append(TupData)


			global GLMsg
			if len(DataSet) == 1:
				GLMsg = False
				self.ui.actionBA.setChecked(True)
				self.ui.actionAA.setChecked(True)
				GLMsg = True
				GermSeq = DNASeq
				Germline = ('Germline', GermSeq)
				DataSet.append(Germline)
			else:
				if self.ui.actionBA.isChecked() == True:
					GLMsg = True
					GermSeq = DNASeq
					Germline = ('Germline', GermSeq)
					DataSet.append(Germline)

		elif DataIn == 'edit':
			DataIn = 'none'
			# DataIs = []

			# SeqName = data[0]

			# DNAseq = self.ui.txtDNASeq.toPlainText()
			# Sequence = (SeqName, DNAseq)
			# DataSet.append(Sequence)


			if len(DataSet) == 1:
				GLMsg = False
				self.ui.actionBA.setChecked(True)
				self.ui.actionAA.setChecked(True)
				GLMsg = True
				GermSeq = self.ui.textSeq.toPlainText()
				Germline = ('Germline', GermSeq)
				DataSet.append(Germline)

		else:
			self.ui.actionBA.setChecked(False)
			DataSet = DataIn

		# import subprocess

		#(fd, outfilename) = tempfile.mkstemp()
		outfilename = ''
		try:
			if os.path.exists(clustal_path):
				outfilename = LibratorSeq.ClustalO(DataSet, 80, True, temp_folder, clustal_path)
			else:
				QMessageBox.warning(self, 'Warning',
				                    'The Clustal Omega does not exist! Check your path!', QMessageBox.Ok,
				                    QMessageBox.Ok)
				return

			lenName = 0
			longestName = 0
			alignmentText = ''
			germseq = ''
			germpeptide = ''

			each = ()
			all = []
			if self.ui.actionBA.isChecked() == False:
				# each.append('Consensus: ')
				longestName = 11
			else:
				# each.append('Germline: ')
				longestName = 10

			# each.append('') #DNA
			# each.append('') #AA
			peptide = ''
			SeqName = ''
			StartAll = False
			if os.path.isfile(outfilename):
				with open(outfilename, 'r') as currentfile:
					for line in currentfile:
						Readline = line.replace('\n', '').replace('\r', '').replace('-', '.')
						Readline = Readline.strip()
						if Readline[0] == '>':
							if StartAll == True:
								all.append(each)
							StartAll = True
							# each.clear()
							SeqName = Readline[1:] + ':'
							lenName = len(SeqName)
							if lenName > longestName:
								longestName = lenName + 2

						# if SeqName != 'Germline':
						#     each.append(SeqName)

						else:

							if self.ui.actionAA.isChecked() == True:
								AASeq, ErMessage = LibratorSeq.Translator(Readline, 0)


								#Position, Amino Acid, H1-segment (HA1 or HA2), H1Number, A/California/4/2009-residue, H1-antigenic-region


								if DataIn == 'RF':AASeq2, ErMessage = LibratorSeq.Translator(Readline, 1)
								if DataIn == 'RF':AASeq3, ErMessage = LibratorSeq.Translator(Readline, 2)
								peptide = ''
								if DataIn == 'RF':peptide2 = ''
								if DataIn == 'RF':peptide3 = ''

								for res in AASeq:
									peptide += (' ' + res + ' ')

								if DataIn == 'RF':
									for res in AASeq2:
										peptide2 += (' ' + res + ' ')
								if DataIn == 'RF':
									for res in AASeq3:
										peptide3 += (' ' + res + ' ')

								# peptide2 = ' ' + peptide2
								# peptide3 = '  ' + peptide3
							peptide = peptide[0:len(Readline)]

							if DataIn == 'RF': peptide = peptide[1:]

							if DataIn == 'RF': peptide2 = peptide2[0:len(Readline)]

							if DataIn == 'RF': peptide3 = peptide3[0:len(Readline)]
							if DataIn == 'RF': peptide3 = ' ' + peptide3



							if SeqName != 'Germline:':
								if DataIn == 'RF':
									each = (SeqName, Readline, peptide, peptide2, peptide3)
								else:
									each = (SeqName, Readline, peptide)
							# each.append(Readline)
							# each.append(peptide)
							else:
								germseq = Readline
								germpeptide = peptide
								StartAll = False
				if StartAll == True:
					all.append(each)
			else:
				return
		# todo add header that says what germline based on
		except:
			print('no')

		finally:
			os.remove(outfilename)

		if self.ui.actionBA.isChecked() == True:
			consensusDNA = germseq
			consensusAA = germpeptide

		else:
			firstOne = all[1]
			seqlen = len(firstOne[1])
			if self.ui.actionDNA.isChecked() == True:
				consensusDNA = ''
				tester = ''
				# testl = []
				for i in range(0, seqlen - 1):
					tester = ''
					Cnuc = ''
					for item in all:
						seq = item[1]
						tester += seq[i]

					frequencies = [(c, tester.count(c)) for c in set(tester)]
					Cnuc = max(frequencies, key=lambda x: x[1])[0]
					consensusDNA += Cnuc

			if self.ui.actionAA.isChecked() == True:
				consensusAA = ''
				tester = ''
				firstOne = all[1]
				seqlen = len(firstOne[1])
				# testl = []
				for i in range(0, seqlen - 1):
					tester = ''
					Caa = ''
					for item in all:
						seq = item[2]
						tester += seq[i]

					frequencies = [(c, tester.count(c)) for c in set(tester)]
					Caa = max(frequencies, key=lambda x: x[1])[0]
					consensusAA += Caa

			# need build numbering lines also
			# first record is germline or consensus whatever used and empty seq and AA
			# need to use ones produced above
			# also longestName is longest and need code to ensure all that long with ': '
			# build alignment with name and 50 per

		header = 'VGenes multiple alignment using Clustal Omega. \n'
		RFSeqName = self.ui.txtName.toPlainText()
		if self.ui.actionBA.isChecked() == False:
			ConName = 'Consensus: '

		else:
			ConName = 'Germline: '
			if DataIn != 'RF':
				header += 'Alignment relative to the predicted germline gene for ' + SeqName + '.\n'
			else:
				header += 'Reading frames of '+ RFSeqName + '.\n'

		if DataIn == 'RF': ConName = 'Sequence: '

		while len(ConName) < longestName:
			ConName += ' '

		AASpaces = ''
		while len(AASpaces) < longestName:
			AASpaces += ' '

		if self.ui.actionDNA.isChecked() == False and self.ui.actionAA.isChecked() == False:
			self.ui.actionDNA.setChecked(True)

		alignmentText = header
		i = 0
		endSeg = 0
		done = False
		ConAdd = True

		# for j in range[0,longestName]:
		#     AASpaces += ' '
		if self.ui.actionDNA.isChecked() == True:
			maxLen = len(consensusDNA)
		else:
			NewConAA = consensusAA.replace(' ', '')

			# canAA = False
			maxLen = len(NewConAA)

		# canAA = True
		while endSeg <= maxLen - 1:
			if i + 60 < maxLen:
				# if i == 0:
				#     endSeg = 49
				# else:
				endSeg = i + 60
			else:
				endSeg = maxLen

			for seq in all:
				SeqName = seq[0]
				DNASeq = seq[1]
				AASeq = seq[2]
				if DataIn == 'RF':AASeq2 = seq[3]
				if DataIn == 'RF':AASeq3 = seq[4]

				NewAA = AASeq.replace(' ', '')
				if DataIn == 'RF':NewAA2 = AASeq2.replace(' ', '')
				if DataIn == 'RF':NewAA3 = AASeq3.replace(' ', '')

				while len(SeqName) < longestName:
					SeqName += ' '
				# todo can build num line even add CDR if align relative to germline instead just number as end
				toSpace = len(str(maxLen))
				endLabel = str(endSeg)
				while len(endLabel) < toSpace:
					endLabel += ' '
				endLabel = '  ' + endLabel

				if self.ui.actionDNA.isChecked() == True:

					ConSegDNA = consensusDNA[i:endSeg]
					DNASeqSeg = DNASeq[i:endSeg]
					ConSegDNA = ConSegDNA.upper()
					DNASeqSeg = DNASeqSeg.upper()

					DNAArt = ''
					for n in range(0, len(ConSegDNA)):
						if DNASeqSeg[n] == ConSegDNA[n]:
							if DataIn == 'RF':
								DNAArt += '-'
							else:
								char = DNASeqSeg[n]
								char = char.upper()
								# DNAArt += char
								DNAArt += '-'
						else:
							if DataIn == 'RF':
								DNAArt += DNASeqSeg[n]
							else:
								char = DNASeqSeg[n]
								char = char.lower()
								DNAArt += char


					ConSegDNA = ConName + ConSegDNA + endLabel
					DNASeqSeg = SeqName + DNAArt + endLabel
					if self.ui.actionAA.isChecked() == True:
						AArt = ''
						ConSegAA = consensusAA[i:endSeg]
						if DataIn == 'RF': ConSegAA2 = AASeq2[i:endSeg]
						if DataIn == 'RF': ConSegAA3 = AASeq3[i:endSeg]

						AASeqSeg = AASeq[i:endSeg]

						for n in range(0, len(ConSegAA)):
							if AASeqSeg[n] == ConSegAA[n]:
								AArt += ' '
							else:
								AArt += AASeqSeg[n]

						AASeqSeg = AASpaces + AArt  # + endLabel
						if DataIn == 'RF':
							ConSegAA = AASpaces + 'RF1: ' + ConSegAA
						else:
							ConSegAA = AASpaces + ConSegAA


						if DataIn == 'RF': ConSegAA2 = AASpaces + 'RF2: ' +  ConSegAA2
						if DataIn == 'RF': ConSegAA3 = AASpaces + 'RF3: ' +  ConSegAA3

						if ConAdd == True:
							alignmentText += '\n' + ConSegAA + '\n'
							if DataIn == 'RF': alignmentText += '\n' + ConSegAA2 + '\n'
							if DataIn == 'RF': alignmentText += '\n' + ConSegAA3 + '\n'

							if DataIn == 'RF':
								alignmentText += '     ' + ConSegDNA + '\n'
							else:
								alignmentText += ConSegDNA + '\n'
							ConAdd = False
						if DataIn != 'RF': alignmentText += AASeqSeg + '\n'
						if DataIn != 'RF': alignmentText += DNASeqSeg + '\n'
					else:
						if ConAdd == True:
							alignmentText += '\n' + ConSegDNA + '\n'
							ConAdd = False
						if DataIn != 'RF': alignmentText += DNASeqSeg + '\n'

				else:
					if self.ui.actionAA.isChecked() == True:
						AArt = ''
						ConSegAA = NewConAA[i:endSeg]
						AASeqSeg = NewAA[i:endSeg]

						for n in range(0, len(ConSegAA)):
							if AASeqSeg[n] == ConSegAA[n]:
								AArt += '-'
							else:
								AArt += AASeqSeg[n]

						AASeqSeg = SeqName + AArt + endLabel
						ConSegAA = ConName + ConSegAA
						if ConAdd == True:
							alignmentText += '\n' + ConSegAA + '\n'

							ConAdd = False
						alignmentText += AASeqSeg + '\n'

			i += 60
			ConAdd = True
			alignmentText += '\n'

		Style = 'aligned'

		if Notes != 'Tab':
			ColorMap = 'none'

			window_id = int(time.time() * 100)
			VGenesTextWindows[window_id] = VGenesTextMain()
			VGenesTextWindows[window_id].id = window_id
			VGenesTextWindows[window_id].data = DataIn
			VGenesTextWindows[window_id].note = Notes
			VGenesTextWindows[window_id].type = 'RF'
			VGenesTextWindows[window_id].dnaAct.setChecked(False)
			VGenesTextWindows[window_id].aaAct.setChecked(False)
			VGenesTextWindows[window_id].baAct.setChecked(False)

			self.ShowVGenesTextEdit(alignmentText, Style, ColorMap, window_id)
		else:
			self.ui.txtSeqAlignment.setText(alignmentText)

		QApplication.restoreOverrideCursor()

	@pyqtSlot()
	def on_action_Save_triggered(self):
		# SeqName, Sequence, SeqLen, SubType, Form, VFrom, VTo, Active, Role, Donor, Mutations, ID
		if DBFilename == 'none':
			QMessageBox.warning(self, 'Warning', 'No Librator database determined!', QMessageBox.Ok, QMessageBox.Ok)
			return
		listSaves = []

		SeqName = self.ui.txtName.toPlainText()


		SubType = self.ui.cboSubtype.currentText()
		SubTypeT = (SubType, 'SubType')

		Form = self.ui.cboForm.currentText()
		FormT = (Form, 'Form')

		VFrom = str(self.ui.spnFrom.value())
		VFromT = (VFrom, 'VFrom')

		VTo = str(self.ui.spnTo.value())
		VToT = (VTo, 'VTo')


		self.ui.spnFrom.setValue(0)
		self.ui.spnTo.setValue(5000)

		Sequence = self.ui.textSeq.toPlainText()
		SequenceT = (Sequence, 'Sequence')

		SeqLen = str(len(Sequence))
		SeqLenT = (SeqLen, 'SeqLen')

		self.ui.spnFrom.setValue(int(VFrom))
		self.ui.spnTo.setValue(int(VTo))



		Role = self.ui.cboRole.currentText()
		RoleT = (Role, 'Role')

		Donor = self.ui.txtDonorRegions.toPlainText()
		DonorT = (Donor, 'Donor')

		Mutations = self.ui.txtInsert_Base.toPlainText()
		MutationsT = (Mutations, 'Mutations')



		listSaves.append(SequenceT)
		listSaves.append(SeqLenT)
		listSaves.append(SubTypeT)
		listSaves.append(FormT)
		listSaves.append(VFromT)
		listSaves.append(VToT)
		listSaves.append(RoleT)
		listSaves.append(DonorT)
		listSaves.append(MutationsT)


		for item in listSaves:

			self.UpdateSeq(SeqName, item[0], item[1])

	@pyqtSlot()
	def FormChanged(self):
		global MoveNotChange
		if MoveNotChange:
			return
		selections = self.ui.listWidgetStrainsIn.selectedItems()
		name_selections = []
		for item in selections:
			name_selections.append(item.text())
		CurrVal = self.ui.cboForm.currentText()

		question = 'You will change Form information to: ' + CurrVal + '\nfor the following sequences:\n\n'
		question += '\n'.join(name_selections)
		question += '\n\nAre you sure?'
		buttons = 'YN'
		answer = questionMessage(self, question, buttons)
		if answer == 'Yes':
			for seq in name_selections:
				self.UpdateSeq(seq, CurrVal, 'Form')
				self.ui.cboForm.last_value = CurrVal
		else:
			MoveNotChange = True
			self.ui.cboForm.setCurrentText(self.ui.cboForm.last_value)
			MoveNotChange = False
			return
		self.rebuildTree()

	@pyqtSlot()
	def SubTypeChanged(self):
		global MoveNotChange
		if MoveNotChange:
			return
		selections = self.ui.listWidgetStrainsIn.selectedItems()
		name_selections = []
		for item in selections:
			name_selections.append(item.text())
		CurrVal = self.ui.cboSubtype.currentText()

		question = 'You will change SubType information to: ' + CurrVal + '\nfor the following sequences:\n\n'
		question += '\n'.join(name_selections)
		question += '\n\nAre you sure?'
		buttons = 'YN'
		answer = questionMessage(self, question, buttons)
		if answer == 'Yes':
			for seq in name_selections:
				self.UpdateSeq(seq, CurrVal, 'SubType')
				self.ui.cboSubtype.last_value = CurrVal
		else:
			MoveNotChange = True
			self.ui.cboSubtype.setCurrentText(self.ui.cboSubtype.last_value)
			MoveNotChange = False
			return

		self.rebuildTree()

	@pyqtSlot()
	def RoleChanged(self):
		global BaseSeq
		global MoveNotChange
		if MoveNotChange:
			return

		selections = self.ui.listWidgetStrainsIn.selectedItems()
		name_selections = []
		for item in selections:
			name_selections.append(item.text())
		CurrVal = self.ui.cboRole.currentText()
		CurName = self.ui.txtName.toPlainText()
		if CurrVal == 'BaseSeq':
			if len(name_selections) > 1:
				Msg = 'You can not set multiple sequences as Base Sequence because it is unique!!'
				QMessageBox.warning(self, 'Warning', Msg, QMessageBox.Ok, QMessageBox.Ok)
				return
			if BaseSeq != CurName and BaseSeq != '':
				question = BaseSeq + ':\n\n is already denoted as the Base sequence and there can only be one.\n' \
				                     ' Reassign the Base sequence to:\n\n' + CurName + '?'
				buttons = 'YN'
				answer = questionMessage(self, question, buttons)
				if answer == 'Yes':
					self.UpdateSeq(BaseSeq, 'Unassigned', 'Role')
					BaseSeq = CurName
					self.UpdateSeq(BaseSeq, 'BaseSeq', 'Role')
					self.ui.lblBaseName.setText(BaseSeq)
					self.ui.cboRole.last_value = BaseSeq
				else:
					MoveNotChange = True
					self.ui.cboRole.setCurrentText(self.ui.cboRole.last_value)
					MoveNotChange = False
					return
			else:
				BaseSeq = CurName
				self.UpdateSeq(BaseSeq, 'BaseSeq', 'Role')
				self.ui.lblBaseName.setText(BaseSeq)
		# self.ui.cboRole.setEnabled(False)
		else:
			question = 'You will change Role information to: ' + CurrVal + '\nfor the following sequences:\n\n'
			question += '\n'.join(name_selections)
			question += '\n\nAre you sure?'
			buttons = 'YN'
			answer = questionMessage(self, question, buttons)
			if answer == 'Yes':
				for seq in name_selections:
					self.UpdateSeq(seq, CurrVal, 'Role')
					self.ui.cboRole.last_value = self.ui.cboRole.currentText()
			else:
				MoveNotChange = True
				self.ui.cboRole.setCurrentText(self.ui.cboRole.last_value)
				MoveNotChange = False
				return
		self.rebuildTree()

	@pyqtSlot()
	def SetActive(self,IsActive):

		CurName = self.ui.txtName.toPlainText()
		if IsActive == True:
			CurrVal = True
		elif IsActive == False:
			CurrVal = False

		self.UpdateSeq(CurName, CurrVal, 'Active')

	@pyqtSlot()
	def SeqFrom(self):
		CurName = self.ui.txtName.toPlainText()
		CurrVal = self.ui.spnFrom.value()



		self.UpdateSeq(CurName, str(CurrVal), 'VFrom')

		self.ListItemChanged()

	@pyqtSlot()
	def SeqTo(self):
		CurName = self.ui.txtName.toPlainText()
		CurrVal = self.ui.spnTo.value()


		self.UpdateSeq(CurName, str(CurrVal), 'VTo')
		self.ListItemChanged()

	@pyqtSlot()
	def SeqChanged(self):
		global MoveNotChange
		if MoveNotChange == False:
			CurName = self.ui.txtName.toPlainText()

			VFrom = str(self.ui.spnFrom.value())

			VTo = str(self.ui.spnTo.value())


			self.ui.spnFrom.setValue(1)
			self.ui.spnTo.setValue(5000)

			Sequence = self.ui.textSeq.toPlainText()

			SeqLen = str(len(Sequence))

			# MoveNotChange = True
			self.ui.spnFrom.setValue(int(VFrom))
			self.ui.spnTo.setValue(int(VTo))


			self.UpdateSeq(CurName, Sequence, 'Sequence')
			self.UpdateSeq(CurName, SeqLen, 'SeqLen')
			MoveNotChange = False

	@pyqtSlot()
	def UpdateSequences(self):
		global DataIs
		for item in DataIs:
			FromV = int(item[5])-1
			if FromV == -1: FromV = 0
			ToV = int(item[6])-1

			HASeq = item[1]
			HASeq = HASeq[FromV:ToV]

			HAAA = Translator(HASeq.upper(), 0)
			self.ui.textSeq.setPlainText(HASeq.upper())
			self.ui.textSeq.repaint()
			self.ui.textAA.setPlainText(HAAA[0])

	@pyqtSlot()
	def DonorRegions(self):
		global SeqMove
		if SeqMove == False:
			CurName = self.ui.txtName.toPlainText()
			CurrVal = self.ui.txtDonorRegions.toPlainText()

			self.UpdateSeq(CurName, CurrVal, 'Donor')
		SeqMove = False

	@pyqtSlot()
	def DonorRegionsDialog(self):
		if self.ui.txtName.toPlainText() == "":
			QMessageBox.warning(self, 'Warning', 'Please select a sequence first!', QMessageBox.Ok, QMessageBox.Ok)
		else:
			CurName = self.ui.txtName.toPlainText()
			#CurrVal = self.ui.txtDonorRegions.toPlainText()

			text_start, ok1 = QInputDialog.getText(self, 'Input Dialog',
											'Enter start of Donor region:')
			if ok1:
				text_end, ok2 = QInputDialog.getText(self, 'Input Dialog',
											'Enter end of Donor region:')
			if ok1 and ok2:
				if text_start == "":
					text_start = '1'
				if text_end == "":
					text_end = "999"
				if int(text_start) >= int(text_end):
					QMessageBox.warning(self, 'Warning', 'Region start position should be smaller than end position!', QMessageBox.Ok, 
						QMessageBox.Ok)
				else:
					CurrVal = text_start + "-" + text_end
					self.UpdateSeq(CurName, CurrVal, 'Donor')
					self.ui.txtDonorRegions.setText(CurrVal)

	@pyqtSlot()
	def EditSeqName(self):
		global DataIs
		global SeqMove

		if SeqMove == False:
			for item in DataIs:

				CurName = item[0]
			listRow = self.ui.listWidgetStrainsIn.currentRow()
			message = 'Edit name for ' + CurName + '?'
			CurrVal = setText(self, message, CurName)

			# CurrVal = self.ui.txtInsert_Base.toPlainText()

			if CurrVal != "Cancelled Action":
				self.UpdateSeq(CurName, CurrVal, 'SeqName')
				self.ui.listWidgetStrainsIn.takeItem(listRow)

				self.ui.listWidgetStrainsIn.addItem(CurrVal)

				# self.UpdateSeq(eachItemIs, 'True', 'Active')
			self.UpdateFields()
		SeqMove = False
		self.rebuildTree()

	@pyqtSlot()
	def Mutations(self):

		global SeqMove
		if SeqMove == False:
			CurName = self.ui.txtName.toPlainText()
			CurrVal = self.ui.txtInsert_Base.toPlainText()

			self.UpdateSeq(CurName, CurrVal, 'Mutations')
		SeqMove = False

	@pyqtSlot()
	def MutationsDialog(self):
		if self.ui.txtName.toPlainText() == "":
			QMessageBox.warning(self, 'Warning', 'Please select a sequence first!', QMessageBox.Ok, QMessageBox.Ok)
		else:
			QMessageBox.warning(self, 'Warning', 'Modifying Mutation info is prohibited! \nIf you '
											 'believe the information is wrong, \nplease re-generate'
											 ' new sequence with correct mutation!', QMessageBox.Ok, QMessageBox.Ok)

	@pyqtSlot()
	def UpdateSeq(self, ID, ItemValue, FieldName):
		global DBFilename
		# ID = item[0]
		UpdateField(ID, ItemValue, FieldName, DBFilename)

	@pyqtSlot()
	def ShowVGenesTextEdit(self, textToShow, style, ColorMap, window_id):
		global VGenesTextWindows

		# delete close window objects
		del_list = []
		for id, obj in VGenesTextWindows.items():
			if id != window_id:
				if obj.isVisible() == False:
					del_list.append(id)

		for id in del_list:
			del_obj = VGenesTextWindows.pop(id)

		#a = VGenesTextWindows

		if style == 'aligned':
			FontIs = VGenesTextWindows[window_id].textEdit.currentFont()
			font = QFont(FontIs)

			# FontSize = int(font.pointSize())
			font.setPointSize(16)
			font.setFamily('Courier New')

			VGenesTextWindows[window_id].textEdit.setFont(font)

		elif style == 'standard':
			FontIs = VGenesTextWindows[window_id].textEdit.currentFont()
			font = QFont(FontIs)

			# FontSize = int(font.pointSize())
			font.setPointSize(16)
			font.setFamily('Lucida Grande')

			VGenesTextWindows[window_id].textEdit.setFont(font)

		elif style == 'ProteinReport':
			FontIs = VGenesTextWindows[window_id].textEdit.currentFont()
			font = QFont(FontIs)

			# FontSize = int(font.pointSize())
			font.setPointSize(6)
			font.setFamily('Courier New')

			VGenesTextWindows[window_id].textEdit.setFont(font)

		VGenesTextWindows[window_id].show()

		VGenesTextWindows[window_id].textEdit.setText(textToShow)
		if ColorMap != 'none':
			cursor = VGenesTextWindows[window_id].textEdit.textCursor()

			# test running time
			#start = time.time()
			self.DecorateText(ColorMap, cursor)
			#end = time.time()
			#print('Running time for new function' + str(end - start) + '\n')

			#start = time.time()
			#self.DecorateTextOld(ColorMap, cursor)
			#end = time.time()
			#print('Running time for old function' + str(end - start) + '\n')

	@pyqtSlot()
	def ShowVGenesTextEditLegend(self, textToShow, ColorMap, window_id):
		global VGenesTextWindows
		FontIs = VGenesTextWindows[window_id].textEdit_legend.currentFont()
		font = QFont(FontIs)

		# FontSize = int(font.pointSize())
		font.setPointSize(20)
		font.setFamily('Courier New')

		VGenesTextWindows[window_id].textEdit_legend.setFont(font)

		VGenesTextWindows[window_id].show()

		VGenesTextWindows[window_id].textEdit_legend.setText(textToShow)
		cursor = VGenesTextWindows[window_id].textEdit_legend.textCursor()
		self.DecorateText(ColorMap, cursor)

	@pyqtSlot()
	def on_action_Help_triggered(self):
		Msg = 'Librator was developed and supported by Wilson Lab. Please refer to http://Wilsonlab.uchicago.edu ' \
		      'for more information'
		QMessageBox.information(self, 'information', Msg, QMessageBox.Ok,
		                        QMessageBox.Ok)

	@pyqtSlot()
	def on_actionPreferences_triggered(self):
		self.open_basepath_dialog()

	@pyqtSlot()
	def on_actionMutation_triggered(self):
		self.open_mutation_dialog()

	@pyqtSlot()
	def on_actionEditing_triggered(self):
		self.sequence_editing()

	@pyqtSlot()
	def on_actionEditing_triggered(self):
		self.sequence_editing()

	@pyqtSlot()
	def on_actionFusion_triggered(self):
		self.open_fusion_dialog()

	@pyqtSlot()
	def on_actionPyMOL_triggered(self):
		global pymol_path, working_prefix

		seq = self.ui.txtName.toPlainText()
		if seq == '':
			QMessageBox.warning(self, 'Warning',
			                    'Please select a sequence first!', QMessageBox.Ok, QMessageBox.Ok)
			return
		mutation = self.ui.txtInsert_Base.toPlainText().strip(",")
		subtype = str(self.ui.cboSubtype.currentText())

		# set 3D templates for different subtypes
		if subtype in Group1:
			pdb_path = os.path.join(working_prefix, '..', 'Resources', 'PDB', '4jtv.pdb')
		elif subtype in Group2:
			pdb_path = os.path.join(working_prefix, '..', 'Resources', 'PDB', '4hmg.pdb')
		elif subtype in GroupNA:
			pdb_path = os.path.join(working_prefix, '..', 'Resources', 'PDB', '3hto.pdb')
		elif subtype == "B":
			pdb_path = os.path.join(working_prefix, '..', 'Resources', 'PDB', '3hto.pdb')
		else:
			pdb_path = os.path.join(working_prefix, '..', 'Resources', 'PDB', '3hto.pdb')

		self.show3Dstructure(mutation, pdb_path, pymol_path, subtype)

	@pyqtSlot()
	def on_actionGibsonClone_triggered(self):
		self.open_gibson_dialog()

	@pyqtSlot()
	def on_action_Open_triggered(self):  # how to activate menu and toolbar actions!!!
		#need to simply get database name and populate list views
		global DBFilename
		global DataIs
		global BaseSeq

		DBFilename = openFile(self, 'ldb')
		if DBFilename == None or DBFilename == 'none':
			return
		self.open_db(DBFilename)

	def open_db(self, infile):  # how to activate menu and toolbar actions!!!
		#need to simply get database name and populate list views
		global DBFilename
		global DataIs
		global BaseSeq

		DBFilename = infile

		# check if this is the right DB
		SQLStatement = 'SELECT * FROM LibDB ORDER BY SeqName DESC LIMIT 1 '
		try:
			DataIn = RunSQL(DBFilename, SQLStatement)
		except:
			QMessageBox.warning(self, 'Warning', 'There is no LibDB table in the selected database!',
			                    QMessageBox.Ok,
			                    QMessageBox.Ok)
			return

		if isinstance(DBFilename, str):
			titletext = 'Librator - ' + DBFilename
			self.setWindowTitle(titletext)
			# self.ui.listWidgetStrainsIn.setCurrentRow(0)
			self.PopulateCombos()
			self.UpdateRecentFilelist(DBFilename)

			# refresh the list - active sequence list
			self.ui.listWidgetStrainsIn.clear()
			SQLStatement = 'SELECT `SeqName` FROM LibDB WHERE Active = "True"'
			records = RunSQL(DBFilename, SQLStatement)
			new_records = []
			for x in records:
				new_records.append(x[0])
			self.ui.listWidgetStrainsIn.addItems(new_records)

			# check if the database have base sequence
			SQLStatement = 'SELECT * FROM LibDB WHERE `Role` = "BaseSeq"'
			data_fetch = RunSQL(DBFilename, SQLStatement)

			if len(data_fetch) == 1:
				CurName = data_fetch[0][0]
				BaseSeq = CurName
				self.ui.lblBaseName.setText(CurName)
			elif len(data_fetch) > 1:
				QMessageBox.warning(self, 'Warning', 'Your database have multiple base sequences! Will choose the first one as current base sequence',
									QMessageBox.Ok, QMessageBox.Ok)
				CurName = data_fetch[0][0]
				BaseSeq = CurName
				self.ui.lblBaseName.setText(CurName)
			else:
				BaseSeq = ''
				self.ui.lblBaseName.setText('Sequence Name')

			self.rebuildTree()

	def rebuildTree(self):
		global DBFilename

		if DBFilename == 'none':
			return

		# clear tree
		self.ui.treeWidget.clear()

		orderBy = self.ui.groupCombo.currentText()
		self.ui.treeWidget.setColumnCount(1)
		self.ui.treeWidget.setHeaderHidden(True)
		root = QtWidgets.QTreeWidgetItem(self.ui.treeWidget)
		root.setText(0, 'All Sequences')
		
		# set up base seq
		SQLStatement = 'SELECT `SeqName`,`SubType`,`Active`,`Role`,`Form` FROM LibDB WHERE `Role` = "BaseSeq"'
		data_fetch = RunSQL(DBFilename, SQLStatement)
		if len(data_fetch) > 0:
			subtype = data_fetch[0][1]
			cur_name = data_fetch[0][0]
			base_node = QtWidgets.QTreeWidgetItem(root)
			base_node.setText(0, 'Base Sequence')
			base_node.setFlags(base_node.flags() | Qt.ItemIsUserCheckable)

			cur_node = QtWidgets.QTreeWidgetItem(base_node)
			cur_node.setText(0, cur_name)
			seq_icon = QtGui.QIcon()
			if subtype[0] == 'H':
				seq_icon.addPixmap(QtGui.QPixmap(":/PNG-Icons/HA.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			elif subtype[0] == 'N':
				seq_icon.addPixmap(QtGui.QPixmap(":/PNG-Icons/NA.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			else:
				seq_icon.addPixmap(QtGui.QPixmap(":/PNG-Icons/Seq.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			cur_node.setIcon(0, seq_icon)
			cur_node.setFlags(cur_node.flags() | Qt.ItemIsUserCheckable)
			if data_fetch[0][2] == 'True':
				cur_node.setCheckState(0, Qt.Checked)
				base_node.setCheckState(0, Qt.Checked)
			else:
				cur_node.setCheckState(0, Qt.Unchecked)
				base_node.setCheckState(0, Qt.Unchecked)

		# list all sequences by specific group factor
		if orderBy == 'SubType':
			SQLStatement = 'SELECT `SeqName`,`SubType`,`Active`,`Role`,`Form` FROM LibDB WHERE `Role` <> "BaseSeq" ORDER BY `SubType` ASC'
			records = RunSQL(DBFilename, SQLStatement)
			subtype_index = 1
			group_index = 1
		elif orderBy == 'Role':
			SQLStatement = 'SELECT `SeqName`,`SubType`,`Active`,`Role`,`Form` FROM LibDB WHERE `Role` <> "BaseSeq" ORDER BY `Role` ASC'
			records = RunSQL(DBFilename, SQLStatement)
			subtype_index = 1
			group_index = 3
		elif orderBy == 'Form':
			SQLStatement = 'SELECT `SeqName`,`SubType`,`Active`,`Role`,`Form` FROM LibDB WHERE `Role` <> "BaseSeq" ORDER BY `Form` ASC'
			records = RunSQL(DBFilename, SQLStatement)
			subtype_index = 1
			group_index = 4
		else:
			return

		group = ''
		group_node = ''
		for record in records:
			cur_name = record[0]
			cur_group = record[group_index]
			cur_subtype = record[subtype_index]
			if cur_group != group:
				group_node = QtWidgets.QTreeWidgetItem(root)
				group_node.setText(0, cur_group)
				group_node.setFlags(group_node.flags() | Qt.ItemIsUserCheckable)
				group_node.setCheckState(0, Qt.Unchecked)
				group = cur_group

			seq_icon = QtGui.QIcon()
			if cur_subtype[0] == 'H':
				seq_icon.addPixmap(QtGui.QPixmap(":/PNG-Icons/HA.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			elif cur_subtype[0] == 'N':
				seq_icon.addPixmap(QtGui.QPixmap(":/PNG-Icons/NA.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			else:
				seq_icon.addPixmap(QtGui.QPixmap(":/PNG-Icons/Seq.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			cur_node = QtWidgets.QTreeWidgetItem(group_node)
			cur_node.setText(0, cur_name)
			cur_node.setIcon(0, seq_icon)
			cur_node.setFlags(cur_node.flags() | Qt.ItemIsUserCheckable)
			if record[2] == 'True':
				cur_node.setCheckState(0, Qt.Checked)
			else:
				cur_node.setCheckState(0, Qt.Unchecked)

		self.ui.treeWidget.itemClicked['QTreeWidgetItem*', 'int'].connect(self.TreeItemClicked)
		self.ui.treeWidget.expandAll()

	def TreeItemClicked(self, item, column):
		if item.checkState(0):
			if item.childCount() > 0:
				for i in range(item.childCount()):
					cur_child = item.child(i)
					cur_child.setCheckState(0, Qt.Checked)
		else:
			if item.childCount() > 0:
				for i in range(item.childCount()):
					cur_child = item.child(i)
					cur_child.setCheckState(0, Qt.Unchecked)
		self.updateSelection()

	def updateSelection(self):
		global DBFilename
		root = self.ui.treeWidget.invisibleRootItem()
		root = root.child(0)

		self.ui.listWidgetStrainsIn.clear()
		selections = []
		unselections = []

		num_subtype = root.childCount()
		for i in range(num_subtype):
			node_subtype = root.child(i)
			num_seq = node_subtype.childCount()
			for j in range(num_seq):
				node_seq = node_subtype.child(j)
				if node_seq.checkState(0):
					selections.append(node_seq.text(0))
				else:
					unselections.append(node_seq.text(0))

		# update MySQL
		Where = '("' + '","'.join(selections) + '")'
		SQLStatement = 'UPDATE LibDB SET `Active` = "True" WHERE `SeqName` in ' + Where
		RunInsertion(DBFilename, SQLStatement)

		Where = '("' + '","'.join(unselections) + '")'
		SQLStatement = 'UPDATE LibDB SET `Active` = "False" WHERE `SeqName` in ' + Where
		RunInsertion(DBFilename, SQLStatement)
		# updata interface
		self.ui.listWidgetStrainsIn.addItems(selections)

	@pyqtSlot()
	def OpenRecent(self):  # how to activate menu and toolbar actions!!!
		#need to simply get database name and populate list views
		if self.ui.cboRecent.currentText() == 'Open previous' or self.ui.cboRecent.currentText() == '':
			pass
		else:
			cur_file = self.ui.cboRecent.currentText()
			if os.path.exists(cur_file):
				# check if this is the right DB
				SQLStatement = 'SELECT * FROM LibDB ORDER BY SeqName DESC LIMIT 1 '
				try:
					DataIn = RunSQL(cur_file, SQLStatement)
				except:
					QMessageBox.warning(self, 'Warning', 'There is no LibDB table in the selected database!',
					                    QMessageBox.Ok,
					                    QMessageBox.Ok)
					return

				self.open_db(self.ui.cboRecent.currentText())
			else:
				self.UpdateRecent()
				QMessageBox.warning(self, 'Warning', 'This DB file does not exist!',
				                    QMessageBox.Ok, QMessageBox.Ok)

	@pyqtSlot()
	def UpdateRecentFilelist(self, DBFilename):
		global working_prefix
		record_file = os.path.join(working_prefix, '..', 'Resources', 'Conf', 'db_record.txt')

		if os.path.exists(record_file):
			my_open = open(record_file, 'r')
			my_infor = my_open.readlines()
			my_open.close()
			if len(my_infor) != 0:
				my_infor = my_infor[0]
				my_infor = my_infor.split(',')
				if DBFilename in my_infor:
					pass
				else:
					file_handle = open(record_file, 'a')
					str = ',' + DBFilename
					file_handle.write(str)
					file_handle.close()
					self.ui.cboRecent.addItem(DBFilename)
			else:
				file_handle = open(record_file, 'w')
				file_handle.write(DBFilename)
				file_handle.close()
				self.ui.cboRecent.addItem(DBFilename)
		else:
			file_handle = open(record_file, 'w')
			file_handle.write(DBFilename)
			file_handle.close()
			self.ui.cboRecent.addItem(DBFilename)

	@pyqtSlot()
	def on_btnCopyRecords_clicked(self):
		global DBFilename
		# selected records
		listItems = self.ui.listWidgetStrainsIn.selectedItems()
		if len(listItems) == 0:
			QMessageBox.warning(self, 'Warning', 'Please select at least one record!',
			                    QMessageBox.Ok,
			                    QMessageBox.Ok)
			return
		else:
			SQLStatement = 'SELECT * FROM LibDB WHERE '
			WhereState = ''
			NumSeqs = len(listItems)
			i = 1
			# search selected sequence name
			for item in listItems:
				eachItemIs = item.text()
				WhereState += 'SeqName = "' + eachItemIs + '"'
				if NumSeqs > i:
					WhereState += ' OR '
				i += 1
			SQLStatement = SQLStatement + WhereState

		# select target DB
		new_db = openFile(self, 'ldb')

		if new_db != None and new_db != '':
			# import data
			BackMessage = CopyDatatoDB2(SQLStatement, DBFilename, new_db)
			if BackMessage == 1:
				QMessageBox.warning(self, 'Warning', 'Faiil to attach DB!',
				                    QMessageBox.Ok,
				                    QMessageBox.Ok)
			elif BackMessage == 2:
				QMessageBox.warning(self, 'Warning',
				                    'No data table detected in your database!',
				                    QMessageBox.Ok,
				                    QMessageBox.Ok)
			elif BackMessage == 3:
				QMessageBox.warning(self, 'Warning',
				                    'Fail to insert data into your DB! Duplicated records identified!',
				                    QMessageBox.Ok,
				                    QMessageBox.Ok)
			else:
				question = 'Would you like to open the target Database?'
				buttons = 'YN'
				answer = questionMessage(self, question, buttons)
				if answer == 'Yes':
					DBFilename = new_db
					self.open_db(DBFilename)

	@pyqtSlot()
	def on_btnExtractRecords_clicked(self):
		global DBFilename
		# selected records
		listItems = self.ui.listWidgetStrainsIn.selectedItems()
		if len(listItems) == 0:
			QMessageBox.warning(self, 'Warning', 'Please select at least one record!',
			                    QMessageBox.Ok,
			                    QMessageBox.Ok)
			return
		else:
			SQLStatement = 'SELECT * FROM LibDB WHERE '
			WhereState = ''
			NumSeqs = len(listItems)
			i = 1
			# search selected sequence name
			for item in listItems:
				eachItemIs = item.text()
				WhereState += 'SeqName = "' + eachItemIs + '"'
				if NumSeqs > i:
					WhereState += ' OR '
				i += 1
			SQLStatement = SQLStatement + WhereState
		# create DB
		options = QtWidgets.QFileDialog.Options()

		# options |= QtWidgets.QFileDialog.DontUseNativeDialog
		new_db, _ = QtWidgets.QFileDialog.getSaveFileName(self,
		                                                      "New Database",
		                                                      "New database",
		                                                      "Librator database Files (*.ldb);;All Files (*)",
		                                                      options=options)

		if new_db != None and new_db != '':
			(dirname, filename) = os.path.split(new_db)
			(shortname, extension) = os.path.splitext(filename)

			if extension != '.ldb':
				new_db = shortname + '.ldb'
			creatnewDB(new_db)

			# import data
			BackMessage = CopyDatatoDB2(SQLStatement, DBFilename, new_db)
			if BackMessage == 1:
				QMessageBox.warning(self, 'Warning', 'Faiil to insert those resords into target DB!',
				                    QMessageBox.Ok,
				                    QMessageBox.Ok)
			else:
				question = 'Would you like to open the target Database?'
				buttons = 'YN'
				answer = questionMessage(self, question, buttons)
				if answer == 'Yes':
					DBFilename = new_db
					self.open_db(DBFilename)

	@pyqtSlot()
	def on_actionHANumbering_triggered(self):
		# answer = informationMessage(self, 'Would you like to generate a numbering report?' 'YN')
		AASeq = self.ui.textAA.toPlainText()
		if AASeq != '':
			Numbering = HANumbering(AASeq)
			self.ui.tabWidget.setCurrentIndex(1)

	@pyqtSlot()
	def ListItemChanged(self):
		global DataIs
		listItems = self.ui.listWidgetStrainsIn.selectedItems()
		if len(listItems) == 0:
			return
		# if not listItems: return
		for item in listItems:
			eachItemIs = item.text()

		SQLStatement = 'SELECT * FROM LibDB WHERE SeqName = "' + eachItemIs +'"'
		DataIs = RunSQL(DBFilename, SQLStatement)
		# 	 SeqName , Sequence , SeqLen, SubType , Form , Placeholder, ID
		self.UpdateFields()

	@pyqtSlot()
	def UpdateFields(self):
		# 	 SeqName, Sequence, SeqLen, SubType, Form, From, To, Active, Role, Donor, Mutations, ID
		global DataIs
		global BaseSeq
		global MoveNotChange
		MoveNotChange = True
		global SeqMove
		SeqMove = True
		CurIndex = 0
		for item in DataIs:

			self.ui.txtName.setPlainText(item[0])
			self.ui.txtSeqName2.setPlainText(item[0])

			# self.ui.cboSubtype.setCurrentText(item[3])
			# self.ui.cboForm.setCurrentText(item[4])

			# self.ui.lblDNA.setText(item[7])

			FromV = int(item[5])
			self.ui.spnFrom.setValue(FromV)
			ToV = int(item[6])
			self.ui.spnTo.setValue(ToV)

			self.UpdateSequences()

			Role = item[8]
			if Role == 'Unassigned':
				CurIndex = 0
			if Role == 'BaseSeq':
				CurIndex = 1
				BaseSeq = item[0]
			if Role == 'Reference':
				CurIndex = 2
			if Role == 'Generated':
				CurIndex = 3
			if Role == 'none':
				CurIndex = 0

			self.ui.cboRole.setCurrentIndex(CurIndex)
			self.ui.cboRole.last_value = Role


			SubType = item[3]
			CurIndex = subtype_switch(SubType)
			self.ui.cboSubtype.setCurrentIndex(CurIndex)
			self.ui.cboSubtype.last_value = self.ui.cboSubtype.currentText()

			Form = item[4]
			if Form == 'Full HA':
				CurIndex = 0
			if Form == 'Probe HA':
				CurIndex = 1
			if Form == 'Full NA':
				CurIndex = 2
			if Form == 'Probe NA':
				CurIndex = 3
			if Form == 'Other':
				CurIndex = 4


			self.ui.cboForm.setCurrentIndex(CurIndex)
			self.ui.cboForm.last_value = Form
			self.ui.txtDonorRegions.setText(item[9])

			self.ui.txtInsert_Base.setText(item[10])

		MoveNotChange = False

	@pyqtSlot()
	def on_btnClearStrain_clicked(self):
		self.removeSel()

	@pyqtSlot()
	def on_btnClearAll_clicked(self):
		self.removeAll()

	@pyqtSlot()
	def on_btnSeqIn_clicked(self):
		self.AddActive()

	@pyqtSlot()
	def AddActive(self):
		listItems = self.ui.listWidgetStrains.selectedItems()
		if not listItems: return
		activeItems = []
		count = self.ui.listWidgetStrainsIn.count()
		for i in range(count):
			activeItems.append(self.ui.listWidgetStrainsIn.item(i).text())
		for item in listItems:
			eachItemIs = item.text()
			if eachItemIs in activeItems:
				Msg = 'The selected sequence: ' + eachItemIs + ' is already in the active list!'
				QMessageBox.warning(self, 'Warning', Msg, QMessageBox.Ok, QMessageBox.Ok)
			else:
				self.ui.listWidgetStrainsIn.addItem(eachItemIs)
				self.UpdateSeq(eachItemIs, 'True', 'Active')

			# self.FillAlignmentTab()

	@pyqtSlot()
	def on_actionPrint_triggered(self):
		if DBFilename == 'none':
			QMessageBox.warning(self, 'Warning', 'No Librator database determined!', QMessageBox.Ok, QMessageBox.Ok)
			return
		global DataIs

		FontIs = self.TextEdit.textEdit.currentFont()
		font = QFont(FontIs)

		# SeqName, Sequence, SeqLen, SubType, Form, VFrom, VTo, Active, Role, Donor, Mutations, ID
		if self.ui.tabWidget.currentIndex() == 0:
			fields = ['SeqName', 'Sequence', 'Length', 'Subtype', 'Form', 'From', 'To', 'Active', 'Role', 'Donor regions',
			          'Mutations']
			# SQLStatement = VGenesSQL.MakeSQLStatement(self, fields, data[0])
			if len(DataIs) == 0:
				return
			for data in DataIs:
				DataIn = [data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10]]

			Document = ''
			i = 0
			for item in DataIn:
				Document += (fields[i] + ': \t' + str(item) + '\n')
				i += 1
			Document += ('Protein: ' + self.ui.textAA.toPlainText() + '\n')
			Document += '\n'
			Document += self.windowTitle()
			font.setPointSize(10)
			font.setFamily('Lucida Grande')

		elif self.ui.tabWidget.currentIndex() == 1:
			# return
			# self.ui.txtAASeq.setFont(font)
			# self.ui.txtAA.setText(Document)
			font.setPointSize(10)
			font.setFamily('Courier New')
			self.ui.txtAASeq.setFont(font)
			document = self.ui.txtAASeq.document()
			printer = QtPrintSupport.QPrinter()

			dlg = QtPrintSupport.QPrintDialog(printer, self)
			if dlg.exec_() != QtWidgets.QDialog.Accepted:
				return
			# printer.setOrientation(QtPrintSupport.QPrinter.Landscape)
			document.print_(printer)

			font.setPointSize(14)
			font.setFamily('Courier New')
			self.ui.txtAASeq.setFont(font)

			return
			# Document += ('DNA: ' + self.ui.txtDNASeq.toPlainText() + '\n')
			# Document += ('Protein: ' + self.ui.txtAASeq.toPlainText() + '\n')
			# Document += ('\n' + self.windowTitle())
			# font.setPointSize(10)
			# font.setFamily('Lucida Grande')

		elif self.ui.tabWidget.currentIndex() == 2:
			Document = self.ui.txtName.toPlainText() + '\n'
			Document += self.ui.txtSeqAlignment.toPlainText()
			Document += ('\n' + self.windowTitle())
			font.setPointSize(7)
			font.setFamily('Courier New')

		elif self.ui.tabWidget.currentIndex() == 3:
			return

		self.TextEdit.textEdit.setFont(font)

		#self.TextEdit.show()

		self.TextEdit.textEdit.setText(Document)

		document = self.TextEdit.textEdit.document()
		printer = QPrinter()

		dlg = QPrintDialog(printer, self)
		if dlg.exec_() != QtWidgets.QDialog.Accepted:
			return

		if self.ui.tabWidget.currentIndex() == 3: printer.setOrientation(QPrinter.Landscape)
		document.print_(printer)

		self.statusBar().showMessage("Ready", 2000)

	@pyqtSlot()
	def on_listWidgetStrains_mouseDoubleClickEvent(self):
		self.AddActive()

	@pyqtSlot()
	def PopulateCboActiveCbo(self):
		listItems = self.ui.listWidgetStrainsIn.selectedItems()
		if not listItems: return

		for item in listItems:
			eachItemIs = item.text()
		self.ui.cboActive.addItems(listItems)

	@pyqtSlot()
	def removeSel(self):
		listRow = self.ui.listWidgetStrainsIn.currentRow()
		listItems = self.ui.listWidgetStrainsIn.selectedItems()
		for item in listItems:
			eachItemIs = item.text()
			self.UpdateSeq(eachItemIs,'False','Active')
		if listRow>-1:
			self.ui.listWidgetStrainsIn.takeItem(listRow)
		self.rebuildTree()

	@pyqtSlot()
	def removeAll(self):
		# listRow = self.ui.listWidgetStrainsIn.currentRow()
		# if not listRow: return

		self.ui.listWidgetStrainsIn.selectAll()
		listItems = self.ui.listWidgetStrainsIn.selectedItems()
		for item in listItems:
			eachItemIs = item.text()
			self.UpdateSeq(eachItemIs,'False','Active')
		self.ui.listWidgetStrainsIn.clear()
		self.rebuildTree()

	@pyqtSlot()
	def on_listWidgetStrainsIn_changeEvent(self):
		self.PopulateCboActiveCbo()

	@pyqtSlot()
	def on_actionCheck_Update_bin_folder_triggered(self):
		self.open_binpath_dialog()

	@pyqtSlot()
	def on_actionCheck_Update_base_folder_triggered(self):
		self.open_basepath_dialog()

	@pyqtSlot()
	def on_action_New_triggered(self):  # how to activate menu and toolbar actions!!!

		options = QtWidgets.QFileDialog.Options()
		global DBFilename
		# options |= QtWidgets.QFileDialog.DontUseNativeDialog
		DBFilename, _ = QtWidgets.QFileDialog.getSaveFileName(self,
		                                                      "New Database",
		                                                      "New database",
		                                                      "Librator database Files (*.ldb);;All Files (*)",
		                                                      options=options)

		if DBFilename != None and DBFilename != 'none' and DBFilename != '':
			(dirname, filename) = os.path.split(DBFilename)
			(shortname, extension) = os.path.splitext(filename)

			if extension != '.ldb':
				DBFilename = shortname + '.ldb'

			creatnewDB(DBFilename)

			# self.UpdateRecentList(DBFilename, True)
			question = 'Would you like to enter sequences into your new database?'
			buttons = 'YN'
			answer = questionMessage(self, question, buttons)
			if answer == 'Yes':
				self.ImportSeqs()
		self.UpdateRecentFilelist(DBFilename)
			# if os.path.isfile(DBFilename):
			# 	self.LoadDB(DBFilename)
		self.ui.cboRecent.setCurrentIndex(0)

	@pyqtSlot()
	def on_actionImportLei_triggered(self):
		global DBFilename

		typeOpen = 'csv'
		SavedFile = openFile(self, typeOpen)
		AASeq = []
		FASTA = ''
		with open(SavedFile, 'r') as currentfile:
			try:
				for row in currentfile:  # imports data from file
					Rawentry = row.strip('\n')
					entryFields = Rawentry.split(',')


					if len(entryFields) == 2:
						SeqName = entryFields[0]
						SeqName = '>' + SeqName + '\n'
						Sequence = entryFields[1] + '\n'
						FASTA += SeqName
						FASTA += Sequence
			except:
				print('oops')

		typeOpen = 'fasta'
		SavedFile = saveFile(self, typeOpen)

		with open(SavedFile, 'w') as currentFile:
			currentFile.write(FASTA)

	@pyqtSlot()
	def on_action_Import_triggered(self):
		self.ImportSeqs()

	@pyqtSlot()
	def on_btnImport_clicked(self):
		self.ImportSeqs()

	@pyqtSlot()
	def on_btnDelete_clicked(self):
		self.open_delete_dialog()

	@pyqtSlot()
	def ImportSeqs(self):
		global DBFilename
		if DBFilename == 'none':
			Msg = 'Please open or create a sequence database first!'
			QMessageBox.warning(self, 'Warning', Msg, QMessageBox.Ok, QMessageBox.Ok)
			return

		SeqInfoPacket = []
		filename = openFile(self, 'FASTA')
		if filename is None:
			return
		HA_Read = ReadFASTA(filename)
		SequenceFiltered = []
		# check if any sequence have strange nt
		ErrMsg = 'The following sequences will not be imported due to unlawful nucleotide more than 5%:\n\n'
		ErrSign = False
		pattern = re.compile(r'[^ATCGUatcgu]')
		for element in HA_Read:
			cur_name = element[0]
			cur_seq = element[1]
			cur_strange = pattern.findall(cur_seq)
			if len(cur_strange) > int(0.05 * len(cur_seq)):
				cur_strange = list(set(cur_strange))
				ErrMsg += cur_name + ':\n\nUnlawful nucleotide are: ' + ','.join(cur_strange) + '\n'
				ErrSign = True
			else:
				SequenceFiltered.append(element)
		if ErrSign:
			QMessageBox.warning(self, 'Warning', ErrMsg, QMessageBox.Ok, QMessageBox.Ok)

		HA_Read = SequenceFiltered

		StopAsking = 'No'
		AlreadyAsked = 'No'
		StopAskingForm = 'No'
		AlreadyAskedForm = 'No'


		if len(HA_Read) == 0:
			answer = informationMessage(self,
			                            'Please select a FASTA file of a full length HA beginning at the first coding nucleotide',
			                            'OK')
			return

		for item in HA_Read:
			HAName = item[0]
			HASeq = item[1].upper()

			# HAAA = Translator(HASeq.upper(), 0)
			if StopAsking == 'No':
				items = ('H1','H2','H3','H4','H5','H6','H7','H8','H9','H10','H11','H12','H13','H14','H15','H16','H17',
				         'H18','N1','N2','N3','N4','N5','N6','N7','N8','N9','N10','N11','B','Other')
				title = 'Choose infleunza subtype for ' + HAName
				subtype = setItem(self, items, title)
				# self.ui.cmbSubtypes_Base.setCurrentText(subtype)
				if subtype == "Cancel":
					subtype = 'none'
					return
			if AlreadyAsked == 'No':
				StopAsking = informationMessage(self, 'Use this subtype information for all strains?', 'YN')
				AlreadyAsked = 'Yes'

			if StopAskingForm == 'No':
				items = ('Full HA', 'Probe HA', "Full NA", "Probe NA", 'Other')
				title = 'Choose form of molecule for ' + HAName
				form = setItem(self, items, title)
				# self.ui.cmbForm_Base.setCurrentText(form)
				if subtype == "Cancel":
					form = 'none'
					return



			if AlreadyAskedForm == 'No':
				StopAskingForm = informationMessage(self, 'Use this form information for all strains?', 'YN')
				AlreadyAskedForm = 'Yes'


			# self.ui.textBaseSeq.setText(HASeq.upper())
			# self.ui.textBaseAA.setText(HAAA[0])
			# self.ui.textBaseSeqName.setText(HAName)
			Active = 'False'
			Role = 'Unassigned'
			VFrom = '1'
			VTo = '5000'
			Donor = 'none'
			Mutations = 'none'
			# SeqName, Sequence, SeqLen, SubType, Form, VFromw, VTo, Active, Role, Donor, Mutations, ID

			ItemIn = [HAName, HASeq, str(len(HASeq)), subtype, form, VFrom, VTo, Active, Role, Donor, Mutations, 0]
			SeqInfoPacket.clear()
			SeqInfoPacket.append(ItemIn)
			if DBFilename == 'none':
				self.on_action_New_triggered()
				return
			NumEnterred = enterData(self, DBFilename,SeqInfoPacket)
		self.PopulateCombos()

	@pyqtSlot()
	def PopulateCombos(self):
		DataIs = RunSQL(DBFilename, 'None')
		global BaseSeq

		# refresh left part
		self.rebuildTree()
		# refresh right part
		self.ui.listWidgetStrainsIn.clear()
		for item in DataIs:
			SeqName = item[0]
			if item[7] == 'True':
				self.ui.listWidgetStrainsIn.addItem(SeqName)
			if item[8] == 'Base':
				BaseSeq = SeqName
				self.ui.lblBaseName.setText(BaseSeq)

	def show3Dstructure(self, mutation, pdbPath, pymolPath, subtype):
		global temp_folder

		time_stamp = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()) + '.pml'
		pml_path = os.path.join(temp_folder, time_stamp)
		with open(pml_path , "w") as pml:
			# write pml script
			text = "load " + pdbPath + "\n"
			pml.write(text)
			text = "as cartoon\n" \
					+ "show mesh\n" \
					+ "bg_color white\n" \
					+ "color lightorange\n"
			pml.write(text)

			# highlight antigentic sites for H3N2 (A,B,C,D,E) and H1N1 (Ca1, Ca2, Cb, Sa, Sb)
			if subtype in Group1:
				text = "sel ABS-Ca1, chain A+C+E+G+I+K and (resi 142+143+144+145+146+147+172+173+174+175+176+209+210+211)\n" \
						+ "sel ABS-Ca2, chain A+C+E+G+I+K and (resi 227+228+229)\n" \
						+ "sel ABS-Cb, chain A+C+E+G+I+K and (resi 76+77+78+79+80+81)\n" \
						+ "sel ABS-Sa, chain A+C+E+G+I+K and (resi 130+131+159+160+161+162+163+165+166+167+168+169+170)\n" \
						+ "sel ABS-Sb, chain A+C+E+G+I+K and (resi 190+191+192+193+194+195+196+197+198+199+200)\n" \
						+ "color purple, ABS-Ca1\n" \
						+ "color yellow, ABS-Ca2\n" \
						+ "color gray, ABS-Cb\n" \
						+ "color chocolate, ABS-Sa\n" \
						+ "color green, ABS-Sb\n"
				pml.write(text)
			elif subtype in Group2:
				text = "sel ABS-A, chain A+C+E+G+I+K and (resi 122+126+127+128+129+130+131+132+133+137+141+142+143+144)\n" \
						+ "sel ABS-B, chain A+C+E+G+I+K and (resi 155+156+157+158+159+160+164+186+188+189+190+191+192+193+194+195+196+197+198+201)\n" \
						+ "sel ABS-C, chain A+C+E+G+I+K and (resi 52+53+54+275+276)\n" \
						+ "sel ABS-D, chain A+C+E+G+I+K and (resi 174+182+207+220+226+229+230+242+244)\n" \
						+ "sel ABS-E, chain A+C+E+G+I+K and (resi 62+63+78+81+83)\n" \
						+ "color purple, ABS-A\n" \
						+ "color yellow, ABS-B\n" \
						+ "color gray, ABS-C\n" \
						+ "color chocolate, ABS-D\n" \
						+ "color green, ABS-E\n"
				pml.write(text)
			else:
				QMessageBox.warning(self, 'Warning', 'We only support HA structure now!', QMessageBox.Ok, QMessageBox.Ok)
				return

			# highlight mutations in red on the 3D structure
			if mutation != "none":
				position = re.sub('[A-Za-z]', '', mutation)
				position = position.strip(',')
				real_pos_arr = position.split(',')
				# convert original position numbering to H1 or H3 numbering
				seq_name = self.ui.txtName.toPlainText()
				WhereState = "SeqName = " + '"' + seq_name + '"'
				SQLStatement = 'SELECT * FROM LibDB WHERE ' + WhereState
				DataIn = RunSQL(DBFilename, SQLStatement)
				HASeq = DataIn[0][1]
				FromV = int(DataIn[0][5]) - 1
				if FromV == -1: FromV = 0
				ToV = int(DataIn[0][6]) - 1

				HASeq = HASeq[FromV:ToV]
				# translate nt to aa
				HAAA = Translator(HASeq.upper(), 0)
				HAAA = HAAA[0]
				# HA numbering
				HANumbering(HAAA)

				if subtype  in Group1:
					numbering = H1Numbering
				elif subtype  in Group2:
					numbering = H3Numbering
				else:
					QMessageBox.warning(self, 'Warning',
					                    'We will support NA and FLU B later!', QMessageBox.Ok, QMessageBox.Ok)
					return

				# for HA1 mutations:
				position = ''
				for x in real_pos_arr:
					if numbering[int(x)][0] == 'HA1' and numbering[int(x)][2] != '-':
						position += str(numbering[int(x)][2]) + '+'

				position = position.strip('+')
				text = "sel ha1mutation, chain A+C+E+G+I+K and (resi " + position + ")\n"
				pml.write(text)
				text = "color red, ha1mutation\n"
				pml.write(text)

				labels = mutation.split(",")
				for label in labels:
					number = int(re.sub('[A-Za-z]', '', label))
					if numbering[number][0] == 'HA1' and numbering[number][2] != '-':
						position = str(numbering[number][2])
						text = "label chain A+C+E+G+I+K and resi " + position + " and name C, \"" + label + "\"\n"
						pml.write(text)

				# for HA2 mutations:
				position = ''
				for x in real_pos_arr:
					if numbering[int(x)][0] == 'HA2' and numbering[int(x)][2] != '-':
						position += str(numbering[int(x)][2]) + '+'

				position = position.strip('+')
				text = "sel ha2mutation, chain B+D+F+H+J+L and (resi " + position + ")\n"
				pml.write(text)
				text = "color red, ha2mutation\n"
				pml.write(text)

				labels = mutation.split(",")
				for label in labels:
					number = int(re.sub('[A-Za-z]', '', label))
					if numbering[number][0] == 'HA2' and numbering[number][2] != '-':
						position = str(numbering[number][2])
						text = "label chain B+D+F+H+J+L and resi " + position + " and name C, \"" + label + "\"\n"
						pml.write(text)

				text = "set label_size, 25\n"
				pml.write(text)

		cmd = pymolPath + " " + pml_path
		#print(cmd)
		bot1 = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True, env={"LANG": "en_US.UTF-8", "LC_ALL": "en_US.UTF-8"})

	@pyqtSlot()
	def on_gibsonBTN_clicked(self):
		self.open_gibson_dialog()

	@pyqtSlot()
	def on_pymolBTN_clicked(self):
		global pymol_path, working_prefix

		seq = self.ui.txtName.toPlainText()
		if seq == '':
			QMessageBox.warning(self, 'Warning',
			                    'Please select a sequence first!', QMessageBox.Ok, QMessageBox.Ok)
			return
		mutation = self.ui.txtInsert_Base.toPlainText().strip(",")
		subtype = str(self.ui.cboSubtype.currentText())

		# set 3D templates for different subtypes
		if subtype in Group1:
			pdb_path = os.path.join(working_prefix, '..', 'Resources', 'PDB', '4jtv.pdb')
		elif subtype in Group2:
			pdb_path = os.path.join(working_prefix, '..', 'Resources', 'PDB', '4hmg.pdb')
		elif subtype in GroupNA:
			pdb_path = os.path.join(working_prefix, '..', 'Resources', 'PDB', '3hto.pdb')
		elif subtype == "B":
			pdb_path = os.path.join(working_prefix, '..', 'Resources', 'PDB', '3hto.pdb')
		else:
			pdb_path = os.path.join(working_prefix, '..', 'Resources', 'PDB', '3hto.pdb')

		self.show3Dstructure(mutation, pdb_path, pymol_path, subtype)

	def generate_mutation_sequence(self, mode, template_name, seq_name, mutation1, mutation2):
		# load data records from database
		WhereState = "SeqName = " + '"' + seq_name + '"'
		SQLStatement = 'SELECT * FROM LibDB WHERE ' + WhereState
		DataIn = RunSQL(DBFilename, SQLStatement)

		if len(DataIn) == 1:
			QMessageBox.warning(self, 'Warning', 'The sequence name \n' + seq_name + "\nhas been taken!",
								QMessageBox.Ok, QMessageBox.Ok)
		else:
			# load data records from database
			WhereState = "SeqName = " + '"' + template_name + '"'
			SQLStatement = 'SELECT * FROM LibDB WHERE ' + WhereState
			DataIn = RunSQL(DBFilename, SQLStatement)
			HASeq = DataIn[0][1]
			Seqlen = DataIn[0][2]
			subtype = DataIn[0][3]
			Form = DataIn[0][4]
			FromV = int(DataIn[0][5]) - 1
			if FromV == -1: FromV = 0
			ToV = int(DataIn[0][6]) - 1
			Active = DataIn[0][7]
			Role = DataIn[0][8]
			Donor = DataIn[0][9]
			existing_mutation = DataIn[0][10]
			Base_seq = DataIs[0][12]

			HASeq = HASeq[FromV:ToV]
			# translate nt to aa
			HAAA = Translator(HASeq.upper(), 0)
			HAAA = HAAA[0]

			# check AA sequence
			#Msg = SequenceCheck(HAAA, 'aa')
			#if Msg != 'none':
			#	Msg =  'Your AA Sequence of \n' + DataIn[0][0] + '\nhave some improper Amino Acid: ' + Msg + '.\nDo you still want to continue?'
			#	reply = QMessageBox.question(self, 'Information',
			#	                             Msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
			#	if reply == QMessageBox.No:
			#		return

			# HA numbering
			HANumbering(HAAA)
			if subtype in Group1:
				numbering = H1Numbering
			elif subtype in Group2:
				numbering = H3Numbering
			else:
				numbering = H3Numbering

			# get correct positions, also check if the mutation is correct
			if mode == "OriPos":
				# create mutation dictionarys
				mutations = mutation1.split(",")
				mutations_dic_oriAA = {}
				mutations_dic_mutAA = {}
				for ele in mutations:
					ele = ele.upper()
					match_obj = re.search(r'(^[GAVLIPFYWSTCMNQDEKRH])(\d+)([GAVLIPFYWSTCMNQDEKRH])$', ele, re.M | re.I)
					if match_obj == None:
						QMessageBox.warning(self, 'Warning', 'The pattern \n' + ele + "\nis not in correct format!",
											QMessageBox.Ok, QMessageBox.Ok)
					else:
						mutations_dic_oriAA[int(match_obj.group(2))] = match_obj.group(1)
						mutations_dic_mutAA[int(match_obj.group(2))] = match_obj.group(3)
				# foreach by sort the mutation position, check if all the mutation are correct
				for pos in sorted(mutations_dic_oriAA.keys()):
					cur_oriAA = mutations_dic_oriAA[pos]
					if cur_oriAA == numbering[pos][1]:
						pass
					else:
						QMessageBox.warning(self, 'Warning', "On the AA sequence, position " + str(pos) + " (count from M) is "
											+ numbering[pos][1] + ", not " + cur_oriAA
											+ ". Please check your numbering carefully!",
											QMessageBox.Ok, QMessageBox.Ok)
						return

				# after all the mutations passed the check, we can start to add mutation into template sequence
				for pos in sorted(mutations_dic_oriAA.keys()):
					cur_mutAA = mutations_dic_mutAA[pos]
					cur_condon = AACodonDict[cur_mutAA]
					condon_start = (pos - 1) * 3
					condon_end = pos * 3
					HASeq = HASeq[:condon_start] + cur_condon + HASeq[condon_end:]

				if BaseSeq != '' and existing_mutation != 'none':
					template_name = BaseSeq
					existing_mutation = existing_mutation.strip(',')
					mutation1 = existing_mutation + ',' + mutation1

				# after generate nt sequence with all mutations, we can import the sequence into the DB
				SQLStatement = "INSERT INTO LibDB(`SeqName`, `Sequence`, `SeqLen`, `SubType`, `Form`, `VFrom`, `VTo`, `Active`, `Role`, " \
							   "`Donor`, `Mutations`, `ID`, `Base`) VALUES('" \
							   + seq_name + "','" \
							   + HASeq + "','" \
							   + str(len(HASeq)) + "','" \
							   + subtype + "','" \
							   + Form + "','" \
							   + "1" + "','" \
							   + "5000" + "','" \
							   + Active + "','" \
							   + "Generated" + "','" \
							   + "none" + "','" \
							   + mutation1 + "','" \
							   + "0" + "','" \
							   + template_name + "')"
				response = RunInsertion(DBFilename, SQLStatement)
				if(response == 1):
					QMessageBox.warning(self, 'Warning', "Error happen when insert the new sequence!",
										QMessageBox.Ok, QMessageBox.Ok)
				else:
					# add new sequence information into listWidgetStrainsIn
					self.ui.listWidgetStrainsIn.addItem(seq_name)
					self.rebuildTree()

					if self.modalessMutationDialog != None:
						self.modalessMutationDialog.close()
			elif mode == "H1H3pos":
				mutations = []
				# convert H1/H3 numbering to original numbering
				# start with HA1
				if mutation1 == "":
					pass
				else:
					mutations_ha1 = mutation1.split(",")
					for ele in mutations_ha1:
						match_obj = re.search(r'(^[GAVLIPFYWSTCMNQDEKRH])(\d+)([GAVLIPFYWSTCMNQDEKRH])$', ele, re.M | re.I)
						if match_obj == None:
							QMessageBox.warning(self, 'Warning', 'The pattern \n' + ele + "\nis not in correct format!",
												QMessageBox.Ok, QMessageBox.Ok)
						else:
							pos = int(match_obj.group(2))
							for n in range(1, len(numbering)):
								if numbering[n][0] == "HA1" and numbering[n][2] == pos:
									tmp_str = match_obj.group(1) + str(n) + match_obj.group(3)
									mutations.append(tmp_str)
				# then HA2
				if mutation2 == "":
					pass
				else:
					mutations_ha2 = mutation2.split(",")
					for ele in mutations_ha2:
						match_obj = re.search(r'(^[GAVLIPFYWSTCMNQDEKRH])(\d+)([GAVLIPFYWSTCMNQDEKRH])$', ele, re.M | re.I)
						if match_obj == None:
							QMessageBox.warning(self, 'Warning', 'The pattern \n' + ele + "\nis not in correct format!",
												QMessageBox.Ok, QMessageBox.Ok)
						else:
							pos = int(match_obj.group(2))
							for n in range(1, len(numbering)):
								if numbering[n][0] == "HA2" and numbering[n][2] == pos:
									tmp_str = match_obj.group(1) + str(n) + match_obj.group(3)
									mutations.append(tmp_str)

				# Now all the H1/H3 numbering mutations have been converted to original positions
				mutations_dic_oriAA = {}
				mutations_dic_mutAA = {}
				seprator = ','
				mutation_text = seprator.join(mutations)
				for ele in mutations:
					ele = ele.upper()
					match_obj = re.search(r'(^[GAVLIPFYWSTCMNQDEKRH])(\d+)([GAVLIPFYWSTCMNQDEKRH])$', ele, re.M | re.I)
					if match_obj == None:
						QMessageBox.warning(self, 'Warning', 'The pattern \n' + ele + "\nis not in correct format!",
											QMessageBox.Ok, QMessageBox.Ok)
					else:
						mutations_dic_oriAA[int(match_obj.group(2))] = match_obj.group(1)
						mutations_dic_mutAA[int(match_obj.group(2))] = match_obj.group(3)
				# foreach by sort the mutation position, check if all the mutation are correct
				contiune_run = 0
				for pos in sorted(mutations_dic_oriAA.keys()):
					cur_oriAA = mutations_dic_oriAA[pos]
					if cur_oriAA == numbering[pos][1]:
						contiune_run = 1
					else:
						QMessageBox.warning(self, 'Warning', "On the AA sequence, position " + str(pos) + " (count from M) is "
											+ numbering[pos][1] + ", not " + cur_oriAA
											+ ". Please check your numbering carefully!",
											QMessageBox.Ok, QMessageBox.Ok)
						contiune_run = 0

				# after all the mutations passed the check, we can start to add mutation into template sequence
				if contiune_run == 1:
					for pos in sorted(mutations_dic_oriAA.keys()):
						cur_mutAA = mutations_dic_mutAA[pos]
						cur_condon = AACodonDict[cur_mutAA]
						condon_start = (pos - 1) * 3
						condon_end = pos * 3
						HASeq = HASeq[:condon_start] + cur_condon + HASeq[condon_end:]

					if BaseSeq != '' and existing_mutation != 'none':
						template_name = BaseSeq
						existing_mutation = existing_mutation.strip(',')
						mutation_text = existing_mutation + ',' + mutation_text

					# after generate nt sequence with all mutations, we can import the sequence into the DB
					SQLStatement = "INSERT INTO LibDB(SeqName, Sequence, SeqLen, SubType, Form, VFrom, VTo, Active, Role, " \
								   "Donor, Mutations, ID, Base) VALUES('" \
								   + seq_name + "','" \
								   + HASeq + "','" \
								   + str(len(HASeq)) + "','" \
								   + subtype + "','" \
								   + Form + "','" \
								   + "1" + "','" \
								   + "5000" + "','" \
								   + Active + "','" \
								   + "Generated" + "','" \
								   + "none" + "','" \
								   + mutation_text + "','" \
								   + "0" + "','" \
								   + template_name + "')"
					response = RunInsertion(DBFilename, SQLStatement)
					if response == 1:
						QMessageBox.warning(self, 'Warning', "Error happen when insert the new sequence!",
											QMessageBox.Ok, QMessageBox.Ok)
					else:
						# add new sequence information into listWidgetStrainsIn
						self.ui.listWidgetStrainsIn.addItem(seq_name)
						if self.modalessMutationDialog != None:
							self.modalessMutationDialog.close()

	def generate_mutation_sequence_pre(self, numbering, template_name, seq_name, mutation1, mutation2, mode):
		if mode == 'single':
			self.generate_mutation_sequence(numbering, template_name, seq_name, mutation1, mutation2)
		else:
			if numbering == "OriPos":
				mutation1 = mutation1.strip(',')
				mutations = mutation1.split(',')
				for x in mutations:
					if x != '':
						seq_name1 = template_name + '-' + x
						self.generate_mutation_sequence(numbering, template_name, seq_name1, x, mutation2)
			else:
				mutation1 = mutation1.strip(',')
				mutations = mutation1.split(',')
				for x in mutations:
					if x != '':
						seq_name1 = template_name + '-' + x + '(HA1)'
						self.generate_mutation_sequence(numbering, template_name, seq_name1, x, '')

				mutation2 = mutation2.strip(',')
				mutations = mutation2.split(',')
				for x in mutations:
					if x != '':
						seq_name1 = template_name + '-' + x + '(HA2)'
						self.generate_mutation_sequence(numbering, template_name, seq_name1, '', x)

	def open_mutation_dialog(self):
		if self.ui.txtName.toPlainText() == "":
			QMessageBox.warning(self, 'Warning', 'Please select a sequence first!', QMessageBox.Ok, QMessageBox.Ok)
		else:
			cur_seq_name = self.ui.txtName.toPlainText()
			self.modalessMutationDialog = MutationDialog()
			self.modalessMutationDialog.ui.CurSeq.setText(cur_seq_name)
			# check sequence subtype
			if self.ui.cboSubtype.currentText() in Group1 or self.ui.cboSubtype.currentText() in Group2:
				pass
			else:
				self.modalessMutationDialog.ui.tabWidget.removeTab(1)

			# get active sequences from Qlist in main window
			donor_num = self.ui.listWidgetStrainsIn.count()
			donor_list = []
			for i in range(donor_num):
				donor_list.append(self.ui.listWidgetStrainsIn.item(i).text())

			self.modalessMutationDialog.active_sequence = donor_list
			self.modalessMutationDialog.ui.SeqName.setText(self.ui.txtName.toPlainText())
			self.modalessMutationDialog.applySignal.connect(self.generate_mutation_sequence_pre)
			self.modalessMutationDialog.show()

	def open_gibson_dialog(self):
		global working_prefix
		global joint_down
		global joint_up
		global H1_start, H1_end
		global fragmentdb_path
		global DBFilename


		if self.ui.listWidgetStrainsIn.count() == 0:
			QMessageBox.warning(self, 'Warning', 'Please active some sequences first!', QMessageBox.Ok, QMessageBox.Ok)
		else:
			self.modalessGibsonDialog = gibsoncloneDialog()
			self.modalessGibsonDialog.ui.jointUP.setText(joint_up)
			self.modalessGibsonDialog.ui.jointDOWN.setText(joint_down)

			self.modalessGibsonDialog.ui.F1_start.setText(str(H1_start[0]))
			self.modalessGibsonDialog.ui.F2_start.setText(str(H1_start[1]))
			self.modalessGibsonDialog.ui.F3_start.setText(str(H1_start[2]))
			self.modalessGibsonDialog.ui.F4_start.setText(str(H1_start[3]))
			self.modalessGibsonDialog.ui.F1_end.setText(str(H1_end[0]))
			self.modalessGibsonDialog.ui.F2_end.setText(str(H1_end[1]))
			self.modalessGibsonDialog.ui.F3_end.setText(str(H1_end[2]))
			self.modalessGibsonDialog.ui.F4_end.setText(str(H1_end[3]))

			# fill the selection table
			SQLStatement = 'SELECT SeqName,SubType FROM LibDB WHERE `Active` = "True"'
			DataIn = RunSQL(DBFilename, SQLStatement)
			num_row = len(DataIn)
			num_col = 2
			self.modalessGibsonDialog.ui.selectionTable.setRowCount(num_row)
			self.modalessGibsonDialog.ui.selectionTable.setColumnCount(num_col)
			horizontalHeader = ['Name', 'Subtype']
			self.modalessGibsonDialog.ui.selectionTable.setHorizontalHeaderLabels(horizontalHeader)
			self.modalessGibsonDialog.ui.selectionTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
			self.modalessGibsonDialog.ui.selectionTable.horizontalHeader().setSectionResizeMode(1,QtWidgets.QHeaderView.Fixed)
			self.modalessGibsonDialog.ui.selectionTable.setColumnWidth(1,60)

			for row_index in range(num_row):
				cell_checkBox = QCheckBox()
				cell_checkBox.setText(DataIn[row_index][0])
				cell_checkBox.setChecked(False)
				self.modalessGibsonDialog.ui.selectionTable.setCellWidget(row_index, 0, cell_checkBox)
				self.modalessGibsonDialog.ui.selectionTable.setItem(row_index, 1,
				                            QTableWidgetItem(DataIn[row_index][1]))

			self.modalessGibsonDialog.gibsonSignal.connect(self.GenerateGibson)

			# check saved MYSQL setting
			mysql_setting_file = os.path.join(working_prefix, '..', 'Resources', 'Conf', 'mysql_setting.txt')

			if os.path.exists(mysql_setting_file):
				my_open = open(mysql_setting_file, 'r')
				my_info = my_open.readlines()
				my_open.close()
				my_info = my_info[0]
			else:
				file_handle = open(mysql_setting_file, 'w')
				my_info = ',,,,'
				file_handle.write(my_info)
				file_handle.close()

			my_info = my_info.strip('\n')
			Setting = my_info.split(',')

			self.modalessGibsonDialog.ui.IPinput.setText(Setting[0])
			self.modalessGibsonDialog.ui.Portinput.setText(Setting[1])
			self.modalessGibsonDialog.ui.DBnameinput.setText(Setting[2])
			self.modalessGibsonDialog.ui.Userinput.setText(Setting[3])
			self.modalessGibsonDialog.ui.Passinput.setText(Setting[4])

			self.modalessGibsonDialog.ui.dbpath.setText(fragmentdb_path)

			self.modalessGibsonDialog.show()

	def open_update_dialog(self):
		global BaseSeq
		if self.ui.txtName.toPlainText() == "":
			QMessageBox.warning(self, 'Warning', 'Please determine a sequence first!', QMessageBox.Ok, QMessageBox.Ok)
		else:
			self.modalessUpdateDialog = updateSeqDialog()
			#
			self.modalessUpdateDialog.ui.lineEdit.setText(self.ui.txtName.toPlainText())
			self.modalessUpdateDialog.ui.textEdit.setText(self.ui.textSeq.toPlainText())
			self.modalessUpdateDialog.highRegion()
			self.modalessUpdateDialog.updateSignal.connect(self.updateNTseq)
			self.modalessUpdateDialog.show()

	def updateNTseq(self,SeqName,Seq):
		# update the value in DB
		self.UpdateSeq(SeqName, Seq, 'Sequence')
		# refresh the interface
		self.ListItemChanged()
		# close the dialog
		self.modalessUpdateDialog.close()
		self.ui.spnFrom.setValue(1)

	def open_delete_dialog(self):
		delete = self.ui.listWidgetStrainsIn.selectedItems()

		list = []
		for item in delete:
			list.append(item.text())

		self.modalessDeleteDialog = deleteDialog()
		self.modalessDeleteDialog.ui.listWidget.addItems(list)
		self.modalessDeleteDialog.deleteSignal.connect(self.delRecords)
		self.modalessDeleteDialog.show()

	def delRecords(self, del_list):
		NumSeqs = len(del_list)
		if NumSeqs == 0:
			return

		WhereState = ''
		i = 1
		for element in del_list:
			WhereState += 'SeqName = "' + element + '"'
			if NumSeqs > i:
				WhereState += ' OR '
			i += 1

		SQLStatement = 'DELETE FROM LibDB WHERE ' + WhereState
		deleterecords(DBFilename, SQLStatement)

		# refresh the list - all sequence list
		self.rebuildTree()

		# refresh the list - active sequence list
		self.ui.listWidgetStrainsIn.clear()
		SQLStatement = 'SELECT `SeqName` FROM LibDB WHERE Active = "True"'
		records = RunSQL(DBFilename, SQLStatement)
		new_records = []
		for x in records:
			new_records.append(x[0])
		self.ui.listWidgetStrainsIn.addItems(new_records)

		self.modalessDeleteDialog.close()

	def open_tree_dialog(self, Names, Seqs, this_path):
		self.modalessTreeDialog = treeDialog()

		self.modalessTreeDialog.ui.nameList.addItems(Names)
		seq_text = '\n'.join(Seqs) + '\n'
		self.modalessTreeDialog.ui.seqEdit.setText(seq_text)
		self.modalessTreeDialog.path = this_path
		self.modalessTreeDialog.names = Names
		self.modalessTreeDialog.seqs = Seqs
		self.modalessTreeDialog.treeSignal.connect(self.drawTree)

		self.modalessTreeDialog.show()

	def drawTree(self, Data, this_path):
		global raxml_path
		global figtree_path
		outfilename = this_path + "/alignment_parsed.fas"
		treefilename = 'tree'
		# generate output file
		file_handle = open(outfilename, 'w')
		for i in range(0,len(Data)):
			file_handle.write('>' + Data[i][0] + '\n')
			file_handle.write(Data[i][1] + '\n')
		file_handle.close()

		# generate tree
		cmd = 'cd ' + this_path + ';'
		cmd += raxml_path
		cmd += ' -m PROTGAMMAAUTO -p 12345 -T 2 -s ' + outfilename + ' -n ' + treefilename
		os.system(cmd)

		# open file folder
		my_cur_os = system()
		if my_cur_os == 'Windows':
			cmd = 'explorer ' + this_path  # Windows
		elif my_cur_os == 'Darwin':
			cmd = 'open ' + this_path  # mac
		elif my_cur_os == 'Linux':
			cmd = 'nautilus' + this_path  # Linux
		else:
			cmd = ''
		if cmd != '':
			try:
				os.system(cmd)
			except ValueError:
				pass

		# try to open best tree using FigTree
		try:
			cmd = figtree_path + ' ' + this_path + '/RAxML_bestTree.tree'
			bot1 = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True,
			             env={"LANG": "en_US.UTF-8", "LC_ALL": "en_US.UTF-8"})
		except:
			QMessageBox.warning(self, 'Warning',
			                    'Can not find FigTree in your computer! Please open trees manually in the folder',
			                    QMessageBox.Ok,
			                    QMessageBox.Ok)

	def open_fusion_dialog(self):
		if self.ui.lblBaseName.toPlainText() == "":
			QMessageBox.warning(self, 'Warning', 'Please determine a base sequence first!', QMessageBox.Ok, QMessageBox.Ok)
		else:
			self.modalessFusionDialog = fusionDialog()
			# get active sequences from Qlist in main window
			donor_num = self.ui.listWidgetStrainsIn.count()
			donor_list = []
			for i in range(donor_num):
				donor_list.append(self.ui.listWidgetStrainsIn.item(i).text())

			# remove the base seq from donor list
			if BaseSeq in donor_list:
				donor_list.remove(BaseSeq)
			self.modalessFusionDialog.ui.selection.addItems(donor_list)
			self.modalessFusionDialog.ui.basename.setText(BaseSeq)
			self.modalessFusionDialog.fusionSignal.connect(self.showhumbering)
			self.modalessFusionDialog.fusionSeqSignal.connect(self.fusionseq)
			self.modalessFusionDialog.displaySeq()
			self.modalessFusionDialog.show()

	def open_basepath_dialog(self):
		global working_prefix
		global muscle_path
		global clustal_path
		global pymol_path
		global figtree_path
		global raxml_path
		global fragmentdb_path

		self.modalessbaseDialog = basePathDialog()
		self.modalessbaseDialog.ui.musclePath.setText(muscle_path)
		self.modalessbaseDialog.ui.clustaloPath.setText(clustal_path)
		self.modalessbaseDialog.ui.pymolPath.setText(pymol_path)
		self.modalessbaseDialog.ui.FigtreePath.setText(figtree_path)
		self.modalessbaseDialog.ui.RaxmlPath.setText(raxml_path)
		self.modalessbaseDialog.ui.FragmentDB_path.setText(fragmentdb_path)

		# check saved MYSQL setting
		mysql_setting_file = os.path.join(working_prefix, '..', 'Resources', 'Conf', 'mysql_setting.txt')

		if os.path.exists(mysql_setting_file):
			my_open = open(mysql_setting_file, 'r')
			my_info = my_open.readlines()
			my_open.close()
			my_info = my_info[0]
		else:
			file_handle = open(mysql_setting_file, 'w')
			my_info = ',,,,'
			file_handle.write(my_info)
			file_handle.close()

		my_info = my_info.strip('\n')
		Setting = my_info.split(',')

		self.modalessbaseDialog.ui.IPinput.setText(Setting[0])
		self.modalessbaseDialog.ui.Portinput.setText(Setting[1])
		self.modalessbaseDialog.ui.DBnameinput.setText(Setting[2])
		self.modalessbaseDialog.ui.Userinput.setText(Setting[3])
		self.modalessbaseDialog.ui.Passinput.setText(Setting[4])

		self.modalessbaseDialog.show()

	def showhumbering(self, Data, Note, dnaCheck, aaCheck, posCheck):
		for item in Data:
			DataIn = []
			DataIn.append(item)
			self.AlignSequencesFusion(DataIn, Note, dnaCheck, aaCheck, posCheck)
			time.sleep(0.1)

	def fusionseq(self, base_seq, donor_seq, del_start, del_end, add_start, add_end):
		global DBFilename
		# donor sequence
		WhereState = 'SeqName = "' + donor_seq + '"'
		SQLStatement = 'SELECT SeqName, Sequence, Vfrom, VTo FROM LibDB WHERE ' + WhereState
		DataIn = RunSQL(DBFilename, SQLStatement)
		Sequence = DataIn[0][1]
		VFrom = int(DataIn[0][2]) - 1
		if VFrom == -1: VFrom = 0
		VTo = int(DataIn[0][3])
		Sequence = Sequence[VFrom:VTo]
		Sequence = Sequence.upper()

		add_start_nt = int((add_start - 1) * 3)
		add_end_nt = int(add_end * 3)
		if add_end_nt > len(Sequence):
			QMessageBox.warning(self, 'Warning', 'Donor end position larger than donor sequence!', QMessageBox.Ok,
			                    QMessageBox.Ok)
			return
		else:
			add_sequence = Sequence[add_start_nt:add_end_nt]

		# base sequence
		WhereState = 'SeqName = "' + base_seq + '"'
		SQLStatement = 'SELECT SeqName, Sequence, Vfrom, VTo FROM LibDB WHERE ' + WhereState
		DataIn = RunSQL(DBFilename, SQLStatement)
		Sequence = DataIn[0][1]
		VFrom = int(DataIn[0][2]) - 1
		if VFrom == -1: VFrom = 0
		VTo = int(DataIn[0][3])
		Sequence = Sequence[VFrom:VTo]
		Sequence = Sequence.upper()

		del_start_nt = (del_start - 1) * 3
		del_end_nt = del_end * 3
		del_sequence = Sequence[del_start_nt:del_end_nt]

		Sequence = Sequence[:del_start_nt] + add_sequence + Sequence[del_end_nt:]

		# insert into DB
		SQLStatement = 'SELECT * FROM LibDB WHERE ' + WhereState
		DataIn = RunSQL(DBFilename, SQLStatement)

		seq_name = base_seq + '(' + str(del_start) + '-' + str(del_end) + ')' + '+' + donor_seq + '(' + str(
			add_start) + '-' + str(add_end) + ')'
		AA_seq = Translator(add_sequence, 0)
		i = 0
		mutations = []
		for aa in AA_seq[0]:
			cur_pos = del_start + i
			cur = 'X' + str(cur_pos) + aa
			mutations.append(cur)
			i += 1
		mutations = ','.join(mutations)

		SQLStatement = "INSERT INTO LibDB(`SeqName`, `Sequence`, `SeqLen`, `SubType`, `Form`, `VFrom`, `VTo`, `Active`, `Role`, " \
		               "`Donor`, `Mutations`, `ID`, `Base`) VALUES('" \
		               + seq_name + "','" \
		               + Sequence + "','" \
		               + str(len(Sequence)) + "','" \
		               + DataIn[0][3] + "','" \
		               + DataIn[0][4] + "','" \
		               + "1" + "','" \
		               + "5000" + "','" \
		               + DataIn[0][7] + "','" \
		               + "Generated" + "','" \
		               + "none" + "','" \
		               + mutations + "','" \
		               + "0" + "','" \
		               + base_seq + "')"
		response = RunInsertion(DBFilename, SQLStatement)
		if (response == 1):
			QMessageBox.warning(self, 'Warning', "Error happen when insert the new sequence!",
			                    QMessageBox.Ok, QMessageBox.Ok)
		else:
			# add new sequence information into listWidgetStrainsIn
			self.ui.listWidgetStrainsIn.addItem(seq_name)
			self.rebuildTree()
			if self.modalessFusionDialog != None:
				self.modalessFusionDialog.close()

	def sequence_editing(self):
		if BaseSeq == "":
			QMessageBox.warning(self, 'Warning', 'Please determine base sequence first!', QMessageBox.Ok, QMessageBox.Ok)
		else:
			self.modalessSeqEditDialog = SequenceEditDialog()
			self.modalessSeqEditDialog.ui.BaseSeqName.setText(BaseSeq)
			# get active sequences from Qlist in main window
			donor_num = self.ui.listWidgetStrainsIn.count()
			donor_list = []
			for i in range(donor_num):
				donor_list.append(self.ui.listWidgetStrainsIn.item(i).text())
			# remove the base seq from donor list
			if BaseSeq in donor_list:
				donor_list.remove(BaseSeq)
			# set donor list for Qlists in pop up window
			self.modalessSeqEditDialog.ui.DonorList_tab1.addItems(donor_list)
			self.modalessSeqEditDialog.ui.DonorList_tab2.addItems(donor_list)
			# set multiple selection mode for Qlist in tab1
			self.modalessSeqEditDialog.ui.DonorList_tab1.setSelectionMode(QAbstractItemView.ExtendedSelection)
			# connect the signal with a handle function
			self.modalessSeqEditDialog.seqEditSignal.connect(self.get_sequence_edit_info)
			self.modalessSeqEditDialog.show()

	def get_sequence_edit_info(self, editing_mode, base_sequence, donor_sequences, mutation_schema):  # For modaless dialog
		global muscle_path
		# this function only process sequence editing within same subtype
		if editing_mode == 0:   # base biased mode
			# get information for base sequence
			WhereState = "SeqName = " + '"' + base_sequence + '"'
			SQLStatement = 'SELECT * FROM LibDB WHERE ' + WhereState
			DataIn = RunSQL(DBFilename, SQLStatement)
			base_nt_seq = DataIn[0][1]
			base_subtype = DataIn[0][3]
			base_from = int(DataIn[0][5]) - 1
			base_to = int(DataIn[0][6])
			if base_from == -1: base_from = 0
			base_nt_seq = base_nt_seq[base_from:base_to]
			base_nt_seq = base_nt_seq.upper()
			base_aa_seq = Translator(base_nt_seq, 0)
			base_aa_seq = base_aa_seq[0]
			base_aa_seq = re.sub(r'\*.+', "", base_aa_seq)

			# get information for donor sequences
			donor_sequence_names = donor_sequences.split("\t")
			donor_sequences_arr = []
			for cur_seq in donor_sequence_names:
				# get information for donor sequence
				WhereState = "SeqName = " + '"' + cur_seq + '"'
				SQLStatement = 'SELECT * FROM LibDB WHERE ' + WhereState
				DataIn = RunSQL(DBFilename, SQLStatement)
				donor_nt_seq = DataIn[0][1]
				donor_subtype = DataIn[0][3]
				donor_from = int(DataIn[0][5]) - 1
				donor_to = int(DataIn[0][6])
				donor_donor = DataIn[0][9]
				if donor_from == -1: donor_from = 0
				donor_nt_seq = donor_nt_seq[donor_from:donor_to]
				donor_nt_seq = donor_nt_seq.upper()
				donor_aa_seq = Translator(donor_nt_seq, 0)
				donor_aa_seq = donor_aa_seq[0]
				donor_aa_seq = re.sub(r'\*.+', "", donor_aa_seq)
				if donor_donor == "none":
					donor_start = 0
					donor_end = len(donor_aa_seq)
				else:
					tmp = donor_donor.split('-')
					donor_start = int(tmp[0])
					donor_end = int(tmp[1])

				if base_subtype != donor_subtype:
					QMessageBox.warning(self, 'Warning', 'This Function only works for same subtype!',
										QMessageBox.Ok,
										QMessageBox.Ok)
					return

				cur_array = [cur_seq, donor_aa_seq, donor_start, donor_end, donor_subtype]
				donor_sequences_arr.append(cur_array)

			# align all sequences
			# write sequence into file for alignment
			time_stamp = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime())
			in_file = os.path.join(temp_folder, "in" + time_stamp + ".fas")
			out_file = os.path.join(temp_folder, "out" + time_stamp + ".fas")
			temp_file = open(in_file, "w")
			temp_file.write(">" + base_sequence + "\n")
			temp_file.write(base_aa_seq + "\n")

			for x in range(len(donor_sequences_arr)):
				temp_file.write(">" + donor_sequences_arr[x][0] + "\n")
				temp_file.write(donor_sequences_arr[x][1] + "\n")

			temp_file.close()

			# check if muscle exist or not
			if os.path.exists(muscle_path):
				pass
			else:
				QMessageBox.warning(self,'Warning','The muscle file does not exist!',QMessageBox.Ok, QMessageBox.Ok)
				return
			# run muscle to align query seuqnece to template sequence
			cmd = muscle_path
			cmd += " -in " + in_file + " -out " + out_file
			# print(cmd)
			try:
				os.system(cmd)
			except:
				QMessageBox.warning(self, 'Warning', 'Fail to run muscle! Check your muscle path!', QMessageBox.Ok,
				                    QMessageBox.Ok)
				return

			# read alignment from muscle results
			align_file = open(out_file, "r")
			alignment = align_file.read()
			sequences_block = alignment.split(">")

			for cur_block in sequences_block:
				if cur_block == '':
					continue
				tmp = cur_block.split("\n")
				cur_name = tmp[0]
				tmp = tmp[1:]
				seperator = ""
				cur_seq = seperator.join(tmp)

				if base_sequence == cur_name:
					base_aa_seq = cur_seq
				else:
					for x in range(len(donor_sequences_arr)):
						if donor_sequences_arr[x][0] in cur_name:
							donor_sequences_arr[x][1] = cur_seq

			# correct numbering according to alignment result
			if '-' in base_aa_seq:
				QMessageBox.warning(self, 'Warning', 'Just let you know that there are insertions in donor!', QMessageBox.Ok,
									QMessageBox.Ok)
				# new sequences have insertion, adjust the start and end position for all fragments based on current alignment
				hyphen_pos_base = [i.start() for i in re.finditer('-', base_aa_seq)]

				for x in range(len(donor_sequences_arr)):
					donor_aa_seq = donor_sequences_arr[x][1]
					donor_start = donor_sequences_arr[x][2]
					donor_end = donor_sequences_arr[x][3]

					hyphen_pos_donor = [i.start() for i in re.finditer('-', donor_aa_seq)]
					for pos_iter in hyphen_pos_base:
						donor_aa_seq = donor_aa_seq[:pos_iter] + '#' + donor_aa_seq[pos_iter + 1:]

					remove_hyphen = str.maketrans('', '', '-')
					base_aa_seq = base_aa_seq.translate(remove_hyphen)
					remove_sharp = str.maketrans('', '', '#')
					donor_aa_seq = donor_aa_seq.translate(remove_sharp)

					# step 1: convert donor region from original numbering to alignment numbering
					if len(hyphen_pos_donor) > 0:
						for pos_iter in hyphen_pos_donor:
							if donor_start >= pos_iter:
								donor_start += 1
								donor_end += 1
							elif donor_end >= pos_iter:
								donor_end += 1
					# step 2: convert donor region from alignment numbering to base sequence numbering
					alignment_donor_start = donor_start
					alignment_donor_end = donor_end
					for pos_iter in hyphen_pos_base:
						if alignment_donor_start >= pos_iter:
							donor_start -= 1
							donor_end -= 1
						elif alignment_donor_end >= pos_iter:
							donor_end -= 1

					donor_sequences_arr[x][1] = donor_aa_seq
					donor_sequences_arr[x][2] = donor_start
					donor_sequences_arr[x][3] = donor_end

			else:
				for x in range(len(donor_sequences_arr)):
					donor_aa_seq = donor_sequences_arr[x][1]
					donor_start = donor_sequences_arr[x][2]
					donor_end = donor_sequences_arr[x][3]

					hyphen_pos_donor = [i.start() for i in re.finditer('-', donor_aa_seq)]
					# step 1: convert donor region from original numbering to alignment numbering
					if len(hyphen_pos_donor) > 0:
						for pos_iter in hyphen_pos_donor:
							if donor_start >= pos_iter:
								donor_start += 1
								donor_end += 1
							elif donor_end >= pos_iter:
								donor_end += 1

					donor_sequences_arr[x][1] = donor_aa_seq
					donor_sequences_arr[x][2] = donor_start
					donor_sequences_arr[x][3] = donor_end

			# base biased sequence generate residue by residue
			mutation = []
			for x in range(len(base_aa_seq)):
				cur_residue_base = base_aa_seq[x]

				cur_residue_donor = []
				for y in range(len(donor_sequences_arr)):
					cur_donor_seq = donor_sequences_arr[y][1]
					if x >= donor_sequences_arr[y][2] and x < donor_sequences_arr[y][3]:
						cur_residue_donor.append(cur_donor_seq[x])
				count = Counter(cur_residue_donor).most_common(2)

				if count[0][0] != cur_residue_base:
					if len(count) > 1:
						if count[0][1] > count[1][1]:
							cur_mutation = cur_residue_base + str(x + 1) + count[0][0]
							mutation.append(cur_mutation)
					else:
						cur_mutation = cur_residue_base + str(x + 1) + count[0][0]
						mutation.append(cur_mutation)

			# generate sequence
			if len(mutation) != 0:
				mutation = ",".join(mutation)
				# generate new base baised sequence
				new_seq_name = base_sequence + "-" + mutation + "(Base Biased)"
				self.generate_mutation_sequence("OriPos", base_sequence, new_seq_name, mutation, "")
				self.modalessSeqEditDialog.close()
			else:
				QMessageBox.warning(self, 'Warning', 'The base biased sequence is identical to base sequence! Do nothing!',
									QMessageBox.Ok,
									QMessageBox.Ok)

			os.remove(in_file)
			os.remove(out_file)

		elif editing_mode == 1:     # Cocktail mode
			# get information for base sequence
			WhereState = "SeqName = " + '"' + base_sequence + '"'
			SQLStatement = 'SELECT * FROM LibDB WHERE ' + WhereState
			DataIn = RunSQL(DBFilename, SQLStatement)
			base_nt_seq = DataIn[0][1]
			base_subtype = DataIn[0][3]
			base_from = int(DataIn[0][5]) - 1
			base_to = int(DataIn[0][6])
			if base_from == -1: base_from = 0
			base_nt_seq = base_nt_seq[base_from:base_to]
			base_nt_seq = base_nt_seq.upper()
			base_aa_seq = Translator(base_nt_seq, 0)
			base_aa_seq = base_aa_seq[0]
			base_aa_seq = re.sub(r'\*.+', "", base_aa_seq)

			# get information for donor sequence
			WhereState = "SeqName = " + '"' + donor_sequences + '"'
			SQLStatement = 'SELECT * FROM LibDB WHERE ' + WhereState
			DataIn = RunSQL(DBFilename, SQLStatement)
			donor_nt_seq = DataIn[0][1]
			donor_subtype = DataIn[0][3]
			donor_from = int(DataIn[0][5]) - 1
			donor_to = int(DataIn[0][6])
			donor_donor = DataIn[0][9]
			if donor_from == -1: donor_from = 0
			donor_nt_seq = donor_nt_seq[donor_from:donor_to]
			donor_nt_seq = donor_nt_seq.upper()
			donor_aa_seq = Translator(donor_nt_seq, 0)
			donor_aa_seq = donor_aa_seq[0]
			donor_aa_seq = re.sub(r'\*.+', "", donor_aa_seq)
			donor_aa_seq = re.sub(r'\*.?', "", donor_aa_seq)
			donor_aa_seq = re.sub(r'\~', "", donor_aa_seq)

			if donor_donor == "none":
				donor_start = 0
				donor_end = len(donor_aa_seq)
			else:
				tmp = donor_donor.split('-')
				donor_start = int(tmp[0])
				donor_end = int(tmp[1])

			if base_subtype != donor_subtype:
				QMessageBox.warning(self, 'Warning', 'This Function only works for same subtype!',
									QMessageBox.Ok,
									QMessageBox.Ok)
				return

			# get all mutation information in donor region
			# write sequence into file for alignment
			time_stamp = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime())
			in_file = os.path.join(temp_folder, "in" + time_stamp + ".fas")
			out_file = os.path.join(temp_folder, "out" + time_stamp + ".fas")
			temp_file = open(in_file, "w")
			temp_file.write(">" + base_sequence + "\n")
			temp_file.write(base_aa_seq + "\n")
			temp_file.write(">" + donor_sequences + "\n")
			temp_file.write(donor_aa_seq + "\n")
			temp_file.close()

			# check if muscle exist or not
			if os.path.exists(muscle_path):
				pass
			else:
				QMessageBox.warning(self, 'Warning', 'The muscle file does not exist!', QMessageBox.Ok, QMessageBox.Ok)
				return
			# run muscle to align query seuqnece to template sequence
			cmd = muscle_path
			cmd += " -in " + in_file + " -out " + out_file
			# print(cmd)
			try:
				os.system(cmd)
			except:
				QMessageBox.warning(self, 'Warning', 'Errors happen when running muscle! Current command: \n' + cmd, QMessageBox.Ok, QMessageBox.Ok)
				return

			# read alignment from muscle results
			align_file = open(out_file, "r")
			alignment = align_file.read()
			sequences_block = alignment.split(">")
			sequences_block = sequences_block[1:]

			for cur_block in sequences_block:
				tmp = cur_block.split("\n")
				cur_name = tmp[0]
				tmp = tmp[1:]
				seperator = ""
				cur_seq = seperator.join(tmp)

				if base_sequence == cur_name:
					base_aa_seq = cur_seq
				else:
					donor_aa_seq = cur_seq


			if '-' in base_aa_seq:
				QMessageBox.warning(self, 'Warning', 'Just let you know that there are insertions in donor!', QMessageBox.Ok,
									QMessageBox.Ok)
				# new sequences have insertion, adjust the start and end position for all fragments based on current alignment
				hyphen_pos_base = [i.start() for i in re.finditer('-', base_aa_seq)]
				hyphen_pos_donor = [i.start() for i in re.finditer('-', donor_aa_seq)]
				for pos_iter in hyphen_pos_base:
					donor_aa_seq = donor_aa_seq[:pos_iter] + '#' + donor_aa_seq[pos_iter + 1:]

				remove_hyphen = str.maketrans('', '', '-')
				base_aa_seq = base_aa_seq.translate(remove_hyphen)
				remove_sharp = str.maketrans('', '', '#')
				donor_aa_seq = donor_aa_seq.translate(remove_sharp)

				# step 1: convert donor region from original numbering to alignment numbering
				if len(hyphen_pos_donor) > 0:
					for pos_iter in hyphen_pos_donor:
						if donor_start >= pos_iter:
							donor_start += 1
							donor_end += 1
						elif donor_end >= pos_iter:
							donor_end += 1
				# step 2: convert donor region from alignment numbering to base sequence numbering
				alignment_donor_start = donor_start
				alignment_donor_end = donor_end
				for pos_iter in hyphen_pos_base:
					if alignment_donor_start >= pos_iter:
						donor_start -= 1
						if donor_start < 0:
							donor_start = 0
						donor_end -= 1
					elif alignment_donor_end >= pos_iter:
						donor_end -= 1

			else:
				if '-' in donor_aa_seq:
					hyphen_pos_donor = [i.start() for i in re.finditer('-', donor_aa_seq)]
					# step 1: convert donor region from original numbering to alignment numbering
					if len(hyphen_pos_donor) > 0:
						for pos_iter in hyphen_pos_donor:
							if donor_start >= pos_iter:
								donor_start += 1
								donor_end += 1
							elif donor_end >= pos_iter:
								donor_end += 1

			base_donor_region_seq = base_aa_seq[donor_start:donor_end]
			donor_donor_region_seq = donor_aa_seq[donor_start:donor_end]

			# generate all single mutations
			all_single_mutations = []
			for num in range(len(base_donor_region_seq)):
				cur_aa_base = base_donor_region_seq[num]
				cur_aa_donor = donor_donor_region_seq[num]
				cur_pos = donor_start + num + 1
				if cur_aa_donor != "-" and cur_aa_donor != cur_aa_base:
					cur_mutation = cur_aa_base + str(cur_pos) + cur_aa_donor
					all_single_mutations.append(cur_mutation)

			# generate mutated sequences
			if mutation_schema == "all":
				# calculate total mutations number
				single_mutation_number = len(all_single_mutations)
				Msg = 'Total ' + str(single_mutation_number) + ' single mutations detected between ' + base_sequence \
				      + ' and ' + donor_sequences + '\n'
				total_num = 0
				for i in range(1,single_mutation_number+1):
					cur_total_num = int(factorial(single_mutation_number)/(factorial(i)*factorial(single_mutation_number-i)))
					total_num += cur_total_num
					Msg += 'There are ' + str(cur_total_num) + ' different combinations of ' + str(i) + ' mutations\n'
				Msg += 'There are ' + str(total_num) + ' different combinations of all mutations\n'
				Msg += 'Do you still want continue?'

				buttons = 'YN'
				answer = questionMessage(self, Msg, buttons)
				if answer == 'No':
					return

				all_mutation_combination = []
				for x in range(1,single_mutation_number+1):
					tmp = list(combinations(all_single_mutations, x))
					all_mutation_combination.extend(tmp)

				for mutation in all_mutation_combination:
					mutation = ','.join(mutation)
					new_seq_name = base_sequence + '-' + mutation + '(Cocktail)'
					self.generate_mutation_sequence("OriPos", base_sequence, new_seq_name, mutation, "")
			elif mutation_schema == "single":
				single_mutation_number = len(all_single_mutations)
				Msg = 'Total ' + str(single_mutation_number) + ' single mutations detected between ' + base_sequence \
				      + ' and ' + donor_sequences + '\n'
				Msg += 'Do you still want continue?'

				buttons = 'YN'
				answer = questionMessage(self, Msg, buttons)
				if answer == 'No':
					return

				for mutation in all_single_mutations:
					new_seq_name = base_sequence + '-' + mutation + '(Cocktail)'
					self.generate_mutation_sequence("OriPos", base_sequence, new_seq_name, mutation, "")
			else:
				return
			self.modalessSeqEditDialog.close()
			os.remove(in_file)
			os.remove(out_file)

		elif editing_mode == 2:
			pass
		elif editing_mode == 3:
			pass

	def GenerateGibson(self, mode, selections, joint_up_str, joint_down_str, out_dir, db_file, subtype, joint_plan):
		listItems = selections.split("\n")
		WhereState = ''
		NumSeqs = len(listItems)
		i = 1
		for item in listItems:
			WhereState += 'SeqName = "' + item + '"'
			if NumSeqs > i:
				WhereState += ' OR '
			i += 1

		SQLStatement = 'SELECT SeqName, Sequence, Vfrom, VTo, SubType FROM LibDB WHERE ' + WhereState
		DataIn = RunSQL(DBFilename, SQLStatement)

		# initial data container
		data_list = []
		subtype1 = ""
		error_code = 0
		for item in DataIn:
			SeqName = item[0]
			Sequence = item[1]
			VFrom = int(item[2]) - 1
			if VFrom == -1: VFrom = 0
			VTo = int(item[3])
			Sequence = Sequence[VFrom:VTo]
			SequenceNT = Sequence.upper()
			SequenceAA = Translator(SequenceNT, 0)
			cur_subtype = item[4]
			if subtype1 == "":
				subtype1 = cur_subtype
			elif subtype1 != cur_subtype:
				QMessageBox.warning(self, 'Warning', "All candidate sequences should be same subtype!", QMessageBox.Ok,
									QMessageBox.Ok)
				return

			if len(SequenceAA[1]) > 0:
				separator = "\n"
				errMsg = separator.join(SequenceAA[1])
				# QMessageBox.warning(self, 'Warning', errMsg, QMessageBox.Ok,
				# 					QMessageBox.Ok)
				pass
				#error_code = 1
				#break
			EachIn = (SeqName, SequenceNT, SequenceAA[0])
			data_list.append(EachIn)

		if subtype1 in Group1 or subtype1 in Group2:
			if subtype1 in Group1 and subtype == 'H3':
				QMessageBox.warning(self, 'Warning', "Your joint design is for H3/Group2, your sequences are " + subtype1 + '(Group1)!',
				                    QMessageBox.Ok,
				                    QMessageBox.Ok)
				return
			if subtype1 in Group2 and subtype == 'H1':
				QMessageBox.warning(self, 'Warning', "Your joint design is for H1/Group1, your sequences are " + subtype1 + '(Group2)!',
				                    QMessageBox.Ok,
				                    QMessageBox.Ok)
				return
			if subtype == 'NA':
				QMessageBox.warning(self, 'Warning', "Your joint design is for NA, your sequences are " + subtype1 + '(HA)!',
				                    QMessageBox.Ok,
				                    QMessageBox.Ok)
				return
		elif subtype1 in GroupNA:
			if subtype == 'H3' or subtype == 'H1':
				QMessageBox.warning(self, 'Warning',
				                    "Your joint design is for HA, your sequences are " + subtype1 + '(NA)!',
				                    QMessageBox.Ok,
				                    QMessageBox.Ok)
				return
			else:
				subtype = subtype1
		else:
			QMessageBox.warning(self, 'Warning', "Our Gibson Clone Designer only supports HA for now!", QMessageBox.Ok,
			                    QMessageBox.Ok)
			return

		if error_code == 0:
			data = pd.DataFrame(data_list)
			data.columns = ['Name', 'NTseq', 'AAseq']
			self.generate_gibson_fragments(data, temp_folder, out_dir, joint_up_str, joint_down_str, db_file, mode, subtype, joint_plan)

	def generate_gibson_fragments(self, data, temp_folder, out_dir, joint_up_str, joint_down_str, db_file, mode, subtype, joint_plan):
		global muscle_path
		global H1_start, H1_end, H3_start, H1_end, H1template, H1template_seq, H3template, H3template_seq, NA_start, NA_end
		global H1_start_user, H1_end_user, H3_start_user, H3_end_user, NA_start_user, NA_end_user
		global NAtemplate_name, NAtemplate_seq

		# initial the temp file name
		time_stamp = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime())
		in_file = os.path.join(temp_folder, "in" + time_stamp + ".fas")
		out_file = os.path.join(temp_folder, "out" + time_stamp + ".fas")

		if subtype == "H1":
			# set template
			template_name = H1template
			template_seq = H1template_seq
			if joint_plan == 'Default':
				aa_start = list(H1_start);
				aa_end = list(H1_end);
			else:
				aa_start = list(H1_start_user);
				aa_end = list(H1_end_user);
		elif subtype == "H3":
			# set template
			template_name = H3template
			template_seq = H3template_seq
			if joint_plan == 'Default':
				aa_start = list(H3_start);
				aa_end = list(H3_end);
			else:
				aa_start = list(H3_start_user);
				aa_end = list(H3_end_user);
		elif subtype in GroupNA:
			# set template
			template_name = NAtemplate_name[subtype]
			template_seq = NAtemplate_seq[subtype]
			if joint_plan == 'Default':
				aa_start = list(NA_start);
				aa_end = list(NA_end);
			else:
				aa_start = list(NA_start_user);
				aa_end = list(NA_end_user);
		else:
			print("We only support FLU A for now! Please input Influenza A HA or NA!")
			return
		# number of fragments
		num_fragment = len(aa_start)

		# write sequence into file for alignment
		temp_file = open(in_file, "w")
		temp_file.write(">" + template_name + "\n")
		temp_file.write(template_seq + "\n")

		for index in data.index:
			temp_file.write(">" + data.loc[index, 'Name'] + "\n")
			temp_file.write(data.loc[index, 'AAseq'] + "\n")
		temp_file.close()

		# check if muscle exist or not
		if os.path.exists(muscle_path):
			pass
		else:
			QMessageBox.warning(self, 'Warning', 'The muscle file does not exist!', QMessageBox.Ok, QMessageBox.Ok)
			return
		# run muscle to align query seuqnece to template sequence
		cmd = muscle_path
		cmd += " -in " + in_file + " -out " + out_file
		# print(cmd)
		try:
			os.system(cmd)
		except:
			QMessageBox.warning(self, 'Warning', 'Fail to run muscle! Check your muscle path!', QMessageBox.Ok,
			                    QMessageBox.Ok)
			return

		# read alignment from muscle results
		align_file = open(out_file, "r")
		alignment = align_file.read()
		sequences_block = alignment.split(">")

		for cur_seq in sequences_block:
			if template_name in cur_seq:
				template = cur_seq
				break

		tmp = template.split("\n")
		tmp = tmp[1:]
		seperator = ""
		template = seperator.join(tmp)

		if "-" in template:
			# new sequences have insertion, adjust the start and end position for all fragments based on current alignment
			hyphen_pos = [i.start() for i in re.finditer('-', template)]
			for pos_iter in hyphen_pos:
				cur_pos = pos_iter + 1
				for i in range(num_fragment):
					if (aa_start[i] >= cur_pos):
						aa_start[i] = aa_start[i] + 1
					if (aa_end[i] >= cur_pos):
						aa_end[i] = aa_end[i] + 1

		# test the position update with template
		#print("Sequence Name:\t" + template_name)
		#for i in range(num_fragment):
		#	fragment = template[aa_start[i] - 1: aa_end[i]]
		#	print("F" + str(i + 1) + ":\t" + fragment)

		# initial fragment data matrix
		fragment_data = []
		# get all the query alignments
		sequences_block = sequences_block[1:]

		for cur_seq_block in sequences_block:
			cur_seq_fragment_data = []
			if template_name in cur_seq_block:
				continue

			tmp = cur_seq_block.split("\n")
			cur_name = tmp[0]
			cur_seq_fragment_data.append(cur_name)
			tmp = tmp[1:]
			seperator = ""
			cur_seq = seperator.join(tmp)
			cur_index = np.where(data.Name == cur_name)[0][0]
			cur_seq_nt = data.loc[cur_index, 'NTseq']

			# remove the hyphen in AA sequences and modify nt start and end
			nt_start = [0] * num_fragment
			nt_end = [0] * num_fragment
			num_of_hyphen = 0

			# find how many '-' before fragment 1
			pre_fragment = cur_seq[0:aa_start[0] - 1]
			hyphen_pos = [i.start() for i in re.finditer('-', pre_fragment)]
			num_of_hyphen = num_of_hyphen + len(hyphen_pos)
			joint_aa_len = aa_end[0] - aa_start[1] + 1
			num_of_hyphen_last_joint = 0

			for i in range(num_fragment):
				fragment = cur_seq[aa_start[i] - 1: aa_end[i]]

				# check if sequence is incomplete
				if fragment[0] == '-' and i == 0:
					question = 'Fragment 1 of you sequence ' + cur_name + ' is incomplete, do you still want continue?'
					buttons = 'YN'
					answer = questionMessage(self, question, buttons)
					if answer == 'No':
						return

				hyphen_pos = [i.start() for i in re.finditer('-', fragment)]
				nt_start[i] = (aa_start[i] - 1 - num_of_hyphen + num_of_hyphen_last_joint) * 3 + 1
				num_of_hyphen = num_of_hyphen + len(hyphen_pos)
				nt_end[i] = (aa_end[i] - num_of_hyphen + num_of_hyphen_last_joint) * 3
				fragment1 = fragment.replace("-", "")
				hyphen_pos_joint = [i.start() for i in re.finditer('-', fragment[0-joint_aa_len:])]
				num_of_hyphen_last_joint += len(hyphen_pos_joint)

				nt_fragment = cur_seq_nt[nt_start[i] - 1: nt_end[i]]

				cur_seq_fragment_data.append(fragment)
				cur_seq_fragment_data.append(fragment1)
				cur_seq_fragment_data.append(nt_fragment)

				# check if NT seq perfect match AA
				nt_fragment_aa = Translator(nt_fragment,0)
				nt_fragment_aa = nt_fragment_aa[0]
				if nt_fragment_aa != fragment1:
					Msg = 'AA seq for current fragment is:\n\n'
					Msg += fragment1 + '\n\n'
					Msg += 'AA seq translated from current NT fragment is:\n\n'
					Msg += nt_fragment_aa + '\n\n'
					Msg += 'The two sequences do not match!\n'
					Msg += 'Please chekc your original NT sequences to make sure there are no strange nucleotide!'
					QMessageBox.warning(self, 'Warning', Msg, QMessageBox.Ok, QMessageBox.Ok)
					#return

			fragment_data.append(cur_seq_fragment_data)

		# make col name
		col_name = ["Name"]
		for i in range(num_fragment):
			col_name.append("F_AA_" + str(i + 1) + "_origin")
			col_name.append("F_AA_" + str(i + 1) + "_refine")
			col_name.append("F_NT_" + str(i + 1))

		fragment_data = pd.DataFrame(fragment_data)
		fragment_data.columns = col_name
		# generate fragments done!

		# open dialog to show fragments and let user to confirm
		seq_names = fragment_data['Name'].tolist()
		F1_seqs = fragment_data['F_AA_1_origin'].tolist()
		F2_seqs = fragment_data['F_AA_2_origin'].tolist()
		F3_seqs = fragment_data['F_AA_3_origin'].tolist()

		F1_seq_text = '\n'.join(F1_seqs) + '\n'
		F2_seq_text = '\n'.join(F2_seqs) + '\n'
		F3_seq_text = '\n'.join(F3_seqs) + '\n'

		# create dialog
		self.modalessGibsonMSADialog = GibsonMSADialog()
		# set values and text
		self.modalessGibsonMSADialog.ui.nameList.addItems(seq_names)
		self.modalessGibsonMSADialog.ui.seqEditF1.setText(F1_seq_text)
		self.modalessGibsonMSADialog.ui.seqEditF2.setText(F2_seq_text)
		self.modalessGibsonMSADialog.ui.seqEditF3.setText(F3_seq_text)

		# color text for F1, F2, F3, F4
		num_seq = len(seq_names)
		format = QTextCharFormat()
		format_hyphen = QTextCharFormat()
		format_hyphen.setBackground(QBrush(QColor("red")))
		format_hyphen.setForeground(QBrush(QColor("white")))

		# F1
		cursor1 = self.modalessGibsonMSADialog.ui.seqEditF1.textCursor()
		len_f1 = len(F1_seqs[0])
		CurPos = 0
		for i in range(0,num_seq):
			format.setForeground(QBrush(QColor("red")))
			cursor1.setPosition(CurPos + len_f1 - 9)
			cursor1.setPosition(CurPos + len_f1, QTextCursor.KeepAnchor)
			cursor1.mergeCharFormat(format)
			CurPos += len_f1 + 1

		text = self.modalessGibsonMSADialog.ui.seqEditF1.toPlainText()
		pos_list = [i.start() for i in re.finditer('-', text)]
		if len(pos_list) > 0:
			for pos in pos_list:
				cursor1.setPosition(pos)
				cursor1.setPosition(pos + 1, QTextCursor.KeepAnchor)
				cursor1.mergeCharFormat(format_hyphen)
		# F2
		cursor2 = self.modalessGibsonMSADialog.ui.seqEditF2.textCursor()
		len_f2 = len(F2_seqs[0])
		CurPos = 0
		for i in range(0, num_seq):
			format.setForeground(QBrush(QColor("red")))
			cursor2.setPosition(CurPos + 0)
			cursor2.setPosition(CurPos + 9, QTextCursor.KeepAnchor)
			cursor2.mergeCharFormat(format)

			cursor2.setPosition(CurPos + len_f2 - 9)
			cursor2.setPosition(CurPos + len_f2, QTextCursor.KeepAnchor)
			cursor2.mergeCharFormat(format)
			CurPos += len_f2 + 1

		text = self.modalessGibsonMSADialog.ui.seqEditF2.toPlainText()
		pos_list = [i.start() for i in re.finditer('-', text)]
		if len(pos_list) > 0:
			for pos in pos_list:
				cursor2.setPosition(pos)
				cursor2.setPosition(pos + 1, QTextCursor.KeepAnchor)
				cursor2.mergeCharFormat(format_hyphen)
		# F3
		cursor3 = self.modalessGibsonMSADialog.ui.seqEditF3.textCursor()
		len_f3 = len(F3_seqs[0])
		CurPos = 0
		for i in range(0, num_seq):
			format.setForeground(QBrush(QColor("red")))
			cursor3.setPosition(CurPos + 0)
			cursor3.setPosition(CurPos + 9, QTextCursor.KeepAnchor)
			cursor3.mergeCharFormat(format)

			if num_fragment == 4:
				cursor3.setPosition(CurPos + len_f3 - 9)
				cursor3.setPosition(CurPos + len_f3, QTextCursor.KeepAnchor)
				cursor3.mergeCharFormat(format)
			CurPos += len_f3 + 1

		text = self.modalessGibsonMSADialog.ui.seqEditF3.toPlainText()
		pos_list = [i.start() for i in re.finditer('-', text)]
		if len(pos_list) > 0:
			for pos in pos_list:
				cursor3.setPosition(pos)
				cursor3.setPosition(pos + 1, QTextCursor.KeepAnchor)
				cursor3.mergeCharFormat(format_hyphen)
		if num_fragment == 4:
			F4_seqs = fragment_data['F_AA_4_origin'].tolist()
			F4_seq_text = '\n'.join(F4_seqs) + '\n'
			self.modalessGibsonMSADialog.ui.seqEditF4.setText(F4_seq_text)
			# F4
			cursor4 = self.modalessGibsonMSADialog.ui.seqEditF4.textCursor()
			len_f4 = len(F4_seqs[0])
			CurPos = 0
			for i in range(0, num_seq):
				format.setForeground(QBrush(QColor("red")))
				cursor4.setPosition(CurPos + 0)
				cursor4.setPosition(CurPos + 9, QTextCursor.KeepAnchor)
				cursor4.mergeCharFormat(format)
				CurPos += len_f4 + 1

			text = self.modalessGibsonMSADialog.ui.seqEditF4.toPlainText()
			pos_list = [i.start() for i in re.finditer('-', text)]
			if len(pos_list) > 0:
				for pos in pos_list:
					cursor4.setPosition(pos)
					cursor4.setPosition(pos + 1, QTextCursor.KeepAnchor)
					cursor4.mergeCharFormat(format_hyphen)
		else:
			len_f4 = 0
			self.modalessGibsonMSADialog.ui.tabWidget.removeTab(3)

		# link data
		self.modalessGibsonMSADialog.fragment_data = fragment_data
		self.modalessGibsonMSADialog.mode = mode
		self.modalessGibsonMSADialog.db_file = db_file
		self.modalessGibsonMSADialog.out_dir = out_dir
		self.modalessGibsonMSADialog.names = seq_names
		self.modalessGibsonMSADialog.len = [len_f1, len_f2, len_f3, len_f4]
		self.modalessGibsonMSADialog.num_frag = num_fragment
		self.modalessGibsonMSADialog.joint = [joint_up_str, joint_down_str]
		self.modalessGibsonMSADialog.subtype = subtype
		# link signals
		self.modalessGibsonMSADialog.gibson_msa_Signal.connect(self.GibsonConfirm)
		# show dialog
		self.modalessGibsonMSADialog.show()

	def GibsonConfirm(self, fragment_data, mode, db_file, out_dir, joint, subtype, num_fragment):
		new_fragment_name_list = []
		existing_fragment_name_list = []
		joint_up_str = joint[0]
		joint_down_str = joint[1]

		# get time stamp for current data
		time_stamp = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime())
		# initial output file 1, summary EXCEL file
		summary_out_file = out_dir + "/Summary_" + time_stamp + ".xlsx"
		writer_summary = pd.ExcelWriter(summary_out_file)
		summary_array = []
		summary_index = 0

		# initial output file 2, IDT 96 well order format
		idt_out_file = out_dir + "/IDTorder_" + time_stamp + ".xlsx"
		writer_idt = pd.ExcelWriter(idt_out_file)
		idt_array = [["" for i in range(4)] for j in range(96)]
		well_row = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
		well_col = range(1, 13)

		cur_idt_index = 0
		for cur_row in well_row:
			for cur_col in well_col:
				idt_array[cur_idt_index][0] = str(cur_row) + str(cur_col)
				cur_idt_index += 1
		cur_idt_index = 0

		#print("Seq_name\tFragment\tAAseq\tName\tInstock\tNTseq")
		for index in fragment_data.index:
			# for each virus, open a file for its all 4 fragments
			seq_name = fragment_data.loc[index, "Name"]
			seq_fragment_file_name = out_dir + "/" + seq_name.replace("/", "_") + ".fas"
			temp_file = open(seq_fragment_file_name, "w")
			tmp_array = ["",seq_name]

			for i in range(num_fragment):
				aa_col_name = "F_AA_" + str(i + 1) + "_refine"
				nt_col_name = "F_NT_" + str(i + 1)

				aa_seq = fragment_data.loc[index, aa_col_name]
				nt_seq = fragment_data.loc[index, nt_col_name]

				if i == 0: # fragment 1, add upstream joint
					aa_seq = joint_up_str + aa_seq
					nt_seq = joint_up_str + nt_seq
				elif i == num_fragment - 1:  # fragment 4 or last fragment, add 3' joint
					aa_seq = aa_seq + joint_down_str
					nt_seq = nt_seq + joint_down_str

				# search from SQL DB
				SQLCommand = "SELECT * FROM Fragments WHERE AAseq = '" + aa_seq + "'"

				if mode == 0: #local mode
					fetch_results = RunSQL(db_file[0], SQLCommand)
				else:
					fetch_results = RunMYSQL(db_file, SQLCommand)

				row = len(fetch_results)
				if (row != 0):
					fragment_name = fetch_results[0][0]
					nt_seq = fetch_results[0][7]
					in_stock = fetch_results[0][8]
					if in_stock == "yes":
						existing_fragment_name_list.append(fragment_name)
					else:
						if fragment_name in new_fragment_name_list:
							pass
						else:
							new_fragment_name_list.append(fragment_name)
							idt_array[cur_idt_index][1] = fragment_name
							idt_array[cur_idt_index][2] = nt_seq
							cur_idt_index += 1
				else:
					SQLCommand = "SELECT Name FROM Fragments WHERE Fragment = '" + str(
						i + 1) + "' AND Subtype = '" + subtype + "'"

					if mode == 0:  # local mode
						fetch_results = RunSQL(db_file[0], SQLCommand)
					else:
						fetch_results = RunMYSQL(db_file, SQLCommand)

					row = len(fetch_results)
					num_id = str(row + 1)
					num_id_len = len(num_id)
					num_id = "0" * (4 - num_id_len) + num_id

					fragment_name = subtype + "-F" + str(i + 1) + "-" + num_id
					in_stock = "no"
					fragment = str(i + 1)
					if ("H" in subtype):
						segment = "HA"
					else:
						segment = "NA"

					SQLCommand = 'INSERT INTO Fragments(`Name`, `Segment`, `Fragment`, `Subtype`, `ID`, `Template`, `AAseq`, `NTseq`, `Instock`) VALUES(' \
								 + "'" + fragment_name + "'," \
								 + "'" + segment + "'," \
								 + "'" + fragment + "'," \
								 + "'" + subtype + "'," \
								 + "'" + num_id + "'," \
								 + "'" + seq_name + "'," \
								 + "'" + aa_seq + "'," \
								 + "'" + nt_seq + "'," \
								 + "'" + in_stock + "')"

					if mode == 0:  # local mode
						response = RunInsertion(db_file[0], SQLCommand)
					else:
						response = RunMYSQLInsertion(db_file, SQLCommand)

					if response == 1:
						QMessageBox.warning(self, 'Warning', "Error happen when insert the new fregment records!",
											QMessageBox.Ok, QMessageBox.Ok)
						return
					else:
						new_fragment_name_list.append(fragment_name)
						idt_array[cur_idt_index][1] = fragment_name
						idt_array[cur_idt_index][2] = nt_seq
						cur_idt_index += 1

				# print(seq_name + "\t" + str(i + 1) + "\t" + aa_seq + "\t" + fragment_name + "\t" + in_stock + "\t" + nt_seq)
				# print(seq_name + "\t" + str(i + 1) + "\t" + fragment_name + "\t" + in_stock)
				temp_file.write(">" + seq_name + "-Fragment" + str(i + 1) + "(" + fragment_name + ")" + "\n")
				temp_file.write(nt_seq + "\n")

				tmp_array.append(fragment_name)

				#SnapGene_file_name = "SnapGene/" + seq_name.replace("/", "_") + "-Fragment" + str(i + 1) + ".fas"
				#snapgene_temp_file = open(SnapGene_file_name, "w")
				#snapgene_temp_file.write(
				#	">" + seq_name + "-Fragment" + str(i + 1) + "(" + fragment_name + ")" + "\n")
				#snapgene_temp_file.write(nt_seq + "\n")
				#snapgene_temp_file.close()

			summary_array.append(tmp_array)
			temp_file.close()

		#print("\n")
		# print fragments information
		existing_fragment_name_list = np.unique(existing_fragment_name_list)
		new_fragment_name_list = np.unique(new_fragment_name_list)
		seperator = "\n"
		successMsg = "The Gibson clone fragments are generated successfully!\n"
		successMsg = "The files were generated under:\n" + out_dir + "\n"
		successMsg += "Existing fragments used:\n" + seperator.join(existing_fragment_name_list) + "\n"
		successMsg += "New fragments generated:\n" + seperator.join(new_fragment_name_list) + "\n"

		QMessageBox.information(self, 'information', successMsg, QMessageBox.Ok,
							QMessageBox.Ok)

		# save IDT EXCEL file
		idt_array = pd.DataFrame(data=idt_array)
		idt_array.columns = ["Well Position","Name","Sequence","5' Phosphorylation (for blunt cloning only)"]
		idt_array.to_excel(writer_idt, sheet_name='Sheet1', index=False)
		writer_idt.save()

		# save summary EXCEL file
		new_fragment_name_list = new_fragment_name_list.tolist()
		new_fragment_name_list.insert(0,"")
		existing_fragment_name_list = existing_fragment_name_list.tolist()
		existing_fragment_name_list.insert(0,"")
		summary_array_a = [["To order:"],new_fragment_name_list, [""], ["In stock:"], existing_fragment_name_list, [""], ["Recipe:"]]
		summary_array_a.extend(summary_array)
		summary_array_a = pd.DataFrame(data=summary_array_a)
		summary_array_a.to_excel(writer_summary, sheet_name='Sheet1', index=False)
		writer_summary.save()

		self.modalessGibsonDialog.close()

		# open Fragments file folder
		my_cur_os = system()
		if my_cur_os == 'Windows':
			cmd = 'explorer ' + path     # Windows
		elif my_cur_os == 'Darwin':
			cmd = 'open ' + out_dir      # mac
		elif my_cur_os == 'Linux':
			cmd = 'nautilus' + out_dir   # Linux
		else:
			cmd = ''
		if cmd != '':
			try:
				os.system(cmd)
			except ValueError:
				pass

def MakeRuler(pos1, pos2, step, mode):
	ErrMsg = ""
	if len(str(pos2)) > step - 1:
		ErrMsg = "Please use larger step! Current step is too short!"

	# start to make ruler
	if mode == "aa":
		step_count = int(pos2) - int(pos1) + 1
		ruler = ' . ' * step_count

		for x in range(100):
			cur_pos = pos1 + x * step
			if cur_pos <= pos2:
				ruler = ruler[:x * 3 * step + 1] + str(cur_pos) + ruler[len(str(cur_pos)) + x * 3 * step + 1:]

	else:
		ruler = ''
		cur_pos = pos1
		step_count = 0
		space_left = 0
		while cur_pos <= pos2:
			if cur_pos == pos1 + step_count * step:
				ruler += str(cur_pos)
				space_left = len(str(cur_pos)) - 1
				cur_pos += 1
				step_count += 1
			else:
				if space_left > 0:
					space_left = space_left - 1
					cur_pos += 1
				else:
					ruler += '.'
					cur_pos += 1
	return ruler

def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return (n*factorial(n-1))

def HANumbering(AASeq):
	import uuid
	global H1Numbering
	global H3Numbering
	H1Numbering.clear()
	H3Numbering.clear()
	global NumberingMap
	global temp_folder
	global muscle_path
	NumberingMap.clear()


	NameBase = str(uuid.uuid4())
	# NameBase = NameBase[:12]
	NameBase = NameBase.replace('-', '')

	NameBase = NameBase.replace(' ', '')

	MyInFiles = NameBase + 'In.txt'
	MyOutFiles = NameBase + 'Out.txt'

	workingfilename = os.path.join(temp_folder, MyInFiles)
	musclepath = re.sub(r'[^\/]+$','',muscle_path)
	savefilename = os.path.join(temp_folder,  MyOutFiles)

	workingdir, filename = os.path.split(workingfilename)
	os.chdir(workingdir)

	NumberingQuery = 'musclepath '
	NumberingQuery += musclepath + '\n' + 'ha_sequence '

	NumberingQuery += AASeq + '\n'

	Sites = 'sites '
	for Res in range(0, len(AASeq)):
		Sites += str(Res+1)
		Sites += ' '

	NumberingQuery += Sites + '\n'

	SavedFile = savefilename#'Out.txt'

	# write input sequence into input file
	with open(workingfilename, 'w') as currentFile:
		currentFile.write(NumberingQuery)

	# run HA numbering code
	HA_numbering_Jesse(workingfilename, savefilename)

	MoveOn = False
	tester = ''
	while MoveOn is False:  #function to delay progression until numbering script completes
		if os.path.isfile(SavedFile):

			with open(SavedFile, 'r') as currentFile:
				TheLines = currentFile.readlines()

				LenLines = len(TheLines)
				if LenLines > 0:
					tester = TheLines[LenLines-1]

				if tester == "Script complete.\n":
					MoveOn = True
		else:
			MoveOn = False
	Starts = ''
	for line in TheLines:
		tester = line[10:13]
		if tester == 'HA1':
			Starts = 'HA1'
			break
		elif tester == 'HA2':
			Starts = 'HA2'
			break

	AASeq = []
	HAIn = ()
	# H3In = ()
	Position = 0
	PositionT = ''
	PositionN = ''
	HASegment = ''
	HANumber = ''
	HAbase = ''
	TriOn = False
	MapEnds = 'none'


	for line in TheLines:
		line = line.strip()

		words = line.split(' ')
		if words[0] == 'Residue':
			PositionT = words[1]
			AA = PositionT[0]
			PositionN = PositionT[1:]
			Position = int(PositionN)


			# AASeq.append(words[1]) #from sequence line

		# Format: List of tuples with each tuple containing:
		# Tuple 1: Position: H1-segment (HA1 or HA2),  Amino Acid, H1Number, A/California/4/2009-residue, H1-antigenic-region
		# Tuple 2: Position: H3-segment (HA1 or HA2), Amino Acid, H3Number, A/Aichi/2/1968-residue, H3-antigenic-region
		if len(words) > 5:
			if words[5] == '4HMG':
				if words[3] == 'gap':
					HASegment = Starts
					HANumber = '-'
					HAbase = '-'


				elif words[3] == 'HA1':

					HASegment = 'HA1'
					ResidueIs = words[1]
					HANumber = int(ResidueIs[1:])
					HAbase = ResidueIs[0]
					if MapEnds == 'none':
						MapEnds = 'HA1'

				elif words[3] == 'HA2':

					HASegment = 'HA2'
					ResidueIs = words[1]
					HANumber = int(ResidueIs[1:])
					HAbase = ResidueIs[0]

				if HASegment == 'HA1':
					if str(HANumber) in H3HA1Regions.keys():
						HAAg = H3HA1Regions[str(HANumber)]
					else:
						HAAg = '-'

				elif HASegment == 'HA2':
					if str(HANumber) in H3HA2Regions.keys():
						HAAg = H3HA2Regions[str(HANumber)]
					else:
						HAAg = '-'

				HAIn = (HASegment, AA, HANumber, HAbase, HAAg, MapEnds)
				H3Numbering[Position] = HAIn
	# todo add probe components including trimer domain, avitag, his-tag
			if words[5] == '4JTV':
				if words[3] == 'gap':
					HASegment = Starts
					HANumber = '-'
					HAbase = '-'


				elif words[3] == 'HA1':

					HASegment = 'HA1'
					ResidueIs = words[1]
					HANumber = int(ResidueIs[1:])
					HAbase = ResidueIs[0]



				elif words[3] == 'HA2':

					HASegment = 'HA2'
					ResidueIs = words[1]
					HANumber = int(ResidueIs[1:])
					HAbase = ResidueIs[0]


				if HASegment == 'HA1':
					if str(HANumber) in H1HA1Regions.keys():
						HAAg = H1HA1Regions[str(HANumber)]
					else:
						HAAg = '-'

				elif HASegment == 'HA2':
					if str(HANumber) in H1HA2Regions.keys():
						HAAg = H1HA2Regions[str(HANumber)]
					else:
						HAAg = '-'

				HAIn = (HASegment, AA, HANumber, HAbase, HAAg)
				H1Numbering[Position] = HAIn

	# if len(H3Numbering) > 425:
	testString = ''
	TMOn = False
	# StartTest = False
	for i in range(1,len(H3Numbering)):
		CurRes = H3Numbering[i]
		HASegment = CurRes[0]
		AA = CurRes[1]
		HANumber = CurRes[2]
		HAbase = CurRes[3]
		HAAg = CurRes[4]
		if HASegment == 'HA1':
			if MapEnds == 'none':
				NumberingMap['H3HA1beg'] = i
				MapEnds = 'HA1'
			NumberingMap['H3HA1end'] = i

		elif HASegment == 'HA2':
			if MapEnds == 'HA1' or MapEnds == 'none':
				NumberingMap['H3HA2beg'] = i
				MapEnds = 'HA2'

			NumberingMap['H3HA2end'] = i


		try:
			testString = ''
			if AA == 'V':

				for j in range(i,i+6):
					testRes = H3Numbering[j]
					AATest = testRes[1]
					testString += AATest
				if testString == 'VELKSG' or testString == 'VQLKSG' or testString == 'VKLESM' or testString == 'VKLEST' or testString == 'VKLDS':
					TMOn = True
			elif AA == 'G':
				for j in range(i,i+6):
					testRes = H3Numbering[j]
					AATest = testRes[1]
					testString += AATest
				if testString == 'GSGYIP':
					TriOn = True
		except:
			print('tried')

		if AA == '*':
			TMOn = False
			TriOn = False
		if TMOn == True:
			HASegment = 'TM'
			HAIn = (HASegment, AA, HANumber, HAbase, HAAg)
			H3Numbering[i] = HAIn
			StartTest = False
		if TriOn == True:
			HASegment = 'Trimer-Avitag-H6'
			HAIn = (HASegment, AA, HANumber, HAbase, HAAg)
			H3Numbering[i] = HAIn
			StartTest = False

	TMOn = False
	# StartTest = False
	for i in range(1,len(H1Numbering)):
		CurRes = H1Numbering[i]
		HASegment = CurRes[0]
		AA = CurRes[1]
		HANumber = CurRes[2]
		HAbase = CurRes[3]
		HAAg = CurRes[4]
		if HASegment == 'HA1':
			if MapEnds == 'none':
				NumberingMap['H1HA1beg'] = i
				MapEnds = 'HA1'
			NumberingMap['H1HA1end'] = i

		elif HASegment == 'HA2':
			if MapEnds == 'HA1' or MapEnds == 'none':
				NumberingMap['H1HA2beg'] = i
				MapEnds = 'HA2'

			NumberingMap['H1HA2end'] = i


		try:
			testString = ''
			if AA == 'V':

				for j in range(i,i+6):
					testRes = H1Numbering[j]
					AATest = testRes[1]
					testString += AATest
				if testString == 'VELKSG' or testString == 'VQLKSG' or testString == 'VKLESM' or testString == 'VKLEST' or testString == 'VKLDS':
					TMOn = True
			elif AA == 'G':
				for j in range(i,i+6):
					testRes = H1Numbering[j]
					AATest = testRes[1]
					testString += AATest
				if testString == 'GSGYIP':
					TriOn = True
		except:
			print('tried')

		if AA == '*':
			TMOn = False
			TriOn = False
		if TMOn == True:
			HASegment = 'TM'
			HAIn = (HASegment, AA, HANumber, HAbase, HAAg)
			H1Numbering[i] = HAIn
			StartTest = False
		if TriOn == True:
			HASegment = 'Trimer-Avitag-H6'
			HAIn = (HASegment, AA, HANumber, HAbase, HAAg)
			H1Numbering[i] = HAIn
			StartTest = False

	os.remove(SavedFile)
	os.remove(workingfilename)

def ReadFASTA(outfilename):
	ReadFile = []
	# ReadFile.clear
	# SeqRead = []
	Readline = ''
	currentFile2 = ''
	if outfilename is None:
		pass
	else:
		with open(outfilename, 'r') as currentFile2:  # using with for this automatically closes the file even if you crash
			# currentFile.write(FASTAfile)
			Seq = ''
			SeqName = ''
			Readline = ''
			for line in currentFile2:
				Readline = line.replace('\n', '').replace('\r', '')
				if Readline != '':
					if Readline[0] == '>':
						if Seq != '':  # saves the previous except on first round
							SeqRead = (SeqName, Seq)
							ReadFile.append(SeqRead)
							Seq = ''
						SeqName = Readline[1:]
					else:
						Seq += Readline
			SeqRead = (SeqName, Seq)  # must save last one at end
			ReadFile.append(SeqRead)

		# os.remove(workingfilename)
		# os.chdir(CurDir)

		# Returns a list of seqname and sequences, but now aligned
		return ReadFile

def MakeDivNT(class_name, line_name, data):
	div_name = 	'<div class="' + class_name + '">'
	div_name += '<span class="name">' + line_name + '<span class ="name_tip">' +  line_name + '</span></span>'
	div_name += '</div>'
	div_seq = '<div class="' + class_name + '">'
	count = 0
	for i in range(len(data)):
		if count == 0:
			div_seq += '<span class="unit_pack">'
		elif count%3 == 0:
			div_seq += '</span><span class="unit_pack">'
		div_seq += '<span class="unit">' + data[i] + '</span>'
		count += 1
	div_seq += '</span>'
	div_seq += '</div>'

	return div_name, div_seq

def MakeDivAA(class_name, line_name, data):
	div_name = '<div class="' + class_name + '">'
	div_name += '<span class="name">' + line_name + '<span class ="name_tip">' +  line_name + '</span></span>'
	div_name += '</div>'
	div_seq = '<div class="' + class_name + '">'
	for i in range(len(data)):
		div_seq += '<span class="unit_pack"><span class="insert">&nbsp;</span><span class="unit">' + data[i] + '</span><span class="insert">&nbsp;</span></span>'
	div_seq += '</div>'

	return div_name, div_seq

def MakeDivPosAA(class_name, line_name, tip_text, data):
	div_name = '<div class="' + class_name + '">'
	div_name += '<span class="name">' + line_name + '</span>'
	div_name += '</div>'
	div_seq = '<div class="' + class_name + '">'
	for i in range(len(data[0])):
		if data[0][i] != '-':
			if int(data[0][i]) % 5 == 0:
				div_seq += '<span class="unit_pack"><span class="insert">&nbsp;</span><span class="unit">' + str(data[0][i]) + \
				               '<span class ="unit_tip">' + tip_text + str(data[1][i]) + \
				               '</span></span><span class="insert">&nbsp;</span></span>'
			else:
				div_seq += '<span class="unit_pack"><span class="insert">&nbsp;</span><span class="unit">' + '.' + \
				               '<span class ="unit_tip">' + tip_text + str(data[1][i]) + \
				               '</span></span><span class="insert">&nbsp;</span></span>'
		else:
			div_seq += '<span class="unit_pack"><span class="insert">&nbsp;</span><span class="unit">' + str(data[0][i]) + \
			               '<span class ="unit_tip">' + tip_text + str(data[1][i]) + \
			               '</span></span><span class="insert">&nbsp;</span></span>'
	div_seq += '</div>'

	return div_name, div_seq

def MakeDivH1N3(class_name, line_name, tip_text, data):
	div_name = '<div class="' + class_name + '">'
	div_name += '<span class="name">' + line_name + '</span>'
	div_name += '</div>'
	div_seq = '<div class="' + class_name + '">'
	for i in range(len(data)):
		if data[i][2] == '':
			if data[i][0] != '-':
				if int(data[i][0]) % 5.0 == 0:
					div_seq += '<span class="unit_pack"><span class="insert">&nbsp;</span><span class="unit">' + str(data[i][0]) + \
					               '<span class ="unit_tip">' + tip_text + str(data[i][1]) + \
					               '</span></span><span class="insert">&nbsp;</span></span>'
				else:
					div_seq += '<span class="unit_pack"><span class="insert">&nbsp;</span><span class="unit">' + '.' + \
					               '<span class ="unit_tip">' + tip_text + str(data[i][1]) + \
					               '</span></span><span class="insert">&nbsp;</span></span>'
			else:
				div_seq += '<span class="unit_pack"><span class="insert">&nbsp;</span><span class="unit">' + str(data[i][0]) + \
				               '<span class ="unit_tip">' + tip_text + str(data[i][1]) + \
				               '</span></span><span class="insert">&nbsp;</span></span>'
		else:
			if data[i][0] != '-':
				if int(data[i][0]) % 5.0 == 0:
					div_seq += '<span class="unit_pack"><span class="insert ' + data[i][2] + '">&nbsp;</span><span class="unit ' + \
					               data[i][2] + '">' + str(data[i][0]) + \
					               '<span class ="unit_tip">' + tip_text + str(data[i][1]) + \
					               '</span></span><span class="insert ' + data[i][2] + '">&nbsp;</span></span>'
				else:
					div_seq += '<span class="unit_pack"><span class="insert ' + data[i][2] + '">&nbsp;</span><span class="unit ' + \
					               data[i][2] + '">' + '.' + \
					               '<span class ="unit_tip">' + tip_text + str(data[i][1]) + \
					               '</span></span><span class="insert ' + data[i][2] + '">&nbsp;</span></span>'
			else:
				div_seq += '<span class="unit_pack"><span class="insert ' + data[i][2] + '">&nbsp;</span><span class="unit ' + \
				               data[i][2] + '">' + str(data[i][0]) + \
				               '<span class ="unit_tip">' + tip_text + str(data[i][1]) + \
				               '</span></span><span class="insert ' + data[i][2] + '">&nbsp;</span></span>'
	div_seq += '</div>'

	return div_name, div_seq

def MakeDivPosNT(class_name, line_name, tip_text, data):
	div_name = '<div class="' + class_name + '">'
	div_name += '<span class="name">' + line_name + '</span>'
	div_name += '</div>'
	div_seq = '<div class="' + class_name + '">'
	count = 0
	for i in range(len(data[0])):
		if count == 0:
			div_seq += '<span class="unit_pack">'
			if data[0][i] % 5.0 == 0:
				div_seq += '<span class="unit">' + str(data[0][i]) + '<span class ="unit_tip">' + tip_text + \
				               str(data[1][i]) + ' - ' + str(int(data[1][i]) + 2) +  '</span></span>'
			else:
				div_seq += '<span class="unit">' + '.' + '<span class ="unit_tip">' + tip_text + str(data[1][i]) + \
				           ' - ' + str(int(data[1][i]) + 2) +  '</span></span>'
		elif count % 3 == 0:
			div_seq += '</span><span class="unit_pack">'
			if data[0][i] % 5.0 == 0:
				div_seq += '<span class="unit">' + str(data[0][i]) + '<span class ="unit_tip">' + tip_text + \
				               str(data[1][i])  + ' - ' + str(int(data[1][i]) + 2) +  '</span></span>'
			else:
				div_seq += '<span class="unit">' + '.' + '<span class ="unit_tip">' + tip_text + str(data[1][i]) + \
				           ' - ' + str(int(data[1][i]) + 2) +  '</span></span>'
		else:
			if data[0][i] % 5.0 == 0:
				div_seq += '<span class="unit">' + str(data[0][i]) + '</span>'
			else:
				div_seq += '<span class="unit">' + '.' + '</span>'
		count += 1
	div_seq += '</span>'
	div_seq += '</div>'
	return div_name, div_seq

def AlignSequencesHTML(DataSet):
	# import tempfile
	import os
	TupData = ()
	global GLMsg
	global working_prefix
	global clustal_path
	global temp_folder
	global VGenesTextWindows
	global muscle_path

	# align selected sequences (AA) using muscle
	all = dict()
	time_stamp = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime())
	outfilename = os.path.join(temp_folder, "out-" + time_stamp + ".fas")
	aafilename = os.path.join(temp_folder, "in-" + time_stamp + ".fas")
	if len(DataSet) == 1:
		SeqName = DataSet[0][0].replace('\n', '').replace('\r', '')
		SeqName = SeqName.strip()
		NTseq = DataSet[0][1]
		AAseq, ErMessage = LibratorSeq.Translator(NTseq, 0)
		all[SeqName] = [NTseq, AAseq]

		out_handle = open(outfilename,'w')
		out_handle.write('>' + SeqName + '\n')
		out_handle.write(AAseq)
		out_handle.close()
	else:
		aa_handle = open(aafilename,'w')
		for record in DataSet:
			SeqName = record[0].replace('\n', '').replace('\r', '')
			SeqName = SeqName.strip()
			NTseq = record[1]
			AAseq, ErMessage = LibratorSeq.Translator(NTseq, 0)
			AAseq = AAseq.replace('*','X').replace('~','Z').replace('.','J')
			all[SeqName] = [NTseq, AAseq]
			aa_handle.write('>' + SeqName + '\n')
			aa_handle.write(AAseq + '\n')
		aa_handle.close()

		cmd = muscle_path
		cmd += " -in " + aafilename + " -out " + outfilename
		try:
			os.system(cmd)
		except:
			QMessageBox.warning(self, 'Warning', 'Fail to run muscle! Check your muscle path!', QMessageBox.Ok,
			                    QMessageBox.Ok)
			return

	# read alignment file, make alignment NT and AA sequences
	SeqName = ''
	AAseq = ''
	if os.path.isfile(outfilename):
		currentfile = open(outfilename, 'r')
		lines = currentfile.readlines()
		for line in lines:
			Readline = line.replace('\n', '').replace('\r', '')
			Readline = Readline.strip()
			if Readline[0] == '>':
				if SeqName != '':
					AAseq, NTseq = BuildNTalignment(AAseq, all[SeqName][0])
					all[SeqName] = [NTseq, AAseq]
				SeqName = Readline[1:]
				AAseq = ''
			else:
				AAseq += Readline
		AAseq, NTseq = BuildNTalignment(AAseq, all[SeqName][0])
		all[SeqName] = [NTseq, AAseq]
	else:
		return

	if os.path.exists(outfilename):
		os.remove(outfilename)
	if os.path.exists(aafilename):
		os.remove(aafilename)

	# generate consnesus sequences (AA and NT)
	if len(all) == 1:
		for key in all:
			consensusDNA = all[key][0]
			consensusAA = all[key][1]
	else:
		firstOne = all[SeqName]
		seqlen = len(firstOne[0])

		consensusDNA = ''
		tester = ''
		for i in range(seqlen):
			tester = ''
			Cnuc = ''
			for key in all:
				seq = all[key][0]
				tester += seq[i]

			frequencies = [(c, tester.count(c)) for c in set(tester)]
			Cnuc = max(frequencies, key=lambda x: x[1])[0]
			consensusDNA += Cnuc

		consensusAA = ''
		firstOne = all[SeqName]
		seqlen = len(firstOne[1])
		for i in range(seqlen):
			tester = ''
			Caa = ''
			for key in all:
				seq = all[key][1]
				tester += seq[i]

			frequencies = [(c, tester.count(c)) for c in set(tester)]
			Caa = max(frequencies, key=lambda x: x[1])[0]
			consensusAA += Caa

	# align consensus AA sequence with template to generate H1 and H3 numbering
	compact_consensusAA = consensusAA.replace(' ', '')
	HANumbering(compact_consensusAA)

	# prepare H1 data
	pos_h1_data = []
	for i in range(1, len(H1Numbering) + 1):
		cur_data = H1Numbering[i]
		if cur_data[4] in ['Ca1','Ca2','Cb','Sa','Sb','Stalk-MN']:
			if cur_data[2] == '-':
				unit = (cur_data[2], cur_data[2], cur_data[4])
			else:
				if cur_data[0] == 'HA1':
					unit = (cur_data[2], 'HA1 ' + str(cur_data[2]), cur_data[4])
				else:
					unit = (cur_data[2], 'HA2 ' + str(cur_data[2]), cur_data[4])
		else:
			if cur_data[2] == '-':
				unit = (cur_data[2], cur_data[2], '')
			else:
				if cur_data[0] == 'HA1':
					unit = (cur_data[2], 'HA1 ' + str(cur_data[2]), '')
				else:
					unit = (cur_data[2], 'HA2 ' + str(cur_data[2]), '')
		pos_h1_data.append(unit)
	# prepare H3 data
	b = H3Numbering
	pos_h3_data = []
	for i in range(1, len(H3Numbering) + 1):
		cur_data = H3Numbering[i]
		if cur_data[4] in ['A','B','C','D','E','Stalk-MN']:
			if cur_data[2] == '-':
				unit = (cur_data[2], cur_data[2], cur_data[4])
			else:
				if cur_data[0] == 'HA1':
					unit = (cur_data[2], 'HA1 ' + str(cur_data[2]), cur_data[4])
				else:
					unit = (cur_data[2], 'HA2 ' + str(cur_data[2]), cur_data[4])
		else:
			if cur_data[2] == '-':
				unit = (cur_data[2], cur_data[2], '')
			else:
				if cur_data[0] == 'HA1':
					unit = (cur_data[2], 'HA1 ' + str(cur_data[2]), '')
				else:
					unit = (cur_data[2], 'HA2 ' + str(cur_data[2]), '')
		pos_h3_data.append(unit)

	# make header HTML
	pos_aa_data = [list(range(1,len(compact_consensusAA)+1)),list(range(1,len(compact_consensusAA)+1))]
	div_pos_aa = MakeDivPosAA('line line_pos_aa', 'Position AA:', 'Original AA position: ', pos_aa_data)
	div_h1 = MakeDivH1N3('line line_h1', 'H1 numbering', 'H1 numbering: ', pos_h1_data)
	div_h3 = MakeDivH1N3('line line_h3', 'H3 numbering', 'H3 numbering: ', pos_h3_data)
	div_con_aa = MakeDivAA('line con_aa', 'Consensus AA:', compact_consensusAA)
	pos_nt_data = [list(range(1, len(consensusDNA) + 1)), list(range(1, len(consensusDNA) + 1))]
	div_pos_nt = MakeDivPosNT('line line_pos_nt', 'Position NT:', 'Original NT position: ', pos_nt_data)
	div_con_nt = MakeDivNT('line con_nt', 'Consensus NT:', consensusDNA)

	# initial and open HTML file
	time_stamp = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime())
	out_html_file = os.path.join(temp_folder, time_stamp + '.html')
	header_file = os.path.join(working_prefix, '..', 'Resources', 'Data', 'template.html')
	shutil.copyfile(header_file, out_html_file)
	out_file_handle = open(out_html_file, 'a')

	name_div = '<div class="name_div">\n'
	seq_div = '<div class = "seq_div">\n'
	# write header section
	name_div += div_pos_aa[0] + '\n'
	seq_div += div_pos_aa[1] + '\n'
	name_div += div_h1[0] + '\n'
	seq_div += div_h1[1] + '\n'
	name_div += div_h3[0] + '\n'
	seq_div += div_h3[1] + '\n'
	name_div += div_con_aa[0] + '\n'
	seq_div += div_con_aa[1] + '\n'
	name_div += div_pos_nt[0] + '\n'
	seq_div += div_pos_nt[1] + '\n'
	name_div += div_con_nt[0] + '\n'
	seq_div += div_con_nt[1] + '\n'
	# make sequence section HTML
	for key in all:
		seq_nt = all[key][0]
		seq_aa = all[key][1]
		con_nt = MakeConSeq(seq_nt, consensusDNA)
		con_aa = MakeConSeq(seq_aa, compact_consensusAA)

		div_aa = MakeDivAA('line line_aa', key, seq_aa)
		div_aa_mut = MakeDivAA('line line_con_aa', key, con_aa)
		div_nt = MakeDivNT('line line_nt', key, seq_nt)
		div_nt_mut = MakeDivNT('line line_con_nt', key, con_nt)
		# write sequence section
		name_div += div_aa[0] + '\n'
		seq_div += div_aa[1] + '\n'
		name_div += div_aa_mut[0] + '\n'
		seq_div += div_aa_mut[1] + '\n'
		name_div += div_nt[0] + '\n'
		seq_div += div_nt[1] + '\n'
		name_div += div_nt_mut[0] + '\n'
		seq_div += div_nt_mut[1] + '\n'

	name_div += '</div>\n'
	seq_div += '</div>\n'
	out_file_handle.write(name_div)
	out_file_handle.write(seq_div)
	out_file_handle.write('\n</div>\n</body>\n</html>')
	out_file_handle.close()
	return out_html_file

def MakeConSeq(seq, con):
	for i in range(len(seq)):
		if seq[i] == con[i]:
			seq = seq[:i] + '.' + seq[i+1:]
	return seq

def BuildNTalignment(aa, nt):
	pos = 0
	new_nt = ''
	for i in range(len(aa)):
		cur_aa = aa[i]
		if cur_aa == '-':
			new_nt += '---'
		elif cur_aa == 'X':
			new_nt += nt[pos:pos + 3]
			aa = aa[:i] + '*' + aa[i+1:]
			pos = pos + 3
		elif cur_aa == 'Z':
			new_nt += nt[pos:] + '-'*(3 - len(nt[pos:]))
			aa = aa[:i] + '~' + aa[i + 1:]
			pos = pos + 3
		elif cur_aa == 'J':
			new_nt += nt[pos:pos + 3]
			pos = pos + 3
		else:
			new_nt += nt[pos:pos + 3]
			pos = pos + 3
	a = 1
	return aa, new_nt

def SequenceCheck(sequence, type):
	Msg = 'none'
	if type == 'aa':
		pattern = re.compile(r'[^ILVFMCAGPTSYWQNHEDKR]')
	else:
		pattern = re.compile(r'[^ATCUG]')

	strange_residues = re.findall(pattern, sequence)

	if len(strange_residues) > 0:
		Msg = ','.join(strange_residues)

	return Msg

def Translator(Sequence, frame):
        # Translate sequence into a list of codons
    CodonList = [ ]
    for x in range(frame, len(Sequence), 3):
            CodonList.append(Sequence[x:x+3])
    # For each codon, translate it into amino acid, and create a list
    ProteinSeq = [ ]
    for codon in CodonList:
        if codon in CodonDict:
            ProteinSeq.append(CodonDict[codon])
        else:
            ProteinSeq.append('~')

    AASeq = ''.join(ProteinSeq)

    # print("Translated in frame %d: %s (%.1f Da)" % ((frame+1), ''.join(ProteinSeq), sum(ProteinWeight)))
    # Check position of stop codon, making sure it's at the end, and the only one
    XCount = 0
    UCount = 0
    for acid in ProteinSeq:
        if acid == "*":
            XCount += 1
    for acid in ProteinSeq:
        if acid == "~":
            UCount += 1
    ErMessage = []
    # ErMessage.append()
    if XCount > 0:
        if XCount == 1:
            ErMes =  'WARNING: '+ str(XCount) + ' stop codon was found (marked as "*")!'
        else:
            ErMes =  'WARNING: '+ str(XCount) + ' stop codons found (marked as "*")!'
        ErMessage.append(ErMes)
    if UCount > 0:
        # todo this doesn't label errors properly
        AASeq2 = AASeq.replace ('.', '')
        ErMes = 'Codon errors (marked as "~"): '
        if len(Sequence) % 3 != 0 and UCount == 1:
            ErMes += 'Incomplete codon at end.'
            ErMessage.append(ErMes)
            return AASeq, ErMessage

        elif UCount == 1:

            if AASeq2[0] == '~':
                ErMes += 'The first codon is incomplete.'
                ErMessage.append(ErMes)
                return AASeq, ErMessage

            else:
                ErMes += '1 codon error internally.'
                ErMessage.append(ErMes)
                return AASeq, ErMessage

        elif UCount > 1:


            if AASeq2[0] == '~':
                ErMes += 'The first codon is incomplete. '
                ErMessage.append(ErMes)
                UCount -= 1

            if len(Sequence) % 3 != 0:
                if UCount > 1:
                    ErMes += '1 incomplete on end and '
                    if UCount-1 > 1:
                        ErMes += str(UCount-1) + ' others with errors internally.'
                    elif UCount - 1 == 1:
                        ErMes += '1 other with errors internally.'
                else:
                    ErMes += '1 incomplete on end.'

            else:
                ErMes += str(UCount) + ' errors within the sequence.'
        ErMessage.append(ErMes)

    return AASeq, ErMessage
# AminoDict={'A':89.09,   'R':174.20, 'N':132.12, 'D':133.10, 'C':121.15,
# 'Q':146.15, 'E':147.13, 'G':75.07,  'H':155.16, 'I':131.17, 'L':131.17,
# 'K':146.19, 'M':149.21, 'F':165.19, 'P':115.13, 'S':105.09, 'T':119.12,
# 'W':204.23, 'Y':181.19, 'V':117.15, 'X':0.0,    '-':0.0,    '*':0.0,
# '?':0.0}

global Group1, Group2, GroupNA
Group1 = ['H1','H2','H5','H6','H8','H9','H11','H12','H13','H16','H17','H18']
Group2 = ['H3','H4','H7','H10','H14','H15']
GroupNA = ['N1','N2','N3','N4','N5','N6','N7','N8','N9','N10','N11']

def subtype_switch(subtype):
    subtypes = {
	    'H1': 0,
	    'H2': 1,
	    'H3': 2,
	    'H4': 3,
	    'H5': 4,
	    'H6': 5,
	    'H7': 6,
	    'H8': 7,
	    'H9': 8,
	    'H10': 9,
	    'H11': 10,
	    'H12': 11,
	    'H13': 12,
	    'H14': 13,
	    'H15': 14,
	    'H16': 15,
	    'H17': 16,
	    'H18': 17,
	    'N1': 18,
	    'N2': 19,
	    'N3': 20,
	    'N4': 21,
	    'N5': 22,
	    'N6': 23,
	    'N7': 24,
	    'N8': 25,
	    'N9': 26,
	    'N10': 27,
	    'N11': 28,
	    'B': 29,
	    'Other': 30
    }
    value = subtypes.get(subtype, 30)
    return value

global H3template
global H3template_seq
global H3_start
global H3_end
H3template = "A/Aichi/2/1968|H3N2"
H3template_seq = "MKTIIALSYIFCLAIGQDLPGNDNSTATLCLGHHAVPNGTLVKTITDDQIEVTNATELVQSSSTGKICNNPHRILDGIDCT" \
                 "LIDALLGDPHCDVFQNETWDLFVERSKAFSNCYPYDVPDYASLRSLVASSGTLEFITEGFTWTGVTQNGGSNACKRGPSSG" \
                 "FFSRLNWLTKSGSTYPVLNVTMPNNDNFDKLYIWGVHHPSTNQEQTSLYVQASGRVTVSTRRSQQTIIPNIGSRPWVGGLS" \
                 "SRISIYWTIVKPGDVLVINSNGNLIAPRGYFKMRTGKSSIMRSDAPIDTCISECITPNGSIPNDKPFQNVNKITYGACPKY" \
                 "VKQNTLKLATGMRNVPEKQTRGLFGAIAGFIENGWEGMIDGWYGFRHQNSEGTGQAADLKSTQAAIDQINGKLNRVIEKTN" \
                 "EKFHQIEKEFSEVEGRIQDLEKYVEDTKIDLWSYNAELLVALENQHTIDLTDSEMNKLFEKTRRQLRENAEDMGNGCFKIY" \
                 "HKCDNACIESIRNGTYDHDVYRDEALNNRFQIKGVELKSGYKDWILWISFAISCFLLCVVLLGFIMWACQRGNIRCNICI"

H3_start = [1, 123, 264, 403];
H3_end = [131, 272, 411, 520];

global H1template
global H1template_seq
global H1_start
global H1_end
H1template = "A/California/04/2009|H1N1"
H1template_seq = "MKAILVVLLYTFATANADTLCIGYHANNSTDTVDTVLEKNVTVTHSVNLLEDKHNGKLCKLRGVAPLHLGKCNIAGWILGN" \
                 "PECESLSTASSWSYIVETPSSDNGTCYPGDFIDYEELREQLSSVSSFERFEIFPKTSSWPNHDSNKGVTAACPHAGAKSFY" \
                 "KNLIWLVKKGNSYPKLSKSYINDKGKEVLVLWGIHHPSTSADQQSLYQNADTYVFVGSSRYSKKFKPEIAIRPKVRDQEGR" \
                 "MNYYWTLVEPGDKITFEATGNLVVPRYAFAMERNAGSGIIISDTPVHDCNTTCQTPKGAINTSLPFQNIHPITIGKCPKYV" \
                 "KSTKLRLATGLRNIPSIQSRGLFGAIAGFIEGGWTGMVDGWYGYHHQNEQGSGYAADLKSTQNAIDEITNKVNSVIEKMNT" \
                 "QFTAVGKEFNHLEKRIENLNKKVDDGFLDIWTYNAELLVLLENERTLDYHDSNVKNLYEKVRSQLKNNAKEIGNGCFEFYH" \
                 "KCDNTCMESVKNGTYDYPKYSEEAKLNREEIDGVKLESTRIYQILAIYSTVASSLVLVVSLGAISFWMCSNGSLQCRICI"
H1_start = [1, 123, 264, 403];
H1_end = [131, 272, 411, 518];

# NA part need more discussion
global NAtemplate_name
global NAtemplate_seq
global NA_start
global NA_end
NAtemplate_name = {
	'N1':'A/California/04/2009|QEH91764|N1',
	'N2':'A/Texas/08/2019|QBP39026|N2',
	'N3':'A/mallard/Maryland/13OS3019/2014|AKF18550|N3',
	'N4':'A/mallard/Utah/AH0020452/2015|AQS26331|N4',
	'N5':'A/commonredshank/Singapore/F83-1/2015|ALR83194|N5',
	'N6':'A/duck/Guangdong/G1345/2014|AJS16549|N6',
	'N7':'A/mallard/Sweden/124987/2010|AHZ37263|N7',
	'N8':'A/northernpintail/Alaska/UGAI15-7291/2015|AOX49352|N8',
	'N9':'A/green-winged-teal/Ohio/14OS1103/2014|AMQ30738|N9',
	'N10':'A/little-yellow-shouldered-bat/Guatemala/060/2010|EPI_ISL_105896|N10',
	'N11':'A/flat-faced-bat/Peru/033/2010|AGX84936|N11'
	}

NAtemplate_seq = {
	'N1':'MNPNQKIITIGSVCMTIGMANLILQIGNIISIWISHSIQLGNQNQIETCNQSVITYENNTWVNQTYVNISNTNFAAGQSVVSVKLAGNSSLCPVSGWAIYSKDNSVRIGSKGDVFVIREPFISCSPLECRTFFLTQGALLNDKHSNGTIKDRSPYRTLMSCPIGEVPSPYNSRFESVAWSASACHDGINWLTIGISGPDNGAVAVLKYNGIITDTIKSWRNNILRTQESECACVNGSCFTVMTDGPSNGQASYKIFRIEKGKIVKSVEMNAPNYHYEECSCYPDSSEITCVCRDNWHGSNRPWVSFNQNLEYQIGYICSGIFGDNPRPNDKTGSCGPVSSNGANGVKGFSFKYGNGVWIGRTKSISSRNGFEMIWDPNGWTGTDNNFSIKQDIVGINEWSGYSGSFVQHPELTGLDCIRPCFWVELIRGRPKENTIWTSGSSISFCGVNSDTVGWSWPDGAELPFTIDK',
	'N2':'MNPNQKIITIGSVSLTISTICFFMQIAILITTVTLHFKQYEFNSPPNNQVMLCEPTIIERNITEIVYLTNTTIEREICPKPAEYRNWSKPQCSITGFAPFSKDNSIRLSAGGDIWVTREPYVSCDPDKCYQFALGQGTTINNVHSNNTARDRTPHRTLLMSELGVPFHLGTKQVCIAWSSSSCHDGKAWLHVCITGDDKNATASFIYNGRLVDSVVSWSKDILRTQESECVCINGTCTVVMTDGNATGKADTKILFIEEGKIVHTSKLSGSAQHVEECSCYPRYPGVRCVCRDNWKGSNRPIVDINIKDHSIVSSYVCSGLVGDTPRKTDSSSSSHCLNPNNEKGGHGVKGWAFDEGNDVWMGRTINETSRLGYETFKVVEGWSNSKSKLQINRQVIVDRGDRSGYSGIFSVEGKSCINRCFYVELIRGRKEETEVLWTSNSIVVFCGTSGTYGTGSWPDGADLNLMHI',
	'N3':'MNPNQKIITIGVVNTTLSTIALLIGVGNLVFNTVIHEKIGDHQTVTHPTITTPAIPNCSDTIITYNNTVINNITTTIITEAERPFKSPLPLCPFRGFFPFHKDNAIRLGENKDVIVTREPYISCDDDNCWSFALAQGALLGTKHSNGTIKDRTPYRSLIRFPIGTAPVLGNYKEICIAWSSSSCFDGKEWMHVCMTGNDNDASAQIIYAGRMTDSIKSWRRDILRTQESECQCIDGTCVVAVTDGPAANSADHRVYWIREGKIIKYEDVPKTKIQHLEECSCYVDIDVYCICRDNWKGSNRPWMRINNETILETGYVCSKFHSDTPRPADPSTMSCDSPSNINGGPGVKGFGFKAGNDVWLGRTVSTSGRSGFEIIKVTEGWINSPNHAKSITQTLVSNNDWSGYSGSFIVKTKDCFQPCFYVELIRGRPNKNDDVSWTSNSIVTFCGLDNEPGSGNWPDGSNIGFMPK',
	'N4':'MNPNQKIITIGSVSIILTTVGLLLQITSLCSIWFSHYNQVTQTHEQPCSNNTTNYYNETFVNVTNVQNNYTTIAEPSAPDVIHYSSGRDLCPIRGWAPLSKDNGIRIGSRGEVFVIREPFISCSISECRTFFLTQGALLNDKHSNGTVKDRSPFRTLMSCPIGVAPSPSNSRFESVAWSATACSDGPGWLTLGITGPDSTAVAVLKYNGIITDTLKSWKGNIMRTQESECVCQDEFCYTLITDGPSNAQAFYKILKIRKGKIVSMKDVDATGFHFEECSCYPSGTEIECVCRDNWQGSNRPWIRFNSDLDYQIGYVCSGIFGDNPRPVDGTGSCNGPVNNGKGRYGVKGFSFRYGDGVWIGRTKSLESRSGFEMVWDANGWVSTDKDSNGVQDIIDNDNWSGYSGSFSIRGETTGKNCTVPCFWVEMIRGQPKEKTIWTSGSSIAFCGVNSDTTGWSWPDGALLPFDIDK',
	'N5':'MNPNQKIITIGSISLGLVVFNILLHVASIVLGIISVTKDHEAYTCNTTEVYNETVRVETVTIPVNNTIYIERELTHEPEFLNNTEPLCEVSGFAIVSKDNGIRIGSRGHVFVIREPFVACGPSECRTFFLTQGALLNDKHSNNTVKDRSPYRALMSVPLGSSPNAYQAKFESVGWSATACHDGKEWMAIGVSGADDDAYAVIHYGGIPTDVVRSWRKQILRTQESSCVCMKGECYWVMTDGPANNQASYKIFKSQKGLVVDEKEISFQGGHIEECSCYPNMGKVECVCRDNWNGMNRPILTFDENLEYEVGYLCAGIPTDTPRVQDSSFTGSCTNAVGGSGTNNYGVKGFGFRQGTSVWAGRTISTSSRSGFEVLLIEDGWIRPSKTISKKVEVLNNKNWSGYSGSFTIPTAMTSKSCLVPCFWLEMIRGKPEERTSIWTSSSSTVFCGVSSEVPGWSWDDGAILPFDIDKM',
	'N6':'MNPNQKITCISATGMTLSVVSLLIGVANLGLNIGLHYKVSDSSNINIPNMNETNPTTTIINNNPQNNFTNITNIIVNKNEEGKFLNLTKPLCEVNSWHILSKDNAIRIGEDAHILVTREPYLSCDPQGCRMFAMSQGTTLRGRHANGTIHDRSPFRALINWEMGQAPSPYNARVECIGWSSTSCHDGMSRMSICISGPNNNASAVVWYGGRPVTEIPSWAGNILRTQESECVCHKGICPVVMTDGPANNRAATKIIYFKEGKIQKIEELKGNAQHIEECSCYGAAGMIKCICRDNCKGANRPVITLDPEMMTHTSKYLCSKILTDTSRPNDPTSGNCDAPITGGSPDPGVKGFAFLDGENSWLGRTISKDSRSGYEMLKVPNAETDTQSGPISYQTIVNNQNWSGYSGAFIDYWANKECFNPCFYVELIRGRPKESSVLWTSNSIVALCGSRERLGSWSWHDGAEIIYFK',
	'N7':'MNPNQKLFALSGVAIALSILNLLIGISNVGLNVSLHLREKGTKQEENLTCTTITQNNTTVVENTYVNNTTIITKETDLETPSYLLLNKSLCNVEGWVVIAKDNAVRFGESEQIIVTREPYVSCDPTGCKMYALHQGTTIRNKHSNGTIHDRTAFRGLISTPLGTPPTVSNSDFICVGWSSTTCHDGVGRMTICIQGNNDNATATVYYNRRLTTTIKTWARNILRTQESECVCHNGTCAVVMTDGSASSQAYTKIMYFHKGLVVKEEALKGSARHIEECSCYGHSQKATCVCRDNWQGANRPIIEIDMNTLEHTSRYVCTGILTDTSRPGDKSSGDCSNPITGSPGAPGVKGFGFLNGDNTWLGRTISPRSRSGFEMLKIPNAGTDPNSRIAERQEIVDNNNWSGYSGSFIDYWNDNSECYNPCFYVELIRGRPEEAKYVWWTSNSLIALCGSPFPVGSGSFPDGAQIQYFS',
	'N8':'MNPNQKIITIGSISLGLVVLNILLHIVSITVTVLVLPGNGSNGNCSETVIREYNETVRVEKVTQWHNTSVIEYVERPENDHFMNNTEALCDAKGFAPFSKDNGIRIGSRGHVFVIREPFVSCSPTECRTFFLTQGSLLNDKHSNGTVKDRSPYRTLMSVEIGQSPNVYQARFEAVAWSATACHDGKKWMTIGVTGPDAKAMAVVHYGGIPTDVINSWAGDILRTQESSCTCIQGECFWVMTDGPANRQAQYRAFKAKQGKVVGQAEISFNGGHIEECSCYPNEGKVECVCRDNWTGTNRPVLVISPDLSYRVGYLCAGLPSDTPRGEDSQFTGSCTSPMGNQGYGVKGFGFRQGNDVWMGRTISRTSRSGFEILKVRNGWVQNSKEQIKRQVVVDNLNWSGYSGSFTLPVELTKRNCLVPCFWVEMIRGKPEEKTIWTSSSSIVMCGVDHEIADWSWHDGAILPFDIDKM',
	'N9':'MNPNQKILCTSATAIVIGIIAVLIGIANLGLNIGLHLKPNCNCSHSQPEATNASQTIINNYYNETNITQISNTNIQMEEKAGREFNNLTKGLCTINSWHIYGKDNAVRIGEDSDVLVTREPYVSCDPDECRFYALSQGTTIRGKHSNGTIHDRSQYRALISWPLSSPPTVYNSRVECIGWSSTSCHDGRARMSICISGPNNNASAVIWYNRRPITEINTWARNILRTQESECVCHNGVCPVVFTDGSATGPAETRVYYFKEGKILKWESLTGTAKHIEECSCYGEQAGITCTCRDNWQGSNRPVIQIDPVAMTHTSQYICSPVLTDNPRPNDPTVGKCNDPYPGNNNNGVKGFSYLDGGNTWLGRTISTASRSGYEMLKVPNALTDDRSKPTQGQTIVLNTDWSGYSGSFMDYWAEGECYRACFYIELIRGRPKEDKVWWTSNSIVSMCSSTEFLGQWNWPDGAEIEYFL',
	'N10':'MSINGTTCLLTLSLILNIVMIGLQVLMPFVLLWTNSPPPEIYNSTSCCNGTFLNETNNNITNISQITNNFLKEEKFYWKARSQMCEVKGWVPTHRGFPWGPELPGDLILSRRAYVSCDLTSCFKFFIAYGLSANQHLLNTSMEWEESLYKTPIGSANTLSTSEMILPGRSSSACFDGLKWTVLVSNGRDRNSFIMIKYGEEITDTFSASRGGPLRLPNSECICVEGSCFVLVSDGPNVNQSVHRIYELQNGTVQRWKQLNTTGINFEYSTCYTINNLIKCTGTNLWNDAKRPLLRFTKDLNYQIVEPCNGAPTDFPRGGLTTPSCKMAQEKGEGGIQGFILDEKPAWTSKTKTELSQNGFVLEQIPDGIESEGTVSLSYELFSNKRTGRSGFFQPKGDLISECQRVCFWLEIEDQTVGLGMIQELSTFCGINSPVQNINWDS',
	'N11':'MSFQTSTCLLIVSLICGILTVCLQVLLPFILIWTNTEPNYSCECPAPNISLSCPNGTSVTYDSKNITENSFYSSTTNYLSPVIATPLVLGENLCSINGWVPTYRGEGTTGKIPDEQMLTRQNFVSCSDKECRRFFVSMGYGTTTNFADLIVSEQMNVYSVKLGDPPTPDKLKFEAVGWSASSCHDGFQWTVLSVAGDGFVSILYGGIITDTIHPTNGGPLRTQASSCICNDGTCYTIIADGTTYTASSHRLYRLVNGTSAGWKALDTTGFNFEFPTCYYTSGKVKCTGTNLWNDAKRPFLEFDQSFTYTFKEPCLGFLGDTPRGIDTTNYCDKTTTEGEGGIQGFMIEGSNSWIGRIINPGSKKGFEIYKFLGTLFSVQTVGNRNYQLLSNSTIGRSGLYQPAYESRDCQELCFWIEIAATTKAGLSSNDLITFCGTGGSMPDVNWG'
	}


NA_start = [1, 131, 292];
NA_end = [139, 301, 468];

# SETUP user defined joint regions
global H3_start_user, H3_end_user, H1_start_user, H1_end_user, NA_end_user, NA_start_user
H3_start_user = []
H3_end_user = []
H1_start_user = []
H1_end_user = []
NA_end_user = []
NA_start_user = []

global H1_Gibson_file, H3_Gibson_file, NA_Gibson_file
H1_Gibson_file = os.path.join(working_prefix, '..', 'Resources', 'Conf','H1_Gibson.txt')
H3_Gibson_file = os.path.join(working_prefix, '..', 'Resources', 'Conf','H3_Gibson.txt')
NA_Gibson_file = os.path.join(working_prefix, '..', 'Resources', 'Conf','NA_Gibson.txt')

if os.path.exists(H1_Gibson_file):
	file_handle = open(H1_Gibson_file, 'r')
	configure = file_handle.read()
	configure = configure.split('\n')
	tmp_start = configure[0].split(',')
	H1_start_user = list(map(int, tmp_start))
	tmp_end = configure[1].split(',')
	H1_end_user = list(map(int, tmp_end))

if os.path.exists(H3_Gibson_file):
	file_handle = open(H3_Gibson_file, 'r')
	configure = file_handle.read()
	configure = configure.split('\n')
	tmp_start = configure[0].split(',')
	H3_start_user = list(map(int, tmp_start))
	tmp_end = configure[1].split(',')
	H3_end_user = list(map(int, tmp_end))

if os.path.exists(NA_Gibson_file):
	file_handle = open(NA_Gibson_file, 'r')
	configure = file_handle.read()
	configure = configure.split('\n')
	tmp_start = configure[0].split(',')
	NA_start_user = list(map(int, tmp_start))
	tmp_end = configure[1].split(',')
	NA_end_user = list(map(int, tmp_end))


CodonDict={'ATT':'I',   'ATC':'I',  'ATA':'I',  'CTT':'L',  'CTC':'L',
'CTA':'L',  'CTG':'L',  'TTA':'L',  'TTG':'L',  'GTT':'V',  'GTC':'V',
'GTA':'V',  'GTG':'V',  'TTT':'F',  'TTC':'F',  'ATG':'M',  'TGT':'C',
'TGC':'C',  'GCT':'A',  'GCC':'A',  'GCA':'A',  'GCG':'A',  'GGT':'G',
'GGC':'G',  'GGA':'G',  'GGG':'G',  'CCT':'P',  'CCC':'P',  'CCA':'P',
'CCG':'P',  'ACT':'T',  'ACC':'T',  'ACA':'T',  'ACG':'T',  'TCT':'S',
'TCC':'S',  'TCA':'S',  'TCG':'S',  'AGT':'S',  'AGC':'S',  'TAT':'Y',
'TAC':'Y',  'TGG':'W',  'CAA':'Q',  'CAG':'Q',  'AAT':'N',  'AAC':'N',
'CAT':'H',  'CAC':'H',  'GAA':'E',  'GAG':'E',  'GAT':'D',  'GAC':'D',
'AAA':'K',  'AAG':'K',  'CGT':'R',  'CGC':'R',  'CGA':'R',  'CGG':'R',
'AGA':'R',  'AGG':'R',  'TAA':'*',  'TAG':'*',  'TGA':'*',  '...':'.',
'NNN':'.'}


AACodonDict={'I':'ATT','L':'CTT','V':'GTT','F':'TTT','M':'ATG','C':'TGT',
			 'A':'GCT','G':'GGT','P':'CCT','T':'ACT','S':'TCT','Y':'TAT',
			 'W':'TGG','Q':'CAA','N':'AAT','H':'CAT','E':'GAA','D':'GAT',
			 'K':'AAA','R':'CGT'}


H1HA1Regions = {'1':'Stalk', '2':'Stalk', '3':'Stalk', '4':'Stalk', '5':'Stalk', '6':'Stalk', '7':'Stalk',
				'8':'Stalk', '9':'Stalk', '10':'Stalk', '11':'Stalk', '12':'Stalk-MN',
				'13':'Stalk', '14':'Stalk', '15':'Stalk', '16':'Stalk', '17':'Stalk', '18':'Stalk', '19':'Stalk',
				'20':'Stalk', '21':'Stalk', '22':'Stalk', '23':'Stalk', '24':'Stalk', '25':'Stalk', '26':'Stalk',
				'27':'Stalk', '28':'Stalk', '29':'Stalk', '30':'Stalk', '31':'Stalk', '32':'Stalk', '33':'Stalk',
				'34':'Stalk-MN', '35':'Stalk-MN', '36':'Stalk-MN', '37':'Stalk-MN', '38':'Stalk-MN', '39':'Stalk',
				'40':'Stalk','41':'Stalk', '42':'Stalk', '43':'Stalk', '44':'Stalk', '45':'Stalk', '46':'Stalk',
				'47':'Stalk', '48':'Head', '49':'Head', '50':'Head', '51':'Head', '52':'Head', '53':'Head',
				'54':'Head', '55':'Head', '56':'Head', '57':'Head', '58':'Head', '59':'Head', '60':'Head',
				'61':'Head', '62':'Head', '63':'Head', '64':'Head', '65':'Head', '66':'Head', '67':'Head', '68':'Head',
				'69':'Head', '70':'Head', '71':'Head', '72':'Head', '73':'Head', '74':'Head', '75':'Head',
				'76':'Cb', '77':'Cb', '78':'Cb', '79':'Cb', '80':'Cb',  '81':'Cb', '82':'Head', '83':'Head',
				'84':'Head', '85':'Head', '86':'Head', '87':'Head', '88':'Head', '89':'Head', '90':'Head',
				'91':'Head', '92':'Head', '93':'Head', '94':'Head', '95':'Head', '96':'Head', '97':'Head',
				'98':'Head', '99':'Head', '100':'Head', '101':'Head', '102':'Head', '103':'Head', '104':'Head',
				'105':'Head', '106':'Head', '107':'Head', '108':'Head', '109':'Head', '110':'Head', '111':'Head',
				'112':'Head', '113':'Head', '114':'Head', '115':'Head', '116':'Head', '117':'Head', '118':'Head',
				'119':'Head', '120':'Head', '121':'Head', '122':'Head', '123':'Head', '124':'Head', '125':'Head',
				'126':'Head', '127':'Head', '128':'Head', '129':'Head', '130':'Sa', '131':'Sa', '132':'Head',
				'133':'Head', '134':'Head', '135':'Head', '136':'Head', '137':'Head', '138':'Head', '139':'Head',
				'140':'Head', '141':'Head', '142':'Ca1', '143':'Ca1', '144':'Ca1','145':'Ca1', '146':'Ca1',
				'147':'Ca1', '148':'Head', '149':'Head', '150':'Head', '151':'Head', '152':'Head', '153':'Head',
				'154':'Head', '155':'Head', '156':'Head', '157':'Head', '158':'Head','159':'Sa', '160':'Sa',
				'161':'Sa', '162':'Sa', '163':'Sa', '164':'Head', '165':'Sa', '166':'Sa', '167':'Sa', '168':'Sa',
				'169':'Sa', '170':'Sa', '172':'Ca1', '173':'Ca1', '174':'Ca1', '175':'Ca1', '176':'Ca1',
				'177':'Head', '178':'Head', '179':'Head', '180':'Head', '181':'Head', '182':'Head', '183':'Head',
				'184':'Head', '185':'Head', '186':'Head', '187':'Head', '188':'Head', '189':'Head', '190':'Sb',
				'191':'Sb', '192':'Sb', '193':'Sb', '194':'Sb', '195':'Sb', '196':'Sb', '197':'Sb', '198':'Sb',
				'199':'Sb', '200':'Sb', '201':'Head', '202':'Head', '203':'Head', '204':'Head', '205':'Head',
				'206':'Head', '207':'Head', '208':'Head', '209':'Ca1', '210':'Ca1', '211':'Ca1', '212':'Head',
				'213':'Head', '214':'Head', '215':'Head', '216':'Head', '217':'Head', '218':'Head', '219':'Head',
				'220':'Head', '221':'Head', '222':'Head', '223':'Head', '224':'Head', '225':'Head', '226':'Head',
				'227':'Ca2', '228':'Ca2', '229':'Ca2','230':'Head', '231':'Head', '232':'Head', '233':'Head',
				'234': 'Head', '235': 'Head', '236': 'Head', '237': 'Head', '238': 'Head', '239': 'Head', '240': 'Head',
				'241': 'Head', '242': 'Head', '243': 'Head', '244': 'Head', '245': 'Head', '246': 'Head', '247': 'Head',
				'248': 'Head', '249': 'Head', '250': 'Head', '251': 'Head', '252': 'Head', '253': 'Head', '254': 'Head',
				'255': 'Head', '256': 'Head', '257': 'Head', '258': 'Head', '259': 'Head', '260': 'Head', '261': 'Head',
				'262': 'Head', '263': 'Head', '264': 'Head', '265': 'Head', '266': 'Head', '267': 'Head', '268': 'Head',
				'269': 'Head', '270': 'Head', '271': 'Head', '272': 'Head', '273': 'Head', '274': 'Head', '275': 'Head',
				'276': 'Head', '277': 'Head', '278': 'Head', '279': 'Head', '280': 'Head', '281':'Head', '282':'Stalk',
				'283':'Stalk', '284':'Stalk', '285':'Stalk', '286':'Stalk', '287':'Stalk', '288':'Stalk',
				'289':'Stalk',  '290':'Stalk', '291':'Stalk', '292':'Stalk', '293':'Stalk', '294':'Stalk',
				'295':'Stalk-MN', '296':'Stalk-MN', '297':'Stalk-MN', '298':'Stalk', '299':'Stalk', '300':'Stalk',
				'301':'Stalk',  '302':'Stalk', '303':'Stalk', '304':'Stalk', '305':'Stalk', '306':'Stalk','307':'Stalk',
				'308':'Stalk', '309':'Stalk', '310':'Stalk', '311':'Stalk', '312':'Stalk','313':'Stalk',  '314':'Stalk',
				'315':'Stalk', '316':'Stalk', '317':'Stalk', '318':'Stalk', '319':'Stalk', '320':'Stalk', '321':'Stalk',
				'322':'Stalk-MN', '323':'Stalk-MN','324':'Stalk-MN', '325':'Stalk', '326':'Stalk', '327':'Stalk',
				'328':'Stalk', '329':'Stalk', '330':'Stalk', '331':'Stalk', '332':'Stalk', '333':'Stalk'}

# H1 numbering
H1HA2Regions = {'1':'Stalk', '2':'Stalk', '3':'Stalk', '4':'Stalk', '5':'Stalk', '6':'Stalk', '7':'Stalk',
				'8':'Stalk', '9':'Stalk', '10':'Stalk', '11':'Stalk', '12':'Stalk', '13':'Stalk', '14':'Stalk',
				'15':'Stalk', '16':'Stalk', '17':'Stalk', '18':'Stalk-MN', '19':'Stalk-MN', '20':'Stalk-MN',
				'21':'Stalk-MN', '22':'Stalk', '23':'Stalk', '24':'Stalk', '25':'Stalk', '26':'Stalk',
				'27':'Stalk', '28':'Stalk', '29':'Stalk', '30':'Stalk', '31':'Stalk', '32':'Stalk', '33':'Stalk',
				'34':'Stalk', '35':'Stalk', '36':'Stalk-MN', '37':'Stalk', '38':'Stalk-MN', '39':'Stalk',
				'40':'Stalk', '41':'Stalk-MN', '42':'Stalk-MN', '43':'Stalk', '44':'Stalk', '45':'Stalk-MN',
				'46':'Stalk-MN', '47':'Stalk', '48':'Stalk-MN', '49':'Stalk-MN', '50':'Stalk', '51':'Stalk',
				'52':'Stalk-MN', '53':'Stalk-MN', '54':'Stalk', '55':'Stalk', '56':'Stalk-MN', '57':'Stalk',
				'58':'Stalk', '59':'Stalk', '60':'Stalk', '61':'Stalk', '62':'Stalk', '63':'Stalk', '64':'Stalk',
				'65':'Stalk', '66':'Stalk', '67':'Stalk', '68':'Stalk', '69':'Stalk', '70':'Stalk','71':'Stalk',
				'72':'Stalk', '73':'Stalk', '74':'Stalk', '75':'Stalk', '76':'Stalk','77':'Stalk', '78':'Stalk',
				'79':'Stalk', '80':'Stalk', '81':'Stalk', '82':'Stalk','83':'Stalk', '84':'Stalk', '85':'Stalk',
				'86':'Stalk', '87':'Stalk', '88':'Stalk','89':'Stalk', '90':'Stalk', '91':'Stalk', '92':'Stalk',
				'93':'Stalk', '94':'Stalk','95':'Stalk', '96':'Stalk', '97':'Stalk', '98':'Stalk', '99':'Stalk',
				'100':'Stalk','101':'Stalk', '102':'Stalk', '103':'Stalk', '104':'Stalk', '105':'Stalk', '106':'Stalk',
				'107':'Stalk', '108':'Stalk', '109':'Stalk', '110':'Stalk', '111':'Stalk', '112':'Stalk','113':'Stalk',
				'114':'Stalk', '115':'Stalk', '116':'Stalk', '117':'Stalk', '118':'Stalk','119':'Stalk', '120':'Stalk',
				'121':'Stalk', '122':'Stalk', '123':'Stalk', '124':'Stalk','125':'Stalk', '126':'Stalk', '127':'Stalk',
				'128':'Stalk', '129':'Stalk', '130':'Stalk','131':'Stalk', '132':'Stalk', '133':'Stalk', '134':'Stalk',
				'135':'Stalk', '136':'Stalk','137':'Stalk', '138':'Stalk', '139':'Stalk', '140':'Stalk', '141':'Stalk',
				'142':'Stalk', '143':'Stalk','144':'Stalk', '145':'Stalk', '146':'Stalk', '147':'Stalk', '148':'Stalk',
				'149':'Stalk', '150':'Stalk', '151':'Stalk', '152':'Stalk', '153':'Stalk', '154':'Stalk','155':'Stalk',
				'156':'Stalk', '157':'Stalk', '158':'Stalk', '159':'Stalk', '160':'Stalk','161':'Stalk', '162':'Stalk',
				'163':'Stalk', '164':'Stalk', '165':'Stalk', '166':'Stalk','167':'Stalk', '168':'Stalk', '169':'Stalk',
				'170':'Stalk', '171':'Stalk', '172':'Stalk','173':'Stalk', '174':'Stalk', '175':'Stalk', '176':'Stalk',
				'177':'Stalk', '178':'Stalk','179':'Stalk', '180':'Stalk', '181':'Stalk', '182':'Stalk', '183':'Stalk',
				'184':'Stalk','185':'Stalk'}



H3HA1Regions = {'1':'Stalk', '2':'Stalk', '3':'Stalk', '4':'Stalk', '5':'Stalk', '6':'Stalk', '7':'Stalk',
				'8':'Stalk', '9':'Stalk', '10':'Stalk', '11':'Stalk', '12':'Stalk-MN',
				'13':'Stalk', '14':'Stalk', '15':'Stalk', '16':'Stalk', '17':'Stalk', '18':'Stalk', '19':'Stalk',
				'20':'Stalk', '21':'Stalk-MN', '22':'Stalk', '23':'Stalk', '24':'Stalk', '25':'Stalk', '26':'Stalk',
				'27':'Stalk', '28':'Stalk', '29':'Stalk', '30':'Stalk', '31':'Stalk', '32':'Stalk', '33':'Stalk',
				'34':'Stalk', '35':'Stalk', '36':'Stalk', '37':'Stalk', '38':'Stalk-MN', '39':'Stalk',
				'40':'Stalk-MN','41':'Stalk-MN', '42':'Stalk-MN', '43':'Stalk', '44':'Stalk', '45':'Stalk', '46':'Stalk',
				'47':'Stalk', '48':'Stalk', '49':'Stalk', '50':'Stalk', '51':'Stalk', '52':'C', '53':'C',
				'54':'C', '55':'Head', '56':'Head', '57':'Head', '58':'Head', '59':'Head', '60':'Head',
				'61':'Head', '62':'E', '63':'E', '64':'Head', '65':'Head', '66':'Head', '67':'Head', '68':'Head',
				'69':'Head', '70':'Head', '71':'Head', '72':'Head', '73':'Head', '74':'Head', '75':'Head',
				'76':'Head', '77':'Head', '78':'E', '79':'Head', '80':'Head',  '81':'E', '82':'Head', '83':'E',
				'84':'Head', '85':'Head', '86':'Head', '87':'Head', '88':'Head', '89':'Head', '90':'Head',
				'91':'Head', '92':'Head', '93':'Head', '94':'Head', '95':'Head', '96':'Head', '97':'Head',
				'98':'Head', '99':'Head', '100':'Head', '101':'Head', '102':'Head', '103':'Head', '104':'Head',
				'105':'Head', '106':'Head', '107':'Head', '108':'Head', '109':'Head', '110':'Head', '111':'Head',
				'112':'Head', '113':'Head', '114':'Head', '115':'Head', '116':'Head', '117':'Head', '118':'Head',
				'119':'Head', '120':'Head', '121':'Head', '122':'A', '123':'Head', '124':'Head', '125':'Head',
				'126':'A', '127':'A', '128':'A', '129':'A', '130':'A', '131':'A', '132':'A',
				'133':'A', '134':'Head', '135':'Head', '136':'Head', '137':'A', '138':'Head', '139':'Head',
				'140':'Head', '141':'A', '142':'A', '143':'A', '144':'A','145':'Head', '146':'Head',
				'147':'Head', '148':'Head', '149':'Head', '150':'Head', '151':'Head', '152':'Head', '153':'Head',
				'154':'Head', '155':'B', '156':'B', '157':'B', '158':'B','159':'B', '160':'B',
				'161':'Head', '162':'Head', '163':'Head', '164':'B', '165':'Head', '166':'Head', '167':'Head', '168':'Head',
				'169':'Head', '170':'Head', '172':'Head', '173':'Head', '174':'D', '175':'Head', '176':'Head',
				'177':'Head', '178':'Head', '179':'Head', '180':'Head', '181':'Head', '182':'D', '183':'Head',
				'184':'Head', '185':'Head', '186':'B', '187':'Head', '188':'B', '189':'B', '190':'B',
				'191':'B', '192':'B', '193':'B', '194':'B', '195':'B', '196':'B', '197':'B', '198':'B',
				'199':'Head', '200':'Head', '201':'B', '202':'Head', '203':'Head', '204':'Head', '205':'Head',
				'206':'Head', '207':'D', '208':'Head', '209':'Head', '210':'Head', '211':'Head', '212':'Head',
				'213':'Head', '214':'Head', '215':'Head', '216':'Head', '217':'Head', '218':'Head', '219':'Head',
				'220':'D', '221':'Head', '222':'Head', '223':'Head', '224':'Head', '225':'Head', '226':'D',
				'227':'Head', '228':'Head', '229':'D','230':'D','231':'Head','232':'Head', '233':'Head',
				'234': 'Head', '235':'Head', '236':'Head', '237': 'Head', '238':'Head', '239':'Head', '240':'Head',
				'241': 'Head', '242':'D', '243': 'Head','244':'D', '245':'Head', '246':'Head', '247':'Head',
				'248': 'Head', '249':'Head', '250':'Head', '251':'Head', '252':'Head', '253':'Head', '254':'Head',
				'255': 'Head', '256':'Head', '257':'Head', '258':'Head', '259':'Head', '260':'Head', '261':'Head',
				'262': 'Head', '263':'Head', '264':'Head', '265':'Head', '266':'Head', '267':'Head', '268':'Head',
				'269': 'Head', '270':'Head', '271':'Head', '272':'Head', '273':'Head', '274':'Head', '275':'C',
				'276': 'C', '277':'Head', '278':'Stalk', '279':'Stalk', '280':'Stalk', '281':'Stalk', '282':'Stalk',
				'283':'Stalk', '284':'Stalk', '285':'Stalk', '286':'Stalk', '287':'Stalk', '288':'Stalk',
				'289':'Stalk',  '290':'Stalk', '291':'Stalk-MN', '292':'Stalk-MN', '293':'Stalk-MN', '294':'Stalk',
				'295':'Stalk', '296':'Stalk', '297':'Stalk', '298':'Stalk', '299':'Stalk', '300':'Stalk',
				'301':'Stalk',  '302':'Stalk', '303':'Stalk', '304':'Stalk', '305':'Stalk', '306':'Stalk','307':'Stalk',
				'308':'Stalk', '309':'Stalk', '310':'Stalk', '311':'Stalk', '312':'Stalk','313':'Stalk',  '314':'Stalk',
				'315':'Stalk', '316':'Stalk', '317':'Stalk', '318':'Stalk-MN', '319':'Stalk', '320':'Stalk', '321':'Stalk',
				'322':'Stalk', '323':'Stalk','324':'Stalk', '325':'Stalk-MN', '326':'Stalk-MN', '327':'Stalk',
				'328':'Stalk'}

H3HA2Regions = {'1':'Stalk', '2':'Stalk', '3':'Stalk', '4':'Stalk', '5':'Stalk', '6':'Stalk', '7':'Stalk',
				'8':'Stalk', '9':'Stalk', '10':'Stalk', '11':'Stalk', '12':'Stalk', '13':'Stalk', '14':'Stalk',
				'15':'Stalk-MN', '16':'Stalk-MN', '17':'Stalk', '18':'Stalk-MN', '19':'Stalk-MN', '20':'Stalk-MN',
				'21':'Stalk-MN', '22':'Stalk', '23':'Stalk', '24':'Stalk', '25':'Stalk', '26':'Stalk',
				'27':'Stalk', '28':'Stalk', '29':'Stalk', '30':'Stalk-MN', '31':'Stalk', '32':'Stalk-MN', '33':'Stalk-MN',
				'34':'Stalk-MN', '35':'Stalk-MN', '36':'Stalk-MN', '37':'Stalk', '38':'Stalk-MN', '39':'Stalk',
				'40':'Stalk', '41':'Stalk-MN', '42':'Stalk-MN', '43':'Stalk', '44':'Stalk', '45':'Stalk-MN',
				'46':'Stalk-MN', '47':'Stalk', '48':'Stalk-MN', '49':'Stalk-MN', '50':'Stalk', '51':'Stalk',
				'52':'Stalk-MN', '53':'Stalk', '54':'Stalk', '55':'Stalk', '56':'Stalk-MN', '57':'Stalk',
				'58':'Stalk', '59':'Stalk', '60':'Stalk', '61':'Stalk', '62':'Stalk', '63':'Stalk', '64':'Stalk',
				'65':'Stalk', '66':'Stalk', '67':'Stalk', '68':'Stalk', '69':'Stalk', '70':'Stalk','71':'Stalk',
				'72':'Stalk', '73':'Stalk', '74':'Stalk', '75':'Stalk', '76':'Stalk','77':'Stalk', '78':'Stalk',
				'79':'Stalk', '80':'Stalk', '81':'Stalk', '82':'Stalk','83':'Stalk', '84':'Stalk', '85':'Stalk',
				'86':'Stalk', '87':'Stalk', '88':'Stalk','89':'Stalk', '90':'Stalk', '91':'Stalk', '92':'Stalk',
				'93':'Stalk', '94':'Stalk','95':'Stalk', '96':'Stalk', '97':'Stalk', '98':'Stalk', '99':'Stalk',
				'100':'Stalk','101':'Stalk', '102':'Stalk', '103':'Stalk', '104':'Stalk', '105':'Stalk', '106':'Stalk',
				'107':'Stalk', '108':'Stalk', '109':'Stalk', '110':'Stalk', '111':'Stalk', '112':'Stalk','113':'Stalk',
				'114':'Stalk', '115':'Stalk', '116':'Stalk', '117':'Stalk', '118':'Stalk','119':'Stalk', '120':'Stalk',
				'121':'Stalk', '122':'Stalk', '123':'Stalk', '124':'Stalk','125':'Stalk', '126':'Stalk', '127':'Stalk',
				'128':'Stalk', '129':'Stalk', '130':'Stalk','131':'Stalk', '132':'Stalk', '133':'Stalk', '134':'Stalk',
				'135':'Stalk', '136':'Stalk','137':'Stalk', '138':'Stalk', '139':'Stalk', '140':'Stalk', '141':'Stalk',
				'142':'Stalk', '143':'Stalk','144':'Stalk', '145':'Stalk', '146':'Stalk-MN', '147':'Stalk', '148':'Stalk',
				'149':'Stalk', '150':'Stalk-MN', '151':'Stalk', '152':'Stalk', '153':'Stalk', '154':'Stalk','155':'Stalk',
				'156':'Stalk', '157':'Stalk', '158':'Stalk', '159':'Stalk', '160':'Stalk','161':'Stalk', '162':'Stalk',
				'163':'Stalk', '164':'Stalk', '165':'Stalk', '166':'Stalk','167':'Stalk', '168':'Stalk', '169':'Stalk',
				'170':'Stalk', '171':'Stalk', '172':'Stalk','173':'Stalk', '174':'Stalk', '175':'Stalk', '176':'Stalk',
				'177':'Stalk', '178':'Stalk','179':'Stalk', '180':'Stalk', '181':'Stalk', '182':'Stalk', '183':'Stalk',
				'184':'Stalk','185':'Stalk'}

if __name__ == '__main__':
	import sys

	app = QtWidgets.QApplication(sys.argv)
	Librator = LibratorMain()

	# test path
	#print(__file__)
	#print(os.path.realpath(__file__))
	#print('using sys.executable:', repr(os.path.dirname(os.path.realpath(sys.executable))))
	#print('using sys.argv[0]:', repr(os.path.dirname(os.path.realpath(sys.argv[0]))))
	#print(sys.argv[0])
	#print(sys.path[0])


	# Librator.exec_()
	Librator.show()
	sys.exit(app.exec_())
