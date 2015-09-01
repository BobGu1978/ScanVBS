# coding=utf-8
from tkinter import *
from tkinter.messagebox import *
from tkinter.simpledialog import askstring
from tkinter import filedialog
from tkinter import PhotoImage
import threading
from LibsView import *
from MultipleSearch import *
from MyText import *
from VbsTrView import *

class MainWin:
    """This class is to infrustucture a window which contains 1 left tree view, 1
right tree view,1 label view to show comments and definition from the selected item,
one new label to show searching result, and menu bar.
"""
    def __init__(self,module='ScanVbsFile'):
        self.__version= '1.12'
        self.__img={}
        self.__workdir=''
        self.root = Tk(className='Uft lib file scanner')
        self.__module = module
        self.__temp = ''
        self.__countofLefttree =0
        self.__BuildMenu()
        self.__BuildFrame()

    def __CleanView(self):
        self.lf.treeView.CleanView()
        self.rf.CleanView()
        self.__lt.config(state = NORMAL)
        self.__lt.delete('1.0',END)
        self.__lt.config(state=DISABLED)
        
        
    def SetVersion(self, version):
        """this function is to set version No. """
        self.__version = version

    def __BuildFrame(self):
        pw1 = PanedWindow(self.root)
        pw1.pack(fill=BOTH , expand=NO)
        self.lf = LibView(pw1)
        pw1.add(self.lf.fr)
        pw2 = PanedWindow(self.root , orient= VERTICAL)
        pw2.pack(fill=BOTH, expand = YES)
        pw1.add(pw2)
        self.rf = MyTreeView( self.__module , pw2)
        self.lf.SetRightView(self.rf)
        pw2.add(self.rf.topfr)
        pw2.add(self.rf.btmfr)
        pw3=PanedWindow(self.root)
        pw3.pack(fill=BOTH,expand=YES)
        fr = Frame(pw3)
        fr.pack(expand=YES , fill= BOTH)
        pw3.add(fr)
        self.__lt = MyTextView(fr)

    def __SetStateofSearchMenu(self):
        """ it will enable or disable  the menu 'search' depanding on if left treeview contains item. """
        if self.lf.treeView.IfViewContainItem():
            self.__editmenu.entryconfig(1,state=NORMAL)
        else:
            self.__editmenu.entryconfig(1,state=DISABLED)

    def __SelectTSP(self):
        """the callback method of menu 'select tsp'. it will popup one file dialog and let you pick up one tsp file. if libs are retrieved from that tsp file,
it will insert them into the left tree view. and enable the menu 'search'. """
        op={}
        op['defaultextension'] = '.tsp'
        op['filetypes'] = [('tsp files', '.tsp')]
        op['initialdir'] = 'C:\\'
        op['initialfile'] = ''
        op['parent'] = self.root
        op['title'] = 'Please select one tsp file'
        f = filedialog.askopenfilename(**op)
        if f=='':
            return
        filename = os.path.abspath(f)
        if os.path.isfile(filename):
            self.__CleanView()
            self.root.title(filename)
            (self.__workdir,fn)=os.path.split(filename)
            self.lf.Show(filename)
            self.__countofLefttree = self.lf.GetCount()
            self.__SetStateofSearchMenu()

    def __SelectLibFile(self):
        """it is callback method of menu 'select lib file'. it will try to scan the lib file after you pick up one from the file dialog. and display the result in the
right tree view, at the same time, it will 1) clean left tree view, 2) disable the menu 'select for'. """
        op={}
        op['defaultextension'] = '.qfl'
        op['filetypes'] = [('qfl files', '.qfl'),('vbs files','.vbs'),('text files','.txt')]
        op['initialdir'] = 'C:\\'
        op['initialfile'] = ''
        op['parent'] = self.root
        op['title'] = 'Please select one function library file'
        f = filedialog.askopenfilename(**op)
        if f=="":
            return
        filename = os.path.abspath(f)
        if os.path.isfile(filename):
            self.__CleanView()
            self.root.title(filename)
            (folder, fn) = os.path.split(filename)
            self.__countofLefttree = 0
            self.__workdir=''
            self.rf.Show(filename)
            self.__SetStateofSearchMenu()

    def __SelectFolder(self):
        """it is callback method of menu 'select folder', it retrieves one folder from the path dialog, and retrieves all lib file names, then insert them into the left tree
view, at the same time, it enable the menu 'select for'. """
        op={}
        op["initialdir"]=os.getcwd()
        f = filedialog.askdirectory(**op)
        if f=="":
            return
        filepath = os.path.abspath(f)
        if os.path.isdir(filepath):
            self.__CleanView()
            self.root.title(filepath)
            self.__workdir= os.path.abspath(filepath)
            self.lf.ShowWithoutAnalys(filepath)
            self.__countofLefttree = self.lf.GetCount()
            self.__SetStateofSearchMenu()

    def __AboutDialog(self):
        """it is the callback method of menu ''About'. it only popsup a dialog to show basic information of this app. """
        dlg=Toplevel()
        dlg.title('About...')
        dlg.resizable(width=False, height=False)
        Label(dlg,text="This is a tiny tool to scan UFT lib file.\r\nThe version is " + self.__version + ".\r\nAuthor is Bob Gu.").pack()
        Button(dlg,text='Close',command=dlg.destroy).pack()
        dlg.focus_set()
        dlg.grab_set()
        dlg.wait_window()

    def __DoSearch(self):
        """this is callback method of menu 'search for'. it pops upa dialog to let you input the keyword. """
        mystr = askstring("search for","please enter one keyword:")
        if mystr:
            self.__temp = mystr
            if  self.__countofLefttree <=0:
                self.__astr.set("there is no item listed in the libs view.please check.")
                return
            threads=[]
            mutex = threading.Lock()
            for i in self.lf.treeView.get_children():
                filename = os.path.join(self.__workdir,self.lf.treeView.item(i,'text'))
                thread = MultipleSearch(mutex,filename,mystr)
                thread.start()
                threads.append(thread)
            for thread in threads: thread.join()
            output = 'trying to search for \'' + mystr + '\':\r\n'
            mystr = ''
            for i in threads:
                (fn,count) = i.ShowResult()
                (fd,name)= os.path.split(fn)
                if count>0:
                    mystr += 'in file \'' + os.path.join(os.path.abspath(fd), name) + '\', ' + str(count) + ' hits.\r\n'
            if mystr=='':
                mystr = 'there is no hit.\r\n'
            output+=mystr
            self.__lt.config(state = NORMAL)
            self.__lt.delete('1.0',END)
            self.__lt.insert('1.0',output)
            self.__lt.config(state=DISABLED)

    def Show(self):
        """the main loop of the main window. """
        self.root.mainloop()

    def __BuildMenu(self):
        """this is to build menu bar for the app. """
        self.__menubar = Menu(self.root)
        self.__filemenu = Menu(self.__menubar, tearoff=0)
        self.__filemenu.add_command(label="Open UFT project file", command=self.__SelectTSP)
        self.__filemenu.add_command(label="Open Libs from folder", command = self.__SelectFolder)
        self.__filemenu.add_command(label="Open UFT Library file", command=self.__SelectLibFile)
        self.__filemenu.add_separator()
        self.__filemenu.add_command(label="Exit", command=self.root.destroy)
        self.__menubar.add_cascade(label="File", menu=self.__filemenu)
        self.__editmenu = Menu(self.__menubar , tearoff =0)
        self.__editmenu.add_command(label="Search for...",command = self.__DoSearch)
        self.__editmenu.entryconfig(1,state=DISABLED)
        self.__menubar.add_cascade(label="Edit",menu=self.__editmenu)
        self.__helpmenu = Menu(self.__menubar, tearoff=0)
        self.__helpmenu.add_command(label="About...", command=self.__AboutDialog)
        self.__menubar.add_cascade(label="Help", menu=self.__helpmenu)
        self.root.config(menu=self.__menubar)

if __name__=='__main__':
    mw = MainWin(module = "ScanVbsFileNormal")
    mw.SetVersion('1.16')
    mw.Show()
    
