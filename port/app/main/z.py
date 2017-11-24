from . import cur, conn
import hashlib
from flask import render_template, request, jsonify, session, make_response, redirect, url_for, g
import time
import functools
import json
import pymysql
import calendar

# c = pymysql.connect(host='127.0.0.1',user='root',password='mysql',db='admin_user',charset="utf8")
# u = conn.cursor()

# 查询
def check_mysql(tables=None, column='*', where=None, sql=None):
    if sql:
        employee = cur.execute(sql)
        return cur.fetchall()

    if where:
        sql = 'select %s from %s where %s' % (column, tables, where)
        # print(sql)
        employee = cur.execute(sql)
        return cur.fetchall()


    sql = 'select %s from %s' % (column, tables)
    employee = cur.execute(sql)
    return cur.fetchall()




# 保存
def save_mysql(tables, data):
    '''
    例：
    data['user_id'] = user_id
    data['value'] = value
    data['time'] = time.time()
    save_mysql('session', data)
    :param tables:表名
    :param data: 字典　键：字段　值：值　
    :return:
    '''
    fields = ''
    values = ''
    for k, v in data.items():
        fields += str(k) + ','
        values += '"%s",' % str(v)

    sql = 'insert into %s(%s) values(%s);' % (tables, fields[:-1], values[:-1])
    print(sql)
    employee = cur.execute(sql)
    conn.commit()
    return employee

# 修改
def update_mysql(tables, data, where):
    '''
    例子：update_mysql('admin_role', {'exempla':'角色'}, 'role="角色D"')
    '''
    set = ''
    for k, v in data.items():
        if type(1) == type(v):
            set += '%s=%d,' % (k, v)
            continue
        set += '%s="%s",' % (k, v)
    sql = 'update %s set %s where %s' % (tables, set[:-1], where)
    print(sql)
    employee = cur.execute(sql)
    conn.commit()
    return employee

# 加密
def md5(password):
    hash = hashlib.md5()
    hash.update(password.encode('utf-8'))
    return hash.hexdigest()

# 判断成功登录装饰器:　没用
def login_required(function):
    @functools.wraps(function)
    def ll(*args, **kwargs):
        # 获取值并判断是否为空
        id = request.cookies.get('id')
        if id == None:
            return render_template('login.html')

        # 根据值和时间，查询用户ｉｄ值
        user = check_mysql('session', 'user_id', where='value="%s" and time>"%s"' % (id, time.time()-30000))
        user_id = None
        if user:
            user = user[0]
        if user:
            user_id = user[0]

        # 判断用户id 是否未空
        if not user_id:
            return render_template('login.html')

        # print(user_id)
        g.user_id = user_id
        admin = check_mysql('admin_user', 'id, name, tel', where='id="%s"' % user_id)
        g.tel = admin[0][2]
        g.admin_id = admin[0][0]
        g.name = admin[0][1]
        print(g.tel, '电话')
        print(g.admin_id, '用户ｉｄ')
        print(g.name, '用户姓名')

        # print(tel)
        # 函数
        return function(*args, **kwargs)

        # return redirect(url_for('.home'))
    return ll


# 电话存在执行
def have_tel_run(function):
    @functools.wraps(function)
    def ll(*args, **kwargs):
        data = {
            "code": 404,
            "msg": "成功",
            "result": "-1",
        }
        tel = request.form['tel']
        g.tel = tel
        if 11 != len(tel):
            data['msg'] = '手机号错误'

        info = check_mysql('360_user', 'id', where='mobile="%s"' % tel)
        if not len(info):
            data['msg'] = '电话不存在'
            json_data = json.dumps(data)
            print('电话不存在')
            return json_data
        if not len(info[0]):
            data['msg'] = '电话不存在'
            json_data = json.dumps(data)
            print('电话不存在')
            return json_data

        return function(*args, **kwargs)
    return ll

# 查询注册用户个人信息
def user_info(mobile):
    '''
    获取手机号查询信息，返回字典信息　和　用户ｉｄ
    :param mobile: 手机号
    :return: 字典，　用户ｉｄ
    '''
    user_info_tuple = check_mysql('360_user',
                                 'username, nikename, header_image, email, card_number, Province_id, City_id, House_adress, User_type, Source_channel, Ip_address, Status, House_type, sex, sb_id, gjj_id, gs_id, id, mobile',
                                 where='mobile="%s"' % mobile)

    if not len(user_info_tuple):
        return {}

    data = {
        "username": user_info_tuple[0][0],  # 用户名
        "nikename": user_info_tuple[0][1],  # 昵称
        "header_image": user_info_tuple[0][2],  # 头像地址
        "email": user_info_tuple[0][3],  # 邮箱
        "card_number": user_info_tuple[0][4],  # 身份证号
        "Province_id": user_info_tuple[0][5],  # 省份ID
        "City_id": user_info_tuple[0][6],  # 城市ID
        "House_adress": user_info_tuple[0][7],  # 户口所在地
        "User_type": user_info_tuple[0][8],  # 用户类型（1代表正常注册，2代表推广用户）
        "Source_channel": user_info_tuple[0][9],  # 来源渠道（1代表PC，2代表微信，3代表手机站，4代表android，5代表IOS）
        "Ip_address": user_info_tuple[0][10],  # IP地址
        "Status": user_info_tuple[0][11],  # 用户状态（1代表正常用户，2代表禁用）
        "House_type": user_info_tuple[0][12],  # 户口类型
        "sex": user_info_tuple[0][13],  # 性别
        "sb_id": user_info_tuple[0][14],  # 社保
        "gjj_id": user_info_tuple[0][15],  # 公积金
        "gs_id": user_info_tuple[0][16],  # 个税
        "id" : user_info_tuple[0][17],  # id
        "mobile" : user_info_tuple[0][18],  # 电话
    }

    return data, str(user_info_tuple[0][17])

# save log
def save_log(tel, inner, p_type, ip=''):
    try:
        user_dict, id = user_info(tel)
        data = {
            "user_id" : user_dict['id'],  #
            "source" : user_dict['Source_channel'],  # 用户来源
            "info" : inner,  # 内容
            "type" : p_type,  # 类型
            "province" : user_dict['Province_id'],   # 省id
            "city" : user_dict['City_id'],  # 市id
            "name" : user_dict['username'],  # 操作人姓名
            "ip" : ip,  # 操作人ip
        }
        save_mysql('log_info', data)
    except Exception as ret:
        print('存入log错误：', ret)


# 查询关于注册用户所有社保信息
def sb_all_info(id):
    '''
    获取注册用户的ｉｄ　查询所有关联下的社保信息
    :param id: 注册用户ｉｄ
    :return: 社保所有信息
    '''
    # social_all_info = check_mysql('SocialSecurity_info',
    #                           'id, name, House_type, Total_paymonth, Card_number, Social_number, Phone, Payment_type, Income_wages, owned_company, Insured_area, Hospital1, Hospital2, Hospital3, Hospital4, Hospital5, Insured_status, Recently_paid',
    #                           where='find_in_set(%s, userid)' % id)

    social_all_info = check_mysql('SocialSecurity_info',
                              'id, name, House_type, Total_paymonth, Card_number, Social_number, Phone, Payment_type, Income_wages, owned_company, Insured_area, Hospital1, Hospital2, Hospital3, Hospital4, Hospital5, Insured_status, Recently_paid, Card_progress',
                              where='userid="%s"' % id)
    if not len(social_all_info):
        return []

    data_list = []
    for social_tuple in social_all_info:
        data = {
            "username": social_tuple[1],  # 社保用户名
            # "House_type": social_tuple[2],  # 户口类型
            # "Total_paymonth": social_tuple[3],  # 累计缴纳
            # "Card_number": social_tuple[4],  # 身份证号
            # "Social_number": social_tuple[5],  # 社保编号
            # "Phone": social_tuple[6],  # 联系电话
            # "Payment_type": social_tuple[7],  # 缴费人员类别
            # "Income_wages": social_tuple[8],  # 申报月工资收入
            # "owned_company": social_tuple[9],  # 所属公司
            # "Insured_area": social_tuple[10],  # 参保区域
            # "Hospital1": social_tuple[11],  # 定点医院1
            # "Hospital2": social_tuple[12],  # 定点医院2
            # "Hospital3": social_tuple[13],  # 定点医院3
            # "Hospital4": social_tuple[14],  # 定点医院4
            # "Hospital5": social_tuple[15],  # 定点医院5
            # "Insured_status": social_tuple[16],  # 参保状态
            # "Recently_paid": social_tuple[17],  # 最近缴纳
            "id": social_tuple[0],  # 社保ｉｄ
            # "Card_progress" : social_tuple[18],  # 制卡进度字段（1，2，3..代表制卡的进度）
            "type": 2,
        }
        # 添加性别
        try:
            data['sex'] = '0' if int(social_tuple[4][-2]) % 2 == 0 else '1'
        except Exception as e:
            print(e)
            data['sex'] = '身份证错误'
        data_list.append(data)

    return data_list

# 查询社保个人信息
def sb_info(sb_id):
    '''
    根据ｉｄ查询社保个人信息，返回字段　和　绑定用户注册用户的ｉｄ列表
    :param sb_id: 表id值
    :return: 字典：个人信息　　　列表：关联注册用户ｉｄ
    '''
    social_info = check_mysql('SocialSecurity_info',
                              'userid, name, House_type, Total_paymonth, Card_number, Social_number, Phone, Payment_type, Income_wages, owned_company, Insured_area, Hospital1, Hospital2, Hospital3, Hospital4, Hospital5, Insured_status, Recently_paid, id, Card_progress',
                              where='id="%s"' % sb_id)

    # 判断查询社保是否为空
    if not len(social_info):
        return {}

    data = {
        "name": social_info[0][1],  # 社保用户名
        "House_type": social_info[0][2],  # 户口类型
        "Total_paymonth": social_info[0][3],  # 累计缴纳
        "Card_number": social_info[0][4],  # 身份证号
        "Social_number": social_info[0][5],  # 社保编号
        "Phone": social_info[0][6],  # 联系电话
        "Payment_type": social_info[0][7],  # 缴费人员类别
        "Income_wages": social_info[0][8],  # 申报月工资收入
        "owned_company": social_info[0][9],  # 所属公司
        "Insured_area": social_info[0][10],  # 参保区域
        "Hospital1": social_info[0][11],  # 定点医院1
        "Hospital2": social_info[0][12],  # 定点医院2
        "Hospital3": social_info[0][13],  # 定点医院3
        "Hospital4": social_info[0][14],  # 定点医院4
        "Hospital5": social_info[0][15],  # 定点医院5
        "Insured_status": social_info[0][16],  # 参保状态
        "Recently_paid": social_info[0][17],  # 最近缴纳
        "id" : social_info[0][18],  # id
        "Card_progress" : social_info[0][19],  # 制卡进度字段（1，2，3..代表制卡的进度）
    }
    user_id_list = social_info[0][0].split(',')  # 社保用户关联的注册用户的ｉｄ

    return data, user_id_list

# 查询社保历史信息
def sb_history_info(sb_id):
    '''
    根据社保ｉｄ，查询社保历史信息返回数据
    :param sb_id: 　社保ｉｄ
    :return: {'medical':[{},{}], ....}
    '''
    social_history = check_mysql('SocialSecurity_list',
                'deposit_time, companypay_money, Individualspay_money, basemoney, Owned_company, remark',
                where='Userid="%s" order by deposit_time desc' % sb_id)

    if not len(social_history):
        return {}

    data_dict = {
        "medical": [],  # 医保
        "endowment": [],  # 养老
        "unemployment": [],  # 失业
        "wound": [],  # 工伤
        "maternity": [],  # 生育
    }
    data_dict1 = {"year": '', "list": []}
    data_dict2 = {"year": '', "list": []}
    data_dict3 = {"year": '', "list": []}
    data_dict4 = {"year": '', "list": []}
    data_dict5 = {"year": '', "list": []}
    data = {}
    for social in social_history:

        data = {
            "deposit_time": social[0],  # 缴存时间
            "companypay_money": social[1],  # 单位缴纳数额
            "Individualspay_money": social[2],  # 个人缴纳数额
            "basemoney": social[3],  # 缴纳基数
            "Owned_company": social[4],  # 缴办单位
        }
        remark = social[5]
        if remark == '医保':
            # data_dict['medical'].append(data)
            if social[0][:4] == data_dict1["year"]:
                data_dict1["list"].append(data)
                continue
            if data_dict1["year"]:
                data_dict['medical'].append(data_dict1)
            data_dict1 = {"year": social[0][:4], "list": [data]}

        elif remark == '养老':
            if social[0][:4] == data_dict2["year"]:
                data_dict2["list"].append(data)
                continue
            if data_dict2["year"]:
                data_dict['endowment'].append(data_dict2)
            data_dict2 = {"year": social[0][:4], "list": [data]}
            # data_dict['endowment'].append(data)
        elif remark == '失业':
            if social[0][:4] == data_dict3["year"]:
                data_dict3["list"].append(data)
                continue
            if data_dict3["year"]:
                data_dict['unemployment'].append(data_dict3)
            data_dict3 = {"year": social[0][:4], "list": [data]}
            # data_dict['unemployment'].append(data)
        elif remark == '工伤':
            if social[0][:4] == data_dict4["year"]:
                data_dict4["list"].append(data)
                continue
            if data_dict4["year"]:
                data_dict['wound'].append(data_dict4)
            data_dict4 = {"year": social[0][:4], "list": [data]}
            # data_dict['wound'].append(data)
        elif remark == '生育':
            if social[0][:4] == data_dict5["year"]:
                data_dict5["list"].append(data)
                continue
            if data_dict5["year"]:
                data_dict['maternity'].append(data_dict5)
            data_dict5 = {"year": social[0][:4], "list": [data]}
            # data_dict['maternity'].append(data)
        else:
            print(data, '分类五险失败')
    data_dict['medical'].append(data_dict1)
    data_dict['endowment'].append(data_dict2)
    data_dict['unemployment'].append(data_dict3)
    data_dict['wound'].append(data_dict4)
    data_dict['maternity'].append(data_dict5)

    return data_dict


            # info:[]


# 个税：关联注册用户　所有个人信息
def gs_all_info(id):
    gs_all_info = check_mysql('personaltax_info',
                                  'Username, Sex, Card_number, Recently_paid, Monthly_deposit, owned_company, pay_total, id',
                                  where='UserID="%s"' % id)
    if not len(gs_all_info):
        return []

    data_list = []
    for gs_info in gs_all_info:
        data = {
            "username" : gs_info[0],  # 用户姓名
            "sex" : str(gs_info[1]),  # 1代表男，2代表女
            # "Card_number" : gs_info[2],  # 身份证号
            # "Recently_paid" : gs_info[3],  # 最近缴纳
            # "Monthly_deposit" : gs_info[4],  # 月缴存额
            # "owned_company" : gs_info[5],  # 所属单位
            # "pay_total" : gs_info[6],  # 缴纳总额
            "id": gs_info[7],  # id
            "type": 1,
        }
        data_list.append(data)

    return data_list

# 个税：　个人信息
def gs_info(gs_id):
    '''
    返回：信息，　关联ｉｄ
    '''

    gs_info = check_mysql('personaltax_info',
                              'UserID, Username, Sex, Card_number, Recently_paid, Monthly_deposit, owned_company, pay_total, id, Update_time',
                              where='id="%s"' % gs_id)

    # 判断查询社保是否为空
    if not len(gs_info):
        return {}

    data = {
        "Username" : gs_info[0][1],  # 用户姓名
        "Sex" : gs_info[0][2],  # 1代表男，2代表女
        "Card_number" : gs_info[0][3],  # 身份证号
        "Recently_paid" : gs_info[0][4],  # 最近缴纳
        "Monthly_deposit" : gs_info[0][5],  # 月缴存额
        "owned_company" : gs_info[0][6],  # 所属单位
        "pay_total" : gs_info[0][7],  # 缴纳总额
        "id" : gs_info[0][8],  # id
        "recent_update_time": gs_info[0][9]  # 修改时间(最近更新时间)
    }
    user_id_list = gs_info[0][0].split(',')  # 社保用户关联的注册用户的ｉｄ

    return data, user_id_list

# 查询个税历史信息
def gs_history_info(gs_id):
    '''
    :return: [{}, {}...]
    '''
    gs_history = check_mysql('personaltax_list',
                'Pay_time, Tax_type, Tax_rate, Taxable_income, Income_money, Withhold_taxable, Owned_company, Update_time',
                where='Userid="%s" order by Pay_time desc' % gs_id)

    if not len(gs_history):
        return []


    data_list = []

    data_dict = {"year":'', "list":[], "tax_sum":0}
    for info in gs_history:


        data = {
            "Pay_time" : info[0],  # 缴纳时间
            "Tax_type" : info[1],  # 纳税项目
            "Tax_rate" : info[2],  # 税率
            "Taxable_income" : info[3],  # 纳税所得
            "Income_money" : info[4],  # 收入额
            "Withhold_taxable" : info[5],  # 实际扣缴所得税
            "Owned_company" : info[6],  # 纳税义务人
        }
        if info[0][:4] == data_dict["year"]:
            data_dict["list"].append(data)
            data_dict["tax_sum"] += int(info[5])
            continue
        if data_dict["year"]:
            data_list.append(data_dict)
        data_dict = {"year": info[0][:4], "list": [data], "tax_sum":0}

    data_list.append(data_dict)
        # data_list.append(data)

    return data_list


# 公积金：关联注册用户　所有个人信息
def gjj_all_info(id):
    gjj_all_info = check_mysql('bjgjj_info',
                                  'id, username, Sex, Card_number, Department_number, Bank_card, Phone, Pay_status, Fund_banlance, Insured_area, Owned_company',
                                  where='User_id="%s"' % id)
    if not len(gjj_all_info):
        return []

    data_list = []
    for gjj_info in gjj_all_info:
        data = {
            "id" : gjj_info[0],  # id
            "username" : gjj_info[1],  # 用户名
            "sex" : str(gjj_info[2]),  # 性别
            # "Card_number" : gjj_info[3],  # 身份证号
            # "Department_number" : gjj_info[4],  # 职工账号
            # "Bank_card" : gjj_info[5],  # 银行卡号
            # "Phone" : gjj_info[6],  # 电话
            # "Pay_status" : gjj_info[7],  # 当前缴纳状态
            # "Fund_banlance" : gjj_info[8],  # 公积金余额
            # "Insured_area" : gjj_info[9],  # 当前缴纳区域
            # "Owned_company" : gjj_info[10],  # 所属公司单位
            "type": 3,
        }
        data_list.append(data)

    return data_list

# 公积金：　个人信息
def gjj_info(gjj_id):
    '''
    返回：信息，　关联ｉｄ
    '''

    gjj_info = check_mysql('bjgjj_info',
                              'id, username, Sex, Card_number, Department_number, Bank_card, Phone, Pay_status, Fund_banlance, Insured_area, Owned_company, User_id, last_year_money',
                              where='id="%s"' % gjj_id)

    # 判断查询社保是否为空
    if not len(gjj_info):
        return {}

    data = {
        "id": gjj_info[0][0],  # id
        "username": gjj_info[0][1],  # 用户名
        "Sex": gjj_info[0][2],  # 性别
        "Card_number": gjj_info[0][3],  # 身份证号
        "Department_number": gjj_info[0][4],  # 职工账号
        "Bank_card": gjj_info[0][5],  # 银行卡号
        "Phone": gjj_info[0][6],  # 电话
        "Pay_status": gjj_info[0][7],  # 当前缴纳状态
        "Fund_banlance": gjj_info[0][8],  # 公积金余额
        "Insured_area": gjj_info[0][9],  # 当前缴纳区域
        "Owned_company": gjj_info[0][10],  # 所属公司单位
        "last_year_money": gjj_info[0][12]  # 去年余额
    }
    user_id_list = gjj_info[0][11].split(',')  # 社保用户关联的注册用户的ｉｄ

    return data, user_id_list

# 公积金：　历史信息
def gjj_history_info(gjj_id):
    '''
    :return: [{}, {}...]
    '''
    gjj_history = check_mysql('bjgjj_history',
                'Transact_time, Abstract, Occurrencev, Balance, Company_number, Owned_company, type, increase, reduce',
                where='Userid="%s" order by Transact_time desc' % gjj_id)

    if not len(gjj_history):
        return []

    print(gjj_history)

    data_list = []

    data_info = {
        "add": '',  # 月缴存额（该月增加额）
        "unit_pay": '',  # 单位月缴纳额
        "individual_pay": '',  # 个人月缴纳额
        "year_sum": 0,  # 本年缴交，增加额度相加
        "year_reduce": 0,  # 本年支取
        "pay_bottom": '',  # 缴至年月
    }

    data_dict = {
        "year": '',
        "list": [],
        "gjj_sum": 0,
    }
    # 提取个人信息
    gjj_individual, user_id_list = gjj_info(gjj_id)
    data_info["Fund_banlance"] = gjj_individual["Fund_banlance"]  # 转出余额
    data_info["last_year_money"] = gjj_individual["last_year_money"]  # 上年结转余额


    for info in gjj_history:

        data = {
            "Transact_time": info[0],  # 入账办结时间
            "Abstract": info[1],  # 摘要／业务逻辑
            "Occurrencev": info[2],  # 发生额
            "Balance": info[3],  # 公积金余额
            "Company_number": info[4],  # 单位账号
            "Owned_company": info[5],  # 纳税义务人（公司）
            # "type" : info[6],  # 业务逻辑
            "increase": info[7],  # 增加额(元)
            "reduce": info[8],  # 减少额(元)
        }
        print(info)

        # data_list.append(data)
        # 月缴存额
        if not data_info["add"] and data["increase"]:
            data_info["add"] = data["increase"]
            data_info["unit_pay"] = round(data['increase']/2, 2)
            data_info["individual_pay"] = round(data['increase'] / 2, 2)

        # 缴至年月=（可抓取到就是最近一次办理业务的时间，往后推到月底。）
        if not data_info["pay_bottom"]:
            time_str = ''.join(info[0].split('-'))
            w, m = calendar.monthrange(int(time_str[:4]), int(time_str[4:6]))
            data_info["pay_bottom"] = time_str[:6] + str(m)


        # 本年缴纳额
        if time.strftime('%Y-%m-%d',time.localtime(time.time())) == info[0][4] and data["increase"]:
            data_info["year_sum"] += data["increase"]

        # 本年支取
        if time.strftime('%Y-%m-%d', time.localtime(time.time())) == info[0][4] and data["reduce"]:
            data_info["year_reduce"] += data["reduce"]

        # 每年总额
        if info[0][:4] == data_dict["year"]:
            data_dict["list"].append(data)
            data_dict["gjj_sum"] += int(info[7] if info[7] else 0)
            continue
        if data_dict["year"]:
            data_list.append(data_dict)
        data_dict = {"year": info[0][:4], "list": [data], "gjj_sum": 0}

    data_list.append(data_dict)
    data_list.append(data_info)

    return data_list


