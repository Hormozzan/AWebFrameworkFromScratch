'''
A simple web server using built-in wsgiref module
'''

from wsgiref.simple_server import demo_app, make_server

if __name__ == '__main__':
    with make_server(host='localhost', port=8000, app=demo_app) as server:
        server.serve_forever()