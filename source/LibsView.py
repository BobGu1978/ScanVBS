# coding=utf-8
from tkinter import *
from tkinter import ttk
from ScanTsp  import *
from VbsTrView import *
from ScrolledTreeView import *

import ScanVbsFile
import os.path
import os

class LibView(AnalysisTSP):
    """this class is to display all lib file names analysised from the tsp file into the tree view.also bind the event of left-mouse double-click """
    def __init__(self, parent=None,  rightview=None , filename=''):
        self.__count =0
        self.__Libs={}
        AnalysisTSP.__init__(self,filename)
        self.workdir = AnalysisTSP.WorkDir(self)
        self.fr = Frame(parent)
        self.fr.pack(expand = YES, fill=BOTH)
        self.treeView = ScrolledTreeview(self.fr)
        self.__rightView = rightview
        self.__menu = Menu(self.treeView, tearoff=0)
        self.__menu.add_command(label="do my Job", command=self.__donothing)
        self.treeView.bind('<Double-1>',self.__MyDBClick)
        self.treeView.bind('<Button-3>' , self.__showMenu)
    def SetRightView(self, rightview):
        self.__rightView = rightview
    def __donothing(self):
        print("doing nothing.")
    def __InertTreeView(self, data):
        """it inserts data to the tree view and store the item name as value of a dictionary key which is the ID of inserted item.
it will be used later when we trigger the double click event."""
        for i in data:
            key = self.treeView.insert('','end',text = i)
            self.__Libs[key]=i

    def __MyDBClick(self,event):
        """the callback method binded to left-mouse double-click event.it first get the selected item's ID, and gets the file name
with this ID which we have already stored as paire of key-value.then it generates instance of class MyTreeView and do the data-show."""
        mysel = self.treeView.selection()
        if mysel=="":
            print("OOPs, nothing is selected")
            return
        item = mysel[0]
        file = os.path.join(self.workdir,self.__Libs[item])
        (folder, filename) = os.path.split(file)
        if self.__rightView!=None:
            self.__rightView.Show( os.path.join(folder,filename))
    def __showMenu(self,event):
        mysel = self.treeView.selection()
        if mysel=="":
            print("OOPs, nothing is selected")
            return
        self.__menu.post(event.x_root,event.y_root)

    def __GetAllFiles(self):
        """it reads the file names from the folder, and only stores the files,
which have expected extension name from the module 'ScanVbsFile', and it returns trip of array,
which contains the file name and length of this array."""
        fl=[]
        for i in os.listdir(self.workdir):
            if os.path.isfile(os.path.join(self.workdir,i)):
                (fn,ext) = os.path.splitext(i)
                if ext.lower() in ScanVbsFile.filetype:
                    fl.append(i)
        return (fl,len(fl))

    def Show(self,filename=''):
        """this function is to analysis the lib files from the tsp, then do insert items to tree view ,
and bind left-mouse double click event with self-defined callback method. """
        libs=AnalysisTSP.GetLibs(self,filename)
        self.__count= len(libs)
        self.__InertTreeView(libs)

    def GetCount(self):
        """it returns the count of the items in the tree view."""
        return self.__count

    def ShowWithoutAnalys(self,filefolder):
        """this function is to get lib files from the folder instead of tsp file. """
        self.workdir = os.path.abspath(filefolder)
        (libs,self.__count)= self.__GetAllFiles()
        self.__InertTreeView(libs)

def test():
    rt= Tk()
    lf = Frame(rt)
    lf.pack(side=LEFT, expand = YES , fill= BOTH)
    rf = Frame(rt)
    rf.pack(side=RIGHT , expand=YES, fill = BOTH)
    rv = MyTreeView("ScanVbsFileNormal",rf)
    lv = LibView(lf,rv,'C:\\WORK\\GSCS\\automation\\RM\\example\\My Own\\PrimitiveTest\\PrimitiveTest\\Test.tsp')
    lv.Show()
    rt.mainloop()


if __name__=='__main__': test()

