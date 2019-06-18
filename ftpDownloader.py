# config: UTF-8
import asyncio
import time
from ftplib import FTP
import os
import re


async def downloader(urldata):
    """
    ダウンローダー

    @param  urldata {dict}
        {'domain':'', 'id':'', 'pass':'', 'root':'', 'path':['path','path'...]}
    @return result  {string}        -val encode
    """
    try:
        ftp = FTP(urldata['domain'], urldata['id'], passwd=urldata['pass'])
        ftp.cwd(urldata['root'])
    except Exception:
        raise ValueError(urldata['domain'], f'not connection')

    sem = asyncio.Semaphore(5)

    async def __run_request(path, domain, ftp):
        async with sem:
            return await __downloadFtp(path, domain, ftp)

    tasks = [__run_request(path, urldata['domain'], ftp)
             for path in urldata['path']]
    res = await asyncio.gather(*tasks)

    # 接続はきちんと閉じる
    ftp.quit()
    return res


async def __downloadFtp(path, domain, ftp):
    await asyncio.sleep(1)

    # ファイルの存在確認
    try:
        ftp.size(path)
    except Exception:
        raise ValueError(path, f'file not found')

    # 保存先
    localPath = './ftp/' + domain + path

    # ディレクトリが存在しなければつくる
    localDir = re.sub(r'[^/]*\.[^\.]*$', '', localPath[2:])
    os.makedirs(localDir, exist_ok=True)

    # ダウンロード処理
    try:
        with open(localPath, 'wb') as f:
            # 対象ファイルをバイナリ転送モードで取得
            ftp.retrbinary('RETR ' + path, f.write)
        print('download : ' + path)
    except Exception as e:
        raise ValueError(path, f'faild download status:{e}')

    return path
