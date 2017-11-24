#coding:utf-8
import pymysql
import re

class BjgjjMsql(object):
    def __init__(self):

        self.conn =pymysql.connect(host='127.0.0.1',user='root',password='mysql',db='bjgjj',charset="utf8")
        self.cur=self.conn.cursor()

    def insert(self):
        # 插入一条
        sql = "insert into user(name, id_number) values('%s', '%s');" % ('姓名1', '身份证1')
        employee=self.cur.execute(sql)
        self.conn.commit()

    def create_individual_info(self):
        # 创建公积金表  个人信息
        sql = '''
            create table bjgjj_individual_info(
            id int unsigned auto_increment primary key not null,
            name varchar(10),  # 姓名
            register_id varchar(20),  # 个人登记号
            certificate_type varchar(20),  # 证件类型
            Id_number varchar(20),  # 证件号
            isdelete bit default 0
            );
        '''
        employee=self.cur.execute(sql)
        self.conn.commit()

    def create_bills_info(self):
        # 创建表  公司单位信息
        sql = '''
            create table bjgjj_bills_info(
            id int unsigned auto_increment primary key not null,
            bjgjj_info_id int,  # 关联 个人信息  bjgjj_info_id
            numbering varchar(30),  # 个人编号
            unit_id varchar(30),  # 单位登记号
            unit_name varchar(30),  # 单位名称
            administer_id varchar(30),  # 所属管理部编号
            administer_name varchar(30),  # 所属管理部名称
            when_balance varchar(30),  # 当前余额
            account_state varchar(30),  # 账户状态
            when_year_Pay varchar(30),  # 当年缴存金额
            when_year_take varchar(30),  # 当年提取金额
            Last_year_balance varchar(30),  # 上年结转余额
            end_business_time varchar(30),  # 最后业务时间
            Roll_out_balance varchar(30),  # 转出余额
            isdelete bit default 0
            );
        '''
        employee=self.cur.execute(sql)
        self.conn.commit()

    def create_history_info(self):
        # 创建表  公司单位信息
        sql = '''
            create table bjgjj_history_info(
            id int unsigned auto_increment primary key not null,
            bjgjj_bills_id int,  # 关联公司信息  bjgjj_bills_id
            time varchar(30),  # 到账时间
            year varchar(30),  # 汇补缴年月
            type varchar(30),  # 业务类型
            add_money varchar(30),  # 增加额（元）
            less_money varchar(30),  # 减少额（元）
            balance varchar(30),  # 余额（元）
            isdelete bit default 0
            );
        '''
        employee=self.cur.execute(sql)
        self.conn.commit()

    def save_mysql_bills(self):
        bjgjj_info_id = 1
        numbering = 'aaaaaaa'
        unit_id = '2'
        unit_name = '3'
        administer_id = '4'
        administer_name = '5'
        when_balance = '5'
        account_state = '6'
        when_year_Pay = '7'
        when_year_take = '8'
        Last_year_balance = '9'
        end_business_time = '10'
        Roll_out_balance = '11'

        sql = "insert into bjgjj_bills_info(bjgjj_info_id, numbering, unit_id, unit_name, administer_id, administer_name, when_balance, account_state, when_year_Pay, when_year_take, Last_year_balance, end_business_time, Roll_out_balance)" \
              " values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);" \
              % (
              bjgjj_info_id, numbering, unit_id, unit_name, administer_id, administer_name, when_balance, account_state,
              when_year_Pay, when_year_take, Last_year_balance, end_business_time, Roll_out_balance)
        employee = self.cur.execute(sql)
        self.conn.commit()

    def save_mysql_history(self, item):
        print(item)
        bjgjj_bills_id = 1
        times = re.findall(r'\d+', item['time'])[0] if re.findall(r'\d+', item['time']) else ''  # 到账时间
        year = item['year']  # 汇补缴年月
        type = item['type']  # 业务类型
        add_money = item['add_money']  # 增加额（元）
        less_money = item['less_money']  # 减少额（元）
        balance = item['balance']  # 余额（元）

        sql = "insert into bjgjj_history_info(bjgjj_bills_id, time, year, type, add_money, less_money, balance)" \
              " values('%s','%s','%s','%s','%s','%s','%s');" \
              % (bjgjj_bills_id, times, year, type, add_money, less_money, balance)
        print(sql)
        employee = self.cur.execute(sql)
        self.conn.commit()

    def start(self):
        # self.create_individual_info()  # 创建 公积金个人信息
        # self.create_bills_info()  # 创建 住房公积金个人总账信息
        # self.create_history_info()  # 创建 个人历史明细账单信息
        # self.save_mysql_bills()  # 存入 公积金个人总账单
        item1 = {'time': '\xa0\r\n          20060616', 'year': '\xa0\r\n          200605', 'type': '\xa0\r\n          汇缴', 'add_money': '110', 'less_money': '0', 'balance': '\xa0110'}

        item = {'time': '20060616', 'year': '00605',
                'type': '汇缴', 'add_money': '110', 'less_money': '0', 'balance': '110'}

        self.save_mysql_history(item)

    def close(self):
        self.cur.close()
        self.conn.close()  # 关闭连接


class BjrbjMsql(object):
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='mysql', db='bjgjj', charset="utf8")
        self.cur = self.conn.cursor()


    def create_individual_info(self):
        # 创建公积金表  个人信息
        sql = '''
            create table bjrbj_individual_info(
            id int unsigned auto_increment primary key not null,
            name varchar(40),
            idcard varchar(40),
            sex varchar(40),
            born_day varchar(40),
            peoples varchar(40),
            country varchar(40),
            individual_identity varchar(40),
            work_dates varchar(40),
            city varchar(40),
            city_addr varchar(40),
            city_code varchar(40),
            live_addr varchar(40),
            live_code varchar(40),
            culture varchar(40),
            applicant_phone varchar(40),
            applicant_tel varchar(40),
            months_revenue varchar(40),
            Banks varchar(40),
            banks_code varchar(40),
            isdelete bit default 0
            );
        '''
        employee = self.cur.execute(sql)
        self.conn.commit()


    def create_insurance_info(self, insurance):
        # 创建表  公司单位信息
        sql = '''
            create table bjrbj_%s_info(
            id int unsigned auto_increment primary key not null,
            bjgjj_info_id int,  # 关联 个人信息  bjgjj_info_id
            a varchar(30),
            b varchar(30),
            c varchar(30),
            d varchar(30),
            e varchar(30),
            f varchar(30),
            g varchar(30),
            isdelete bit default 0
            );
        ''' % insurance
        employee = self.cur.execute(sql)
        self.conn.commit()


    def create_card_info(self):
        # 创建表  公司单位信息
        sql = '''
            create table bjrbj_card_info(
            id int unsigned auto_increment primary key not null,
            bjgjj_bills_id int,  # 关联
            a varchar(80),
            b varchar(80),
            c varchar(80),
            d varchar(80),
            e varchar(80),
            f varchar(80),
            g varchar(80),
            h varchar(80),
            i varchar(80),
            j varchar(80),
            k varchar(80),
            isdelete bit default 0
            );
        '''
        employee = self.cur.execute(sql)
        self.conn.commit()




    def start(self):
        # self.create_individual_info()  # 创建　社保个人信息
        # for insurance in ['oldage', 'unemployment', 'injuries', 'maternity', 'medicalcare']:
        #     self.create_insurance_info(insurance)  # 创建5个表
        self.create_card_info()  #　创建社保　状态

    def close(self):
        self.cur.close()
        self.conn.close()  # 关闭连接


if __name__ == '__main__':
    # 北京公积金
    # db_mysql = BjgjjMsql()
    # db_mysql.start()
    # db_mysql.close()

    # 北京社保
    bjrbj = BjrbjMsql()
    bjrbj.start()
    bjrbj.close()



