# ベースイメージとしてPythonを使用
FROM python:3.12-slim

# 作業ディレクトリを設定
WORKDIR /app

# 現在のディレクトリの内容をコンテナ内の/appにコピー
COPY . /app

# requirements.txtに指定された必要なパッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# dataディレクトリが存在することを保証
RUN mkdir -p /app/data

# スクリプトのエントリーポイントを指定
CMD ["python", "src/retrieve_datasets.py"]
