import sys
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

class StreamCatcher(object):
    '''redirects stdout and stderr to string buffer'''
    def __init__(self):
        self.stdout = StringIO()
        self.stderr = StringIO()

    def catchStreams(self):
        '''redirects stdout and stderr'''
        sys.stdout = self.stdout
        sys.stderr = self.stderr


    def releaseStreams(self):
        '''resets stdout and stderr and returns what was caught'''
        catch = {'stdout':self.stdout.getvalue(), 'stderr':self.stderr.getvalue()}
        self.stdout.close()
        self.stderr.close()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        return catch
