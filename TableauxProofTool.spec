# -*- mode: python -*-
a = Analysis(['src/TableauxProofTool.py'],
             pathex=['/windows/D/Users/fabior/workspace/TableauxProofTool-v0.1'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='TableauxProofTool',
          debug=False,
          strip=None,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='TableauxProofTool')
