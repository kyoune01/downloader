#config: UTF-8
from urllib.parse import urlparse
import requests
import shutil
import csv
import os
import re
import wx
import time

class CurlFrame(wx.Frame):
	def __init__(self):
		super().__init__(None, wx.ID_ANY, "curl_downloader", size=(600, 500), style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
		CurlFrame.txtareaID = 1000
		CurlFrame.flag      = 0

		#statusBar
		self.CreateStatusBar()
		self.SetStatusText("stand bye...stand bye...")

		#main
		mainPanel = wx.Panel(self, wx.ID_ANY)
		#main config
		self.Bind(wx.EVT_CLOSE, self.closeFrame)
		#item
		notePanel = CurlFrame.NotePanel(mainPanel)
		btnPanel = CurlFrame.BtnPanel(mainPanel)
		#item config
		#btnPanel.SetBackgroundColour("#00ff00")
		#layout
		mainLayout = wx.FlexGridSizer(rows=2, cols=5, gap=(0, 0))
		mainLayout.Add(notePanel, flag=wx.GROW | wx.ALL, border=10)
		mainLayout.Add(btnPanel, flag=wx.GROW | wx.ALL, border=20)
		mainLayout.AddGrowableRow(0,1)
		mainLayout.AddGrowableCol(0,3)
		mainLayout.AddGrowableRow(1,1)
		mainLayout.AddGrowableCol(1,2)
		#set
		mainPanel.SetSizer(mainLayout)

	def closeFrame(self, ev):
		temp1000 = wx.FindWindowById(1000)
		temp1001 = wx.FindWindowById(1001)
		#lib.writeFile("init/temp1000.txt", temp1000.GetValue())
		#lib.writeFile("init/temp1001.txt", temp1001.GetValue())
		self.Destroy()

	class NotePanel(wx.Panel):
		def __init__(self, parent):
			super().__init__(parent, wx.ID_ANY)
			#item
			noteBook = wx.Notebook(self, 100)
			#item config
			tab1 = wx.Panel(noteBook, 110)
			tab2 = wx.Panel(noteBook, 111)
			noteBook.AddPage(tab1, 'Page 1')
			noteBook.AddPage(tab2, 'Page 2')
			tab1.SetBackgroundColour("#ff0000")
			noteBook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.setTxtareaID)
			CurlFrame.TxtAreaItem(tab1, 1000)
			CurlFrame.TxtAreaItem(tab2, 1001)
			#layout
			noteLayout = wx.BoxSizer(wx.VERTICAL)
			noteLayout.Add(noteBook, 1, flag= wx.EXPAND)
			#set
			self.SetSizer(noteLayout)

		def setTxtareaID(self, ev):
			index = ev.GetSelection()
			CurlFrame.txtareaID = 1000 if index == 0 else 1001

	class BtnPanel(wx.Panel):
		def __init__(self, parent):
			super().__init__(parent, wx.ID_ANY)
			#item
			APanel = CurlFrame.TxtAreaItem(self)
			BPanel = CurlFrame.SliderItem(self, 2000)
			CPanel = CurlFrame.BtnItem(self, "DL")
			#item config
			#APanel.SetBackgroundColour("#ff0000")
			#BPanel.SetBackgroundColour("#00ff00")
			#CPanel.SetBackgroundColour("#0000ff")
			#layout
			btnLayout = wx.FlexGridSizer(rows=12, cols=1, gap=(0, 0))
			btnLayout.Add(APanel, flag=wx.EXPAND)
			btnLayout.Add(BPanel, flag=wx.EXPAND)
			btnLayout.Add(CPanel, flag=wx.EXPAND)
			btnLayout.AddGrowableRow(0, 10)
			btnLayout.AddGrowableRow(1, 1)
			btnLayout.AddGrowableRow(2, 3)
			btnLayout.AddGrowableCol(0)
			#set
			self.SetSizer(btnLayout)

	class TxtAreaItem(wx.Panel):
		def __init__(self, parent, wxid=wx.ID_ANY):
			super().__init__(parent, wx.ID_ANY)
			#item
			textArea = wx.TextCtrl(parent, wxid, style=wx.TE_MULTILINE)
			#item config

			# キーの設定
			textArea.RegisterHotKey(1234, wx.MOD_CONTROL, 65)
			# ホットキーイベントハンドラ
			textArea.Bind(wx.EVT_HOTKEY, self.callhotkey)
			#txt = lib.readFile("init/temp"+wxid+".txt")
			#textArea.SetValue(txt)
			#layout
			Layout = wx.BoxSizer(wx.HORIZONTAL)
			Layout.Add(textArea, 1, flag= wx.EXPAND)
			#set
			parent.SetSizer(Layout)

		def callhotkey(self, ev):
			txtObj = wx.FindWindowById(1000) if CurlFrame.txtareaID == 1000 else wx.FindWindowById(CurlFrame.txtareaID)
			txtObj.SelectAll()

	class BtnItem(wx.Panel):
		def __init__(self, parent, txt, wxid=""):
			super().__init__(parent, wx.ID_ANY)
			wxid = wx.ID_ANY if wxid == "" else wxid
			#item
			btn = wx.Button(self, wxid, txt)
			#item config
			if txt == "DL":
				btn.Bind(wx.EVT_BUTTON, self.download)
			#layout
			Layout = wx.BoxSizer(wx.VERTICAL)
			Layout.Add(btn, 1, flag=wx.SHAPED | wx.ALIGN_CENTER | wx.ALL, border=20)
			#set
			self.SetSizer(Layout)

		def download(self, ev):
			txtObj = wx.FindWindowById(1000) if CurlFrame.txtareaID == 1000 else wx.FindWindowById(CurlFrame.txtareaID)
			CurlFrame.txt = txtObj.GetValue()	
			if CurlFrame.flag is not None:
				flagObj = wx.FindWindowById(2000)
				CurlFrame.flag = flagObj.GetValue()
			curlMain(CurlFrame.txt, CurlFrame.flag)

	class SliderItem(wx.Panel):
		def __init__(self, parent, wxid=wx.ID_ANY):
			super().__init__(parent, wx.ID_ANY)
			#item
			slider = wx.Slider(self, wxid)
			self.txt = wx.StaticText(self, wx.ID_ANY, 'FTP_only')
			#item config
			slider.SetMin(0)
			slider.SetMax(1)
			slider.Bind(wx.EVT_SLIDER, self.getVal)
			#layout
			Layout = wx.BoxSizer(wx.VERTICAL)
			Layout.Add(self.txt, 0, flag= wx.ALIGN_CENTER | wx.ALIGN_BOTTOM)
			Layout.Add(slider, 0, flag=wx.SHAPED | wx.ALL, border=20)
			#set
			self.SetSizer(Layout)

		def getVal(self, ev):
			val = ev.GetEventObject()
			CurlFrame.flag = val.GetValue()
			txt = 'HTTP_only' if val.GetValue() else 'FTP_only'
			self.txt.SetLabel(txt)

class curlSup(object):
	def get_psd(self, psdlist=''):
		psddic = [x for x in psdlist if x['host'] == self.host]
		if len(psddic) is not 0 and psddic[0]['scheme'] == 'http':
			psddic = [x for x in psddic if x['root'] in self.path]
		if len(psddic) is 0:
			return []
		else:
			return psddic[0]

	def url_check(self, psdlist=''):
		self.urldist = []
		f = self.url
		r = ''

		if len(self.scheme) == 0:
			return 2

		self.urldist = self.get_psd(psdlist)
		if len(self.urldist) == 0:
			if self.scheme == "http" or self.scheme == "https":
				f = self.url
			else:
				return 3
		else:
			if self.urldist['scheme'] == "ftp":
				f = self.url.replace('ftp', 'http')
			elif self.urldist['scheme'] == "sftp":
				path = re.sub(self.urldist['root'], '', self.path)
				host = self.host.replace(self.urldist['user']+'@', '')
				f = 'http://'+ host+ '/' + path

		if f.endswith('/'):
			return 4

		r = requests.get(f, timeout=10, allow_redirects=False)
		if r.status_code == 200:
			return 1
		code = ''
		try:
			code = r.status_code
		except Exception as ex:
			return 5
		mes = 99
		if code == 401:
			r = requests.post(f, data={'some':'data'}, auth=(self.urldist['user'], self.urldist['psd']), allow_redirects=False)
		if r.status_code == 200:
			mes = 1
		if '30' in str(r.status_code):
			mes = 6
		return mes

	def curl_http(self, psdlist=''):
		flag = self.url_check(psdlist)

		if flag == 1:
			localpath  = self.cwd +'\\http\\'+ self.host + self.path.replace('/', '\\')
			if len(self.urldist) == 0:
				if self.scheme == "http":
					cmd = '{}\\curl.exe {} -k --create-dirs --output {}'.format(self.cwd, self.url, localpath)
				elif self.scheme == "https":
					cmd = '{}\\curl.exe {} -k --create-dirs --output {}'.format(self.cwd, self.url, localpath)
				else:
					wx.MessageBox(u"想定外URL_code修正要: {}".format(self.url))
					return False
			elif self.urldist['scheme'] == "http":
				cmd = '{}\\curl.exe -k -u {}:{} {} --create-dirs --output {}'.format(self.cwd, self.urldist['user'], self.urldist['psd'], self.url, localpath)
			elif self.urldist['scheme'] == "ftp":
				cmd = '{}\\curl.exe -k -u {}:{} {} --create-dirs --output {}'.format(self.cwd, self.urldist['user'], self.urldist['psd'], self.url.replace('ftp', 'http'), localpath)
			elif self.urldist['scheme'] == "sftp":
				self.path = self.path.replace(self.urldist['root'], '')
				localpath = self.cwd +'\\http\\'+ self.host +'\\'+ self.path.replace('/', '\\').replace(self.urldist['root'], '')
				cmd = '{}\\curl.exe -k -u {}:{} {} --create-dirs --output {}'.format(self.cwd, self.urldist['user'], self.urldist['psd'], 'http://'+self.urldist['host']+'/'+self.path, localpath)
			else:
				wx.MessageBox(u"想定外URL_code修正要: {}".format(self.url))
				return False
		else:
			if flag == 99:
				pass
				wx.MessageBox(u"対象URL: {}".format(self.url), u'URL error')
			elif flag == 6:
				pass
				wx.MessageBox(u'リダイレクトしています: {}'.format(self.url), u'URL error')
			elif flag == 5:
				pass
				wx.MessageBox(u'サーバからの応答がない')
			elif flag == 4:
				pass
				wx.MessageBox(u'末尾が/のファイルはダウンロードできません')
			elif flag == 3:
				pass
				wx.MessageBox(u'ID・PASSが未登録です。')
			return False
		if cmd is not None:
			print(cmd)
			try:
				os.system(cmd)
				return True
			except Exception as e:
				wx.MessageBox(u'system error')
		else:
			wx.MessageBox(u'実行不可')
		return False

	def curl_ftp(self, psdlist=''):
		flag = self.url_check(psdlist)

		if flag == 1:
			if len(self.urldist) == 0:
				if self.scheme == "http" or self.scheme == "https":
					localpath  = self.cwd +'\\http\\'+ self.host + self.path.replace('/', '\\')
					cmd = '{}\\curl.exe {} -k --create-dirs --output {}'.format(self.cwd, self.url, localpath)
				else:
					wx.MessageBox(u"想定外URL_code修正要: {}".format(self.url))
					return False
			elif self.urldist['scheme'] == "http":
				localpath  = self.cwd +'\\http\\'+ self.host + self.path.replace('/', '\\')
				cmd = '{}\\curl.exe -k -u {}:{} {} --create-dirs --output {}'.format(self.cwd, self.urldist['user'], self.urldist['psd'], self.url, localpath)
			elif self.urldist['scheme'] == "ftp":
				localpath  = self.cwd +'\\ftp\\'+ self.host + self.path.replace('/', '\\')
				cmd = '{}\\curl.exe -k -u {}:{} {} --create-dirs --output {}'.format(self.cwd, self.urldist['user'], self.urldist['psd'], self.url.replace('http', 'ftp'), localpath)
			elif self.urldist['scheme'] == "sftp":
				self.path = self.path.replace(self.urldist['root'], '')
				localpath = self.cwd +'\\sftp\\'+ self.host +'\\'+ self.path.replace('/', '\\').replace(self.urldist['root'], '')
				cmd = '{}\\curl.exe -k -u {}:{} {} --create-dirs --output {}'.format(self.cwd, self.urldist['user'], self.urldist['psd'], 'sftp://'+self.urldist['host']+self.urldist['root']+self.path, localpath)
			else:
				wx.MessageBox(u"想定外URL_code修正要: {}".format(self.url))
				return False
		else:
			if flag == 99:
				pass
				wx.MessageBox(u"対象URL: {}".format(self.url), u'URL error')
			elif flag == 6:
				pass
				wx.MessageBox(u'リダイレクトしています: {}'.format(self.url), u'URL error')
			elif flag == 5:
				pass
				wx.MessageBox(u'サーバからの応答がない')
			elif flag == 4:
				pass
				wx.MessageBox(u'末尾が/のファイルはダウンロードできません')
			elif flag == 3:
				pass
				wx.MessageBox(u'ID・PASSが未登録です。')
			return False
		if cmd is not None:
			print(cmd)
			try:
				os.system(cmd)
				return True
			except Exception as e:
				wx.MessageBox(u'system error')
		else:
			wx.MessageBox(u'実行不可')
		return False

	def __init__(self, url=''):
		self.url  = url
		self.html = urlparse(url)
		self.host = re.sub(r'^[^@]*@','',self.html.netloc) if '@' in self.html.netloc else self.html.netloc
		self.path = self.html.path
		self.cwd  = os.getcwd()
		self.scheme   = self.html.scheme

def curlMain(urls, flag):
	psdlist = []
	cwd     = os.path.dirname(os.path.abspath(__file__))
	try:
		with open(cwd+"\\some.csv", "r") as f:
			reader = csv.reader(f)
			header = next(reader)
			for row in reader:
				psdlist.append({"host":str(row[0]), "user":str(row[1]), "psd":str(row[2]), "scheme":str(row[3]), "root":str(row[4])})
		if psdlist is None:
			wx.MessageBox(u'some.csv read error')
			exit()
	except Exception as ex:
		wx.MessageBox(u'some.csv is none:')
		exit()
	for f in urls.split():
		curl = curlSup(f)
		if flag is 1:
			curl.curl_http(psdlist)
		else:
			curl.curl_ftp(psdlist)
	wx.MessageBox(u'処理完了')

def main():
	app = wx.App()
	frame = CurlFrame()
	frame.Show()
	app.MainLoop()

if __name__ == '__main__':
	main()