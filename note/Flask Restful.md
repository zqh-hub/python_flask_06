##### Flask Restful

###### 快速入门

```python
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


# user/view.py
from flask import Blueprint
from flask_restful import Resource, marshal_with, fields
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
    @marshal_with(user_format)   # 绑定模版,marshal_with()的作用：转成序列化对象
    def get(self):
        user_list = UserModel.query.all()
        return user_list

    def post(self):
        return {"msg": "------------->post"}


api.add_resource(UserResource, "/user")   # 绑定 类视图与uri
```

###### 传递参数：解析路由方式

```python
from flask_restful import Resource, marshal_with, fields, reqparse
from exts import api, db
# 定义展示的格式
user_format = {
    "id": fields.Integer,
    "username": fields.String,
    "password": fields.String,
    "ctime": fields.DateTime,
}

class UserSimpleResource(Resource):
    @marshal_with(user_format)
    def get(self, uid):   # 传参
        user = UserModel.query.get(uid)
        return user

api.add_resource(UserSimpleResource, "/user/<int:uid>", endpoint="one_user")
```

###### 参数传递：键值对方式

```python
# 定义展示的格式
user_format = {
    "id": fields.Integer,
    "username": fields.String,
    "password": fields.String,
    "ctime": fields.DateTime,
}

# 解析请求
parser = reqparse.RequestParser()
# type:指定类型；required:是否必填;help:如果没填写就提示。。;location=["form"]:必须是表单提交
parser.add_argument("username", type=str, required=True, help="用户名必填",location=["form"])

# type=inputs.regex(r'^\d{6,12}$'):使用正则进行匹配是否合法
parser.add_argument("password", type=inputs.regex(r'^\d{6,12}$'), help="6-12位数字", location=["form"])

# action="append":复选框
parser.add_argument("hobby", action="append")

# 定义类视图
class UserResource(Resource):
    @marshal_with(user_format)
    def post(self):
        args = parser.parse_args()   # 解析所有参数
        username = args.get("username") # 获取参数
        password = args.get("password")
        print(args.get("hobby"))   # 复选框 ['game', 'book']
        user = UserModel()
        user.username = username
        user.password = password
        db.session.add(user)
        db.session.commit()
        return user

api.add_resource(UserResource, "/user", endpoint="all_user")
```

###### 参数来源

```python
# Look only in the POST body
parser.add_argument('name', type=int, location='form')

# Look only in the querystring
parser.add_argument('PageSize', type=int, location='args')

# From the request headers
parser.add_argument('User-Agent', location='headers')

# From http cookies
parser.add_argument('session_id', location='cookies')

# From file uploads
parser.add_argument('picture', type=werkzeug.datastructures.FileStorage, location='files')
```

###### 上传文件

```python
from flask_restful import Resource, marshal_with, fields, reqparse, inputs
from werkzeug.datastructures import FileStorage
from settings import Config
from apps.user.models import UserModel

# 定义展示的格式
user_format = {
    "id": fields.Integer,
    "username": fields.String,
    "password": fields.String,
    "ctime": fields.DateTime,
}

# 参数解析
parser = reqparse.RequestParser()
# type:指明是文件，FileStorage类型；location=["files"]:来源是文件
parser.add_argument("icon", type=FileStorage, location=["files"])


# 定义类视图
class UserResource(Resource):
    @marshal_with(user_format)
    def post(self):
        args = parser.parse_args()
        icon = args.get("icon") # 获取到FileStorage类型
        # 存储的路径
        upload_path = os.path.join(Config.ICON_DIR, icon.filename)
        icon.save(upload_path)  # 存储
        user = UserModel()
        print(os.path.join("icon", icon.filename))
        user.icon = os.path.join("icon", icon.filename)  # 将文件相对于static的路径存储在数据库中
        db.session.add(user)
        db.session.commit()
        return user

api.add_resource(UserResource, "/user", endpoint="all_user")
```

###### 错误处理

```
parser = reqparse.RequestParser(bundle_errors=True)
# 这样设置后，会将所有的报错都显示出来
```

###### 约束输入的值

```
# 输入的参数只能是one或者two，否则报错：不存在的值
parser.add_argument("cho", type=str, choices=("one", "two"), help="不存在的值")
```

###### attribute与default

```python
# 定义展示的格式
user_format = {
    "id": fields.Integer,
    # attribute:设置的值是面向数据库的，与数据库保持一直；un是对外的，传参时候用
    # default:没有获取到参数时，使用默认值
    "un": fields.String(attribute="username", default="aoao"),
    "password": fields.String,
    "ctime": fields.DateTime(),
}

# 定义类视图
class UserResource(Resource):
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
```

![restful_001](/Users/eric/Documents/python/python_code/python_flask_06/note/img/restful_001.png)

###### 自定义fields

```python
1、继承fields.Raw
2、重写format方法
class DeleteShow(fields.Raw):   # 1、自定义
    def format(self, value):
    		# value 就是从数据库获取到到值，因为attribute已经绑定了is_delete字段，所以获取到了它的值
        print(value)
        return "删除" if value else "未删除"


# 定义展示的格式
user_format = {
    "id": fields.Integer,
    "un": fields.String(attribute="username", default="aoao"),
    "password": fields.String,
    "is_delete": fields.Boolean,
    "is_delete_show": DeleteShow(attribute="is_delete"),  # 2、绑定数据库的is_delete字段
    "ctime": fields.DateTime(),
}

# 定义类视图
class UserResource(Resource):
    @marshal_with(user_format)
    def get(self):
        user_list = UserModel.query.all()
        return user_list

api.add_resource(UserResource, "/user", endpoint="all_user")
```

###### Field.Url的使用

```python
# 定义展示的格式
user_format = {  # 1、每一个的详情要展示的字段
    "id": fields.Integer,
    "username": fields.String(),
    "password": fields.String,
    "is_delete": fields.Boolean,
    "ctime": fields.DateTime(),
}
user_format_view = {   # 2、每一个的简介要展示的字段
    "id": fields.Integer,  # 注意这里，id要和详情（user_format）里的一致
    "username": fields.String(),
    "uri": fields.Url("one_user", absolute=True)  # 注意这里，one_user
}

class UserSimpleResource(Resource):  # 获取详情时，使用这个类，并绑定/user/id路由
    @marshal_with(user_format)
    def get(self, id):
        user = UserModel.query.get(id)
        return user

class UserResource(Resource):
    @marshal_with(user_format_view)    # 获取所有时，使用这个类
    def get(self):
        user_list = UserModel.query.all()
        return user_list

api.add_resource(UserSimpleResource, "/user/<int:id>", endpoint="one_user")
api.add_resource(UserResource, "/user", endpoint="all_user")
```

![restful_002](/Users/eric/Documents/python/python_code/python_flask_06/note/img/restful_002.png)

###### 复杂结构：marshal

```python
# model.py
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255))
    icon = db.Column(db.String(255))
    is_delete = db.Column(db.Boolean)
    ctime = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user_model.id"))
    user = db.relationship("UserModel", back_populates="friend", remote_side=[id])
    friend = db.relationship("UserModel", back_populates="user", cascade='all')
    
    
# app.py
from flask_restful import Resource, marshal

# 定义展示的格式
user_format = {
    "id": fields.Integer,
    "username": fields.String(),
    "password": fields.String,
    "is_delete": fields.Boolean,
    "ctime": fields.DateTime(),
}

class FriendResource(Resource):
    def get(self, uid):  # 通过 id 获取到所有的朋友
        friends = UserModel.query.filter(UserModel.user_id == uid).all()
        user = UserModel.query.get(uid)
        print(friends)
        data = {
            "username": user.username,
            "nums": len(friends),
            "friends": marshal(friends, user_format) # marshal(要格式化的数据, 绑定格式)
        }
        return data
api.add_resource(FriendResource, "/friend/<int:uid>")
```

###### 复杂结构：Nested Field

```python
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
    "friends": fields.Nested(user_format)   # 注意，这里将friends的格式指向了“user_format”
}

class FriendResource(Resource):
    @marshal_with(friend_format)  # 这里绑定“friend_format”
    def get(self, uid):
        friends = UserModel.query.filter(UserModel.user_id == uid).all()
        user = UserModel.query.get(uid)
        print(friends)
        data = {       # 这里的data格式和键，要与“friend_format”一样
            "username": user.username,
            "nums": len(friends),
            "friends": friends
        }
        return data

api.add_resource(FriendResource, "/friend/<int:uid>")
```

