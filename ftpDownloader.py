# config: UTF-8
from ftplib import FTP
import re
import os
import asyncio


async def downloader(urldata):
    loop = asyncio.get_event_loop()
    sem = asyncio.Semaphore(5)
    async with sem:
        return await loop.run_in_executor(None, downloadFtp, urldata)


def downloadFtp(urldata):
    path = urldata['path']
    host = urldata['host']
    if urldata['psdlist'] == [] or urldata['psdlist']['category'] != 'ftp':
        # some.csv に登録のないURLを弾く
        raise ValueError(
            urldata['url'],
            urldata['category'],
            f'not Setting'
        )
    if (
        urldata['psdlist']['webroot'] != '/' and
        not re.match(urldata['psdlist']['webroot'], path)
    ):
        # host を名前のみにする
        ftppath = urldata['psdlist']['webroot'] + path
    host = urldata['host'].replace(urldata['psdlist']['user'] + '@', '')

    ret = []
    with FTP(host) as ftp:
        ftp.login(urldata['psdlist']['user'], urldata['psdlist']['psd'])
        ftp.retrlines('RETR ' + ftppath, ret.append)
    saveResult(host, path, ''.join(ret))


def saveResult(host, path, text):
    # DL 成功
    filename = './ftp/' + host + path
    # ディレクトリがなければ作る
    file_path = os.path.dirname(filename)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    # 結果を保存
    with open(filename, 'w') as f:
        f.write(text)
