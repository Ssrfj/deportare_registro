import os
import pandas as pd
import logging
import chardet

from src.folder_management.make_folders import create_folders
from src.core.logginng import setup_logging, save_logs
from src.data_processing.processing_reception_data import processing_reception_data
from src.data_processing.marge_reception_data_with_club_info import marge_reception_data_with_club_info
from src.data_processing.reception_statues import reception_statues
# from src.folder_management.make_detailed_data_folders import make_detailed_data_folders  # 不要なフォルダ作成のため無効化
from src.checklist.generators.make_chacklists import make_chacklists
from src.checklist.automation.automation_check_and_update_checklist import automation_check_and_update_checklist

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
    logging.info("プログラムを開始します")
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
    elif latest_reception_data_date == "no_data":
        logging.info("処理済みデータも申請データも見つからないため、処理を終了します。")
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
    # 注：申請内容チェック用の空フォルダは作成しない（実際には使用されないため）
    # logging.info("受付内容チェック用のフォルダを作成します")
    # make_detailed_data_folders()
    # logging.info("受付内容チェック用のフォルダを作成しました")

    # チェックリストを作成
    logging.info("チェックリストを作成します")
    make_chacklists(latest_reception_data_date)
    logging.info("チェックリストの作成が完了しました")

    # チェックリストの更新・自動チェック
    logging.info("チェックリストの更新・自動チェックを実行します")
    automation_check_and_update_checklist(latest_reception_data_date)
    logging.info("チェックリストの更新・自動チェックが完了しました")

    # 今後の作業memo
    # チェック状況に応じたメールの文面案の作成
    # チェック結果をPDＦで出力
    # めも：書類間の整合性は、ある程度自動化できるかも…

    # チェック状況に応じたメールの文面案の作成
    # logging.info("チェック状況に応じたメールの文面案を作成します")
    # make_email_templates()
    # logging.info("チェック状況に応じたメールの文面案の作成が完了しました")

    # # チェック結果をPDＦで出力
    # logging.info("チェック状況をPDFで出力します")
    # output_check_status_pdf()
    # logging.info("チェック状況のPDF出力が完了しました")

    # ログファイルの保存（個別実行分と統合版の両方）
    save_logs()


# メインの処理を実行
if __name__ == "__main__":
    try:
        print("プログラムを開始します")
        main()
        print("プログラムが終了しました")
        
    except Exception as e:
        logging.critical(f"予期せぬ致命的なエラーが発生しました: {e}", exc_info=True)
        print(f"予期せぬ致命的なエラーが発生しました: {e}")

# memo:
# 変なカラムが出力されている