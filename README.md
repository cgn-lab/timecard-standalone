# Timecard

## ドキュメント

ドキュメントは `documents/` にあります。  
Python の mkdocs ライブラリに準拠しています。

サーバー用仮想環境に mkdocs のライブラリも含まれています。

```bash
# サーバー用ディレクトリに移動
cd server
# 仮想環境の同期
uv sync
# 仮想環境の有効化
source .venv/bin/activate
# documentsに移動
cd ../documents

# ビルド
mkdocs build

# ビルドせずに閲覧
mkdocs serve
```
