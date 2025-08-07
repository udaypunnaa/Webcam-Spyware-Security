# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['webcam_security_interface.py'],
    pathex=[],
    binaries=[],
    datas=[('webcam-icon.png', '.'), ('simple_firebase.py', '.'), ('simple_face_detection.py', '.'), ('disable_cam.bat', '.'), ('enable_cam.bat', '.'), ('project_info_new.html', '.'), ('haarcascade_frontalface_default.xml', '.')],
    hiddenimports=['cv2', 'requests', 'tkinter', 'tkinter.messagebox', 'tkinter.simpledialog', 'tkinter.scrolledtext', 'PIL.Image', 'PIL.ImageTk', 'numpy'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Webcam_Security_App',
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
)
