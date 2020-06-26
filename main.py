from sanic import Sanic, response
from sanic_openapi import swagger_blueprint, doc
from sanic_session import Session, InMemorySessionInterface

from controller.auth import authorized
import controller.auth

from conn.connection import connect
from sanic.log import logger
from sanic.response import text

app = Sanic(name='blockChainServer')
app.blueprint(swagger_blueprint)
Session(app, interface=InMemorySessionInterface())


@app.route("/")
async def test(request):
    return response.json({"hello": "world"})


# 公告
# 鉴权装饰器位于 controller.auth
@app.route("/post")
@authorized
async def test(request):
    return response.json({"hello": "world"})


app.add_route(controller.auth.Auth.as_view(), '/api/login')

if __name__ == "__main__":
    app.run(debug=True, access_log=True)
