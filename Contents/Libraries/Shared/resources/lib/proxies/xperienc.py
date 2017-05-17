import re,urllib,urlparse,base64,time,json

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import control
from resources.lib import resolvers


# Web Proxy
name = 'Xperienc'
PROXY_URL = "https://www.xperienc.com/browsexp.php?b=40&u="

class proxy:
	def __init__(self):
		self.base_link = 'https://www.xperienc.com'
		self.name = name
		self.captcha = False
		self.ssl = True
		self.speedtest = 0
		self.headers = {'Connection' : 'keep-alive', 'User-Agent' : client.randomagent()}
		self.working = self.testSite(disabled=False)
		
	def testSite(self, disabled=False):
		try:
			x1 = time.time()
			http_res = client.request(url=self.base_link, output='responsecode')
			self.speedtest = time.time() - x1
			
			if disabled == True:
				return False
			
			if http_res not in client.HTTP_GOOD_RESP_CODES:
				return False
			return True
		except:
			return False
		
	def request(self, url, close=True, redirect=True, followredirect=False, error=False, proxy=None, post=None, headers=None, mobile=False, limit=None, referer=None, cookie=None, output='', timeout='30', httpsskip=False, use_web_proxy=False, XHR=False, IPv4=False):
	
		if self.working == False:
			print "Proxy: %s is disabled internally" % (name)
			return None
	
		if headers == None:
			headers = self.headers

		return requestdirect(url=url, close=close, redirect=redirect, followredirect=followredirect, error=error, proxy=proxy, post=post, headers=headers, mobile=mobile, limit=limit, referer=referer, cookie=cookie, output=output, timeout=timeout, httpsskip=httpsskip, use_web_proxy=use_web_proxy, XHR=XHR, IPv4=IPv4)
			
def requestdirect(url, close=True, redirect=True, followredirect=False, error=False, proxy=None, post=None, headers=None, mobile=False, limit=None, referer=None, cookie=None, output='', timeout='30', httpsskip=False, use_web_proxy=False, XHR=False, IPv4=False):

	print "Requesting: %s Using via: %s" % (url, PROXY_URL)
	
	urlhost = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
	
	if headers == None:
		headers = {'Connection' : 'keep-alive'}
		headers['User-Agent'] = client.randomagent()
	
	res = client.request(url = PROXY_URL + url, close=close, redirect=redirect, followredirect=followredirect, error=error, proxy=proxy, post=post, headers=headers, mobile=mobile, limit=limit, referer=referer, cookie=cookie, output=output, timeout=timeout, httpsskip=httpsskip, use_web_proxy=use_web_proxy, XHR=XHR, IPv4=IPv4)
	
	page_data_string = client.getPageDataBasedOnOutput(res, output)
	
	pattern = re.compile('<script[\s\S]+?/script>')
	page_data_string = re.sub(pattern, '', page_data_string)
		
	try:
		page_data_string = page_data_string.replace('\n','')	
		#page_data_string = page_data_string.replace('\r','r').replace('\n','<br/>').replace('\w','').replace('\.','').replace('\t','').replace('\ ','')
	except Exception as e:
		control.log("Error1: %s - %s" % (name, e))
		
	#print page_data_string

	page_data_string = json.dumps(page_data_string)
	page_data_string = page_data_string.replace('\\','')
	page_data_string = page_data_string[1:-1]
	
	#print page_data_string
	#page_data_string = str(page_data_string)
	
	try:
		r = unicode(page_data_string, "utf-8")
		page_data_string = r
	except Exception as e:
		control.log("Error2: %s - %s" % (name, e))
		try:
			r = str(page_data_string)
			page_data_string = r
		except Exception as e:
			control.log("Error3: %s - %s" % (name, e))
	
	page_data_string = page_data_string.replace('https://www.xperienc.com/browsexp.php?', '')
	page_data_string = page_data_string.replace('b=40', '')
	page_data_string = page_data_string.replace('u=', '')
	page_data_string = page_data_string.replace('browsexp.php?', '')
	page_data_string = page_data_string.replace('&http', 'http')
	page_data_string = page_data_string.replace('/http', 'http')
	
	page_data_string = page_data_string.decode('utf-8')
	page_data_string = urllib.unquote_plus(page_data_string)
	page_data_string = page_data_string.encode('utf-8')
	
	return client.getResponseDataBasedOnOutput(page_data_string, res, output)
