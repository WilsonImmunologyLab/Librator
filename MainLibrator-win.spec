# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
             (r'C:\Users\leili\Documents\GitHub\Librator\Data\*','Data'),
             (r'C:\Users\leili\Documents\GitHub\Librator\Conf\db_record.txt','Conf'),
             (r'C:\Users\leili\Documents\GitHub\Librator\Conf\Default','Conf/Default'),
             (r'C:\Users\leili\Documents\GitHub\Librator\Conf\db_record.txt','Temp'),
             (r'C:\Users\leili\Documents\GitHub\Librator\PDB\4jtv.cif','PDB'),
             (r'C:\Users\leili\Documents\GitHub\Librator\PDB\4hmg.cif','PDB'),
             (r'C:\Users\leili\Documents\GitHub\Librator\Tools\*','Tools'),
             (r'C:\Users\leili\Documents\GitHub\Librator\Js\*','Js'),
             (r'C:\Users\leili\Documents\GitHub\Librator\codon_usage_data','codon_usage_data'),
             (r'C:\Users\leili\Documents\GitHub\Librator\python_codon_tables','python_codon_tables')
             ]


a = Analysis(['MainLibrator.py'],
             pathex=[r'C:\Users\leili\Documents\GitHub\Librator'],
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
              'NSPrincipalClass': 'NSApplication',
              'NSAppleScriptEnabled': False,
              'NSHumanReadableCopyright':"Copyright @ 2021, Wilson Lab, All Rights Reserved",
              'NSHighResolutionCapable': 'True'
             })
