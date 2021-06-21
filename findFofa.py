import pyfofa
import configparser
import socket
import socks
import tkinter.messagebox
import os
import sys

os.chdir(os.path.dirname(sys.path[0]))


class Go():
	"""docstring for Go"""
	def __init__(self):
		self.search = ''
		self.email = ''
		self.key = ''
		self.proxyIp = ''
		self.proxyPort = 0
		self.proxyUser = ''
		self.proxyPass = ''
		self.socket = socket.socket
		try:
			f = open('config.ini','r')
			self.config('api')
			self.hasconf = True
			f.close()
		except:
			self.hasconf = False
			f = open('config.ini','w')
			f.write('[api]\n[proxy]')
			f.close()
		# self.setProxy('175.24.60.104',19999)

	def setSearch(self, search):
		self.search = search
	
	def config(self, sec):
		cf = configparser.ConfigParser()
		cf.read('config.ini')
		if sec == 'api':
			self.email = cf.get('api','email')  
			self.key = cf.get('api','key')
		elif sec == 'proxy':
			self.proxyIp = cf.get('proxy','ip')
			self.proxyPort = cf.getint('proxy','port')
			self.proxyUser = cf.get('proxy','username')
			self.proxyPass = cf.get('proxy','password')
			
	def configKey(self,email,key):
		cf = configparser.ConfigParser()
		cf.read('config.ini')
		cf.set('api','email',email)
		cf.set('api','key',key)
		with open('config.ini','w') as f:
			cf.write(f)

	def configProxy(self,ip,port,username,password):
		cf = configparser.ConfigParser()
		cf.read('config.ini')
		cf.set('proxy','ip',ip)
		cf.set('proxy','port',port)
		cf.set('proxy','username',username)
		cf.set('proxy','password',password)
		with open('config.ini','w') as f:
			cf.write(f)

	def setProxy(self):
		'''
		设置socks5代理
		'''
		socks.set_default_proxy(socks.SOCKS5, self.proxyIp, self.proxyPort, username=self.proxyUser, password=self.proxyPass)
		socket.socket = socks.socksocket
		# print('socks open:'+self.proxyIp+str(self.proxyPort))

	def closeProxy(self):
		socket.socket = self.socket
		# print(requests.get("https://ifconfig.me/ip").text)

	def run(self, page):
		'''
		错误代码：
			-1:网络错误或封IP
			-2：超时
		'''
		try:
			search = pyfofa.FofaAPI(self.email, self.key)
		except:
			return -1

		# for host, ip in search.get_data('cert="baidu.com"', 1, "host,ip")['results']:
		#     print(host, ip)
		try:
			r = search.get_data(self.search,page,'host,ip,port,protocol,title')
		except:
			return -2

		return r
		# for i in r:
		# 	for j in i:
		# 		print(j,end='   ')
		# 	print('\n')



# if __name__ == '__main__':
# 	# go = Go(sys.argv[1])
# 	go = Go('ip="1.1.1.1"')
# 	go.run()