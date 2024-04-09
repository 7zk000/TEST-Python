import sys
import argparse
from cryptography.fernet import Fernet
import os
import requests

def decrypt_config(key):
    f = Fernet(key)
    with open('Config/config.txt', 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data).decode()
    return decrypted_data

def load_config(key):
    try:
        decrypted_data = decrypt_config(key)
    except FileNotFoundError:
        print("設定ファイルが見つかりません。")
        sys.exit(1)

    config = {}
    for line in decrypted_data.split('\n'):
        if line.strip() == '':
            continue
        key, value = line.strip().split(' = ', 1)
        config[key] = value
    return config

def display_title():
    print("------はろー　わーるど!------")

def search_books(api_key):
    print(f"APIキー: {api_key} を使用して書籍情報を検索します。")
    # 実際のAPIリクエストの例
    endpoint = "https://example.com/api/books"  # ダミーのエンドポイント
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            data = response.json()
            for book in data['books']:
                print(f"タイトル: {book['title']}, 著者: {book['author']}, ISBN: {book['isbn']}")
        else:
            print(f"書籍情報の取得に失敗しました。ステータスコード: {response.status_code}")
    except requests.RequestException as e:
        print(f"書籍情報の取得中にエラーが発生しました: {e}")

def main():
    parser = argparse.ArgumentParser(description='Endpoint.py')
    parser.add_argument('--api_key', help='Amazon APIキー', required=True)
    parser.add_argument('--firebase_sdk_path', help='Firebase SDKのパス', required=True)
    args = parser.parse_args()

    key_path = 'Config/secret.key'
    if not os.path.exists(key_path):
        print("秘密鍵が見つかりません。")
        sys.exit(1)

    with open(key_path, 'rb') as key_file:
        key = key_file.read()

    config = load_config(key)
    display_title()
    search_books(config.get("AMAZON_API_KEY"))

if __name__ == '__main__':
    main()
