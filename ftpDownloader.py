# config: UTF-8
import urllib.request as URLLIB
import re
import os
import asyncio
import encodings.idna
import time


async def downloader(urldata):
    loop = asyncio.get_event_loop()
    sem = asyncio.Semaphore(5)
    async with sem:
        return await loop.run_in_executor(None, downloadFtp, urldata)


def downloadFtp(urldata):
    time.sleep(1)
    # some.csv に登録のないURLを弾く
    if urldata['psdlist'] == {} or urldata['psdlist']['scheme'] != 'ftp':
        raise ValueError(
            urldata['url'],
            f'not Setting'
        )

    path = urldata['path']
    host = urldata["psdlist"]["domain"]
    user = urldata["psdlist"]["id"]
    psd = urldata["psdlist"]["pass"]

    ftppath = path
    if (
        urldata['psdlist']['root'] != '/' and
        not re.match(urldata['psdlist']['root'], path)
    ):
        # ドキュメントルートからのパスにする
        ftppath = urldata['psdlist']['root'] + path

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
    try:
        file_path = os.path.dirname(filename)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
    except Exception:
        # エラーを握りつぶす
        pass
    # 結果を保存
    with open(filename, 'wb') as f:
        f.write(value)
