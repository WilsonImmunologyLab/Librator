#!/usr/bin/python
# -*- coding: UTF-8 -*- 
import os,re
import pandas as pd
import numpy as np
import sqlite3 as db

global H3template
global H3template_seq
global H3_start
global H3_end
H3template = "A/Perth/16/2009|H3N2"
H3template_seq = "MKTIIALSYILCLVFAQKLPGNDNSTATLCLGHHAVPNGTIVKTITNDQIEVTNATELVQSSSTGEICDSPHQILDGKNCT" \
  "LIDALLGDPQCDGFQNKKWDLFVERSKAYSNCYPYDVPDYASLRSLVASSGTLEFNNESFNWTGVTQNGTSSACIRRSKNSFFSRLNWLTHLNFKY" \
  "PALNVTMPNNEQFDKLYIWGVLHPGTDKDQIFLYAQASGRITVSTKRSQQTVSPNIGSRPRVRNIPSRISIYWTIVKPGDILLINSTGNLIAPRGY" \
  "FKIRSGKSSIMRSDAPIGKCNSECITPNGSIPNDKPFQNVNRITYGACPRYVKQNTLKLATGMRNVPEKQTRGIFGAIAGFIENGWEGMVDGWYGF" \
  "RHQNSEGRGQAADLKSTQAAIDQINGKLNRLIGKTNEKFHQIEKEFSEVEGRIQDLEKYVEDTKIDLWSYNAELLVALENQHTIDLTDSEMNKLFE" \
  "KTKKQLRENAEDMGNGCFKIYHKCDNACIGSIRNGTYDHDVYRDEALNNRFQIKGVELKSGYKDWILWISFAISCFLLCVALLGFIMWACQKGNIR" \
  "CNICI"
H3_start = [1, 123, 264, 403];
H3_end = [131, 272, 411, 520];

global H1template
global H1template_seq
global H1_start
global H1_end
H1template = "A/California/04/2009|H1N1"
H1template_seq = "MKAILVVLLYTFATANADTLCIGYHANNSTDTVDTVLEKNVTVTHSVNLLEDKHNGKLCKLRGVAPLHLGKCNIAGWILGN" \
  "PECESLSTASSWSYIVETPSSDNGTCYPGDFIDYEELREQLSSVSSFERFEIFPKTSSWPNHDSNKGVTAACPHAGAKSFYKNLIWLVKKGNSYPK" \
  "LSKSYINDKGKEVLVLWGIHHPSTSADQQSLYQNADTYVFVGSSRYSKKFKPEIAIRPKVRDQEGRMNYYWTLVEPGDKITFEATGNLVVPRYAFA" \
  "MERNAGSGIIISDTPVHDCNTTCQTPKGAINTSLPFQNIHPITIGKCPKYVKSTKLRLATGLRNIPSIQSRGLFGAIAGFIEGGWTGMVDGWYGYH" \
  "HQNEQGSGYAADLKSTQNAIDEITNKVNSVIEKMNTQFTAVGKEFNHLEKRIENLNKKVDDGFLDIWTYNAELLVLLENERTLDYHDSNVKNLYEK" \
  "VRSQLKNNAKEIGNGCFEFYHKCDNTCMESVKNGTYDYPKYSEEAKLNREEIDGVKLESTRIYQILAIYSTVASSLVLVVSLGAISFWMCSNGSLQ" \
  "CRICI"
H1_start = [1, 123, 264, 403];
H1_end = [131, 272, 411, 520];

global DB_name
DB_name = "AAATester.ldb"

def generate_fragments(data,subtype):
	# initial the temp file name
	in_file = "in.fas"
	out_file = "out.fas"

	if(subtype == "H1"):
		# set template
		template_name = H1template
		template_seq = H1template_seq
		aa_start = H1_start;
		aa_end = H1_end;
	elif(subtype == "H3"):
		# set template
		template_name = H3template
		template_seq = H3template_seq
		aa_start = H3_start;
		aa_end = H3_end;
	else:
		print("We don't support other subtypes for now! Please input H3N2 or H1N1!")
		return
	# number of fragments
	num_fragment = len(aa_start)

	# write sequence into file for alignment
	temp_file = open(in_file, "w")
	temp_file.write(">" + template_name + "\n")
	temp_file.write(template_seq + "\n")

	#for (name,seq) in  sequence.items():
	#	temp_file.write(">" + name + "\n")
	#	temp_file.write(seq['AAseq'] + "\n")
	for index in  data.index:
		temp_file.write(">" + data.loc[index,'Name'] + "\n")
		temp_file.write(data.loc[index,'AAseq'] + "\n")

	temp_file.close()

	# run muscle to align query seuqnece to template sequence
	cmd = "muscle -in " + in_file + " -out " + out_file
	print(cmd)
	os.system(cmd)

	# read alignment from muscle results
	align_file = open(out_file, "r")
	alignment = align_file.read()

	sequences = alignment.split(">")

	for cur_seq in sequences:
		if template_name in cur_seq:
			template = cur_seq
			break

	tmp = template.split("\n")
	tmp = tmp[1:]
	seperator = ""
	template = seperator.join(tmp)

	if "-" in template:
		# new sequences have insersion, adjust the start and end position for all fragments based on current alignment
		hyphen_pos = [i.start() for i in re.finditer('-', template)]
		for pos_iter in hyphen_pos:
			cur_pos = pos_iter + 1
			for i in range(num_fragment):
				if(aa_start[i] >= cur_pos):
					aa_start[i] = aa_start[i] + 1
				if(aa_end[i] >= cur_pos):
					aa_end[i] = aa_end[i] + 1

	# test the position update with template
	print("Sequence Name:\t" + template_name)
	for i in range(num_fragment):
		fragment = template[aa_start[i] -1: aa_end[i]]
		print("F" + str(i + 1) + ":\t" + fragment)

	# initial fragment data matrix
	fragment_data = []
	# get all the query alignments
	sequences = sequences[1:]
	for cur_seq_block in sequences:
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
		cur_seq_nt = data.loc[cur_index,'NTseq']

		# remove the hyphen in AA sequences and modify nt start and end
		nt_start = [0] * num_fragment
		nt_end = [0] * num_fragment
		diff = 0

		for i in range(num_fragment):
			fragment = cur_seq[aa_start[i] -1: aa_end[i]]

			hyphen_pos = [i.start() for i in re.finditer('-', fragment)]
			nt_start[i] = (aa_start[i] - 1)*3 + 1 - diff
			diff = diff + len(hyphen_pos)*3
			nt_end[i] = aa_end[i]*3 - diff
			fragment1 = fragment.replace("-","")

			nt_fragment = cur_seq_nt[nt_start[i] -1: nt_end[i]]

			cur_seq_fragment_data.append(fragment)
			cur_seq_fragment_data.append(fragment1)
			cur_seq_fragment_data.append(nt_fragment)
		fragment_data.append(cur_seq_fragment_data)

	# make col name
	col_name = ["Name"]
	for i in range(num_fragment):
		col_name.append("F_AA_" + str(i + 1) + "_origin")
		col_name.append("F_AA_" + str(i + 1) + "_refine")
		col_name.append("F_NT_" + str(i + 1))
	
	fragment_data = pd.DataFrame(fragment_data)
	fragment_data.columns = col_name

	# save to Excel
	# writer=pd.ExcelWriter('excel.xlsx') 
	# fragment_data.to_excel(writer)
	# writer.save()

	# connect to DB
	conn = db.connect(DB_name)
	cursor = conn.cursor()

	new_fragment_name_list = []
	print("Seq_name\tFragment\tAAseq\tName\tInstock\tNTseq")
	for index in  fragment_data.index:
		# for each virus, open a file for its all 4 fragments
		seq_name = fragment_data.loc[index,"Name"]
		seq_fragment_file_name = "Fragments/" + seq_name.replace("/","_") + ".fas"
		temp_file = open(seq_fragment_file_name, "w")
		
		for i in range(num_fragment):
			aa_col_name = "F_AA_" + str(i + 1) + "_refine"
			nt_col_name = "F_NT_" + str(i + 1)

			aa_seq = fragment_data.loc[index,aa_col_name]
			nt_seq = fragment_data.loc[index,nt_col_name]
			
			# search from SQL DB
			SQLCommand = "SELECT * FROM Fragments WHERE AAseq = '" + aa_seq + "'"
			cursor.execute(SQLCommand)
			row = cursor.fetchone()

			if(row != None):
				fragment_name = row[0]
				nt_seq = row[7]
				in_stock = row[8]
			else:
				SQLCommand = "SELECT Name FROM Fragments WHERE Fragment = '" + str(i + 1) + "' AND Subtype = '" + subtype + "'"
				cursor.execute(SQLCommand)
				row = cursor.fetchall()
				num_id = str(len(row) + 1)
				num_id_len = len(num_id)
				num_id = "0" * (4-num_id_len) + num_id

				fragment_name = subtype + "-F" + str(i + 1) + "-" + num_id
				in_stock = "no"
				fragment = str(i + 1)
				if("H" in subtype):
					segment = "HA"
				else:
					segment = "NA"

				SQLCommand =  'INSERT INTO Fragments(`Name`, `Segment`, `Fragment`, `Subtype`, `ID`, `Template`, `AAseq`, `NTseq`, `Instock`) VALUES(' \
				+ "'" + fragment_name + "'," \
				+ "'" + segment + "'," \
				+ "'" + fragment + "'," \
				+ "'" + subtype + "'," \
				+ "'" + num_id + "'," \
				+ "'" + seq_name + "'," \
				+ "'" + aa_seq + "'," \
				+ "'" + nt_seq + "'," \
				+ "'" + in_stock + "')"

				try:
					cursor.execute(SQLCommand)
				except db.Error:
					print("error happen when insert!")
					print(SQLCommand)
				else:
					conn.commit()

				new_fragment_name_list.append(fragment_name)

			#print(seq_name + "\t" + str(i + 1) + "\t" + aa_seq + "\t" + fragment_name + "\t" + in_stock + "\t" + nt_seq)
			print(seq_name + "\t" + str(i + 1) + "\t" +  fragment_name + "\t" + in_stock )
			temp_file.write(">" + seq_name + "-Fragment" + str(i + 1) + "(" + fragment_name + ")" + "\n")
			temp_file.write(nt_seq + "\n")

			SnapGene_file_name = "SnapGene/" + seq_name.replace("/","_") + "-Fragment" + str(i + 1) + ".fas"
			snapgene_temp_file = open(SnapGene_file_name, "w")
			snapgene_temp_file.write(">" + seq_name + "-Fragment" + str(i + 1) + "(" + fragment_name + ")" + "\n")
			snapgene_temp_file.write(nt_seq + "\n")
			snapgene_temp_file.close()
			
		temp_file.close()

	print("\n")
	# print new fragments
	for x in new_fragment_name_list:
		SQLCommand = "SELECT * FROM Fragments WHERE Name = '" + x + "'"
		cursor.execute(SQLCommand)
		row = cursor.fetchone()
		if(row != None):
			print(row[0], row[6], row[7], row[8])
		else:
			print(x)

	# close DB connection
	conn.close



# test data
raw_file = open('H3_8.csv', "r")
raw_seq = raw_file.read()
raw_sequences = raw_seq.split("\n")

data = []

for cur_raw_seq in raw_sequences:
	tmp = cur_raw_seq.split(",")
	data.append(tmp)


data=pd.DataFrame(data=data)
data.columns=['Name', 'AAseq', 'NTseq']
subtype = "H3"
generate_fragments(data,subtype)




