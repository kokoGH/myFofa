import findFofa
import tkinter
from tkinter import ttk
import tkinter.messagebox
import pyperclip


class guiCommand():
	def __init__(self):
		pass
		# self.search = ''
		# self.result = []
		self.pages = 1
		self.page = 1
		self.go = findFofa.Go()
		if not self.go.hasconf:
			tkinter.messagebox.showinfo('api error','请先配置api key！')

	def start(self):
		'''搜索'''
		s = text.get()
		# tree.insert("", 0, values=("卡恩", "18", "180", "65", "title"))	# #给第0行添加数据，索引值可重复
		for item in tree.get_children():
			tree.delete(item)
		# go = findFofa.Go(s)
		# response = go.run(self.page)
		self.go.setSearch(s)
		response = self.go.run(self.page)
		# print(response)
		if response == -1:
			tkinter.messagebox.showinfo('network error','请检查网络，被封IP请添加代理')
			return 0
		if response['error']:
			tkinter.messagebox.showinfo('fofa error',response['errmsg'])
			return 0
		r = response['results']

		self.pages = response['size']//100 + 1
		label_page['text'] = str(self.page) + '/' + str(self.pages)

		for i in range(len(r)):
			tree.insert("",i,values=(r[i]))

	def search(self):
		self.page = 1
		self.start()

	def next(self):
		if self.page == self.pages:
			return 0
		else:
			self.page += 1
			self.start()

	def previous(self):
		if self.page == 1:
			return 0
		else:
			self.page -= 1
			self.start()

	def jump(self):
		try:
			numb = int(entry_page.get())
		except:
			return 0
		if numb > 0 and numb <= self.pages:
			self.page = numb
			self.start()
		else:
			return 0

	def writeClipboard(self,string):
		pyperclip.copy(string)

	def rclick(self,event):
		'''列表事件：右击复制ip:port'''
		item = tree.selection()
		x = tree.item(item,"values")
		if item:
			self.writeClipboard(x[0])

	def save(self):
		s = entry_page.get()
		# print(s)

	def setProxy(self):
		try:
			self.go.config('proxy')
		except:
			tkinter.messagebox.showinfo('配置错误','请检查配置')
			self.go.closeProxy()
			return 0
		self.go.setProxy()

	def closeProxy(self):
		self.go.closeProxy()

	def configKey(self):
		top1 = tkinter.Toplevel(top)

		frame1 = tkinter.Frame(top1)
		frame2 = tkinter.Frame(top1)
		frame3 = tkinter.Frame(top1)
		
		label1 = tkinter.Label(frame1,text='email')
		# text = tkinter.StringVar(top1)
		entry1 = tkinter.Entry(frame1,borderwidth=1) 
		# entry['textvariable'] = text  

		label2 = tkinter.Label(frame2,text='  key  ')
		entry2 = tkinter.Entry(frame2)

		button1 = tkinter.Button(frame3,text='确定',command=lambda:[self.go.configKey(entry1.get(),entry2.get()),self.go.config('api'),top1.destroy()])

		frame1.pack(side='top')
		frame2.pack(side='top')
		frame3.pack(side='bottom')

		label1.pack(side='left',anchor='nw',expand='no',padx=1)
		entry1.pack(side='right',anchor='ne',expand='no',padx=1)
		label2.pack(side='left',anchor='sw',expand='no',padx=1)
		entry2.pack(side='right',anchor='se',expand='no',padx=1)
		button1.pack(side='top')


	def configProxy(self):
		top1 = tkinter.Toplevel(top)

		frame1 = tkinter.Frame(top1)
		frame2 = tkinter.Frame(top1)
		frame3 = tkinter.Frame(top1)
		frame4 = tkinter.Frame(top1)
		frame5 = tkinter.Frame(top1)
		
		label1 = tkinter.Label(frame1,text='  ip  ')
		# text = tkinter.StringVar(top1)  
		entry1 = tkinter.Entry(frame1,borderwidth=1) 
		# entry['textvariable'] = text  

		label2 = tkinter.Label(frame2,text='port')
		entry2 = tkinter.Entry(frame2)

		label3 = tkinter.Label(frame3,text='user')
		entry3 = tkinter.Entry(frame3)

		label4 = tkinter.Label(frame4,text='pass')
		entry4 = tkinter.Entry(frame4)

		button1 = tkinter.Button(frame5,text='确定',command=lambda:[self.go.configProxy(entry1.get(),entry2.get(),entry3.get(),entry4.get()),self.go.config('proxy'),top1.destroy()])

		frame1.pack(side='top')
		frame2.pack(side='top')
		frame3.pack(side='top')
		frame4.pack(side='top')
		frame5.pack(side='bottom')

		label1.pack(side='left',anchor='nw',expand='no',padx=1)
		entry1.pack(side='right',anchor='ne',expand='no',padx=1)
		label2.pack(side='left',anchor='sw',expand='no',padx=1)
		entry2.pack(side='right',anchor='se',expand='no',padx=1)
		label3.pack(side='left',anchor='sw',expand='no',padx=1)
		entry3.pack(side='right',anchor='se',expand='no',padx=1)
		label4.pack(side='left',anchor='sw',expand='no',padx=1)
		entry4.pack(side='right',anchor='se',expand='no',padx=1)

		button1.pack(side='top')

if __name__ == '__main__':

	top=tkinter.Tk(className=' FOFA CLIENT  --by SELAX') 
	top.geometry("%dx%d" % (1200, 700))
	# top.grid_rowconfigure(minsize=5)
	command = guiCommand()
	#菜单栏-----------------------------------------------
	menubar = tkinter.Menu(top)  
	proxy = tkinter.Menu(menubar, tearoff=0)
	config = tkinter.Menu(menubar, tearoff=0)
	menubar.add_cascade(label='代理', menu=proxy)
	menubar.add_cascade(label='配置', menu=config)

	proxy.add_command(label='开启', command=lambda:command.setProxy())
	proxy.add_command(label='关闭', command=command.closeProxy)

	config.add_command(label='账号设置', command=command.configKey)
	config.add_command(label='代理设置', command=command.configProxy)

	#菜单栏结束-------------------------------------------


	frame1 = tkinter.Frame(top) #搜索栏容器

	# frame2 = tkinter.Frame(top) #数据标题栏容器

	frame3 = tkinter.Frame(top) #数据栏容器
	frame4 = tkinter.Frame(top) #分页栏容器
	# frame5 = tkinter.Frame(top) #底部保存容器

	frame1.pack(side='top',fill='x',anchor='n')
	# frame2.pack(side='top',fill='x',anchor='center',padx=5)
	frame3.pack(side='top',fill='both',expand='yes',anchor='s',padx=5)
	frame4.pack(side='bottom',fill='x',expand='no',anchor='n',padx=5,pady=30)
	# frame5.pack(side='bottom',fill='x',expand='yes',anchor='s',padx=5)

	#搜索栏----------------------------------------
	text = tkinter.StringVar(frame1)
	text.set('输入查询规则')  
	entry = tkinter.Entry(frame1,borderwidth=1) 
	entry['textvariable'] = text  


	#搜索按钮
	button = tkinter.Button(frame1)               
	button['text'] = 'search'
	button['command'] = command.search

	entry.pack(side='left',anchor='center',expand='yes',fill='x',padx=5)
	button.pack(side='right',anchor='w',padx='50',pady=5)


	#结果显示区域------------------------------------
	tree = ttk.Treeview(frame3,show="headings")	# #创建表格对象
	tree["columns"] = ("host", "ip", "port", "protocol","title")	# #定义列

	tree.column("host", width=100, anchor='center')	# #设置列
	tree.column("ip", width=100, anchor='center')
	tree.column("port", width=100, anchor='center')
	tree.column("protocol", width=100, anchor='center')
	tree.column("title", width=100, anchor='center')

	tree.heading("host", text="host")	# #设置显示的表头名
	tree.heading("ip", text="ip")
	tree.heading("port", text="port")
	tree.heading("protocol", text="protocol")
	tree.heading("title", text="title")

	tree.pack(side='left',expand='yes',fill='both')
	tree.bind('<ButtonRelease-3>',command.rclick)

	#滚动条
	VScroll1 = tkinter.Scrollbar(frame3, orient='vertical', command=tree.yview)
	VScroll1.pack(side='right',fill='y')
	# 给treeview添加配置
	tree.configure(yscrollcommand=VScroll1.set)

	#分页容器---------------------------------
	button_previous = tkinter.Button(frame4)
	button_previous['text'] = '上一页'
	button_previous['command'] = command.previous
	button_previous.pack(side='left',anchor='center',padx='50',pady=5)

	label_page = tkinter.Label(frame4,text="/")
	label_page.pack(side='left',anchor='center')

	button_next = tkinter.Button(frame4)
	button_next['text'] = '下一页'
	button_next['command'] = command.next 
	button_next.pack(side='left',anchor='center',padx='50',pady=5)
	#################TODO######################
	entry_page = tkinter.Entry(frame4,width=3) 
	entry_page.place(width=10, height=50)
	entry_page.pack(side='left',anchor='center',expand='no',padx='10',pady=5)

	button_go = tkinter.Button(frame4)
	button_go['text'] = '跳转'
	button_go['command'] = command.jump
	button_go.pack(side='left',anchor='center',padx='10',pady=5)

	button_save = tkinter.Button(frame4)
	button_save['text'] = '保存'
	button_save['command'] = command.save
	button_save.pack(side='right',anchor='center',padx='100',pady=5)

	#################TODO######################

	#底部容器--------------------------------
	top.config(menu=menubar)
	top.mainloop()
