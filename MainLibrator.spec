# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(5000)

block_cipher = None

added_files = [
             ('./Data/*','Data'),
             ('./Conf/db_record.txt','Conf'),
             ('./Conf/Default','Conf/Default'),
             ('./Conf/db_record.txt','Temp'),
             ('./PDB/4jtv.cif','PDB'),
             ('./PDB/4jtv-ba1.pdb','PDB'),
             ('./PDB/4hmg.cif','PDB'),
             ('./Tools/*','Tools'),
             ('./Js/*','Js'),
             ('./codon_usage_data','codon_usage_data'),
             ('./python_codon_tables','python_codon_tables')
             ]

a = Analysis(['MainLibrator.py'],
             pathex=['./'],
             binaries=[],
             datas=added_files,
             hiddenimports=['cmath','openpyxl'],
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
              'NSHumanReadableCopyright':"Copyright @ 2022, Wilson Lab, All Rights Reserved",
              'NSHighResolutionCapable': 'True'
             })
