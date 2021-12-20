# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(5000)

block_cipher = None

added_files = [
             ('/Users/lel4003/Documents/Projects/Librator/Librator/Data/*','Data'),
             ('/Users/lel4003/Documents/Projects/Librator/Librator/Conf/db_record.txt','Conf'),
             ('/Users/lel4003/Documents/Projects/Librator/Librator/Conf/Default','Conf/Default'),
             ('/Users/lel4003/Documents/Projects/Librator/Librator/Conf/db_record.txt','Temp'),
             ('/Users/lel4003/Documents/Projects/Librator/Librator/PDB/4jtv.cif','PDB'),
             ('/Users/lel4003/Documents/Projects/Librator/Librator/PDB/4jtv-ba1.pdb','PDB'),
             ('/Users/lel4003/Documents/Projects/Librator/Librator/PDB/4hmg.cif','PDB'),
             ('/Users/lel4003/Documents/Projects/Librator/Librator/Tools/*','Tools'),
             ('/Users/lel4003/Documents/Projects/Librator/Librator/Js/*','Js'),
             ('/Users/lel4003/Documents/Projects/Librator/codon_usage_data','codon_usage_data'),
             ('/Users/lel4003/Documents/Projects/Librator/python_codon_tables','python_codon_tables')
             ]

a = Analysis(['MainLibrator.py'],
             pathex=['/Users/lel4003/Documents/Projects/Librator/Librator'],
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
