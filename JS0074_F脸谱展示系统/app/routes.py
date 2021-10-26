from flask import render_template, url_for, request, redirect, flash
from app import app, db
from app.models import User,Category,face,FeedBackMessage
from app.models import collectFace as CollectFace
from app.forms import LoginForm, CreateAccountForm
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from sqlalchemy.sql import func
from app.predict import predict


@app.route("/")
@login_required
def home():
    if current_user.status==1:
        return redirect("/user/list/")
    else:
        return redirect("/cate")
#登陆接口
@app.route("/login", methods=['GET', 'POST'])
@app.route("/login/", methods=['GET', 'POST'])
def login():
    #获取form表单
    login_form = LoginForm(request.form)
    #如果为post请求
    if request.method == "POST":
        #获取用户名和密码
        username = request.form['username']
        password = request.form['password']
        #根据用户名查询
        user = User.query.filter_by(username=username).first()
        #如果用户存在并且密码和传入密码一致，则登陆
        if user and password == user.password:
            login_user(user)#利用flask_login登陆
            if user.status==0:
                return redirect("/index/")
            else:
                return redirect("/user/list/")
        #如果没有认证成功
        if not current_user.is_authenticated:
            #返回道登陆页面，病提示
            return render_template(
                'login/login.html',
                login_form=login_form, msg="手机号或者密码不正确"
            )

    return render_template('login/login.html', login_form=login_form)


@app.route("/signup/", methods=['GET', 'POST'])
def signup():
    #定义注册form表单
    signup_form = CreateAccountForm(request.form)
    #如果为post请求，则获取参数
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        phone = request.form['phone']
        real_name = request.form['real_name']
        #判断两次密码输入是否一致
        if password != password2:
            return render_template(
                'login/signup.html',
                signup_form=signup_form, msg="两次密码不一致"
            )
        #查询用户是否存在，
        user = User.query.filter_by(phone=phone).first()
        #如果存在则提示错误
        if user is not None:
            return render_template(
                'login/signup.html',
                signup_form=signup_form, msg="该手机号已经存在"
            )
        #注册用户，提交
        user = User(username=username, password=password,phone=phone,real_name=real_name)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template(
        'login/signup.html',
        signup_form=signup_form
    )


@app.route("/cate/")
@login_required
def index():
    cate=request.args.get("cate")
    categorylist=Category.query.all()
    keyword=request.args.get("keyword")
    if keyword is not None and keyword!="":
        categoryke=Category.query.filter(Category.name.like('%{keyword}%'.format(keyword=keyword))).all()
        catelist=[]
        for i in categoryke:
            catelist.append(i.id)
        facelist=face.query.filter(face.id.in_(catelist))
        catenow=False



    elif cate is None or cate =="":
        facelist=face.query.all()
        catenow=False
    else:
        facelist=face.query.filter(face.category_id==cate)
        catenow = Category.query.get(cate)
    result=[]

    for i in facelist:
        dict1={}
        dict1["face_url"]=i.face_url
        dict1["id"]=i.id

        collect=CollectFace.query.filter(CollectFace.user_id==current_user.id).filter(CollectFace.face_id==i.id).first()
        if collect is not None:
            dict1["collect"]=True
        else:
            dict1["collect"]=False
        result.append(dict1)

    return render_template("faceshow.html",facelist=result,categorylist=categorylist,catenow=catenow,keyword=keyword)
@app.route("/collect/face/")
@login_required
def collectFace():
    id=request.args.get("id")
    cate=request.args.get("cate")
    back=request.args.get("back")

    collect = CollectFace.query.filter(CollectFace.user_id == current_user.id).filter(
        CollectFace.face_id ==id).first()
    if collect is None:
        c=CollectFace(user_id=current_user.id,face_id=id)
        db.session.add(c)
        db.session.commit()
    else:
        db.session.delete(collect)
        db.session.commit()
    if back is not None:
        return redirect("/collect/my/")

    if cate is not None:
        return redirect("/cate/?cate="+cate)
    else:
        return redirect("/cate/")


@app.route("/face/del/")
@login_required
def faceDel():
    id = request.args.get('id')
    face2= face.query.get(id)
    db.session.delete(face2)
    db.session.commit()
    return redirect("/face/list/")
@app.route("/face/list/")
@login_required
def faceList():
    facelist = face.query.all()
    result=[]
    for i in facelist:
        dict1={}
        dict1['id']=i.id
        dict1["face_url"]=i.face_url
        category=Category.query.get(i.category_id)
        dict1["category"]=category.name
        result.append(dict1)
    return render_template("facelist.html", result=result)

@app.route("/face/opt/",methods=["GET","POST"])
@login_required
def faceOpt():
    categorylist=Category.query.all()
    if request.method=="GET":
        return render_template("faceopt.html", categorylist=categorylist)
    file=request.files.get("file")
    category_id=request.form.get("cate")
    path =  "./app/static/images/"
    file_path = path + file.filename
    file.save(file_path)

    face1=face(face_url="/static/images/"+file.filename,category_id=category_id)

    db.session.add(face1)
    db.session.commit()
    return redirect("/face/list/")


@app.route("/feedback/list/")
@login_required
def feedbackList():
    facebacklist = FeedBackMessage.query.all()
    result=[]
    for i in facebacklist:
        dict1={}
        dict1['id']=i.id
        dict1['user']=User.query.get(i.user_id)

        dict1["face_url"]=i.face_url
        dict1["create_time"]=i.creat_time
        dict1["content"]=i.content
        result.append(dict1)
    return render_template("facebackMessagelist.html", result=result)


@app.route("/feedback/show/")
@login_required
def feedbackDetail():
    id=request.args.get("id")
    feedbackmessage=FeedBackMessage.query.get(id)
    user=User.query.get(feedbackmessage.user_id)
    return render_template("feedbackshow.html", feedbackmessage=feedbackmessage,user=user)
@app.route("/feedback/del/")
@login_required
def feedbackDel():
    id = request.args.get('id')
    feed2= FeedBackMessage.query.get(id)
    db.session.delete(feed2)
    db.session.commit()
    return redirect("/feedback/list/")

@app.route("/cate/list/")
@login_required
def CategoryList():
    categorylist = Category.query.all()
    return render_template("categorylist.html", categorylist=categorylist)

@app.route("/cate/opt/",methods=["GET","POST"])
@login_required
def CategoryOpt():
    id=request.args.get("id")
    category = Category.query.get(id)
    if request.method=="GET":
        return render_template("categroyadd.html", category=category)
    name=request.form.get("name")
    if id is not None and id!="":
        category.name=name
        db.session.commit()
    else:
        category=Category(name=name)
        db.session.add(category)
        db.session.commit()
    return redirect("/cate/list/")

@app.route("/cate/del/")
@login_required
def cateDel():
    id = request.args.get('id')
    cate = Category.query.get(id)
    db.session.delete(cate)
    db.session.commit()
    return redirect("/cate/list/")


@app.route("/user/list/")
@login_required
def userList():
    #查询普通用户
    user = User.query.filter(User.status == 0)
    return render_template("userlist.html", user=user)




@app.route("/user/del/")
@login_required
def userDel():
    #前端获取id，根据id查询用户，然后进行删除
    id = request.args.get('id')
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/user/list/")


@app.route("/password/", methods=['GET', "POST"])
@login_required
def userPassword():
    #根据id查询用户
    user = User.query.get(current_user.id)

    if request.method == "GET":
        return render_template("login/password.html", user=user)
    #获取写入的密码
    password = request.form.get('password')
    #更新密码，保存
    user.password = password
    db.session.add(user)
    db.session.commit()
    return redirect("/login")



@app.route("/person", methods=['GET', "POST"])
@login_required
def person():
    #根据id查询用户
    user = User.query.get(current_user.id)

    if request.method=="GET":
        return render_template('login/person.html',user=user)
    else:
        real_name=request.form.get("real_name")
        username=request.form.get("username")
        phone=request.form.get("phone")
        userha=User.query.filter(User.phone==phone).first()
        if userha is None or phone==current_user.phone:
            user.phone=phone
            user.username=username
            user.real_name=real_name
            db.session.add(user)
            db.session.commit()
            login_user(user)  # 利用flask_login登陆

        return redirect("/person")
@app.route("/collect/my/")
def collectmy():
    collectlist=CollectFace.query.filter(CollectFace.user_id==current_user.id)
    categorylist=Category.query.all()

    result=[]
    for i in collectlist:
        face1=face.query.filter(face.id==i.face_id).first()
        if face1 is not None:
            result.append(face1)
    return render_template('collect.html',result=result,categorylist=categorylist)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login/")
import uuid
@app.route("/face/now/",methods=['GET',"POST"])
def facenow():
    categorylist=Category.query.all()

    if request.method=="GET":
        return render_template('facenow.html',categorylist=categorylist)
    file=request.files.get("file")
    path =  "./app/static/images/"
    filename=str(uuid.uuid4())+".png"

    file_path = path +filename
    file.save(file_path)
    predict(file_path)
    cate=predict(file_path)
    data={"cate":cate,"face_url":"/static/images/"+filename}
    return render_template('facenow.html',categorylist=categorylist,data=data)
@app.route("/feedback",methods=["POST"])
def feedback():
    face_url=request.form.get("face_url")
    content=request.form.get("feedback")

    feedback=FeedBackMessage(face_url=face_url,content=content,user_id=current_user.id,creat_time=datetime.now())
    db.session.add(feedback)
    db.session.commit()
    return render_template('facenow2.html')
