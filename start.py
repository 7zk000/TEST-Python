import os
from cryptography.fernet import Fernet
import requests
import subprocess
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

if not firebase_admin._apps:
    cred_path = 'Config/serviceAccountKey.json'
    if not os.path.exists(cred_path):
        raise FileNotFoundError(f"Firebaseサービスアカウントキーファイルが見つかりません: {cred_path}")
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def load_or_create_key():
    key_path = 'Config/secret.key'
    if os.path.exists(key_path):
        with open(key_path, 'rb') as key_file:
            key = key_file.read()
    else:
        key = Fernet.generate_key()
        with open(key_path, 'wb') as key_file:
            key_file.write(key)
    return key

def encrypt_config(data, key):
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    with open('Config/config.txt', 'wb') as file:
        file.write(encrypted_data)

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
        return {"AMAZON_API_KEY": "none", "FIREBASE_SDK_PATH": "none"}

    config = {}
    for line in decrypted_data.split('\n'):
        if line.strip() == '':
            continue
        key, value = line.strip().split(' = ', 1)
        config[key] = value
    return config

def prompt_user_input():
    amazon_api_key = input("Amazon APIキー (AMAZON_API_KEY) を入力してください: ")
    firebase_sdk_path = input("Firebase SDKのパス (FIREBASE_SDK_PATH) を入力してください: ")
    return amazon_api_key, firebase_sdk_path

def validate_and_process(api_key, sdk_path, key):
    if api_key.lower() == 'none' or sdk_path.lower() == 'none':
        amazon_api_key, firebase_sdk_path = prompt_user_input()
        config_data = f"AMAZON_API_KEY = {amazon_api_key}\nFIREBASE_SDK_PATH = {firebase_sdk_path}\n"
        encrypt_config(config_data, key)
    else:
        amazon_api_key, firebase_sdk_path = api_key, sdk_path
    return amazon_api_key, firebase_sdk_path

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

def execute_next_step(api_key, sdk_path):
    try:
        subprocess.run(['python', 'midpoint-DB-load.py', '--api_key', api_key, '--firebase_sdk_path', sdk_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"実行中にエラーが発生しました: {e}")
    except Exception as e:
        print(f"(midpoint-DB-load.py) ERROR: {e}")

def main():
    key = load_or_create_key()
    config = load_config(key)
    amazon_api_key, firebase_sdk_path = validate_and_process(config.get("AMAZON_API_KEY", "none"), config.get("FIREBASE_SDK_PATH", "none"), key)

    if not validate_amazon_api_key(amazon_api_key):
        print("Amazon APIキーが無効です。もう一度入力してください。")
        amazon_api_key, firebase_sdk_path = prompt_user_input()
        config_data = f"AMAZON_API_KEY = {amazon_api_key}\nFIREBASE_SDK_PATH = {firebase_sdk_path}\n"
        encrypt_config(config_data, key)

    if not validate_firebase_sdk_path(firebase_sdk_path):
        print("Firebase SDKのパスが無効です。もう一度入力してください。")
        amazon_api_key, firebase_sdk_path = prompt_user_input()
        config_data = f"AMAZON_API_KEY = {amazon_api_key}\nFIREBASE_SDK_PATH = {firebase_sdk_path}\n"
        encrypt_config(config_data, key)

    print("Successful! 次のステップに進みます。")
    execute_next_step(amazon_api_key, firebase_sdk_path)

if __name__ == '__main__':
    main()
