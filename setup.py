from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
import sys

buildOptions = dict(packages=[], excludes=[])

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('main.py', base=base, targetName='AutoPauseMC.exe')
]

setup(name='AutoPauseMC',
      version='0.1',
      description='Automatically suspend minecraft process.',
      options=dict(build_exe=buildOptions),
      executables=executables,
      requires=['psutil', 'win32gui', 'wxPython'])
