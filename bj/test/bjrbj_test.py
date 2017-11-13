import requests
from lxml import etree
import re

url = 'http://www.bjrbj.gov.cn/csibiz/indinfo/search/ind/indNewInfoSearchAction'

cookie = '_gscu_2065735475=064738243ukwmp90;_gscbrs_2065735475=1;_gscs_2065735475=06476000low4bz90|pv:1;mjrzMBJgZO=MDAwM2IyYWYyZjQwMDAwMDAwMDgwcFF/QV4xNTA2NTAxMzE1;JSESSIONID=BCFA0FC37FE7A94C7EEF039BE36F2368;'



headers = {
    'Accept' : 'text/javascript, text/html, application/xml, text/xml, */*',
    'Accept-Encoding' : 'gzip, deflate',
    'Accept-Language' : 'zh-CN,zh;q=0.8',
    'Connection' : 'keep-alive',
    'Content-Length' : '0',
    'Content-type' : 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie' : cookie,
    'Host' : 'www.bjrbj.gov.cn',
    'Origin' : 'http://www.bjrbj.gov.cn',
    'Referer' : 'http://www.bjrbj.gov.cn/csibiz/indinfo/search/ind/ind_new_info_index.jsp',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'X-Prototype-Version' : '1.5.1.1',
    'X-Requested-With' : 'XMLHttpRequest',
}
# 请求
response = requests.post(url, headers=headers)
html = etree.HTML(response.text)
info_list = html.xpath('//tr/td')

# 测试打印所有td的内容加上下标
n = 0
for info in info_list:
    print(n, ':', info.xpath('./text()'))
    n += 1

# 提取信息存入item
item = {}
info_head = re.findall(r'[\u4E00-\u9FA5()]+|\d+', info_list[0].xpath('./text()')[0])
item['unit'] = info_head[1]  # 单位名称
item['organization_code'] = info_head[3]  # 组织机构代码
item['insurance_number'] = info_head[5]  # 社会保险登记证编号
item['address'] = info_head[7]  # 所属区县

item['have_insurance'] = info_list[2].xpath('./text()')[0] if info_list[2].xpath('./text()') else ''  # 参加险种  （列表格式没有处理）
item['name'] = info_list[5].xpath('./text()')[0] if info_list[5].xpath('./text()') else ''  # 姓名
item['idcard'] = info_list[7].xpath('./text()')[0] if info_list[7].xpath('./text()') else ''  # 公民身份证号码
item['sex'] = info_list[9].xpath('./text()')[0] if info_list[9].xpath('./text()') else ''  # 性别
item['born_day'] = info_list[11].xpath('./text()')[0] if info_list[11].xpath('./text()') else ''  # 出生日期
item['peoples'] = info_list[13].xpath('./text()')[0] if info_list[13].xpath('./text()') else ''  # 民族
item['country'] = info_list[15].xpath('./text()')[0] if info_list[15].xpath('./text()') else ''  # 国家/地区
item['individual_identity'] = info_list[17].xpath('./text()')[0] if info_list[17].xpath('./text()') else ''  # 个人身份
item['work_dates'] = info_list[19].xpath('./text()')[0] if info_list[19].xpath('./text()') else ''  # 参加工作日期
item['city'] = info_list[23].xpath('./text()')[0] if info_list[23].xpath('./text()') else ''  # 户口性质
item['city_addr'] = info_list[25].xpath('./text()')[0] if info_list[25].xpath('./text()') else ''  # 户口所在地地址
item['city_code'] = info_list[27].xpath('./text()')[0] if info_list[27].xpath('./text()') else ''  # 户口所在地邮政编码
item['live_addr'] = info_list[29].xpath('./text()')[0] if info_list[29].xpath('./text()') else ''  # 居住地（联系）地址
item['live_code'] = info_list[31].xpath('./text()')[0] if info_list[31].xpath('./text()') else ''  # 居住地（联系）邮政编码
item['culture'] = info_list[40].xpath('./text()')[0] if info_list[40].xpath('./text()') else ''  # 文化程度
item['applicant_phone'] = info_list[43].xpath('./text()')[0] if info_list[43].xpath('./text()') else ''  # 参保人电话
item['applicant_tel'] = info_list[45].xpath('./text()')[0] if info_list[45].xpath('./text()') else ''  # 参保人手机
item['months_revenue'] = info_list[47].xpath('./text()')[0] if info_list[47].xpath('./text()') else ''  # 申报月均工资收入（元）
item['Banks'] = info_list[53].xpath('./text()')[0] if info_list[53].xpath('./text()') else ''  # 委托代发银行名称
item['banks_code'] = info_list[55].xpath('./text()')[0] if info_list[55].xpath('./text()') else ''  # 银行账号
print(item)


# 社保养老
url = 'http://www.bjrbj.gov.cn/csibiz/indinfo/search/ind/indPaySearchAction!oldage?searchYear=2018'
response = requests.post(url, headers=headers)
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
for tr in tr_lxml[2:]:
    year = tr.xpath('./td/text()')
    item.append(year)

print(item)







