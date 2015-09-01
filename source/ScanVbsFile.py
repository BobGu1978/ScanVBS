#! /usr/bin/python
# coding=utf-8
import os.path
import re
import sys
from OpenEncodingFile import *
from FormatString import *
global filetype
filetype = ['.qfl','.txt','.vbs']
class ScanVbs(FormatString, OpenEncodingFile):
    """ This class is to implment functions/methods to scan uft lib files and organize them like class:function/sub/property"""
    def __init__(self,sp={}):
        print("vbs doc scan starts")
        if type(sp)!=type({}):
            raise TypeError("class ScanVbs needs a dictionary as parameter but now it is %s" %type(sp))
        self.storePoint = sp
        self.fileType = filetype
        FormatString.__init__(self)
        OpenEncodingFile.__init__(self)
        return
    def __GetSectionName(self,line, section):
        """This function is to retrieve the name of the sector from the line depanding on the input sector name.it first finds if the sector
name is contained, then try to get all string which is not part of comments and return them."""
        aList = line.split()
        count = len(aList)
        for i in range(count):
            if aList[i].lower() == section.lower():
                break
        j=i+1
        if section.lower() == self.sectorProperty:
            j=j+1
        if j<count:
            p=re.search( self.patternSection,aList[j])
            if p == None:
                return aList[j]
            else:
                return p.group()
        return ''

    def __CheckItemRecorded(self,sp,itemName,className):
        """as our storage structure is a little complex, which is a dictionary, contains key-value paires. and the value
is a dictionary too. so that this function is to 1) if the item name is a key of the root dictionary, 2) check if the class name is
the key of the item's dictonaty."""
        if type(sp)!=type({}):
            return False
        if itemName not in sp.keys():
            return False
        if type(sp[itemName])!=type({}):
            raise Exception("the type of strucutre 'class' should be dictionaty, but now it is %s\n" %type(sp[itemName]))
            return False
        if className in sp[itemName].keys():
            return True
        else:
            return False
    
    def __ScanLines(self,sp,fh):
        """This function is to receive handle of a file opened with read-only mode, then start to scan it line by line. at the end,
it stores all information in the storepoint dictionary which is as input parameter. it is a recursive function, it will be called internally
when we deal with strucutre of class. it will return either detecting 'end of class' or reaching end of the file-stream."""
        record = False
        line = fh.readline()
        arr=[]
        codeLine=''
        while line:
            if record:
                codeLine += line
                if re.match(self.patternEndFunction,line) or re.match(self.patternEndSub,line) or re.match(self.patternEndProperty,line):
                    sp[item][name][-1]+=codeLine
                    codeLine=''
                    record = False
            else:
                for item in self.section.keys():
                    if re.match(self.section[item][0],line):
                        if item == self.sectorComment:
                            arr.append(line)
                            continue
                        if item == self.sectorEndClass:
                            arr=[]
                            return True
                        if item != self.sectorClass:
                            record = True
                            codeLine = line
                        name = self.__GetSectionName(line,item)
                        if item not in sp.keys():
                            sp[item]={}
                        if not self.__CheckItemRecorded(sp,item ,name):
                            if item == self.sectorClass:
                                sp[item][name]={}
                                self.__ScanLines(sp[item][name],fh)
                            else:
                                i = line.find(self.CommentSign)
                                if i>=0:
                                    mystr = line[:i]
                                else:
                                    mystr = line
                                arr.append(self.VBSDocCommentSign + FormatString.Header_Define(self) +' ' + mystr.lstrip() + self.SoftReturn)
                                ad = FormatString.FormatDict(self,arr)
                                sp[item][name]=[item,FormatString.Formatoutput(self,ad),self.section[item][-1],'']
                            arr=[]
                        break
            line = fh.readline()
        return True

    def __SortStorePorint(self,sp):
        """it sorts the data of value of sub-dictionary inside storepoint. and it is a recursive function."""
        for item in sp.keys():
            if type(sp[item]) == type({}):
                sp[item]= self.__SortStorePorint(sp[item])
        return sorted(sp.iteritems(),key=lambda d:d[0])

    def __CheckIfFileValid(self,filename):
        """this function checks if the given file name is linked to a meaningful file by checking its extension name is one of the fieltype."""
        ext = os.path.splitext(filename)[-1].lower()
        for i in range(len(self.fileType)):
            if ext.lower() == self.fileType[i]:
                return True
        return False

    def ScanVbsFile(self,filename):
        """this function is to scan vbs lib files by given file name."""
        self.storePoint.clear()
        if not os.path.isfile(filename):
            return self.storePoint
        if not self.__CheckIfFileValid(filename):
            return self.storePoint
        et = OpenEncodingFile.DetectFileEncoding(self,filename)
        fh = OpenEncodingFile.OpenFileReadOnly(self,filename,et)
        if fh != None:
            try:
                self.__ScanLines(self.storePoint,fh)
            except:
                print('we encounter error here.')
            finally:
                fh.close()
        return self.storePoint

def test():
    f = ScanVbs()
    print(f.ScanVbsFile('c:\\a1.qfl'))

if __name__=='__main__':test()
##    if (len(sys.argv)==1) or (type(sys.argv[1])==type(None)):
##        f= ScanVbs()
##        print("now we get the structure of the file:")
##        print(f.ScanVbsFile("C:\\WORK\\GSCS\\automation\\RM\\example\\My Own\\Lib\\TestCaseClass.qfl"))
##    elif type(sys.argv[1]!=type('')):
##        print("the parameter is expected to be string, but now it is %s" %type(sys.argv[1]))
##    else:
##        f= ScanVbs()
##        print("now we get the structure of the file:")
##        print(f.ScanVbsFile(sys.argv[1]))
