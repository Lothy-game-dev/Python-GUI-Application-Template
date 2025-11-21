# -*- mode: python ; coding: utf-8 -*-
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules
from PyInstaller.building.api import PYZ, EXE, COLLECT

# Define block_cipher (None if not using encryption)
block_cipher = None

hidden_imports = [
    "PyQt5",
    "PyQt5.QtWebEngineWidgets",
    "PyQt5.QtWidgets",
    "PyQt5.QtCore",
    "engineio.async_drivers.threading",
    "flask",
    "io",
    "flask_socketio",
    "flask.helpers",
    "flask.send_file",
    "threading",
    "multiprocessing",
    "waitress",
    "PyMuPDF",
    "pdfplumber",
]

binaries = [
    (
        "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/pypdfium2_raw/libpdfium.dylib",
        "pypdfium2_raw",
    ),
    (
        "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/pypdfium2_raw/version.json",
        "pypdfium2_raw",
    ),
    (
        "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/pypdfium2/version.json",
        "pypdfium2",
    ),
]
datas = [
    ('../app/static/testing_files/standard_files/mojiichiran.pdf', 'app/static/testing_files/standard_files'),

    ('../app/static/js/script.js', 'app/static/js'),
    ('../app/static/js/menu-control.js', 'app/static/js'),
    ('../app/static/js/socket.js', 'app/static/js'),

    ('../app/static/constants/tabs.constant.js', 'app/static/constants'),

    ('../app/static/css/styles.css', 'app/static/css'),
    ('../app/static/css/test.css', 'app/static/css'),

    ('../app/templates/app.html', 'app/templates'),
    ('../app_run.py','.'),
    ('../waitress_server/server.py', 'waitress_server'),
    ('../gui/main_window.py','gui'),
    ('../app/__init__.py','app'),
    ('../app/config.py','app'),
    ('../app/routes.py','app'),
    ('../app/hidden_web_run.py','app'),
    ('../scripts/common/main.py','scripts/common'),
    ('../scripts/e_tax/color_pdf_file.py','scripts/e_tax'),
    ('../scripts/e_tax/color_xlsx_file.py','scripts/e_tax'),
    ('../scripts/e_tax/helper.py','scripts/e_tax'),
    ('../scripts/e_tax/main.py','scripts/e_tax'),
    ('../scripts/navitime/helper.py','scripts/navitime'),
    ('../scripts/navitime/main.py','scripts/navitime'),
    ('../.env','.'),
]

a = Analysis(
    ["../app_run.py"],
    pathex=["."],
    binaries=binaries,
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name="e-Tax",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    onefile=True,
    onedir=True,
    windowed=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="launcher",
)
