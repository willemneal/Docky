from cStringIO import StringIO
import sys
import traceback#.print_last([limit[, file]])
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import *



from pygments.formatter import Formatter

class NewFormatter(Formatter):

    def __init__(self, **options):
        Formatter.__init__(self, **options)

        # create a dict of (start, end) tuples that wrap the
        # value of a token so that we can use it in the format
        # method later
        self.styles = {}

        # we iterate over the `_styles` attribute of a style item
        # that contains the parsed style values.
        for token, style in self.style:
            if style['color'] is not None:
                color = "#"+style['color']
            else:
                color = style['color']
            self.styles[token] = (color, style['bold'],style['italic'],style['underline'])

    def writeToBuffer(self,lasttype, lastval,outfile):
        color, bold,italic,underline = self.styles[lasttype]
        outfile.write((lastval,{'color':color,'bold':bold,'italic':italic,'underline':underline}))

    def format(self, tokensource, outfile):
        # lastval is a string we use for caching
        # because it's possible that an lexer yields a number
        # of consecutive tokens with the same token type.
        # to minimize the size of the generated html markup we
        # try to join the values of same-type tokens here
        lastval = ''
        lasttype = None

        # wrap the whole output with <pre>
        #outfile.write('<pre>')

        for ttype, value in tokensource:
            # if the token type doesn't exist in the stylemap
            # we try it with the parent of the token type
            # eg: parent of Token.Literal.String.Double is
            # Token.Literal.String
            while ttype not in self.styles:
                ttype = ttype.parent
            if ttype == lasttype:
                # the current token type is the same of the last
                # iteration. cache it
                lastval += value
            else:
                # not the same token as last iteration, but we
                # have some data in the buffer. wrap it with the
                # defined style and write it to the output file
                if lastval:
                    self.writeToBuffer(lasttype,lastval,outfile)
                # set lastval/lasttype to current values
                lastval = value
                lasttype = ttype

        # if something is left in the buffer, write it to the
        # output file, then close the opened <pre> tag
        if lastval:
            self.writeToBuffer(lasttype, lastval, outfile)




class listBuffer(object):
    
    def __init__(self):
        self.buff = []
        pass

    def write(self, e):
        self.buff.append(e)


lB = listBuffer()

l = highlight(s, PythonLexer(), NewFormatter(), outfile=lB)
print lB.buff[0][1]['color']












# def makeDefn(definitions):
#     """calls all statements and returns their def'n in doman"""
#     domain = {}
#     exec definitions in domain
#     return domain

# def removeAll(List, Element):
#     """Removes all Instances of element"""
#     while Element in List:
#         List.remove(Element)

# def executedCode(calls, domain):
#     """Calls eval on each separate line of code"""
#     calls = calls.split('\n')
#     removeAll(calls,'')
#     res = []
#     for call in calls:
#         try:
#             tmp = eval(call,domain)
#             res.append(tmp)
#         except:
#             try:
#                 sys.stderr.write(str(sys.exc_info()[0])+'\n'+str(sys.exc_info()[1])+'\n')

#             except:
#                 print sys.exc_info()
#             pass

#     removeAll(res,None)
#     return res

# def redirectStreams():
#     sys.stdout = stdout = StringIO()
#     sys.stderr = stderr = StringIO()
#     return stdout,stderr

# def resetStreams(stdout, stderr):
#     stdout.close()
#     stderr.close()
#     sys.stdout = sys.__stdout__
#     sys.stderr = sys.__stderr__

# def runCode(code):
#     """runs the code sent to the server. Also redirects stdout and stderr"""
#     stdout,stderr = redirectStreams()

#     definitions, calls = code.split('run')##split

#     domain = makeDefn(definitions)
#     text = executedCode(calls, domain)

#     result = {'text':text,'stdout':stdout.getvalue(),'stderr':stderr.getvalue()}
    
#     resetStreams(stdout,stderr)
    
#     return result


# print runCode(s)