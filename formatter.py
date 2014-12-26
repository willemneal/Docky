
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name, get_all_styles
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
            if style['bgcolor'] is not None:
                bgcolor = "#"+style['bgcolor']
            else:
                bgcolor = self.style.background_color
            if style['color'] is not None:
                color = "#"+style['color']
            else:
                color = style['color']
            self.styles[token] = {'color':color,
                                'bold':style['bold'], 
                                'italic':style['italic'], 
                                'underline':style['underline'],
                                'bgcolor':bgcolor}

    def writeToBuffer(self,lasttype, lastval,outfile):
        outfile.write((lastval,self.styles[lasttype]))

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
        if e[0] != ' ':
            self.buff.append(e)


def highlightCode(text,Style='monokai'):
    Style = checkStyle(Style)
    Buff = listBuffer()
    highlight(text, PythonLexer(), NewFormatter(style=Style), outfile=Buff)
    return Buff.buff

def checkStyle(style):
    if style is None or style not in list(get_all_styles()):
        return 'monokai'
    return style



# s = '''
# def lineOfCode(x):
#     print 'line of code'
#     print 'hello my firend'
#     return 547.0/x
#     '''
# print highlightCode(s)

