from functools import wraps
from urllib import response

import jwt
from sanic import json


async def check_auth(request):
    if not request.token:
        return False
    try:
        jwt.decode(
            request.token, request.app.config.custom.SECRET, algorithms=["HS256"]
        )
    except jwt.exceptions.InvalidTokenError:
        return False
    else:
        return True

def protected(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authenticated = check_auth(request)

            if is_authenticated:
                response = await f(request, *args, **kwargs)
                return response
            else: 
                return json({
                    "code": -1,
                    "msg": "you are unauthorized"
                }, status=401)
        return decorated_function
    return decorator(wrapped)
