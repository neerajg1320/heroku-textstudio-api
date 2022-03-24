from werkzeug.wrappers import Request, Response, ResponseStream
import time

class middleware():
    '''
    Simple WSGI middleware
    '''

    def __init__(self, app, delay):
        self.app = app
        self.delay = delay

    def __call__(self, environ, start_response):
        request = Request(environ)
        if (request.method == "POST"):
            if self.delay > 0:
                print("simple_delay_middleware: adding delay of {}ms to POST request".format(self.delay))
                time.sleep(self.delay)
        
        return self.app(environ, start_response)
