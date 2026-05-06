# AGENT_MEMORY

## これまでの進捗
- `YouTube_Time_Estimator/main.py` の解析と改修要件の確認完了
- `implementation_plan.md` を作成し、ユーザーの承認（追加要件を含む）を取得
- `main.py` に対して以下の改修を実施：
  - **ログの独立化**: `log_<URL下10桁>_<PID>.txt` の命名規則でプロセスごとに独立したログファイルを生成
  - **パス解決の堅牢化**: `getattr(sys, 'frozen', False)` を利用して、`.exe`実行時も確実に同階層へ出力されるよう `get_base_dir()` を実装
  - **プロファイル分離**: `--user-data-dir` を利用して `chrome_profile_<PID>_<UUID>` という一意な一時ディレクトリを作成。プロセス終了時に削除（失敗してもエラーとせず `ignore_errors=True` で処理）
  - **ポート競合回避**: `--remote-debugging-port=0` を指定し自動割り当て化
- `requirements.txt`, `build.txt` の作成完了

## 未解決の課題
- 特になし。

## 現在の技術スタック
- Python 3.x
- tkinter (GUI)
- selenium (ブラウザ自動化・スクリーンショット撮影)
- webdriver-manager (ChromeDriverの自動取得)
- PyInstaller (exe化用)

## 重要な意思決定
- **ログの生成タイミング**: URLが確定する「開始」ボタンの押下時にログファイルを生成する仕様とした。
- **プロファイルディレクトリの命名**: `PID` のみでは万が一のプロセスID再利用や競合リスクを考慮し、`PID` + `UUID(8桁)` を用いることで一意性を強化。
- **出力ディレクトリの判定**: 単に `__file__` を使うのではなく、PyInstallerでパッケージ化された場合（`sys.frozen`）を考慮したベースディレクトリ解決ロジックを導入。
