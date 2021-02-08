# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['run.py'],
           pathex=['C:\\Users\\alper\\Workspace\\Dongle-App\\dongle-app'],
           binaries=[],
           datas=[('./dongle/data/cnf/app.json', './dongle/data/cnf/'), ('./dongle/data/cnf/dongle_ui.json', './dongle/data/cnf/')],
           hiddenimports=['uuid', 'time', 'decimal', 'serial', 'threading'],
           hookspath=[],
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
         name='dongle-app',
         debug=False,
         strip=False,
         upx=True,
         runtime_tmpdir=None,
         console=True )