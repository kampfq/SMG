# -*- mode: python -*-
a = Analysis(['update.py'],
             pathex=['C:\\Users\\martijn\\Documents\\Python\\automatisering\\backups\\guiv2 [DO NOT TOUCH]\\Dist\\update'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'update.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=True , icon='C:\\Users\\martijn\\Documents\\Python\\automatisering\\Icons\\favicon.ico')
