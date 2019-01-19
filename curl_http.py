from urllib.parse import urlparse
import requests
import csv
import os
import re
import wx


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
                host = self.host.replace(self.urldist['user'] + '@', '')
                f = 'http://' + host + '/' + path

        if f.endswith('/'):
            return 4

        r = requests.get(f, timeout=10, allow_redirects=False)
        if r.status_code == 200:
            return 1
        code = ''
        try:
            code = r.status_code
        except Exception:
            return 5
        mes = 99
        if code == 401:
            r = requests.post(f, data={'some': 'data'}, auth=(
                self.urldist['user'],
                self.urldist['psd']), allow_redirects=False)
        if r.status_code == 200:
            mes = 1
        if '30' in str(r.status_code):
            mes = 6
        return mes

    def curl_main(self, psdlist=''):
        flag = self.url_check(psdlist)

        if flag == 1:
            localpath = self.cwd + '\\http\\' + \
                self.host + self.path.replace('/', '\\')
            if len(self.urldist) == 0:
                if self.scheme == "http":
                    cmd = '{}\\curl.exe {} -k --create-dirs --output {}'.format(
                        self.cwd, self.url, localpath)
                elif self.scheme == "https":
                    cmd = '{}\\curl.exe {} -k --create-dirs --output {}'.format(
                        self.cwd, self.url, localpath)
                else:
                    wx.MessageBox(u"想定外URL_code修正要: {}".format(self.url))
                    return False
            elif self.urldist['scheme'] == "http":
                cmd = '{}\\curl.exe -k -u {}:{} {} --create-dirs --output {}'.format(
                    self.cwd,
                    self.urldist['user'],
                    self.urldist['psd'],
                    self.url,
                    localpath)
            elif self.urldist['scheme'] == "ftp":
                cmd = '{}\\curl.exe -k -u {}:{} {} --create-dirs --output {}'.format(
                    self.cwd,
                    self.urldist['user'],
                    self.urldist['psd'],
                    self.url.replace('ftp', 'http'),
                    localpath)
            elif self.urldist['scheme'] == "sftp":
                self.path = self.path.replace(self.urldist['root'], '')
                localpath = self.cwd + '\\http\\' + self.host + '\\' + \
                    self.path.replace('/', '\\').replace(self.urldist['root'], '')
                cmd = '{}\\curl.exe -k -u {}:{} {} --create-dirs --output {}'.format(
                    self.cwd,
                    self.urldist['user'],
                    self.urldist['psd'],
                    'http://' + self.urldist['host'] + '/' + self.path,
                    localpath)
            else:
                wx.MessageBox(u"想定外URL_code修正要: {}".format(self.url))
                return False
        else:
            if flag == 99:
                pass
                wx.MessageBox(u"対象URL: {}".format(self.url), u'URL error')
            elif flag == 6:
                pass
                wx.MessageBox(u'リダイレクトしています: {}'.format(
                    self.url), u'URL error')
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
            except Exception:
                wx.MessageBox(u'system error')
        else:
            wx.MessageBox(u'実行不可')
        return False

    def __init__(self, url=''):
        self.url = url
        self.html = urlparse(url)
        self.host = re.sub(
            r'^[^@]*@', '', self.html.netloc) if '@' in self.html.netloc else self.html.netloc
        self.path = self.html.path
        self.cwd = os.getcwd()
        self.scheme = self.html.scheme


def main():
    psdlist = []
    app = wx.App()
    try:
        with open("list.txt", "rb") as f:
            items = f.read()
            urls = items.decode('utf-8').split()
        if urls is None:
            wx.MessageBox(u'urls is none')
            exit()
    except Exception:
        wx.MessageBox(u'list.txt is none')
        exit()
    try:
        with open("some.csv", "r") as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                psdlist.append({
                    "host": str(row[0]),
                    "user": str(row[1]),
                    "psd": str(row[2]),
                    "scheme": str(row[3]),
                    "root": str(row[4])
                })
        if psdlist is None:
            wx.MessageBox(u'some.csv read error')
            exit()
    except Exception:
        wx.MessageBox(u'some.csv is none')
        exit()
    for f in urls:
        curl = curlSup(f)
        curl.curl_main(psdlist)
    wx.MessageBox(u'処理完了')


if __name__ == '__main__':
    main()
