

def sex(id_card_str, male=1, female=2):
    '''
    根据字符串身份证判断　判断性别
    # 1代表男，2代表女
    :param id_card_str: 字符串身份证
    :param male: 返回　男　样式
    :param female: 返回　女　样式
    :return: 返回　性别
    '''
    if len(id_card_str) < 5:
        return -1
    return male if int(id_card_str[-2]) // 2 == 0 else female