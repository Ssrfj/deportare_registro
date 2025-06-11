import os
import pandas as pd
from datetime import datetime, timezone, timedelta

def make_checklist_for_each_club(application_club_list_df, checklist_create_df, checklist_output_folder, timestamp_for_make_checklist):
    for _, row in application_club_list_df.iterrows():
        try:
            club_data = {
                'クラブ名': [row['クラブ名']],
                '地区名': [row['地区名']],
                '担当者名': [row['申請_申請担当者名']],
                '役職名': [row['申請_申請担当者役職']],
                'メールアドレス': [row['申請_メールアドレス']],
                '電話番号': [row['申請_TEL']],
                'FAX番号': [row['申請_FAX(任意)']],
                '申請時間': [row['R8年度登録申請_タイムスタンプyyyymmddHHMMSS']],
                '自動チェック': [''],
                '自動チェック更新時間': [''],
                '書類チェック': [''],
                '書類チェック更新時間': [''],
                '書類間チェック': [''],
                '書類間チェック更新時間': [''],
                '担当者登録基準最終チェック': [''],
                '担当者登録基準最終チェック更新時間': [''],
            }
            club_df_for_make_checklist = pd.DataFrame(club_data)
            print(f"{row['クラブ名']}のclub_dfが作成されました")

            # checklist_create_dfにクラブ名があるかを確認
            if row['クラブ名'] not in checklist_create_df['クラブ名'].values:
                print('クラブ名がまだ存在しません')
                new_row = pd.DataFrame([{
                    'クラブ名': row['クラブ名'],
                    '申請日時': row['R8年度登録申請_タイムスタンプyyyymmddHHMMSS'],
                    'チェックリスト作成日時': timestamp_for_make_checklist
                }])
                checklist_create_df = pd.concat([checklist_create_df, new_row], ignore_index=True)
                print(f"{row['クラブ名']}の列が追加されました")
            else:
                print('クラブ名がすでに存在します')

            # checklist_create_dfにある申請日時と申請時間を照合
            print('checklist_create_dfにある申請日時と申請時間を照合に移行します')
            if row['R8年度登録申請_タイムスタンプyyyymmddHHMMSS'] == checklist_create_df.loc[checklist_create_df['クラブ名'] == row['クラブ名'], '申請日時'].values[0]:
                # クラブごとのチェックリスト保存先を指定
                output_folder = os.path.join(checklist_output_folder, row['クラブ名'])
                os.makedirs(output_folder, exist_ok=True)
                file_name = f"{row['クラブ名']}_申請{row['R8年度登録申請_タイムスタンプyyyymmddHHMMSS']}_作成{timestamp_for_make_checklist}.csv"
                file_path = os.path.join(output_folder, file_name)
                club_df_for_make_checklist.to_csv(file_path, index=False)
                print(f"{file_path} にチェックリストを保存しました")
                # checklist_create_dfのアップデート
                checklist_create_df.loc[checklist_create_df['クラブ名'] == row['クラブ名'], '申請日時'] = row['R8年度登録申請_タイムスタンプyyyymmddHHMMSS']
                checklist_create_df.loc[checklist_create_df['クラブ名'] == row['クラブ名'], 'チェックリスト作成日時'] = timestamp_for_make_checklist
                # checklist_create_dfを保存
                checklist_folder_path = os.path.join('R7_登録申請処理', '申請入力内容')
                checklist_file_name = 'クラブごとのチェックリスト作成状況.csv'
                checklist_path = os.path.join(checklist_folder_path, checklist_file_name)
                checklist_create_df.to_csv(checklist_path, index=False)
                print(f"{row['クラブ名']}の申請日時が更新されました")
            else:
                print('申請日時が同じチェックリストを作成済みです')
        except Exception as e:
            print(f"クラブ {row['クラブ名']} の処理中にエラーが発生しました: {e}")

# 例：呼び出し側
if __name__ == "__main__":
    # 必要なDataFrameやパスをここで用意して呼び出してください
    pass