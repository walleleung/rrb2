#coding=utf-8
from PIL import Image
import requests
from lxml import etree
from selenium import webdriver
import time
import re
import pymysql
import subprocess
from rk import code_zy
from bjdb import OperationMysql

'''
1、获取社保账号密码
2、使用selenium登录（1、验证码处理 2、登录 3、判断是否登录成功）
3、获取首页的网址
4、获取登录后的cookie
5、使用cookie访问详细信息网址
6、提取信息保存成字典
7、存入数据库
'''
# 公积金
class Bjrbj():
    def __init__(self, user, password):
        '''
        获取登录需要的参数
        :param user: 身份证号
        :param password: 查询密码
        '''
        self.user = user
        self.password = password
        self.cookie = ''
        self.headers = None

        #self.conn = pymysql.connect(host='127.0.0.1', user='root', password='mysql', db='bjgjj', charset="utf8")
        #self.cur = self.conn.cursor()

    def get_cookie_urls(self):
        '''
        使用selenium + PhantomJS 登录， 获取cookie值， 和首页的需要的url
        :return:
        '''


        url = 'http://www.bjrbj.gov.cn/csibiz/indinfo/login.jsp'  # 北京市社会保险网上服务

        # 调用
        driver = webdriver.PhantomJS()
        driver.get(url)



        # 验证码截图
        driver.save_screenshot("bj.png")
        element = driver.find_element_by_id('indsafecode')
        left = element.location['x']
        top = element.location['y']
        right = element.location['x'] + element.size['width']
        bottom = element.location['y'] + element.size['height']
        im = Image.open('bj.png')
        im = im.crop((left, top, right, bottom))
        im.save('code.png')

        # 识别验证码
        self.code_img('code.png', 'code.png')
        self.code_img('code.png', 'code.png')
        subprocess.call(["tesseract", './code.png', "output"])
        with open("output.txt", 'r') as f:
            code = f.read()
            code = code.strip()
        with open('s.txt', 'w')as f:
            f.write(code)
        with open('s.txt', 'r')as f:
            code = f.read()
        time.sleep(3)

        print(code)
        code = input('验证码：')

        # code = code_zy(img_code.content)




        # 输入账号密码验证码
        driver.find_element_by_id("i_username").send_keys(self.user)
        driver.find_element_by_id("i_password").send_keys(self.password)
        driver.find_element_by_id('i_safecode').send_keys(code)

        # 点击发送手机验证码
        driver.find_element_by_id("shoujiyanzhengma").click()

        # alert = driver.switch_to_alert()
        # driver.switch_to.alert
        # print (alert)
        # alert.accept()
        # alert.dismiss()

        tel_code = input('请求输入手机验证码：')
        driver.find_element_by_name("i_phone").send_keys(tel_code)

        driver.save_screenshot("bj.png")  # 测试截图
        driver.find_element_by_xpath('//*[@id="indform"]/div[5]/input').click()  # 按钮　登录
        # driver.find_element_by_xpath('//*[@id="indform"]/div[5]/a').click()  # 测试　注册按钮
        driver.save_screenshot("bj2.png")  # 测试截图



        '''
        # 判断是否登录成功
        for i in range(20):
            try:
                driver.find_element_by_xpath('//*[@id="new-mytable"]/tbody/tr[1]/th[2]/div/text()')
                break
            except:
                time.sleep(0.1)
        try:
            driver.find_element_by_xpath('//*[@id="new-mytable"]/tbody/tr[1]/th[2]/div/text()')
        except:
            return 0
        '''


        # 获取cookie
        cookie_list = driver.get_cookies()
        for cookie_dict in cookie_list:
            self.cookie += cookie_dict['name'] + '=' + cookie_dict['value'] + ';'  # 拼接cookie

        print(self.cookie)  # cs
        # self.cookie = '_gscu_2065735475=065768600hh12z10;_gscbrs_2065735475=1;_gscs_2065735475=07612985v2ec6d10|pv:1;mjrzMBJgZO=MDAwM2IyYWYyZjQwMDAwMDAwMDgwPRgOFGsxNTA3NjM4MjEw;JSESSIONID=A9011EFACDCDC0D47DA0AF0827588CC7;'

        self.headers = {
            'Accept' : 'text/javascript, text/html, application/xml, text/xml, */*',
            'Accept-Encoding' : 'gzip, deflate',
            'Accept-Language' : 'zh-CN,zh;q=0.8',
            'Connection' : 'keep-alive',
            'Content-Length' : '0',
            'Content-type' : 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie' : self.cookie,
            'Host' : 'www.bjrbj.gov.cn',
            'Origin' : 'http://www.bjrbj.gov.cn',
            'Referer' : 'http://www.bjrbj.gov.cn/csibiz/indinfo/search/ind/ind_new_info_index.jsp',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'X-Prototype-Version' : '1.5.1.1',
            'X-Requested-With' : 'XMLHttpRequest',
        }
        # print(self.cookie)
        # print(self.headers)


        driver.quit()
        return 1

    def code_img(self, old_file, new_file):
        '''
        输入验证码图片， 输出黑白的验证码图片
        old_file: 文件路径
        new_file: 保存路径
        '''
        image = Image.open(old_file)
        image = image.point(lambda x: 0 if x < 143 else 255)
        pix = image.load()
        for x in range(0, image.size[0]):
            for y in range(0, image.size[1]):
                r, g, b, n = pix[x,y]
                if r<143 or g<143 or b<143:
                    pix[x,y] = (0, 0, 0, n)

        image.save(new_file)

    def get_code(self, driver):

        for i in range(10):
            driver.save_screenshot("bj.png")
            element = driver.find_element_by_id('indsafecode')
            left = element.location['x']
            top = element.location['y']
            right = element.location['x'] + element.size['width']
            bottom = element.location['y'] + element.size['height']
            im = Image.open('bj.png')
            im = im.crop((left, top, right, bottom))
            im.save('code.png')
            # 识别验证码
            self.code_img('code.png', 'code.png')
            self.code_img('code.png', 'code.png')
            subprocess.call(["tesseract", './code.png', "output"])
            with open("output.txt", 'r') as f:
                code = f.read()
                code = code.strip()
            with open('s.txt', 'w')as f:
                f.write(code)
            with open('s.txt', 'r')as f:
                code = f.read()
            if len(code) != 4:
                driver.find_element_by_id("indsafecode").click()
                break
            if code.isalnum():
                return code
            driver.find_element_by_id("indsafecode").click()


    def me_info(self, url):
        '''
        获取北京社保公司url， 返回页面里面的 个人数据
        :param url: 个人基本信息查询 url
        :return: 返回 字典格式的个人信息
        '''

        # 测试
        # print(self.headers)
        # print(self.cookie)

        # 发送请求
        response = requests.post(url, headers=self.headers)
        html = etree.HTML(response.text)

        # 提取大概标签
        info_list = html.xpath('//tr/td')

        # 测试打印所有td的内容加上下标
        # n = 0
        # for info in info_list:
        #     print(n, ':', info.xpath('./text()'))
        #     n += 1

        with open('cs.html', 'wb')as f:
            f.write(response.content)

        print(info_list[0].xpath('./text()')[0])
        # 提取信息存入item
        item = {}

        info_head = re.findall(r'[\u4E00-\u9FA5()]+|\d+', info_list[0].xpath('./text()')[0])
        print(info_head)
        item['unit'] = info_head[1]  # 单位名称
        item['organization_code'] = info_head[4]  # 组织机构代码
        item['insurance_number'] = info_head[6]  # 社会保险登记证编号
        item['address'] = info_head[8]  # 所属区县


        # item['have_insurance'] = info_list[2].xpath('./text()')[0] if info_list[2].xpath(
            # './text()') else ''  # 参加险种  （列表格式没有处理）
        item['name'] = info_list[5].xpath('./text()')[0] if info_list[5].xpath('./text()') else ''  # 姓名
        item['idcard'] = info_list[7].xpath('./text()')[0] if info_list[7].xpath('./text()') else ''  # 公民身份证号码
        item['sex'] = info_list[9].xpath('./text()')[0] if info_list[9].xpath('./text()') else ''  # 性别
        item['born_day'] = info_list[11].xpath('./text()')[0] if info_list[11].xpath('./text()') else ''  # 出生日期
        item['peoples'] = info_list[13].xpath('./text()')[0] if info_list[13].xpath('./text()') else ''  # 民族
        item['country'] = info_list[15].xpath('./text()')[0] if info_list[15].xpath('./text()') else ''  # 国家/地区
        item['individual_identity'] = info_list[17].xpath('./text()')[0] if info_list[17].xpath(
            './text()') else ''  # 个人身份
        item['work_dates'] = info_list[19].xpath('./text()')[0] if info_list[19].xpath('./text()') else ''  # 参加工作日期
        item['city'] = info_list[23].xpath('./text()')[0] if info_list[23].xpath('./text()') else ''  # 户口性质
        item['city_addr'] = info_list[25].xpath('./text()')[0] if info_list[25].xpath('./text()') else ''  # 户口所在地地址
        item['city_code'] = info_list[27].xpath('./text()')[0] if info_list[27].xpath('./text()') else ''  # 户口所在地邮政编码
        item['live_addr'] = info_list[29].xpath('./text()')[0] if info_list[29].xpath('./text()') else ''  # 居住地（联系）地址
        item['live_code'] = info_list[31].xpath('./text()')[0] if info_list[31].xpath('./text()') else ''  # 居住地（联系）邮政编码
        item['culture'] = info_list[40].xpath('./text()')[0] if info_list[40].xpath('./text()') else ''  # 文化程度
        item['applicant_phone'] = info_list[43].xpath('./text()')[0] if info_list[43].xpath('./text()') else ''  # 参保人电话
        item['applicant_tel'] = info_list[45].xpath('./text()')[0] if info_list[45].xpath('./text()') else ''  # 参保人手机
        item['months_revenue'] = info_list[47].xpath('./text()')[0] if info_list[47].xpath(
            './text()') else ''  # 申报月均工资收入（元）
        item['pay_people_type'] = (info_list[57].xpath('./text()')[0] if info_list[65].xpath('./text()') else '')  # 缴纳人员类别
        item['hospital1'] = (info_list[65].xpath('./text()')[0] if info_list[65].xpath('./text()') else '')  # 医院1
        item['hospital2'] = (info_list[67].xpath('./text()')[0] if info_list[47].xpath('./text()') else '')  # 医院2
        item['hospital3'] = (info_list[69].xpath('./text()')[0] if info_list[69].xpath('./text()') else '')  # 医院3
        item['hospital4'] = (info_list[71].xpath('./text()')[0] if info_list[71].xpath('./text()') else '')  # 医院4
        item['hospital5'] = (info_list[73].xpath('./text()')[0] if info_list[73].xpath('./text()') else '')  # 医院5

        item['Banks'] = info_list[53].xpath('./text()')[0] if info_list[53].xpath('./text()') else ''  # 委托代发银行名称
        item['banks_code'] = info_list[55].xpath('./text()')[0] if info_list[55].xpath('./text()') else ''  # 银行账号
        # print(item)

        return item

    def get_history(self, url):
        '''
        获取历史记录url 历史记录信息
        :param url:  历史url
        :return:  type = [{}, {}]  返回当页历史记录
        '''
        # url = 'http://www.bjrbj.gov.cn/csibiz/indinfo/search/ind/indPaySearchAction!oldage?searchYear=2016'
        response = requests.post(url, headers=self.headers)
        # with open('cs.html', 'wb') as f:
        #     f.write(response.content)
        html = etree.HTML(response.text)
        tr_lxml = html.xpath('//tr')

        # 测试
        # print('---')
        # for tr in tr_lxml[2:]:
        #     print(tr.xpath('./td/text()'))

        # 提取字段
        item = []
        for tr in tr_lxml[2:-1]:
            year = tr.xpath('./td/text()')
            item.append(year)

        # print(item)

        return item

    def get_history_many(self, few_year):
        '''
        需要查询最新几年的数据， 返回列表形式的数据
        :param few_year: 查询最近几年的数据   类型 int
        :return:  返回列表形式的数据 {养老：[], 失业:[], ...}
        '''
        url_1 = 'http://www.bjrbj.gov.cn/csibiz/indinfo/search/ind/indPaySearchAction!oldage?searchYear='  # 养老
        url_2 = 'http://www.bjrbj.gov.cn/csibiz/indinfo/search/ind/indPaySearchAction!unemployment?searchYear='  # 失业
        url_3 = 'http://www.bjrbj.gov.cn/csibiz/indinfo/search/ind/indPaySearchAction!injuries?searchYear='  # 工伤
        url_4 = 'http://www.bjrbj.gov.cn/csibiz/indinfo/search/ind/indPaySearchAction!maternity?searchYear='  # 生育
        url_5 = 'http://www.bjrbj.gov.cn/csibiz/indinfo/search/ind/indPaySearchAction!medicalcare?searchYear='  # 医疗
        name_list = ['oldage', 'unemployment', 'injuries', 'maternity', 'medicalcare']
        toyear = int(time.strftime('%Y',time.localtime(time.time())))
        history_dict = {}

        for index, url_base in enumerate([url_1, url_2, url_3, url_4, url_5]):
            item = []
            for year in range(toyear, toyear-few_year, -1):
                url = url_base + str(year)
                item.append(self.get_history(url))
            history_dict[name_list[index]] = item


        return history_dict

    def get_card_state(self):
        '''
        对社保卡办理状态查询， 流程环节名称
        :return:返回所有状态  类型：list    例：[[''], [''], ['', '']]
        '''

        item_list = []
        url = 'http://www.bjrbj.gov.cn/csibiz/indinfo/cardstatus/ind/indCardStatusAction!getCardStatus'
        response = requests.get(url, headers=self.headers)
        html = etree.HTML(response.text)
        state_lxml_list = html.xpath('//*[@id="page"]/div[5]/div/dl')
        for state_lxml in state_lxml_list:
            state = state_lxml.xpath('./dt/text()') + state_lxml.xpath('./dd/text()')
            item_list.append(state)
        # print(item_list)
        return item_list

    def save_mysql_individual(self, item, history_dict, state_list):
        '''
        存入数据库
        :param item:个人信息字段
        :param history_dict: 五险缴费历史信息
        :param state_list: 办卡状态
        :return:
        '''
        data = {}
        # data['Id'] = item['']  # 自增id
        # data['userid'] = item['']  # 关联user用户id
        data['name'] = item['name']  # 社保用户名
        data['House_type'] = item['city']  # 户口类型
        # data['Total_paymonth'] = item['']  # 累计缴纳
        data['Card_number'] = item['idcard']  # 身份证号
        data['Social_number'] = item['insurance_number']  # 社保编号
        data['Phone'] = item['applicant_phone']  # 联系电话
        data['Payment_type'] = 1 if item['pay_people_type'] == '外埠城镇职工' else 0  # 缴费人员类别
        data['Income_wages'] = item['months_revenue']  # 申报月工资收入
        data['owned_company'] = item['unit']  # 所属公司
        data['Insured_area'] = item['address']  # 参保区域
        data['Hospital1'] = item['hospital1']  # 定点医院1
        data['Hospital2'] = item['hospital2']  # 定点医院2
        data['Hospital3'] = item['hospital3']  # 定点医院3
        data['Hospital4'] = item['hospital4']  # 定点医院4
        data['Hospital5'] = item['hospital5']  # 定点医院5
        # data['Insured_status'] = item['']  # 参保状态
        # data['Recently_paid'] = item['']  # 最近缴纳
        # data['medicalcare_status'] = item['']  # 医疗保险缴纳情况
        # data['endowment_status'] = item['']  # 养老保险缴纳情况
        # data['unemployment_status'] = item['']  # 失业保险缴纳情
        # data['business_status'] = item['']  # 工商保险缴纳情况
        # data['maternity_status'] = item['']  # 生育保险缴纳情况
        data['Card_progress'] = len(state_list)  # 制卡进度字段（1，2，3..代表制卡的进度）
        # data['Update_time'] = item['']  # 更新时间
        # data['Create_time'] = item['']  # 创建时间

        print(data)
        db = OperationMysql(host='127.0.0.1', user='root', password='mysql', db='bj')
        tables = 'SocialSecurity_info'
        db.insert_sql(data, tables)

    def save_mysql_history(self, item, history_dict, state_list):

        oldage = history_dict['oldage']  # 养老
        unemployment = history_dict['unemployment']  # 失业
        injuries = history_dict['injuries']  # 工伤
        maternity = history_dict['maternity']  # 生育
        medicalcare = history_dict['medicalcare']  # 医保


        history = {}

        for history in [oldage, unemployment, injuries, maternity, medicalcare]:
            history = self.take_new_risk(history)
            data = {}
            # data['Userid'] = history['']  # 关联用户表userid
            data['deposit_time'] = history[0]  # 缴存时间
            if len(history) == 3:
                data['companypay_money'] = history[2]  # 单位缴纳数额
                data['basemoney'] = history[1]  # 缴纳基数
                # data['Owned_company'] = history['']  # 缴办单位
            if len(history) == 4:
                data['companypay_money'] = history[2]  # 单位缴纳数额
                data['Individualspay_money'] = history[3]  # 个人缴纳数额
                data['basemoney'] = history[1]  # 缴纳基数
                # data['Owned_company'] = history['']  # 缴办单位
            if len(history) == 6:
                data['companypay_money'] = history[3].strip()  # 单位缴纳数额
                data['Individualspay_money'] = history[4].strip()  # 个人缴纳数额
                data['basemoney'] = history[2].strip()  # 缴纳基数
                data['Owned_company'] = history[5].strip()  # 缴办单位


            # data['Update_time'] = history['']  # 数据更新时间
            # data['Create_time'] = history['']  # 创建时间
            # 分类需要添加
            # data['remark'] = history['']  # 注释

            print(data)
            db = OperationMysql(host='127.0.0.1', user='root', password='mysql', db='bj')
            tables = 'SocialSecurity_list'
            db.insert_sql(data, tables)


    def take_new_risk(self, risk_list):

        risk = []
        for i in range(len(risk_list[0]) - 1, -1, -1):
            if len(risk_list[0][i][-1]) > 2:
                risk = risk_list[0][i]
                break

        return risk


    # def save_mysql_individual(self, item):
    #
    #     name = item['name']
    #     idcard = item['idcard']
    #     sex = item['sex']
    #     born_day = item['born_day']
    #     peoples = item['peoples']
    #     country = item['country']
    #     individual_identity = item['individual_identity']
    #     work_dates = item['work_dates']
    #     city = item['city']
    #     city_addr = item['city_addr']
    #     city_code = item['city_code']
    #     live_addr = item['live_addr']
    #     live_code = item['live_code']
    #     culture = item['culture']
    #     applicant_phone = item['applicant_phone']
    #     applicant_tel = item['applicant_tel']
    #     months_revenue = item['months_revenue']
    #     Banks = item['Banks']
    #     banks_code = item['banks_code']
    #
    #     sql = "insert into bjrbj_individual_info(name, idcard, sex, born_day, peoples, country, individual_identity, work_dates, city, city_addr, city_code, live_addr, live_code, culture, applicant_phone, applicant_tel, months_revenue, Banks, banks_code)" \
    #           " values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" \
    #           % (name, idcard, sex, born_day, peoples, country, individual_identity, work_dates, city, city_addr, city_code, live_addr, live_code, culture, applicant_phone, applicant_tel, months_revenue, Banks, banks_code)
    #     employee = self.cur.execute(sql)
    #     self.conn.commit()
    #
    #
    # def save_mysql_insurance(self, item):
    #     oldage = item['oldage']
    #     unemployment = item['unemployment']
    #     injuries = item['injuries']
    #     maternity = item['maternity']
    #     medicalcare = item['medicalcare']
    #
    #     insurance_list = [oldage, unemployment, injuries, maternity, medicalcare]
    #     name_list = ['oldage', 'unemployment', 'injuries', 'maternity', 'medicalcare']
    #
    #     for index, insurance_name in enumerate(insurance_list):
    #         for insurance_year in insurance_name:
    #             for insurance_day in insurance_year:
    #                 if len(str(insurance_day[-1])) > 1:
    #                     sql = "insert into bjrbj_%s_info(a,b,c)" \
    #                           " values('%s','%s','%s');" \
    #                           % (name_list[index],insurance_day[0], insurance_day[1], insurance_day[2])
    #                     employee = self.cur.execute(sql)
    #                     self.conn.commit()
    #
    #
    # def save_mysql_card(self, item):
    #     print('存入状态表')
    #     table_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']
    #     data = ''
    #     n = 0
    #     for card_list in item:
    #         for card in card_list:
    #             data += ',' + '"' + card + '"'
    #             n+=1
    #     ','.join(table_list[:n])
    #     sql = "insert into bjrbj_card_info(%s)" \
    #           " values(%s);" \
    #           % (','.join(table_list[:n]), data[1:])
    #     print(sql)
    #     employee = self.cur.execute(sql)
    #     self.conn.commit()




    def cs(self):
        self.headers = {
            'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=37950C06189BE2822F43E6D149A9B745; _trs_uv=38cd_365_j8l134ia; mjrzMBJgZO=MDAwM2IyYWYyZjQwMDAwMDAwMDgwb0QUWHsxNTA3ODg2Nzkw; _gscs_2065735475=t07861585302e1n13|pv:5; _gscbrs_2065735475=1; _gscu_2065735475=06417242mcjo0j22',
            'Host': 'www.bjrbj.gov.cn',
            'Origin': 'http://www.bjrbj.gov.cn',
            'Referer': 'http://www.bjrbj.gov.cn/csibiz/indinfo/search/ind/ind_new_info_index.jsp',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'X-Prototype-Version': '1.5.1.1',
            'X-Requested-With': 'XMLHttpRequest',
        }

        item = {'organization_code': '80176897', 'city_code': '332000', 'months_revenue': '3000',
         'idcard': '360403199307261840', 'unit': '曼帕尔人力资源(北京)有限公司', 'applicant_phone': '18607925870',
         'city_addr': '九江市浔阳区', 'sex': '女', 'live_code': '332000', 'banks_code': ' 1170547388(医保)', 'city': '城镇（非农业户口）',
         'hospital3': '民航总医院 ', 'culture': '*文化程度', 'hospital1': '306医院 ', 'hospital2': '三零一医院 ',
         'individual_identity': '干部', 'country': '中国', 'hospital5': ' ', 'hospital4': '北京医院 ', 'peoples': '汉族',
         'live_addr': '九江市浔阳区', 'Banks': ' 北京银行（只限本市）(医保)', 'pay_people_type': '外埠城镇职工',
         'insurance_number': '110105041715', 'name': '马妮', 'work_dates': '20140911', 'applicant_tel': '18607925870',
         'born_day': '19930726  ', 'address': '朝阳区'}

        history_dict = {'unemployment': [[['2017-01', '2834', '22.67', '5.67'], ['2017-02', '2834', '22.67', '5.67'],
                           ['2017-03', '2834', '22.67', '5.67'], ['2017-04', '2834', '22.67', '5.67'],
                           ['2017-05', '2834', '22.67', '5.67'], ['2017-06', '2834', '22.67', '5.67'],
                           ['2017-07', '3082', '24.66', '6.16'], ['2017-08', '3082', '24.66', '6.16'],
                           ['2017-09', '-', '-', '-'], ['2017-10', '-', '-', '-'], ['2017-11', '-', '-', '-'],
                           ['2017-12', '-', '-', '-']],
                          [['2016-01', '2585', '25.85', '5.17'], ['2016-02', '2585', '25.85', '5.17'],
                           ['2016-03', '2585', '25.85', '5.17'], ['2016-04', '2585', '25.85', '5.17'],
                           ['2016-05', '2585', '20.68', '5.17'], ['2016-06', '2585', '20.68', '5.17'],
                           ['2016-07', '2834', '22.67', '5.67'], ['2016-08', '2834', '22.67', '5.67'],
                           ['2016-09', '2834', '22.67', '5.67'], ['2016-10', '2834', '22.67', '5.67'],
                           ['2016-11', '2834', '22.67', '5.67'], ['2016-12', '2834', '22.67', '5.67']]], 'oldage': [
            [['2017-01', '正常缴费', '2834', '538.46', '226.72', '曼帕尔人力资源(北京)有限公司'],
             ['2017-02', '正常缴费', '2834', '538.46', '226.72', '曼帕尔人力资源(北京)有限公司'],
             ['2017-03', '正常缴费', '2834', '538.46', '226.72', '曼帕尔人力资源(北京)有限公司'],
             ['2017-04', '正常缴费', '2834', '538.46', '226.72', '曼帕尔人力资源(北京)有限公司'],
             ['2017-05', '正常缴费', '2834', '538.46', '226.72', '曼帕尔人力资源(北京)有限公司'],
             ['2017-06', '正常缴费', '2834', '538.46', '226.72', '曼帕尔人力资源(北京)有限公司'],
             ['2017-07', '正常缴费', '3082', '585.58', '246.56', '北京上晋通途电力工程有限公司'],
             ['2017-08', '正常缴费', '3082', '585.58', '246.56', '北京上晋通途电力工程有限公司'], ['2017-09', '-', '-', '-', '-', '-'],
             ['2017-10', '-', '-', '-', '-', '-'], ['2017-11', '-', '-', '-', '-', '-'],
             ['2017-12', '-', '-', '-', '-', '-']], [['2016-01', '正常缴费', '2585', '517', '206.8', '曼帕尔人力资源(北京)有限公司'],
                                                     ['2016-02', '正常缴费', '2585', '517', '206.8', '曼帕尔人力资源(北京)有限公司'],
                                                     ['2016-03', '正常缴费', '2585', '517', '206.8', '曼帕尔人力资源(北京)有限公司'],
                                                     ['2016-04', '正常缴费', '2585', '517', '206.8', '曼帕尔人力资源(北京)有限公司'],
                                                     ['2016-05', '正常缴费', '2585', '491.15', '206.8', '曼帕尔人力资源(北京)有限公司'],
                                                     ['2016-06', '正常缴费', '2585', '491.15', '206.8', '曼帕尔人力资源(北京)有限公司'],
                                                     ['2016-07', '正常缴费', '2834', '538.46', '226.72', '曼帕尔人力资源(北京)有限公司'],
                                                     ['2016-08', '正常缴费', '2834', '538.46', '226.72', '曼帕尔人力资源(北京)有限公司'],
                                                     ['2016-09', '正常缴费', '2834', '538.46', '226.72', '曼帕尔人力资源(北京)有限公司'],
                                                     ['2016-10', '正常缴费', '2834', '538.46', '226.72', '曼帕尔人力资源(北京)有限公司'],
                                                     ['2016-11', '正常缴费', '2834', '538.46', '226.72', '北京永盛达通科技有限公司'],
                                                     ['2016-12', '正常缴费', '2834', '538.46', '226.72', '北京永盛达通科技有限公司']]],
         'injuries': [[['2017-01', '4252', '12.76'], ['2017-02', '4252', '12.76'], ['2017-03', '4252', '12.76'],
                       ['2017-04', '4252', '12.76'], ['2017-05', '4252', '12.76'], ['2017-06', '4252', '12.76'],
                       ['2017-07', '4624', '46.24'], ['2017-08', '4624', '46.24'], ['2017-09', '-', '-'],
                       ['2017-10', '-', '-'], ['2017-11', '-', '-'], ['2017-12', '-', '-']],
                      [['2016-01', '3878', '11.63'], ['2016-02', '3878', '11.63'], ['2016-03', '3878', '11.63'],
                       ['2016-04', '3878', '11.63'], ['2016-05', '3878', '11.63'], ['2016-06', '3878', '11.63'],
                       ['2016-07', '4252', '12.76'], ['2016-08', '4252', '12.76'], ['2016-09', '4252', '12.76'],
                       ['2016-10', '4252', '12.76'], ['2016-11', '4252', '17.01'], ['2016-12', '4252', '17.01']]],
         'maternity': [[['2017-01', '4252', '34.02'], ['2017-02', '4252', '34.02'], ['2017-03', '4252', '34.02'],
                        ['2017-04', '4252', '34.02'], ['2017-05', '4252', '34.02'], ['2017-06', '4252', '34.02'],
                        ['2017-07', '4624', '36.99'], ['2017-08', '4624', '36.99'], ['2017-09', '-', '-'],
                        ['2017-10', '-', '-'], ['2017-11', '-', '-'], ['2017-12', '-', '-']],
                       [['2016-01', '3878', '31.02'], ['2016-02', '3878', '31.02'], ['2016-03', '3878', '31.02'],
                        ['2016-04', '3878', '31.02'], ['2016-05', '3878', '31.02'], ['2016-06', '3878', '31.02'],
                        ['2016-07', '4252', '34.02'], ['2016-08', '4252', '34.02'], ['2016-09', '4252', '34.02'],
                        ['2016-10', '4252', '34.02'], ['2016-11', '4252', '34.02'], ['2016-12', '4252', '34.02']]],
         'medicalcare': [[['2017-01', '\r\n\t\t\t\t\r\n\t\t\t\t\t正常缴纳\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t4252.00\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t425.20\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t88.04\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t曼帕尔人力资源(北京)有限公司\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t'],
                          ['2017-02', '\r\n\t\t\t\t\r\n\t\t\t\t\t正常缴纳\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t4252.00\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t425.20\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t88.04\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t曼帕尔人力资源(北京)有限公司\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t'],
                          ['2017-03', '\r\n\t\t\t\t\r\n\t\t\t\t\t正常缴纳\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t4252.00\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t425.20\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t88.04\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t曼帕尔人力资源(北京)有限公司\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t'],
                          ['2017-04', '\r\n\t\t\t\t\r\n\t\t\t\t\t正常缴纳\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t4252.00\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t425.20\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t88.04\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t曼帕尔人力资源(北京)有限公司\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t'],
                          ['2017-05', '\r\n\t\t\t\t\r\n\t\t\t\t\t正常缴纳\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t4252.00\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t425.20\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t88.04\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t曼帕尔人力资源(北京)有限公司\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t'],
                          ['2017-06', '\r\n\t\t\t\t\r\n\t\t\t\t\t正常缴纳\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t4252.00\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t425.20\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t88.04\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t曼帕尔人力资源(北京)有限公司\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t'],
                          ['2017-07', '\r\n\t\t\t\t\r\n\t\t\t\t\t正常缴纳\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t4624.00\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t462.40\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t95.48\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t北京上晋通途电力工程有限公司\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t'],
                          ['2017-08', '\r\n\t\t\t\t\r\n\t\t\t\t\t正常缴纳\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t4624.00\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t462.40\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t95.48\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                           '\r\n\t\t\t\t\r\n\t\t\t\t\t北京上晋通途电力工程有限公司\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t'],
                          ['2017-09', '-', '-', '-', '-', '-'], ['2017-10', '-', '-', '-', '-', '-'],
                          ['2017-11', '-', '-', '-', '-', '-'], ['2017-12', '-', '-', '-', '-', '-']], [
                             ['2016-01', '\r\n\t\t\t\t\r\n\t\t\t\t\t正常缴纳\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t3878.00\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t387.80\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t80.56\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t曼帕尔人力资源(北京)有限公司\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t'],
                             ['2016-02', '\r\n\t\t\t\t\r\n\t\t\t\t\t正常缴纳\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t3878.00\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t387.80\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t80.56\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t曼帕尔人力资源(北京)有限公司\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t'],
                             ['2016-03', '\r\n\t\t\t\t\r\n\t\t\t\t\t正常缴纳\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t3878.00\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t387.80\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t80.56\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t曼帕尔人力资源(北京)有限公司\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t'],
                             ['2016-04', '\r\n\t\t\t\t\r\n\t\t\t\t\t正常缴纳\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t3878.00\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t387.80\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t80.56\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t曼帕尔人力资源(北京)有限公司\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t'],
                             ['2016-05', '\r\n\t\t\t\t\r\n\t\t\t\t\t正常缴纳\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t3878.00\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t387.80\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t80.56\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t曼帕尔人力资源(北京)有限公司\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t'],
                             ['2016-06', '\r\n\t\t\t\t\r\n\t\t\t\t\t正常缴纳\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t3878.00\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t387.80\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t80.56\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t曼帕尔人力资源(北京)有限公司\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t'],
                             ['2016-07', '\r\n\t\t\t\t\r\n\t\t\t\t\t正常缴纳\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t4252.00\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t425.20\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t88.04\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t曼帕尔人力资源(北京)有限公司\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t'],
                             ['2016-08', '\r\n\t\t\t\t\r\n\t\t\t\t\t正常缴纳\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t4252.00\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t425.20\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t88.04\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t曼帕尔人力资源(北京)有限公司\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t'],
                             ['2016-09', '\r\n\t\t\t\t\r\n\t\t\t\t\t正常缴纳\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t4252.00\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t425.20\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t88.04\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t曼帕尔人力资源(北京)有限公司\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t'],
                             ['2016-10', '\r\n\t\t\t\t\r\n\t\t\t\t\t正常缴纳\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t4252.00\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t425.20\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t88.04\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t曼帕尔人力资源(北京)有限公司\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t'],
                             ['2016-11', '\r\n\t\t\t\t\r\n\t\t\t\t\t正常缴纳\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t4252.00\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t425.20\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t88.04\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t北京永盛达通科技有限公司\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t'],
                             ['2016-12', '\r\n\t\t\t\t\r\n\t\t\t\t\t正常缴纳\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t4252.00\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t425.20\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t88.04\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t',
                              '\r\n\t\t\t\t\r\n\t\t\t\t\t北京永盛达通科技有限公司\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t']]]}
        state_list = [['单位提交制卡信息'], ['等待卡运营公司提取制卡数据（8个工作日）'], ['卡运营公司正在进行数据交接准备工作（5个工作日）'], ['卡片制作公司进行卡面印刷（11个工作日）'],
         ['卡片安全集成公司正在进行数据写入和封装（11个工作日）'], ['卡片制作完成，送达区县（2个工作日）'],
         ['单位已领卡', '您的社保卡已被北京众合天下管理咨询有限公司海淀分公司领取，请您与北京众合天下管理咨询有限公司海淀分公司联系尽快领卡。'], ['个人已领卡']]
        return item, history_dict, state_list


    def start(self):
        # 获取cookie
        self.get_cookie_urls()


        # self.cs()  # 测试
        # a, b, c = self.cs()  # cs 字段
        # self.save_mysql_individual(a,b,c)  # cs 存
        # self.save_mysql_history(a,b,c)  # cs
        # return




        # 个人基本信息查询， 返回数据
        print('个人信息')
        me_info_url = 'http://www.bjrbj.gov.cn/csibiz/indinfo/search/ind/indNewInfoSearchAction'
        item = self.me_info(me_info_url)
        print(1)
        print(item)
        # self.save_mysql_individual(item)


        # 历史缴费信息
        print('历史缴费信息')
        history_dict = self.get_history_many(2)
        print(2)
        print(history_dict)
        # self.save_mysql_insurance(history_dict)

        # 社保卡办理状态查询
        print('社保卡办理状态')
        state_list = self.get_card_state()
        print(3)
        print(state_list)
        # self.save_mysql_card(state_list)

        self.save_mysql_individual(item, history_dict, state_list)
        self.save_mysql_history(item, history_dict, state_list)



    # def close(self):
    #
    #     # 关闭myslq
    #     self.cur.close()
    #     self.conn.close()



