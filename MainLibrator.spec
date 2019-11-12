# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
             ('/Users/leil/Documents/Projects/Librator/Librator/Resources/HA_AAVI.csv','.'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Resources/HA_PCT.csv','.'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Resources/NA_AAVI.csv','.'),
             ('/Users/leil/Documents/Projects/Librator/Librator/Resources/NA_PCT.csv','.'),
             ('/Users/leil/Documents/Projects/Librator/Librator/PDB/3hto.pdb','.'),
             ('/Users/leil/Documents/Projects/Librator/Librator/PDB/4hmg.pdb','.'),
             ('/Users/leil/Documents/Projects/Librator/Librator/PDB/4jtv.pdb','.'),
             ('/Users/leil/Documents/Projects/Librator/Librator/PDB/3lzg.pdb','.'),
             ('/Users/leil/Documents/Projects/Librator/Librator/PDB/1ruz.pdb','.'),
             ('/Users/leil/Documents/Projects/Librator/Librator/PDB/1ru7.pdb','.'),
             ('/Users/leil/Documents/Projects/Librator/Librator/PDB/1ru7.pdb','.')
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='MainLibrator',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , 
          icon='Flu.icns')
app = BUNDLE(exe,
             name='MainLibrator.app',
             icon='Flu.icns',
             bundle_identifier=None,
             info_plist={
              'NSHumanReadableCopyright':"Copyright @ 2019, Wilson Lab, All Rights Reserved",
              'NSHighResolutionCapable': 'True'
             })
