# -*- coding: utf-8 -*-
from app.services import services
from sanic import Blueprint
from sanic.response import json, raw
from sanic_validation import validate_json

certificate = Blueprint("certificate", url_prefix="/staff/certificate")


@certificate.delete("/<c_id:int>")  # 移除证件 1
async def remove(request, c_id):
    row = {
        "c_id": c_id
    }
    res = await services.certificate.remove(request, row)
    if res:
        return json({"code": 0, "msg": "删除成功"})
    else:
        return json({"code": -1, "msg": "删除失败"})

@certificate.post("/lists")  # 获取所有证件信息
@validate_json(
    {
        "searchKey": {"type": "string", "required": False},
        "searchValue": {"required": False},
        "currentpage": {"type": "integer", "required": False},  # 当前第几页
        "listrows": {"type": "integer", "required": False},  # 每页多少行
    }
)
async def lists(request):
    row = {
        "curpage": int(request.json.get("currentpage", 1)),
        "listrows": int(request.json.get("listrows", 10)),
    }
    if request.json.get("searchKey"):
        row["searchKey"] = request.json.get("searchKey")
        row["searchValue"] = request.json.get("searchValue")
    print(row)
    res = await services.certificate.lists(request, row)
    return json({'code': 0, 'msg': '获取成功', 'data': res })

@certificate.post("/list")  # 获取证件
async def list_cert(request):
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
        elif res == []:
            return json({"code": 0, "msg": "查询成功", "data": res})
        else:
            return json({"code": -1, "msg": "查询失败"})
    else:
        return json({"code": -1, "msg": "关键字错误"})


@certificate.post("/add")  # 添加证件 1
async def add(request):
    c_id = request.form.get("c_id")
    s_id = request.form.get("s_id")
    c_name = request.form.get("c_name")
    c_stime = request.form.get("c_stime")
    c_etime = request.form.get("c_etime")
    c_img = list(request.files.get("file"))[1]
    row = {
        "c_id" : c_id,
        "c_name": c_name,
        "c_stime" : c_stime,
        "c_etime" : c_etime,
        "s_id": s_id,
        "c_img": c_img
    }
    print("\n"*10)
    print(row)
    res = await services.certificate.add(request, row)
    if res == 0:
        return json({"code": 0, "msg": "上传成功"})
    elif res == -2:
        return json({"code": -2, "msg": "职工号不存在"})
    else:
        return json({"code": -1, "msg": "上传失败"})

@certificate.get("/img/<id:int>")
async def getImg(request, id: int):
    print("\n"* 10)
    print("获取图片")
    row = {
        "id" : id
    }
    res = await services.certificate.getImg(request, row)
    if res:
        return raw(res)
    else:
        return json({"code": -1, "msg": "获取失败"})
