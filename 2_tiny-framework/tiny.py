'''
A tiny web framework, abstracting WSGI concepts as Request/Response classes
'''

from urllib.parse import parse_qs
from wsgiref.headers import Headers
from http.client import responses

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


def wrapper(func):
    '''
    Wrap a request-in response-out application as a WSGI-callable function
    '''
    def application(environment, start_response):
        req = Request(environment=environment)
        res: Response = func(req)
        start_response(res.status, res.headers)
        return iter(res)
    return application
