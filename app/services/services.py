from app.models.mysql import certificate, staff
from sqlalchemy import select


class Staff:  # 员工类 1
    async def add(self, request, row):  # 添加新员工数据 1
        conn = request.app.ctx.db
        try:
            query = staff.insert().values(**row)
            print(query)
            res = await conn.execute(query=query)
            return True if res > 0 else False
        except Exception as e:
            print(e)
            return False

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
            print(res)
            return True if res == 1 else False
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


class Certificate:
    async def add(self, request, row):  # 添加员工证件 
        conn = request.app.ctx.db
        try:
            query = certificate.insert().values(**row)
            print(query)
            res = await conn.execute(query=query)
            return True if res > 0 else False
        except Exception as e:
            print(e)
            return False

    async def remove(self, request, row):
        conn = request.app.ctx.db
        query = (
            select(certificate.c.c_id)
            .select_from(certificate)
            .where(certificate.c.c_id == row["c_id"])
        )
        print(query)
        res = conn.fetch_all(query=query)
        print(res)
        # try:
        #     query = (
        #         certificate
        #         .delete()
        #         .where(certificate.c.c_id == row["c_id"])
        #     )
        #     print(query)
        #     await conn.execute(query=query)
        # except Exception as e:
        #     print(e)
        #     return False
        # else:
        #     return True

    async def change(self, request, row):
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

    async def list(self, request, c_id, c_name, s_id):
        conn = request.app.ctx.db
        row = None
        if c_id is not None:
            row = c_id
        elif c_name is not None:
            row = c_name
        else:
            row = s_id
        query = (
            select(["*"])
            .select_from(certificate)
            .where(certificate.c.c_id == row)
        )
        print(query)
        res = await conn.fetch_one(query=query)
        print(res)
        return res
