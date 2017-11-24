# coding:utf-8
import requests
from lxml import etree

# 模拟登陆

url = 'https://gt3app9.tax861.gov.cn/Gt3GsWeb/gsmxwyNo/GrnsxxcxAction.action'

headers = {
	'Host' : 'gt3app9.tax861.gov.cn',
	'Origin' : 'https://gt3app9.tax861.gov.cn',
	'Referer' : 'https://gt3app9.tax861.gov.cn/Gt3GsWeb/gsmxwyNo/GrnsxxcxAction.action?code=query',
	'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
}
ssion = requests.session()
ssion.get(url, headers=headers, verify=False)
code_url = 'https://gt3app9.tax861.gov.cn/Gt3GsWeb/RandomCode.action'  # 验证码图片

img_code = ssion.get(code_url, headers=headers, verify = False)  # 请求验证码

with open('code.jpg', 'wb') as f:
	f.write(img_code.content)


code = input('请输入验证码')

data = {
	'zjlx':'201',
	'zzhm':'372924199601063012',
	'xm':'刘敬',
	'password':'liu123456',
	'yzm':code
}
log_url = 'https://gt3app9.tax861.gov.cn/Gt3GsWeb/gsmxwyNo/YhdlAction.action?code=login'
response = ssion.post(url, headers=headers, data=data, verify = False)

with open('cs1.html', 'wb')as f:
	f.write(response.content)

# dcap["phantomjs.page.settings.userAgent"] = ('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')












# 个人纳税获得
url = 'https://gt3app9.tax861.gov.cn/Gt3GsWeb/gsmxwyNo/GrnsxxcxAction.action?code=query'

headers = {
	'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding' : 'gzip, deflate, br',
	'Accept-Language' : 'zh-CN,zh;q=0.8',
	'Cache-Control' : 'max-age=0',
	'Connection' : 'keep-alive',
	'Content-Length' : '100',
	'Content-Type' : 'application/x-www-form-urlencoded',
	# 'Cookie' : 'JSESSIONID=BF176C2D95FB806AB237616C8923866B; _gscu_825391512=06599433kcses486; _gscs_825391512=06599433gc5ecp86|pv:1; _gscbrs_825391512=1; _gscs_163945954=06599433dosivj86|pv:1; _gscbrs_163945954=1; _gscu_163945954=06599433mkqdrb86',
	'Host' : 'gt3app9.tax861.gov.cn',
	'Origin' : 'https://gt3app9.tax861.gov.cn',
	'Referer' : 'https://gt3app9.tax861.gov.cn/Gt3GsWeb/gsmxwyNo/YhdlAction.action?code=login',
	'Upgrade-Insecure-Requests' : '1',
	'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
}

data = {
	'tijiao' : 'grsbxxcx',
	'actionType' : 'query',
	'skssksrqN' : '2006',
	'skssksrqY' : '1',
	'skssjsrqN' : '2017',
	'skssjsrqY' : '9'
}

response = ssion.post(url, headers=headers, data=data, verify = False)
with open('cs.html', 'wb')as f:
    f.write(response.content)
html = etree.HTML(response.text)

inner_lxml = html.xpath('//table[3]')[0]

inner = inner_lxml.xpath('.//td/text()')

print(inner)
