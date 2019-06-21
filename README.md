# downloader
http／ftp／sftp（鍵なし）に対応したダウンローダー
## 使い方
ダウンロードしたい対象のURLを「list.txt」に記載<br>
もしFTP／SFTPからダウンロードしたい場合は「some.csv」にカラムにそって記載

ダウンロードしたいプロトコルによって<br>
- FTP／SFTPダウンロード：「curl_ftp.py」
- httpダウンロード：「curl_http.py」

を実行する
## 追記事項（メモ）
- pyinstaller 対応確認済
## ライセンス
MIT
