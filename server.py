from databases import Database
from orjson import dumps
from sanic import Sanic

from app.routes import routes
from config.config import config

# from middleware.auth import check_auth

# 将默认的json换成orjson
app = Sanic("SACMS", dumps=dumps)


# 配置注入到上下文中
app.config.custom = config

# 配置数据库
database = Database(app.config.custom["mysql"])


# 设定监视器，服务开启前连接数据库
@app.before_server_start
async def startup_db(app, loop):
    await database.connect()


# 设定监视器，服务结束之后断开数据库
@app.after_server_stop
async def shutdown_db(app, loop):
    await database.disconnect()


# 将数据库连接池句柄写入数据库上下文
app.ctx.db = database

# # 中间件， 注册到request上
# app.register_middleware(check_auth, "request")

# 蓝图，路由
app.blueprint(routes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6888, workers=1, debug=True, auto_reload=True)
