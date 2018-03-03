from functools import wraps
from flask import request


def log_endpoint(logger):
    def actual_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            form = {}
            for k, v in request.form.iteritems():
                form[str(k)] = str(v)

            logger.info({
                'msg': 'received {method} request to {endpoint}'.format(
                    method=request.method, endpoint=request.endpoint),
                'form': form})
            return func(*args, **kwargs)
        return wrapper
    return actual_decorator
