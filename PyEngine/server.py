from bottle import run, route, template
from api import app
from cors_setup import *
from gevent.pywsgi import WSGIServer


if __name__ == '__main__':
    http_server = WSGIServer(('localhost', 8000), app)
    http_server.serve_forever()
    # run(app, host='localhost', port=8000)