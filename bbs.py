import pymysql
from flask import Flask,render_template,request,Blueprint
import time
import gl
import flask

bbs=Blueprint('bbs',__name__)#蓝图

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
        if data:
            return data
        else:
            return res
    except:
        db.rollback()  # 当代码出现错误时，进行回滚
    finally:
        # 6.关闭数据库连接
        db.close()


# 留言板列表 显示留言信息
@bbs.route("/bbs_show")
def hello():
    # 1.获取所有的留言板数据
    # 2.把数据分配到模板中(html页面)
    if gl.flag==0:
        # 用户没有登陆
        print('用户还没有登陆!即将重定向!')
        return flask.redirect('/login')
    row = model("select * from lyb")
    return render_template('bbs_show.html',data=row)


# 定义视图 显示留言添加的页面
@bbs.route('/bbs_add')
def add():
    return render_template('bbs_add.html')


# 定义视图函数 接收表单数据，完成数据的入库
@bbs.route('/insert', methods=['POST'])
def insert():
    # 1.接收表单数据
    data = request.form.to_dict()
    data['date'] = time.strftime('%Y-%m-%d %H:%M:%S')
    print(data)
    # 2.把数据添加到数据库
    sql = f'insert into lyb values(null,"{data["nikename"]}","{data["info"]}","{data["date"]}")'
    res = model(sql)
    print(res)
    # 3.成功后页面跳转到 留言列表界面
    if res:
        return '<script>alert("留言成功！");location.href="/bbs_show"</script>'
    else:
        return '<script>alert("留言发布失败！");location.href="/bbs_add"</script>'


'''@bbs.route("/update")
def update():
    id = request.args.get('id')
    sql = f'select * from lyb where id={id}'
    res = model(sql)
    return render_template('update.html', data=res)'''


if __name__ == '__main__':
    bbs.run(debug=True, host='127.0.0.1')
