import flask
import pymysql
import gl
from flask import Flask, render_template, request, Blueprint, url_for
import time

search = Blueprint('search', __name__)  # 蓝图


# 连接数据库并发起请求 获取请求结果
def model(sql):
    # 1.链接mysql数据库
    db = pymysql.connect(host="127.0.0.1", port=3306, user='root', password="720228", charset='utf8', db='admins')
    try:
        # 2.创建游标对象
        cursor = db.cursor()
        # 3.执行sql语句
        res = cursor.execute(sql)
        db.commit()  # 在执行sql语句时，注意进行提交
        # 4.提取结果
        data = cursor.fetchall()
        print(data)
        if data:
            return data
        else:
            return res
    except:
        db.rollback()  # 当代码出现错误时，进行回滚
    finally:
        # 6.关闭数据库连接
        db.close()


@search.route("/center", methods=["GET", "POST"])
def center():
    print(gl.flag)
    if gl.flag == 0:
        # 用户没有登陆
        print('用户还没有登陆!即将重定向!')
        return flask.redirect('/login')
    return render_template("center.html");


'''@search.route("/search_show")
def search_show():
    row = model("select * from cats")
    return render_template('search_show.html', data=row)'''


@search.route('/centerdef')
def centerdef():
    name = request.values.get("nickname", "")
    # 与数据库中数据进行比较
    sql = "select * from cats where nickname='" + name + "';"
    sql2 = "select cat_photo from cats where nickname='" + name + "';"
    results = model(sql)
    img_path = model(sql2)
    str = ''
    for i in img_path:
        str = str + i[0];
    #row = model("select * from cats")
    if len(results) == 1:
        return render_template('search_show.html', data=results, img=str)
    else:
        return '<script>alert("查无此猫");location.href="/center"</script>'
    # 提交到数据库执行
    db.commit()
    # 关闭数据库连接
    db.close()


# 定义视图 显示留言添加的页面
@search.route('/request')
def add_request():
    return render_template('request.html')


# 定义视图函数 接收表单数据，完成数据的入库
@search.route('/insert_search', methods=["GET", "POST"])
def insert_search():
    # 1.接收表单数据
    data = request.form.to_dict()
    print(data)
    # 2.把数据添加到数据库
    sql = f'insert into request values(null,"{data["cat_name"]}","{data["realname"]}","{data["number"]}","{data["email"]}","{data["address"]}",null)'
    print(sql)
    res = model(sql)

    if res:
        return '<script>alert("申请成功！");location.href="/center"</script>'
    else:
        return '<script>alert("申请失败！");location.href="/request"</script>'


if __name__ == '__main__':
    search.run(debug=True, host='127.0.0.1')
