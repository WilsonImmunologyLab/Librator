# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(5000)

block_cipher = None

added_files = [
             ('/Users/leil/Documents/Projects/Librator/Librator/Data/*','Data'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Conf/db_record.txt','Conf'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Conf/Default','Conf/Default'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Conf/db_record.txt','Temp'),
             ('/Users/leil/Documents/Projects/Librator/Librator/PDB/4jtv.cif','PDB'),
             ('/Users/leil/Documents/Projects/Librator/Librator/PDB/4jtv-ba1.pdb','PDB'),
             ('/Users/leil/Documents/Projects/Librator/Librator/PDB/4hmg.cif','PDB'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Tools/*','Tools'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Js/*','Js'),
             ('/Users/leil/Documents/Projects/Librator/codon_usage_data','codon_usage_data'),
             ('/Users/leil/anaconda3/lib/python3.7/site-packages/python_codon_tables','python_codon_tables')
             ]

a = Analysis(['MainLibrator.py'],
             pathex=['/Users/leil/Documents/Projects/Librator/Librator'],
             binaries=[],
             datas=added_files,
             hiddenimports=['cmath'],
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
              'NSHumanReadableCopyright':"Copyright @ 2021, Wilson Lab, All Rights Reserved",
              'NSHighResolutionCapable': 'True'
             })
