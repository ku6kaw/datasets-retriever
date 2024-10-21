# ベースイメージとしてPythonを使用
FROM python:3.12-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコンテナにコピー
COPY src/ src/
COPY requirements.txt .

# 必要なパッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# スクリプトのエントリーポイントを指定
CMD ["python", "src/datasets_from_datacite_by_query.py"]
