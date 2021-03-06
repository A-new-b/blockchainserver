from sanic import response
from sanic_openapi import swagger_blueprint, doc
from sanic.response import json
from sanic.views import HTTPMethodView

from controller.auth import class_authorized
from models.block_chain import get_blocks_by_device_id


class Block(HTTPMethodView):
    # 使用装饰器鉴权
    @class_authorized
    @doc.description('获取区块，需要 Cookie')
    def get(self, req):
        return response.json(get_blocks_by_device_id(req.ctx.session.get('user')['device_id']))
