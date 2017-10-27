from . import main  #, cur
# from flask import render_template, request, jsonify, session, make_response, redirect, url_for
import json
import requests
import random
from .z import *

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
    return json_data

# 社保历史信息
@main.route('/society/history', methods=['post'])
def society_history():
    sb_id = request.form['sb_id']

    society_dict = sb_history_info(sb_id)


    data = {
        "code": 200,
        "msg": "成功",
        "result": "1",
    }
    data['data'] = society_dict
    json_data = json.dumps(data)
    print('查询关联注册用户所有社保信息成功')
    print(json_data)
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
    return json_data

# 个税：历史信息
@main.route('/tax/history', methods=['post'])
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
    return json_data

# 公积金：历史信息
@main.route('/fund/history', methods=['post'])
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
    return json_data
