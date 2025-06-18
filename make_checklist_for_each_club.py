import os
import pandas as pd
import logging
from dataframe_utils import clean_column_names
from utils import get_jst_now
logging.basicConfig(
    level=logging.INFO,
    encoding='utf-8',
    format="%(asctime)s [%(levelname)s] %(message)s"
)
import glob

def make_checklist_for_each_club(apried_club_list_df, checklist_status_df, checklist_output_folder, timestamp_for_make_checklist):
    updated_df = checklist_status_df.copy()
    if '申請日時' not in updated_df.columns:
        logging.error("checklist_status_dfに'申請日時'カラムがありません")
    if '申請日時' not in apried_club_list_df.columns:
        logging.error("apried_club_list_dfに'申請日時'カラムがありません")
    if 'R8年度登録申請_タイムスタンプyyyymmddHHMMSS' not in apried_club_list_df.columns:
        logging.error("apried_club_list_dfに'R8年度登録申請_タイムスタンプyyyymmddHHMMSS'カラムがありません")

    for _, row in apried_club_list_df.iterrows():
        try:
            club_name = str(row['クラブ名']).strip()
            application_timestamp = str(row['R8年度登録申請_タイムスタンプyyyymmddHHMMSS']).strip()
            output_folder = os.path.join(checklist_output_folder, club_name)
            os.makedirs(output_folder, exist_ok=True)
            file_name = f"{club_name}_申請{application_timestamp}_作成{timestamp_for_make_checklist}.csv"
            file_path = os.path.join(output_folder, file_name)

            # 申請日時が同じファイルが既に存在するかチェック
            pattern = os.path.join(output_folder, f"{club_name}_申請{application_timestamp}_作成*.csv")
            existing_files = glob.glob(pattern)
            if existing_files:
                logging.info(f"申請日時が同じチェックリストファイルが既に存在するためスキップ: {existing_files[0]}")
                # ここでupdated_dfに必ず追加する
                new_row = pd.DataFrame([{
                    'クラブ名': club_name,
                    '申請日時': application_timestamp,
                    'チェックリスト作成日時': timestamp_for_make_checklist
                }])
                updated_df = pd.concat([updated_df, new_row], ignore_index=True)
                checklist_folder_path = os.path.join('R7_登録申請処理', '申請入力内容')
                checklist_file_name = 'クラブごとのチェックリスト作成状況.csv'
                checklist_path = os.path.join(checklist_folder_path, checklist_file_name)
                updated_df.to_csv(checklist_path, index=False)
                continue

            # ...以下は新規作成処理...
            club_data = {
                'クラブ名': [club_name],
                '申請日時': [row['申請日時']],
                '担当者名': [row['申請_申請担当者名']],
                '役職名': [row['申請_申請担当者役職']],
                'メールアドレス': [row['申請_メールアドレス']],
                '電話番号': [row['申請_TEL']],
                'FAX番号': [row['申請_FAX(任意)']],
                '申請時間': [application_timestamp],
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
            club_df_for_make_checklist = clean_column_names(club_df_for_make_checklist)
            club_df_for_make_checklist.to_csv(file_path, index=False)
            logging.info(f"{file_path} にチェックリストを保存しました")
            # DataFrameも更新
            new_row = pd.DataFrame([{
                'クラブ名': club_name,
                '申請日時': application_timestamp,
                'チェックリスト作成日時': timestamp_for_make_checklist
            }])
            updated_df = pd.concat([updated_df, new_row], ignore_index=True)
            checklist_folder_path = os.path.join('R7_登録申請処理', '申請入力内容')
            checklist_file_name = 'クラブごとのチェックリスト作成状況.csv'
            checklist_path = os.path.join(checklist_folder_path, checklist_file_name)
            updated_df.to_csv(checklist_path, index=False)
            logging.info(f"{club_name}の申請日時が更新されました")
        except Exception as e:
            logging.error(f"クラブ {row['クラブ名']} の処理中にエラーが発生しました: {e}")
    return updated_df