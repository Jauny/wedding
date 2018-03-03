import logging
from functools import wraps
from flask import request

logger = logging.getLogger(__name__)


def log_endpoint(func):
    """Log requests through endpoint, including form data."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        form = {}
        for k, v in request.form.iteritems():
            form[k] = v

        logger.info({
            'msg': 'received {method} request to {endpoint}'.format(
                method=request.method, endpoint=request.endpoint),
            'form': form})

        return func(*args, **kwargs)
    return wrapper
