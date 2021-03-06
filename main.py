from sanic import Sanic, response
from sanic_openapi import swagger_blueprint, doc
from sanic_session import Session, InMemorySessionInterface

from controller.auth import authorized
import controller.auth
import controller.block
import controller.notice

app = Sanic(name='blockChainServer')
app.blueprint(swagger_blueprint)
Session(app, interface=InMemorySessionInterface())


@app.route("/")
async def test(request):
    return response.json({"hello": "world"})


app.add_route(controller.auth.Auth.as_view(), '/api/login')
app.add_route(controller.block.Block.as_view(), '/api/blocks')
app.add_route(controller.notice.Notices.as_view(), '/api/notices')

if __name__ == "__main__":
    app.run(debug=True, access_log=True)
