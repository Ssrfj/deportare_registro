import os
import pandas as pd
from auto_check import perform_automatic_checks
from utils import get_jst_now
from excel_to_csv import excel_to_csv
from load_latest_club_data import load_latest_club_data
from merge_and_save_apcption_data import merge_and_save_apcption_data
from make_checklist_for_each_club import make_checklist_for_each_club
from make_and_write_documents_checklist_for_human import make_documents_checklist_for_human, write_checklist_by_human_check
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
# ログファイルの設定
log_file_path = os.path.join('R7_登録申請処理', 'logs', 'process_log.txt')
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
file_handler.setFormatter(formatter)
logging.getLogger().addHandler(file_handler)

def main():
    try:
        # 1. Excel→CSV化
        try:
            excel_to_csv()
        except Exception as e:
            logging.error(f"Excel→CSV化処理でエラー: {e}", exc_info=True)
            return

        # 2. 最新クラブデータの読み込み
        try:
            latest_club_df = load_latest_club_data()
        except Exception as e:
            logging.error(f"最新クラブデータの読み込みでエラー: {e}", exc_info=True)
            return

        # 3. 申請内容と過去データを結合
        try:
            merge_and_save_apcption_data()
        except Exception as e:
            logging.error(f"申請内容と過去データの結合でエラー: {e}", exc_info=True)
            return

        # 4. 申請受付リストの最新ファイルを取得
        folder_path = os.path.join('R7_登録申請処理','申請受付リスト')
        try:
            files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]
            if not files:
                logging.error(f"{folder_path} にCSVファイルが存在しません。")
                return
            latest_file = max(files, key=os.path.getctime)
            club_list_df = pd.read_csv(latest_file)
            club_list_df['R8年度登録申請_タイムスタンプ'] = pd.to_datetime(club_list_df['R8年度登録申請_タイムスタンプ'], errors='coerce')
            club_list_df['R8年度登録申請_タイムスタンプyyyymmddHHMMSS'] = club_list_df['R8年度登録申請_タイムスタンプ'].dt.strftime('%Y%m%d%H%M%S')
            logging.info("申請内容の読み込みが完了しました")
        except Exception as e:
            logging.error(f"申請受付リストの取得・読み込みでエラー: {e}", exc_info=True)
            return

        # 5. チェックリスト作成状況ファイルの読み込みまたは新規作成
        folder_of_checklist_create_status = os.path.join('R7_登録申請処理', '申請入力内容')
        file_of_checklist_create_status = os.path.join(folder_of_checklist_create_status, 'クラブごとのチェックリスト作成状況.csv')
        try:
            os.makedirs(folder_of_checklist_create_status, exist_ok=True)
            logging.info(f"チェックリスト作成状況フォルダ: {folder_of_checklist_create_status} を作成しました")
            if os.path.exists(file_of_checklist_create_status):
                checklist_status_df = pd.read_csv(file_of_checklist_create_status)
                for col in ['クラブ名', '申請日時', 'チェックリスト作成日時']:
                    if col not in checklist_status_df.columns:
                        checklist_status_df[col] = ''
                # ここでR8年度登録申請_タイムスタンプyyyymmddHHMMSSカラムも追加
                if 'R8年度登録申請_タイムスタンプyyyymmddHHMMSS' not in checklist_status_df.columns:
                    checklist_status_df['R8年度登録申請_タイムスタンプyyyymmddHHMMSS'] = ''
                logging.debug(f"checklist_status_df columns after clean: {checklist_status_df.columns.tolist()}")
                logging.info('クラブごとのチェックリスト作成状況.csvはすでに存在しています')
            else:
                checklist_status_df = pd.DataFrame(columns=['クラブ名','申請日時', 'チェックリスト作成日時', 'R8年度登録申請_タイムスタンプyyyymmddHHMMSS'])
                checklist_status_df.to_csv(file_of_checklist_create_status, index=False)
                logging.info('クラブごとのチェックリスト作成状況.csvが作成されました')
        except Exception as e:
            logging.error(f"チェックリスト作成状況ファイルの処理でエラー: {e}", exc_info=True)
            return

        # 6. club_list_dfの['R8年度登録申請状況']が1のクラブのみを抽出
        try:
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
        except Exception as e:
            logging.error(f"クラブ抽出処理でエラー: {e}", exc_info=True)
            return

        # 7. 各種処理
        try:
            # カラム名の確認とリネーム
            if '申請日時' not in apried_club_list_df.columns and 'R8年度登録申請_タイムスタンプyyyymmddHHMMSS' in apried_club_list_df.columns:
                apried_club_list_df['申請日時'] = apried_club_list_df['R8年度登録申請_タイムスタンプyyyymmddHHMMSS']
            checklist_output_folder = folder_of_checklist_create_status
            timestamp_for_make_checklist = get_jst_now().strftime('%Y%m%d%H%M%S')
            checklist_status_df = make_checklist_for_each_club(
                apried_club_list_df,
                checklist_status_df,
                checklist_output_folder,
                timestamp_for_make_checklist
            )
            logging.info('各クラブの自動チェックを実行します...')
            checklist_status_df = perform_automatic_checks(checklist_status_df, apried_club_list_df)
            logging.info('全てのクラブの自動チェックが完了しました。')
            logging.info('処理が終了しました')

            logging.info('人間がチェックする用のリストの作成をクラブごとに実行します...')
            checklist_status_df = make_documents_checklist_for_human(apried_club_list_df, checklist_status_df)
            if checklist_status_df is None:
                logging.error("make_documents_checklist_for_humanの戻り値がNoneです")
                return
            logging.info('人間がチェックする用のリストの作成をクラブごとに作成しました。')

            logging.info('人間がチェックする用チェックリストのチェック状況の更新を行います...')
            checklist_status_df = write_checklist_by_human_check(checklist_status_df, apried_club_list_df, folder_of_checklist_create_status)
            logging.info('人間がチェックする用チェックリストのチェック状況の更新を行いました。')
            logging.info('全ての処理が完了しました。')
            print("全ての処理が完了しました。")
        except Exception as e:
            logging.error(f"チェックリスト関連処理でエラー: {e}", exc_info=True)
            return

    except Exception as e:
        logging.critical(f"予期せぬ致命的なエラーが発生しました: {e}", exc_info=True)
        return
    
    # logをtxtファイルに保存
    log_file_path = os.path.join('R7_登録申請処理', 'logs', f'log_{get_jst_now().strftime("%Y%m%d%H%M%S")}.txt')
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    with open(log_file_path, 'w') as log_file:
        for handler in logging.getLogger().handlers:
            if isinstance(handler, logging.FileHandler):
                log_file.write(f"Log file: {handler.baseFilename}\n")
                with open(handler.baseFilename, 'r') as f:
                    log_file.write(f.read())
    logging.info(f"ログファイルを保存しました: {log_file_path}")
    print(f"ログファイルを保存しました: {log_file_path}")

if __name__ == "__main__":
    main()