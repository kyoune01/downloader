# config: UTF-8
import asyncio
import time
from ftplib import FTP
import os
import re


async def __downloader(urldata):

    try:
        ftp = FTP(urldata['domain'], urldata['id'], passwd=urldata['pass'])
        ftp.cwd(urldata['root'])
    except Exception:
        raise ValueError('not connection')

    async def __run_request(path, urldata, ftp):
        loop = asyncio.get_event_loop()
        sem = asyncio.Semaphore(5)
        async with sem:
            return await loop.run_in_executor(None, __downloadFtp, path, urldata['domain'], ftp)

    tasks = [__run_request(path, urldata, ftp) for path in urldata['path']]
    return await asyncio.gather(*tasks)


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
        raise ValueError('not connection')

    sem = asyncio.Semaphore(5)

    async def __run_request(path, domain, ftp):
        async with sem:
            return await __downloadFtp(path, domain, ftp)

    tasks = [__run_request(path, urldata['domain'], ftp)
             for path in urldata['path']]
    return await asyncio.gather(*tasks)


async def __downloadFtp(path, domain, ftp):
    await asyncio.sleep(1)

    localPath = './ftp/' + domain + path

    localDir = re.sub(r'[^/]*\.[^\.]*$', '', localPath[2:])
    os.makedirs(localDir, exist_ok=True)

    try:
        print('start : ' + localPath)
        with open(localPath, 'wb') as f:
            # 対象ファイルをバイナリ転送モードで取得
            ftp.retrbinary('RETR ' + path, f.write)
        print('finish: ' + localPath)
    except Exception as e:
        pass
        # raise ValueError('not download')

    return path
