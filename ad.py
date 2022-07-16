import flask
from flask import url_for, Blueprint, render_template, request, redirect
import os  # 用于操作系统文件的依赖库
import re  # 引入正则表达式对用户输入进行限制
import pymysql  # 连接数据库

# 初始化
app = flask.Flask(__name__)
# 初始化数据库连接
# 使用pymysql.connect方法连接本地mysql数据库
db = pymysql.connect(host='127.0.0.1', port=3306, user='root',
                     password='720228', database='admins', charset='utf8')
ad = Blueprint('ad', __name__)  # 蓝图
# 操作数据库，获取db下的cursor对象
cursor = db.cursor()
# 存储登陆用户的名字用户其它网页的显示
users = []


@ad.route("/alogin", methods=["GET", "POST"])
def alogin():
    return render_template('ad_login.html')


@ad.route("/adlogin", methods=["GET", "POST"])
def adlogin():
    user = request.values.get("user", "")
    pwd = request.values.get("pwd", "")
    # 与数据库中数据进行比较
    sql = "select * from admin where admin_name='" + \
          user + "' and admin_password='" + pwd + "';"
    cursor.execute(sql)  # 游标接口
    db.commit()
    result = cursor.fetchone()
    print(sql)
    # 匹配得到结果即管理员数据库中存在此管理员
    if result:
        # 登陆成功
        # return render_template('ad_cats_info.html')
        return redirect(url_for('ad.cats_info'))
    else:
        return render_template('ad_login.html')
    db.commit()
    # 关闭数据库连接
    db.close()


@ad.route('/cats_info', methods=['GET', "POST"])
def cats_info():
    insert_result = ''
    # 获取显示管理员数据信息(GET方法的时候显示数据)
    if flask.request.method == 'GET':
        sql_list = "select * from cat"
        cursor.execute(sql_list)
        results = cursor.fetchall()
    if flask.request.method == 'POST':
        # 获取输入的学生信息
        cat_id = request.values.get("id", "")
        cat_name = request.values.get("name", "")
        cat_gender = request.values.get("gender", "")
        cat_conditions = request.values.get("conditions", "")
        cat_sterilization = request.values.get("sterilization", "")
        cat_characters = request.values.get("characters", "")
        cat_exp = request.values.get("exp", "")

        if cat_id is not None and cat_name is not None:  # 验证通过
            # 获取下拉框的数据
            select = request.form.get('selected_one')
            if select == '增加猫咪信息':
                try:
                    sql = "insert into cat(id, name, gender, conditions, sterilization, characters, exp)values(%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql, (
                        cat_id, cat_name, cat_gender, cat_conditions, cat_sterilization, cat_characters, cat_exp))
                    insert_result = "成功增加了一名小可爱"
                    print(insert_result)
                except Exception as err:
                    print(err)
                    insert_result = "增加小可爱操作失败"
                    print(insert_result)
                    pass
                db.commit()
            if select == '修改猫咪信息':
                try:
                    sql = "update cat set exp=%s where name=%s;"
                    cursor.execute(sql, (cat_exp, cat_name))
                    print(sql)
                    insert_result = "猫咪" + cat_name + "的情况修改成功!"
                except Exception as err:
                    print(err)
                    insert_result = "修改猫咪信息失败!"
                    pass
                db.commit()
            if select == '删除猫咪信息':
                try:
                    sql_delete = "delete from cat where name='" + cat_name + "';"
                    cursor.execute(sql_delete)
                    print(sql_delete)
                    insert_result = "成功删除猫咪" + cat_name
                except Exception as err:
                    print(err)
                    insert_result = "删除猫咪信息失败"
                    pass
                db.commit()
        else:  # 输入验证不通过
            insert_result = "输入的格式不符合要求!"
            # POST方法时显示数据
        sql_list = "select * from cat"
        cursor.execute(sql_list)
        results = cursor.fetchall()
        print()
    return render_template('ad_cats_info.html', insert_result=insert_result, results=results)


@ad.route('/user_info', methods=['GET', "POST"])
def user_info():
    insert_result = ''
    # 获取显示管理员数据信息(GET方法的时候显示数据)
    if flask.request.method == 'GET':
        sql_list = "select * from register"
        cursor.execute(sql_list)
        results = cursor.fetchall()
    if request.method == 'POST':

        user_id = request.values.get("username", "")
        user_password = request.values.get("password", "")
        user_email = request.values.get("email", "")
        user_name = request.values.get("name", "")
        user_exp = request.values.get("exp", "")
        user_number = request.values.get("number", "")
        user_sex = request.values.get("sex", "")
        if user_name is not None:
            # 查询
            sql = "select * from register where name='" + user_name + "';"
            result = cursor.execute(sql)
            insert_result = "查询成功！"
            print(insert_result)
            # sql_list = "select * from register where"
            if result:
                results = cursor.fetchall()
            if len(results) == 1:
                print(results)
                return render_template('ad_user_info.html', results=results, insert_result=insert_result)
            else:
                return '<script>alert("查无此人");location.href="/user_info"</script>'

    return render_template('ad_user_info.html', insert_result=insert_result, results=results)


@ad.route('/adminstator', methods=['GET', "POST"])
def adminstator():
    insert_result = ''
    # 获取显示管理员数据信息(GET方法的时候显示数据)
    if flask.request.method == 'GET':
        sql_list = "select * from admin"
        cursor.execute(sql_list)
        results = cursor.fetchall()

    if flask.request.method == 'POST':
        # 获取输入的管理员信息
        admin_name = flask.request.values.get("admin_name", "")
        admin_password = flask.request.values.get("admin_password", "")
        # print(admin_name, admin_password)
        admin_name_result = re.search(r"^[a-zA-Z]+$", admin_name)  # 限制用户名为全字母
        admin_password_result = re.search(
            r"^[a-zA-Z\d]+$", admin_password)  # 限制密码为 字母和数字的组合
        # 验证通过
        if admin_name_result != None and admin_password_result != None:  # 验证通过
            # 获取下拉框的数据
            select = flask.request.form.get('selected_one')
            if select == '增加管理员':
                try:
                    sql = "create table if not exists admins(id int primary key auto_increment,admin_name varchar(15),admin_password varchar(20));"
                    cursor.execute(sql)
                    sql_1 = "insert into admin(admin_name,admin_password)values(%s,%s)"
                    cursor.execute(sql_1, (admin_name, admin_password))
                    insert_result = "成功增加了一名管理员"
                    print(insert_result)
                except Exception as err:
                    print(err)
                    insert_result = "增加管理员操作失败"
                    print(insert_result)
                    pass
                db.commit()
            if select == '修改管理员密码':
                try:
                    sql = "update admin set admin_password=%swhere admin_name=%s;"
                    cursor.execute(sql, (admin_password, admin_name))
                    insert_result = "管理员" + admin_name + "的密码修改成功!"
                except Exception as err:
                    print(err)
                    insert_result = "修改管理员密码失败!"
                    pass
                db.commit()
            if select == '删除管理员':
                try:
                    sql_delete = "delete from admin where admin_name='" + admin_name + "';"
                    cursor.execute(sql_delete)
                    insert_result = "成功删除管理员" + admin_name
                except Exception as err:
                    print(err)
                    insert_result = "删除管理员失败"
                    pass
                db.commit()

        else:  # 输入验证不通过
            insert_result = "输入的格式不符合要求!"
        # POST方法时显示数据
        sql_list = "select * from admin"
        cursor.execute(sql_list)
        results = cursor.fetchall()
    return flask.render_template('adminstator.html', insert_result=insert_result, results=results)


@ad.route('/application', methods=['GET', "POST"])
def application():
    insert_result = ''
    # 获取显示管理员数据信息(GET方法的时候显示数据)
    if flask.request.method == 'GET':
        sql_list = "select * from request"
        cursor.execute(sql_list)
        results = cursor.fetchall()

    if flask.request.method == 'POST':

        cat_name = request.values.get("cat_name", "")
        user_name = request.values.get("user_name", "")
        phone = request.values.get("phone", "")
        email = request.values.get("email", "")
        address = request.values.get("address", "")
        exp = request.values.get("exp", "")
        print(user_name, cat_name, phone, email, address, exp)
        try:

            # 信息存入数据库
            sql_1 = "update request set exp=%s where realname=%s and cat_name=%s;"

            cursor.execute(sql_1, (exp, user_name, cat_name))
            insert_result = "审核通过！"
            print(insert_result)
        except Exception as err:
            print(err)
            insert_result = "审核失败！"
            print(insert_result)
            pass
        db.commit()
        # POST方法时显示数据
        sql_list = "select * from request"
        cursor.execute(sql_list)
        results = cursor.fetchall()
    return flask.render_template('application.html', insert_result=insert_result, results=results)


if __name__ == '__main__':
    ad.run(debug=True, host='127.0.0.1')
