# downloader

http／ftp／sftp（鍵なし）に対応したダウンローダー

## 使い方

1. ダウンロードしたい対象のURLを「list.txt」へ記載  
	(e.g. echo "https://domain/hoge/target_url.html" > list.txt
1. FTP／SFTPからダウンロードしたい場合は「some.csv」にカラムにそって記載
1. ダウンロードしたいプロトコルによって

	- FTP／SFTPダウンロード：「curl_ftp.py」
    - httpダウンロード：「curl_http.py」

    を実行する

### 「some.csv」記載方法

```python
"""
domain: str
	server domain
	(e.g. www.google.com, 192.168.0.0)

id: str
	login username
	(e.g. User)

pass: str
	login pass
	(e.g. Pass)

scheme: [fpt|sftp]
	connect protocol

root: str
	current dirctory 
	(e.g. /hoge/ if http://domain/file is /hoge/file)

isTLS: [true|false]
	http or https?
"""
```

## 追記事項（開発メモ）

### パッケージ追加方法

pipでインストールする。必ずrequirements.txtを更新すること（イメージへ反映するため）

```
pip install <package_name>
pip freeze > requirements.txt
```

### pyinstaller 対応確認済

```Linux command
docker run --rm -v "$(pwd):/src/" --entrypoint `/bin/sh cdrx/pyinstaller-windows -c "/usr/bin/pip install -r requirements.txt && pyinstaller curl_ftp.py --onefile"`
```

## Warnig

本プログラムを用いた、いかなる相手への悪意のある行動を禁止します。

Any malicious activity using this program is prohibited.

また本プログラムを実行することによって生じた損害・不利益、本プログラムを用いられたことによる損害・不利益等、本プログラムに関した事象に対していかなる責任も負いません

We will not be liable for any damage or disadvantage caused by the use of this program or by the use of this program.

## ライセンス

MIT
