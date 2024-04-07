import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate(r"File Of JSON")
firebase_admin.initialize_app(cred)
db = firestore.client()

def add_note(title, content):
    doc_ref = db.collection('notes').document(title)
    doc = doc_ref.get()
    if doc.exists:
        print("このタイトルのメモは既に存在します。別のタイトルを選んでください。")
        return

    try:
        doc_ref.set({
            'title': title,
            'content': content,
            'created_at': firestore.SERVER_TIMESTAMP,
            'updated_at': firestore.SERVER_TIMESTAMP
        })
        print("メモを追加しました。")
    except Exception as e:
        print(f"メモの追加中にエラーが発生しました: {e}")

from datetime import datetime

def get_notes():
    try:
        docs = db.collection('notes').stream()
        for doc in docs:
            note = doc.to_dict()
            created_at = note['created_at'].strftime('%Y-%m-%d %H:%M:%S') if 'created_at' in note else '不明'
            updated_at = note['updated_at'].strftime('%Y-%m-%d %H:%M:%S') if 'updated_at' in note else '不明'

            print(f"タイトル　：{note['title']}")
            print(f"作成時間　：{created_at}")
            print(f"更新時間　：{updated_at}")
            print(f"内容　　　：{note['content']}：\n")
    except Exception as e:
        print(f"メモの取得中にエラーが発生しました: {e}")

def main():
    while True:
        print("メモ帳アプリへようこそ！")
        print("1: メモを追加")
        print("2: メモを表示")
        print("3: 終了")
        choice = input("選択してください: ")

        if choice == '1':
            title = input("メモのタイトルを入力してください: ")
            content = input("メモの内容を入力してください: ")
            add_note(title, content)
        elif choice == '2':
            print("保存されているメモ:")
            get_notes()
        elif choice == '3':
            print("アプリを終了します。")
            break
        else:
            print("無効な選択です。もう一度試してください。")

if __name__ == '__main__':
    main()
