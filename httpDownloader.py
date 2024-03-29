# config: UTF-8
import requests
import re
import os
import asyncio
import time


async def downloader(urldata):
    loop = asyncio.get_event_loop()
    sem = asyncio.Semaphore(5)
    async with sem:
        return await loop.run_in_executor(None, downloadHttp, urldata)


def downloadHttp(urldata):
    time.sleep(1)
    path = urldata['path']
    host = urldata['host']
    scheme = urldata['scheme']

    # 変換処理＋DL
    if urldata['psdlist'] == {}:
        # some.csv に登録のないURL
        url = urldata['url']
        res = requests.get(url, verify=False)
    elif urldata['psdlist']['scheme'] == 'http':
        # basic 認証が設定されてるURL
        if scheme != 'http' or scheme != 'https':
            # scheme がhttp(s)以外であれば修正
            scheme = 'https' if urldata['psdlist'][
                'isTLS'] == 'true' else 'http'
        url = scheme + '://' + host + path
        res = requests.post(
            url,
            auth=(urldata['psdlist']['id'], urldata['psdlist']['pass']),
            verify=False
        )
    else:
        # ftp などファイルサーバーが設定されているURL
        if scheme != 'http' or scheme != 'https':
            # scheme がhttp(s)以外であれば修正
            scheme = 'https' if urldata['psdlist'][
                'isTLS'] == 'true' else 'http'
        path = '/' + re.sub(urldata['psdlist']['root'], '', urldata['path'], 1)
        host = urldata['host'].replace(urldata['psdlist']['id'] + '@', '')
        url = scheme + '://' + host + path
        res = requests.post(
            url,
            auth=(urldata['psdlist']['id'], urldata['psdlist']['pass']),
            verify=False
        )

    # ステータスコードで結果の判断
    if res.status_code == 200:
        print(f'{url} sucusess')
        saveResult(host, path, res.content)
        return urldata['url']
    elif '30' in str(res.status_code):
        if path == re.sub(r'https?://' + host, '', res.url):
            # http→https リダイレクトは許可
            print(f'{url} sucusess')
            saveResult(host, path, res.content)
            return urldata['url']
        # リダイレクト
        print(f'{url} faild')
        raise ValueError(
            urldata['url'],
            f'redirect page to:{res.url}'
        )
    elif '40' in str(res.status_code):
        # not found
        print(f'{url} faild')
        raise ValueError(
            urldata['url'],
            f'page not found status:{res.status_code}'
        )
    else:
        # undefind error
        print(f'{url} faild')
        raise ValueError(
            urldata['url'],
            f'undefind error status:{res.status_code} url:{res.url}'
        )


def saveResult(host, path, value):
    # DL 成功
    filename = './http/' + host + path
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
