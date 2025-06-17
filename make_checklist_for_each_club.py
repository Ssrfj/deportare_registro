import os
import pandas as pd
import logging
from dataframe_utils import clean_column_names
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def make_checklist_for_each_club(apried_club_list_df, checklist_status_df, checklist_output_folder, timestamp_for_make_checklist):
    updated_df = checklist_status_df.copy()  # ここで初期化
    # デバッグ用にapried_club_list_dfとchecklist_status_dfに'申請日時'と'R8年度登録申請_タイムスタンプyyyymmddHHMMSS'のカラムが存在するか確認
    if '申請日時' not in checklist_status_df.columns:
        logging.error("checklist_status_dfに'申請日時'カラムがありません")
    if '申請日時' not in apried_club_list_df.columns:
        logging.error("apried_club_list_dfに'申請日時'カラムがありません")
    if 'R8年度登録申請_タイムスタンプyyyymmddHHMMSS' not in apried_club_list_df.columns:
        logging.error("apried_club_list_dfに'R8年度登録申請_タイムスタンプyyyymmddHHMMSS'カラムがありません")
    if 'R8年度登録申請_タイムスタンプyyyymmddHHMMSS' not in apried_club_list_df.columns:
        logging.error("apried_club_list_dfに'R8年度登録申請_タイムスタンプyyyymmddHHMMSS'カラムがありません")

    for _, row in apried_club_list_df.iterrows():
        try:
            club_data = {
                'クラブ名': [row['クラブ名']],
                '申請日時': [row['申請日時']],
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
            logging.debug(f"before: {club_df_for_make_checklist.columns.tolist()}")
            club_df_for_make_checklist = clean_column_names(club_df_for_make_checklist)
            logging.debug(f"after: {club_df_for_make_checklist.columns.tolist()}")
            logging.info(f"{row['クラブ名']}のclub_dfが作成されました")

            if row['クラブ名'] not in checklist_status_df['クラブ名'].values:
                logging.info('クラブ名がまだ存在しません')
                new_row = pd.DataFrame([{
                    'クラブ名': row['クラブ名'],
                    '申請日時': row['R8年度登録申請_タイムスタンプyyyymmddHHMMSS'],
                    'チェックリスト作成日時': timestamp_for_make_checklist
                }])
                checklist_status_df = pd.concat([checklist_status_df, new_row], ignore_index=True)
                logging.info(f"{row['クラブ名']}の列が追加されました")
            else:
                logging.info('クラブ名がすでに存在します')

            logging.debug('checklist_status_dfにある申請日時と申請時間を照合に移行します')
            # 申請日時の参照を修正
            club_name = row['クラブ名']
            application_timestamp = row.get('R8年度登録申請_タイムスタンプyyyymmddHHMMSS', '')
            # checklist_status_dfの'申請日時'が存在しない場合は空文字列で比較
            current_application_timestamp = updated_df.loc[updated_df['クラブ名'] == club_name, '申請日時'].values[0] if not updated_df.loc[updated_df['クラブ名'] == club_name].empty else ''
            if application_timestamp == current_application_timestamp:
                output_folder = os.path.join(checklist_output_folder, row['クラブ名'])
                os.makedirs(output_folder, exist_ok=True)
                file_name = f"{row['クラブ名']}_申請{row['R8年度登録申請_タイムスタンプyyyymmddHHMMSS']}_作成{timestamp_for_make_checklist}.csv"
                file_path = os.path.join(output_folder, file_name)
                club_df_for_make_checklist.to_csv(file_path, index=False)
                logging.info(f"{file_path} にチェックリストを保存しました")
                updated_df.loc[updated_df['クラブ名'] == row['クラブ名'], '申請日時'] = row['R8年度登録申請_タイムスタンプyyyymmddHHMMSS']
                updated_df.loc[updated_df['クラブ名'] == row['クラブ名'], 'チェックリスト作成日時'] = timestamp_for_make_checklist
                checklist_folder_path = os.path.join('R7_登録申請処理', '申請入力内容')
                checklist_file_name = 'クラブごとのチェックリスト作成状況.csv'
                checklist_path = os.path.join(checklist_folder_path, checklist_file_name)
                updated_df.to_csv(checklist_path, index=False)
                logging.info(f"{row['クラブ名']}の申請日時が更新されました")
            else:
                logging.info('申請日時が同じチェックリストを作成済みです')
        except Exception as e:
            logging.error(f"クラブ {row['クラブ名']} の処理中にエラーが発生しました: {e}")
    return updated_df