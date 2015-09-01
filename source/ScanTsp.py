import os.path

class AnalysisTSP:
    """this class is to retrieve the library files list from the tsp file. it only accept a file name in full and absolute path"""
    def __init__(self,fileName=''):
        self.__TagName = b'<FuncLibs>'
        self.__SectorName = '<FuncLib '
        self.__CDName = '[CDATA['
        self.__LengthofCDName = len(self.__CDName)
        self.__End = ']]'
        self.__EndTab = '</FuncLibs>'
        self.workdir = ''
        self.__filename = ''
        if os.path.isfile(fileName):
            (self.workdir,self.__filename) = os.path.split(fileName)

    def __ScanTSP(self):
        """this function is to scan the tsp file, and returns the string of data where the lib information locates."""
        fn = os.path.join(self.workdir,self.__filename)
        if not os.path.isfile(fn):
            return ''
        line = b''
        try:
            fh = open(fn,'rb')
            try:
                while True:
                    temp = fh.read(1024)
                    if temp == b'':
                        break
                    line+=temp
            finally:
                fh.close()
        finally:
            line = line.replace(b'\x00',b'')
            nPos = line.find(self.__TagName)
            if nPos<0:
                return ''
            else:
                return line[nPos::].decode('utf-8','ignore')

    def __RetrieveLibName(self,data):
        """this function is analysis the library file names from the input string.
the file names will be stored in one array."""
        nPos = data.index(self.__EndTab)
        mystr = data[0:nPos]
        libs=[]
        nPos = mystr.find(self.__CDName)
        while nPos >=0:
            nEnd = mystr.find(self.__End, nPos+1)
            l = nPos + self.__LengthofCDName
            libs.append(mystr[l:nEnd])
            nPos = mystr.find(self.__CDName , nEnd+1)
        return libs
    def WorkDir(self):
        """the base diretory splitted from the tsp file, which is a main project file."""
        return self.workdir
    
    def GetLibs(self,filename=''):
        """this function is to retrieve the lib names from the tsp file. """
        if filename != '':
            if os.path.isfile(filename):
                (self.workdir,self.__filename) = os.path.split(filename)
        if self.workdir=='':
            return []
        lines = self.__ScanTSP();
        if lines == '':
            return []
        return self.__RetrieveLibName(lines)

if __name__=='__main__':
    import sys
    if (len(sys.argv)==1) or (type(sys.argv[1])==type(None)):
        fn = 'C:\\WORK\\GSCS\\automation\\RM\\example\\My Own\\PrimitiveTest\\PrimitiveTest\\Test.tsp'
        f= AnalysisTSP(fn)
        print("now we get libraries from the project file:%s" %fn)
        print(f.GetLibs())
    elif type(sys.argv[1]!=type('')):
        print("the parameter is expected to be string, but now it is %s" %type(sys.argv[1]))
    else:
        f= ScanVbs(sys.argv[1])
        print("now we get the structure of the file:")
        print(f.GetLibs())    


