# config: UTF-8
import re
from urllib.parse import urlparse


class urlData():

    def __init__(self, psdlist):
        self.category = ''
        self.psdlist = psdlist
        self.path = ''
        self._url = ''

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        # url をパース
        html = urlparse(url)
        # url だと判断できなければ終了
        if len(html.scheme) == 0:
            self._url = None
            return True
        self._url = url
        self.scheme = html.scheme
        self.path = html.path
        self.host = re.sub(
            r'^[^@]*@',
            '',
            html.netloc) if '@' in html.netloc else html.netloc
        self.psdlist = self.__setPsdList()

    def __setPsdList(self):
        """
            host と path からサーバー情報を探す
            @param  string host    ホスト情報（アドレス）
            @param  string path    パス
            @return array  psddic  サーバー情報
        """
        psddic = [x for x in self.psdlist if x['domain'] == self.host]
        if len(psddic) != 0 and psddic[0]['scheme'] == 'basic':
            psddic = [x for x in psddic if x['root'] in self.path]
        if len(psddic) == 0:
            return {}
        else:
            return psddic[0]


async def convertUrlFormat(text, category, psdlist):
    urls = urlData(psdlist)
    urls.category = category
    urls.url = text
    if urls.url != None:
        return urls
    else:
        raise ValueError('error')
