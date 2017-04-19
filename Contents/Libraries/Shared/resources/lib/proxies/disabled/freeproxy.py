import re,urllib,urlparse,base64,time

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import control
from resources.lib import resolvers


# Web Proxy
name = 'FreeProxy'
PROXY_URL = "https://freeproxy.io/o.php?b=4&mobile=&u="

class proxy:
	def __init__(self):
		self.base_link = 'https://freeproxy.io'
		self.name = name
		self.captcha = False
		self.ssl = False
		self.speedtest = 0
		self.headers = {'Connection' : 'keep-alive'}
		self.working = self.testSite()
		
	def testSite(self):
		x1 = time.time()
		http_res = client.request(url=self.base_link, output='responsecode')
		print "http_res : %s" % http_res
		self.speedtest = time.time() - x1
		if http_res not in client.HTTP_GOOD_RESP_CODES:
			return False
		return True
		
	def request(self, url, close=True, redirect=True, followredirect=False, error=False, proxy=None, post=None, headers=None, mobile=False, limit=None, referer=None, cookie=None, output='', timeout='30', httpsskip=False, use_web_proxy=False):
	
		if headers == None:
			headers = self.headers
		else:
			headers['Connection'] = self.headers['Connection']

		return requestdirect(url=url, close=close, redirect=redirect, followredirect=followredirect, error=error, proxy=proxy, post=post, headers=headers, mobile=mobile, limit=limit, referer=referer, cookie=cookie, output=output, timeout=timeout, httpsskip=httpsskip, use_web_proxy=use_web_proxy)
			
def requestdirect(url, close=True, redirect=True, followredirect=False, error=False, proxy=None, post=None, headers=None, mobile=False, limit=None, referer=None, cookie=None, output='', timeout='30', httpsskip=False, use_web_proxy=False):
	#try:
	print "Requesting: %s Using via: %s" % (url, PROXY_URL)
	
	urlhost = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
	
	if headers == None:
		headers = {'Connection' : 'keep-alive'}
	headers['User-Agent'] = client.randomagent()
	
	page_data_string = client.request(url = PROXY_URL + url, close=close, redirect=redirect, followredirect=followredirect, error=error, proxy=proxy, post=post, headers=headers, mobile=mobile, limit=limit, referer=referer, cookie=cookie, output=output, timeout=timeout, httpsskip=httpsskip, use_web_proxy=use_web_proxy)
	
	page_data_string = page_data_string.decode('utf-8')
	page_data_string = urllib.unquote_plus(page_data_string)
	page_data_string = page_data_string.encode('utf-8')
	
	page_data_string = page_data_string.replace('/o.php?b=4&amp;f=frame&amp;mobile=&amp;u=', '')
	page_data_string = page_data_string.replace('/o.php?b=4&amp;mobile=&amp;u=', '')
	page_data_string = page_data_string.replace('/o.php?b=4&mobile=&u=', '')
	
	
	
	# page_data_string_t = None
	# regex = r'{.*[token:]}]}'
	# matches = re.finditer(regex, page_data_string)
	# for matchNum, match in enumerate(matches):
		# page_data_string_t = match.group()
		# break
	# if page_data_string_t != None and 'token' in page_data_string_t:
		# page_data_string = page_data_string_t
	
	return page_data_string
	#except Exception as e:
	#	print "Error: %s - %s" % (name, e)	
	#	return None