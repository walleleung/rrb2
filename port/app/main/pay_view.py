from . import main  #, cur
# from flask import render_template, request, jsonify, session, make_response, redirect, url_for
import json
import requests
import random
from .z import *
from threading import Thread
from .bj.bjgjj import bjgjj_one, bjgjj_two
from .bj.bjgs import bjgs_one, bjgs_two
from .bj.bjrbj import bjsb_one, bjsb_two

# 社保
@main.route('/society/info', methods=['post'])
def society_info():
    '''
    根据用户电话查询ｉｄ
    根据社保ｉｄ查询社保信息和关联用户ｉｄ
    判断用户ｉｄ是否关联社保信息
    :return: 社保个人信息
    '''
    tel = request.form['tel']
    sb_id = request.form['sb_id']

    data = {
        "code": 404,
        "msg": "查询成功",
        "result": "-1",
        # "userinfo":''
    }

    # 获取用户信息　和　ｉｄ
    user, id = user_info(tel)

    # 根据ｉｄ查询社保信息
    social_info, user_id_list = sb_info(sb_id)


    # 判断查询社保是否为空
    if not social_info:
        data['msg'] = '查询失败'
        json_data = json.dumps(data)
        print('查询数据为空')
        return json_data

    # 判断用户ｉｄ是否关联社保ｉｄ
    if id not in user_id_list:
        data['msg'] = '查询失败'
        json_data = json.dumps(data)
        print('不是关联的社保')
        return json_data



    data['code'] = 200
    data['result'] = '1'
    data['data'] = social_info
    json_data = json.dumps(data)
    print('查询成功')
    print(json_data)
    save_log(tel, '查询社保个人信息', '社保', ip=request.remote_addr)
    return json_data

# 关于注册用户所有社保个人信息
@main.route('/society/all', methods=['post'])
def society_all():
    tel = request.form['tel']

    user, id = user_info(tel)
    society_all_list = sb_all_info(id)

    data = {
        "code": 200,
        "msg": "成功",
        "result": "1",
    }
    data['list'] = society_all_list
    json_data = json.dumps(data)
    print('查询关联注册用户所有社保信息成功')
    print(json_data)
    save_log(tel, '查询关联社保人', '社保', ip=request.remote_addr)
    return json_data

# 社保历史信息
@main.route('/society/history', methods=['post'])
@have_tel_run
def society_history():
    sb_id = request.form['sb_id']
    type5 = request.form['type']
    type_list = [
        "medical",  # 医保
        "endowment",  # 养老
        "unemployment",  # 失业
        "wound",  # 工伤
        "maternity",  # 生育
    ]
    society_dict = sb_history_info(sb_id)[type_list[int(type5)-1]]




    data = {
        "code": 200,
        "msg": "成功",
        "result": "1",
    }
    data['list'] = society_dict
    json_data = json.dumps(data)
    print('查询关联注册用户所有社保信息成功')
    print(json_data)
    save_log(g.tel, '查询社保历史信息', '社保', ip=request.remote_addr)
    return json_data


# 个税：　全部
@main.route('/tax/all', methods=['post'])
def tax_all():
    tel = request.form['tel']

    user, id = user_info(tel)
    tax_all_list = gs_all_info(id)

    data = {
        "code": 200,
        "msg": "成功",
        "result": "1",
    }
    data['list'] = tax_all_list
    json_data = json.dumps(data)
    print('查询关联注册用户所有个税信息成功')
    print(json_data)
    save_log(tel, '查询用户关联个税用户', '个税', ip=request.remote_addr)
    return json_data

    # gs_all_info()

# 个税：　一个
@main.route('/tax/info', methods=['post'])
def tax_info():
    tel = request.form['tel']
    gs_id = request.form['gs_id']

    data = {
        "code": 404,
        "msg": "查询成功",
        "result": "-1",
    }

    # 获取注册用户ｉｄ　查询个税信息和关联字段
    user, id = user_info(tel)
    tax_info, user_id_list = gs_info(gs_id)


    # 判断查询社保是否为空
    if not tax_info:
        data['msg'] = '查询失败'
        json_data = json.dumps(data)
        print('查询数据为空')
        return json_data

    print(id, user_id_list)
    # 判断用户ｉｄ是否关联社保ｉｄ
    if id not in user_id_list:
        data['msg'] = '查询失败'
        json_data = json.dumps(data)
        print('不是关联的个税')
        return json_data

    data['code'] = 200
    data['result'] = '1'
    data['data'] = tax_info
    json_data = json.dumps(data)
    print('查询个税成功')
    print(json_data)
    save_log(tel, '查询个税单个信息', '个税', ip=request.remote_addr)
    return json_data

# 个税：历史信息
@main.route('/tax/history', methods=['post'])
@have_tel_run
def tax_history():
    gs_id = request.form['gs_id']

    tax_list = gs_history_info(gs_id)


    data = {
        "code": 200,
        "msg": "成功",
        "result": "1",
    }
    data['list'] = tax_list
    json_data = json.dumps(data)
    print('查询关联注册用户所有个税信息成功')
    print(json_data)
    save_log(g.tel, '查询个税历史信息', '个税', ip=request.remote_addr)
    return json_data


# 公积金：　全部
@main.route('/fund/all', methods=['post'])
def fund_all():
    tel = request.form['tel']

    user, id = user_info(tel)
    fund_all_list = gjj_all_info(id)

    data = {
        "code": 200,
        "msg": "成功",
        "result": "1",
    }

    data['list'] = fund_all_list
    json_data = json.dumps(data)
    print('查询关联注册用户所有公积金信息成功')
    print(json_data)
    save_log(tel, '查询用户关联公积金用户', '公积金', ip=request.remote_addr)
    return json_data

# 公积金：　一个
@main.route('/fund/info', methods=['post'])
def fund_info():
    tel = request.form['tel']
    gjj_id = request.form['gjj_id']

    data = {
        "code": 404,
        "msg": "查询成功",
        "result": "-1",
    }

    # 获取注册用户ｉｄ　查询个税信息和关联字段
    user, id = user_info(tel)
    fund_info, user_id_list = gjj_info(gjj_id)


    # 判断查询社保是否为空
    if not fund_info:
        data['msg'] = '查询失败'
        json_data = json.dumps(data)
        print('查询数据为空')
        return json_data

    # 判断用户ｉｄ是否关联社保ｉｄ
    if id not in user_id_list:
        data['msg'] = '查询失败'
        json_data = json.dumps(data)
        print('不是关联的个税')
        return json_data

    data['code'] = 200
    data['result'] = '1'
    data['data'] = fund_info
    json_data = json.dumps(data)
    print('查询个税成功')
    print(json_data)
    save_log(tel, '查询公积金单个信息', '公积金', ip=request.remote_addr)
    return json_data

# 公积金：历史信息
@main.route('/fund/history', methods=['post'])
@have_tel_run
def fund_history():
    gjj_id = request.form['gjj_id']

    fund_list = gjj_history_info(gjj_id)


    data = {
        "code": 200,
        "msg": "成功",
        "result": "1",
    }
    data['list'] = fund_list
    json_data = json.dumps(data)
    print('查询关联注册用户所有公积金信息成功')
    print(json_data)
    save_log(g.tel, '查询公积金历史信息', '公积金', ip=request.remote_addr)
    return json_data



# 添加：社保
@main.route('/society/add', methods=['post'])
def society_add():
    user_id = request.form['user_id']
    id_card = request.form['id_card']
    password = request.form['password']
    card_type = request.form['card_type']
    # 调用爬虫，传入参数用户ｉｄ，存入数据库
    # save_mysql('SocialSecurity_info', {"userid" : user_id, 'card_number' : id_card, "password" : password})  # 测试

    # 线程 调用爬虫
    t = Thread(target=bjsb_one, args=(id_card, password, card_type, user_id))
    t.start()

    # 返回结果
    data = {
        "code": 200,
        "msg": "成功",
        "result": "1",
    }
    json_data = json.dumps(data)
    print('社保调用爬虫成功')

    return json_data

# 获取:社保 手机短信
@main.route('/society/tel/code', methods=['post'])
def society_code():
    id_card = request.form['id_card']
    tel_code = request.form['tel_code']
    with open('./tel_code/'+ id_card+'.txt', 'w')as f:
        f.write(tel_code)
    # print(id_card)

    data = {
        "code": 200,
        "msg": "成功",
        "result": "1",
    }
    for i in range(600):
        with open('./tel_code/'+ id_card+'.txt', 'r')as f:
            text = f.read()
        if '成功' == text:
            return json.dumps(data)
        time.sleep(0.1)

    data = {
        "code": 404,
        "msg": "失败",
        "result": "-1",
    }
    return json.dumps(data)


# 添加：个税
@main.route('/tax/add', methods=['post'])
def tax_add():
    user_id = request.form['user_id']
    card = request.form['card']
    name = request.form['name']
    card_type = request.form['card_type']
    password = request.form['password']
    # 调用爬虫，传入参数用户ｉｄ，存入数据库
    # save_mysql('personaltax_info', {"UserID": user_id, 'card': card, "password": password, 'Username' : name, 'card_type':card_type})  # 测试
    status = bjgs_one(card, password, name, card_type, user_id)
    # 返回结果
    if status:
        data = {
            "code": 200,
            "msg": "成功",
            "result": "1",
        }
        json_data = json.dumps(data)
        print('存储个税成功')
        return json_data
    data = {
        "code": 404,
        "msg": "失败",
        "result": "-1",
    }
    json_data = json.dumps(data)
    print('存储个税成功')
    return json_data

# 添加：公积金
@main.route('/fund/add', methods=['post'])
def fund_add():
    user_id = request.form['user_id']
    card = request.form['card']
    card_type = request.form['card_type']
    password = request.form['password']
    # 调用爬虫，传入参数用户ｉｄ，存入数据库
    status = bjgjj_one(card, password, card_type, user_id)

    # 抓取失败时:
    if not status:
        data = {
            "code": 404,
            "msg": "失败",
            "result": -1
        }
        json_data = json.dumps(data)
        print('存储公积金失败')
        return json_data

    # save_mysql('bjgjj_info',
    #            {"User_id": user_id, 'card': card, "password": password, 'card_type': card_type})  # 测试
    # 返回结果
    data = {
        "code": 200,
        "msg": "成功",
        "result": "1",
    }
    json_data = json.dumps(data)
    print('存储公积金成功')
    return json_data


# 删除：社保
@main.route('/society/delete', methods=['post'])
@have_tel_run
def society_delete():
    sb_id = request.form['sb_id']
    # user_id = request.form['user_id']
    edit_data = {
        'userid' : 0
    }
    update_mysql('SocialSecurity_info', edit_data, 'id=%s' % sb_id)

    data = {
        "code": 200,
        "msg": "成功",
        "result": "1",
    }
    json_data = json.dumps(data)
    print('删除社保成功')
    return json_data

# 删除：个税
@main.route('/tax/delete', methods=['post'])
@have_tel_run
def tax_delete():
    gs_id = request.form['gs_id']
    edit_data = {
        'UserID': 0
    }
    update_mysql('personaltax_info', edit_data, 'id=%s' % gs_id)

    data = {
        "code": 200,
        "msg": "成功",
        "result": "1",
    }
    json_data = json.dumps(data)
    print('删除个税成功')
    return json_data

# 删除：公积金
@main.route('/fund/delete', methods=['post'])
@have_tel_run
def fund_delete():
    gjj_id = request.form['gjj_id']
    edit_data = {
        'User_id': 0
    }
    update_mysql('bjgjj_info', edit_data, 'id=%s' % gjj_id)

    data = {
        "code": 200,
        "msg": "成功",
        "result": "1",
    }
    json_data = json.dumps(data)
    print('删除公积金成功')
    return json_data

# 更新:社保 (根据社保id抓取数据存储)
@main.route('/society/update', methods=['post'])
@have_tel_run
def society_update():
    sb_id = request.form['sb_id']

    # 线程 调用爬虫
    t = Thread(target=bjsb_two, args=(sb_id,))
    t.start()

    # 返回结果
    data = {
        "code": 200,
        "msg": "成功",
        "result": "1",
    }
    print('更新社保调用爬虫成功')
    #
    return json.dumps(data)


# 更新:个税 (根据个税id抓取数据存储)
@main.route('/tax/update', methods=['post'])
@have_tel_run
def tax_update():
    gs_id = request.form['gs_id']
    status = bjgs_two(gs_id)
    if status:
        data = {
            "code": 200,
            "msg": "成功",
            "result": "1",
        }
        json_data = json.dumps(data)
        print('更新个税成功')
        return json_data

    data = {
        "code": 404,
        "msg": "失败",
        "result": -1
    }
    json_data = json.dumps(data)
    print('更新个税失败')
    return json_data


# 更新:公积金 (根据公积金id抓取数据存储)
@main.route('/fund/update', methods=['post'])
@have_tel_run
def fund_update():
    gjj_id = request.form['gjj_id']
    status = bjgjj_two(gjj_id)
    if status:
        data = {
            "code": 200,
            "msg": "成功",
            "result": "1",
        }
        json_data = json.dumps(data)
        print('更新公积金成功')
        return json_data

    data = {
        "code": 404,
        "msg": "失败",
        "result": -1
    }
    json_data = json.dumps(data)
    print('更新公积金失败')
    return json_data


def cs_sleep():
    a = 0
    while True:
        print(a)
        time.sleep(4)
        a += 1


@main.route('/cs/yield', methods=['post'])
def cs_yield():
    print('111')
    t = Thread(target=cs_sleep)
    t.start()
    # cs_sleep()
    print('222')

    return '333'



@main.route('/cs', methods=['post'])
def cs():
    return 'cs...... ...... ...'

