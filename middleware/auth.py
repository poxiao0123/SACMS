import jwt
from sanic.response import json


async def check_token(request):
    url = request.url
    if "/api/login" in url:
        ...
    elif "/api/staff/certificate/img" in url:
        ...
    else:  # 判断是否为登录或者获取图片
        if not request.token:  # 没有token
            return json({'code': -1, 'msg': '未认证'}, status=401)
        try:
            jwt.decode(request.token, request.app.config.custom['SECRET'], algorithms=['HS256'])
        except jwt.exceptions.InvalidAlgorithmError:  # token验证出错
            return json({'code': -1, 'msg': '未认证'}, status=401)
        except jwt.exceptions.ExpiredSignatureError:  # token过期
            return json({'code': -2, 'msg': 'token过期'}, status=401)
