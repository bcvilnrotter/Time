import sys
from cx_Freeze import setup, Executable

executables = [
    Executable("time.py", appendScriptToExe=True, appendScriptToLibrary=False)
]

buildOptions = {"includes": ["re"]}

setup(
    name = "time",
    version = "0.0.0.1",
    description = "time project",
    option = dict(build_exe = buildOptions),
    executables = executables)
