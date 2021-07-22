import os
from flask import Blueprint
from flask_restful import Resource, marshal_with, fields, reqparse, inputs
from werkzeug.datastructures import FileStorage
from settings import Config
from apps.user.models import UserModel
from exts import api, db

user_bp = Blueprint("user", __name__, url_prefix="/api")


class DeleteShow(fields.Raw):
    def format(self, value):
        print("==========>", value)   # value 就是从数据库获取到到值，因为attribute已经绑定了is_delete字段，所以获取到了它的值
        return "删除" if value else "未删除"


# 定义展示的格式
user_format = {
    "id": fields.Integer,
    # attribute:设置的值是面向数据库的，与数据库保持一直；un是对外的，传参时候用
    # default:没有获取到参数时，使用默认值
    "un": fields.String(attribute="username", default="aoao"),
    "password": fields.String,
    "is_delete": fields.Boolean,
    "is_delete_show": DeleteShow(attribute="is_delete"),  # 绑定数据亏的is_delete字段
    "ctime": fields.DateTime(),
}

# 参数解析
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument("username", type=str, location=["form"])
parser.add_argument("password", type=int, help="6-12位数字", required=True, location=["form"])


# 定义类视图
class UserResource(Resource):
    @marshal_with(user_format)
    def get(self):
        user_list = UserModel.query.all()
        return user_list

    @marshal_with(user_format)
    def post(self):
        args = parser.parse_args()
        username = args.get("username")
        password = args.get("password")
        user = UserModel()
        user.username = username
        user.password = password
        return user


api.add_resource(UserResource, "/user", endpoint="all_user")
