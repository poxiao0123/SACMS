from datetime import datetime
from time import time

import jwt
from sanic import Blueprint
from sanic.response import json
from sanic_validation import validate_json

login = Blueprint("login", url_prefix="/login")


@login.post("/")
@validate_json(
    {
        "username": {"type": "string", "required": True},  # 账号
        "password": {"type": "string", "required": True},  # 密码
    }
)
async def admin_login(request):
    username = request.json.get("username")
    password = request.json.get("password")
    print(username, password)
    if (
        username != request.app.config.custom["USERNAME"]
        or password != request.app.config.custom["PASSWORD"]
    ):
        return json({"code": -1, "msg": "账号或密码不正确"})
    else:
        current_time = time()
        # current_time = datetime.now()
        print(current_time)
        header = {
            'typ': 'JWT',
            'alg': 'HS256'
        }
        payload = {
            'iat': current_time,
            'exp': current_time + 10800,
        }
        token = jwt.encode(payload=payload, key=request.app.config.custom["SECRET"], algorithm=['HS256'], headers=header)
        print(token)
        return json(
            {
                'code': 0,
                'msg': '登录成功',
                'data': {
                    'token': token
                }
            }
        )
