from PIL import Image
import requests
from lxml import etree
from selenium import webdriver
import time
import re
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
class BjGjj():
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

		# driver.find_element_by_xpath(
		# 	'/html/body/table[2]/tbody/tr[3]/td/table/tbody/tr/td/div/form/div[1]/ul/li[3]/a').click()
		# driver.find_element_by_id("1").click()  # 点击到身份证


		# 输入账号密码
		driver.find_element_by_id("i_username").send_keys(self.user)
		driver.find_element_by_id("i_password").send_keys(self.password)


		# 识别验证码
		self.code_img('code.png', 'code.png')
		code = input('验证码：')

		# 输入验证码， 点击登录
		driver.find_element_by_id('i_safecode').send_keys(code)
		driver.find_element_by_xpath('//*[@id="indform"]/div[4]/input').click()


		# 判断是否登录成功
		for i in range(20):
			try:
				driver.find_element_by_xpath('//*[@id="new-mytable"]/tbody/tr[1]/th[2]/div/text()')
				break
			except:
				time.sleep(0.1)

		# 提取网址 进行拼接
		'''
		text = driver.page_source
		html = etree.HTML(text)
		java_onclick = html.xpath('//*[@id="new-mytable"]/tbody/tr/td/div/a/@onclick')
		url_list = []
		for onclick in java_onclick:
			url_list.append('http://www.bjgjj.gov.cn/wsyw/wscx/gjj_cx.jsp?' + re.findall(r'\?(.*?)"', onclick)[0])
		'''

		# 获取cookie
		cookie_list = driver.get_cookies()
		for cookie_dict in cookie_list:
			self.cookie += cookie_dict['name'] + '=' + cookie_dict['value'] + ';'  # 拼接cookie

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
		return

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

		# item['have_insurance'] = info_list[2].xpath('./text()')[0] if info_list[2].xpath(
			# './text()') else ''  # 参加险种  （列表格式没有处理）
		item['name'] = info_list[5].xpath('./text()')[0] if info_list[5].xpath('./text()') else ''  # 姓名
		item['idcard'] = info_list[7].xpath('./text()')[0] if info_list[7].xpath('./text()') else ''  # 公民身份证号码
		# item['sex'] = info_list[9].xpath('./text()')[0] if info_list[9].xpath('./text()') else ''  # 性别
		# item['born_day'] = info_list[11].xpath('./text()')[0] if info_list[11].xpath('./text()') else ''  # 出生日期
		# item['peoples'] = info_list[13].xpath('./text()')[0] if info_list[13].xpath('./text()') else ''  # 民族
		# item['country'] = info_list[15].xpath('./text()')[0] if info_list[15].xpath('./text()') else ''  # 国家/地区
		item['individual_identity'] = info_list[17].xpath('./text()')[0] if info_list[17].xpath(
			'./text()') else ''  # 个人身份
		# item['work_dates'] = info_list[19].xpath('./text()')[0] if info_list[19].xpath('./text()') else ''  # 参加工作日期
		# item['city'] = info_list[23].xpath('./text()')[0] if info_list[23].xpath('./text()') else ''  # 户口性质
		# item['city_addr'] = info_list[25].xpath('./text()')[0] if info_list[25].xpath('./text()') else ''  # 户口所在地地址
		# item['city_code'] = info_list[27].xpath('./text()')[0] if info_list[27].xpath('./text()') else ''  # 户口所在地邮政编码
		# item['live_addr'] = info_list[29].xpath('./text()')[0] if info_list[29].xpath('./text()') else ''  # 居住地（联系）地址
		# item['live_code'] = info_list[31].xpath('./text()')[0] if info_list[31].xpath('./text()') else ''  # 居住地（联系）邮政编码
		# item['culture'] = info_list[40].xpath('./text()')[0] if info_list[40].xpath('./text()') else ''  # 文化程度
		# item['applicant_phone'] = info_list[43].xpath('./text()')[0] if info_list[43].xpath('./text()') else ''  # 参保人电话
		# item['applicant_tel'] = info_list[45].xpath('./text()')[0] if info_list[45].xpath('./text()') else ''  # 参保人手机
		# item['months_revenue'] = info_list[47].xpath('./text()')[0] if info_list[47].xpath(
		# 	'./text()') else ''  # 申报月均工资收入（元）
		# item['Banks'] = info_list[53].xpath('./text()')[0] if info_list[53].xpath('./text()') else ''  # 委托代发银行名称
		# item['banks_code'] = info_list[55].xpath('./text()')[0] if info_list[55].xpath('./text()') else ''  # 银行账号
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
		for tr in tr_lxml[2:]:
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

	def start(self):
		# 获取cookie
		# self.get_cookie_urls()

		# 测试用 headers
		self.cookie = 'JSESSIONID=F849C2A256859D4E680DB2AF031B94BB; mjrzMBJgZO=MDAwM2IyYWYyZjQwMDAwMDAwMDgwdX1FGRUxNTA2NTE4MDc0; _gscs_2065735475=t064911527at1ie22|pv:2; _gscbrs_2065735475=1; _gscu_2065735475=06417242mcjo0j22'


		self.headers = {
			'Cookie': self.cookie,
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
		}
		# 上面测试用------------


		# 个人基本信息查询， 返回数据
		me_info_url = 'http://www.bjrbj.gov.cn/csibiz/indinfo/search/ind/indNewInfoSearchAction'
		item = self.me_info(me_info_url)
		print(item)

		# 历史缴费信息
		history_dict = self.get_history_many(2)
		print(history_dict)

		# 社保卡办理状态查询
		state_list = self.get_card_state()
		print(state_list)


if __name__ == '__main__':
	bjgjj = BjGjj('360403199307261840', '810064mn')
	bjgjj.start()

