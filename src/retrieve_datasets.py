import requests
import csv
import json
import os
from tqdm import tqdm
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()
SCOPUS_API_KEY = os.getenv('SCOPUS_API_KEY')

# APIのベースURL
OPENCITATIONS_BASE_URL = "https://opencitations.net/index/api/v1/citations/"
CITATION_COUNT_URL = "https://opencitations.net/index/api/v1/citation-count/"
DATACITE_API_BASE_URL = "https://api.datacite.org/dois"
SCOPUS_BASE_URL = "https://api.elsevier.com/content/abstract/doi/"

def retrieve_datasets(query, rows=10, max_pages=3):
    """
    DataCite APIを使用して指定したクエリのデータセットを最大3ページまで取得する関数
    """
    page_number = 1
    all_datasets = []
    while page_number <= max_pages:
        params = {
            "query": query,  # クエリ文字列
            "resource-type-id": "dataset",  # データセットを対象とする
            "page[size]": rows,  # 取得するデータ数
            "page[number]": page_number  # 現在のページ番号
        }
        headers = {
            "Accept": "application/vnd.api+json"
        }
        response = requests.get(DATACITE_API_BASE_URL, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            datasets = data.get("data", [])
            if not datasets:
                break
            all_datasets.extend(datasets)
            page_number += 1
        else:
            print(f"Failed to retrieve datasets for query: {query}, Status code: {response.status_code}")
            break
    return all_datasets

def fetch_citation_count(doi):
    """
    OpenCitations APIを使用してDOIのcitation数を取得する関数
    """
    url = f"{CITATION_COUNT_URL}{doi}"
    response = requests.get(url)
    if response.status_code == 200:
        count = response.json()
        if isinstance(count, list) and len(count) == 0:
            return 0
        elif isinstance(count, list) and len(count) > 0 and 'count' in count[0]:
            return int(count[0]['count'])
        return int(count) if count is not None else 0
    else:
        print(f"Failed to fetch citation count for DOI: {doi}, Status code: {response.status_code}")
        return 0

def fetch_citation_details(doi):
    """
    OpenCitations APIを使用してDOIのcitation詳細情報を取得する関数
    """
    url = f"{OPENCITATIONS_BASE_URL}{doi}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        filtered_data = [
            {
                "doi": entry.get("citing", ""),
                "creation": entry.get("creation", ""),
                "journal_sc": entry.get("journal_sc", ""),
                "author_sc": entry.get("author_sc", "")
            }
            for entry in data
        ]
        return filtered_data
    else:
        print(f"Failed to fetch citation details for DOI: {doi}, Status code: {response.status_code}")
        return []

def fetch_scopus_info(doi):
    """
    Scopus Abstract Retrieval APIを使用してDOIの情報を取得する関数
    """
    headers = {
        'X-ELS-APIKey': SCOPUS_API_KEY,
        'Accept': 'application/json'
    }
    url = f"{SCOPUS_BASE_URL}{doi}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch Scopus info for DOI: {doi}, Status code: {response.status_code}")
        return None

def extract_scopus_info(scopus_data):
    """
    Scopus APIのレスポンスからタイトル、アブストラクト、主題領域を抽出する関数
    """
    item = scopus_data.get('abstracts-retrieval-response', {})
    title = item.get('coredata', {}).get('dc:title', 'Not found')
    abstract = item.get('coredata', {}).get('dc:description', 'Not found')

    subject_areas = item.get('subject-areas', {}).get('subject-area', [])
    subjects = [subject.get('$', 'Not found') for subject in subject_areas]

    return {
        "title": title,
        "abstract": abstract,
        "subject_areas": subjects,
        "use_dataset": ""
    }

def main():
    # クエリを指定してデータセットを取得
    query = input("Enter your search query: ")
    datasets = retrieve_datasets(query, rows=100, max_pages=3)

    if not datasets:
        print("No datasets found for the given query.")
        return

    print(f"Found {len(datasets)} datasets for query: '{query}'")
    enriched_records = []

    # 各データセットについてcitation数と詳細情報、Scopus情報を取得
    for dataset in tqdm(datasets, desc="Processing Datasets"):
        doi = dataset.get("attributes", {}).get("doi", "")
        if not doi:
            continue

        citation_count = fetch_citation_count(doi)

        # citation_countが0または10以上の場合はスキップ
        if citation_count == 0 or citation_count >= 10:
            continue

        citation_details = fetch_citation_details(doi)

        enriched_record = {
            "doi": doi,
            "citation_count": citation_count,
            "citations": []
        }
        for detail in citation_details:
            citing_doi = detail.get("doi", "")
            scopus_data = fetch_scopus_info(citing_doi)
            if scopus_data:
                scopus_info = extract_scopus_info(scopus_data)
                detail.update(scopus_info)
            else:
                detail.update({"title": "Not found", "abstract": "Not found", "subject_areas": [], "use_dataset": ""})

            enriched_record["citations"].append(detail)

        enriched_records.append(enriched_record)

    # 取得した詳細情報をJSONファイルに保存
    output_file = f"data/datasets_{query.replace(' ', '_')}.json"
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(enriched_records, f, indent=4)

    print(f"Enriched data saved to {output_file}")

if __name__ == "__main__":
    main()
