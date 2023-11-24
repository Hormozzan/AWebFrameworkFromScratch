#! ./.venv/bin/python

'''
Custom web application based on low-level WSGI concepts.
Greet the incoming 'name' query element if availabe;
otherwise, greet the World!
'''

from urllib.parse import parse_qs

ENCODING = 'utf8'

def app(environment, start_response):
    status = '200 OK'
    headers = [('Content-Type', f'text/html; charset={ENCODING}')]

    qdict = parse_qs(environment['QUERY_STRING'])
    names = ' & '.join([i for i in qdict.get('name', ['World']) if len(i) > 0 and i != ' '])

    start_response(status, headers)
    return [f'<h1>Hello, {names}!</h1>'.encode(ENCODING)]
