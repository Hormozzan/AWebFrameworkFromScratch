#! ./.venv/bin/python

'''
A custom web application. Greets the incoming 'name' query element if availabe;
otherwise, greets the World!
'''

from wsgiref.simple_server import make_server
from urllib.parse import parse_qs

ENCODING = 'utf8'

def app(environment, start_response):
    status = '200 OK'
    headers = [('Content-Type', f'text/html; charset={ENCODING}')]

    qdict = parse_qs(environment['QUERY_STRING'])
    name = qdict.get('name', ['World'])[0]

    start_response(status, headers)
    return [f'<h1>Hello, {name}!</h1>'.encode(ENCODING)]

if __name__ == '__main__':
    with make_server(host='localhost', port=8000, app=app) as server:
        server.serve_forever()