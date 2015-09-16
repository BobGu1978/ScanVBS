class VbsStructure:
    def __init__(self):
        self.Tab = '\t'
        self.SoftReturn = '\r\n'
        self.CommentSign = '\''
        self.VBSDocCommentSign = self.CommentSign + '!'
        self.CommentSignLine = '^[\s\p{Zs}]*' + self.CommentSign
        self.VBSDocCommentSignLine = self.CommentSignLine+'!'
        self.attributePrivate = '^[\s\p{Zs}]*(?!)private'
        self.patternSection = '.*(?=\(|\')' #this pattern is to match the string which only has ( or ' at the end of the char[a-zA-Z]
        self.sectorProperty = 'property'
        self.patternProperty = '^[\s\p{Zs}]*(?i)(public|private)?[\s\p{Zs}]*property[\s\p{Zs}]+[lgs]et'
        self.flagProperty = 1
        self.sectorClass = 'class'
        self.patternClass = '^[\s\p{Zs}]*(?i)class\s'
        self.flagClass = 0
        self.sectorFunction = 'function'
        self.PatternFunction = '^[\s\p{Zs}]*(?i)(private|public)?[\s\p{Zs}]*function\s'
        self.flagFunction = 4
        self.sectorSub = 'sub'
        self.patternSub = '^[\s\p{Zs}]*(?i)(private|public)?[\s\p{Zs}]*sub\s'
        self.flagSub = 6
        self.sectorEndClass = 'endclass'
        self.patternEndClass = '^[\s\p{Zs}]*(?i)end class'
        self.sectorEndFunction = 'endfunction'
        self.patternEndFunction = '^[\s\p{Zs}]*(?i)end function'
        self.sectorEndProperty = 'endproperty'
        self.patternEndProperty = '^[\s\p{Zs}]*(?i)end property'
        self.sectorEndSub = 'endsub'
        self.patternEndSub = '^[\s\p{Zs}]*(?i)end sub'
        self.sectorComment = 'comment'
        self.patternComment = '^[\s\p{Zs}]*\''
        self.flagComment = 8
        self.section={self.sectorComment:(self.patternComment, self.flagComment),
                        self.sectorClass: (self.patternClass,self.flagClass) ,
                        self.sectorProperty: (self.patternProperty , self.flagProperty),
                        self.sectorFunction: (self.PatternFunction , self.flagFunction),
                        self.sectorSub: (self.patternSub , self.flagSub),
                        self.sectorEndClass: (self.patternEndClass, self.flagClass),
                        self.sectorEndFunction: (self.patternEndFunction, self.flagFunction),
                        self.sectorEndSub: (self.patternEndSub, self.flagSub),
                        self.sectorEndProperty: (self.patternEndProperty, self.flagProperty)}

    def ExportSector(self):
        """it returns the tripple of sectors we are checking."""
        return (self.sectorClass,self.sectorProperty,self.sectorFunction,self.sectorSub)

    def nameofProperty(self):
        """it returns the definition name of property used in VBScript."""
        return self.sectorProperty

    def PropertyName(self,name):
        return ''.join(('^[\s\p{Zs}]*(?i)property[\s\p{Zs}]+[lgs]et[\s\p{Zs}]+',name , '[\s\p{Zs}]*(?=\(|\')'))

    def ClassName(self, name):
        return ''.join(('^[\s\p{Zs}]*(?i)class[\s\p{Zs}]+' , name , '[\s\p{Zs}]+'))

    def nameofClass(self):
        """it returns the definition name of class used in VBScript."""
        return self.sectorClass

    def nameofFunction(self):
        """it returns the definition name of function used in VBScript."""
        return self.sectorFunction

    def FunctionName(self,name):
        return ''.join(('^[\s\p{Zs}]*(?i)(private|public)?[\s\p{Zs}]*function[\s\p{Zs}]+' , name , '[\s\p{Zs}]*(?=\(|\')' ))

    def nameofSub(self):
        """it returns the definition name of sub procedure used in VBScript."""
        return self.sectorSub

    def SubName(self,name):
        return ''.join(('^[\s\p{Zs}]*(?i)(private|public)?[\s\p{Zs}]*sub[\s\p{Zs}]+' , name , '[\s\p{Zs}]*(?=\(|\')'))

    def nameofComment(self):
        """it returns the keyword of comment we defined ourselves."""
        return self.sectorComment

