from app.models.mysql import certificate, staff
from sqlalchemy import select


class Staff:
    async def add(self, request, row):
        conn = request.app.ctx.db
        try:
            query = staff.insert().values(**row)
            print(query)
            await conn.execute(query=query)
        except Exception as e:
            print(e)
            return False
        else:
            return True

    async def list(self, request, row):
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
        print(result)
        return result

    async def remove(self, request, row):
        conn = request.app.ctx.db
        query = select(staff.c.id).select_from(staff).where(staff.c.id == row["id"])
        res = await conn.fetch_all(query=query)
        if res == []:
            print("ID不存在")
            return False
        try:
            query = staff.delete().where(staff.c.id == row["id"])
            print(query)
            await conn.execute(query=query)
        except Exception as e:
            print(e)
            return False
        else:
            return True

    async def change(self, request, row):
        conn = request.app.ctx.db
        try:
            query = staff.update().where(staff.c.id == row["id"]).values(**row)

            await conn.execute(query=query)
        except Exception as e:
            print(e)
            return False
        else:
            return True


class Certificate:
    async def add(self, request, row):
        conn = request.app.ctx.db
        try:
            query = certificate.insert().values(**row)
            await conn.execute(query=query)
        except Exception as e:
            print(e)
            return False
        else:
            return True

    async def remove(self, request, row):
        conn = request.app.ctx.db
        try:
            query = certificate.delete().where(staff.c.id == row["id"])
            await conn.execute(query=query)
        except Exception as e:
            print(e)
            return False
        else:
            return True

    async def change(self, request, row):
        conn = request.app.ctx.db
        try:
            query = (
                certificate.update().where(certificate.c.id == row["id"]).values(**row)
            )
            await conn.execute(query=query)
        except Exception as e:
            print(e)
            return False
        else:
            return True
