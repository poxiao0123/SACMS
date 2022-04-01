from functools import wraps

import jwt
from sanic.response import json


async def check_token(request):
    if not request.token:  # 没有token
        return -1
    try:
        jwt.decode(request.token, request.app.config.custom['SECRET'], algorithms=['HS256'])
    except jwt.exceptions.InvalidAlgorithmError:  # token验证出错
        return -1
    except jwt.exceptions.ExpiredSignatureError:  # token过期
        return -2
    else:  # 验证成功
        return 0

def protected(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authenticated = await check_token(request)
            if is_authenticated == 0:
                response = await f(request, *args, **kwargs)
                return response
            if is_authenticated == -1:
                return json({'code': -1, 'msg': '未认证'}, status=401)
            if is_authenticated == -2:
                return json({'code': -2, 'msg': 'token过期'}, status=401)
        return decorated_function
    return decorator(wrapped)
