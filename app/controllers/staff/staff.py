from app.services import services
# from middleware.auth import protected
from sanic import Blueprint
from sanic.response import json
from sanic_validation import validate_json

staff = Blueprint("staff", url_prefix="/staff/")


@staff.post("/remove")  # 删除员工1
@validate_json(
    {
        "id": {"type": "integer", "required": True},
    }
)
async def remove(request):
    row = {
        "id": int(request.json.get("id", 0)),
    }
    res = await services.staff.remove(request, row)
    if res:
        return json({"code": 0, "msg": "删除成功"})
    else:
        return json({"code": -1, "msg": "删除失败"})


@staff.post("/list")  # 获取员工详细信息1
@validate_json(
    {
        "id": {"type": "string", "required": True},  # 职工号
    }
)
async def lists(request):
    row = {"id": int(request.json.get("id"))}
    res = await services.staff.list(request, row)
    if res:
        return json({"code": 0, "msg": "查询成功", "data": res})
    else:
        return json({"code": -1, "msg": "查询失败"})


@staff.post("/add")  # 添加职工1
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
        "sex": {"type": "string", "required": True},
        "province": {"type": "string", "required": True},
        "city": {"type": "string", "required": True},
        "area": {"type": "string", "required": True},
        "nation": {"type": "string", "required": True},
        "marriage": {"type": "string", "required": True},
        "birth" : {"type": "string", "required":True},
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
    row["birth"] = row["birth"].split("T")[0]
    print(row)
    res = await services.staff.add(request, row)
    print(res)
    if res >= 0:
        return json({"code": 0, "msg": "添加成功", 'data': {'s_id': res}})
    elif res == -1:
        return json({"code": -1, "msg": "重复添加"})
    else:
        return json({"code": -2, "msg": "添加失败"})


@staff.post("/change")  # 修改职工信息 1
@validate_json(
    {
        "id": {"type": "integer", "required": True},
        "name": {"type": "string", "required": False},
        "cardnum": {
            "type": "string",
            "required": False,
            "regex": r"(^\d{15}$)|(^\d{17}([0-9]|X$))",
        },
        "mobile": {
            "type": "string",
            "required": False,
            "regex": r"^1[3456789]\d{9}$",  # 正则匹配手机号
        },
        "email": {"type": "string", "required": False},
        "marriage": {"type": "string", "required": False},
        "department": {"type": "string", "required": False},
        "job": {"type": "string", "required": False},
    }
)
async def change(request):
    print(request)
    items = ["id", "name", "mobile", "email", "marriage", "department", "job"]
    row = {}
    for item in items:
        value = request.json.get(item)
        if value is not None:
            row[item] = value
    res = await services.staff.change(request, row)
    if res:
        return json({"code": 0, "msg": "修改成功"})
    else:
        return json({"code": -1, "msg": "修改失败"})


@staff.post("/lists")  # 获取职工列表
@validate_json(
    {
        "currentpage": {"type": "integer", "required": False},  # 当前第几页
        "listrows": {"type": "integer", "required": False},  # 每页多少行
    }
)
async def lists(request):
    row = {
        "curpage": int(request.json.get("currentpage", 1)),
        "listrows": int(request.json.get("listrows", 10)),
    }
    res = await services.staff.lists(request, row)
    return json({'code': 0, 'msg': '获取成功', 'data': res })
