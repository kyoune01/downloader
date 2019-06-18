# config: UTF-8
import json
import re


def formatDataForFTP(urldatas):
    tmpUrldatas = []
    serverlist = []

    # 受け取ったデータからサーバ情報を持たないデータを削除
    # サーバ情報だけのリストを生成
    for urldata in urldatas:
        if urldata['psdlist'] == {}:
            continue
        # urldatasから直接削除すると正常にループしないため一時変数へ追加する
        tmpUrldatas.append(urldata)
        serverlist.append(urldata['psdlist'])

    # サーバ情報の重複を削除
    serverlist = list(map(json.loads, set(map(json.dumps, serverlist))))

    # サーバ情報へDL対象のパスを配列で追加
    for server in serverlist:
        # server は参照渡し
        pathList = [x['path'] for x in tmpUrldatas if x[
            'psdlist']['domain'] == server['domain']]
        # 末尾が「/」で終わるURLは処理しない
        pathList = [url for url in pathList if re.match(
            r'[^\.]*/$', url) is None]
        server['path'] = pathList if pathList else None

    return serverlist
