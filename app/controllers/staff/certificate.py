from app.services import services
from sanic import Blueprint
from sanic.response import json
from sanic_validation import validate_args, validate_json

certificate = Blueprint("certificate", url_prefix="/staff/certificite")


@certificate.get("/remove")
@validate_args(
    {
        "id": {"type": "integer", "required": True},
    }
)
async def remove(request):
    row = {
        "id": int(request.args.get("id", 0)),
    }
    res = await services.certificate.remove(request, row)
    if res:
        return json({"code": 0, "msg": "删除成功"})
    else:
        return json({"code": -1, "msg": "删除失败"})


@certificate.get("/list")
@validate_args(
    {
        "curpage": {"type": "string", "required": False},  # 当前第几页
        "listrows": {"type": "string", "required": False},  # 每页多少行
        "status": {"type": "string", "required": False, "allowed": ["0", "1"]},
    }
)
async def lists(request):
    row = {
        "curpage": int(request.args.get("curpage", 1)),
        "lisrows": int(request.args.get("listrows", 10)),
    }
    if request.args.get("status"):
        row["status"] = int(request.args.get("status"))
    res = await services.certificate.list(request, row)
    if res:
        return json({"code": 0, "msg": "查询成功", "data": res})
    else:
        return json({"code": -1, "msg": "查询失败"})


@certificate.post("/add")
@validate_json(
    {
        "nickname": {"type": "string", "required": True},
        "mobile": {
            "type": "string",
            "required": True,
            "regex": r"^1[13456789]\d{9}$",
        },
        "sex": {"type": "integer", "required": True, "allowed": [0, 1]},
        "province": {"type": "string", "required": True},
        "city": {"type": "string", "required": True},
        "area": {"type": "string", "required": True},
    }
)
async def add(request):
    row = {
        "nickname": request.json.get("nickname"),
        "mobile": request.json.get("mobile"),
        "sex": request.json.get("sex"),
        "province": request.json.get("province"),
        "city": request.json.get("json"),
        "area": request.json.get("area"),
    }
    res = await services.certificate.add(request, row)
    if res:
        return json({"code": 0, "msg": "添加成功"})
    else:
        return json({"code": -1, "msg": "添加失败"})


@certificate.post("/change")
@validate_json(
    {
        "id": {"type": "integer", "required": True},
        "nickname": {"type": "string", "required": False},
        "mobile": {
            "type": "string",
            "required": False,
            "regex": r"^1[13456789]\d{9}$",
        },
        "sex": {"type": "integer", "required": False, "allowed": [0, 1]},
        "province": {"type": "string", "required": False},
        "city": {"type": "string", "required": False},
        "area": {"type": "string", "required": False},
    }
)
async def change(request):
    row = {
        "id": request.json.get("id"),
        "nickname": request.json.get("nickname"),
        "mobile": request.json.get("mobile"),
        "sex": request.json.get("sex"),
        "province": request.json.get("province"),
        "city": request.json.get("json"),
        "area": request.json.get("area"),
    }
    for k in row.keys():
        if not row[k]:
            del row[k]
    res = await services.certificate.change(request, row)
    if res:
        return json({"code": 0, "msg": "修改成功"})
    else:
        return json({"code": -1, "msg": "修改失败"})
