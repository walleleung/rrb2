
import pymysql

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
    return sql
    # employee = cur.execute(sql)
    # conn.commit()
    # return employee

class BjgsDb():
    '''
    对北京个人税进行传入数据库
    '''
    def __init__(self):

        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='mysql', db='bj', charset="utf8")
        self.cur = self.conn.cursor()


    def save_mysql_individual(self, id, info, item):

        # UserID = '1'  # 用户ID
        # Username = info['name']  # 用户姓名
        # Sex = '1' if int(info['id_card'][-2])//2==0 else '2'  # 1代表男，2代表女
        # Card_number = info['id_card']  # 身份证号
        # Recently_paid = format(float(item['income'])/100 * float(item['rate']), '.2f')  # 最近缴纳
        # Monthly_deposit = item['tax']  # 月缴存额
        # owned_company = item['obligation']  # 所属单位
        if item:
            item = item[-1]
        data = {
            "UserID": id,  # 用户ID
            "Username": info['name'],  # 用户姓名
            "Sex": '1' if int(info['id_card'][-2]) // 2 == 0 else '2',  # 1代表男，2代表女
            "Card_number": info['id_card'],  # 身份证号
            # "Recently_paid": format(float(item['income']) / 100 * float(item['rate']), '.2f'),  # 最近缴纳
            "owned_company": item['company'],  # 所属单位
        }
        if item['tax_rate'] != '——':
            data["Monthly_deposit"] = item['tax_rate']  # 月缴存额

        if item['tax_rate'] != '——':
            data['Recently_paid'] = format(float(item['income']) / 100 * float(item['tax_rate']), '.2f')  # 最近缴纳

        sql = save_mysql('personaltax_info',data)



        # sql = "insert into personaltax_info(UserID, Username, Sex, Card_number, Recently_paid, Monthly_deposit, owned_company)" \
        #       " values('%s', '%s', '%s', '%s', '%s', '%s', '%s');" \
        #       % (
        #           UserID, Username, Sex, Card_number, Recently_paid, Monthly_deposit, owned_company,
        #       )
        employee = self.cur.execute(sql)
        self.conn.commit()


    def save_mysql_history(self, id, info, item_list):
        print('-')
        '''
        Userid = '1'  # 关联用户ID
        Pay_time = item['time']  # 缴纳时间
        Tax_type = item['projects']  # 纳税项目
        Tax_rate = item['rate']  # 税率
        Taxable_income = format(float(item['income']) - float(item['income'])/100 * float(item['rate']), '.2f')  # 纳税所得
        Income_money = item['income']  # 收入额
        Withhold_taxable = format(float(item['income']) - float(item['income'])/100 * float(item['rate']) + float(item['tax']), '.2f')  # 实际扣缴所得税
        Owned_company = item['obligation']  # 纳税义务人

        sql = "insert into personaltax_list(Userid, Pay_time, Tax_type, Tax_rate, Taxable_income, Income_money, Withhold_taxable, Owned_company)" \
              " values('%s','%s','%s','%s','%s','%s','%s','%s');" \
              % (Userid, Pay_time, Tax_type, Tax_rate, Taxable_income, Income_money, Withhold_taxable, Owned_company)
        '''
        self.cur.execute('select id,Username from personaltax_info where UserID="%s" and Username="%s"' % (id, info['name']))
        id = self.cur.fetchall()[-1][0]
        for item in item_list:
            data = {
                "Userid" : id,  # 关联用户ID
                "Pay_time" : item['date'],  # 缴纳时间
                "Tax_type" : item['get_projects'],  # 纳税项目
                # "Tax_rate" : item['tax_rate'],  # 税率
                "Income_money" : item['income'],  # 收入额
                "Owned_company" : item['company'],  # 纳税义务人
            }
            if item['tax_rate'] != '——':
                data["Taxable_income"] = format(float(item['income']) - float(item['income'])/100 * float(item['tax_rate']), '.2f')  # 纳税所得
                data["Withhold_taxable"] = format(float(item['income']) - float(item['income'])/100 * float(item['tax_rate']) + float(item['tax_rate']), '.2f')  # 实际扣缴所得税
                data["Tax_rate"] = item['tax_rate']  # 税率
            # if item['tax_rate'] != '——':

            print(data)
            sql = save_mysql('personaltax_list', data)
            # print(sql)

            employee = self.cur.execute(sql)
            self.conn.commit()


    def start(self,user_id, info, item):
        # 存入
        self.save_mysql_individual(user_id, info, item)
        self.save_mysql_history(user_id, info, item)

        # 关闭myslq
        self.cur.close()
        self.conn.close()


class OperationMysql():
    '''
    对mysql进行　增　改　查　操作
    未实现：改，查
    '''
    def __init__(self, host='127.0.0.1', user='root', password='mysql', db='bj'):
        '''
        链接数据库
        '''
        self.conn = pymysql.connect(host=host, user=user, password=password, db=db, charset="utf8")
        self.cur = self.conn.cursor()

    def insert_sql(self, data, tables):
        '''
        存入字典　存入数据库
        :param data: 字典　ｋｅｙ：字段
        :param tables: 表名
        :return:
        '''
        fields = ''
        values = ''
        for k, v in data.items():
            fields += str(k) + ','
            values += '"%s",' % str(v)

        sql = 'insert into %s(%s) values(%s);' % (tables, fields[:-1], values[:-1])
        print(sql)
        employee = self.cur.execute(sql)
        self.conn.commit()
        return employee

    # 查询
    def check_mysql(self, tables=None, column='*', where=None, sql=None, page=None, step=10):
        limit = ''
        if page:
            page = int(page)*step-step
            limit = ' limit %d,%d'%(page, step)

        if sql:
            # print(sql)
            sql += limit
            employee = self.cur.execute(sql)
            return self.cur.fetchall()

        if where:
            sql = 'select %s from %s where %s' % (column, tables, where)
            sql += limit
            print(sql)
            employee = self.cur.execute(sql)
            return self.cur.fetchall()

        sql = 'select %s from %s' % (column, tables)
        sql += limit
        employee = self.cur.execute(sql)
        return self.cur.fetchall()


if __name__ == '__main__':
    # cs = OperationMysql(db='test')
    #
    # # 存
    # data = {}
    # data['name'] = '测试'
    # data['subject'] = '测试'
    # data['score'] = '1'
    # tables = 'student'
    # cs.insert_sql(data, tables)
    d = BjgsDb()
    d.save_mysql_history('1', {'name':'刘敬'}, {})

