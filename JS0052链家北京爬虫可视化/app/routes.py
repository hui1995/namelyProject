from flask import render_template, url_for, request, redirect, flash
from app import app, db
from app.models import User, dongcheng, xicheng, fengtai, shijingshan, haidian, chaoyang, SpiderRecord
from app.forms import LoginForm, CreateAccountForm
from flask_login import login_user, logout_user, login_required, current_user
from spider import dongchengSpider
from spider import xichengSpider
from spider import chaoyangSpider
from spider import fengtaiSpider
from spider import haidianSpider
from spider import shijingshanSpider
from datetime import datetime
from sqlalchemy.sql import func

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
            return redirect("/index/")
        #如果没有认证成功
        if not current_user.is_authenticated:
            #返回道登陆页面，病提示
            return render_template(
                'login/login.html',
                login_form=login_form, msg="用户名或者密码不正确"
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
        #判断两次密码输入是否一致
        if password != password2:
            return render_template(
                'login/signup.html',
                signup_form=signup_form, msg="两次密码不一致"
            )
        #查询用户是否存在，
        user = User.query.filter_by(username=username).first()
        #如果存在则提示错误
        if user is not None:
            return render_template(
                'login/signup.html',
                signup_form=signup_form, msg="用户名已存在"
            )
        #注册用户，提交
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template(
        'login/signup.html',
        signup_form=signup_form
    )


@app.route("/index/")
@app.route("/")
@login_required
def index():
    #查询爬取记录，
    spiderRecord = SpiderRecord.query.filter(SpiderRecord.spider_name == "all").first()
    if spiderRecord is not None:
        update_last = spiderRecord.update_time
    else:
        #如果不存在，则设置为null
        update_last = None
    return render_template('index.html', update_last=update_last)


@app.route("/room/num/")
@login_required
def roomNum():
    #统计六个地区的房型数据，
    #执行6次sql查询六张表，通过求和语句
    dongchegncount = dongcheng.query.count()
    xichengcount = xicheng.query.count()
    shijingshancount = shijingshan.query.count()
    chaoyangcount = chaoyang.query.count()
    fengtaicount = fengtai.query.count()
    haidiancount = haidian.query.count()
    return render_template('roomnum.html', dongchegncount=dongchegncount, xichengcount=xichengcount,
                           shijingshancount=shijingshancount, fengtaicount=fengtaicount, haidiancount=haidiancount,
                           chaoyangcount=chaoyangcount)

@app.route("/avg/total/")
@login_required
def avgtotalprice():
    #获取总价的平均值，通过sql语句的求平均数语句
    dongchegnavg = dongcheng.query.with_entities(func.avg(dongcheng.total_price)).scalar()
    xichengavg  = xicheng.query.with_entities(func.avg(xicheng.total_price)).scalar()
    shijingshanavg  = shijingshan.query.with_entities(func.avg(shijingshan.total_price)).scalar()
    chaoyangavg  = chaoyang.query.with_entities(func.avg(chaoyang.total_price)).scalar()
    fengtaiavg  = fengtai.query.with_entities(func.avg(fengtai.total_price)).scalar()
    haidianavg = haidian.query.with_entities(func.avg(haidian.total_price)).scalar()
    #获取单价的平均值
    singledongchegnavg = dongcheng.query.with_entities(func.avg(dongcheng.single_price)).scalar()
    singlexichengavg  = xicheng.query.with_entities(func.avg(xicheng.single_price)).scalar()
    singleshijingshanavg  = shijingshan.query.with_entities(func.avg(shijingshan.single_price)).scalar()
    singlechaoyangavg  = chaoyang.query.with_entities(func.avg(chaoyang.single_price)).scalar()
    singlefengtaiavg  = fengtai.query.with_entities(func.avg(fengtai.single_price)).scalar()
    singlehaidianavg = haidian.query.with_entities(func.avg(haidian.single_price)).scalar()
    #如果数据库没有数据，则返回为0，为了页面正常显示，所以都做一下判断，为NOne则设置为0
    if singledongchegnavg is None:
        singledongchegnavg = 0
    if singlexichengavg is None:
        singlexichengavg = 0
    if singleshijingshanavg is None:
        singleshijingshanavg = 0

    if singlechaoyangavg is None:
        singlechaoyangavg = 0
    if singlefengtaiavg is None:
        singlefengtaiavg = 0
    if singlehaidianavg is None:
        singlehaidianavg = 0
    if dongchegnavg is None:
        dongchegnavg=0
    if xichengavg is None:
        xichengavg=0
    if shijingshanavg is None:
        shijingshanavg=0

    if chaoyangavg is None:
        chaoyangavg=0
    if haidianavg is None:
        haidianavg=0
    if fengtaiavg is None:
        fengtaiavg=0

    return render_template('avgprice.html', dongchegnavg=dongchegnavg, xichengavg=xichengavg,
                           shijingshanavg=shijingshanavg, chaoyangavg=chaoyangavg, fengtaiavg=fengtaiavg,
                           haidianavg=haidianavg,
                           singledongchegnavg=singledongchegnavg,
                           singlexichengavg=singlexichengavg,
                           singleshijingshanavg=singleshijingshanavg,
                           singlechaoyangavg=singlechaoyangavg,
                           singlefengtaiavg=singlefengtaiavg,
                           singlehaidianavg=singlehaidianavg
                           )

@app.route("/area/count/")
@login_required
def areaCount():
    #利用原生sql，分组统计每一个阶段内的大小数量，因为前端无法支持数字取值，所以每一个阶段定义成了一个字母
    #a:0-50
    #b:50-100
    #c:100-150
    #以此类推
    sql="""select elt(interval(area,0,50,100,150,200,250,300),"a","b","c","d","e","f","g") as region ,count(*) from {} group by region"""
    sqld=sql.format("dongcheng")
    #查询东城区，将字段存入dict中，其中东城区一个dict，
    # 一个全部的dict，存放六个区域的所有内容
    allDict1={}
    dongchengDict1={}
    ret=db.session.execute(sqld)
    for i in ret:
        dongchengDict1[i[0]]=i[1]
        allDict1[i[0]]=i[1]

    sqld=sql.format("xicheng")
    #西城区数据，跟东城区一样操作
    xichengDict1={}
    ret=db.session.execute(sqld)
    for i in ret:
        xichengDict1[i[0]]=i[1]
        allDict1[i[0]]+=i[1]
    #朝阳区
    sqld=sql.format("chaoyang")

    chaoyangDict1={}
    ret=db.session.execute(sqld)
    for i in ret:
        chaoyangDict1[i[0]]=i[1]
        allDict1[i[0]]+=i[1]
    #丰台
    sqld=sql.format("fengtai")

    fengtaiDict1={}
    ret=db.session.execute(sqld)
    for i in ret:
        fengtaiDict1[i[0]]=i[1]
        allDict1[i[0]]+=i[1]
    #石景山
    sqld=sql.format("shijingshan")

    shijingshanDict1={}
    ret=db.session.execute(sqld)
    for i in ret:
        shijingshanDict1[i[0]]=i[1]
        allDict1[i[0]]+=i[1]
    sqld=sql.format("haidian")
    #海淀
    haidianDict1={}
    ret=db.session.execute(sqld)
    for i in ret:
        haidianDict1[i[0]]=i[1]
        allDict1[i[0]]+=i[1]

    return render_template('area.html', allDict1=allDict1, dongchengDict=dongchengDict1)

#散点图
@app.route("/shan/dian/")
@login_required
def shandian():
    #查询所有的数据，根据总价进行排序
    dongchegninfo = dongcheng.query.order_by(dongcheng.total_price).all()
    xichenginfo = xicheng.query.order_by(xicheng.total_price).all()
    shijingshaninfo = shijingshan.query.order_by(shijingshan.total_price).all()
    chaoyanginfo = chaoyang.query.order_by(chaoyang.total_price).all()
    fengtaiinfo = fengtai.query.order_by(fengtai.total_price).all()
    haidianinfo = haidian.query.order_by(haidian.total_price).all()
    #初始化一个字符串，这个字符串主要是为了在前端渲染散点图数据，其结构是一个二维数组
    dongchegnData=""
    xichengData=""
    shijiangshanData=""
    chaoyangData=""
    fengtaiData=""
    haidianData=""
    allinfo=""
    #东城区数据渲染
    for i in dongchegninfo:
        #定义一个content
        #一个完整的content的格式为['area','total_price']

        content=""
        content+='['
        content+=str(i.area)
        content+=','
        content+=str(i.total_price)
        content+='],'
        #将content添加道dongchengdate和allinfo中
        dongchegnData+=content
        allinfo+=content
    #其他五个区惨遭东城区操作
    for i in xichenginfo:
        content=""
        content+='['
        content+=str(i.area)
        content+=','
        content+=str(i.total_price)
        content+='],'
        xichengData+=content
        allinfo+=content
    for i in chaoyanginfo:
        content=""
        content+='['
        content+=str(i.area)
        content+=','
        content+=str(i.total_price)
        content+='],'
        chaoyangData+=content
        allinfo+=content
    for i in shijingshaninfo:
        content=""
        content+='['
        content+=str(i.area)
        content+=','
        content+=str(i.total_price)
        content+='],'
        shijiangshanData+=content
        allinfo+=content
    for i in fengtaiinfo:
        content=""
        content+='['
        content+=str(i.area)
        content+=','
        content+=str(i.total_price)
        content+='],'
        fengtaiData+=content
        allinfo+=content
    for i in haidianinfo:
        content=""
        content+='['
        content+=str(i.area)
        content+=','
        content+=str(i.total_price)
        content+='],'
        haidianData+=content
        allinfo+=content
    return render_template('shandian.html', allinfo=allinfo, dongchegnData=dongchegnData)

#词云
@app.route("/cloud/")
@login_required
def cloud():
    #获取展示的数量
    size=request.args.get("size")
    #查询，根据户型分组
    sql="select type, count(1) from {} group by type"
    sqld=sql.format("dongcheng")
    #如果传入参数不为数字或者不传入，设置为20
    try:
        size=int(size)
    except:
        size=20
    #对结果进行遍历，存入dict，每一个城区一个dict，整个北京一个dict，key为户型，value为数量
    allDict1={}
    dongchengDict1={}
    ret=db.session.execute(sqld)
    #将结果存入道dict中去
    for i in ret:
        dongchengDict1[i[0]]=i[1]

        allDict1[i[0]]=i[1]
    sqld = sql.format("xicheng")

    xichengDict1 = {}
    ret = db.session.execute(sqld)
    for i in ret:
        #城区dict直接存入
        xichengDict1[i[0]] = i[1]
        #如果为真个北京的dict，判断该户型是否在该字段中，如果有累加，没有则新加一个
        if i[0] in allDict1.keys():
            allDict1[i[0]]+= i[1]
        else:
            allDict1[i[0]]=i[1]

    sqld = sql.format("chaoyang")

    chaoyangDict1 = {}
    ret = db.session.execute(sqld)
    for i in ret:
        chaoyangDict1[i[0]] = i[1]
        if i[0] in allDict1.keys():
            allDict1[i[0]] += i[1]
        else:
            allDict1[i[0]] = i[1]

    sqld = sql.format("fengtai")

    fengtaiDict1 = {}
    ret = db.session.execute(sqld)
    for i in ret:
        fengtaiDict1[i[0]] = i[1]
        if i[0] in allDict1.keys():
            allDict1[i[0]] += i[1]
        else:
            allDict1[i[0]] = i[1]

    sqld = sql.format("shijingshan")

    shijingshanDict1 = {}
    ret = db.session.execute(sqld)
    for i in ret:
        shijingshanDict1[i[0]] = i[1]
        if i[0] in allDict1.keys():
            allDict1[i[0]] += i[1]
        else:
            allDict1[i[0]] = i[1]
    sqld = sql.format("haidian")

    haidianDict1 = {}
    ret = db.session.execute(sqld)
    for i in ret:
        haidianDict1[i[0]] = i[1]
        if i[0] in allDict1.keys():
            allDict1[i[0]] += i[1]
        else:
            allDict1[i[0]] = i[1]
    #根据value排序，整个是为了截取排名靠前的户型
    allDict1=sorted(allDict1.items(), key = lambda kv:(kv[1], kv[0]),reverse=True)
    dongchengDict1=sorted(dongchengDict1.items(), key = lambda kv:(kv[1], kv[0]),reverse=True)
    #进行截取,因为防止size大于列表长度，所以先判断一下大小
    if len(allDict1)>int(size):
        allDict1=allDict1[0:size]
    if len(dongchengDict1)>size:
        dongchengDict1=dongchengDict1[0:size]
    return render_template('cloud.html',allDict1=allDict1,dongchengDict1=dongchengDict1,size=size)


#爬虫启动
@app.route("/start/spider/")
@login_required
def startSpider():
    #启动六个爬虫
    dongchengSpider.spider()
    xichengSpider.spider()
    haidianSpider.spider()
    shijingshanSpider.spider()
    fengtaiSpider.spider()
    chaoyangSpider.spider()
    #将爬虫记录添加道数据库中去
    spiderRecord=SpiderRecord.query.filter(SpiderRecord.spider_name=="all").first()
    if spiderRecord is None:
        spiderRecord = SpiderRecord(spider_name="all", update_time=datetime.now())
    else:
        spiderRecord.update_time=datetime.now()
    db.session.add(spiderRecord)
    db.session.commit()
    return redirect("/index")


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


@app.route("/user/password/", methods=['GET', "POST"])
@login_required
def userPassword():
    #根据id查询用户
    id = request.args.get('id')
    user = User.query.get(id)

    if request.method == "GET":
        return render_template("password.html", user=user)
    #获取写入的密码
    password = request.form.get('password')
    #更新密码，保存
    user.password = password
    db.session.add(user)
    db.session.commit()
    return redirect("/user/list/")


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login/")
