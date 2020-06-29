from functools import wraps

from sanic import response
from sanic.response import json
from sanic_session import Session

from models.user import get_user_by_device_id
from sanic.views import HTTPMethodView
from sanic_openapi import doc


class Auth(HTTPMethodView):
    @doc.description('登录接口，所需参数有username,password')
    @doc.consumes(doc.JsonBody(
        {
            "device_id": doc.String("456"),
            "password": doc.String("123"),
        }
    ),
        location="body",
    )
    @doc.response(400, {"msg": str}, description="帐号密码输错了")
    @doc.response(500, {'msg': str}, description="程序出错，找后端查看日志")
    @doc.response(403, {'msg': str}, description="未登录")
    def post(self, req):
        try:
            device_id = req.json['device_id']
            login_user = get_user_by_device_id(device_id)
            if login_user['password'] == "" or req.json['password'] != login_user['password']:
                return response.json({'msg': '帐号不存在或密码错误'}, status=400)
            # 默认无法序列化实体类，使用 dict 代替
            req.ctx.session['user'] = login_user
            return response.json(login_user)
        except Exception as e:
            print(e)
            return response.json({'msg': '服务器错误'}, status=500)


def check_authorization(req):
    return req.ctx.session.get('user')


def authorized(f):
    @wraps(f)
    async def decorated_function(request, *args, **kwargs):
        print(request)
        print(args)
        print(kwargs)
        login_user = check_authorization(request)

        # 用户未登录
        if login_user is None:
            return json({'msg': '未登录'}, 403)

        # 用户已登录
        # 运行 handler 方法，并返回 response
        resp = await f(request, *args, **kwargs)
        return resp

    return decorated_function


def class_authorized(f):
    @wraps(f)
    async def decorated_function(self, request, *args, **kwargs):
        print(request)
        login_user = check_authorization(request)

        # 用户未登录
        if login_user is None:
            return json({'msg': '未登录'}, 403)

        # 用户已登录
        # 运行 handler 方法，并返回 response
        resp = f(self, request, *args, **kwargs)
        return resp

    return decorated_function
