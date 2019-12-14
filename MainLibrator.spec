# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
             ('/Users/leil/Documents/Projects/Librator/Resources/Data/H1_AAVI.csv','Data'),
             ('/Users/leil/Documents/Projects/Librator/Resources/Data/H1_PCT.csv','Data'),
             ('/Users/leil/Documents/Projects/Librator/Resources/Data/H3_AAVI.csv','Data'),
             ('/Users/leil/Documents/Projects/Librator/Resources/Data/H3_PCT.csv','Data'),
             ('/Users/leil/Documents/Projects/Librator/Resources/Data/NA_AAVI.csv','Data'),
             ('/Users/leil/Documents/Projects/Librator/Resources/Data/NA_PCT.csv','Data'),
             ('/Users/leil/Documents/Projects/Librator/Resources/Data/template.html','Data'),
             ('/Users/leil/Documents/Projects/Librator/Resources/Data/template1.html','Data'),
             ('/Users/leil/Documents/Projects/Librator/Resources/Conf/db_record.txt','Conf'),
             ('/Users/leil/Documents/Projects/Librator/Resources/Conf/db_record.txt','Temp'),
             ('/Users/leil/Documents/Projects/Librator/Resources/Tools/raxml','Tools'),
             ('/Users/leil/Documents/Projects/Librator/Resources/Tools/muscle','Tools'),
             ('/Users/leil/Documents/Projects/Librator/Resources/Tools/clustalo','Tools'),
             ('/Users/leil/Documents/Projects/Librator/Resources/Js/echarts.min.js','Js'),
             ('/Users/leil/Documents/Projects/Librator/Resources/Js/jquery.js','Js')
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
