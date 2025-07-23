import logging

from src.folder_management.make_folders import create_folders
from src.core.logginng import setup_logging, save_logs
from src.data_processing.processing_reception_data import processing_reception_data
from src.data_processing.marge_reception_data_with_club_info import marge_reception_data_with_club_info
from src.data_processing.reception_statues import reception_statues
from src.checklist.generators.make_chacklists import make_chacklists
from src.checklist.automation.automation_check_and_update_checklist import automation_check_and_update_checklist
from src.human_interface.email_draft_generator import EmailDraftGenerator
from src.core.setting_paths import email_drafts_folder_path
import pandas as pd
import os

def make_email_templates(latest_reception_data_date):
    """
    チェック状況に応じたメールの文面案を作成
    """
    try:
        # 最新の総合チェックリストファイルを探す
        overall_checklist_folder = f"output/R7_登録受付処理/受付内容チェック/総合チェックリスト"
        
        if not os.path.exists(overall_checklist_folder):
            logging.warning(f"総合チェックリストフォルダが見つかりません: {overall_checklist_folder}")
            return
        
        # 最新の総合チェックリストファイルを取得
        checklist_files = [f for f in os.listdir(overall_checklist_folder) if f.endswith('.xlsx')]
        if not checklist_files:
            logging.warning("総合チェックリストファイルが見つかりません")
            return
        
        # 最新ファイルを選択
        latest_checklist_file = max(checklist_files)
        checklist_path = os.path.join(overall_checklist_folder, latest_checklist_file)
        
        logging.info(f"総合チェックリストを読み込み中: {checklist_path}")
        
        # 総合チェックリストを読み込み
        checklist_df = pd.read_excel(checklist_path)
        
        # メール文面案生成器を初期化
        email_generator = EmailDraftGenerator()
        
        # 一括でメール文面案を生成
        generated_files = email_generator.generate_bulk_email_drafts(
            checklist_df=checklist_df,
            output_folder=email_drafts_folder_path
        )
        
        if generated_files:
            logging.info(f"メール文面案を生成しました（{len(generated_files)}件）:")
            for club_name, file_path in generated_files.items():
                logging.info(f"  - {club_name}: {file_path}")
        else:
            logging.info("エラーのあるクラブが見つからないため、メール文面案は生成されませんでした")
        
    except Exception as e:
        logging.error(f"メール文面案作成中にエラーが発生しました: {e}")


# メインの処理
def main():
    # ログの設定
    setup_logging()
    logging.info("プログラムを開始します")

    # フォルダの作成
    create_folders()
    logging.info("必要なフォルダを作成しました")

    # 受付データ処理
    logging.info("受付データ処理を開始します")
    latest_reception_data_date = processing_reception_data()
    if latest_reception_data_date is None:
        logging.error("受付データ処理に失敗しました。処理を終了します。")
        return
    elif latest_reception_data_date == "no_data":
        logging.info("処理済みデータも申請データも見つからないため、処理を終了します。")
        return
    logging.info(f"受付データ処理が完了しました - 最新データ日付: {latest_reception_data_date}")

    # 処理済みデータにクラブ情報を追加
    marge_reception_data_with_club_info(latest_reception_data_date)
    logging.info("クラブ情報の追加が完了しました")

    # 受付状況を更新
    reception_statues(latest_reception_data_date)
    logging.info("受付状況の更新が完了しました")

    # チェックリストを作成
    make_chacklists(latest_reception_data_date)
    logging.info("チェックリストの作成が完了しました")

    # 人間用のチェックリストを作成
    logging.info("人間用のチェックリストを作成します")
    from src.human_interface.make_and_write_documents_checklist_for_human import make_documents_checklist_for_human, write_checklist_by_human_check
    from src.core.load_latest_club_data import load_latest_club_reception_data
    from src.core.setting_paths import output_main_folder_path
    
    # 最新の受付データを読み込み
    club_reception_df = load_latest_club_reception_data()
    if club_reception_df is not None:
        # 初期のチェックリスト作成状況を作成（空のDataFrame）
        import pandas as pd
        checklist_status_df = pd.DataFrame(columns=['クラブ名', '申請日時', 'チェックリスト作成日時'])
        
        # 人間用チェックリストを作成
        checklist_status_df = make_documents_checklist_for_human(checklist_status_df, club_reception_df)
        logging.info("人間用のチェックリストの作成が完了しました")
        
        # 人間によるチェック状況の確認・更新
        logging.info("人間によるチェック状況の確認を実行します")
        checklist_status_df = write_checklist_by_human_check(checklist_status_df, club_reception_df, output_main_folder_path)
        logging.info("人間によるチェック状況の確認が完了しました")
    else:
        logging.error("受付データの読み込みに失敗しました")

    # チェックリストの更新・自動チェック
    automation_check_and_update_checklist(latest_reception_data_date)
    logging.info("チェックリストの更新・自動チェックが完了しました")

    # チェック状況に応じたメールの文面案の作成
    logging.info("チェック状況に応じたメールの文面案を作成します")
    make_email_templates(latest_reception_data_date)
    logging.info("チェック状況に応じたメールの文面案の作成が完了しました")

    # 今後の作業memo
    # チェック結果をPDFで出力
    
    # # チェック結果をPDFで出力
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
