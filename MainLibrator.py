# Librator by Patrick Wilson
from PyQt5.QtCore import pyqtSlot, QTimer, QDateTime, Qt, QSortFilterProxyModel, QModelIndex, QEventLoop, pyqtSignal,QEventLoop
from PyQt5 import QtWidgets, QtPrintSupport
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QTextCursor, QFont, QPixmap, QTextCharFormat, QBrush, QColor, QTextCursor, QCursor
from LibratorSQL import creatnewDB, enterData, RunSQL, UpdateField, deleterecords
import os, sys, re

from MainLibrator_UI import Ui_MainLibrator
from mutationdialog import Ui_MutationDialog
from LibDialogues import openFile, openFiles, newFile, saveFile, questionMessage, informationMessage, setItem, setText, openfastq
from VgenesTextEdit import VGenesTextMain
from ui_VGenesTextEdit import ui_TextEditor
import LibratorSeq

global BaseSeq
BaseSeq = ''

# from PyQt5.QtPrintSupport import QPrintDialog, QPrinter

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

global GLMsg
GLMsg = False

global DataIs
DataIs = []

global DBFilename
DBFilename = 'none'

global working_prefix
working_prefix = '/Users/leil/Documents/Projects/Librator/'
global bin_prefix
bin_prefix = '/usr/local/bin/'


class MutationDialog(QtWidgets.QDialog):
	applySignal = pyqtSignal(str, str, str, str)  # user define signal
	def __init__(self):
		super(MutationDialog, self).__init__()
		self.ui = Ui_MutationDialog()
		self.ui.setupUi(self)

		self.ui.addMutation.clicked.connect(self.accept)
		self.ui.cancel.clicked.connect(self.reject)

	def accept(self):  # redo accept method
		# send signal
		active_tab = self.ui.tabWidget.currentIndex()
		seq_name = self.ui.SeqName.text()
		mutation = self.ui.Mutation.text()
		mutation_ha1 = self.ui.HA1mutation.text()
		mutation_ha2 = self.ui.HA2mutation.text()

		if active_tab == 0: 		# OriPos
			self.applySignal.emit("OriPos", seq_name, mutation, "Nothing")
		elif active_tab == 1:		# H1H3pos
			self.applySignal.emit("H1N3pos", seq_name, mutation_ha1, mutation_ha2)

		#self.applySignal.emit(seq_name, seq_name, mutation_ha1, mutation_ha2)

	 	#self.hide()

class VGenesTextMain(QtWidgets.QMainWindow, ui_TextEditor):
	def __init__(self, parent=None):
		QtWidgets.QMainWindow.__init__(self, parent)
		# super(VGenesTextMain, self).__init__()
		self.setupUi()



class LibratorMain(QtWidgets.QMainWindow):
	def __init__(self):  # , parent=None):
	# def __init__(self, master=None):
		super(LibratorMain, self).__init__()  # parent)

		self.ui = Ui_MainLibrator()

		self.ui.setupUi(self)

		self.ui.listWidgetStrainsIn.itemClicked['QListWidgetItem*'].connect(self.ListItemChanged)

		# self.ui.listWidgetStrainsIn.itemDoubleClicked['QListWidgetItem*'].connect(self.ChangeListName)

		self.ui.cboRole.currentTextChanged['QString'].connect(self.RoleChanged)

		self.ui.cboForm.currentTextChanged['QString'].connect(self.FormChanged)

		self.ui.cboSubtype.currentTextChanged['QString'].connect(self.SubTypeChanged)

		self.ui.cboRecent.currentTextChanged['QString'].connect(self.OpenRecent)

		self.ui.cboReportOptions.currentTextChanged['QString'].connect(self.GenerateReport)

		self.ui.spnFrom.valueChanged['int'].connect(self.SeqFrom)

		self.ui.spnTo.valueChanged['int'].connect(self.SeqTo)

		self.ui.spnAlignFont.valueChanged['int'].connect(self.AlignFont)

		self.ui.txtDonorRegions.textChanged.connect(self.DonorRegions)

		self.ui.txtInsert_Base.textChanged.connect(self.Mutations)

		self.ui.txtName.cursorPositionChanged.connect(self.EditSeqName)

		self.ui.tabWidget.currentChanged['int'].connect(self.FillAlignmentTab)

		self.ui.textSeq.textChanged.connect(self.SeqChanged)

		self.TextEdit = VGenesTextMain()

		self.UpdateRecent()

		self.modalessMutationDialog = None



	@pyqtSlot()
	def UpdateRecent(self):
		filename = os.path.join(working_prefix, 'Librator', 'RecentFiles')
		# filename = os.path.join(os.path.expanduser('~'), 'Applications', 'Librator', 'RecentFiles')
		# filename = 'RecentFiles'
		workingdir, filename = os.path.split(filename)
		os.chdir(workingdir)

		DBdir, DBfile = os.path.split(DBFilename)

		if os.path.isfile(filename):
			with open(filename, 'r') as currentFile:
				RecentFiles = currentFile.readlines()

			i = 0
			for file in RecentFiles:
				file.strip()
				workingdir, fileIs = os.path.split(file)
				fileIs.replace('\n', '')
				if len(fileIs) > 1:
					self.ui.cboRecent.addItem(fileIs)

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

		# elif self.ui.tabWidget.currentIndex() == 1:
		# 	FontIs = self.ui.tableView.font()
		# 	font = QFont(FontIs)
		#
		# 	FontSize = int(font.pointSize())
		# 	if FontSize > 7:
		# 		FontSize += 1
		# 	font.setPointSize(FontSize)
		# 	font.setFamily('Lucida Grande')
		#
		# 	self.ui.tableView.setFont(font)

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

			items = ('H1N1', 'H3N2', "B", "Group 1", 'Group 2', 'Other')
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
		self.AlignSequences('RF', 'none')

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
	def on_btnSearch_clicked(self):

		search = self.ui.txtSearch.toPlainText()
		if search != '':
			self.FindSeq(search)

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
	def on_actionMultiple_Alignement_triggered(self):

		global DataIs
		# global DataIs
		# self.ui.cboActive.clear()
		AlignIn = []
		listItems = self.ui.listWidgetStrainsIn.selectedItems()
		# if not listItems: return
		WhereState = ''
		NumSeqs = len(listItems)
		i = 1
		for item in listItems:

			eachItemIs = item.text()
			WhereState += 'SeqName = "' + eachItemIs + '"'
			if NumSeqs > i:
				WhereState += ' OR '

			i += 1

		SQLStatement = 'SELECT SeqName, Sequence, Vfrom, VTo FROM LibDB WHERE ' + WhereState  # SeqName = "327_Cl15_H1" OR SeqName = "327_Cl16_H1" OR SeqName = "327_Cl17_H1"'
		# SQLStatement = 'SELECT * FROM LibDB WHERE SeqName = "' + eachItemIs + '"'
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
	def FillAlignmentTab(self):
		AlignIn = []
		EachIn = ()

		if self.ui.tabWidget.currentIndex() == 2:
			self.ui.actionAA.setChecked(True)
			self.ui.actionDNA.setChecked(True)
			self.ui.actionGL.setChecked(False)
			self.ui.listWidgetStrainsIn.selectAll()
			listItems = self.ui.listWidgetStrainsIn.selectedItems()
			# if not listItems: return
			WhereState = ''
			NumSeqs = len(listItems)
			i = 1
			for item in listItems:

				eachItemIs = item.text()
				WhereState += 'SeqName = "' + eachItemIs + '"'
				if NumSeqs > i:
					WhereState += ' OR '

				i += 1


			SQLStatement = 'SELECT SeqName, Sequence, Vfrom, VTo FROM LibDB WHERE ' + WhereState  #SeqName = "327_Cl15_H1" OR SeqName = "327_Cl16_H1" OR SeqName = "327_Cl17_H1"'
			# SQLStatement = 'SELECT * FROM LibDB WHERE SeqName = "' + eachItemIs + '"'
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

			Subtype = self.ui.cboSubtype.currentText()
			self.ui.cboSubtype_2.setCurrentText(Subtype)
			if Subtype == 'H3N2' or Subtype == 'Group 2' or Subtype == 'Other':
				self.ui.btnH1Num.setChecked(False)
				self.ui.btnH3Num.setChecked(True)
			elif Subtype == 'H1N1' or Subtype == 'Group 1':
				self.ui.btnH1Num.setChecked(True)
				self.ui.btnH3Num.setChecked(False)

			self.CheckDecorations()


	@pyqtSlot()
	def GenerateReport(self):
		RepOption = self.ui.cboReportOptions.currentText()
		if RepOption == 'Make Secreted Probe':
			self.MakeProbe()
		elif RepOption == 'Gibson fragments':
			self.GenerateGibson()
		elif RepOption == 'New sequence with user specific mutations':
			self.open_mutation_dialog()
		self.ui.cboReportOptions.setCurrentIndex(0)

	@pyqtSlot()
	def GenerateGibson(self):
		MutList = self.ui.txtInsert_Base.toPlainText()
		Mutations = MutList.split(',')




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
				self.HANumbering(AASeq)
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
							NumEnterred = enterData(DBFilename, SeqInfoPacket)

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

		ItemsList = self.ui.listWidgetStrainsIn.count()

		AASeqIs = ''

		if ItemsList > 0:
			AASeqIs = self.ui.textAA.toPlainText()

			self.HANumbering(AASeqIs)
		else:
			return

		self.Decorate(Decorations)


	@pyqtSlot()
	def Decorate(self, Decorations):
		AAColorMap = ''

		cursor = self.ui.txtAASeq.textCursor()
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

			if Decoration == 'DonRegs':

				DomainsLine = ''
				DomainsOn = True

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
		AAKey = 'Sequence elements:  HA1    HA2   stop   Transmembrane  Trimerization-Avitag-H6 \n'
		AAKeyC = '000000000000000000000000099999991111111888888888888888BBBBBBBBBBBBBBBBBBBBBBBBB\n'

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

		Sequence = SeqName + '\n'
		ColorMap = ''
		for i in range(0,LenSeqName):
			ColorMap += '0'
		ColorMap += '\n'

		# NumLine += '.'
		# AAPosColorMap += '0'
		for i in range(0, len(AASeq), 60):

			AASeqSeg = '    Sequence: ' + AASeq[i:i+60] + '\n\n'
			AAColorSeg = '00000000000000' + AAColorMap[i:i + 60] + '\n\n'
			NumLineSeg = '    Position: ' + NumLine[i:i+60] + '\n'
			AAPosColorSeg = '00000000000000' + AAPosColorMap[i:i + 60] + '\n'

			Sequence += NumLineSeg
			ColorMap += AAPosColorSeg

			if H3NumOn == True:
				H3NumSeg = 'H3-Numbering: ' + H3NumLine[i:i+60] + '\n'
				H3ColorSeg = '00000000000000' + H3ColorMap[i:i + 60] + '\n'
				Sequence += H3NumSeg
				ColorMap += H3ColorSeg

				# Sequence += AASeqSeg
				# ColorMap += AAColorSeg

			if H1NumOn == True:
				H1NumSeg = 'H1-Numbering: ' + H1NumLine[i:i + 60] + '\n'
				H1ColorSeg = '00000000000000' + H1ColorMap[i:i + 60] + '\n'
				Sequence += H1NumSeg
				ColorMap += H1ColorSeg

			Sequence += AASeqSeg
			ColorMap += AAColorSeg
			# NumberLine += NumLineSeg
			# AAPositionColor += AAPosColorSeg

		Sequence += ' \n'
		ColorMap += '0\n'


		Sequence += AAKey + H3Key + H1Key
		ColorMap += AAKeyC + H3KeyCMap + H1KeyCMap
		# Add note at begining that HA1 is black andHA2 is grey or
		self.ui.txtAASeq.setText(Sequence)
		self.DecorateText(ColorMap, cursor)
		#
		# KeyDoc =
		# KeyCMap =
		# cursor = self.ui.txtKey.textCursor()
		# self.ui.txtKey.setText(KeyDoc)
		# self.DecorateText(KeyCMap, cursor)


		# for pos in range(1, len(H3Numbering)):
		# 	residue = H3Numbering[pos]

	@pyqtSlot()
	def DecorateText(self, ColorMap, cursor):
		# o in colormap is black text on white background
		#  cursor is cursor from textbox being decorated, i.e.:
		# cursor = self.ui.txtAASeq.textCursor()   when from sequence panel
		#  need provide cursor strat as well...so starts color mid window:
		#          CurPos = (WindowSize // 2)      when from sequence panel
		#  CurPos and cursor will allow me to run through entire text of
		# any window with different paramaters and colormaps


		CurPos = 0
		# Setup the desired format for matches
		format = QTextCharFormat()

		for valueIs in ColorMap:  #QColor is RGB: 0-255, 0-255, 0-255
			if valueIs == '0':
				format.setBackground(QBrush(QColor("white")))
				format.setForeground(QBrush(QColor("black")))
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


			cursor.setPosition(CurPos)
			cursor.setPosition(CurPos + 1, QTextCursor.KeepAnchor)
			cursor.mergeCharFormat(format)

			CurPos += 1




	@pyqtSlot()
	def AlignSequences(self, DataIn, Notes):
		# import tempfile
		import os
		TupData = ()
		DataSet = []
		QApplication.setOverrideCursor(Qt.WaitCursor)
		global GLMsg


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
				self.ui.actionGL.setChecked(True)
				self.ui.actionAA.setChecked(True)
				GLMsg = True
				GermSeq = DNASeq
				Germline = ('Germline', GermSeq)
				DataSet.append(Germline)
			else:
				if self.ui.actionGL.isChecked() == True:
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
				self.ui.actionGL.setChecked(True)
				self.ui.actionAA.setChecked(True)
				GLMsg = True
				GermSeq = self.ui.textSeq.toPlainText()
				Germline = ('Germline', GermSeq)
				DataSet.append(Germline)

		else:
			self.ui.actionGL.setChecked(False)
			DataSet = DataIn

		# import subprocess

		#(fd, outfilename) = tempfile.mkstemp()
		outfilename = ''
		try:

			outfilename = LibratorSeq.ClustalO(DataSet, 80, True)

			lenName = 0
			longestName = 0
			alignmentText = ''
			germseq = ''
			germpeptide = ''

			each = ()
			all = []
			if self.ui.actionGL.isChecked() == False:
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

		if self.ui.actionGL.isChecked() == True:
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
		if self.ui.actionGL.isChecked() == False:
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
			self.ShowVGenesTextEdit(alignmentText, Style)
		else:
			self.ui.txtSeqAlignment.setText(alignmentText)

		QApplication.restoreOverrideCursor()

		# for item in Aligned:

		# print('done')

	# do lengthy process

	@pyqtSlot()
	def on_action_Save_triggered(self):
		# SeqName, Sequence, SeqLen, SubType, Form, VFrom, VTo, Active, Role, Donor, Mutations, ID
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

		CurName = self.ui.txtName.toPlainText()
		CurrVal = self.ui.cboForm.currentText()

		self.UpdateSeq(CurName, CurrVal,'Form')

	@pyqtSlot()
	def SubTypeChanged(self):

		CurName = self.ui.txtName.toPlainText()
		CurrVal = self.ui.cboSubtype.currentText()

		self.UpdateSeq(CurName, CurrVal, 'SubType')




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

	@pyqtSlot()
	def Mutations(self):

		global SeqMove
		if SeqMove == False:
			CurName = self.ui.txtName.toPlainText()
			CurrVal = self.ui.txtInsert_Base.toPlainText()

			self.UpdateSeq(CurName, CurrVal, 'Mutations')
		SeqMove = False

	@pyqtSlot()
	def RoleChanged(self):
		global BaseSeq
		global DataIs
		NoChange = False
		answer  = 'No'
		CurName = self.ui.txtName.toPlainText()
		CurrVal = self.ui.cboRole.currentText()
		if CurrVal == 'Base':

			if BaseSeq != CurName and BaseSeq != '':

				question = BaseSeq + ':\n\n is already denoted as the Base sequence and there can only be one.\n Reassign the Base sequence to:\n\n' + CurName + '?'
				buttons = 'YN'
				answer = questionMessage(self, question, buttons)
				if answer == 'Yes':
					self.UpdateSeq(BaseSeq, 'Unassigned', 'Role')
					BaseSeq = CurName
					self.ui.lblBaseName.setText(BaseSeq)
				else:
					NoChange = True


		# self.ui.cboRole.setEnabled(False)

		if NoChange == False:
			self.UpdateSeq(CurName, CurrVal,'Role')


	@pyqtSlot()
	def UpdateSeq(self, ID, ItemValue, FieldName):
		global DBFilename
		# ID = item[0]


		UpdateField(ID, ItemValue, FieldName, DBFilename)


	@pyqtSlot()
	def ShowVGenesTextEdit(self, textToShow, style):

		if style == 'aligned':
			FontIs = self.TextEdit.textEdit.currentFont()
			font = QFont(FontIs)

			# FontSize = int(font.pointSize())
			font.setPointSize(10)
			font.setFamily('Courier New')

			self.TextEdit.textEdit.setFont(font)

		elif style == 'standard':
			FontIs = self.TextEdit.textEdit.currentFont()
			font = QFont(FontIs)

			# FontSize = int(font.pointSize())
			font.setPointSize(10)
			font.setFamily('Lucida Grande')

			self.TextEdit.textEdit.setFont(font)

		elif style == 'ProteinReport':
			FontIs = self.TextEdit.textEdit.currentFont()
			font = QFont(FontIs)

			# FontSize = int(font.pointSize())
			font.setPointSize(6)
			font.setFamily('Courier New')

			self.TextEdit.textEdit.setFont(font)

		self.TextEdit.show()

		self.TextEdit.textEdit.setText(textToShow)


	@pyqtSlot()
	def on_action_Open_triggered(self):  # how to activate menu and toolbar actions!!!
		#need to simply get database name and populate list views
		global DBFilename
		global DataIs

		DBFilename = openFile(self, 'ldb')

		titletext = 'Librator - ' + DBFilename
		self.setWindowTitle(titletext)



		# self.ui.listWidgetStrainsIn.setCurrentRow(0)

		self.PopulateCombos()
		# self.UpdateRecentFilelist()
		# self.ui.listWidgetStrainsIn.setCurrentIndex(0)


		ItemsList = self.ui.listWidgetStrainsIn.count()
		if ItemsList >0:
			self.ui.listWidgetStrainsIn.setCurrentRow(0)
			self.ListItemChanged()
			for item in DataIs:
				FromV = int(item[5])-1
				if FromV == -1: FromV = 0
				ToV = int(item[6])-1

				HASeq = item[1]
				HASeq = HASeq[FromV:ToV]

				AASeq = Translator(HASeq.upper(), 0)
				AASeqIs = AASeq[0]
			self.HANumbering(AASeqIs)


	@pyqtSlot()
	def OpenRecent(self):  # how to activate menu and toolbar actions!!!
		#need to simply get database name and populate list views
		global DBFilename

		filename = os.path.join(working_prefix, 'Librator', 'RecentFiles')
		#filename = os.path.join(os.path.expanduser('~'), 'Applications', 'Librator', 'RecentFiles')
		# filename = 'RecentFiles'
		workingdir, filename = os.path.split(filename)
		os.chdir(workingdir)

		if self.ui.cboRecent.currentText() == 'Open previous':
			self.ui.cboRecent.setCurrentIndex(1)
			filename = self.ui.cboRecent.currentText()
			# filename = 'RecentFiles'
			workingdir, filename = os.path.split(filename)
			os.chdir(workingdir)
			DBFilename = filename

		titletext = 'Librator - ' + DBFilename
		self.setWindowTitle(titletext)

		self.PopulateCombos()

		self.ui.listWidgetStrainsIn.setCurrentRow(0)
		self.UpdateRecentFilelist()

	@pyqtSlot()
	def UpdateRecentFilelist(self):
		# todo make recent files an SQL file then can use all SQL tools to clean

		filename = os.path.join(working_prefix, 'Librator', 'RecentFiles')
		#filename = os.path.join(os.path.expanduser('~'), 'Applications', 'Librator', 'RecentFiles')
		# filename = 'RecentFiles'
		# workingdir, filename = os.path.split(filename)
		# os.chdir(workingdir)
		#
		# DBdir, DBfile = os.path.split(DBFilename)
		#
		# NewRecentFile = ''
		# if os.path.isfile(filename):
		# 	with open(filename, 'r') as currentFile:
		# 		RecentFiles = currentFile.readlines()
		#
		# 	i = 0
		# 	for file in RecentFiles:
		# 		file.strip()
		# 		workingdir, fileIs = os.path.split(file)
		# 		if fileIs == DBfile:
		#
		#
		# 			RecentFiles.remove(i)
		#
		# 		i += 1
		#
		# 	# if len(RecentFiles) > 10:  #limits length of recents to 10
		# 	# 	RecentFiles.remove(0)
		#
		# 	RecentFiles.append(DBFilename)
		# 	for item in RecentFiles:
		# 		item.replace('\n', '')
		# 		NewRecentFile += item + '\n'
		#
		#
		# 	with open(filename, 'w') as currentFile:
		# 		currentFile.write(NewRecentFile)
		#
		# else:
		# 	NewRecentFile = DBFilename + '\n'
		# 	with open(filename, 'w') as currentFile:
		# 		currentFile.write(NewRecentFile)

	# 	todo Add code to populate list cobo


	# actionHANumbering

	@pyqtSlot()
	def on_actionHANumbering_triggered(self):


		# answer = informationMessage(self, 'Would you like to generate a numbering report?' 'YN')
		AASeq = self.ui.textAA.toPlainText()
		Numbering = self.HANumbering(AASeq)
		self.ui.tabWidget.setCurrentIndex(1)




	@pyqtSlot()
	def HANumbering(self, AASeq):

		import uuid
		global H1Numbering
		global H3Numbering
		H1Numbering.clear()
		H3Numbering.clear()
		global NumberingMap
		NumberingMap.clear()


		NameBase = str(uuid.uuid4())
		# NameBase = NameBase[:12]
		NameBase = NameBase.replace('-', '')

		NameBase = NameBase.replace(' ', '')

		MyInFiles = NameBase + 'In.txt'
		MyOutFiles = NameBase + 'Out.txt'

		workingfilename = os.path.join(working_prefix, 'Librator', MyInFiles)
		#workingfilename = os.path.join(os.path.expanduser('~'), 'Applications', 'Librator', MyInFiles)
		musclepath = os.path.join(bin_prefix)
		#musclepath = os.path.join(os.path.expanduser('~'), 'Applications', 'Librator', 'muscle')
		savefilename = os.path.join(working_prefix, 'Librator', MyOutFiles)
		#savefilename = os.path.join(os.path.expanduser('~'), 'Applications', 'Librator', MyOutFiles)
	# 	probconspath /Users/jbloom/probcons/

		workingdir, filename = os.path.split(workingfilename)
		os.chdir(workingdir)

		# NumberingCommandLine = 'python3 HA_Numbering.py ' + workingfilename + ' > ' + savefilename #workingfilename #+ '\n'

		NumberingCommandLine = 'python3 HA_Numbering.py In.txt > '+ MyOutFiles #Out.txt'  # workingfilename #+ '\n'


		NumberingQuery = 'musclepath '
		NumberingQuery += musclepath + '\n' + 'ha_sequence '

		NumberingQuery += AASeq + '\n'

		Sites = 'sites '
		for Res in range(0, len(AASeq)):
			Sites += str(Res+1)
			Sites += ' '

		NumberingQuery += Sites + '\n'

		workingfilename = 'In.txt'
		SavedFile = MyOutFiles#'Out.txt'

		with open(workingfilename, 'w') as currentFile:
			currentFile.write(NumberingQuery)

		# NumberingOut = os.popen(NumberingCommandLine)
		try:
			NumberingOut = os.popen(NumberingCommandLine)
		except:
			print('end')


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


		#
		# * **4HMG** is H3N2 strain A/Aichi/2/1968 (or X-31 HA). This is the numbering scheme that is often referred to as the "H3 numbering system." The HA1 and HA2 polypeptides are numbered as different sequences in this numbering scheme.
		#
		# * **4JTV**  human 2009 pandemic H1N1 strain A/California/4/2009. The HA1 and HA2 polypeptides are numbered as different sequences in this numbering scheme.



	@pyqtSlot()
	def ListItemChanged(self):
		# self.ui.listWidgetStrainsIn.event
		global DataIs
		# self.ui.cboActive.clear()
		listItems = self.ui.listWidgetStrainsIn.selectedItems()
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
			if Role == 'Donor':
				CurIndex = 1
			if Role == 'Base':
				CurIndex = 2
				BaseSeq = item[0]
			if Role == 'Reference':
				CurIndex = 3

			self.ui.cboRole.setCurrentIndex(CurIndex)


			SubType = item[3]
			if SubType == 'H3N2':
				CurIndex = 0
			if SubType == 'H1N1':
				CurIndex = 1
			if SubType == 'B':
				CurIndex = 2
			if SubType == 'Group 1':
				CurIndex = 3
			if SubType == 'Group 2':
				CurIndex = 4
			if SubType == 'Other':
				CurIndex = 5

			self.ui.cboSubtype.setCurrentIndex(CurIndex)

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
		for item in listItems:
			eachItemIs = item.text()
			self.ui.listWidgetStrainsIn.addItem(eachItemIs)
			self.UpdateSeq(eachItemIs, 'True', 'Active')

			# self.FillAlignmentTab()

	@pyqtSlot()
	def on_actionPrint_triggered(self):
		global DataIs

		FontIs = self.TextEdit.textEdit.currentFont()
		font = QFont(FontIs)

		# SeqName, Sequence, SeqLen, SubType, Form, VFrom, VTo, Active, Role, Donor, Mutations, ID
		if self.ui.tabWidget.currentIndex() == 0:
			fields = ['SeqName', 'Sequence', 'Length', 'Subtype', 'Form', 'From', 'To', 'Active', 'Role', 'Donor regions',
			          'Mutations']
			# SQLStatement = VGenesSQL.MakeSQLStatement(self, fields, data[0])
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

		# self.TextEdit.show()

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
		# self.ui.listWidgetStrainsIn.setCurrentRow(-1)

		listRow = self.ui.listWidgetStrainsIn.currentRow()
		listItems = self.ui.listWidgetStrainsIn.selectedItems()
		for item in listItems:
			eachItemIs = item.text()

			self.UpdateSeq(eachItemIs,'False','Active')

		if listRow>-1:
			self.ui.listWidgetStrainsIn.takeItem(listRow)

		# if not listRow: return
		# self.ui.listWidgetStrainsIn.takeItem(listRow)



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



		# itemIs  = self.ui.listWidgetStrainsIn.changeEvent()


		# self.ui.listWidgetStrainsIn.takeItem(itemIndex)
			# ItemInd = self.listWidgetStrainsIn.row(item)
			# textis  = item.
			# self.ui.listWidgetStrainsIn.sel

	@pyqtSlot()
	def on_listWidgetStrainsIn_changeEvent(self):
		self.PopulateCboActiveCbo()


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

		if DBFilename != None and DBFilename != '':
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
		self.UpdateRecentFilelist()
			# if os.path.isfile(DBFilename):
			# 	self.LoadDB(DBFilename)

		# else:
		# 	self.hide()
		# 	self.ApplicationStarted()


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


	# action_Import
	@pyqtSlot()
	def on_action_Import_triggered(self):
		self.ImportSeqs()

	@pyqtSlot()
	def on_btnImport_clicked(self):
		self.ImportSeqs()

	@pyqtSlot()
	def ImportSeqs(self):


		SeqInfoPacket = []
		filename = openFile(self, 'FASTA')
		HA_Read = ReadFASTA(filename)
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
			HASeq = item[1]

			# HAAA = Translator(HASeq.upper(), 0)
			if StopAsking == 'No':
				items = ('H1N1', 'H3N2', "B", "Group 1", 'Group 2', 'Other')
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
			NumEnterred = enterData(DBFilename,SeqInfoPacket)
		self.PopulateCombos()

	@pyqtSlot()
	def PopulateCombos(self):
		DataIs = RunSQL(DBFilename, 'None')
		global BaseSeq
		self.ui.listWidgetStrainsIn.clear()
		for item in DataIs:
			SeqName = item[0]
			# self.ui.cmbListBase.addItem(SeqName)
			self.ui.listWidgetStrains.addItem(SeqName)
			if item[7] == 'True':
				self.ui.listWidgetStrainsIn.addItem(SeqName)
			if item[8] == 'Base':
				BaseSeq = SeqName
				self.ui.lblBaseName.setText(BaseSeq)

	def show3Dstructure(self, mutation, pdbPath, pymolPath, subtype):
		pml_path = os.path.join(working_prefix, "Librator/local.pml")
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
			if subtype == "H1N1":
				text = "sel ABS-Ca1, resi 171+173+175+176+178+179+180\n" \
						+ "sel ABS-Ca2, resi 169+172+205+206+209+211\n" \
						+ "sel ABS-Cb, resi 182+186+220+253\n" \
						+ "sel ABS-Sa, resi 153+156+158+237+238\n" \
						+ "sel ABS-Sb, resi 87+88+90+91+92+135\n" \
						+ "color purple, ABS-Ca1\n" \
						+ "color yellow, ABS-Ca2\n" \
						+ "color gray, ABS-Cb\n" \
						+ "color chocolate, ABS-Sa\n" \
						+ "color green, ABS-Sb\n"
				pml.write(text)
			elif subtype == "H3N2":
				text = "sel ABS-A, resi 122+126+127+128+129+130+131+132+133+137+141+142+143+144\n" \
						+ "sel ABS-B, resi 155+156+157+158+159+160+164+186+188+189+190+191+192+193+194+195+196+197+198+201\n" \
						+ "sel ABS-C, resi 52+53+54+275+276\n" \
						+ "sel ABS-D, resi 174+182+207+220+226+229+230+242+244\n" \
						+ "sel ABS-E, resi 62+63+77+81+83\n" \
						+ "color purple, ABS-A\n" \
						+ "color yellow, ABS-B\n" \
						+ "color gray, ABS-C\n" \
						+ "color chocolate, ABS-D\n" \
						+ "color green, ABS-E\n"
				pml.write(text)

			# highlight mutations in red on the 3D structure
			if mutation != "none":
				position = re.sub('[A-Za-z]', '', mutation)
				position = position.replace(",", "+")
				text = "sel mutation, resi " + position + "\n"
				pml.write(text)
				text = "color red, mutation\n"
				pml.write(text)

				labels = mutation.split(",")
				for label in labels:
					number = re.sub('[A-Za-z]', '', label)
					text = "label resi " + number + " and name C, \"" + label + "\"\n"
					pml.write(text)

			text = "set label_size, 25\n"
			pml.write(text)

		cmd = pymolPath + " " + pml_path
		os.popen(cmd)

	@pyqtSlot()
	def on_btnFieldSearch_clicked(self):
		mutation = "M131L,N171K,Q144R"
		pymol_path = "pymol"

		#AASeq = self.ui.textAA.toPlainText()
		mutation = self.ui.txtInsert_Base.toPlainText().strip(",")
		subtype = str(self.ui.cboSubtype.currentText())

		if subtype == "H1N1":
			pdb_path = working_prefix + "Librator/PDB/1ruz.pdb"
		elif subtype == "H3N2":
			pdb_path = working_prefix + "Librator/PDB/4hmg.pdb"
		elif subtype == "B":
			pdb_path = working_prefix + "Librator/PDB/3hto.pdb"
		elif subtype == "Group 1":
			pdb_path = working_prefix + "Librator/PDB/3hto.pdb"
		elif subtype == "Group 2":
			pdb_path = working_prefix + "Librator/PDB/3hto.pdb"
		else:
			pdb_path = working_prefix + "Librator/PDB/3hto.pdb"

		self.show3Dstructure(mutation, pdb_path, pymol_path, subtype)

	def updateUI(self, a, b, c, d):  # For modaless dialog
		print("Mutation mode: " + a)
		print("Sequence Name: " + b)
		if a == "OriPos":
			print("Mutations: " + c)
		elif a == "H1N3pos":
			print("Mutations on HA1: " + c)
			print("Mutations on HA2: " + d)

	def open_mutation_dialog(self):
		if self.modalessMutationDialog is None:
			cur_seq_name = "Current Sequence: " + self.ui.txtName.toPlainText()
			self.modalessMutationDialog = MutationDialog()
			self.modalessMutationDialog.ui.CurSeq.setText(cur_seq_name)
			self.modalessMutationDialog.ui.SeqName.setText(self.ui.txtName.toPlainText())
			self.modalessMutationDialog.applySignal.connect(self.updateUI)
		self.modalessMutationDialog.show()



def ReadFASTA(outfilename):
	ReadFile = []
	# ReadFile.clear
	# SeqRead = []
	Readline = ''
	currentFile2 = ''
	with open(outfilename, 'r') as currentFile2:  # using with for this automatically closes the file even if you crash
		# currentFile.write(FASTAfile)
		Seq = ''
		SeqName = ''
		Readline = ''
		for line in currentFile2:
			Readline = line.replace('\n', '').replace('\r', '')

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

# * **4HMG** is H3N2 strain A/Aichi/2/1968 (or X-31 HA). This is the numbering scheme that is often referred to as the "H3 numbering system." The HA1 and HA2 polypeptides are numbered as different sequences in this numbering scheme.
#
# * **4JTV**  human 2009 pandemic H1N1 strain A/California/4/2009. The HA1 and HA2 polypeptides are numbered as different sequences in this numbering scheme.

if __name__ == '__main__':
	import sys

	app = QtWidgets.QApplication(sys.argv)
	Librator = LibratorMain()

	# Librator.exec_()
	Librator.show()
	sys.exit(app.exec_())
