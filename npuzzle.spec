# PyInstaller build: pyinstaller npuzzle.spec
a = Analysis(
    ["src/npuzzle/__main__.py"],
    pathex=["src"],
    datas=[("src/npuzzle/assets", "npuzzle/assets")],
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    name="n-puzzle",
    console=False,
)
