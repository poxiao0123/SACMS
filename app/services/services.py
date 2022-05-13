import os
import shutil

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
        else:
            query = (
                select(staff)
                .limit(row["listrows"])
                .offset(int(row['curpage'] -1) * row["listrows"])
            )
        res = await conn.fetch_all(query=query)
        results = []
        for item in res:
            item = list(item)
            staff_items = ["id", "s_id", "name", "cardnum", "mobile", "email", "sex", "province", "city", "area", "nation", "birth", "marriage", "department", "job"]
            result = {}
            for i in range(len(staff_items)):
                result[staff_items[i]] = item[i]
            results.append(result)
        return results

    async def add(self, request, row):  # 添加新员工数据 1
        conn = request.app.ctx.db
        try:
            query = staff.insert().values(**row)
            await conn.execute(query=query)
            query = select(staff.c.s_id).where(staff.c.cardnum == row["cardnum"])
            res = await conn.fetch_one(query = query)
            res = list(res)[0]
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
            select(staff.c.id, staff.c.s_id, staff.c.name,staff.c.cardnum, staff.c.mobile, staff.c.email, staff.c.sex, staff.c.province, staff.c.city, staff.c.area, staff.c.nation, staff.c.birth, staff.c.marriage, staff.c.department, staff.c.job)
            .where(staff.c.id == row["id"])
        )
        res = await conn.fetch_one(query=query)
        res = list(res)  # 将元组转为列表
        staff_items = ["id", "s_id", "name", "cardnum", "mobile", "email", "sex", "province", "city", "area", "nation", "birth", "marriage", "department", "job"]
        result = {}
        for i in range(len(staff_items)):
            result[staff_items[i]] = res[i]
        print(result)
        return result

    async def remove(self, request, row):  # 删除员工信息 1
        conn = request.app.ctx.db
        try:
            query = staff.delete().where(staff.c.s_id == row["s_id"])
            res = await conn.execute(query=query)
            print("\n"*10)
            print(res)
            if res > 0:
                query = certificate.delete().where(certificate.c.s_id == row["s_id"])
                await conn.execute(query=query)
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
                .where(staff.c.s_id == row["id"])
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
            conn = request.app.ctx.db
            # 查询是否存在该员工
            query = select(staff).where(staff.c.s_id == row["s_id"])
            res = await conn.fetch_one(query=query)
            print("\n" *10)
            print(res)
            if not res:
                return -2
            else:
                query = certificate.insert().values(**row)
                res = await conn.execute(query=query)
                return 0 if res > 0 else -1
        except Exception as e:
            print(e)
            return False

    async def remove(self, request, row):  # 删除员工证件 1
        # 删除证件信息
        conn = request.app.ctx.db
        query = certificate.delete().where(certificate.c.c_id == row["c_id"])
        res = await conn.execute(query=query)
        print(res)
        if res > 0:
           return True
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
        query = str(
                select(certificate.c.c_id, certificate.c.c_name, certificate.c.c_stime, certificate.c.c_etime, certificate.c.s_id, staff.c.name, staff.c.department, staff.c.job, certificate.c.id)
                .select_from(
                    certificate.outerjoin(
                        staff,staff.c.s_id==certificate.c.s_id
                    )
                )
            )
        # 判断是否为特定条件查询
        if "searchKey" in row:
            searchKey = row["searchKey"]
            searchValue = row["searchValue"]
            where = f" where certificate.{searchKey}='{searchValue}' "
            query = query + where
        query = query + " limit {} offset {}".format(row["listrows"],int(row['curpage'] -1) * row["listrows"])
        print("\n"* 10)
        print(query)
        res = await conn.fetch_all(query=query)
        results = []
        for item in res:
            item = list(item)
            cert_items = ['c_id', 'c_name', 'c_stime', 'c_etime', 's_id', 's_name', 's_department', 's_job', 'id']
            result = {}
            for i in range(len(cert_items)):
                result[cert_items[i]] = item[i]
            results.append(result)
        print(results)
        return results

    async def list_by_c_id(self, request, row):  # 按照证件id获取 1
        conn = request.app.ctx.db
        query = (
            select(certificate)
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
            select(certificate)
            .where(certificate.c.s_id == row)
        )
        res = await conn.fetch_all(query=query)
        results = []
        for item in res:
            item = list(item)
            cert_items = ["c_id", "c_name", "c_img", "s_id"]
            result = {}
            for i in range(len(cert_items)):
                result[cert_items[i]] = item[i]
            results.append(result)
        return results

    # 获取证件图片
    async def getImg(self, request, row):
        conn = request.app.ctx.db
        query = (
            select(certificate.c.c_img)
            .where(certificate.c.id == row['id'])
        )
        res = await conn.fetch_one(query=query)
        res = list(res)[0]
        return res
