'''
A tiny web framework, abstracting WSGI concepts as Request/Response classes
'''

from urllib.parse import parse_qs
from wsgiref.headers import Headers
from http.client import responses, NOT_FOUND
from typing import Callable
import importlib
import os
import re

APP_ENV_NAME = 'TINY_APP'
ROUTER_NAME = 'router'

class Request:
    '''
    Abstract the 'environment' dictionary from WSGI as a class
    '''

    def __init__(self, environment: dict) -> None:
        self._env = environment

    @property
    def queries(self) -> dict[str, str]:
        '''
        Return parsed query elements of a request
        '''
        return parse_qs(self._env['QUERY_STRING'])

    @property
    def path(self) -> str:
        '''
        Return path of a request
        '''
        return self._env['PATH_INFO']


class Response:
    '''
    Abstract response elements returned to WSGI as a class
    '''

    def __init__(self,
                 encoding: str = 'utf8',
                 body: list[str | bytes] = [],
                 status_code: int = 200,
                 content_type: str = 'text/html'
                 ) -> None:
        self._encoding = encoding
        self.body = body
        self._status_code = status_code
        self._headers = Headers()
        self._headers.add_header('Content-Type', f'{content_type}; charset={self._encoding}')

    @property
    def status(self) -> str:
        '''
        Return status code and a string description of the response
        '''
        status_string = responses.get(self._status_code, 'UNKNOWN')
        return f'{self._status_code} {status_string}'

    @property
    def headers(self) -> list[tuple[str, str]]:
        '''
        Return header items of the response
        '''
        return self._headers.items()

    def __iter__(self) -> bytes:
        '''
        Return elements of the response body as a generator
        '''
        for i in self.body:
            yield i if isinstance(i, bytes) else i.encode(self._encoding)


class Router:
    '''
    Abstract the routing-table logic as a class, mapping regular expression patterns to callables
    '''
    def __init__(self) -> None:
        self.__routing_table: dict[str, Callable] = {}

    def add_route(self, pattern: str, callback: Callable) -> None:
        '''
        Add a new pattern-callable mapping to the routing-table
        '''
        self.__routing_table[pattern] = callback

    def match(self, path: str) -> tuple[Callable, tuple]:
        '''
        Match each pattern inside the table with the input path and return the corresponding callable
        '''
        for pattern, func in self.__routing_table.items():
            m = re.match(pattern, path)
            if m:
                return (func, m.groups())
        raise Exception(f'{NOT_FOUND}')


def application(environment, start_response):
    '''
    Extract the 'router' object from the other file, match the incoming request's path with the
    routing table, and route to the intended endpoint
    '''
    module = importlib.import_module(os.getenv(APP_ENV_NAME))
    router: Router = getattr(module, ROUTER_NAME)
    req = Request(environment)
    path = req.path

    try:
        callback, args = router.match(path)
        res: Response = callback(req.queries, args)
    except Exception as e:
        error_code = str(e)
        res = Response(status_code=int(error_code))
    start_response(res.status, res.headers)
    return iter(res)
