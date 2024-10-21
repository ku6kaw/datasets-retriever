import requests
import json
import os

def retrieve_datasets(query, rows=10):
    # Datacite API endpoint URL
    base_url = "https://api.datacite.org/dois"
    
    # パラメータを指定してクエリを設定
    params = {
        "query": query,  # クエリ文字列
        "resource-type-id": "dataset",  # データセットを対象とする
        "page[size]": rows  # 取得するデータ数
    }
    
    headers = {
        "Accept": "application/vnd.api+json"
    }
    
    try:
        # Datacite APIにGETリクエストを送信
        response = requests.get(base_url, params=params, headers=headers)
        
        # 正常にレスポンスが返された場合、結果をパース
        if response.status_code == 200:
            data = response.json()
            if "data" in data:
                for dataset in data["data"]:
                    print_dataset_info(dataset)
            else:
                print("No datasets found for the given query.")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

def print_dataset_info(dataset):
    # 各データセットのDOIとタイトルを表示
    attributes = dataset.get("attributes", {})
    title = attributes.get("titles", [{}])[0].get("title", "No title available")
    doi = attributes.get("doi", "No DOI available")
    publisher = attributes.get("publisher", "No publisher available")
    publication_year = attributes.get("publicationYear", "No publication year available")
    
    print(f"Title: {title}")
    print(f"DOI: {doi}")
    print(f"Publisher: {publisher}")
    print(f"Publication Year: {publication_year}")
    print("-" * 40)

if __name__ == "__main__":
    # クエリを指定してデータセット情報を取得
    query = input("Enter your search query: ")
    retrieve_datasets(query, rows=5)
