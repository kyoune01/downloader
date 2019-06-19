# config: UTF-8
import asyncio
import pyperclip
from getConfig import getUrlList, getCsvConfig
from decisionUrl import convertUrlFormat
from ftpDownloader import downloader
from formatURLData import formatDataForFTP


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
    checkTasks = [convertUrlFormat(t, 'ftp', psdList) for t in textList]
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

    # count0 のときは終了
    if len(urldatas) == 0:
        print('\nNone download file.')
        print('push key and kill exe.')
        inp = input()
        exit()

    # 主キー：URL　→　主キー：サーバ　の形へ整形
    urldatas = formatDataForFTP(urldatas)

    # ダウンロード対象をカウント
    # path <- (urldata <- urldatas)['path']
    pathList = [path for urldata in urldatas for path in urldata['path']]
    print(f'all download file:{len(pathList)}')

    # ダウンロード処理
    result = []
    downloadTasks = [downloader(urldata) for urldata in urldatas]
    wait_coro = asyncio.wait(downloadTasks, loop=None)
    res, _ = loop.run_until_complete(wait_coro)
    for future in res:
        try:
            # ここでエラーを吐かせる
            result = future.result()
        except Exception as err:
            # 何かが起きた
            print(f'faild: {err.args[0]}\nmessage: {err.args[1]}')

    # error はクリップボードへコピー
    error = [x['url'] + '\n' + x['message'] for x in result if not x['status']]
    error = list(set(error))
    pyperclip.copy('\n\n'.join(error))

    # 入力を受けたら終了
    print('\ndownload finish.')
    print('')
    print('**************************************')
    print(' paste Clip Board. you need Error Log')
    print('**************************************')
    print('\npush key and kill exe.')
    inp = input()
