#from unidecode import unidecode
import sys
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

from formatter import *
from code import InteractiveConsole as Interpreter
from code import compile_command

def catchError():
    try:
        sys.stderr.write(str(sys.exc_info()[0])+'\n'+str(sys.exc_info()[1]))
    except:
        print sys.exc_info()

def removeAll(List, Element):
    """Removes all Instances of element"""
    while Element in List:
        List.remove(Element)

def redirectStreams():
    stdout = StringIO()
    sys.stdout = stdout
    stderr = StringIO()
    sys.stderr = stderr
    return stdout,stderr

def resetStreams(stdout, stderr):
    stdout.close()
    stderr.close()
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__


def formatCode(code,style='monokai'):
        return highlightCode(code,style)

def cleanSplit(string,delimiter):
    splitString = string.split(delimiter)
    for i,word in enumerate(splitString):
        if word == '':
            splitString[i] = delimiter
    return splitString

class PythonBuilder(Interpreter):

    @classmethod
    def getLines(cls,string):
        lines = cleanSplit(string,'\n')
        #print lines
        lines = cls.removeComments(lines)
        #print lines
        return lines

    @staticmethod
    def removeComments(lines):
        return [line for line in lines if not line.strip().startswith("#") ]

    
    def buildAndRun(self,string):
        lines = self.getLines(string)
        for line in lines:
            try:
                incomplete = self.push(line)
            except:
                catchError()
                break

            if incomplete:
                continue
            #print line
            self.resetbuffer()

def buildCode(string):
    domain = {}
    builder = PythonBuilder(domain)
    builder.buildAndRun(unidecode(string))


