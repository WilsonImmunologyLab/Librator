# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
             ('/Users/leil/Documents/Projects/Librator/Librator/Data/H1_AAVI.csv','Data'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Data/H1_PCT.csv','Data'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Data/H3_AAVI.csv','Data'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Data/H3_PCT.csv','Data'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Data/NA_AAVI.csv','Data'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Data/NA_PCT.csv','Data'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Data/template.html','Data'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Data/template1.html','Data'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Data/template2.html','Data'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Data/template3.html','Data'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Data/template4.html','Data'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Data/template5.html','Data'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Data/template6.html','Data'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Data/template7.html','Data'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Conf/db_record.txt','Conf'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Conf/db_record.txt','Temp'),
             ('/Users/leil/Documents/Projects/Librator/Librator/PDB/4jtv.cif','PDB'),
             ('/Users/leil/Documents/Projects/Librator/Librator/PDB/4hmg.cif','PDB'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Tools/raxml','Tools'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Tools/muscle','Tools'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Tools/clustalo','Tools'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Js/echarts.min.js','Js'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Js/jquery.js','Js'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Js/phylotree.css','Js'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Js/phylotree.js','Js'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Js/underscore-min.js','Js'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Js/d3.js','Js'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Js/bootstrap.min.css','Js'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Js/bootstrap-theme.min.css','Js'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Js/bootstrap.min.js','Js'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Js/underscore-min.map','Js')
             ]


a = Analysis(['MainLibrator.py'],
             pathex=['/Users/leil/Documents/Projects/Librator/Librator'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=['hooks'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Librator',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Librator')
app = BUNDLE(coll,
             name='Librator.app',
             icon='Flu.icns',
             bundle_identifier=None,
             info_plist={
              'NSHumanReadableCopyright':"Copyright @ 2019, Wilson Lab, All Rights Reserved",
              'NSHighResolutionCapable': 'True'
             })
