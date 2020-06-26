from sanic import response
from sanic_openapi import swagger_blueprint, doc
from sanic.response import json
from sanic.views import HTTPMethodView

from controller.auth import authorized
from models.block_chain import get_blocks_by_device_id


class Block(HTTPMethodView):
    """
    应当来讲，这里应当使用 @authorized 装饰器来进行验证，但是 req.ctx 不存在，需要更多资料
    考虑使用中间层进行鉴权
    """

    @doc.description('区块，需要 Cookie')
    # @authorized
    def get(self, req):
        user = req.ctx.session.get('user')
        if user is None:
            return json({'msg': '未登录'}, 403)
        return response.json(get_blocks_by_device_id(user['device_id']))
