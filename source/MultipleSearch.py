#coding = utf-8
import threading
from SearchString import *

class MultipleSearch(threading.Thread,SearchString):
    """ this class is to provide the capability to do the searching job with multiple thread.
"""
    def __init__(self,mutex,filename='',searchword=''):
        self.mutex=mutex
        self.__filename = filename
        self.__sp=''
        threading.Thread.__init__(self)
        SearchString.__init__(self,filename,searchword)

    def run(self):
        """working function to do the searching job. it will store tripple of
filename and its hits number. """
        with self.mutex:
            self.__sp = (self.__filename ,SearchString.detect(self))
##        print(self.__sp)

    def ShowResult(self):
        return self.__sp

def test():
    mutex = threading.Lock()
    t=MultipleSearch(mutex,'c:\\a1.qfl','end')
    t.start()
    t.join()
    print(t.ShowResult())

if __name__=='__main__':
    test()

