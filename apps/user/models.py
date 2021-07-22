from exts import db
from datetime import datetime


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
