# -*- coding: utf-8 -*-
from app.services import services
from sanic import Blueprint, response
from sanic.response import json
from sanic_validation import validate_args, validate_json

certificate = Blueprint("certificate", url_prefix="/staff/certificate")


@certificate.get("/remove")
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


@certificate.get("/list")
async def lists(request):
    c_id = request.args.get("c_id", None)
    c_name = request.args.get("c_name", None)
    s_id = request.args.get("s_id", None)
    res = await services.certificate.list(request, c_id, c_name, s_id)
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


@certificate.post("/add")
async def add(request):
    c_name = request.form.get("c_name")
    s_id = request.form.get("s_id")
    c_imgpath = "./static/{}_{}.jpg".format(s_id, c_name)
    row = {
        "c_name": c_name,
        "s_id": s_id,
        "c_imgpath": c_imgpath
    }
    res = await services.certificate.add(request, row)
    if res:
        return await response.file_stream(
            c_imgpath,
            chunk_size=1024,
            mime_type="application/form-data"
        )
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
