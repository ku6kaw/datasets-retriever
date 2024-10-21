# datasets-retriever

このプロジェクトは、指定したクエリに基づいてDataCite APIからデータセットを取得し、そのデータセットに関する引用情報や関連論文の詳細を収集するためのスクリプトです。Dockerコンテナを使用して簡単に実行できるようになっています。

## 必要なツール
- Docker
- Python 3.12.6

## セットアップ手順

### 1. リポジトリのクローン
まず、このリポジトリをローカル環境にクローンします。

```sh
git clone https://github.com/ku6kaw/datasets-retriever
cd datasets-retriever
```

### 2. `requirements.txt` の作成
仮想環境をアクティブにした状態で、必要なパッケージを `requirements.txt` に出力します。

```sh
pip freeze > requirements.txt
```

### 3. Dockerイメージのビルド
プロジェクトのルートディレクトリに移動し、次のコマンドでDockerイメージをビルドします。

```sh
docker build -t datasets-retriever .
```

- `-t datasets-retriever` はイメージに付ける名前です。
- `.` は現在のディレクトリをビルドコンテキストとして指定しています。

### 4. コンテナの実行
Dockerイメージがビルドされたら、次のコマンドでコンテナを起動してスクリプトを実行します。

```sh
docker run --rm -it datasets-retriever
```

- `--rm` オプションは、コンテナの実行が終了したときに削除されるようにします。
- `-it` オプションは、インタラクティブモードでコンテナを起動し、標準入力にアクセスできるようにします。

コンテナが起動すると、`Enter your search query:` と表示されます。ここで、`machine learning` などのクエリを入力してください。

### 5. 結果の確認
スクリプトの実行結果は、`data` ディレクトリ内に `datasets_指定したクエリ名.json` という形式で保存されます。例えば、クエリが `machine learning` であれば、結果は `data/datasets_machine_learning.json` に保存されます。

## 注意事項
- クエリにスペースが含まれている場合は、自動的にファイル名でアンダースコアに変換されます。
- データ取得中にエラーが発生した場合、エラーメッセージが表示されます。その場合は、クエリを変更するか、インターネット接続やAPIの状態を確認してください。

## ディレクトリ構成
- `src/` : スクリプトが含まれています。
  - `retrieve_datasets.py` : データセットを取得し、情報を収集するメインのスクリプト。
- `data/` : データセットの情報が保存されるディレクトリ。
- `Dockerfile` : Dockerイメージを作成するための設定ファイル。
- `requirements.txt` : 必要なPythonパッケージのリスト。

## トラブルシューティング
- **`ModuleNotFoundError`**: コンテナ内で `tqdm` などのモジュールが見つからない場合、`requirements.txt` が正しく生成されているか確認し、再度イメージをビルドしてください。
- **`Read-only file system` エラー**: `/data` ディレクトリが書き込み不可の場合、保存先を変更してみてください。現在はプロジェクトディレクトリ内の `data/` に保存するように設定しています。

## ライセンス
このプロジェクトはMITライセンスの下で公開されています。詳細については、LICENSEファイルをご確認ください。

