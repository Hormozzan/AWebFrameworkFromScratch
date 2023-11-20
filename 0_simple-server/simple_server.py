#! ./.venv/bin/python

'''
A simple web application using wsgiref.simple_server.demo_app.
'''

from wsgiref.simple_server import demo_app, make_server

if __name__ == '__main__':
    with make_server(host='localhost', port=8000, app=demo_app) as server:
        server.serve_forever()