'''
Two endpoints for a simple web application based on the route-capable Tiny web framework
'''

from .tiny import Response, Router

def hello(names: tuple) -> Response:
    message = [f'<h1>Hello, {name}!</h1>' for name in names]
    return Response(body=message)

def goodbye(names: tuple) -> Response:
    message = [f'<h1>Goodbye, {name}!</h1>' for name in names]
    return Response(body=message)


router = Router()
router.add_route(r'^/hello/(\w*)$', hello)
router.add_route(r'^/goodbye/(\w*)$', goodbye)
