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
        return json({"code": 0, "msg": "验证成功"})
