import requests
import time

def bjgs_one(id_card, password, name, id_card_type='201', user_id=None):
    try:
        bjgs = Bjgs(id_card, password, name, id_card_type)
        status = bjgs.first(user_id)
    except Exception as e:
        inner = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        inner += ' 账号:' + str(id_card) + ' 密码:' + str(password) + ' 类型:' + str(id_card_type) + ' 注册用户id:' + str(user_id) + '姓名:' + str(name)
        inner += ' 错误:' + str(e)
        inner += '\n'
        with open('bjgs_error_log.txt', 'a')as f:
            f.write(inner)
        status = 0
    return status

b = bjgs_one(1,2,3, 4, 5)
print(b, '状态')


