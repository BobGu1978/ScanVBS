from distutils.core import setup
import py2exe
import sys
 
#this allows to run it with a simple double click.
sys.argv.append('py2exe')
 
py2exe_options = {
        "includes": ["os",'re','tkinter','sys','codecs','chardet','gc','subprocess','ScanVbsFileNormal','ScanVbsFile'],
        "dll_excludes": ["MSVCP90.dll",],
        "compressed": 1,
        "optimize": 2,
        "ascii": 0,
        "bundle_files": 2,
        }
 
setup(
      name = 'My Tool',
      version = '1.33',
##      windows = ['MainWin.py',],
      windows = ['UftLibFileScanner.py',], 
      zipfile = None,
      data_files= [('icon',['.\\icon\\class.gif','.\\icon\\function.gif','.\\icon\\sub.gif','.\\icon\\property.gif'])],
      options = {'py2exe': py2exe_options}
      )
