# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['LightPubGUI.py', 'NovelFullBook.py'],
    pathex=['.'],
    binaries=[('C:\\Users\\chris\\Documents\\LightPub\\.venv\\lib\\python3.12\\site-packages\\pypub', 'pypub')],
    datas=[],
    hiddenimports=['pypub3', 'lxml'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
a.datas += [('light_pub_icon.png', 'C:\\Users\\chris\\Documents\\LightPub\\light_pub_icon.png', 'DATA')]
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='LightPubGUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='light_pub_icon.png'
)