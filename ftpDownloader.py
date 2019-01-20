# config: UTF-8
# from ftplib import FTP
import urllib.request as URLLIB
import re
import os
import asyncio
import encodings.idna


async def downloader(urldata):
    loop = asyncio.get_event_loop()
    sem = asyncio.Semaphore(5)
    async with sem:
        return await loop.run_in_executor(None, downloadFtp, urldata)


def downloadFtp(urldata):
    # some.csv に登録のないURLを弾く
    if urldata['psdlist'] == {} or urldata['psdlist']['category'] != 'ftp':
        raise ValueError(
            urldata['url'],
            f'not Setting'
        )

    path = urldata['path']
    host = urldata["psdlist"]["host"]
    user = urldata["psdlist"]["user"]
    psd = urldata["psdlist"]["psd"]

    ftppath = path
    if (
        urldata['psdlist']['webroot'] != '/' and
        not re.match(urldata['psdlist']['webroot'], path)
    ):
        # ドキュメントルートからのパスにする
        ftppath = urldata['psdlist']['webroot'] + path

    try:
        ret = URLLIB.urlopen(f'ftp://{user}:{psd}@{host}{ftppath}').read()
    except Exception as e:
        raise ValueError(
            urldata['url'],
            e.args[0]
        )

    print(f'{urldata["url"]} sucusess')
    saveResult(host, path, ret)
    return urldata['url']


def saveResult(host, path, value):
    # DL 成功
    filename = './ftp/' + host + path
    # ディレクトリがなければ作る
    file_path = os.path.dirname(filename)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    # 結果を保存
    with open(filename, 'wb') as f:
        f.write(value)
