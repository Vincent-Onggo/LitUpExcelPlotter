from cx_Freeze import setup, Executable
import sys

build_exe_options = {
    "packages": ["os"],
    "excludes": ["tkinter"],
    "include_files": ["plotter.py"],  # Add any additional files your app needs
}

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

executables = [
    Executable("app.py", base=base)
]

setup(
    name="MyApp",
    version="1.0",
    description="My application description",
    options={"build_exe": build_exe_options},
    executables=executables
)
