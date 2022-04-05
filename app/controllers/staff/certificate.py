# -*- coding: utf-8 -*-
from asyncio import constants

from app.services import services
from sanic import Blueprint
from sanic.response import json
from sanic_validation import validate_args, validate_json

certificate = Blueprint("certificate", url_prefix="/staff/certificate")


@certificate.post("/remove")  # 移除证件 1
@validate_args(
    {
        "c_id": {"type": "string", "required": True},
    }
)
async def remove(request):
    row = {
        "c_id": int(request.args.get("c_id", 0)),
    }
    res = await services.certificate.remove(request, row)
    if res:
        return json({"code": 0, "msg": "删除成功"})
    else:
        return json({"code": -1, "msg": "删除失败"})


@certificate.post("/list")  # 获取证件
async def lists(request):
    c_id = request.json.get("c_id")
    c_name = request.json.get("c_name")
    s_id = request.json.get("s_id")
    res = None
    print(s_id)
    if c_id:
        res = await services.certificate.list_by_c_id(request, c_id)
        if res:
            data = {
                "c_id": res[0],
                "c_name": res[1],
                "c_imgpath": res[2],
                "s_id": res[3]
            }
            return json({"code": 0, "msg": "查询成功", "data": data})
        else:
            return json({"code": -1, "msg": "查询失败"})
    elif c_name:
        res = await services.certificate.list_by_c_name(request, c_name)
        if res:
            return json({"code": 0, "msg": "查询成功", "data": res})
        else:
            return json({"code": -1, "msg": "查询失败"})
    elif s_id:
        res = await services.certificate.list_by_s_id(request, s_id)
        if res:
            return json({"code": 0, "msg": "查询成功", "data": res})
        else:
            return json({"code": -1, "msg": "查询失败"})
    else:
        return json({"code": -1, "msg": "关键字错误"})


@certificate.post("/add")  # 添加证件 1
async def add(request):
    s_id = request.form.get("s_id")
    c_name = request.form.get("c_name")
    c_img = list(request.files.get("file"))
    row = {
        "c_name": c_name,
        "s_id": s_id,
        "c_img": c_img
    }
    print(row)
    res = await services.certificate.add(request, row)
    print(res)
    return json({"code": 0, "msg": "上传成功"}) \
        if res > 0 else json({"code": -1, "msg": "上传失败"})


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



    
