from flask import Blueprint
from flask_restful import Resource, marshal_with, fields, reqparse
from apps.user.models import UserModel
from exts import api
import json

user_bp = Blueprint("user", __name__, url_prefix="/api")

# 定义展示的格式
user_format = {
    "id": fields.Integer,
    "username": fields.String,
    "password": fields.String,
    "ctime": fields.DateTime,
}


# 定义类视图
class UserResource(Resource):
    @marshal_with(user_format)
    def get(self):
        user_list = UserModel.query.all()
        return user_list

    def post(self):
        return {"msg": "------------->post"}


class UserSimpleResource(Resource):
    @marshal_with(user_format)
    def get(self, uid):
        user = UserModel.query.get(uid)
        return user


api.add_resource(UserResource, "/user", endpoint="all_user")
api.add_resource(UserSimpleResource, "/user/<int:uid>", endpoint="one_user")
