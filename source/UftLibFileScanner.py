from MainWinClass import *
from tkinter import *
from tkinter.messagebox import *
import subprocess
import sys
import gc
p_name =b'MainWin.exe'
ctype={"VBSDoc":"ScanVbsFile","Normal":"ScanVbsFileNormal"}

def checkProcessExist(process_name):
    pl = subprocess.Popen('tasklist',stdout=subprocess.PIPE)
    proclist = pl.communicate()[0].splitlines()
    i=0
    for line in  proclist:
        if line.find(p_name)>=0:
            i+=1
    return i
   
class LaunchFileScan:
    def __init__(self):
        self.root=Tk()
        self.__commentType=StringVar()
        self.root.title("Choose Comment Type:")
        self.root.resizable(width = False, height = False)
        
    def __ClickCancel(self):
        self.__commentType.set('')
        self.root.destroy()

    def CommentType(self):
        return self.__commentType.get()

    def ChooseCommentType(self):
        Label(self.root, text="please select one comment type from list below:").pack(side = TOP)
        m1 = Frame(self.root)
        m1.pack(side= TOP)
        for key in sorted(ctype.keys()):
            Radiobutton(m1,text=key,variable= self.__commentType,value = ctype[key]).pack(anchor=NW)
        self.__commentType.set(ctype["VBSDoc"])
        m2= Frame(self.root)
        m2.pack(side=BOTTOM)
        Button(m2,text='OK',command=self.root.destroy).pack(side=LEFT)
        Button(m2,text="Cancel",command=self.__ClickCancel).pack(side=RIGHT)
        self.root.mainloop()

if __name__=="__main__":
    if checkProcessExist(p_name) >1:
##        showinfo(title='check process launched', message='too many')
        sys.exit()
##    else:
##        showinfo(title= 'check process launched' , message = str(i))
    lf = LaunchFileScan()
    lf.ChooseCommentType()
    module = lf.CommentType()
    del lf
    gc.collect()
    if module!='':
        mw = MainWin(module)
        mw.SetVersion('1.33')
        mw.Show()
        del mw
        gc.collect()
