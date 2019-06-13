# config: UTF-8
import json
import re


def formatDataForFTP(urldatas):
    tmpurldatas = []
    serverlist = []

    # 受け取ったデータからサーバ情報を持たないデータを削除
    # サーバ情報だけのリストを生成
    for urldata in urldatas:
        if urldata['psdlist'] == {}:
            continue
        # urldatasから直接削除すると正常にループしないため一時変数へ追加する
        tmpurldatas.append(urldata)
        serverlist.append(urldata['psdlist'])

    # サーバ情報の重複を削除
    serverlist = list(map(json.loads, set(map(json.dumps, serverlist))))

    # サーバ情報へDL対象のパスを配列で追加
    for server in serverlist:
        # server は参照渡し
        values = [x['path'] for x in tmpurldatas if x[
            'psdlist']['domain'] == server['domain']]
        # 末尾が「/」で終わるURLは処理しない
        values = [val for val in values if re.match(r'[^\.]*/$', val) is None]
        server['path'] = values if values else None

    return serverlist
