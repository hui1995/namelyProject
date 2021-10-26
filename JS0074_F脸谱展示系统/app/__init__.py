from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bcb4c11b6b4392de4d292a9c0691e2297c0173f0285d2cc9'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:201212@121.199.29.111:3306/lianpu'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'login'

login_manager.init_app(app)
from app import routes

from app.models import User
db.create_all()


