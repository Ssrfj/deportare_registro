import pandas as pd
import os
from datetime import datetime, timezone, timedelta

# テスト用の人間によるチェック結果をシミュレート
def create_test_human_check():
    """書類1のチェックを人間が行ったとして、クラブごとのチェックリスト作成状況ファイルを作成する"""
    
    # 出力フォルダパス
    output_folder = r"e:\oasobi\deportare_registro\output\R7_登録受付処理"
    
    # クラブごとのチェックリスト作成状況ファイルを作成
    checklist_status_data = {
        'クラブ名': ['北海クラブ', '辰州クラブ', '名古屋クラブ', '京ラクラブ', '東海クラブ'],
        '申請日時': ['20250612234210', '20250612235354', '20250613000539', '20250613001723', '20250613001723'],
        '書類チェック': [
            'info: 書類のチェックで問題は見つかりませんでした',
            'warning: 書類1で問題が見つかりました - 申請者名に不備があります',
            'info: 書類のチェックで問題は見つかりませんでした',
            'error: 書類1で重大な問題が見つかりました - 必須項目が欠落しています',
            'info: 書類のチェックで問題は見つかりませんでした'
        ],
        '書類チェック更新時間': [
            datetime.now(timezone(timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S'),
            datetime.now(timezone(timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S'),
            datetime.now(timezone(timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S'),
            datetime.now(timezone(timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S'),
            datetime.now(timezone(timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S')
        ],
        '書類1チェック者名': ['田中太郎', '佐藤花子', '山田次郎', '鈴木三郎', '高橋四郎']
    }
    
    checklist_status_df = pd.DataFrame(checklist_status_data)
    
    # ファイルを保存
    status_file_path = os.path.join(output_folder, 'クラブごとのチェックリスト作成状況.xlsx')
    checklist_status_df.to_excel(status_file_path, index=False)
    
    print(f"テスト用のチェックリスト作成状況ファイルを作成しました: {status_file_path}")
    print("作成したデータ:")
    print(checklist_status_df)

if __name__ == "__main__":
    create_test_human_check()
