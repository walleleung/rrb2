# coding:utf-8
import requests
from lxml import etree
import pymysql
from rk import code_zy
from selenium import webdriver

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
        self.ssion.get('https://gt3app9.tax861.gov.cn/Gt3GsWeb/gsmxwyNo/css/head.css', headers=headers, verify=False)
        self.ssion.get('https://gt3app9.tax861.gov.cn/Gt3GsWeb/gsmxwyNo/css/yhdlcss.css', headers=headers, verify=False)
        self.ssion.get('https://gt3app9.tax861.gov.cn/Gt3GsWeb/gsmxwy/grsbxxcx/js/qrcode.js', headers=headers, verify=False)
        self.ssion.get('https://gt3app9.tax861.gov.cn/Gt3GsWeb/gsmxwy/grsbxxcx/js/jquery-1.8.3.js', headers=headers, verify=False)
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
            'skssksrqN': '2010',
            'skssksrqY': '1',
            'skssjsrqN': '2017',
            'skssjsrqY': '10'
        }

        # self.ssion.post(url, headers=headers, data=data, verify=False)
        import time
        time.sleep(4)
        response = self.ssion.post(url, headers=headers, data=data, verify=False)

        html = etree.HTML(response.text)
        # inner_lxml = html.xpath('//table[3]')[0]

        inner_lxml_list = html.xpath('//table[3]')

        inner_list = []
        for inner_lxml in inner_lxml_list:
            inner = inner_lxml.xpath('.//td/text()')
            inner_list.append(inner)

        item = inner_list

        with open('cs.html', 'wb')as f:
            f.write(response.content)

        return item



    def save_mysql_individual(self, item):

        name = item['name']
        idcard = item['idcard']
        sex = item['sex']
        born_day = item['born_day']
        peoples = item['peoples']
        country = item['country']
        individual_identity = item['individual_identity']
        work_dates = item['work_dates']
        city = item['city']
        city_addr = item['city_addr']
        city_code = item['city_code']
        live_addr = item['live_addr']
        live_code = item['live_code']
        culture = item['culture']
        applicant_phone = item['applicant_phone']
        applicant_tel = item['applicant_tel']
        months_revenue = item['months_revenue']
        Banks = item['Banks']
        banks_code = item['banks_code']

        sql = "insert into bjrbj_individual_info(name, idcard, sex, born_day, peoples, country, individual_identity, work_dates, city, city_addr, city_code, live_addr, live_code, culture, applicant_phone, applicant_tel, months_revenue, Banks, banks_code)" \
              " values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" \
              % (name, idcard, sex, born_day, peoples, country, individual_identity, work_dates, city, city_addr, city_code, live_addr, live_code, culture, applicant_phone, applicant_tel, months_revenue, Banks, banks_code)
        employee = self.cur.execute(sql)
        self.conn.commit()


    def save_mysql_history(self, item):
        oldage = item['oldage']
        unemployment = item['unemployment']
        injuries = item['injuries']
        maternity = item['maternity']
        medicalcare = item['medicalcare']

        insurance_list = [oldage, unemployment, injuries, maternity, medicalcare]
        name_list = ['oldage', 'unemployment', 'injuries', 'maternity', 'medicalcare']

        for index, insurance_name in enumerate(insurance_list):
            for insurance_year in insurance_name:
                for insurance_day in insurance_year:
                    if len(str(insurance_day[-1])) > 1:
                        sql = "insert into bjrbj_%s_info(a,b,c)" \
                              " values('%s','%s','%s');" \
                              % (name_list[index],insurance_day[0], insurance_day[1], insurance_day[2])
                        employee = self.cur.execute(sql)
                        self.conn.commit()



    def start(self):
        # 获取cookie
        self.get_cookie_urls()



        # 个人基本信息查询， 返回数据
        item = self.get_history()
        print(item)


        # self.save_mysql_individual(item)

        # self.save_mysql_history(item)

    def close(self):

        # 关闭myslq
        self.cur.close()
        self.conn.close()


if __name__ == '__main__':
    bjgs = Bjgs('372924199601063012', 'liu123456', '刘敬')
    # bjrbj = Bjrbj('110107197906121210', 'cuipeng6120')
    bjgs.start()

    #bjrbj.close()

