"""
    复杂结构：Nested Field
"""
from flask import Blueprint
from flask_restful import Resource, fields, marshal, marshal_with
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

friend_format = {
    "username": fields.String,
    "nums": fields.Integer,
    "friends": fields.Nested(user_format)
}


class FriendResource(Resource):
    @marshal_with(friend_format)
    def get(self, uid):
        friends = UserModel.query.filter(UserModel.user_id == uid).all()
        user = UserModel.query.get(uid)
        print(friends)
        data = {
            "username": user.username,
            "nums": len(friends),
            # "friends": marshal(friends, user_format)
            "friends": friends
        }
        return data


api.add_resource(FriendResource, "/friend/<int:uid>")
