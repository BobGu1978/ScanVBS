import os.path
from OpenEncodingFile import *
class SearchString(OpenEncodingFile):
    """this class is to search for single string in specific file and returns how
many times the string matches in that file.
"""
    def __init__(self,filename='',searchstr=''):
        self.__fn = filename
        self.__kstr = searchstr
        OpenEncodingFile.__init__(self)

    def setFileName(self, filename):
        """this function is to accept one filename which we plan to search with,
if it is not given when the class instance is generated."""
        self.__fn = filename

    def getFileName(self):
        """it returns the file name we just receive. """
        return self.__fn

    def setSearchCritiria(self, searchstr):
        """it accept the search key word. """
        self.__kstr = searchstr

    def getSearchCritiria(self):
        """it returns the search key word. """
        return self.__kstr

    def __searchline(self,line):
        """this function receive the string and try to search for the weyword as many times as possible.
it returns the number how many the key word hits in this string."""
        lk = len(self.__kstr)
        ll = len(line)
        i=0
        pos=0
        while (pos+lk)<ll:
            ipos = line[pos:].lower().find(self.__kstr.lower())
##            print(pos)
            if ipos==-1:
                break
            i+=1
            pos+=ipos+lk+1
        return i
    
    def detect(self):
        """this function is to open the file with read-only mode and start to search for the hits of keyword line by line. at the end, it return the amount
of hits."""
        if not os.path.isfile(self.__fn):
            return 0
        et = OpenEncodingFile.DetectFileEncoding(self,self.__fn)
        fp= OpenEncodingFile.OpenFileReadOnly(self,self.__fn,et)
        if fp==None:
            return 0
        i=0
        try:
            line = fp.readline()
            while(1):
                i+=self.__searchline(line)
                line = fp.readline()
                if line =='':
                    break
        finally:
            fp.close()
        return i

def test():
    t= SearchString('c:\\a1.qfl','set')
    print(t.detect())

if __name__=='__main__':
    test()
