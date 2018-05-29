from functools import wraps
from flask import request


def log_endpoint(logger):
    def actual_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            form = {}
            for k, v in request.form.iteritems():
                form[k] = v

            params = {}
            for k, v in request.args.iteritems():
                params[k] = v

            logger.info({
                'msg': 'received {method} request to {endpoint}'.format(
                    method=request.method, endpoint=request.endpoint),
                'form': form,
                'params': params})
            return func(*args, **kwargs)
        return wrapper
    return actual_decorator
