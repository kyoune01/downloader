# config: UTF-8
import asyncio
from ftplib import FTP
import os
import re
import paramiko


async def downloader(urldata):
    """
    ダウンローダー
    @param  urldata {dict}
        {domain:'', id:'', pass:'', root:'', scheme:'' path:[path1,path2...]}
    @return result
    """
    domain = urldata['domain']
    user = urldata['id']
    passwd = urldata['pass']
    root = urldata['root']
    pathList = urldata['path']
    scheme = urldata['scheme']
    result = []

    if scheme == 'ftp':
        result = await __downloaderFTP(domain, user, passwd, root, pathList)
    elif scheme == 'sftp':
        result = await __downloaderSFTP(domain, user, passwd, root, pathList)
    else:
        raise ValueError(domain, 'unknown scheme')

    if result == []:
        raise ValueError(domain, 'what happen')

    return result


async def __downloaderFTP(domain, user, passwd, root, pathList):
    # 接続開始
    try:
        client = FTP(domain, user, passwd=passwd)
    except Exception:
        raise ValueError(domain, 'not connection')

    sem = asyncio.Semaphore(5)

    async def __run_request(root, path, domain, client):
        async with sem:
            return await __downloadFTP(root, path, domain, client)

    tasks = [__run_request(root, path, domain, client) for path in pathList]
    result = await asyncio.gather(*tasks, return_exceptions=True)

    # 接続終了
    client.quit()
    return result


async def __downloaderSFTP(domain, user, passwd, root, pathList):
    # 接続開始
    try:
        connection = paramiko.Transport((domain, 22))
        connection.connect(username=user, password=passwd)
        client = paramiko.SFTPClient.from_transport(connection)
    except Exception:
        raise ValueError(domain, 'not connection')

    sem = asyncio.Semaphore(5)

    async def __run_request(root, path, domain, client):
        async with sem:
            return await __downloadSFTP(root, path, domain, client)

    tasks = [__run_request(root, path, domain, client)
             for path in pathList]
    result = await asyncio.gather(*tasks, return_exceptions=True)

    # 接続終了
    connection.close()
    client.close()
    return result


async def __downloadFTP(root, path, domain, ftp):
    await asyncio.sleep(1)

    # 保存先
    localPath = './ftp/' + domain + path
    remotePath = root + path

    # ファイルの存在確認
    try:
        ftp.size(remotePath)
    except Exception:
        print(f'faild: {path}')
        return {'url': path, 'status': False, 'message': 'file not found'}

    # ディレクトリが存在しなければつくる
    localDir = re.sub(r'[^/]*\.[^\.]*$', '', localPath[2:])
    os.makedirs(localDir, exist_ok=True)

    # ダウンロード処理
    try:
        with open(localPath, 'wb') as f:
            # 対象ファイルをバイナリ転送モードで取得
            ftp.retrbinary('RETR ' + remotePath, f.write)
    except Exception as e:
        print(f'faild: {path}')
        return {
            'url': path,
            'status': False,
            'message': f'faild download status:{e}'
        }

    print(f'download: {path}')
    return {'url': path, 'status': True, 'message': 'success'}


async def __downloadSFTP(root, path, domain, sftp):
    await asyncio.sleep(1)

    # 保存先
    localPath = './ftp/' + domain + path
    remotePath = root + path

    # ファイルの存在確認
    try:
        sftp.stat(remotePath)
    except Exception as e:
        print(e)
        print(f'faild: {path}')
        return {'url': path, 'status': False, 'message': 'file not found'}

    # ディレクトリが存在しなければつくる
    localDir = re.sub(r'[^/]*\.[^\.]*$', '', localPath[2:])
    os.makedirs(localDir, exist_ok=True)

    # ダウンロード処理
    try:
        sftp.get(remotePath, localPath)
    except Exception as e:
        print(f'faild: {path}')
        return {
            'url': path,
            'status': False,
            'message': f'faild download status:{e}'
        }

    print(f'download: {path}')
    return {'url': path, 'status': True, 'message': 'success'}
