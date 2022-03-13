from sanic.response import json


async def check_auth(request):
    if (
        request.form.get("username") != request.app.config.custom["USERNAME"] or request.form.get("password") != request.app.config.custom["PASSWORD"]
    ):
        return json({"code": -1, "msg": "账号或密码不正确"})
    else:
        return json({"code": 0, "msg": "验证成功"})
