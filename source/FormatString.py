import re
from VbsStructure import *

class FormatString(VbsStructure):
    """This class is to 1) format all the comments
and function/sub/property definition into one dictionary,2) format the data dictionaty
 into string in one proper order, at the same time replace the tags of vbsdoc with the other symbols."""
    def __init__(self,vbsdocStyle=True):
        self.UseVbsDoc = vbsdocStyle
        self.__comment = 'comment'
        self.__define = 'define'
        self.__param = 'param'
        self.__return = 'return'
        self.__todo = 'todo'
        self.__see = 'see'
        self.__stringOrder = [self.__comment,self.__define,self.__param,self.__return,self.__todo,self.__see]
        self.__Header_Detail = '@details'
        self.__Header_Param = '@param'
        self.__Header_Define = '@Definition'
        self.__Header_Return = '@return'
        self.__Header_Todo = '@todo'
        self.__Header_Reference = '@see'
        self.__Header_Author = '@author'
        self.__Header_Brief = '@brief'
        self.__Scan={self.__define:self.__Header_Define,
                     self.__param:self.__Header_Param,
                     self.__return:self.__Header_Return,
                     self.__todo:self.__Header_Todo,
                     self.__see:self.__Header_Reference}
        VbsStructure.__init__(self)

    def Header_Define(self):
        return self.__Header_Define

    def __Dealwithcomment(self, mylist):
        """This function is to deal with comments. it only accepts list as parameter
, and will filter all comments that have tag of '@author'/'@brief' at beginning. And
if the comment line has nothing else except '''---or i mean a space line, it will be
filtered too. and it returns one list."""
        mystr = []
        for i in mylist:
            if i.isspace():
                mystr=[]
                continue
            if i.replace(self.SoftReturn,'').isspace():
                mystr=[]
                continue
            elif self.UseVbsDoc:
                temp = i.replace(self.VBSDocCommentSign,'')
                if temp.replace(self.SoftReturn,'').isspace():
                    mystr=[]
                    continue
            else:
                temp = i.replace(self.CommentSign,'')
                if temp.replace(self.SoftReturn,'').isspace():
                    mystr=[]
                    continue
                
            if self.UseVbsDoc:
                if i.find(self.__Header_Author)>0 or i.find(self.__Header_Brief)>0:
                    mystr=[]
                    continue
                if not re.match(self.VBSDocCommentSignLine,i):
                    continue
                mystr.append(i)
            else:
                if not re.match(self.CommentSignLine,i):
                    continue
                mystr.append(i)
        return mystr

    def FormatDict(self, mylist):
        """This function is to organize the comments and definition into one dictionaty"""
        mydict = {}
        a = self.__Dealwithcomment(mylist)
        if self.UseVbsDoc:
            find = False
            for i in a:
                find = False
                for j in self.__Scan.keys():
                    if i.find(self.__Scan[j])>=0:
                        find = True
                        if j == self.__define:
                            mydict[j]= i
                        else:
                            if not j in mydict.keys():
                                mydict[j]=[]
                            mydict[j].append(i)
                        break
                if not find:
                    if not self.__comment in mydict.keys():
                        mydict[self.__comment]=[]
                    mydict[self.__comment].append(i)
        else:
            mydict[self.__comment]=[]
            for i in a:
                mydict[self.__comment].append(i)
##        print(mydict)
        return mydict

    def Formatoutput(self,mydict):
        """This function is to format the dictionary of comments and definitions into
one string, the order will be 1) description, 2) definition, 3) parameter description if existed,
 4) returned value description if existed. it always returns string."""
        mystr = ''
        for i in self.__stringOrder:
            if i in mydict.keys():
                if type(mydict[i])==type([]):
                    for j in mydict[i]:
                        mystr += j
                else:
                    mystr+=mydict[i]
        if self.UseVbsDoc:
##            i = mystr.find(self.VBSDocCommentSign)
##            if i>=0:
##                mystr=mystr[i+len(self.VBsDocCommentSign)::]
            mystr = mystr.replace( self.VBSDocCommentSign , '').lstrip()
            if mystr.find(self.Tab)>=0:
                mystr = mystr.replace( self.Tab ,'')
            if mystr.find(self.__Header_Detail)>=0:
                mystr = mystr.replace(self.__Header_Detail,'')
            if mystr.find(self.__Header_Param)>=0:
                mystr = mystr.replace(self.__Header_Param,''.join((self.__Header_Param[1:],':')))            
            if mystr.find(self.__Header_Return)>=0:
                mystr = mystr.replace(self.__Header_Return,''.join((self.__Header_Return[1:],':')))
            if mystr.find(self.__Header_Todo)>=0:
                mystr = mystr.replace(self.__Header_Todo, ''.join((self.__Header_Todo[1:],':')))
            if mystr.find(self.__Header_Reference)>=0:
                mystr = mystr.replace(self.__Header_Reference , 'Reference:')
            if mystr.find(self.__Header_Define)>=0:
                mystr = mystr.replace(self.__Header_Define , '')
        return mystr

def test():
    a = FormatString()
    print(a.section)
    b = FormatString(False)
    print(b.section)

if __name__=='__main__': test()

