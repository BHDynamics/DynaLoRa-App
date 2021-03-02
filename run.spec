# -*- mode: python ; coding: utf-8 -*-

import platform

block_cipher = None

a = Analysis(['run.py'],
           pathex=[],
           binaries=[],
           datas=[('./dongle/data/cnf/app.json', './dongle/data/cnf/'), ('./dongle/data/cnf/dongle_ui.json', './dongle/data/cnf/'), ('./dongle/data/cnf/bhDynamics.ico', './dongle/data/cnf/'), ('./dongle/data/cnf/banner.png', './dongle/data/cnf/')],
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
         name='dynaLoRa-App',
         debug=False,
         strip=False,
         icon='bhDynamics.ico',
         upx=True,
         runtime_tmpdir=None,
         console=False )

if platform.system() == 'Darwin':
    info_plist = {'addition_prop': 'additional_value'}
    app = BUNDLE(exe,
                 name='dynaLoRa-App.app',
                 bundle_identifier=None,
                 icon='logo.icns'
                 info_plist=info_plist
                 )