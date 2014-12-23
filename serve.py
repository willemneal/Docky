from unidecode import unidecode
import sys
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO


def catchError():
    try:
        sys.stderr.write(str(sys.exc_info()[0])+'\n'+str(sys.exc_info()[1]))
    except *:
        print sys.exc_info()


def makeDefn(definitions):
    """calls all statements and returns their def'n in domain"""
    domain = {}
    try:
        exec definitions in domain
    except:
        catchError()
    return domain

def removeAll(List, Element):
    """Removes all Instances of element"""
    while Element in List:
        List.remove(Element)

def executeCode(calls, domain):
    """Calls eval on each separate line of code"""
    calls = calls.split('\n')
    removeAll(calls,'')
    res = []
    for call in calls:
        try:
            tmp = str(eval(call,domain))
            res.append(tmp)
        except *:
            catchError()

    removeAll(res,None)
    return res

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

def unpackCode():
    code = unidecode(request.args['text']).split('__code__')[-1]
    definitions, calls = code.split('__run__')
    calls = calls.split('__result__')[0]
    return definitions, calls

def getResult(code):
    definitions, calls = code
    domain = makeDefn(definitions)
    return executeCode(calls, domain)