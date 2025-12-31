# -*- mode: python ; coding: utf-8 -*-
import os
import sys

block_cipher = None

# Get the project root directory relative to this spec file
# SPEC is the path to the spec file
spec_dir = os.path.dirname(os.path.abspath(SPEC))
root_dir = os.path.dirname(spec_dir)

# Add src to sys.path for analysis
sys.path.insert(0, os.path.join(root_dir, 'src'))

a = Analysis(
    [os.path.join(root_dir, 'src', 'main.py')],
    pathex=[os.path.join(root_dir, 'src')],
    binaries=[],
    datas=[
        (os.path.join(root_dir, 'assets', 'Ledger.ico'), 'assets'),
    ],
    hiddenimports=['pdfplumber', 'pdfminer', 'pdfminer.six'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Ledger',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(root_dir, 'assets', 'Ledger.ico'),
)
