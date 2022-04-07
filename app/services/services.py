import os
import shutil
import uuid
from re import search

from app.models.mysql import certificate, staff
from sqlalchemy import func, select


class Staff:  # 员工类 1
    async def lists(self, request, row):  # 获取所有员工数据
        conn = request.app.ctx.db
        # 判断是否为特定条件查询
        if "searchKey" in row:
            searchKey = row["searchKey"]
            searchValue = row["searchValue"]
            listrows = int(row["listrows"])
            curpage = int(row['curpage'])
            query = r"select * from staff "
            where = f"where {searchKey}='{searchValue}' "
            limit = f"limit {listrows} "
            offset = f"offset {(curpage -1) * listrows}"
            query = query + where + limit + offset
            print(query)
        else:
            query = (
                select(['*'])
                .select_from(staff)
                .limit(row["listrows"])
                .offset(int(row['curpage'] -1) * row["listrows"])
            )
        res = await conn.fetch_all(query=query)
        results = []
        for item in res:
            item = list(item)
            staff_items = ["id", "name", "cardnum", "mobile", "email", "sex", "province", "city", "area", "nation", "birth", "marriage", "department", "job"]
            result = {}
            for i in range(len(staff_items)):
                result[staff_items[i]] = item[i]
            results.append(result)
        print(results)
        return results

    async def add(self, request, row):  # 添加新员工数据 1
        conn = request.app.ctx.db
        try:
            query = staff.insert().values(**row)
            print(query)
            await conn.execute(query=query)
            query = staff.select(staff.c.id).where(staff.c.cardnum == row["cardnum"])
            res = await conn.fetch_one(query = query)
            res = res[0]
            print(res)
            return res
        except Exception as e:
            print(type(e))
            if "Duplicate" in str(e):
                return -1
            else:
                return -2

    async def list(self, request, row):  # 获取员工详细信息 1
        conn = request.app.ctx.db
        query = (
            select(["*"])
            .select_from(staff)
            .where(
                staff.c.id == row["id"],
            )
        )
        res = await conn.fetch_one(query=query)
        res = list(res)  # 将元组转为列表
        staff_items = ["id", "name", "cardnum", "mobile", "email", "sex", "province", "city", "area", "nation", "birth", "marriage", "department", "job"]
        result = {}
        for i in range(len(staff_items)):
            result[staff_items[i]] = res[i]
        return result

    async def remove(self, request, row):  # 删除员工信息 1
        conn = request.app.ctx.db
        try:
            query = staff.delete().where(staff.c.id == row["id"])
            res = await conn.execute(query=query)
            if res == 1:
                basepath = os.getcwd()
                stafffilepath =  os.path.join(basepath, "static", str(row["id"]))
                print(stafffilepath)
                # 删除员工照片和目录
                shutil.rmtree(stafffilepath)
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    async def change(self, request, row):  # 修改员工信息 1
        conn = request.app.ctx.db
        try:
            query = (
                staff
                .update()
                .where(staff.c.id == row["id"])
                .values(**row)
            )
            print(query)
            res = await conn.execute(query=query)
            return True if res == 1 else False
        except Exception as e:
            print(e)
            return False


    async def count(self, request):  # 获取员工表和证件表总数
        conn = request.app.ctx.db
        staffquery = (
            select(func.count(["*"]))
            .select_from(staff)
        )
        staffres = await conn.fetch_one(query=staffquery)
        certquery = (
            select(func.count(["*"]))
            .select_from(certificate)
        )
        certres = await conn.fetch_one(query=certquery)
        return {
            "staffcount":staffres[0],
            "certcount": certres[0]
        }

class Certificate:
    async def add(self, request, row):  # 添加员工证件 1
        try:
            # 1 创建图片目录
            basepath = os.getcwd()
            c_folder = os.path.join(basepath, "static", row["s_id"])
            folder = os.path.exists(c_folder)
            if not folder:
                os.makedirs(c_folder)
            img_ext = row['c_img'][2].split('.')[-1]
            imgname = ''.join(str(uuid.uuid4()).split('-'))
            c_imgpath = c_folder + "/" + imgname + "." + img_ext
            # 2 写入文件
            with open(c_imgpath, "wb") as fw:
                fw.write(row['c_img'][1])
            # 3 写入数据库
            conn = request.app.ctx.db
            newrow = {
                "c_name": row['c_name'],
                "c_imgpath": imgname + "." + img_ext,
                "s_id": row["s_id"]
            }
            query = certificate.insert().values(**newrow)
            print(query)
            res = await conn.execute(query=query)
            return True if res > 0 else False
        except Exception as e:
            print(e)
            return False

    async def remove(self, request, row):  # 删除员工证件 1
        # 删除证件信息
        conn = request.app.ctx.db
        query = certificate.delete().where(certificate.c.c_id == row["c_id"])
        res = await conn.execute(query=query)
        basepath = os.getcwd()
        c_folder = os.path.join(basepath, "static", str(row["s_id"]))
        c_imgpath = c_folder + "/" + row["c_imgpath"]
        if res > 0:
            # 3 删除图片,并判断文件夹是否为空，为空则删除文件夹
            try:
                os.remove(c_imgpath)
                if not os.listdir(c_folder):
                    os.rmdir(c_folder)
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return False

    async def change(self, request, row):  # 修改证件
        conn = request.app.ctx.db
        try:
            query = (
                certificate
                .update()
                .where(certificate.c.c_id == row["c_id"])
                .values(**row)
            )
            await conn.execute(query=query)
        except Exception as e:
            print(e)
            return False
        else:
            return True

    async def lists(self, request, row):
        conn = request.app.ctx.db
        # 判断是否为特定条件查询
        if "searchKey" in row:
            searchKey = row["searchKey"]
            searchValue = row["searchValue"]
            listrows = int(row["listrows"])
            curpage = int(row['curpage'])
            query = (
                r"select c.c_id, c.c_name, c.c_imgpath, c.s_id, s.name, s.department, s.job "
                r"from certificate as c "
                r"inner join staff as s "
                r"on c.s_id=s.id "
            )
            where = f"where {searchKey}='{searchValue}' "
            limit = f"limit {listrows} "
            offset = f"offset {(curpage -1) * listrows}"
            query = query + where + limit + offset
            print(query)
        else:
            query = (
                r"select c.c_id, c.c_name, c.c_imgpath, c.s_id, s.name, s.department, s.job "
                r"from certificate as c "
                r"inner join staff as s "
                r"on c.s_id=s.id "
                "limit {} offset {}".format(row["listrows"],int(row['curpage'] -1) * row["listrows"])
            )
        res = await conn.fetch_all(query=query)
        results = []
        for item in res:
            item = list(item)
            cert_items = ['c_id', 'c_name', 'c_imgpath', 's_id', 's_name', 's_department', 's_job']
            result = {}
            for i in range(len(cert_items)):
                result[cert_items[i]] = item[i]
            results.append(result)
        print(results)
        return results

    async def list_by_c_id(self, request, row):  # 按照证件id获取 1
        conn = request.app.ctx.db
        query = (
            select(["*"])
            .select_from(certificate)
            .where(certificate.c.c_id == row)
        )
        res = list(await conn.fetch_one(query=query))
        return res

    async def list_by_c_name(self, request, row):  # 按照证件name获取
        conn = request.app.ctx.db
        query = (
            r"select c_id, c_imgpath, s_id , name "
            r"from certificate as c "
            r"inner join staff as s "
            r"on c.s_id = s.id "
            "where c_name='{}'".format(row)
        )
        res = []
        for r in await conn.fetch_all(query=query):
            r = list(r)
            res.append(r)
        print(res)
        return res

    async def list_by_s_id(self, request, row):  # 按照员工id获取 1
        conn = request.app.ctx.db
        query = (
            select(["*"])
            .select_from(certificate)
            .where(certificate.c.s_id == row)
        )
        res = await conn.fetch_all(query=query)
        results = []
        for item in res:
            item = list(item)
            cert_items = ["c_id", "c_name", "c_imgpath", "s_id"]
            result = {}
            for i in range(len(cert_items)):
                result[cert_items[i]] = item[i]
            results.append(result)
        # print(results)
        return results

    async def getImg(self, request, row):  # 拼接图片地址
        basepath = os.getcwd()
        imgpath = os.path.join(basepath, "static", row["s_id"]) + "/" + row["c_imgpath"]
        return imgpath
