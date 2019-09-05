# Librator by Patrick Wilson
from PyQt5.QtCore import pyqtSlot, QTimer, QDateTime, Qt, QSortFilterProxyModel, QModelIndex
from PyQt5 import QtWidgets

from MainLibrator_UI import Ui_MainLibrator

from LibDialogues import openFile, openFiles, newFile, saveFile, questionMessage, informationMessage, setItem, \
	setText, openfastq

from LibratorSQL import creatnewDB, enterData, RunSQL
import os, sys

global DBFilename
DBFilename = 'none'

class LibratorMain(QtWidgets.QMainWindow):
	def __init__(self):  # , parent=None):
	# def __init__(self, master=None):
		super(LibratorMain, self).__init__()  # parent)

		self.ui = Ui_MainLibrator()

		self.ui.setupUi(self)



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
	def on_action_Open_triggered(self):  # how to activate menu and toolbar actions!!!
		#need to simply get database name and populate list views
		global DBFilename

		DBFilename = openFile(self, 'ldb')

		titletext = 'Librator - ' + DBFilename
		self.setWindowTitle(titletext)

		self.PopulateCombos()
	# 	todo Add code to populate list cobo

	@pyqtSlot()
	def on_btnClearStrain_clicked(self):
		self.removeSel()


	def PopulateCboActiveCbo(self):
		listItems = self.ui.listWidgetStrainsIn.selectedItems()
		if not listItems: return

		for item in listItems:
			eachItemIs = item.text()
		self.ui.cboActive.addItems(listItems)

	def removeSel(self):
		listRow = self.ui.listWidgetStrainsIn.currentRow()
		if not listRow: return
		self.ui.listWidgetStrainsIn.takeItem(listRow)






		# itemIs  = self.ui.listWidgetStrainsIn.currentItem()


		# self.ui.listWidgetStrainsIn.takeItem(itemIndex)
			# ItemInd = self.listWidgetStrainsIn.row(item)
			# textis  = item.
			# self.ui.listWidgetStrainsIn.sel


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

			# if os.path.isfile(DBFilename):
			# 	self.LoadDB(DBFilename)

		# else:
		# 	self.hide()
		# 	self.ApplicationStarted()



	def ImportSeqs(self):
		SeqInfoPacket = []
		filename = openFile(self, 'FASTA')
		HA_Read = ReadFASTA(filename)
		StopAsking = 'No'
		AlreadyAsked = 'No'

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

				items = ('Full HA', 'Probe HA', "Full NA", "Probe NA", 'Other')
				title = 'Choose form of molecule for ' + HAName
				form = setItem(self, items, title)
				# self.ui.cmbForm_Base.setCurrentText(form)
				if subtype == "Cancel":
					form = 'none'
					return

			if AlreadyAsked == 'No':
				StopAsking = informationMessage(self, 'Use this subtype and form information for all strains?', 'YN')
				AlreadyAsked = 'Yes'




			# self.ui.textBaseSeq.setText(HASeq.upper())
			# self.ui.textBaseAA.setText(HAAA[0])
			# self.ui.textBaseSeqName.setText(HAName)
			blank = 'spaceholder'
			# SeqName text, Sequence text, SeqLen, SubType text, Form text,

			# question = 'Would you like to enter the sequence into your database?'
			# buttons = 'YN'
			# answer = questionMessage(self, question, buttons)
			# if answer == 'Yes':
			# if DBFilename == 'none':
			# 	items = ('New', 'Open', "Cancel")
			# 	title = 'Choose an option'
			# 	selection = setItem(self, items, title)
			# 	self.ui.cmbSubtypes_Base.setCurrentText(subtype)
			# 	if selection == "Cancel":
			# 		return
			# 	elif selection == 'New':
			# 		self.on_action_New_triggered()
			# 	elif selection == 'Open':
			# 		self.on_action_Open_triggered()

			ItemIn = [HAName, HASeq, str(len(HASeq)), subtype, form, blank,0]
			SeqInfoPacket.clear()
			SeqInfoPacket.append(ItemIn)
			NumEnterred = enterData(DBFilename,SeqInfoPacket)
		self.PopulateCombos()

	def PopulateCombos(self):
		DataIs = RunSQL(DBFilename, 'None')

		for item in DataIs:
			SeqName = item[0]
			self.ui.cmbListBase.addItem(SeqName)
			self.ui.listWidgetStrains.addItem(SeqName)

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



if __name__ == '__main__':
	import sys

	app = QtWidgets.QApplication(sys.argv)
	Librator = LibratorMain()

	# Librator.exec_()
	Librator.show()
	sys.exit(app.exec_())
