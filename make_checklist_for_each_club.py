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

def add_row_if_not_exists(csv_path, club_name, application_datetime, checklist_created_datetime, r8_timestamp=None):
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        df = pd.DataFrame(columns=['クラブ名','申請日時','チェックリスト作成日時','R8年度登録申請_タイムスタンプyyyymmddHHMMSS'])
    # ここで型を揃えて比較
    exists = ((df['クラブ名'].astype(str) == str(club_name)) & (df['申請日時'].astype(str) == str(application_datetime))).any()
    if not exists:
        new_row = {
            'クラブ名': club_name,
            '申請日時': application_datetime,
            'チェックリスト作成日時': checklist_created_datetime,
            'R8年度登録申請_タイムスタンプyyyymmddHHMMSS': r8_timestamp if r8_timestamp else application_datetime
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(csv_path, index=False)
        logging.info(f"状況CSVに新規行を追加: {club_name}, {application_datetime}")
        return df
    else:
        logging.info(f"DEBUG: 既存行あり: {club_name}, {application_datetime}")

def make_checklist_for_each_club(apried_club_list_df, checklist_status_df, checklist_output_folder, timestamp_for_make_checklist):
    if '申請日時' not in checklist_status_df.columns:
        logging.error("checklist_status_dfに'申請日時'カラムがありません")
    if '申請日時' not in apried_club_list_df.columns:
        logging.error("apried_club_list_dfに'申請日時'カラムがありません")
    if 'R8年度登録申請_タイムスタンプyyyymmddHHMMSS' not in apried_club_list_df.columns:
        logging.error("apried_club_list_dfに'R8年度登録申請_タイムスタンプyyyymmddHHMMSS'カラムがありません")

    checklist_folder_path = os.path.join('R7_登録申請処理', '申請入力内容')
    checklist_file_name = 'クラブごとのチェックリスト作成状況.csv'
    checklist_path = os.path.join(checklist_folder_path, checklist_file_name)

    for _, row in apried_club_list_df.iterrows():
        try:
            club_name = str(row['クラブ名']).strip()
            application_timestamp = str(row['R8年度登録申請_タイムスタンプyyyymmddHHMMSS']).strip()
            application_datetime = str(row['申請日時']).strip()
            logging.info(f"DEBUG: club_name={club_name}, application_datetime={application_datetime}, application_timestamp={application_timestamp}")
            output_folder = os.path.join(checklist_output_folder, club_name)
            os.makedirs(output_folder, exist_ok=True)
            file_name = f"{club_name}_申請{application_timestamp}_作成{timestamp_for_make_checklist}.csv"
            file_path = os.path.join(output_folder, file_name)

            # 既存ファイルがあっても必ずCSVに追加
            each_club_checklist_status_df = add_row_if_not_exists(
                checklist_path,
                club_name,
                application_datetime,
                timestamp_for_make_checklist,
                application_timestamp
            )
            logging.info(f"状況CSVに行を追加またはスキップ: {club_name}, {application_datetime}")

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
        except Exception as e:
            logging.error(f"クラブ {row['クラブ名']} の処理中にエラーが発生しました: {e}")
    # 最後に最新の状況CSVを読み込んで返す
    if os.path.exists(checklist_path):
        return pd.read_csv(checklist_path)
    else:
        return each_club_checklist_status_df