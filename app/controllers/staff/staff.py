from app.services import services
from sanic import Blueprint
from sanic.response import json
from sanic_validation import validate_args, validate_json

staff = Blueprint("staff", url_prefix="/staff/")


@staff.get("/remove")  # 删除员工
@validate_args(
    {
        "id": {"type": "string", "required": True},
    }
)
async def remove(request):
    row = {
        "id": int(request.args.get("id", 0)),
    }
    res = await services.staff.remove(request, row)
    if res:
        return json({"code": 0, "msg": "删除成功"})
    else:
        return json({"code": -1, "msg": "删除失败"})


@staff.get("/list")  # 获取员工详细信息
@validate_args(
    {
        "id": {"type": "string", "required": True},  # 职工号
    }
)
async def lists(request):
    row = {"id": int(request.args.get("id"))}
    res = await services.staff.list(request, row)
    if res:
        return json({"code": 0, "msg": "查询成功", "data": res})
    else:
        return json({"code": -1, "msg": "查询失败"})


@staff.post("/add")  # 添加职工
@validate_json(
    {
        "name": {"type": "string", "required": True},
        "cardnum": {
            "type": "string",
            "required": True,
            "regex": r"(^\d{15}$)|(^\d{17}([0-9]|X$))",
        },
        "mobile": {
            "type": "string",
            "required": True,
            "regex": r"^1[3456789]\d{9}$",  # 正则匹配手机号
        },
        "email": {"type": "string", "required": True},
        "sex": {"type": "integer", "required": True, "allowed": [0, 1]},
        "province": {"type": "string", "required": True},
        "city": {"type": "string", "required": True},
        "area": {"type": "string", "required": True},
        "nation": {"type": "string", "required": True},
        "birth": {"type": "string", "required": True},
        "marriage": {"type": "integer", "required": True},
        "department": {"type": "string", "required": True},
        "job": {"type": "string", "required": True},
    }
)
async def add(request):
    row = {
        "name": request.json.get("name"),
        "cardnum": request.json.get("cardnum"),
        "mobile": request.json.get("mobile"),
        "email": request.json.get("email"),
        "sex": request.json.get("sex"),
        "province": request.json.get("province"),
        "city": request.json.get("city"),
        "area": request.json.get("area"),
        "nation": request.json.get("nation"),
        "birth": request.json.get("birth"),
        "marriage": request.json.get("marriage"),
        "department": request.json.get("department"),
        "job": request.json.get("job"),
    }
    print(row)
    res = await services.staff.add(request, row)
    if res:
        return json({"code": 0, "msg": "添加成功"})
    else:
        return json({"code": -1, "msg": "添加失败"})


@staff.post("/change")  # 修改职工信息
async def change(request):
    request.json.query_args()
    row = {
        "id": request.json.get("id"),
    }
    for k in row.keys():
        if not row[k]:
            del row[k]
    res = await services.staff.change(request, row)
    if res:
        return json({"code": 0, "msg": "修改成功"})
    else:
        return json({"code": -1, "msg": "修改失败"})
