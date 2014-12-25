from flask import Flask, request, json
app = Flask(__name__)
app.config['DEBUG'] = True
from serve import *
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.



@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


@app.route('/eval',methods=["POST","GET"])
def runCode():
    """runs the code sent to the server. Also redirects stdout and stderr"""
    stdout,stderr = redirectStreams()   
    response = json.dumps({'text':getResult(unpackCode(request.args['text'])),
                           'stdout':stdout.getvalue(),
                           'stderr':stderr.getvalue()})
    resetStreams(stdout,stderr)
    return response

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

@app.route('/prettify',methods=["GET"])
def makePretty():
    return json.dumps({'text':formatCode(unpackCode(request.args['text']))})