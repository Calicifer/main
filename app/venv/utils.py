from functools import wraps
from flask import make_response, request

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == "user" and auth.password == "pass":
            return f(*args, **kwargs)
        return make_response('Authentication required', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    return decorated