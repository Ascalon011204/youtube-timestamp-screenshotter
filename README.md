# youtube-timestamp-screenshotter
Capture screenshots of a given URL at exact :05 and :55 every minute to estimate YouTube upload times from relative timestamps.
YouTubeの「○時間前」表記から投稿時間を推定するために、指定したURLのスクリーンショットを正確な時刻で取得するPythonツール。

## 概要

本ツールは、指定したWebページ（主にYouTube動画ページ）に対して、毎分「05秒」と「55秒」のタイミングでスクリーンショットを取得します。

取得された画像をもとに、「○時間前」表示の変化タイミングを解析することで、動画の投稿時刻をより正確に推定することが可能です。

## 主な特徴

* 秒指定トリガー（05秒 / 55秒）による高精度な取得
* 1時間あたり120回の自動スクリーンショット取得
* Seleniumによるブラウザ自動操作
* GUI（tkinter / PyQt6）による簡単操作
* 時刻同期ロジックによるズレ防止
* ファイル名にタイムスタンプとURL識別子を付与

## 技術構成

* Python
* Selenium
* ChromeDriver（webdriver-manager対応）
* tkinter / PyQt6

## 使用方法

1. アプリを起動
2. URLを入力
3. 「開始」ボタンを押す
4. 自動で1時間スクリーンショットを取得

## 出力

* /screenshots フォルダに画像保存
* ファイル名形式：
  YYYYMMDDhhmmss_<URL識別子>.png

## 用途

* YouTube投稿時間の逆算
* 時刻依存UIの変化観測
* 定点観測ログの取得

## 注意

* 本ツールは情報収集用途を目的としています
* 過度なアクセスは対象サイトの利用規約に従ってください
