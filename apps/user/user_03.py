"""
    Field.Url的使用
"""
import os
from flask import Blueprint
from flask_restful import Resource, marshal_with, fields, reqparse, inputs, marshal
from werkzeug.datastructures import FileStorage
from settings import Config
from apps.user.models import UserModel
from exts import api, db

user_bp = Blueprint("user", __name__, url_prefix="/api")

# 定义展示的格式
user_format = {
    "id": fields.Integer,
    "username": fields.String(),
    "password": fields.String,
    "is_delete": fields.Boolean,
    "ctime": fields.DateTime(),
}
user_format_view = {
    "id": fields.Integer,
    "username": fields.String(),
    "uri": fields.Url("one_user", absolute=True)
}
# 参数解析
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument("username", type=str, location=["form"])
parser.add_argument("password", type=int, help="6-12位数字", required=True, location=["form"])


class UserSimpleResource(Resource):
    @marshal_with(user_format)
    def get(self, id):
        user = UserModel.query.get(id)
        return user


class UserResource(Resource):
    @marshal_with(user_format_view)
    def get(self):
        user_list = UserModel.query.all()
        return user_list


api.add_resource(UserSimpleResource, "/user/<int:id>", endpoint="one_user")
api.add_resource(UserResource, "/user", endpoint="all_user")
