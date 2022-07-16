import pymysql
import flask
import traceback
import gl
from flask import Flask, request, render_template
from bbs import bbs
from search import search
from ad import ad

app = Flask(__name__)  # app是Flask的实例，它接收包或者模块的名字作为参数
app.debug = True  # Debug模式 页面实时显示
app.register_blueprint(search)
app.register_blueprint(bbs)
app.register_blueprint(ad)


#使用@app.route修饰器
#传入URL规则作为参数，将函数绑定到URL，这个过程便将一个函数注册为路由，这个函数则被称为视图函数
@app.route("/information", methods=["GET", "POST"])
def information():
    if gl.flag == 0:
        # 用户没有登陆
        print('用户还没有登陆!即将重定向!')
        return flask.redirect('/login')
    return render_template("information.html");


@app.route("/nav", methods=["GET", "POST"])
def nav():
    return render_template("nav.html");


@app.route("/", methods=["GET", "POST"])
def unnav():
    gl.flag = 0
    return render_template("unnav.html");


@app.route("/attention", methods=["GET", "POST"])
def attention():
    return render_template("attention.html");


# ----------------------------注册--------------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html");


@app.route("/rg", methods=["GET", "POST"])
def rg():
    username = request.args.get('username')
    email = request.args.get('email')
    pwd = request.args.get('password')
    name = request.args.get('name')
    exp = request.args.get('exp')
    number = request.args.get('number')
    sex = request.args.get('sex')
    # 把用户名和密码注册到数据库中
    # 连接数据库,此前在数据库中创建数据库mysql
    try:
        db = pymysql.connect(host="127.0.0.1", port=3306, user='root', password="720228", charset='utf8', db='admins')
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # SQL 插入语句

        sql = "INSERT INTO register (user,password,email,name,sex,number,exp)" \
              "VALUES('%s','%s','%s','%s','%s','%s','%s')" % (
                  str(username), str(pwd), str(email), str(name), str(sex), str(number), str(exp))
        # 执行sql语句

        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        # 注册成功之后跳转到登录页面
        return render_template('login.html')
    except:
        # 抛出错误信息
        traceback.print_exc()
        # 如果发生错误则回滚
        db.rollback()
        return '注册失败'
    # 关闭数据库连接
    db.close()


# ----------------------------登录--------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html");


@app.route('/logindef')
def getLoginRequest():
    # 查询用户名及密码是否匹配及存在
    # 连接数据库,此前在数据库中创建数据库mysql
    db = pymysql.connect(host="127.0.0.1", port=3306, user='root', password="720228", charset='utf8', db='admins')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    user = flask.request.values.get("user", "")
    pwd = flask.request.values.get("password", "")
    # 与数据库中数据进行比较
    sql = "select * from register where user='" + \
          user + "' and password='" + pwd + "';"
    # 执行sql语句
    cursor.execute(sql)
    results = cursor.fetchall()
    print(len(results))
    if len(results) == 1:
        gl.flag = 1
        return flask.redirect('/nav')  # 返回需要跳转的页面
    else:
        return flask.redirect('/')
    # 提交到数据库执行
    db.commit()
    # 关闭数据库连接
    db.close()


if __name__ == '__main__':
    app.run()
