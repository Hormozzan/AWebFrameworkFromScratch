'''
Two endpoints for a simple web application based on the route-capable Tiny web framework
'''

from .tiny import Response, Router
from .view import render
import json

def control_wrapper(func):
    '''
    A wrapper for endpoints, process query and path variables, and return html or json response
    '''
    def setup_response(queries: dict[str, str], names: tuple) -> Response:
        greet = func()
        name = names[0]
        content_type = queries.get('content-type', ('html',))[0]
        match content_type:
            case 'html':
                message = [render(name=name, greet=greet)]
                return Response(body=message)
            case 'json':
                j = {
                        'name': name,
                        'greet': greet
                    }
                message = json.dumps(j)
                return Response(content_type='application/json', body=message)
    return setup_response

@control_wrapper
def hello(): return True

@control_wrapper
def goodbye(): return False

router = Router()
router.add_route(r'^/hello/(\w*)$', hello)
router.add_route(r'^/goodbye/(\w*)$', goodbye)
