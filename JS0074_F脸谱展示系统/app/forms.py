from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField

## login and registration


class LoginForm(FlaskForm):
    username = TextField('手机号', id='username_login')
    password = PasswordField('密码', id='pwd_login')


class CreateAccountForm(FlaskForm):
    username = TextField('用户名', id='username_create')
    phone = TextField('手机号', id='username_create')
    real_name = TextField('真实姓名', id='username_create')
    password = PasswordField('密码', id='pwd_create')
    password2 = PasswordField('确认密码', id='pwd_create')
