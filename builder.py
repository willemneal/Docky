from code import InteractiveConsole as Interpreter
from streamcatcher import StreamCatcher
from unidecode import unidecode


class NonreactiveInterpreter(Interpreter):
    '''Inherits Interpreter to run "input" lines from text'''

    @classmethod
    def getLines(cls,string):
        '''returns list of lines without comments'''
        return cls.removeComments(cls.cleanSplit(string,'\n'))

    @staticmethod
    def cleanSplit(string,delimiter):
        '''replaces empty strings with delimiter after spliting'''
        splitString = string.split(delimiter)
        for i,word in enumerate(splitString):
            if word == '':
                splitString[i] = delimiter
        return splitString

    @staticmethod
    def removeComments(lines):
        '''Remove lines with comments'''
        return [line for line in lines if not line.strip().startswith("#") ]

    @staticmethod
    def catchError():
        '''Catches errors and writes info to stdout'''
        traceback = str(sys.exc_info()[0])
        errortype = str(sys.exc_info()[1])
        try:
            sys.stderr.write("%s\n%s" % (traceback,errortype))
        except:
            print sys.exc_info()

    def buildAndRun(self,string):
        '''pushes each line to Interpreter'''
        lines = self.getLines(string)
        for line in lines:
            try:
                incomplete = self.push(line)
            except:
                self.catchError()
                break

            if incomplete:
                continue
            #print line
            self.resetbuffer()

def buildCode(string):
    '''redirects stdout and stderr, runs code,
       resets streams and returns what was caught'''
    streams = StreamCatcher()
    streams.catchStreams() 
    domain = {}
    builder = NonreactiveInterpreter(domain)
    builder.buildAndRun(unidecode(string))
    return streams.releaseStreams()