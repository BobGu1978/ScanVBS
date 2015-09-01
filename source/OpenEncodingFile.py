import codecs
import chardet

class OpenEncodingFile:
    def __init__(self):
        return
    def DetectFileEncoding(self,filename):
        u=''
        try:
            f = open(filename,'rb')
            try:
                u = chardet.detect(f.read())
            except:
                u = ''
            f.close()
        finally:
            if type(u['encoding'])==type(''):
                return u['encoding'].lower()
            else:
                return u['encoding']
    def OpenFileReadOnly(self,filename,encoding, mode ='r'):
        try:
            fp = codecs.open(filename,mode,encoding)
        except:
            fp = None
        return fp

def test():
    a = "C:\\WORK\\GSCS\\automation\\RM\\example\\My Own\\Lib\\MyServiceRequestClass.qfl"
    f = OpenEncodingFile()
    et = f.DetectFileEncoding(a)
    print(et)
    fh = f.OpenFileReadOnly(a , et)
    print(fh.readlines())
    fh.close()

if __name__ == '__main__': test()
