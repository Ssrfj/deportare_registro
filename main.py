import os
import pandas as pd
from datetime import datetime, timezone, timedelta

from checklist_generator import (
    make_document1_checklist_for_human, make_document2_1_checklist_for_human,
)
from auto_check import perform_automatic_checks
from utils import get_jst_now

from excel_to_csv import excel_to_csv
from load_latest_club_data import load_latest_club_data
from merge_and_save_apcption_data import merge_and_save_apcption_data
from make_checklist_for_each_club import make_checklist_for_each_club
from make_and_write_documents_checklist_for_human import make_documents_checklist_for_human, write_checklist_by_human_check

from dataframe_utils import clean_column_names
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
def main():
    # 1. Excel→CSV化
    excel_to_csv()

    # 2. 最新クラブデータの読み込み（必要ならここで何か使う場合は変数で受け取る）
    latest_club_df = load_latest_club_data()
    # ※merge_and_save内で再度読み込む場合はこの行は省略可

    # 3. 申請内容と過去データを結合して申請受付リストに保存
    merge_and_save_apcption_data()

    # 4. 申請受付リストの最新ファイルを取得
    folder_path = os.path.join('R7_登録申請処理','申請受付リスト')
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]
    if not files:
        logging.error(f"{folder_path} にCSVファイルが存在しません。")
        return
    latest_file = max(files, key=os.path.getctime)
    try:
        club_list_df = pd.read_csv(latest_file)
        club_list_df['R8年度登録申請_タイムスタンプ'] = pd.to_datetime(club_list_df['R8年度登録申請_タイムスタンプ'], errors='coerce')
        club_list_df['R8年度登録申請_タイムスタンプyyyymmddHHMMSS'] = club_list_df['R8年度登録申請_タイムスタンプ'].dt.strftime('%Y%m%d%H%M%S')
        logging.info("申請内容の読み込みが完了しました")
    except Exception as e:
        logging.error(f"申請内容の読み込み中にエラーが発生しました: {e}")
        return

    # 5. チェックリスト作成状況ファイルの読み込みまたは新規作成
    folder_of_checklist_create_status = os.path.join('R7_登録申請処理', '申請入力内容')
    file_of_checklist_create_status = os.path.join(folder_of_checklist_create_status, 'クラブごとのチェックリスト作成状況.csv')
    if os.path.exists(file_of_checklist_create_status):
        checklist_status_df = pd.read_csv(file_of_checklist_create_status)
        # 必要なカラムがなければ追加
        for col in ['クラブ名', '申請日時', 'チェックリスト作成日時']:
            if col not in checklist_status_df.columns:
                checklist_status_df[col] = ''
        logging.debug(f"checklist_status_df columns after clean: {checklist_status_df.columns.tolist()}")
        logging.info('クラブごとのチェックリスト作成状況.csvはすでに存在しています')
    else:
        checklist_status_df = pd.DataFrame(columns=['クラブ名','申請日時', 'チェックリスト作成日時'])
        checklist_status_df.to_csv(file_of_checklist_create_status, index=False)
        logging.info('クラブごとのチェックリスト作成状況.csvが作成されました')

    # club_list_dfの['R8年度登録申請状況']が1のクラブのみを抽出
    # club_list_dfの['R8年度登録申請状況']が1のクラブのみを抽出
    club_list_df.columns = club_list_df.columns.str.strip()
    logging.debug(f"club_list_df columns: {club_list_df.columns.tolist()}")
    apried_club_list_df = club_list_df[club_list_df['R8年度登録申請状況'] == 1]
    logging.debug(f"apried_club_list_df columns: {apried_club_list_df.columns.tolist()}")
    if 'R7年度登録クラブ' not in apried_club_list_df.columns:
        logging.error("apried_club_list_dfに'R7年度登録クラブ'カラムがありません")
    else:
        logging.info("apried_club_list_dfに'R7年度登録クラブ'カラムが存在します")
    if apried_club_list_df.empty:
        logging.warning("R8年度登録申請状況が1のクラブが存在しません。")
    else:
        logging.info(f"R8年度登録申請状況が1のクラブ数: {len(apried_club_list_df)}")

    # ここでmake_checklist_for_each_clubを呼び出す
    checklist_output_folder = folder_of_checklist_create_status
    timestamp_for_make_checklist = get_jst_now().strftime('%Y%m%d%H%M%S')
    checklist_status_df = make_checklist_for_each_club(
        apried_club_list_df,
        checklist_status_df,
        checklist_output_folder,
        timestamp_for_make_checklist
    )
   
    # 6. 各クラブに対して自動チェックを実行
    logging.info('各クラブの自動チェックを実行します...')
    checklist_status_df = perform_automatic_checks(checklist_status_df, apried_club_list_df)
    logging.info('全てのクラブの自動チェックが完了しました。')
    logging.info('処理が終了しました')

    # 7. 人間がチェックする用チェックリストの作成とチェックリストのチェック状況をクラブごとに更新
    logging.info('人間がチェックする用のリストの作成とチェックリストのチェック状況をクラブごとに更新します...')
    checklist_status_df = make_documents_checklist_for_human(checklist_status_df, apried_club_list_df)
    print('人間がチェックする用のリストの作成とチェックリストのチェック状況の更新を行います...')

    # 8. 人間がチェックする用のリストの作成とチェックリストのチェック状況の更新
    logging.info('人間がチェックする用のリストの作成とチェックリストのチェック状況の更新を行います...')
    checklist_status_df = write_checklist_by_human_check(checklist_status_df, apried_club_list_df, folder_of_checklist_create_status)
    logging.info('人間がチェックする用のリストの作成とチェックリストのチェック状況の更新が完了しました。')
    logging.info('全ての処理が完了しました。')

if __name__ == "__main__":
    main()