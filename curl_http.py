# config: UTF-8
import asyncio
from getConfig import getUrlList, getCsvConfig
from decisionUrl import convertUrlFormat
from httpDownloader import downloader


if __name__ == "__main__":
    # asyncio ループ用意
    loop = asyncio.get_event_loop()

    # config ロード
    textList, psdList = loop.run_until_complete(asyncio.gather(
        getUrlList(),
        getCsvConfig()
    ))
    print('config load')

    # 入力のフォーマット＋サーバー設定取得
    urldatas = []
    checkTasks = [convertUrlFormat(t, 'http', psdList) for t in textList]
    wait_coro = asyncio.wait(checkTasks, loop=None)
    res, _ = loop.run_until_complete(wait_coro)
    for future in res:
        try:
            # ここでエラーを吐かせる
            result = future.result()
            urldatas.append({
                'url': result.url,
                'host': result.host,
                'scheme': result.scheme,
                'path': result.path,
                'category': result.category,
                'psdlist': result.psdlist
            })
        except Exception:
            # テキストにURL以外が入った場合
            pass
    print('text load')
    print(f'all url count:{len(urldatas)}')

    # ダウンロード処理
    sucusess = []
    error = []
    downloadTasks = [downloader(urldata) for urldata in urldatas]
    wait_coro = asyncio.wait(downloadTasks, loop=None)
    res, _ = loop.run_until_complete(wait_coro)
    for future in res:
        try:
            # ここでエラーを吐かせる
            result = future.result()
            sucusess.append(result)
        except Exception as err:
            # 何かが起きた
            error.append(err)
            pass
    print(sucusess)
    print(error)
