import os
from cryptography.fernet import Fernet
import requests
import subprocess
import firebase_admin
from firebase_admin import credentials, firestore

# Firestoreの初期化
if not firebase_admin._apps:
    cred_path = 'Config/serviceAccountKey.json'
    if not os.path.exists(cred_path):
        print("Firebaseサービスアカウントキーファイルが見つかりません。")
        exit()
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

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
        return {}

    config = {}
    for line in decrypted_data.split('\n'):
        if line.strip() == '':
            continue
        key, value = line.strip().split(' = ', 1)
        config[key] = value
    return config

def validate_amazon_api_key(api_key):
    endpoint = "https://api.amazon.com/test"
    headers = {"X-Api-Key": api_key}
    try:
        response = requests.get(endpoint, headers=headers)
        if response.status_code in range(200, 300):
            return True
        else:
            print(f"APIキーの検証に失敗しました。ステータスコード: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"APIキーの検証中にエラーが発生しました: {e}")
        return False

def validate_firebase_sdk_path(sdk_path):
    return os.path.exists(sdk_path)

def prompt_user_input(config):
    amazon_api_key = config.get("AMAZON_API_KEY", input("Amazon APIキー (AMAZON_API_KEY) を入力してください: "))
    firebase_sdk_path = config.get("FIREBASE_SDK_PATH", input("Firebase SDKのパス (FIREBASE_SDK_PATH) を入力してください: "))
    return amazon_api_key, firebase_sdk_path

def execute_next_step(api_key, sdk_path):
    try:
        subprocess.run(['python', 'Endpoint.py', '--api_key', api_key, '--firebase_sdk_path', sdk_path], check=True)
        print("Endpoint.pyが正常に実行されました。")
    except subprocess.CalledProcessError as e:
        print(f"Endpoint.pyの実行中にエラーが発生しました: {e}")
    except Exception as e:
        print(f"Endpoint.pyの実行中にエラーが発生しました: {e}")

def main():
    key_path = 'Config/secret.key'
    if not os.path.exists(key_path):
        print("秘密鍵が見つかりません。")
        return

    with open(key_path, 'rb') as key_file:
        key = key_file.read()

    config = load_config(key)

    while True:
        amazon_api_key, firebase_sdk_path = prompt_user_input(config)

        if not validate_amazon_api_key(amazon_api_key):
            print("Amazon APIキーが無効です。もう一度入力してください。")
            continue

        if not validate_firebase_sdk_path(firebase_sdk_path):
            print("Firebase SDKのパスが無効です。もう一度入力してください。")
            continue

        print("Successful! 次のステップに進みます。")
        execute_next_step(amazon_api_key, firebase_sdk_path)
        break

if __name__ == '__main__':
    main()
