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

    loop = asyncio.get_event_loop()
    downloadTasks = [__run_request(path, urldata['domain'], ftp)
                     for path in urldata['path']]
    wait_coro = asyncio.wait(downloadTasks, loop=None)
    res, _ = loop.run_until_complete(wait_coro)
    # 接続はきちんと閉じる
    ftp.quit()
    success = []
    error = []
    for future in res:
        try:
            # ここでエラーを吐かせる
            success.append(future.result())
        except Exception as e:
            error.append([e.args[0], e.args[1]])

    return success, error


async def __downloadFtp(path, domain, ftp):
    await asyncio.sleep(1)

    # ファイルの存在確認
    try:
        ftp.size(path)
    except Exception:
        raise ValueError(path, 'file not found')

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
