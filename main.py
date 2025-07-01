import os
import pandas as pd
import logging
import chardet

from auto_check import perform_automatic_checks
from utils import get_jst_now
from column_name_change import column_name_change
from load_latest_club_data import load_latest_club_data
from merge_and_save_apcption_data import merge_and_save_apcption_data
from make_checklist_for_each_club import make_checklist_for_each_club
from make_and_write_documents_checklist_for_human import make_documents_checklist_for_human, write_checklist_by_human_check
from setting_paths import (
    output_main_folder,
    log_folder_name,
    log_folder_path,
    reception_data_folder_name,
    reception_data_folder_path,
    reception_data_with_club_info_folder_name,
    reception_data_with_club_info_folder_path,
    Content_check_folder_name,
    Content_check_folder_path
)
from make_folders import create_folders
from logginng import setup_logging, save_logs
from processing_reception_data import processing_reception_data
from marge_reception_data_with_club_info import marge_reception_data_with_club_info
from reception_statues import reception_statues
from make_detailed_data_folders import make_detailed_data_folders
from make_chacklists import make_chacklists
from automation_check_and_update_checklist import automation_check_and_update_checklist
from make_email_templates import make_email_templates
from output_check_status_pdf import output_check_status_pdf

# ログファイルのエンコーディングを自動検出して読み込む関数
# 作業のログを実行ごとにtxtファイルに保存するための関数
import chardet
def read_log_with_detected_encoding(filepath):
    with open(filepath, 'rb') as f:
        raw = f.read()
        result = chardet.detect(raw)
        encoding = result['encoding']
    with open(filepath, 'r', encoding=encoding) as f:
        return f.read()

# メインの処理
def main():
    # ログの設定
    setup_logging()
    logging.info("ロギングを設定しました")

    # フォルダの作成
    logging.info("必要なフォルダを作成します")
    create_folders()
    logging.info("必要なフォルダを作成しました")

    # 受付データ処理の受付処理
    logging.info("受付データ処理の受付を開始します")
    latest_reception_data_date = processing_reception_data()
    if latest_reception_data_date is None:
        logging.error("受付データ処理に失敗しました。処理を終了します。")
        return
    logging.info("受付データ処理の受付が完了しました")
    logging.info(f"最新の受付データの日付: {latest_reception_data_date}")

    # 処理済みデータにクラブ情報を追加
    logging.info("処理済み受付データにクラブ情報を追加します")
    marge_reception_data_with_club_info(latest_reception_data_date)
    logging.info("処理済み受付データにクラブ情報を追加しました")

    # 受付状況を更新
    logging.info("受付状況を更新します")
    reception_statues(latest_reception_data_date)
    logging.info("受付状況の更新が完了しました")

    # 受付内容チェック用ように参照するデータを保存するクラブごとのフォルダを作成
    logging.info("受付内容チェック用のフォルダを作成します")
    make_detailed_data_folders()
    logging.info("受付内容チェック用のフォルダを作成しました")

    # チェックリストを作成
    logging.info("チェックリストを作成します")
    make_chacklists(latest_reception_data_date)
    logging.info("チェックリストの作成が完了しました")

    # チェックリストの更新・自動チェック
    logging.info("チェックリストの更新・自動チェックを実行します")
    automation_check_and_update_checklist()
    logging.info("チェックリストの更新・自動チェックが完了しました")

    # 今後の作業memo
    # チェックリストの更新・自動チェック
    # チェック状況に応じたメールの文面案の作成
    # チェック結果をPDＦで出力
    # めも：書類間の整合性は、ある程度自動化できるかも…

    # チェック状況に応じたメールの文面案の作成
    logging.info("チェック状況に応じたメールの文面案を作成します")
    make_email_templates()
    logging.info("チェック状況に応じたメールの文面案の作成が完了しました")

    # チェック結果をPDＦで出力
    logging.info("チェック状況をPDFで出力します")
    output_check_status_pdf()
    logging.info("チェック状況のPDF出力が完了しました")

    # ログファイルの保存（個別実行分と統合版の両方）
    save_logs()


# メインの処理を実行
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.critical(f"予期せぬ致命的なエラーが発生しました: {e}", exc_info=True)
        print(f"予期せぬ致命的なエラーが発生しました: {e}")

'''一括で過去に書いたコードをコメントアウト
def main():
    try:
        # 1. Excelのカラム名修正
        try:
            column_name_change()
        except Exception as e:
            logging.error(f"Excelのカラム名修正でエラー: {e}", exc_info=True)
            return

        # 2. 最新クラブデータの読み込み
        try:
            latest_club_df = load_latest_club_data()
        except Exception as e:
            logging.error(f"最新クラブデータの読み込みでエラー: {e}", exc_info=True)
            return

        # 3. 受付内容と過去データを結合
        try:
            merge_and_save_apcption_data()
        except Exception as e:
            logging.error(f"受付内容と過去データの結合でエラー: {e}", exc_info=True)
            return

        # 4. 受付受付リストの最新ファイルを取得
        folder_path = os.path.join('R7_登録受付処理','受付受付')
        try:
            os.makedirs(folder_path, exist_ok=True)
            files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.xlsx')]
            if not files:
                logging.error(f"{folder_path} にExcelファイルが存在しません。")
                return
            latest_file = max(files, key=os.path.getctime)
            club_list_df = pd.read_excel(latest_file)
            club_list_df['R8年度登録受付_タイムスタンプ'] = pd.to_datetime(club_list_df['R8年度登録受付_タイムスタンプ'], errors='coerce')
            club_list_df['R8年度登録受付_タイムスタンプyyyymmddHHMMSS'] = club_list_df['R8年度登録受付_タイムスタンプ'].dt.strftime('%Y%m%d%H%M%S')
            logging.info("受付内容の読み込みが完了しました")
        except Exception as e:
            logging.error(f"受付受付リストの取得・読み込みでエラー: {e}", exc_info=True)
            return

        # 5. 受付内容チェックリスト作成状況ファイルの読み込みまたは新規作成
        folder_of_checklist = os.path.join('R7_登録受付処理', '受付内容チェック')
        file_of_checklist_create_status = os.path.join(folder_of_checklist, '受付内容チェックリスト.xlsx')
        logging.info(f"受付内容チェックリストファイル: {file_of_checklist_create_status}")
        try:
            os.makedirs(folder_of_checklist, exist_ok=True)
            logging.info(f"受付内容チェックリスト作成状況フォルダ: {folder_of_checklist} を作成しました")
            if os.path.exists(file_of_checklist_create_status):
                checklist_status_df = pd.read_excel(file_of_checklist_create_status)
                for col in ['クラブ名', '受付日時', 'チェックリスト作成日時']:
                    if col not in checklist_status_df.columns:
                        checklist_status_df[col] = ''
                # ここでR8年度登録受付_タイムスタンプyyyymmddHHMMSSカラムも追加
                if 'R8年度登録受付_タイムスタンプyyyymmddHHMMSS' not in checklist_status_df.columns:
                    checklist_status_df['R8年度登録受付_タイムスタンプyyyymmddHHMMSS'] = ''
                logging.debug(f"checklist_status_df columns after clean: {checklist_status_df.columns.tolist()}")
                logging.info('クラブごとのチェックリスト作成状況.xlsxはすでに存在しています')
            else:
                checklist_status_df = pd.DataFrame(columns=['クラブ名','受付日時', 'チェックリスト作成日時'])
                checklist_status_df.to_excel(file_of_checklist_create_status, index=False)
                logging.info('クラブごとのチェックリスト作成状況.xlsxが作成されました')
        except Exception as e:
            logging.error(f"チェックリスト作成状況ファイルの処理でエラー: {e}", exc_info=True)
            return

        # 6. club_list_dfの['R8年度登録受付状況']が1のクラブのみを抽出
        try:
            club_list_df.columns = club_list_df.columns.str.strip()
            logging.debug(f"club_list_df columns: {club_list_df.columns.tolist()}")
            apried_club_list_df = club_list_df[club_list_df['R8年度登録受付状況'] == 1]
            logging.info(f"apried_club_list_df columns: {apried_club_list_df.columns.tolist()}")
            logging.info(f"apried_club_list_df: {apried_club_list_df}")
            if 'R7年度登録クラブ' not in apried_club_list_df.columns:
                logging.error("apried_club_list_dfに'R7年度登録クラブ'カラムがありません")
            else:
                logging.info("apried_club_list_dfに'R7年度登録クラブ'カラムが存在します")
            if apried_club_list_df.empty:
                logging.warning("R8年度登録受付状況が1のクラブが存在しません。")
            else:
                logging.info(f"R8年度登録受付状況が1のクラブ数: {len(apried_club_list_df)}")
        except Exception as e:
            logging.error(f"クラブ抽出処理でエラー: {e}", exc_info=True)
            return

        # 7. 各種処理
        try:
            # カラム名の確認とリネーム
            if '受付日時' not in apried_club_list_df.columns and 'R8年度登録受付_タイムスタンプyyyymmddHHMMSS' in apried_club_list_df.columns:
                apried_club_list_df['受付日時'] = apried_club_list_df['R8年度登録受付_タイムスタンプyyyymmddHHMMSS']
            # 必要なカラムがなければ追加
            for col in ['チェックリスト作成日時']:
                if col not in apried_club_list_df.columns:
                    apried_club_list_df[col] = ''
                if col not in checklist_status_df.columns:
                    checklist_status_df[col] = ''
            checklist_output_folder = folder_of_checklist
            timestamp_for_make_checklist = get_jst_now().strftime('%Y%m%d%H%M%S')
            each_club_checklist_status_df = make_checklist_for_each_club(
                apried_club_list_df,
                checklist_status_df,
                checklist_output_folder,
                timestamp_for_make_checklist
            )
            logging.info(f"debug; each_club_checklist_status_df columns: {each_club_checklist_status_df.columns.tolist()}")
            logging.info(f"debug; each_club_checklist_status_df: {each_club_checklist_status_df}")
            # クラブごとのチェックリスト作成状況.xlsxを更新
            if each_club_checklist_status_df is None:
                logging.error("make_checklist_for_each_clubの戻り値がNoneです")
                return
            each_club_checklist_status_df.to_excel(file_of_checklist_create_status, index=False)
            logging.info(f"クラブごとのチェックリスト作成状況.xlsxを更新しました: {file_of_checklist_create_status}")
            logging.info(f"make_checklist_for_each_club後のeach_club_checklist_status_df: {each_club_checklist_status_df}")
            logging.info('各クラブの自動チェックを実行します...')
            each_club_checklist_status_df = perform_automatic_checks(each_club_checklist_status_df, apried_club_list_df)
            each_club_checklist_status_df.to_excel(file_of_checklist_create_status, index=False)
            logging.info('全てのクラブの自動チェックが完了しました。')
            logging.info('処理が終了しました')

            logging.info('人間がチェックする用のリストの作成をクラブごとに実行します...')
            each_club_checklist_status_df = make_documents_checklist_for_human(each_club_checklist_status_df, apried_club_list_df)
            if each_club_checklist_status_df is None:
                logging.error("make_documents_checklist_for_humanの戻り値がNoneです")
                return
            logging.info('人間がチェックする用のリストの作成をクラブごとに作成しました。')

            logging.info('人間がチェックする用チェックリストのチェック状況の更新を行います...')
            # apried_club_list_dfに受付_区市町村名というカラムが存在するか確認
            if '受付_区市町村名' not in each_club_checklist_status_df.columns:
                if '受付_区市町村名' in apried_club_list_df.columns:
                    each_club_checklist_status_df['受付_区市町村名'] = apried_club_list_df['受付_区市町村名']
                else:
                    each_club_checklist_status_df['受付_区市町村名'] = ''
            # each_club_checklist_status_dfがNoneでないことを確認
            if each_club_checklist_status_df is None:
                logging.error("each_club_checklist_status_dfがNoneです。")
            else:
                logging.info("each_club_checklist_status_dfはNoneではありません。")
            # each_club_checklist_status_dfが空でないことを確認
            if each_club_checklist_status_df.empty:
                logging.error("each_club_checklist_status_dfが空です。")
            else:
                logging.info("each_club_checklist_status_dfは空ではありません。")
            each_club_checklist_status_df = write_checklist_by_human_check(each_club_checklist_status_df, apried_club_list_df, folder_of_checklist)
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
    log_file_path = os.path.join('R7_登録受付処理', 'logs', f'log_{get_jst_now().strftime("%Y%m%d%H%M%S")}.txt')
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    # ログファイルを出力する箇所で
    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        for handler in logging.getLogger().handlers:
            if isinstance(handler, logging.FileHandler):
                log_file.write(f"Log file: {handler.baseFilename}\n")
                try:
                    log_file.write(read_log_with_detected_encoding(handler.baseFilename))
                except Exception as e:
                    log_file.write(f"\n[ログ読込エラー: {e}]\n")
        logging.info(f"ログファイルを保存しました: {log_file_path}")
        print(f"ログファイルを保存しました: {log_file_path}")

if __name__ == "__main__":
    main()
'''