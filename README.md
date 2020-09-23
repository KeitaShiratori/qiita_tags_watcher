# Qiitaの記事数TOP500タグ一覧を自動投稿
## 実行環境
- AWS Lambda(Python 3.8)

## 環境構築
- AWS Lambda（Python3.8）
  - 依存ライブラリをインストールするため、ローカル環境で下記を実行する
    ```
    cd lambda
    pip install -r requirements.txt -t python
    zip -r pip_libs.zip python/
    ```
  - Lambda Layerを作成し、pip_libs.zipをアップロードする
  - 任意の名前（例：qiita_tags_watcher）でLambda関数を作成する。ランタイムはPython3.8
  - `lambda/lambda_function.py` をLambda関数qiita_tags_watcherにアップロードする
  - qiita_tags_watcherのレイヤーに先ほど作成したレイヤーを追加する
  - 環境変数を設定する
    - TOKEN: 自分のQiita API 認証トークン
    - ITEM_ID: 更新対象のQiita記事のID
  - 基本設定
    - APIの呼び出し時間が掛かるため、タイムアウトは10秒以上を設定する
  - テスト実行して正常終了するか確認する
  - トリガーの追加
    - CloudWatch Eventの定期実行イベントをトリガーに設定する。

## その他
- ローカルでデバッグ実行する方法
  - `.vscode/launch.json`を下記の内容に編集する。
```
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "lambda_function",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/lambda/lambda_function.py",
      "env": {
        "TOKEN": "YOUR_QIITA_API_TOKEN",
        "ITEM_ID": "YOUR_QIITA_ITEM_ID",
      },
      "console": "integratedTerminal"
    }
  ]
}
```