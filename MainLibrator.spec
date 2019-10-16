# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['MainLibrator.py'],
             pathex=['/Users/leil/Documents/Projects/Librator/Librator'],
             binaries=[],
             datas=[],
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
          console=False , icon='Flu.icns')
app = BUNDLE(exe,
             name='MainLibrator.app',
             icon='Flu.icns',
             bundle_identifier=None,
             info_plist={
              'NSHumanReadableCopyright':"Copyright @ 2019, Wilson Lab, All Rights Reserved",
              'NSHighResolutionCapable': 'True'
             })
