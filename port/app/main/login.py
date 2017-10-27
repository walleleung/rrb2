from . import main  #, cur
# from flask import render_template, request, jsonify, session, make_response, redirect, url_for
import json
import requests
import random
from .z import *

def send_code(tel, code):
    data = {}
    data['password'] = 'PqCL1zDWvQ7fwKMD'
    data['mobile'] = '%s' % tel
    data['userId'] = 24
    data['action'] = 'send'
    data['sendTime'] = ''
    data['extno'] = ''
    data['account'] = 'renrenbao1'
    data['content'] = '【人人保】您的验证码：%s，切勿将验证码泄露给他人。' % code
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "charset": "UTF-8"
    }
    url = 'http://101.201.54.221:8888/sms.aspx'

    response = requests.post(url, headers=headers, data=data)
    if -1 == response.text.find('<message>ok</message>'):
        return None
    return 1
    # if response.text.find()


# 主页
@main.route('/', methods=['get'])
def index():
    a = request.get_json()
    print(a)
    return '12345'


# ４种功能：登录　注册　重置密码
@main.route('/base', methods=['POST'])
def base():
    '''
    功能：登陆／注册／发送验证码／重置密码
    sort: 1:登陆　２：注册　３：发送验证码　４：重置密码
    tel: 手机号（账号）
    password: 密码
    code: 短信验证码
    :return:
    '''

    # print(request.form)
    sort = request.form['sort']  # 种类
    tel = request.form['tel']
    # password = request.form['password']
    data = {
        "code": 404,
        "msg": "成功",
        "result": "-1",
        # "tel":tel
    }


    # 登陆
    if '1' == sort:
        password = request.form['password']
        user_login = check_mysql('360_user', 'id, password', where='mobile="%s"' % tel)
        if not len(user_login):
            data['msg'] = '账号不存在'
            json_data = json.dumps(data)
            print('账号不存在')
            return json_data

        check_password = user_login[0][1]
        if check_password != md5(password):
            data['msg'] = '密码错误'
            json_data = json.dumps(data)
            print('密码错误')
            return json_data

        data['code'] = 200
        data['result'] = '1'
        user_dict, id = user_info(tel)
        data['data'] = user_dict
        json_data = json.dumps(data)
        print('登陆成功')
        return json_data


    # 注册,发送验证码，重置密码
    if '2' != sort and '3' != sort and '4' != sort:
        data['msg'] = '参数错误'
        json_data = json.dumps(data)
        print('种类错误')
        return json_data


    if 11 != len(tel):
        data['msg'] = '电话格式错误'
        json_data = json.dumps(data)
        print('电话格式错误')
        return json_data

    # 判断账户是否存在
    if '2' == sort:
        user_login = check_mysql('360_user', 'id, password', where='mobile="%s"' % tel)
        if len(user_login):
            data['msg'] = '用户已存在'
            json_data = json.dumps(data)
            print('用户已存在')
            return json_data

    # 发送验证码
    if '3' == sort:
        print('发送验证码保存到数据库')
        random_code = random.randint(100000,999999)
        # if not send_code(tel, random_code):
        #     data['msg'] = '短信发送失败'
        #     json_data = json.dumps(data)
        #     return json_data
        save_data = {
            'code' : random_code,
            'tel' : tel
        }
        if save_mysql('code_info', save_data) < 1:
            data['msg'] = '位置错误'
            json_data = json.dumps(data)
            print('短信验证保存失败')
            return json_data
        data['code'] = 200
        data['result'] = '1'
        json_data = json.dumps(data)
        print('发送验证码成功', random_code)
        return json_data

    # 判断短信验证是否相等
    password = request.form['password']
    check_mysql(sql='delete from code_info where Create_time<"%s"' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()-20000)))
    user_code = check_mysql('code_info', 'id, code', where='tel="%s" and Create_time>"%s" order by Create_time desc' % (tel, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()-300))))
    # print(user_code)

    code = request.form['code']
    if len(user_code) == 0 or code != user_code[0][1]:
        data['msg'] = '验证码错误'
        json_data = json.dumps(data)
        print('验证码错误')
        return json_data

    # 更改密码
    if '4' == sort:
        save_data = {
            'password': md5(password)
        }
        update_mysql('360_user', save_data, 'mobile="%s"' % tel)
        data['code'] = 200
        data['result'] = '1'
        json_data = json.dumps(data)
        print('更改密码成功')
        return json_data

    # 渠道判断
    channel = request.form['channel']
    if int(channel) not in [1,2,3,4,5]:
        data['msg'] = '参数错误'
        json_data = json.dumps(data)
        print('渠道值错误')
        return json_data

    # 注册保存
    save_data = {
        'mobile' : tel,
        'password' : md5(password)
    }
    if save_mysql('360_user', save_data) < 1:
        data['msg'] = '注册失败'
        json_data = json.dumps(data)
        print('注册失败')
        return json_data

    # print(tel, password, code)

    data['code'] = 200
    data['result'] = '1'
    json_data = json.dumps(data)
    print('注册成功')
    return json_data

# 登录
@main.route('/login', methods=['POST'])
def login():
    tel = request.form['tel']
    password = request.form['password']

    data = {
        "code": 404,
        "msg": "成功",
        "result": "-1",
    }


    # 登陆
    user_login = check_mysql('360_user', 'id, password', where='mobile="%s"' % tel)
    if not len(user_login):
        data['msg'] = '账号不存在'
        json_data = json.dumps(data)
        print('账号不存在')
        return json_data

    check_password = user_login[0][1]
    if check_password != md5(password):
        data['msg'] = '密码错误'
        json_data = json.dumps(data)
        print('密码错误')
        return json_data

    data['code'] = 200
    data['result'] = '1'
    user_dict, id = user_info(tel)
    data['data'] = user_dict
    json_data = json.dumps(data)
    print('登陆成功')
    return json_data

# 注册
@main.route('/register', methods=['POST'])
def register():
    tel = request.form['tel']
    password = request.form['password']
    code = request.form['code']

    data = {
        "code": 404,
        "msg": "成功",
        "result": "-1",
        # "tel":tel
    }

    if 11 != len(tel):
        data['msg'] = '电话格式错误'
        json_data = json.dumps(data)
        print('电话格式错误')
        return json_data

    # 判断账户是否存在
    user_login = check_mysql('360_user', 'id, password', where='mobile="%s"' % tel)
    if len(user_login):
        data['msg'] = '用户已存在'
        json_data = json.dumps(data)
        print('用户已存在')
        return json_data

    # 判断短信验证是否相等
    # password = request.form['password']
    check_mysql(sql='delete from code_info where Create_time<"%s"' % time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                   time.localtime(
                                                                                       time.time() - 20000)))
    user_code = check_mysql('code_info', 'id, code',
                            where='tel="%s" and Create_time>"%s" order by Create_time desc' % (
                            tel, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - 300))))
    # print(user_code)


    if len(user_code) == 0 or code != user_code[0][1]:
        data['msg'] = '验证码错误'
        json_data = json.dumps(data)
        print('验证码错误')
        return json_data

    # 注册保存
    save_data = {
        'mobile': tel,
        'password': md5(password)
    }
    if save_mysql('360_user', save_data) < 1:
        data['msg'] = '注册失败'
        json_data = json.dumps(data)
        print('注册失败')
        return json_data

    # print(tel, password, code)

    data['code'] = 200
    data['result'] = '1'
    json_data = json.dumps(data)
    print('注册成功')
    return json_data

# 发送验证码
@main.route('/send/code', methods=['POST'])
def send_code():
    tel = request.form['tel']

    data = {
        "code": 404,
        "msg": "成功",
        "result": "-1",
        # "tel":tel
    }

    if 11 != len(tel):
        data['msg'] = '电话格式错误'
        json_data = json.dumps(data)
        print('电话格式错误')
        return json_data

    random_code = random.randint(100000, 999999)
    # if not send_code(tel, random_code):
    #     data['msg'] = '短信发送失败'
    #     json_data = json.dumps(data)
    #     return json_data
    random_code = 123456  # 测试
    save_data = {
        'code': random_code,
        'tel': tel
    }
    if save_mysql('code_info', save_data) < 1:
        data['msg'] = '位置错误'
        json_data = json.dumps(data)
        print('短信验证保存失败')
        return json_data
    data['code'] = 200
    data['result'] = '1'
    json_data = json.dumps(data)
    print('发送验证码成功', random_code)
    return json_data

# 找回密码
@main.route('/reset/password', methods=['POST'])
def reset_password():
    tel = request.form['tel']
    password = request.form['password']
    code = request.form['code']

    data = {
        "code": 404,
        "msg": "成功",
        "result": "-1",
    }

    if 11 != len(tel):
        data['msg'] = '电话格式错误'
        json_data = json.dumps(data)
        print('电话格式错误')
        return json_data

    # 判断短信验证是否相等
    # password = request.form['password']
    check_mysql(sql='delete from code_info where Create_time<"%s"' % time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                   time.localtime(
                                                                                       time.time() - 20000)))
    user_code = check_mysql('code_info', 'id, code',
                            where='tel="%s" and Create_time>"%s" order by Create_time desc' % (
                            tel, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - 300))))
    # print(user_code)

    if len(user_code) == 0 or code != user_code[0][1]:
        data['msg'] = '验证码错误'
        json_data = json.dumps(data)
        print('验证码错误')
        return json_data

    # 更改密码
    save_data = {
        'password': md5(password)
    }
    update_mysql('360_user', save_data, 'mobile="%s"' % tel)
    data['code'] = 200
    data['result'] = '1'
    json_data = json.dumps(data)
    print('更改密码成功')
    return json_data

# 修改密码
@main.route('/edit/password', methods=['POST'])
def edit_password():
    tel = request.form['tel']
    new_password = request.form['new_password']
    old_password = request.form['old_password']

    data = {
        "code": 404,
        "msg": "成功",
        "result": "-1",
    }

    if 11 != len(tel):
        data['msg'] = '电话格式错误'
        json_data = json.dumps(data)
        print('电话格式错误')
        return json_data

    # 判断密码
    password = check_mysql(tables='360_user', column='password', where='mobile="%s"' % tel)
    if not len(password):
        data['msg'] = '未知错误'
        json_data = json.dumps(data)
        print('查询数据为空')
        return json_data

    if md5(old_password) != password[0][0]:
        data['msg'] = '密码错误'
        json_data = json.dumps(data)
        print('原密码错误')
        return json_data


    # 更改密码
    save_data = {
        'password': md5(new_password)
    }
    update_mysql('360_user', save_data, 'mobile="%s"' % tel)
    data['code'] = 200
    data['result'] = '1'
    json_data = json.dumps(data)
    print('更改密码成功')
    return json_data

# 查询注册用户信息
@main.route('/user/info', methods=['POST'])
def user_check():
    tel = request.form['tel']
    user_dict, id = user_info(tel)
    data = {
        "code": 200,
        "msg": "成功",
        "result": "1",
        # "userinfo" : ''
    }
    data['data'] = user_dict
    json_data = json.dumps(data)
    print('查询注册用户信息成功')
    print(json_data)
    return json_data


# 修改注册用户信息
@main.route('/user/edit', methods=['POST'])
def user_edit():
    tel = request.form['tel']

    post_dict = request.form.to_dict()
    # key:接受的参数名子　　　　value:数据库的字段
    db_dict = {
        "username": "username",  # 用户名
        "nikename": "nikename",  # 昵称
        "header_image": "header_image",  # 头像地址
        "email": "email",  # 邮箱
        "card_number": "card_number",  # 身份证号
        "Province_id": "Province_id",  # 省份ID
        "City_id": "City_id",  # 城市ID
        "House_adress": "House_adress",  # 户口所在地
        "User_type": "User_type",  # 用户类型（1代表正常注册，2代表推广用户）
        "Source_channel": "Source_channel",  # 来源渠道（1代表PC，2代表微信，3代表手机站，4代表android，5代表IOS）
        "Ip_address": "Ip_address",  # IP地址
        "House_type": "House_type",  # 户口类型
        # "account": "account",  # 账号
        "sex": "sex",  # 性别
    }
    # for post_key in post_dict.keys():
    # 可以添加功能：删除有些不能添加的字段　例：del['***']

    data = {}
    key_list = [key for key in db_dict.keys() if key in post_dict]
    for key in key_list:
        data[db_dict[key]] = request.form[key]

    update_mysql('360_user', data, 'mobile="%s"' % tel)

    data = {
        "code": 200,
        "msg": "成功",
        "result": "1",
    }
    json_data = json.dumps(data)
    print('修改注册用户信息成功')
    # print(json_data)
    return json_data


# 首页社保／公积金／个税
@main.route('/user/sgg', methods=['POST'])
def user_sgg():

    data = {
        "code": 200,
        "msg": "成功",
        "result": "1",
        "sb_info" : '',
        "gs_info" : '',
        "gjj_info" : ''
    }
    try:
        sb_id = request.form['sb_id']
        social_info, user_id_list = sb_info(sb_id)
        data['sb_info'] = social_info
    except:
        print('查询社保失败')

    try:
        gs_id = request.form['gs_id']
        tax_info, user_id_list = gs_info(gs_id)
        data['gs_info'] = tax_info
    except:
        print('查询个税失败')

    try:
        gjj_id = request.form['gjj_id']
        fund_info, user_id_list = gjj_info(gjj_id)
        data['gjj_info'] = fund_info
    except:
        print('查询公积金失败')
    # post_dict = request.form.to_dict()

    json_data = json.dumps(data)
    print('查询３个完成')
    # print(json_data)
    return json_data
