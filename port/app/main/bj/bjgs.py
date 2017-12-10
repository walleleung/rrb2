# coding:utf-8
import requests
from lxml import etree
from .rk import code_zy
import time
from .bjdb import *
import re


# 个税
class Bjgs():
    def __init__(self, id_card=None, password=None, name=None, id_card_type='201'):
        self.zzhm = id_card
        self.password = password
        self.xm = name
        self.cookie = ''
        self.ssion = None
        self.zjlx = id_card_type

        # self.driver = webdriver.PhantomJS()

        #self.conn = pymysql.connect(host='127.0.0.1', user='root', password='mysql', db='bjgjj', charset="utf8")
        #self.cur = self.conn.cursor()

    def get_cookie_urls(self):

        url = 'https://gt3app9.tax861.gov.cn/Gt3GsWeb/gsmxwyNo/GrnsxxcxAction.action'

        headers = {
            'Host': 'gt3app9.tax861.gov.cn',
            'Origin': 'https://gt3app9.tax861.gov.cn',
            'Referer': 'https://gt3app9.tax861.gov.cn/Gt3GsWeb/gsmxwyNo/GrnsxxcxAction.action?code=query',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
        self.ssion = requests.session()
        self.ssion.get(url, headers=headers, verify=False)
        code_url = 'https://gt3app9.tax861.gov.cn/Gt3GsWeb/RandomCode.action'  # 验证码图片

        img_code = self.ssion.get(code_url, headers=headers, verify=False)  # 请求验证码

        # 测试
        # with open('code.jpg', 'wb') as f:
        #     f.write(img_code.content)
        #
        # code = input('请输入验证码')

        # 第三方
        code = code_zy(img_code.content)
        print(code)

        # 登陆
        data = {
            'zjlx': self.zjlx,
            'zzhm': self.zzhm,
            'xm': self.xm,
            'password': self.password,
            'yzm': code
        }
        log_url = 'https://gt3app9.tax861.gov.cn/Gt3GsWeb/gsmxwyNo/YhdlAction.action?code=login'
        response = self.ssion.post(log_url, headers=headers, data=data, verify=False)
        return 1

    def get_history(self):
        '''
        获取个税页面的个人信息　和　个人税信息　
        :return: info: type=dict 个人信息    item: type=dict 个人扣税信息
        '''
        # 个人纳税获得
        url = 'https://gt3app9.tax861.gov.cn/Gt3GsWeb/gsmxwyNo/GrnsxxcxAction.action?code=query'

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            # 'Content-Length': '100',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Cookie' : 'JSESSIONID=D66BB2D98894BE7225E2992A797024E2',
            'Host': 'gt3app9.tax861.gov.cn',
            'Origin': 'https://gt3app9.tax861.gov.cn',
            # 'Referer': 'https://gt3app9.tax861.gov.cn/Gt3GsWeb/gsmxwyNo/YhdlAction.action?code=login',
            'Referer': 'https://gt3app9.tax861.gov.cn/Gt3GsWeb/gsmxwyNo/GrnsxxcxAction.action?code=query',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }

        data = {
            'tijiao': 'grsbxxcx',
            'actionType': 'query',
            'index': '',
            'skssksrqN': '2006',
            'skssksrqY': '1',
            'skssjsrqN': time.strftime('%Y',time.localtime(time.time())),
            'skssjsrqY': time.strftime('%m',time.localtime(time.time())),
            'sbbmc': '',
        }

        response = self.ssion.post(url, headers=headers, data=data, verify=False)
        html = etree.HTML(response.text)

        # 个人信息
        info_list = html.xpath('//table//input/@value')
        info = {}
        # info['name'] = info_list[0]  # 姓名
        info['name']  = self.xm  # 姓名
        info['area'] = info_list[1]  # 国籍（地区）
        info['card_type'] = info_list[2]  # 身份证件类型
        info['id_card'] = info_list[3]  # 身份证件号码
        info['card'] = self.zzhm  # 账号
        info['password'] = self.password  # 密码
        info['card_type'] = self.zjlx  # 账号类型

        # with open('cs.html', 'wb')as f:
        #     f.write(response.content)

        # 个税大概区域信息
        inner_lxml = html.xpath('//table[3]')[0]


        # 根据用户ｉｄ查询数据库中的申报日期：((,),(,),(,))
        # mysql_data = ((,),(,),(,))  # 查询数据
        # if [i for i in mysql_data if zzzz in i]:


        tax_list = []  # 所有历史信息
        # 提取每月信息
        html_tr =inner_lxml.xpath('.//tr')  # 每条信息 （前面两条和最后一条没用）
        for tr_info in html_tr[2:-1]:
            tax_history_dict = {}  # 每条历史信息
            tr = tr_info.xpath('./td/text()')
            # tr[0]  # 序号
            tax_history_dict['get_projects'] = tr[1]  # 所得项目
            tax_history_dict['tax_period'] = tr[2]  # 税款所属期
            tax_history_dict['income'] = tr[3]  # 收入额
            tax_history_dict['tax_rate'] = tr[4].strip()  # 税率
            tax_history_dict['fill_refund'] = tr[5]  # 应补(退)税额
            tax_history_dict['date'] = tr[6]  # 申报日期
            tax_history_dict['company'] = tr[7]  # 扣缴义务人名称

            parameter_list = re.split("\('|','|'\)", tr_info.xpath('./td/a/@onclick')[0])  # 提取报告表网址参数

            if 'null' in parameter_list or len(parameter_list)<4:  # 判断是否为空
                tax_list.append(tax_history_dict)
                continue

            # 发送请求　获取扣缴个人所得页面信息
            url = 'https://gt3app9.tax861.gov.cn/Gt3GsWeb/gsmxwyNo/GrnsxxcxAction.action'
            parameter = {
                "code" : parameter_list[0],
                "sbblx" : parameter_list[1],
                "jylsh" : parameter_list[2],
                "sdxm_dm" : parameter_list[3],
            }
            response = self.ssion.get(url, params=parameter, headers=headers, verify=False)
            html = etree.HTML(response.text)

            # 提取参数
            info_list = html.xpath('//tr[3]/td/text()')
            # info_list[0].strip()  # 序号
            tax_history_dict['name'] = info_list[1].strip()  # 姓名
            tax_history_dict['card_type'] = info_list[2].strip()  # 身份证件类型
            tax_history_dict['id_card'] = info_list[3].strip()  # 身份证件号码
            tax_history_dict['get_projects_2'] = info_list[4].strip()  # 所得项目
            tax_history_dict['interval'] = info_list[5].strip()  # 所得期间
            # tax_history_dict[''] = info_list[6].strip()  # 收入额
            tax_history_dict['get_duty_free'] = info_list[7].strip()  # 免税所得
            tax_history_dict['old_age_risk'] = info_list[8].strip()  # 基本养老保险
            tax_history_dict['medical_risk'] = info_list[9].strip()  # 基本医疗保险
            tax_history_dict['unemployment_risk'] = info_list[10].strip()  # 失业保险费
            tax_history_dict['fund_risk'] = info_list[11].strip()  # 住房公积金
            tax_history_dict['original_value'] = info_list[12].strip()  # 财产原值
            tax_history_dict['tax_deductible'] = info_list[13].strip()  # 允许扣除的税费
            tax_history_dict['others'] = info_list[14].strip()  # 其他
            tax_history_dict['total'] = info_list[15].strip()  # 合计
            tax_history_dict['deduction_money'] = info_list[16].strip()  # 减除费用
            tax_history_dict['amount_deductible'] = info_list[17].strip()  # 准予扣除的捐赠额
            tax_history_dict['get_tax'] = info_list[18].strip()  # 应缴税所得额
            # tax_history_dict[''] = info_list[19].strip()  # 税率
            tax_history_dict['buckle_number'] = info_list[20].strip()  # 速算扣除数
            tax_history_dict['tax_payable'] = info_list[21].strip()  # 应纳税额
            tax_history_dict['tax_credit'] = info_list[22].strip()  # 减免税额
            tax_history_dict['buckle_tax'] = info_list[23].strip()  # 应扣缴税额
            tax_history_dict['tax_withheld'] = info_list[24].strip()  # 已扣缴税额
            # tax_history_dict[''] = info_list[25].strip()  # 应补(退)税额
            tax_history_dict['remark'] = info_list[26].strip()  # 备注

            tax_list.append(tax_history_dict)  # 添加


        # print(info)
        # print(tax_list)
        # item_list = inner_lxml.xpath('.//td/text()')
        # try:
        #     item = {}
        #     item['projects'] = item_list[-12]  # 所得项目
        #     item['income'] = item_list[-10]  # 收入额
        #     item['rate'] = item_list[-9].strip()  # 税率
        #     item['tax'] = item_list[-8]  # 应补（退）税额
        #     item['time'] = item_list[-7]  # 申报日期
        #     item['obligation'] = item_list[-6]  # 扣缴义务人名称
        # except:
        #     item={}

        return info, tax_list

    def start(self):
        # 获取cookie
        self.get_cookie_urls()

        # 个人基本信息查询， 返回数据
        info, item = self.get_history()
        print(item)
        print(info)



        # 存入
        bjgs_db = BjgsDb()
        bjgs_db.start(info, item)

    # 第一次
    def first(self, id):
        '''
        注册用户的id
        '''

        # 获取cookie
        self.get_cookie_urls()
        # 个人基本信息查询， 返回数据
        # info, item = self.get_history()
        info, item = self.pseudo_data()  # 假数据

        print(info)
        print(item)

        # 存入
        bjgs_db = BjgsDb()
        bjgs_db.start(id, info, item)

    # 假数据
    def pseudo_data(self):
        '''假数据'''

        info = {'area': '中国', 'id_card': '372924199601063012', 'name': '刘敬', 'card_type': '201', 'card': '372924199601063012', 'password': 'liu123456'}
        # item = [{'income': '8000.00', 'fill_refund': '315.75', 'company': '北京澳环科技有限公司', 'tax_rate': '——', 'get_projects': '工资薪金所得', 'tax_period': '2016-03-01 至 2016-03-31', 'date': '——'}, {'card_type': '居民身份证', 'id_card': '372924199601063012', 'tax_withheld': '0.00', 'remark': '', 'buckle_tax': '40.74', 'tax_payable': '40.74', 'original_value': '0.00', 'amount_deductible': '0.00', 'get_duty_free': '0.00', 'fill_refund': '40.74', 'buckle_number': '0.00', 'fund_risk': '0.00', 'date': '2017-01-14', 'others': '0.00', 'get_tax': '1358.05', 'tax_credit': '0.00', 'medical_risk': '0.00', 'name': '刘敬', 'unemployment_risk': '0.00', 'tax_rate': '3.00', 'tax_period': '2016-12-01 至 2016-12-31', 'old_age_risk': '0.00', 'get_projects_2': '正常工资薪金', 'income': '4858.05', 'deduction_money': '3500.00', 'interval': '2016-12-01 至 2016-12-31', 'tax_deductible': '0.00', 'total': '0.00', 'get_projects': '工资薪金所得', 'company': '博智时代科技（北京）有限公司'}, {'card_type': '居民身份证', 'id_card': '372924199601063012', 'tax_withheld': '0.00', 'remark': '', 'buckle_tax': '164.89', 'tax_payable': '164.89', 'original_value': '0.00', 'amount_deductible': '0.00', 'get_duty_free': '0.00', 'fill_refund': '164.89', 'buckle_number': '105.00', 'fund_risk': '0.00', 'date': '2017-02-13', 'others': '0.00', 'get_tax': '2698.86', 'tax_credit': '0.00', 'medical_risk': '0.00', 'name': '刘敬', 'unemployment_risk': '0.00', 'tax_rate': '10.0', 'tax_period': '2017-01-01 至 2017-01-31', 'old_age_risk': '0.00', 'get_projects_2': '正常工资薪金', 'income': '6198.86', 'deduction_money': '3500.00', 'interval': '2017-01-01 至 2017-01-31', 'tax_deductible': '0.00', 'total': '0.00', 'get_projects': '工资薪金所得', 'company': '博智时代科技（北京）有限公司'}, {'card_type': '居民身份证', 'id_card': '372924199601063012', 'tax_withheld': '0.00', 'remark': '', 'buckle_tax': '44.98', 'tax_payable': '44.98', 'original_value': '0.00', 'amount_deductible': '0.00', 'get_duty_free': '0.00', 'fill_refund': '44.98', 'buckle_number': '0.00', 'fund_risk': '0.00', 'date': '2017-03-06', 'others': '0.00', 'get_tax': '1499.36', 'tax_credit': '0.00', 'medical_risk': '0.00', 'name': '刘敬', 'unemployment_risk': '0.00', 'tax_rate': '3.00', 'tax_period': '2017-02-01 至 2017-02-28', 'old_age_risk': '0.00', 'get_projects_2': '正常工资薪金', 'income': '4999.36', 'deduction_money': '3500.00', 'interval': '2017-02-01 至 2017-02-28', 'tax_deductible': '0.00', 'total': '0.00', 'get_projects': '工资薪金所得', 'company': '博智时代科技（北京）有限公司'}, {'card_type': '居民身份证', 'id_card': '372924199601063012', 'tax_withheld': '0.00', 'remark': '', 'buckle_tax': '84.90', 'tax_payable': '84.90', 'original_value': '0.00', 'amount_deductible': '0.00', 'get_duty_free': '0.00', 'fill_refund': '84.90', 'buckle_number': '105.00', 'fund_risk': '0.00', 'date': '2017-04-15', 'others': '0.00', 'get_tax': '1899.00', 'tax_credit': '0.00', 'medical_risk': '0.00', 'name': '刘敬', 'unemployment_risk': '0.00', 'tax_rate': '10.0', 'tax_period': '2017-03-01 至 2017-03-31', 'old_age_risk': '0.00', 'get_projects_2': '正常工资薪金', 'income': '5399.00', 'deduction_money': '3500.00', 'interval': '2017-03-01 至 2017-03-31', 'tax_deductible': '0.00', 'total': '0.00', 'get_projects': '工资薪金所得', 'company': '博智时代科技（北京）有限公司'}, {'card_type': '居民身份证', 'id_card': '372924199601063012', 'tax_withheld': '0.00', 'remark': '', 'buckle_tax': '164.92', 'tax_payable': '164.92', 'original_value': '0.00', 'amount_deductible': '0.00', 'get_duty_free': '0.00', 'fill_refund': '164.92', 'buckle_number': '105.00', 'fund_risk': '0.00', 'date': '2017-05-05', 'others': '0.00', 'get_tax': '2699.18', 'tax_credit': '0.00', 'medical_risk': '0.00', 'name': '刘敬', 'unemployment_risk': '85.04', 'tax_rate': '10.0', 'tax_period': '2017-04-01 至 2017-04-30', 'old_age_risk': '226.72', 'get_projects_2': '正常工资薪金', 'income': '6510.94', 'deduction_money': '3500.00', 'interval': '2017-04-01 至 2017-04-30', 'tax_deductible': '0.00', 'total': '311.76', 'get_projects': '工资薪金所得', 'company': '博智时代科技（北京）有限公司'}, {'card_type': '居民身份证', 'id_card': '372924199601063012', 'tax_withheld': '0.00', 'remark': '', 'buckle_tax': '254.92', 'tax_payable': '254.92', 'original_value': '0.00', 'amount_deductible': '0.00', 'get_duty_free': '0.00', 'fill_refund': '254.92', 'buckle_number': '105.00', 'fund_risk': '0.00', 'date': '2017-06-05', 'others': '0.00', 'get_tax': '3599.24', 'tax_credit': '0.00', 'medical_risk': '85.04', 'name': '刘敬', 'unemployment_risk': '0.00', 'tax_rate': '10.0', 'tax_period': '2017-05-01 至 2017-05-31', 'old_age_risk': '226.72', 'get_projects_2': '正常工资薪金', 'income': '7411.00', 'deduction_money': '3500.00', 'interval': '2017-05-01 至 2017-05-31', 'tax_deductible': '0.00', 'total': '311.76', 'get_projects': '工资薪金所得', 'company': '博智时代科技（北京）有限公司'}, {'card_type': '居民身份证', 'id_card': '372924199601063012', 'tax_withheld': '0.00', 'remark': '', 'buckle_tax': '54.92', 'tax_payable': '54.92', 'original_value': '0.00', 'amount_deductible': '0.00', 'get_duty_free': '0.00', 'fill_refund': '54.92', 'buckle_number': '105.00', 'fund_risk': '0.00', 'date': '2017-07-07', 'others': '0.00', 'get_tax': '1599.24', 'tax_credit': '0.00', 'medical_risk': '85.04', 'name': '刘敬', 'unemployment_risk': '0.00', 'tax_rate': '10.0', 'tax_period': '2017-06-01 至 2017-06-30', 'old_age_risk': '226.72', 'get_projects_2': '正常工资薪金', 'income': '5411.00', 'deduction_money': '3500.00', 'interval': '2017-06-01 至 2017-06-30', 'tax_deductible': '0.00', 'total': '311.76', 'get_projects': '工资薪金所得', 'company': '博智时代科技（北京）有限公司'}, {'card_type': '居民身份证', 'id_card': '372924199601063012', 'tax_withheld': '0.00', 'remark': '', 'buckle_tax': '54.92', 'tax_payable': '54.92', 'original_value': '0.00', 'amount_deductible': '0.00', 'get_duty_free': '0.00', 'fill_refund': '54.92', 'buckle_number': '105.00', 'fund_risk': '0.00', 'date': '2017-08-02', 'others': '0.00', 'get_tax': '1599.24', 'tax_credit': '0.00', 'medical_risk': '85.04', 'name': '刘敬', 'unemployment_risk': '0.00', 'tax_rate': '10.0', 'tax_period': '2017-07-01 至 2017-07-31', 'old_age_risk': '226.72', 'get_projects_2': '正常工资薪金', 'income': '5411.00', 'deduction_money': '3500.00', 'interval': '2017-07-01 至 2017-07-31', 'tax_deductible': '0.00', 'total': '311.76', 'get_projects': '工资薪金所得', 'company': '博智时代科技（北京）有限公司'}, {'card_type': '居民身份证', 'id_card': '372924199601063012', 'tax_withheld': '0.00', 'remark': '', 'buckle_tax': '0.00', 'tax_payable': '0.00', 'original_value': '0.00', 'amount_deductible': '0.00', 'get_duty_free': '0.00', 'fill_refund': '0.00', 'buckle_number': '0.00', 'fund_risk': '0.00', 'date': '2017-09-05', 'others': '0.00', 'get_tax': '0.00', 'tax_credit': '0.00', 'medical_risk': '92.48', 'name': '刘敬', 'unemployment_risk': '0.00', 'tax_rate': '3.00', 'tax_period': '2017-08-01 至 2017-08-31', 'old_age_risk': '246.56', 'get_projects_2': '正常工资薪金', 'income': '3338.00', 'deduction_money': '3500.00', 'interval': '2017-08-01 至 2017-08-31', 'tax_deductible': '0.00', 'total': '339.04', 'get_projects': '工资薪金所得', 'company': '博智时代科技（北京）有限公司'}, {'card_type': '居民身份证', 'id_card': '372924199601063012', 'tax_withheld': '0.00', 'remark': '', 'buckle_tax': '0.00', 'tax_payable': '0.00', 'original_value': '0.00', 'amount_deductible': '0.00', 'get_duty_free': '0.00', 'fill_refund': '0.00', 'buckle_number': '0.00', 'fund_risk': '0.00', 'date': '2017-10-10', 'others': '0.00', 'get_tax': '0.00', 'tax_credit': '0.00', 'medical_risk': '92.48', 'name': '刘敬', 'unemployment_risk': '0.00', 'tax_rate': '3.00', 'tax_period': '2017-09-01 至 2017-09-30', 'old_age_risk': '246.56', 'get_projects_2': '正常工资薪金', 'income': '3238.04', 'deduction_money': '3500.00', 'interval': '2017-09-01 至 2017-09-30', 'tax_deductible': '0.00', 'total': '339.04', 'get_projects': '工资薪金所得', 'company': '博智时代科技（北京）有限公司'}]
        item = [{'company': '北京澳环科技有限公司', 'tax_rate': '——', 'fill_refund': '315.75', 'income': '8000.00', 'date': '——', 'get_projects': '工资薪金所得', 'tax_period': '2016-03-01 至 2016-03-31'}, {'tax_withheld': '0.00', 'name': '刘敬', 'tax_deductible': '0.00', 'buckle_tax': '40.74', 'interval': '2016-12-01 至 2016-12-31', 'buckle_number': '0.00', 'get_projects_2': '正常工资薪金', 'tax_credit': '0.00', 'others': '0.00', 'original_value': '0.00', 'date': '2017-01-14', 'card_type': '居民身份证', 'id_card': '372924199601063012', 'tax_period': '2016-12-01 至 2016-12-31', 'unemployment_risk': '0.00', 'medical_risk': '0.00', 'tax_rate': '3.00', 'amount_deductible': '0.00', 'total': '0.00', 'tax_payable': '40.74', 'fund_risk': '0.00', 'company': '博智时代科技（北京）有限公司', 'get_projects': '工资薪金所得', 'fill_refund': '40.74', 'income': '4858.05', 'old_age_risk': '0.00', 'remark': '', 'get_tax': '1358.05', 'get_duty_free': '0.00', 'deduction_money': '3500.00'}, {'tax_withheld': '0.00', 'name': '刘敬', 'tax_deductible': '0.00', 'buckle_tax': '164.89', 'interval': '2017-01-01 至 2017-01-31', 'buckle_number': '105.00', 'get_projects_2': '正常工资薪金', 'tax_credit': '0.00', 'others': '0.00', 'original_value': '0.00', 'date': '2017-02-13', 'card_type': '居民身份证', 'id_card': '372924199601063012', 'tax_period': '2017-01-01 至 2017-01-31', 'unemployment_risk': '0.00', 'medical_risk': '0.00', 'tax_rate': '10.0', 'amount_deductible': '0.00', 'total': '0.00', 'tax_payable': '164.89', 'fund_risk': '0.00', 'company': '博智时代科技（北京）有限公司', 'get_projects': '工资薪金所得', 'fill_refund': '164.89', 'income': '6198.86', 'old_age_risk': '0.00', 'remark': '', 'get_tax': '2698.86', 'get_duty_free': '0.00', 'deduction_money': '3500.00'}, {'tax_withheld': '0.00', 'name': '刘敬', 'tax_deductible': '0.00', 'buckle_tax': '44.98', 'interval': '2017-02-01 至 2017-02-28', 'buckle_number': '0.00', 'get_projects_2': '正常工资薪金', 'tax_credit': '0.00', 'others': '0.00', 'original_value': '0.00', 'date': '2017-03-06', 'card_type': '居民身份证', 'id_card': '372924199601063012', 'tax_period': '2017-02-01 至 2017-02-28', 'unemployment_risk': '0.00', 'medical_risk': '0.00', 'tax_rate': '3.00', 'amount_deductible': '0.00', 'total': '0.00', 'tax_payable': '44.98', 'fund_risk': '0.00', 'company': '博智时代科技（北京）有限公司', 'get_projects': '工资薪金所得', 'fill_refund': '44.98', 'income': '4999.36', 'old_age_risk': '0.00', 'remark': '', 'get_tax': '1499.36', 'get_duty_free': '0.00', 'deduction_money': '3500.00'}, {'tax_withheld': '0.00', 'name': '刘敬', 'tax_deductible': '0.00', 'buckle_tax': '84.90', 'interval': '2017-03-01 至 2017-03-31', 'buckle_number': '105.00', 'get_projects_2': '正常工资薪金', 'tax_credit': '0.00', 'others': '0.00', 'original_value': '0.00', 'date': '2017-04-15', 'card_type': '居民身份证', 'id_card': '372924199601063012', 'tax_period': '2017-03-01 至 2017-03-31', 'unemployment_risk': '0.00', 'medical_risk': '0.00', 'tax_rate': '10.0', 'amount_deductible': '0.00', 'total': '0.00', 'tax_payable': '84.90', 'fund_risk': '0.00', 'company': '博智时代科技（北京）有限公司', 'get_projects': '工资薪金所得', 'fill_refund': '84.90', 'income': '5399.00', 'old_age_risk': '0.00', 'remark': '', 'get_tax': '1899.00', 'get_duty_free': '0.00', 'deduction_money': '3500.00'}, {'tax_withheld': '0.00', 'name': '刘敬', 'tax_deductible': '0.00', 'buckle_tax': '164.92', 'interval': '2017-04-01 至 2017-04-30', 'buckle_number': '105.00', 'get_projects_2': '正常工资薪金', 'tax_credit': '0.00', 'others': '0.00', 'original_value': '0.00', 'date': '2017-05-05', 'card_type': '居民身份证', 'id_card': '372924199601063012', 'tax_period': '2017-04-01 至 2017-04-30', 'unemployment_risk': '85.04', 'medical_risk': '0.00', 'tax_rate': '10.0', 'amount_deductible': '0.00', 'total': '311.76', 'tax_payable': '164.92', 'fund_risk': '0.00', 'company': '博智时代科技（北京）有限公司', 'get_projects': '工资薪金所得', 'fill_refund': '164.92', 'income': '6510.94', 'old_age_risk': '226.72', 'remark': '', 'get_tax': '2699.18', 'get_duty_free': '0.00', 'deduction_money': '3500.00'}, {'tax_withheld': '0.00', 'name': '刘敬', 'tax_deductible': '0.00', 'buckle_tax': '254.92', 'interval': '2017-05-01 至 2017-05-31', 'buckle_number': '105.00', 'get_projects_2': '正常工资薪金', 'tax_credit': '0.00', 'others': '0.00', 'original_value': '0.00', 'date': '2017-06-05', 'card_type': '居民身份证', 'id_card': '372924199601063012', 'tax_period': '2017-05-01 至 2017-05-31', 'unemployment_risk': '0.00', 'medical_risk': '85.04', 'tax_rate': '10.0', 'amount_deductible': '0.00', 'total': '311.76', 'tax_payable': '254.92', 'fund_risk': '0.00', 'company': '博智时代科技（北京）有限公司', 'get_projects': '工资薪金所得', 'fill_refund': '254.92', 'income': '7411.00', 'old_age_risk': '226.72', 'remark': '', 'get_tax': '3599.24', 'get_duty_free': '0.00', 'deduction_money': '3500.00'}, {'tax_withheld': '0.00', 'name': '刘敬', 'tax_deductible': '0.00', 'buckle_tax': '54.92', 'interval': '2017-06-01 至 2017-06-30', 'buckle_number': '105.00', 'get_projects_2': '正常工资薪金', 'tax_credit': '0.00', 'others': '0.00', 'original_value': '0.00', 'date': '2017-07-07', 'card_type': '居民身份证', 'id_card': '372924199601063012', 'tax_period': '2017-06-01 至 2017-06-30', 'unemployment_risk': '0.00', 'medical_risk': '85.04', 'tax_rate': '10.0', 'amount_deductible': '0.00', 'total': '311.76', 'tax_payable': '54.92', 'fund_risk': '0.00', 'company': '博智时代科技（北京）有限公司', 'get_projects': '工资薪金所得', 'fill_refund': '54.92', 'income': '5411.00', 'old_age_risk': '226.72', 'remark': '', 'get_tax': '1599.24', 'get_duty_free': '0.00', 'deduction_money': '3500.00'}, {'tax_withheld': '0.00', 'name': '刘敬', 'tax_deductible': '0.00', 'buckle_tax': '54.92', 'interval': '2017-07-01 至 2017-07-31', 'buckle_number': '105.00', 'get_projects_2': '正常工资薪金', 'tax_credit': '0.00', 'others': '0.00', 'original_value': '0.00', 'date': '2017-08-02', 'card_type': '居民身份证', 'id_card': '372924199601063012', 'tax_period': '2017-07-01 至 2017-07-31', 'unemployment_risk': '0.00', 'medical_risk': '85.04', 'tax_rate': '10.0', 'amount_deductible': '0.00', 'total': '311.76', 'tax_payable': '54.92', 'fund_risk': '0.00', 'company': '博智时代科技（北京）有限公司', 'get_projects': '工资薪金所得', 'fill_refund': '54.92', 'income': '5411.00', 'old_age_risk': '226.72', 'remark': '', 'get_tax': '1599.24', 'get_duty_free': '0.00', 'deduction_money': '3500.00'}, {'tax_withheld': '0.00', 'name': '刘敬', 'tax_deductible': '0.00', 'buckle_tax': '0.00', 'interval': '2017-08-01 至 2017-08-31', 'buckle_number': '0.00', 'get_projects_2': '正常工资薪金', 'tax_credit': '0.00', 'others': '0.00', 'original_value': '0.00', 'date': '2017-09-05', 'card_type': '居民身份证', 'id_card': '372924199601063012', 'tax_period': '2017-08-01 至 2017-08-31', 'unemployment_risk': '0.00', 'medical_risk': '92.48', 'tax_rate': '3.00', 'amount_deductible': '0.00', 'total': '339.04', 'tax_payable': '0.00', 'fund_risk': '0.00', 'company': '博智时代科技（北京）有限公司', 'get_projects': '工资薪金所得', 'fill_refund': '0.00', 'income': '3338.00', 'old_age_risk': '246.56', 'remark': '', 'get_tax': '0.00', 'get_duty_free': '0.00', 'deduction_money': '3500.00'}, {'tax_withheld': '0.00', 'name': '刘敬', 'tax_deductible': '0.00', 'buckle_tax': '0.00', 'interval': '2017-09-01 至 2017-09-30', 'buckle_number': '0.00', 'get_projects_2': '正常工资薪金', 'tax_credit': '0.00', 'others': '0.00', 'original_value': '0.00', 'date': '2017-10-10', 'card_type': '居民身份证', 'id_card': '372924199601063012', 'tax_period': '2017-09-01 至 2017-09-30', 'unemployment_risk': '0.00', 'medical_risk': '92.48', 'tax_rate': '3.00', 'amount_deductible': '0.00', 'total': '339.04', 'tax_payable': '0.00', 'fund_risk': '0.00', 'company': '博智时代科技（北京）有限公司', 'get_projects': '工资薪金所得', 'fill_refund': '0.00', 'income': '3238.04', 'old_age_risk': '246.56', 'remark': '', 'get_tax': '0.00', 'get_duty_free': '0.00', 'deduction_money': '3500.00'}]

        return info, item

    # base 基础
    def save_history(self, id, item, operation_mysql):
        '''
        根据关联id 查询个税历史表信息 去重存入新的信息
        :param id:
        :param item:
        :param operation_mysql:
        :return:
        '''
        tax_history = operation_mysql.check_mysql('personaltax_list', where='Userid="%s"' % id)
        # 5 去重,存入数据
        for info_dict in item:
            # 没存储时：
            if not [i for i in tax_history if info_dict['date'] in i]:
                data = {
                    "Userid": id,  # 关联用户ID
                    "Pay_time": info_dict['date'],  # 缴纳时间
                    "Tax_type": info_dict['get_projects'],  # 纳税项目
                    # "Taxable_income": info_dict[''],  # 纳税所得
                    "Income_money": info_dict['income'],  # 收入额
                    "Withhold_taxable": info_dict['fill_refund'],  # 实际扣缴所得税
                    "Owned_company": info_dict['company'],  # 纳税义务人
                }
                if info_dict['tax_rate'] != '——':
                    data["Tax_rate"] = info_dict['tax_rate']  # 税率

                operation_mysql.insert_sql(data, 'personaltax_list')


    # 自动
    def automatic(self):
        operation_mysql = OperationMysql()
        # 1、获取所有的账号密码
        tax_list = operation_mysql.check_mysql('personaltax_info', 'card_type, card, Username, password')
        login_list = list(set(tax_list))

        # 2、抓取信息
        for account_type, account, name, password in login_list:
            # self.get_cookie_urls()
            # info, item = self.get_history()
            info, item = self.pseudo_data()  # 假数据

            # 3、查询数据库
            id_list = operation_mysql.check_mysql('personaltax_info', 'id',
                                                  where='card_type="%s" and card="%s" and Username="%s" and password="%s"' % (account_type, account, name, password))
            # 4、查询历史信息
            for id in id_list:
                id = id[0]
                self.save_history(id, item, operation_mysql)

    # 第二次
    def second(self, id):
        id = str(id)
        operation_mysql = OperationMysql()
        account_type, account, name, password = operation_mysql.check_mysql('personaltax_info', 'card_type, card, Username, password',
                                              where='id="%s"' % id)[0]
        # self.get_cookie_urls()
        # info, item = self.get_history()
        info, item = self.pseudo_data()  # 假数据
        print(account_type, account, name, password, id)
        self.save_history(id, item, operation_mysql)
        return 1

# def first(id):
#     id = str(id)
#     operation_mysql = OperationMysql()
def bjgs_one(id_card, password, name, id_card_type='201', user_id=None):
    try:
        bjgs = Bjgs(id_card, password, name, id_card_type)
        status = bjgs.first(user_id)
    except Exception as e:
        inner = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        inner += ' 账号:' + str(id_card) + ' 密码:' + str(password) + ' 类型:' + str(id_card_type) + ' 注册用户id:' + str(user_id) + '姓名:' + str(name)
        inner += ' 错误:' + str(e) + '\n'
        with open('bjgs_error_log.txt', 'a')as f:
            f.write(inner)
        status = 0
    return status

def bjgs_two(gs_id):
    try:
        bjgs = Bjgs(gs_id)
        status = bjgs.second(gs_id)
    except Exception as e:
        inner = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        inner += ' 个税id:' + str(gs_id)
        inner += ' 错误:' + str(e) + '\n'
        with open('bjgs_error_log.txt', 'a')as f:
            f.write(inner)
        status = 0
    return status



