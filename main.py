from flask import Flask, request, json
app = Flask(__name__)
app.config['DEBUG'] = True
from builder import buildCode
from formatter import highlightCode
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.



@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Docky-py!'


@app.route('/eval',methods=["POST","GET"])
def runCode():
    """runs the code sent to the server. Also redirects stdout and stderr"""
      
    return json.dumps(buildCode(request.args['text']))

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

@app.route('/prettify',methods=["GET"])
def makePretty():
    '''returns styling '''
    return json.dumps({'text':highlightCode(request.args['text'],request.args['style'])})

