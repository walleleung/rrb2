#coding:utf-8
import pymysql
import re




class BjgjjMysql(object):
    def __init__(self):

        self.conn =pymysql.connect(host='127.0.0.1',user='root',password='mysql',db='bj',charset="utf8")
        self.cur=self.conn.cursor()

    def insert(self):
        # 插入一条
        sql = "insert into user(name, id_number) values('%s', '%s');" % ('姓名1', '身份证1')
        employee=self.cur.execute(sql)
        self.conn.commit()

    def create_bjgjj_info(self):
        # 创建公积金表  个人信息
        sql = '''
            create table bjgjj_info(
            id int unsigned auto_increment primary key not null,
            User_id smallint(5),  # 关联用户userID
            username varchar(20),  # 用户名
            Sex tinyint(1),  # 性别
            Card_number varchar(20),  # 身份证号
            Department_number varchar(15),  # 职工账号
            Bank_card varchar(20),  # 银行卡号
            Phone varchar(15),  # 电话
            Pay_status tinyint(1),  # 当前缴纳状态
            Fund_banlance  float,  # 公积金余额
            Insured_area varchar(50),  # 当前缴纳区域
            Owned_company varchar(50),  # 所属公司单位
            Update_time char(10),  # 修改时间
            Create_time char(10),  # 创建时间
            isdelete bit default 0
            );
        '''
        employee=self.cur.execute(sql)
        self.conn.commit()

    def create_history_info(self):
        # 创建表  公司单位信息
        sql = '''
            create table bjgjj_history(
            id int unsigned auto_increment primary key not null,
            Userid smallint(3),  # 关联用户信息ID
            Transact_time  char(10),  # 入账办结时间
            Abstract varchar(50),  # 摘要
            Occurrencev float(1),  # 发生额
            Balance varchar(15),  # 公积金余额
            Company_number varchar(50),  # 单位账号
            Owned_company Varchar(50),  # 纳税义务人（公司）
            repair_date varchar(10),  # 汇补缴年月
            business_type varchar(10),  # 业务类型
            add_quota varchar(10),  # 增加额（元）
            reduce_quota varchar(10),  # 减少额（元）
            Update_time Char(10),  # 更新时间
            Create_time Char(10),  # 创建时间
            isdelete bit default 0
            );
        '''
        employee=self.cur.execute(sql)
        self.conn.commit()

    def save_mysql_gjgjj_info(self):
        User_id = '1'  # 关联用户userID
        username = '用户名'  # 用户名
        Sex = '1'  # 性别
        Card_number = '123456789012345678'  # 身份证号
        Department_number = '0233'  # 职工账号
        Bank_card = '6222888888888888888'  # 银行卡号
        Phone = '13188888888'  # 电话
        Pay_status = '1'  # 当前缴纳状态
        Fund_banlance = '100.2'  # 公积金余额
        Insured_area = '当前加纳区域'  # 当前缴纳区域
        Owned_company = '所属公司单位'  # 所属公司单位

        sql = "insert into bjgjj_info(User_id, username, Sex, Card_number, Department_number, Bank_card, Phone, Pay_status, Fund_banlance, Insured_area, Owned_company)" \
              " values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" \
              % (
                  User_id, username, Sex, Card_number, Department_number, Bank_card, Phone, Pay_status, Fund_banlance,
                  Insured_area, Owned_company
              )
        employee = self.cur.execute(sql)
        self.conn.commit()

    def save_mysql_history(self):
        Userid = '1'  # 关联用户信息ID
        Transact_time = '1'  # 入账办结时间
        Abstract = '摘要'  # 摘要
        Occurrencev = '1.0'  # 发生额
        Balance = '2.0'  # 公积金余额
        Company_number = '单位账号'  # 单位账号
        Owned_company = '纳税义务人（公司）'  # 纳税义务人（公司）



        sql = "insert into bjgjj_history(Userid,Transact_time,Abstract,Occurrencev,Balance,Company_number,Owned_company)" \
              " values('%s','%s','%s','%s','%s','%s','%s');" \
              % (Userid,Transact_time,Abstract,Occurrencev,Balance,Company_number,Owned_company)
        print(sql)
        employee = self.cur.execute(sql)
        self.conn.commit()

    def start(self):
        # 创建表
        # self.create_bjgjj_info()
        self.create_history_info()

        # 存储
        # self.save_mysql_gjgjj_info()
        # self.save_mysql_history()

    def close(self):
        self.cur.close()
        self.conn.close()  # 关闭连接


class BjrbjMsql(object):
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='mysql', db='bj', charset="utf8")
        self.cur = self.conn.cursor()

    def create_individual_info(self):
        # 创建表  个人信息
        sql = '''
            create table SocialSecurity_info(
            id int unsigned auto_increment primary key not null,
            userid Int(20),  # 关联user用户id
            name varchar(32),  # 社保用户名
            House_type varchar(10),  # 户口类型
            Total_paymonth varchar(20),  # 累计缴纳
            Card_number varchar(20),  # 身份证号
            Social_number  varchar(20),  # 社保编号
            Phone Varchar(11),  # 联系电话
            Payment_type tinyint(2),  # 缴费人员类别
            Income_wages float,  # 申报月工资收入
            owned_company  Varchar(20),  # 所属公司
            Insured_area varchar(20),  # 参保区域
            Hospital1 Varchar(20),  # 定点医院1
            Hospital2 Varchar(20),  # 定点医院2
            Hospital3 Varchar(20),  # 定点医院3
            Hospital4 Varchar(20),  # 定点医院4
            Hospital5 Varchar(20),  # 定点医院5
            Insured_status  Varchar(20),  # 参保状态
            Recently_paid varchar(20),  # 最近缴纳
            medicalcare_status Varchar(20),  # 医疗保险缴纳情况
            endowment_status Varchar(20),  # 养老保险缴纳情况
            unemployment_status Varchar(20),  # 失业保险缴纳情
            business_status Varchar(20),  # 工商保险缴纳情况
            maternity_status Varchar(20),  # 生育保险缴纳情况
            Card_progress varchar(20),  # 制卡进度字段（1，2，3..代表制卡的进度）
            Update_time char(20),  # 更新时间
            Create_time char(20),  # 创建时间
            isdelete bit default 0
            );
        '''
        employee = self.cur.execute(sql)
        self.conn.commit()

    def create_history_info(self):
        # 创建表  公司单位信息
        sql = '''
            create table SocialSecurity_list(
            id int unsigned auto_increment primary key not null,
            Userid int(20),  # 关联用户表userid
            deposit_time varchar(12),  # 缴存时间
            companypay_money float,  # 单位缴纳数额
            Individualspay_money float,  # 个人缴纳数额
            basemoney float,  # 缴纳基数
            Owned_company varchar(30),  # 缴办单位
            Update_time varchar(30),  # 数据更新时间
            Create_time varchar(30),  # 创建时间
            remark varchar(15),  # 注释
            isdelete bit default 0
            );
        '''
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
        # 创建表
        # self.create_individual_info()  # 创建　社保个人信息
        self.create_history_info()





        # for insurance in ['oldage', 'unemployment', 'injuries', 'maternity', 'medicalcare']:
        #     self.create_insurance_info(insurance)  # 创建5个表
        # self.create_card_info()  #　创建社保　状态

    def close(self):
        self.cur.close()
        self.conn.close()  # 关闭连接


class BjgsMysql(object):
    '''
    北京个税信息存储
    '''
    def __init__(self):

        self.conn =pymysql.connect(host='127.0.0.1',user='root',password='mysql',db='bj',charset="utf8")
        self.cur=self.conn.cursor()

    def insert(self):
        # 插入一条
        sql = "insert into user(name, id_number) values('%s', '%s');" % ('姓名1', '身份证1')
        employee=self.cur.execute(sql)
        self.conn.commit()

    def create_user_info(self):
        # 创建个税表  个人信息
        sql = '''
            create table personaltax_info(
            id int unsigned auto_increment primary key not null,
            UserID varchar(32),  # 用户ID
            Username varchar(15),  # 用户姓名
            Sex char(8),  # 1代表男，2代表女
            Card_number varchar(20),  # 身份证号
            Recently_paid varchar(20),  # 最近缴纳
            Monthly_deposit float,  # 月缴存额
            owned_company varchar(50),  # 所属单位
            Update_time	char(20),  # 更新时间
            Create_time	char(20),  # 创建时间
            isdelete bit default 0
            );
        '''
        employee=self.cur.execute(sql)
        self.conn.commit()


    def create_history_info(self):
        # 创建表  公司单位信息
        sql = '''
            create table personaltax_list(
            id int unsigned auto_increment primary key not null,
            Userid Int,  # 关联用户ID
            Pay_time varchar(32),  # 缴纳时间
            Tax_type varchar(50),  # 纳税项目
            Tax_rate float,  # 税率
            Taxable_income float,  # 纳税所得
            Income_money float,  # 收入额
            Withhold_taxable float,  # 实际扣缴所得税
            Owned_company Varchar(50),  # 纳税义务人
            Update_time Char(20),  # 更新时间
            Create_time Char(20),  # 创建时间
            isdelete bit default 0
            );
        '''
        employee=self.cur.execute(sql)
        self.conn.commit()

    def save_mysql_user_info(self):
        UserID = '1'  # 用户ID
        Username = '用户姓名'  # 用户姓名
        Sex = '1'  # 1代表男，2代表女
        Card_number = '123456798012345678'  # 身份证号
        Recently_paid = '1000'  # 最近缴纳
        Monthly_deposit = '2000'  # 月缴存额
        owned_company = '所属单位'  # 所属单位

        sql = "insert into personaltax_info(UserID, Username, Sex, Card_number, Recently_paid, Monthly_deposit, owned_company)" \
              " values('%s', '%s', '%s', '%s', '%s', '%s', '%s');" \
              % (
                  UserID, Username, Sex, Card_number, Recently_paid, Monthly_deposit, owned_company,
              )
        employee = self.cur.execute(sql)
        self.conn.commit()

    def save_mysql_history(self):
        Userid = '1'  # 关联用户ID
        Pay_time = '2017-10-10'  # 缴纳时间
        Tax_type = '缴纳项目'  # 纳税项目
        Tax_rate = '10'  # 税率
        Taxable_income = '20'  # 纳税所得
        Income_money = '30'  # 收入额
        Withhold_taxable = '40'  # 实际扣缴所得税
        Owned_company = '纳税义务人'  # 纳税义务人

        sql = "insert into personaltax_list(Userid, Pay_time, Tax_type, Tax_rate, Taxable_income, Income_money, Withhold_taxable, Owned_company)" \
              " values('%s','%s','%s','%s','%s','%s','%s','%s');" \
              % (Userid, Pay_time, Tax_type, Tax_rate, Taxable_income, Income_money, Withhold_taxable, Owned_company)
        print(sql)
        employee = self.cur.execute(sql)
        self.conn.commit()

    def start(self):
        # self.create_user_info()  # 创建个税用户信息表
        # self.save_mysql_user_info()  # 存入个税用户信息


        # self.create_history_info()  # 创建个税用户缴费信息列表
        self.save_mysql_history()  # 存入个税用户缴费信息


    def close(self):
        self.cur.close()
        self.conn.close()  # 关闭连接


class UserMsql(object):
    '''
    用户信息
    '''
    def __init__(self):

        self.conn =pymysql.connect(host='127.0.0.1',user='root',password='mysql',db='bj',charset="utf8")
        self.cur=self.conn.cursor()

    def insert(self):
        # 插入一条
        sql = "insert into 360_user(username, card_number) values('%s', '%s');" % ('测试用户名', '123456789012345678')
        employee=self.cur.execute(sql)
        self.conn.commit()

    def create_360_user(self):
        # 创建公积金表  个人信息
        sql = '''
            create table 360_user(
            id int unsigned auto_increment primary key not null,
            mobile varchar(20),  # 手机号
            username varchar(20),  # 用户名
            password varchar(32),  # 密码（加密字符串）
            nikename varchar(20),  # 	昵称
            header_image varchar(20),  # 头像地址
            email varchar(30),  # 邮箱
            card_number varchar(30),  # 身份证号
            Province_id Tinyint(2),  # 省份ID
            City_id Tinyint(2),  # 城市ID
            House_adress varchar(30),  # 户口所在地
            User_type Tinyint(2),  # 用户类型（1代表正常注册，2代表推广用户）
            Source_channel Tinyint(2),  # 来源渠道（1代表PC，2代表微信，3代表手机站，4代表android，5代表IOS）
            Ip_address varchar(30),  # IP地址
            Status Tinyint(1),  # 用户状态（1代表正常用户，2代表禁用）
            Update_time char(20),  # 更新时间
            Create_time char(20),  # 创建时间
            isdelete bit default 0
            );
        '''
        employee=self.cur.execute(sql)
        self.conn.commit()

    def start(self):
        # self.create_360_user()  # 创建 360用户表
        self.insert()  #　插入信息

    def close(self):
        self.cur.close()
        self.conn.close()  # 关闭连接


if __name__ == '__main__':
    # 北京公积金
    # db_mysql = BjgjjMysql()
    # db_mysql.start()
    # db_mysql.close()

    # 北京社保
    bjrbj = BjrbjMsql()
    bjrbj.start()
    bjrbj.close()


    # 北京个税
    # bjgs = BjgsMysql()
    # bjgs.start()


    # 用户个人信息
    # user = UserMsql()
    # user.start()



