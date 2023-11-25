'''
Request/Response abstraction for WSGI concepts
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


def app_wrapper(func):
    '''
    Wrap a request-in response-out application as a WSGI-callable function
    '''
    def application(environment, start_response):
        req = Request(environment=environment)
        res: Response = func(req)
        start_response(res.status, res.headers)
        return iter(res)
    return application

@app_wrapper
def req_res_app(request: Request) -> Response:
    '''
    Main app; Greet the incoming 'name' query element if availabe;
    otherwise, greet the World!
    '''
    names = ' & '.join([i for i in request.queries.get('name', ['World']) if len(i) > 0 and i != ' '])
    message = f'<h1>Hello, {names}!</h1>'
    res = Response(body=[message])
    return res
