from sanic import response
from sanic_openapi import swagger_blueprint, doc
from sanic.response import json
from sanic.views import HTTPMethodView

from controller.auth import class_authorized
from models.notice import get_notices


class Notices(HTTPMethodView):
    # 使用装饰器鉴权
    @class_authorized
    @doc.description('获取公告，需要 Cookie')
    def get(self, req):
        return response.json(get_notices())
