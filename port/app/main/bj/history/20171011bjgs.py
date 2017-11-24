# coding:utf-8
import requests
from lxml import etree
import pymysql
from rk import code_zy
from selenium import webdriver
import time
from bjdb import *
# 个税
class Bjgs():
    def __init__(self, user_id, password, name):
        self.zzhm = user_id
        self.password = password
        self.xm = name
        self.cookie = ''
        self.ssion = None
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
        with open('code.jpg', 'wb') as f:
            f.write(img_code.content)

        code = input('请输入验证码')

        #
        # code = code_zy(img_code.content)
        # print(code)

        # 登陆
        data = {
            'zjlx': '201',
            'zzhm': self.zzhm,
            'xm': self.xm,
            'password': self.password,
            'yzm': code
        }
        log_url = 'https://gt3app9.tax861.gov.cn/Gt3GsWeb/gsmxwyNo/YhdlAction.action?code=login'
        response = self.ssion.post(log_url, headers=headers, data=data, verify=False)
        # self.ssion.get('https://gt3app9.tax861.gov.cn/Gt3GsWeb/gsmxwyNo/css/head.css', headers=headers, verify=False)
        # self.ssion.get('https://gt3app9.tax861.gov.cn/Gt3GsWeb/gsmxwyNo/css/yhdlcss.css', headers=headers, verify=False)
        # self.ssion.get('https://gt3app9.tax861.gov.cn/Gt3GsWeb/gsmxwy/grsbxxcx/js/qrcode.js', headers=headers, verify=False)
        # self.ssion.get('https://gt3app9.tax861.gov.cn/Gt3GsWeb/gsmxwy/grsbxxcx/js/jquery-1.8.3.js', headers=headers, verify=False)
        # self.ssion.get('', headers=headers, verify=False)
        # cookiejar = response.cookies
        # cookiedict = requests.utils.dict_from_cookiejar(cookiejar)
        # for key, value in cookiedict.items():
        #     print(key + '=' + value)

        return 1

    def get_history(self):
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
            # 'Cookie' : 'JSESSIONID=BF176C2D95FB806AB237616C8923866B; _gscu_825391512=06599433kcses486; _gscs_825391512=06599433gc5ecp86|pv:1; _gscbrs_825391512=1; _gscs_163945954=06599433dosivj86|pv:1; _gscbrs_163945954=1; _gscu_163945954=06599433mkqdrb86',
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

        # self.ssion.post(url, headers=headers, data=data, verify=False)
        # import time
        # time.sleep(4)
        response = self.ssion.post(url, headers=headers, data=data, verify=False)

        html = etree.HTML(response.text)

        # 个人信息
        info_list = html.xpath('//table//input/@value')
        info = {}
        info['name'] = info_list[0]  # 姓名
        info['area'] = info_list[1]  # 国籍（地区）
        info['card_type'] = info_list[2]  # 身份证件类型
        info['id_card'] = info_list[3]  # 身份证件号码

        # with open('cs.html', 'wb')as f:
        #     f.write(response.content)

        # 个税税信息
        inner_lxml = html.xpath('//table[3]')[0]
        item_list = inner_lxml.xpath('.//td/text()')
        try:
            item = {}
            item['projects'] = item_list[-12]  # 所得项目
            item['income'] = item_list[-10]  # 收入额
            item['rate'] = item_list[-9].strip()  # 税率
            item['tax'] = item_list[-8]  # 应补（退）税额
            item['time'] = item_list[-7]  # 申报日期
            item['obligation'] = item_list[-6]  # 扣缴义务人名称
        except:
            item={}

        return info, item



    def save_mysql_individual(self, info, item):

        UserID = '1'  # 用户ID
        Username = info['name']  # 用户姓名
        Sex = '1' if int(info['id_card'][-2])//2==0 else '2'  # 1代表男，2代表女
        Card_number = info['id_card']  # 身份证号
        Recently_paid = format(float(item['income'])/100 * float(item['rate']), '.2f')  # 最近缴纳
        Monthly_deposit = item['tax']  # 月缴存额
        owned_company = item['obligation']  # 所属单位

        sql = "insert into personaltax_info(UserID, Username, Sex, Card_number, Recently_paid, Monthly_deposit, owned_company)" \
              " values('%s', '%s', '%s', '%s', '%s', '%s', '%s');" \
              % (
                  UserID, Username, Sex, Card_number, Recently_paid, Monthly_deposit, owned_company,
              )
        employee = self.cur.execute(sql)
        self.conn.commit()


    def save_mysql_history(self, info, item):
        Userid = '1'  # 关联用户ID
        Pay_time = item['time']  # 缴纳时间
        Tax_type = item['projects']  # 纳税项目
        Tax_rate = item['rate']  # 税率
        Taxable_income = format(float(item['income']) - float(item['income'])/100 * float(item['rate']), '.2f')  # 纳税所得
        Income_money = item['income']  # 收入额
        Withhold_taxable = format(float(item['income']) - float(item['income'])/100 * float(item['rate']) + item['tax'], '.2f')  # 实际扣缴所得税
        Owned_company = item['obligation']  # 纳税义务人

        sql = "insert into personaltax_list(Userid, Pay_time, Tax_type, Tax_rate, Taxable_income, Income_money, Withhold_taxable, Owned_company)" \
              " values('%s','%s','%s','%s','%s','%s','%s','%s');" \
              % (Userid, Pay_time, Tax_type, Tax_rate, Taxable_income, Income_money, Withhold_taxable, Owned_company)
        print(sql)
        employee = self.cur.execute(sql)
        self.conn.commit()


    def start(self):
        # 获取cookie
        self.get_cookie_urls()

        # 个人基本信息查询， 返回数据
        info, item = self.get_history()
        print(item)
        print(info)


        # 存入
        bjgs_db = BjgsDb()
        bjgs_db.start()

    def close(self):

        # 关闭myslq
        self.cur.close()
        self.conn.close()


if __name__ == '__main__':
    bjgs = Bjgs('372924199601063012', 'liu123456', '刘敬')
    # bjrbj = Bjrbj('110107197906121210', 'cuipeng6120')
    bjgs.start()

    #bjrbj.close()

