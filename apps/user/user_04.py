"""
    复杂结构：marshal
"""
from flask import Blueprint
from flask_restful import Resource, fields, marshal
from apps.user.models import UserModel
from exts import api

user_bp = Blueprint("user", __name__, url_prefix="/api")

# 定义展示的格式
user_format = {
    "id": fields.Integer,
    "username": fields.String(),
    "password": fields.String,
    "is_delete": fields.Boolean,
    "ctime": fields.DateTime(),
}


class FriendResource(Resource):
    def get(self, uid):
        friends = UserModel.query.filter(UserModel.user_id == uid).all()
        user = UserModel.query.get(uid)
        print(friends)
        data = {
            "username": user.username,
            "nums": len(friends),
            "friends": marshal(friends, user_format)
        }
        return data


api.add_resource(FriendResource, "/friend/<int:uid>")
