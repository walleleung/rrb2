# coding=utf-8
from PIL import Image
import requests
from lxml import etree
from selenium import webdriver
import time
import re
import pymysql
import subprocess
from small import sex
from bjdb import OperationMysql

'''
1、获取公积金账号密码
2、使用selenium登录（1、验证码处理 2、登录 3、判断是否登录成功）
3、获取首页的网址
4、获取登录后的cookie
5、使用cookie访问详细信息网址
6、提取信息保存成字典
7、存入数据库
'''


# 公积金
class BjGjj():
    def __init__(self, user, password, user_id=1, account_type=1):
        '''
        获取登录需要的参数
        :param user: 身份证号
        :param password: 查询密码
        '''
        self.user = user  # 账号
        self.password = password  # 密码
        self.user_id = user_id  # 注册用户ｉｄ
        self.account_type = account_type  # 账号类型　１：身份证号／　２：个人登记号／　３：军官证号／　４：护照号／　５：联名卡号
        self.cookie = None
        self.headers = None

        #self.conn = pymysql.connect(host='127.0.0.1', user='root', password='mysql', db='bjgjj', charset="utf8")
        #self.cur = self.conn.cursor()

    def get_cookie_urls(self):
        '''
        使用selenium + PhantomJS 登录， 获取cookie值， 和首页的需要的url
        :return: list(url)
        '''

        url = 'http://www.bjgjj.gov.cn/wsyw/wscx/gjjcx-login.jsp'

        # 调用
        # driver = webdriver.PhantomJS()
        driver = webdriver.Chrome()
        driver.get(url)


        # # 验证码截图
        # driver.save_screenshot("bj.png")
        # element = driver.find_element_by_xpath('//*[@id="sds"]/img')
        # left = element.location['x']
        # top = element.location['y']
        # right = element.location['x'] + element.size['width']
        # bottom = element.location['y'] + element.size['height']
        # im = Image.open('bj.png')
        # im = im.crop((left, top, right, bottom))
        # im.save('code.png')


        code = self.check_code(driver)
        print(code)
        if not code:
            code = self.check_code(driver)
        print('-')
        # driver.find_element_by_xpath('//*[@id="sds"]/input').click()  # 点击换验证码

        driver.find_element_by_xpath(
            '/html/body/table[2]/tbody/tr[3]/td/table/tbody/tr/td/div/form/div[1]/ul/li[3]/a').click()
        # driver.find_element_by_id("1").click()  # 点击到身份证


        # 输入账号密码
        driver.find_element_by_id("bh1").send_keys(self.user)
        driver.find_element_by_name("mm1").send_keys(self.password)

        # 识别验证码
        # self.code_img('code.png', 'code.png')
        # subprocess.call(["tesseract", './code.png', "output"])
        # with open("output.txt", 'r') as f:
        #     code = f.read()
        #     code = code.strip()
        # print(code)

        #code1 = code
        #code = input('请输入验证码:')
        #print(code==code1)
        #if code=='1':
        #    code = code1


        driver.find_element_by_name('gjjcxjjmyhpppp1').send_keys(code)
        driver.save_screenshot("bj.png")
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="login_tab_2"]/div/div[4]/input[1]').click()
        # driver.save_screenshot("bj2.png")

        #
        # for i in range(20):
        #     try:
        #         driver.find_element_by_xpath('//*[@id="new-mytable"]/tbody/tr[1]/th[2]/div/text()')
        #         break
        #     except:
        #         time.sleep(0.1)
        #
        for i in range(20):
            html = driver.page_source
            if html.find('tittle1') != -1:
                break
            time.sleep(0.1)

        # print(type(html))

        if html.find('tittle1') == -1:
            print('登陆失败')
            return 0


        # 提取网址 进行拼接
        text = driver.page_source
        # with open('cs.html', 'w') as f:
        #     f.write(text)
        html = etree.HTML(text)
        java_onclick = html.xpath('//*[@id="new-mytable"]/tbody/tr/td/div/a/@onclick')

        url_list = []
        for onclick in java_onclick:
            url_list.append('http://www.bjgjj.gov.cn/wsyw/wscx/gjj_cx.jsp?' + re.findall(r'\?(.*?)"', onclick)[0])

        # 获取cookie
        cookie_dict = driver.get_cookies()
        self.cookie = cookie_dict[0]['name'] + '=' + cookie_dict[0]['value']  # 拼接cookie

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Cookie': self.cookie,
            'Host': 'www.bjgjj.gov.cn',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://www.bjgjj.gov.cn/wsyw/wscx/gjjcx-choice.jsp',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
        # print(self.cookie)
        # print(self.headers)


        driver.quit()
        return url_list

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
                print(pix[x, y])
                if 3==len(pix[x, y]):
                    r, g, b = pix[x, y]
                else:
                    r, g, b, n = pix[x, y]
                if r < 143 or g < 143 or b < 143:
                    if 3 == len(pix[x, y]):
                        pix[x, y] = (0, 0, 0)
                    else:
                        pix[x, y] = (0, 0, 0, n)

        image.save(new_file)

    def check_code(self, driver):
        print(type(driver))
        for i in range(20):
            if i>0:
                driver.find_element_by_xpath('//*[@id="sds"]/input').click()  # 点击换验证码
            # 验证码截图
            driver.save_screenshot("bj.png")
            element = driver.find_element_by_xpath('//*[@id="sds"]/img')
            left = element.location['x']
            top = element.location['y']
            right = element.location['x'] + element.size['width']
            bottom = element.location['y'] + element.size['height']
            im = Image.open('bj.png')
            im = im.crop((left, top, right, bottom))
            im.save('code.png')

            self.code_img('code.png', 'code.png')
            subprocess.call(["tesseract", './code.png', "output"])
            with open("output.txt", 'r') as f:
                code = f.read()
                code = code.strip()

            if len(code) != 4:
                break

            if not code:
                break

            if not code.isalnum():
                break
            return code

    def inner(self, url):
        '''
        获取北京公积金公司url， 返回里面的数据, 历史记录url
        :param url: 开户单位url
        :return: 返回 字典格式的信息， 历史记录url
        '''
        print(url)
        print(self.headers)

        response = requests.get(url, headers=self.headers)

        with open('cs.html', 'wb') as f:
            f.write(response.content)

        html = etree.HTML(response.text)

        # 提取历史url
        java_onclick = html.xpath('//*[@id="t3Contents"]/div/div[2]/span/a/@onclick')
        # print(java_onclick)
        # test = html.xpath('//*[@id="tabContents"]/div/div[2]/span/a/@onclick')
        # print(test)
        # //*[@id="tabContents"]/div/div[2]/span/a
        # print(java_onclick)
        # print(re.findall(r"\?(.*?)'", java_onclick[0]if java_onclick else ''))
        # print(response.text)
        history_url = 'http://www.bjgjj.gov.cn/wsyw/wscx/gjj_cxls.jsp?' + re.findall(r"\?(.*?)'", java_onclick[0])[0]

        # 中心销户部
        # 基本信息
        inner = html.xpath('//td/text()')
        name = inner[11]  # 姓名
        register_id = inner[12]  # 个人登记号
        certificate_type = inner[13]  # 证件类型
        Id_number = inner[14]  # 证件号
        unit_id = inner[15]  # 单位登记号
        unit_name = inner[16]  # 单位名称
        administer_id = inner[17]  # 所属管理部编号
        administer_name = inner[18]  # 所属管理部名称
        account_state = inner[20]  # 账户状态
        end_business_time = inner[21]  # 最后业务时间
        #
        inner2 = html.xpath('//tr/td/div/text()')
        when_balance = inner2[20]  # 当前余额
        when_year_Pay = inner2[23]  # 当年缴存金额
        when_year_take = inner2[25]  # 当年提取金额
        Last_year_balance = inner2[27]  # 上年结转余额
        Roll_out_balance = inner2[30]  # 转出余额
        #
        numbering = html.xpath('//div/p/text()')[1]  # 个人编号
        # 组成字典
        item = {
            'numbering ': numbering.replace("\n", "").replace("\t", "").replace("\r", "").replace(" ", ""),
            'name ': name.replace("\n", "").replace("\t", "").replace("\r", "").replace(" ", ""),
            'register_id ': register_id.replace("\n", "").replace("\t", "").replace("\r", "").replace(" ", ""),
            'certificate_type ': certificate_type.replace("\n", "").replace("\t", "").replace("\r", "").replace(" ",
                                                                                                                ""),
            'Id_number ': Id_number.replace("\n", "").replace("\t", "").replace("\r", "").replace(" ", ""),
            'unit_id ': unit_id.replace("\n", "").replace("\t", "").replace("\r", "").replace(" ", ""),
            'unit_name ': unit_name.replace("\n", "").replace("\t", "").replace("\r", "").replace(" ", ""),
            'administer_id ': administer_id.replace("\n", "").replace("\t", "").replace("\r", "").replace(" ", ""),
            'administer_name ': administer_name.replace("\n", "").replace("\t", "").replace("\r", "").replace(" ", ""),
            'when_balance ': when_balance.replace("\n", "").replace("\t", "").replace("\r", "").replace(" ", ""),
            'account_state ': account_state.replace("\n", "").replace("\t", "").replace("\r", "").replace(" ", ""),
            'when_year_Pay ': when_year_Pay.replace("\n", "").replace("\t", "").replace("\r", "").replace(" ", ""),
            'when_year_take ': when_year_take.replace("\n", "").replace("\t", "").replace("\r", "").replace(" ", ""),
            'Last_year_balance ': Last_year_balance.replace("\n", "").replace("\t", "").replace("\r", "").replace(" ",
                                                                                                                  ""),
            # 'end_business_time ': end_business_time.replace("\n", "").replace("\t", "").replace("\r", "").replace(" ",
            #                                                                                                       "").replace('\xa0', ''),
            'end_business_time ': end_business_time.strip().replace('\xa0', ''),
            'Roll_out_balance ': Roll_out_balance.replace("\n", "").replace("\t", "").replace("\r", "").replace(" ",
                                                                                                                ""),
        }

        # item = {
        #     'numbering ': numbering.strip(),
        #     'name ': name.strip(),
        #     'register_id ': register_id.strip(),
        #     'certificate_type ': certificate_type.strip(),
        #     'Id_number ': Id_number.strip(),
        #     'unit_id ': unit_id.strip(),
        #     'unit_name ': unit_name.strip(),
        #     'administer_id ': administer_id.strip(),
        #     'administer_name ': administer_name.strip(),
        #     'when_balance ': when_balance.strip(),
        #     'account_state ': account_state.strip(),
        #     'when_year_Pay ': when_year_Pay.strip(),
        #     'when_year_take ': when_year_take.strip(),
        #     'Last_year_balance ': Last_year_balance.strip(),
        #     'end_business_time ': end_business_time.strip().replace('\xa0', ''),
        #     'Roll_out_balance ': Roll_out_balance.strip(),
        # }
        # print(item)

        return item, history_url

    def get_history(self, url):
        '''
        获取历史记录url 历史记录信息
        :param url:  历史url
        :return:  type = [{}, {}]  返回当页历史记录
        '''
        response = requests.get(url, headers=self.headers)
        html = etree.HTML(response.text)
        with open('cs.html', 'wb') as f:
            f.write(response.content)

        history_list = html.xpath('//*[@id="new-mytable3"]//tr')
        # print(history_list)
        item_list = []
        for history in history_list[1:]:
            item = {}
            item['time'] = history.xpath('./td/text()')[0].replace('\xa0', '').strip()  # 到账时间
            item['year'] = history.xpath('./td/text()')[1].replace('\xa0', '').strip()  # 汇补缴年月
            item['type'] = history.xpath('./td/text()')[2].replace('\xa0', '').strip()  # 业务类型
            item['add_money'] = history.xpath('./td/div/text()')[0]  # 增加额（元）
            item['less_money'] = history.xpath('./td/div/text()')[1]  # 减少额（元）
            item['balance'] = history.xpath('./td/div/text()')[2].replace('\xa0', '').strip()  # 余额（元）
            # print(item)
            item_list.append(item)

        return item_list

    def save_mysql_individual(self, item):
        data = {}
        data['username'] = item['name ']  # 用户名
        data['Sex'] = sex(item['Id_number '])  # 性别
        data['Card_number'] = item['Id_number ']  # 身份证号
        data['Department_number'] = item['numbering ']  # 职工账号（个人登记号）
        # data['Bank_card'] = ''  # 银行卡号
        # data['Phone'] = ''  # 电话
        data['Pay_status'] = '1' if item['account_state ']=='缴存' else '0'  # 当前缴纳状态
        data['Fund_banlance'] = item['when_balance '].replace(',', '').replace('元', '')  # 公积金余额
        data['Insured_area'] = item['administer_name ']  # 当前缴纳区域
        data['Owned_company'] = item['unit_name ']  # 所属公司单位

        print(data)
        db = OperationMysql(host='127.0.0.1', user='root', password='mysql', db='bj')
        db.insert_sql(data, 'bjgjj_info')

    def save_mysql_history(self, item, history):
        print(history)
        data = {}
        data['Transact_time '] = item['end_business_time ']  # 入账办结时间
        # data['Abstract'] =  # 摘要
        # data['Occurrencev'] =  # 发生额 float
        data['Balance'] = item['when_balance '].replace(',', '').replace('元', '')  # 公积金余额 float
        data['Company_number'] = item['unit_id ']  # 单位账号
        data['Owned_company'] = item['unit_name ']  # 纳税义务人（公司）
        print(data)
        db = OperationMysql(host='127.0.0.1', user='root', password='mysql', db='bj')
        db.insert_sql(data, 'bjgjj_history')


    # def save_mysql_individual(self, item):
    #     '''
    #     存入mysql
    #     :return:
    #     '''
    #     name = item['name ']
    #     register_id = item['register_id ']
    #     certificate_type = item['certificate_type ']
    #     Id_number = item['Id_number ']
    #
    #     sql = "insert into bjgjj_individual_info(name, register_id, certificate_type, Id_number) values('%s', '%s', '%s', '%s');" \
    #           % (name, register_id, certificate_type, Id_number)
    #     employee = self.cur.execute(sql)
    #     self.conn.commit()
    #
    # def save_mysql_bills(self, item):
    #     bjgjj_info_id = 1
    #     numbering = item['numbering ']
    #     unit_id = item['unit_id ']
    #     unit_name = item['unit_name ']
    #     administer_id = item['administer_id ']
    #     administer_name = item['administer_name ']
    #     when_balance = item['when_balance ']
    #     account_state = item['account_state ']
    #     when_year_Pay = item['when_year_Pay ']
    #     when_year_take = item['when_year_take ']
    #     Last_year_balance = item['Last_year_balance '].replace(',', '')
    #     end_business_time = item['end_business_time '][4:]
    #     Roll_out_balance = item['Roll_out_balance ']
    #
    #     sql = "insert into bjgjj_bills_info(bjgjj_info_id, numbering, unit_id, unit_name, administer_id, administer_name, when_balance, account_state, when_year_Pay, when_year_take, Last_year_balance, end_business_time, Roll_out_balance)" \
    #           " values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" \
    #           % (
    #           bjgjj_info_id, numbering, unit_id, unit_name, administer_id, administer_name, when_balance, account_state,
    #           when_year_Pay, when_year_take, Last_year_balance, end_business_time, Roll_out_balance)
    #     employee = self.cur.execute(sql)
    #     self.conn.commit()
    #
    # def save_mysql_history(self, item):
    #     bjgjj_bills_id = 1
    #     times = re.findall(r'\d+', item['time'])[0] if re.findall(r'\d+', item['time']) else ''  # 到账时间
    #     year = item['year']  # 汇补缴年月
    #     type = item['type']  # 业务类型
    #     add_money = item['add_money']  # 增加额（元）
    #     less_money = item['less_money']  # 减少额（元）
    #     balance = item['balance']  # 余额（元）
    #
    #     sql = "insert into bjgjj_history_info(bjgjj_bills_id, time, year, type, add_money, less_money, balance)" \
    #           " values('%s','%s','%s','%s','%s','%s','%s');" \
    #           % (bjgjj_bills_id, times, year, type, add_money, less_money, balance)
    #     employee = self.cur.execute(sql)
    #     self.conn.commit()


    def start(self):
        for i in range(5):
            url_list = self.get_cookie_urls()  # 获取个人住房信息urllist
            if url_list:
                break

        if not url_list:
            print('登录失败')
            return 0

        '''
        # 提取首页所有链接
        for url in url_list:
            item, history_url = bjgjj.inner(url)
            print(item)  # 个人信息
            #self.save_mysql_individual(item)
            print('成功')
            #self.save_mysql_bills(item)  # 存

            item_list = self.get_history(history_url)  # 缴费历史记录
            # print(item)
            for item in item_list:
                #self.save_mysql_history(item)
                print(item)
        '''


        # 提取最后一个链接信息
        print('最新一条信息')
        if not url_list:
            return 0

        url = url_list[-1]
        item_info, history_url = bjgjj.inner(url)

        item_list = self.get_history(history_url)  # 缴费历史记录
        item_history = None
        if item_list:
            item_history = item_list

        print('个人信息')
        print(item_info)
        self.save_mysql_individual(item_info)
        print('最新历史缴费信息')
        print(item_history)
        self.save_mysql_history(item_info, item_history)


    def close(self):

        # 关闭myslq
        self.cur.close()
        self.conn.close()  # 关闭连接


if __name__ == '__main__':
    bjgjj = BjGjj('110107197906121210', '811130')
    bjgjj.start()
