#region Imports
import sys
from cx_Freeze import setup, Executable # don't have it  pip install cx_Freeze then it should work
#enregion

include_files = ['autorun.inf']
base = None

if sys.platform == "win32":
    base = "Win32GUI"

setup(name="puzzle",
      version="0.1",
      description="Fun computer game",
      options={'build_exe': {'include_files': include_files}},
      executable=[Executable("client.py", base=base)])