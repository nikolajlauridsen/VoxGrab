"""setup script for creating windows executable with cx_freeze"""
import sys
from cx_Freeze import setup, Executable
import requests
import os
from VoxGrab import VERSION

# Set missing path variables
python_path = r"C:\Users\EUC\AppData\Local\Programs\Python\Python35"
os.environ['TCL_LIBRARY'] = os.path.join(python_path, "tcl", "tcl8.6")
os.environ['TK_LIBRARY'] = os.path.join(python_path, "tcl", "tk8.6")

package_list = ['VoxGrab', 'requests', 'tkinter', 'hashlib',
                'os', 're', 'queue', 'threading', 'sys', 'idna']

# Required files in include folder:
# tk86t.dll
# tcl86t.dll
# From the tcl subfolder of the python folder
build_exe_options = {"packages": package_list,
                     "include_files": [os.path.join("include", file) for file
                                       in os.listdir("include")] +
                     [requests.certs.where()]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

exe = Executable("VoxGrab.pyw",
                 base=base,
                 targetName="VoxGrab.exe")

setup(name="VoxGrab",
      version=VERSION,
      description="Hassle free subtitles",
      options={"build_exe": build_exe_options},
      executables=[exe])
