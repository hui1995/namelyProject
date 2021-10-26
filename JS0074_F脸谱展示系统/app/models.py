from datetime import datetime
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
#用户表
class User(UserMixin,db.Model):
  id=db.Column(db.Integer,primary_key=True)
  username=db.Column(db.String(15))
  password=db.Column(db.String(128))
  status=db.Column(db.Integer,default=0)
  real_name=db.Column(db.String(64))
  phone=db.Column(db.String(64),unique=True,nullable=False)


#分类表
class Category(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  name=db.Column(db.String(64))


#脸谱表
class face(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  face_url=db.Column(db.String(2048))
  category_id=db.Column(db.Integer)


class collectFace(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  face_id = db.Column(db.Integer)
  user_id = db.Column(db.Integer)


class FeedBackMessage(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  user_id = db.Column(db.Integer)
  content=db.Column(db.Text)
  face_url=db.Column(db.String(2048))

  creat_time=db.Column(db.DateTime)


@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

