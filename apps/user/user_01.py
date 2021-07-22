import os
from flask import Blueprint
from flask_restful import Resource, marshal_with, fields, reqparse, inputs
from werkzeug.datastructures import FileStorage
from settings import Config
from apps.user.models import UserModel
from exts import api, db

user_bp = Blueprint("user", __name__, url_prefix="/api")

# 定义展示的格式
user_format = {
    "id": fields.Integer,
    "username": fields.String,
    "password": fields.String,
    "ctime": fields.DateTime(),
}

# 参数解析
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument("username", type=str, required=True, help="用户名必填", location=["form"])
parser.add_argument("password", type=int, help="6-12位数字", required=True, location=["form"])
parser.add_argument("hobby", action="append")
parser.add_argument("icon", type=FileStorage, location=["files"])
parser.add_argument("cho", type=str, choices=("one", "two"), help="不存在的值")


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
        icon = args.get("icon")
        upload_path = os.path.join(Config.ICON_DIR, icon.filename)
        icon.save(upload_path)
        print(args.get("hobby"))
        user = UserModel()
        user.username = username
        user.password = password
        print(os.path.join("icon", icon.filename))
        user.icon = os.path.join("icon", icon.filename)
        db.session.add(user)
        db.session.commit()
        return user


api.add_resource(UserResource, "/user", endpoint="all_user")
