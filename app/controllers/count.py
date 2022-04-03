from app.services import services
from sanic import Blueprint
from sanic.response import json

count = Blueprint(name="count", url_prefix="/count")


@count.get("/")
async def getStaffCount(request):
    res = await services.staff.count(request)
    print(res)
    if res:
        return json({"code": 0, "msg": "获取成功", "data": res})
    else:
        return json({"code": 0, "msg": "获取失败"})
