
# 无界面浏览器 登录
from selenium import webdriver
url = 'http://www.bjgjj.gov.cn/wsyw/wscx/gjjcx-login.jsp#login_tab_2'

# 调用
driver = webdriver.PhantomJS()

driver.get(url)

driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[3]/td/table/tbody/tr/td/div/form/div[1]/ul/li[3]/a').click()
# driver.find_element_by_id("1").click()  # 点击到身份证

# 输入账号密码
driver.find_element_by_id("bh1").send_keys(u"110107197906121210")
driver.find_element_by_id("mm1").send_keys(u"811130")

driver.save_screenshot("bj.png")
cookie_dict = driver.get_cookies()
print('1')
print(cookie_dict[0]['name'] + '=' + cookie_dict[0]['value'])  # 拼接cookie
print('2')

print(cookie_dict)

# driver.save_screenshot("bjgjj.png")
driver.quit()

'''
#-------------------
# request请求模拟登录
import requests
ssion = requests.session()
url = 'http://www.bjgjj.gov.cn/wsyw/wscx/gjjcx-login.jsp'  # 登录页面

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
ssion.get(url, headers=headers)  # 登录页面
code_response = ssion.get('http://www.bjgjj.gov.cn/wsyw/servlet/PicCheckCode1', headers=headers)  # 获取验证码图片

with open('cs.jpg', 'wb')as f:
	f.write(code_response.content)

code = input('请输入验证码：')

# post 请求参数
data = {
	'lb' : 1,
	'bh1' : '110107197906121210',
	'mm1' : '811130',
	'gjjcxjjmyhpppp' : str(code),
	'gjjcxjjmyhpppp1' : str(code),
}

# 登录
response = ssion.post('http://www.bjgjj.gov.cn/wsyw/wscx/gjjcx-choice.jsp', data=data, headers=headers)

with open('bj.html', 'wb') as f:
	f.write(response.content)
$("#mm").val($("[name=mm"+lb+"]").val());

text = pytesseract.image_to_string(image)
'''

import requests
from lxml import etree
from PIL import Image	
# url = 'http://www.bjgjj.gov.cn/wsyw/wscx/gjj_cx.jsp?nicam=enpyenI3enk3eXI2ejJ6MnpycnI3NDkA&hskwe=R0pKd3czMzc1MjY2NjM0&vnv=JiMyMzgyODsmIzQwNTI3OwAA&lx=0'
# url2 = 'http://www.bjgjj.gov.cn/wsyw/wscx/gjj_cx.jsp?nicam=enpyenI3enk3eXI2ejJ6MnpycnI3NDkA&hskwe=R0pKd3c4YzZ6d2E2NzAy&vnv=JiMyMzgyODsmIzQwNTI3OwAA&lx=0'

def code_img(old_file, new_file):
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
			r, g, b = pix[x,y]
			if r<143 or g<143 or b<143:
				pix[x,y] = (0, 0, 0)

	image.save('1.jpg')

def inner(url, cookie):
	'''
	获取北京公积金公司url， 返回里面的数据
	:param url: 开户单位url
	:param cookie: cookie值
	:return: 返回 字典格式的信息
	'''
	headers = {
		'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'Accept-Encoding' : 'gzip, deflate',
		'Accept-Language' : 'zh-CN,zh;q=0.8',
		'Cache-Control' : 'max-age=0',
		'Cookie' : cookie,
		'Host' : 'www.bjgjj.gov.cn',
		'Proxy-Connection' : 'keep-alive',
		'Referer' : 'http://www.bjgjj.gov.cn/wsyw/wscx/gjjcx-choice.jsp',
		'Upgrade-Insecure-Requests' : '1',
		'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
	}

	response = requests.get(url, headers=headers)

	# with open('cs.html', 'wb') as f:
	# 	f.write(response.content)

	html = etree.HTML(response.text)

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
		'numbering ' : numbering.replace("\n","").replace("\t","").replace("\r","").replace(" ",""),
		'name ' : name.replace("\n","").replace("\t","").replace("\r","").replace(" ","") ,
		'register_id ' : register_id.replace("\n","").replace("\t","").replace("\r","").replace(" ","") ,
		'certificate_type ' : certificate_type.replace("\n","").replace("\t","").replace("\r","").replace(" ","") ,
		'Id_number ' : Id_number.replace("\n","").replace("\t","").replace("\r","").replace(" ","") ,
		'unit_id ' : unit_id.replace("\n","").replace("\t","").replace("\r","").replace(" ","") ,
		'unit_name ' : unit_name.replace("\n","").replace("\t","").replace("\r","").replace(" ","") ,
		'administer_id ' : administer_id.replace("\n","").replace("\t","").replace("\r","").replace(" ","") ,
		'administer_name ' : administer_name.replace("\n","").replace("\t","").replace("\r","").replace(" ","") ,
		'when_balance ' : when_balance.replace("\n","").replace("\t","").replace("\r","").replace(" ",""),
		'account_state ' : account_state.replace("\n","").replace("\t","").replace("\r","").replace(" ","") ,
		'when_year_Pay ' : when_year_Pay.replace("\n","").replace("\t","").replace("\r","").replace(" ",""),
		'when_year_take ' : when_year_take.replace("\n","").replace("\t","").replace("\r","").replace(" ","") ,
		'Last_year_balance ' : Last_year_balance.replace("\n","").replace("\t","").replace("\r","").replace(" ","") ,
		'end_business_time ' : end_business_time.replace("\n","").replace("\t","").replace("\r","").replace(" ",""),
		'Roll_out_balance ' : Roll_out_balance.replace("\n","").replace("\t","").replace("\r","").replace(" ","") ,
	}

	return item

def main():
	url_1 = 'http://www.bjgjj.gov.cn/wsyw/wscx/gjj_cx.jsp?nicam=enpyenI3enk3eXI2ejJ6MnpycnI3NDkA&hskwe=R0pKd3czMzc1MjY2NjM0&vnv=JiMyMzgyODsmIzQwNTI3OwAA&lx=0'
	url_2 = 'http://www.bjgjj.gov.cn/wsyw/wscx/gjj_cx.jsp?nicam=enpyenI3enk3eXI2ejJ6MnpycnI3NDkA&hskwe=R0pKd3c4YzZ6d2E2NzAy&vnv=JiMyMzgyODsmIzQwNTI3OwAA&lx=0'
	url_3 = 'http://www.bjgjj.gov.cn/wsyw/wscx/gjj_cx.jsp?nicam=enpyenI3enk3eXI2ejJ6MnpycnI3NDkA&hskwe=R0pKd2M3emEyYzZhMzY2&vnv=JiMyMzgyODsmIzQwNTI3OwAA&lx=0'

	cookie = 'JSESSIONID=8AF3519FF052FE4B06E8355AA2D8DA7A.tomcat1; JSESSIONID=5498F46BC0C3EE6693D3C0B006E70F87.tomcat1'

	# 三个网页
	print(inner(url_1, cookie))  #
	print(inner(url_2, cookie))
	print(inner(url_3, cookie))
