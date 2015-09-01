from tkinter import *
from tkinter import ttk

class ScrolledTreeview(ttk.Treeview):
    """this class is to define one tree view with scroll bar at right side"""
    def __init__(self, parent=None):
        scb=Scrollbar(parent)
        scb.pack(side = RIGHT, fill=Y)
        hscb=Scrollbar(parent , orient = 'horizontal')
        hscb.pack(side=BOTTOM, fill=X)
        ttk.Treeview.__init__(self,parent,yscrollcommand= scb.set, xscrollcommand= hscb.set)
        self.pack(expand=YES, fill=BOTH)
        scb.config(command= self.yview)
        hscb.config(command = self.xview)
    def CleanView(self):
        for i in self.get_children():
            self.delete(i)
    def IfViewContainItem(self):
        """ it check if the tree view contains item."""
        if len(self.get_children())>0:
            return True
        else:
            return False

def test():
    rt= Tk()
    fr= Frame(rt)
    fr.pack(expand=YES, fill=BOTH)
    stv = ScrolledTreeview(fr)
    rt.mainloop()

if __name__=='__main__': test()

