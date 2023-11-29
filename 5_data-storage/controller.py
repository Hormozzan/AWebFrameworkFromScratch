'''
Two endpoints for a simple web application based on the route-capable Tiny web framework
'''

from .tiny import Response, Router
from .view import render
from .model import RedisClient
import json


redis = RedisClient()

def setup(func):
    '''
    A wrapper for endpoints, process query and path variables, and return html or json response
    '''
    def wrapper(queries: dict[str, str], names: tuple) -> Response:
        name = names[0]
        greet, number = func(name)
        content_type = queries.get('content-type', ('html',))[0]
        match content_type:
            case 'html':
                message = [render(name=name, greet=greet, number=number)]
                return Response(body=message)
            case 'json':
                j = {
                        'name': name,
                        'greet': greet,
                        'number': number
                    }
                message = json.dumps(j)
                return Response(content_type='application/json', body=message)
    return wrapper

@setup
def hello(key: str) -> tuple[bool, int]:
    '''
    Increment the 'number' variable of each input 'name' on each invocation
    '''
    val = redis.incr_get(key)
    return (True, val)

@setup
def goodbye(key: str) -> tuple[bool, int]:
    '''
    Decrement the 'number' variable of each input 'name' on each invocation
    '''
    val = redis.decr_get(key)
    return (False, val)

router = Router()
router.add_route(r'^/hello/(\w*)$', hello)
router.add_route(r'^/goodbye/(\w*)$', goodbye)
