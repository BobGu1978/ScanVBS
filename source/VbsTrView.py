#! /usr/bin/python
# coding=utf-8
from tkinter import *
from tkinter import ttk
##from ScanVbsFile  import *
from ScrolledTreeView import *
from MyText import *
from VbsStructure import *
import os,os.path
global scanmodule
class MyTreeView:
    """this class is to provide the methods to trigger the lib file scanning and information displaying. it need re-write and re-organize. """
    def __init__(self,module , parent=None,basefolder='',filename=''):
        if type(basefolder)!=type(''):
            raise TypeError("here string is needed, but it is %s" %type(basefolder))
        if type(filename)!=type(''):
            raise TypeError("here string is needed, but it is %s" %type(filename))
        bt = basefolder
        if bt!='':
            if bt[-1] != '\\':
                bt= bt+'\\'
        self.fullPath = os.path.join(bt,filename)
        self.module = __import__(module)
        self.sv = self.module.ScanVbs()
        self.topfr = Frame(parent)
        self.topfr.pack(side=TOP,expand=YES,fill=BOTH)
        self.treeView = ScrolledTreeview(self.topfr)
        self.treeView.bind('<ButtonRelease-1>',self.__MyClick)
        self.btmfr = Frame(parent)
        self.btmfr.pack(side=BOTTOM,expand=YES, fill=BOTH)
        self.text = MyTextView(self.btmfr)
        self.__ImgFolder = os.path.abspath(os.getcwd()+'.\\icon\\')
        self.__img={}
        self.__BindImg()
        self.__menu = Menu(self.treeView, tearoff=0)
        self.__menu.add_command(label="reload file", command=self.__reload)
        self.treeView.bind('<Button-3>' , self.__showMenu)
    def __showMenu(self,event):
        if not os.path.isfile(self.fullPath):
            return
        self.__menu.post(event.x_root,event.y_root)
    def __reload(self):
        self.Show()
##        print("doing nothing.")
    def __BindImg(self):
        """it is to create photoimage instance for images which are used for right tree view. and bind them with proper tags. """
        imgfolder = os.path.abspath(os.getcwd()+'.\\icon\\')
        sn = VbsStructure().ExportSector()
        for i in sn:
           fn = os.path.join(imgfolder , i + ".gif")
           self.__img[i]=PhotoImage(file=fn )
           self.treeView.tag_configure(i , image = self.__img[i])

    def __MyClick(self,event):
        """the callback method of left-mouse click. it retrieve the data from the selected item's tag which is stored when lib file is scanned, then display
the data in the text UI. """
        item = self.treeView.identify('item',event.x,event.y)
        mt = self.treeView.item(item ,'tags')
        self.text.config(state = NORMAL)
        if len(mt)<2:
            self.text.delete('1.0',END)
        else:
            self.text.delete('1.0',END)
            self.text.insert('1.0',''.join((mt[1] , '\r\n' , mt[-1])))
##            self.text.insert('end', mt[-1])
        self.text.config(state=DISABLED)
##        self.text.see('end')

    def __InertTreeView(self,sp,parentID=''):
        """it gets data from the structure generated after lib file scanning and insert items properly into the treeview with their related information."""
        if type(sp)!=type({}):
            raise TypeError("internal error that data strucutre is not get")
        for name in sorted(sp.keys()):
            for sectName in sorted(sp[name].keys()):
                if name == self.sv.nameofClass():
                    newID = self.treeView.insert(parentID,'end',text=sectName,tags= name )
                    self.__InertTreeView(sp[name][sectName],newID)
                else:
                    self.treeView.insert(parentID,'end',text=sectName,tags=sp[name][sectName]) 
    def CleanView(self):
        """this function is to clean data in the tree view and text view. """
        self.treeView.CleanView()
        self.text.config(state= NORMAL)
        self.text.delete('1.0',END)
        self.text.config(state=DISABLED)

    def Show(self,filename=''):
        """this function is to 1) scan the lib file and get the structure, 2) clean the tree view, 3)insert new items to the treeview,4) bind callback method with left-mouse click event. """
        if filename!='':
            self.fullPath = os.path.abspath(filename)
            print(self.fullPath)
        sp = self.sv.ScanVbsFile(self.fullPath)
##        self.treeView.CleanView()
##        self.text.delete('1.0',END)
        self.CleanView()
        self.__InertTreeView(sp)

def testA():
    folder = 'C:\\WORK\\GSCS\\automation\\RM\\example\\My Own\\Lib'
    filename = 'TestCaseClass.qfl'
    rt= Tk()
    scanmodule = StringVar()
    scanmodule.set("ScanVbsFile")
    fr = Frame(rt)
    fr.pack(expand=YES, fill=BOTH)
    MyTreeView( 'ScanVbsFile', fr,folder , filename).Show()
    rt.mainloop()
def testB():
    folder = 'C:\\WORK\\GSCS\\automation\\RM\\example\\My Own\\Lib'
    filename = 'TestCaseClass.qfl'
    rt= Tk()
    scanmodule = StringVar()
    scanmodule.set("ScanVbsFileNormal")
    fr = Frame(rt)
    fr.pack(expand=YES, fill=BOTH)
    MyTreeView( 'ScanVbsFileNormal', fr,folder , filename).Show()
    rt.mainloop()
if __name__=='__main__':
    testA()
    testB()


