# YouTube投稿時間推定用スクリーンショット取得ツール 開発タスク

- [x] 実装計画の修正（事前リロード・高頻度監視への変更）
- [x] プロジェクトディレクトリの作成 (`C:\Users\3076m\Desktop\antigravity\YouTubeTimeEstimator\1st`)
- [x] `main.py` の実装
  - [x] GUI構築（URL入力、開始ボタン、現在時刻、次回リロード予定時刻、次回撮影予定時刻、実行回数）
  - [x] Seleniumヘッドレスブラウザの初期化処理
  - [x] 時刻計算ロジック（02/52秒でリロード、05/55秒で撮影）
  - [x] 高頻度監視による時刻同期ループと撮影処理
  - [x] `missed timing` リカバリ処理
  - [x] ログ出力処理
- [x] `requirements.txt` の作成
- [ ] 動作確認・検証
- [ ] `walkthrough.md` の作成
