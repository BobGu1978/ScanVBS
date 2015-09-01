# coding=utf-8
from tkinter import *

class MyTextView(Text):
    """This class is to define one text control with scrollbar."""
    def __init__(self,parent=None):
        scb=Scrollbar(parent)
        scb.pack(side = RIGHT, fill=Y)
        hscb=Scrollbar(parent , orient = 'horizontal')
        hscb.pack(side=BOTTOM, fill=X)
        Text.__init__(self,parent,relief=SUNKEN,yscrollcommand=scb.set,  xscrollcommand= hscb.set)
        self.pack(expand=YES, fill=BOTH)
        scb.config(command= self.yview)
        hscb.config(command = self.xview)
        self.config(state=DISABLED)
##        self.bind("<KeyPress>", lambda e : "break")
        

def test():
    rt = Tk()
    fr = Frame(rt)
    fr.pack(expand=YES, fill=BOTH)
    mtv = MyTextView(fr)
    mtv.config(state = NORMAL)
    mtv.insert('1.0','<p bgcolor="red">a test</p>')
    mtv.config(state=DISABLED)
    rt.mainloop()

if __name__ == '__main__': test()
