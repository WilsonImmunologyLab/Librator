__author__ = 'wilsonp'
import sqlite3 as db
import os
# first need connect to a database
from LibDialogues import openFile, openFiles, newFile, questionMessage, setText

def creatnewDB(DBpathname):

    (dirname, filename) = os.path.split(DBpathname)

    os.chdir(dirname)
    # print(dirname)


    conn = db.connect(DBpathname)
    cursor = conn.cursor()
    cursor.execute('drop table if exists LibDB')

    cursor.execute("create table LibDB(SeqName text PRIMARY KEY NOT NULL, Sequence text, SeqLen, SubType text, Form text, VFrom text, VTo text, Active text, Role text, Donor text, Mutations text, ID)")
    # ID PRIMARY KEY,

    conn.commit()
    conn.close()



def CopyDatatoDB2(SQLSELECT, DBpathname, DB2path):
    # (dirname, filename) = os.path.split(DBpathname)
    conn = db.connect(DBpathname)
    cursor = conn.cursor()


    # ATTACH DATABASE "\mydir\data\beta.sqlite\" AS beta;
    # CREATE TABLE NewTable AS
    # SELECT * FROM beta.table3;
    # DETACH DATABASE beta;

    # INSERT INTO blog_posts
    # SELECT * FROM BlogProduction.dbo.blog_posts
    SQLStatement = 'ATTACH DATABASE "'+ DB2path + '" AS "DB2"'
    SQLStatement2 = 'INSERT INTO DB2.LibDB '+ SQLSELECT #SELECT * FROM LibDB WHERE ...' #'INSERT INTO + ' "' + LibDB.DB2 ' + '" '+ SQLSELECT #SELECT * FROM LibDB WHERE ...'
    SQLStatement3 = 'DETACH DATABASE DB2'
    try:
        cursor.execute(SQLStatement)
        cursor.execute(SQLStatement2)
        cursor.execute(SQLStatement3)
    except:

        print(SQLStatement + ', '+ SQLStatement2 + ', '+ SQLStatement3)


def UpdateMulti(SQLCommand, DBpathname):
    (dirname, filename) = os.path.split(DBpathname)

    os.chdir(dirname)
    # print(dirname)


    conn = db.connect(DBpathname)
    cursor = conn.cursor()
    # cursor.execute('drop table if exists LibDB')

    # SQLCommand = 'UPDATE LibDB SET ' + Field + ' = "' + Value + '" WHERE ID = ' + ID
    # if Field == 'SeqAlignment':
    #     SQLCommand = 'UPDATE LibDB SET Isotype = "' + Value + '" WHERE ID = ' + ID
    try:
        cursor.execute(SQLCommand)
    except:
        print(SQLCommand)
    # SQLCommand = 'UPDATE LibDB SET SeqName = "DeletionSeq2", V1 = "333" WHERE ID = 7'

    # ID PRIMARY KEY,

    conn.commit()
    conn.close


def UpdateField(ID, Value, Field, DBpathname):
    (dirname, filename) = os.path.split(DBpathname)

    os.chdir(dirname)
    # print(dirname)


    conn = db.connect(DBpathname)
    cursor = conn.cursor()
    # cursor.execute('drop table if exists LibDB')
    # nID = str(ID)
    SQLCommand = 'UPDATE LibDB SET ' + Field + ' = "' + Value + '" WHERE SeqName = ' + '"' + ID + '"'
    # if Field == 'SeqAlignment':
    #     SQLCommand = 'UPDATE LibDB SET Isotype = "' + Value + '" WHERE ID = ' + ID
    try:
        cursor.execute(SQLCommand)
    except:
        print(SQLCommand)
    # SQLCommand = 'UPDATE LibDB SET SeqName = "DeletionSeq2", V1 = "333" WHERE ID = 7'

    # ID PRIMARY KEY,

    conn.commit()
    conn.close




def ProcessFASTA(FASTAfile):
    ErLog = ''
    ErlogFile = ''
    import os
    # FASTAfile = os.path.join(os.path.expanduser('~'), 'Dropbox', 'VGenes', 'Database', 'ALLIMGT.nt')
    if FASTAfile == '':
        return

    with open(FASTAfile, 'r') as currentFile:  #using with for this automatically closes the file even if you crash

        Newline = ''
        Titleline = ''
        ErLog = ''
        CleanSeq = ''
        for FASTAline in currentFile:

            FASTAline = FASTAline.replace('\n', '').replace('\r', '')
            if FASTAline == '':
                FASTAline = ' '

            if FASTAline[0] == '>':
                if len(Newline) > 1:
                    Titleline += '\n'
                    Newline += '\n'
                    CleanSeq += Titleline + Newline
                else:
                    if Newline != ' ' or  Newline != '':
                        if Titleline != '':
                            ErLog += Titleline + ': Sequence error\n'

                Titleline = FASTAline
                Newline = ''
            else:
                FASTAline = FASTAline.upper()
                for nuc in FASTAline:
                    if nuc == 'N' or nuc == 'A' or nuc == 'T' or nuc == 'G' or nuc == 'C' or nuc == '.':
                        Newline += nuc
        # need to write the last sequence into the FASTA file
        if len(Newline) > 1:
            Titleline += '\n'
            Newline += '\n'
            CleanSeq += Titleline + Newline
        else:
            if Newline != ' ' or  Newline != '':
                ErLog += Titleline + '\n'




    return CleanSeq


def enterData(DBpathname, LibratorSeqs):

    (dirname, filename) = os.path.split(DBpathname)

    os.chdir(dirname)


    conn = db.connect(DBpathname)
    #  then need to create a cursor that lets you traverse the database
    cursor = conn.cursor()
    # todo must remember when adding fields to change all of this to fit
    TopNum = 0
    cursor.execute('''SELECT max(ID) FROM LibDB''')  #code to add unique primary keys
    row = cursor.fetchone()
    if row[0] == None:
        TopNum = 0
    else:
        TopNum = int(row[0])
    #to get a unique ID
    # need IgBLASTAnalysis to be list of lists for above operation because tupels are immuntable
    # then convert to a list of tuples for the expandall to work
    numberprocessed = 0
    FinalBLASTed = []
    ErlogFile = '/Applications/Librator/ErLog.txt'
    # ErLog = ''
    # Recordlen = 0
    # ToAllAnswer = 'none'
    # if answer3 == "YesAll":
    #     ToAllAnswer = 'Yes'
    # elif answer3 == 'NoAll':
    #     ToAllAnswer = 'No'

    for item in LibratorSeqs:

        # todo add code to check each seqname and verify not in the currently open db before adding
        uId = item[0]
        # queryis = 'SELECT SeqName FROM LibDB WHERE SeqName = ' + seqnamed
        cursor.execute("SELECT SeqName FROM LibDB WHERE SeqName=:Id", {"Id": uId})

        # cursor.execute(queryis)  #code to check if seqname is already in db
        row = cursor.fetchone()

        exists = True
        if row == None:
            exists = False

        else: #seq already exists with same name


            query = 'Save duplicated sequence with a new name?'
            answer2 = questionMessage(query, 'YN')
            if answer2 == "Yes":
                query = 'Existing name: ' + uId + '\nEnter a new name:'
                DefaultTxt = uId + '_duplicate'
                newName = setText(query, DefaultTxt)
                item[0] = newName
                exists = False



        if exists == False:
            Recordlen = len(item)
            # if answer3 == 'No' or answer3  == 'NoAll':

            if Recordlen == 12:
                TopNum += 1
                # item[6]  = TopNum    #append a unique seqID

                FinalBLASTed.append(tuple(item))
                numberprocessed +=1



    if len(FinalBLASTed) > 0:
        cursor.executemany('''INSERT INTO LibDB(SeqName, Sequence, SeqLen, SubType, Form, VFrom, VTo, Active, Role, Donor, Mutations, ID) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)''', FinalBLASTed)
    #  SeqName, Sequence text, SeqLen, SubType text, Form text, VFrom text, VTo text, Active text, Role text, Donor text, Mutations text, ID



    conn.commit()  #  saves data into file
    conn.close()
    # readData(DBpathname)

    return numberprocessed

def RunInsertion(DBpathname, SQLStatement):
    import os

    (dirname, filename) = os.path.split(DBpathname)
    os.chdir(dirname)
    conn = db.connect(DBpathname)
    cursor = conn.cursor()
    response = cursor.execute(SQLStatement)
    if response.rowcount == 1:
        conn.commit()
        cursor.close()
        conn.close()
        return 1
    else:
        cursor.close()
        conn.close()
        return 0


def RunSQL(DBpathname, SQLStatement):
    # returns a dictionary with seqname as key and all other fileds  as a list as data
    # Note: always needs SeqName to be first field SQLed
    import os

    (dirname, filename) = os.path.split(DBpathname)

    os.chdir(dirname)


    conn = db.connect(DBpathname)
    #  then need to create a cursor that lets you traverse the database
    cursor = conn.cursor()

    if SQLStatement == 'None':
        cursor.execute('''SELECT * FROM LibDB''')
    else:
        cursor.execute(SQLStatement)

    DataIs = []
    KeyName  = ''
    Fields = []
    # rows = cursor.rowcount
    for row in cursor:
        # i = 0
        Fields.clear()
        for column in row:
            # if i == 0:
            #     KeyName = column
            # else:
            Fields.append(column)
            # i +=1

        DataIs.append(tuple(Fields))


    # conn.commit()  #  saves data into file
    conn.close()

    return DataIs


def ImportVDB(pathname, DBFilename):
    (dirname, filename) = os.path.split(DBFilename)

    os.chdir(dirname)


    conn = db.connect(DBFilename)
    #  then need to create a cursor that lets you traverse the database
    cursor = conn.cursor()
    pathname+= '.LibDB'
    cursor.execute('''ATTACH pathname as VGDB2''')
    cursor.execute('''SELECT * FROM VGDB2''')
    DataIs = []
    for row in cursor:
        for column in row:
            DataIs.append(column)


    cursor.execute('''INSERT INTO DBpathname.LibDB SELECT * FROM VGDB2.LibDB''')

    conn.close()

def readData(DBpathname, SQLStatement):
    import os

    (dirname, filename) = os.path.split(DBpathname)

    os.chdir(dirname)


    conn = db.connect(DBpathname)
    #  then need to create a cursor that lets you traverse the database
    cursor = conn.cursor()

    if SQLStatement == 'None':
        cursor.execute('''SELECT * FROM LibDB''')
    else:
        cursor.execute(SQLStatement)

    DataIs = []
    # rows = cursor.rowcount
    for row in cursor:
        for column in row:
            DataIs.append(column)

    # conn.commit()  #  saves data into file
    conn.close()

    return DataIs

def FetchOneRecord(databasename):

    conn = db.connect(databasename)
    #  then need to create a cursor that lets you traverse the database
    cursor = conn.cursor()
    #  then need to create a cursor that lets you traverse the database

    # #can use sql to determine averages
    cursor.execute('select avg(temp) from temps')
    row = cursor.fetchone()

    conn.close()
    print('The average temp for the week was: %s' % row[0])

def deleterecords (DBFilename, SQLStatement):
    import os


    (dirname, filename) = os.path.split(DBFilename)

    os.chdir(dirname)


    conn = db.connect(DBFilename)
    #  then need to create a cursor that lets you traverse the database
    cursor = conn.cursor()
    # SQLStatement2 = 'DELETE' + SQLStatement[18:]
    try:
        if SQLStatement != 'None':
            cursor.execute(SQLStatement)
    except:
        SQLStatement2 = 'DELETE FROM LibDB WHERE Project = "Delete"'
        cursor.execute(SQLStatement)



    # CommandSql = 'delete from LibDB where temp = ' + searchvalue
    # cursor.execute('delete from temps where temp = 40')

    # # need to requery and fetch data to display with changes
    # cursor.execute('select * from temps')
    # rows = cursor.fetchall()
    # for row in rows:
    #     print('%s %s' % (row[0], row[1]))
    conn.commit()
    conn.close()





def MakeSQLStatement(self, fields, SeqName):


    checkedProjects, checkedGroups, checkedSubGroups, checkedkids = self.getTreeChecked()

    SQLStatement = 'SELECT '

    if fields != 'All':
        fieldCount = len(fields)
        i = 1
        for field in fields:
            SQLStatement += field
            if i < fieldCount:
                SQLStatement += ', '
            else:
                SQLStatement += ' FROM LibDB'
            i += 1
    else:
        SQLStatement += '* FROM LibDB'  # 'SELECT * FROM LibDB WHERE ID = '

    firstmore = False

    if (len(checkedProjects) + len(checkedGroups) + len(checkedSubGroups) + len(
            checkedkids)) > 0:  # then something is seleected
        SQLStatement += ' WHERE '
        firstmore = True
    else:
        SQLStatement += ' WHERE SeqName = "'
        SQLStatement += SeqName + '"'


    i = 1
    if len(checkedProjects) > 0:
        if firstmore == True:
            firstmore = False
        else:
            SQLStatement += ', '
            firstmore = False
        project = self.ui.cboTreeOp1.currentText()
        fieldname = self.TransLateFieldtoReal(project, True)
        SQLStatement = SQLStatement + fieldname + ' = '
        for item in checkedProjects:
            SQLStatement += ('"' + item)
            if i < len(checkedProjects):
                SQLStatement += '" OR ' + fieldname + ' = '
            else:
                SQLStatement += '"'
            i += 1

            # if len(checkedGroups) > 0: SQLStatement += ', OR '

    i = 1
    if len(checkedGroups) > 0:
        if firstmore == True:
            firstmore = False
        else:
            if len(checkedProjects) > 0:
                SQLStatement += ' OR '
            else:
                SQLStatement += ', '

            firstmore = False
        group = self.ui.cboTreeOp2.currentText()
        fieldname = self.TransLateFieldtoReal(group, True)
        project = self.ui.cboTreeOp1.currentText()
        Projfieldname = self.TransLateFieldtoReal(project, True)

        # SQLStatement = SQLStatement + fieldname + ' = "'
        for item in checkedGroups:
            statement = fieldname + ' = "' + item[1] + '" AND ' + Projfieldname + ' = "' + item[0]
            SQLStatement += statement
            if i < len(checkedGroups):
                SQLStatement += '" OR '
            else:
                SQLStatement += '"'
            i += 1

    i = 1
    if len(checkedSubGroups) > 0:
        if firstmore == True:
            firstmore = False
        else:
            if len(checkedProjects) > 0 or len(checkedGroups) > 0:
                SQLStatement += ' OR '
            else:
                SQLStatement += ', '
            firstmore = False
        Subgroup = self.ui.cboTreeOp3.currentText()
        fieldname = self.TransLateFieldtoReal(Subgroup, True)
        group = self.ui.cboTreeOp2.currentText()
        Groupfieldname = self.TransLateFieldtoReal(group, True)
        project = self.ui.cboTreeOp1.currentText()
        Projfieldname = self.TransLateFieldtoReal(project, True)

        # SQLStatement = SQLStatement + fieldname + ' = "'
        for item in checkedSubGroups:
            statement = fieldname + ' = "' + item[2] + '" AND ' + Groupfieldname + ' = "' + item[
                1] + '" AND ' + Projfieldname + ' = "' + item[0]
            SQLStatement += statement
            if i < len(checkedSubGroups):
                SQLStatement += '" OR '
            else:
                SQLStatement += '"'
            i += 1

    i = 1
    if len(checkedkids) > 0:
        if firstmore == True:
            firstmore = False
        else:
            if len(checkedProjects) > 0 or len(checkedGroups) > 0 or len(checkedSubGroups) > 0:
                SQLStatement += ' OR '
            else:
                SQLStatement += ', '
            firstmore = False

        for item in checkedkids:
            SQLStatement += 'SeqName = "'
            SQLStatement += item
            if i < len(checkedkids):
                SQLStatement += '" OR '
            else:
                SQLStatement += '"'
            i += 1

    return SQLStatement

