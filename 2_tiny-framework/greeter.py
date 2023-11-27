'''
A simple web application based on the Tiny web framework
'''

from .tiny import Request, Response, wrapper

@wrapper
def req_res_app(request: Request) -> Response:
    '''
    Main app; Greet the incoming 'name' query element if availabe;
    otherwise, greet the World!
    '''
    names = ' & '.join([i for i in request.queries.get('name', ['World']) if len(i) > 0 and i != ' '])
    message = f'<h1>Hello, {names}!</h1>'
    res = Response(body=[message])
    return res
