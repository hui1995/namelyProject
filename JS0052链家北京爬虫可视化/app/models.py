from datetime import datetime
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
#用户表
class User(UserMixin,db.Model):
  id=db.Column(db.Integer,primary_key=True)
  username=db.Column(db.String(15),unique=True,nullable=False)
  password=db.Column(db.String(128))
  status=db.Column(db.Integer,default=0)

#爬虫记录表
class SpiderRecord(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  update_time=db.Column(db.DateTime,default=datetime.now())
  spider_name=db.Column(db.String(64))


#城区数据表
class dongcheng(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  title = db.Column(db.String(2048))#标题
  address = db.Column(db.String(2048))#地址
  floor = db.Column(db.String(2048))#楼层
  year = db.Column(db.String(2048))#年份
  area = db.Column(db.Float())#面积
  direation = db.Column(db.String(2048))#朝向
  type = db.Column(db.String(2048))#户型
  total_price = db.Column(db.Float())#总价
  single_price = db.Column(db.Float())#单价

class xicheng(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  title = db.Column(db.String(2048))
  address = db.Column(db.String(2048))
  floor = db.Column(db.String(2048))
  year = db.Column(db.String(2048))
  area = db.Column(db.Float())
  direation = db.Column(db.String(2048))
  type = db.Column(db.String(2048))
  total_price = db.Column(db.Float())
  single_price = db.Column(db.Float())

class haidian(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  title = db.Column(db.String(2048))
  address = db.Column(db.String(2048))
  floor = db.Column(db.String(2048))
  year = db.Column(db.String(2048))
  area = db.Column(db.Float())
  direation = db.Column(db.String(2048))
  type = db.Column(db.String(2048))
  total_price = db.Column(db.Float())
  single_price = db.Column(db.Float())

class chaoyang(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  title = db.Column(db.String(2048))
  address = db.Column(db.String(2048))
  floor = db.Column(db.String(2048))
  year = db.Column(db.String(2048))
  area = db.Column(db.Float())
  direation = db.Column(db.String(2048))
  type = db.Column(db.String(2048))
  total_price = db.Column(db.Float())
  single_price = db.Column(db.Float())

class fengtai(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  title = db.Column(db.String(2048))
  address = db.Column(db.String(2048))
  floor = db.Column(db.String(2048))
  year = db.Column(db.String(2048))
  area = db.Column(db.Float())
  direation = db.Column(db.String(2048))
  type = db.Column(db.String(2048))
  total_price = db.Column(db.Float())
  single_price = db.Column(db.Float())

class shijingshan(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  title = db.Column(db.String(2048))
  address = db.Column(db.String(2048))
  floor = db.Column(db.String(2048))
  year = db.Column(db.String(2048))
  area = db.Column(db.Float())
  direation = db.Column(db.String(2048))
  type = db.Column(db.String(2048))
  total_price = db.Column(db.Float())
  single_price = db.Column(db.Float())

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

