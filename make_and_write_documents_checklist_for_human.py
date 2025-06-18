import os
import pandas as pd
import logging
from checklist_generator import (
    make_document1_checklist_for_human,
    make_document2_1_checklist_for_human,
    make_document2_2_checklist_for_human,
    make_document3_checklist_for_human,
    make_document4_checklist_for_human,
    make_document5_plan_checklist_for_human,
    make_document5_budget_checklist_for_human,
    make_document6_report_checklist_for_human,
    make_document6_financial_statements_checklist_for_human,
    make_document7_checklist_for_human,
    make_document8_checklist_for_human,
    make_document9_checklist_for_human
)
from utils import get_jst_now
from get_latest_checklist_file import get_latest_checklist_file
logging.basicConfig(
    level=logging.INFO,
    encoding='utf-8',
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# 書類の種類をリストで定義
type_of_documents = [
    'document_1',
    'document_2_1',
    'document_2_2',
    'document_3',
    'document_4',
    'document_5_plan',
    'document_5_budget',
    'document_6_report',
    'document_6_financial_statements',
    'document_7',
    'document_8',
    'document_9'
]

def make_documents_checklist_for_human(applied_club_df, checklist_status_df):
    """
    人間がチェックする用のリストを作成する関数

    Args:
        applied_club_df (pd.DataFrame): 申請済みクラブの一覧
        checklist_status_df (pd.DataFrame): チェックリスト作成状況
    """
    if checklist_status_df is None:
        checklist_status_df = pd.DataFrame(columns=['クラブ名','申請日時', 'チェックリスト作成日時', 'R8年度登録申請_タイムスタンプyyyymmddHHMMSS'])
    try:
        logging.info("人間が確認する用のチェックリストを作成しています...")
        # --- ここから元の処理 ---
        folder_path = os.path.join('R7_登録申請処理', '申請入力内容')
        for index, row in applied_club_df.iterrows():
            club_name = str(row['クラブ名']).strip()
            apried_date_str = str(row.get('申請日時', row.get('R8年度登録申請_タイムスタンプyyyymmddHHMMSS', ''))).strip()
            if 'R8年度登録申請_タイムスタンプyyyymmddHHMMSS' not in checklist_status_df.columns:
                checklist_status_df['R8年度登録申請_タイムスタンプyyyymmddHHMMSS'] = ''
            match = checklist_status_df[
                (checklist_status_df['クラブ名'] == club_name) &
                (checklist_status_df['申請日時'] == apried_date_str)
            ]
            if 'チェックリスト作成日時' in match.columns and not match.empty:
                checklist_creation_date_str = match.iloc[0]['チェックリスト作成日時']
            logging.info(f"クラブ名: {club_name} の人間が確認する用のチェックリスト作成を開始します")
            # 保存されているチェックリストを読み込み、チェックを実行
            club_folder_path = os.path.join(folder_path, club_name)
            if not os.path.exists(club_folder_path):
                logging.warning(f"クラブ '{club_name}' のフォルダが存在しません。スキップします。")
                continue
            document1_checklist_for_human_folder_name = 'document_1_checklist_for_human'
            document1_checklist_for_human_folder_path = os.path.join(club_folder_path, document1_checklist_for_human_folder_name)
            document2_1_checklist_for_human_folder_name = 'document_2_1_checklist_for_human'
            document2_1_checklist_for_human_folder_path = os.path.join(club_folder_path, document2_1_checklist_for_human_folder_name)
            document2_2_checklist_for_human_folder_name = 'document_2_2_checklist_for_human'
            document2_2_checklist_for_human_folder_path = os.path.join(club_folder_path, document2_2_checklist_for_human_folder_name)
            document3_checklist_for_human_folder_name = 'document_3_checklist_for_human'
            document3_checklist_for_human_folder_path = os.path.join(club_folder_path, document3_checklist_for_human_folder_name)
            document4_checklist_for_human_folder_name = 'document_4_checklist_for_human'
            document4_checklist_for_human_folder_path = os.path.join(club_folder_path, document4_checklist_for_human_folder_name)
            document5_plan_checklist_for_human_folder_name = 'document_5_plan_checklist_for_human'
            document5_plan_checklist_for_human_folder_path = os.path.join(club_folder_path, document5_plan_checklist_for_human_folder_name)
            document5_budget_checklist_for_human_folder_name = 'document_5_budget_checklist_for_human'
            document5_budget_checklist_for_human_folder_path = os.path.join(club_folder_path, document5_budget_checklist_for_human_folder_name)
            document6_report_checklist_for_human_folder_name = 'document_6_report_checklist_for_human'
            document6_report_checklist_for_human_folder_path = os.path.join(club_folder_path, document6_report_checklist_for_human_folder_name)
            document6_financial_statements_checklist_for_human_folder_name = 'document_6_financial_statements_checklist_for_human'
            document6_financial_statements_checklist_for_human_folder_path = os.path.join(club_folder_path, document6_financial_statements_checklist_for_human_folder_name)
            document7_checklist_for_human_folder_name = 'document_7_checklist_for_human'
            document7_checklist_for_human_folder_path = os.path.join(club_folder_path, document7_checklist_for_human_folder_name)
            document8_checklist_for_human_folder_name = 'document_8_checklist_for_human'
            document8_checklist_for_human_folder_path = os.path.join(club_folder_path, document8_checklist_for_human_folder_name)
            document9_checklist_for_human_folder_name = 'document_9_checklist_for_human'
            document9_checklist_for_human_folder_path = os.path.join(club_folder_path, document9_checklist_for_human_folder_name)
            
            # 各書類のチェックリストを作成
            club_df = checklist_status_df[
                (checklist_status_df['クラブ名'] == club_name) &
                (checklist_status_df['申請日時'] == apried_date_str)
            ]
            # 書類1
            document1_checklist = make_document1_checklist_for_human(club_df, applied_club_df)
            os.makedirs(document1_checklist_for_human_folder_path, exist_ok=True)
            # 書類1のチェックリストをExcelファイルとして保存
            document1_checklist_for_human_file_name = f'{club_name}_document1_checklist_申請{apried_date_str}.xlsx'
            pd.DataFrame(document1_checklist).to_excel(
                os.path.join(document1_checklist_for_human_folder_path, document1_checklist_for_human_file_name),
                index=False
            )
            # 書類2_1
            document2_1_checklist,document2_1_number_of_menbers,document2_1_number_of_annual_fee_members = make_document2_1_checklist_for_human(club_df, applied_club_df)
            os.makedirs(document2_1_checklist_for_human_folder_path, exist_ok=True)
            # 書類2_1のフォルダが存在しない場合は作成
            if not os.path.exists(document2_1_checklist_for_human_folder_path):
                os.makedirs(document2_1_checklist_for_human_folder_path)
            # 書類2_1のチェックリストをExcelファイルとして保存(1つのExcelで、複数のシートに分けて出力)
            document2_1_checklist_for_human_file_name = f'{club_name}_document2_1_checklist_申請{apried_date_str}.xlsx'
            document2_1_checklist_for_human_file_path = os.path.join(document2_1_checklist_for_human_folder_path, document2_1_checklist_for_human_file_name)
            with pd.ExcelWriter(document2_1_checklist_for_human_file_path, engine='openpyxl') as writer:
                # チェックリストのデータフレームをシートに書き込む
                pd.DataFrame(document2_1_checklist).to_excel(writer, sheet_name='チェックリスト', index=False)
                # 会員数のデータフレームをシートに書き込む
                pd.DataFrame(document2_1_number_of_menbers).to_excel(writer, sheet_name='会員数', index=False)
                # 年会費会員数のデータフレームをシートに書き込む
                pd.DataFrame(document2_1_number_of_annual_fee_members).to_excel(writer, sheet_name='年会費会員数', index=False)
            # 書類2_2
            document2_2_checklist, document2_2_discipline_and_coaches = make_document2_2_checklist_for_human(club_df, applied_club_df)
            os.makedirs(document2_2_checklist_for_human_folder_path, exist_ok=True)
            # 書類2_2のフォルダが存在しない場合は作成
            if not os.path.exists(document2_2_checklist_for_human_folder_path):
                os.makedirs(document2_2_checklist_for_human_folder_path)
            # 書類2_2のチェックリストをExcelファイルとして保存(1つのExcelで、複数のシートに分けて出力)
            document2_2_checklist_for_human_file_name = f'{club_name}_document2_2_checklist_申請{apried_date_str}.xlsx'
            document2_2_checklist_for_human_file_path = os.path.join(document2_2_checklist_for_human_folder_path, document2_2_checklist_for_human_file_name)
            with pd.ExcelWriter(document2_2_checklist_for_human_file_path, engine='openpyxl') as writer:
                # チェックリストのデータフレームをシートに書き込む
                pd.DataFrame(document2_2_checklist).to_excel(writer, sheet_name='チェックリスト', index=False)
                # 競技種目のデータフレームをシートに書き込む
                pd.DataFrame(document2_2_discipline_and_coaches).to_excel(writer, sheet_name='競技種目_および_指導者', index=False)
            # 書類3
            document3_checklist = make_document3_checklist_for_human(club_df, applied_club_df)
            os.makedirs(document3_checklist_for_human_folder_path, exist_ok=True)
            # 書類3のフォルダが存在しない場合は作成
            if not os.path.exists(document3_checklist_for_human_folder_path):
                os.makedirs(document3_checklist_for_human_folder_path)
            # 書類3のチェックリストをExcelファイルとして保存
            document3_checklist_for_human_file_name = f'{club_name}_document3_checklist_申請{apried_date_str}.xlsx'
            document3_checklist_for_human_file_path = os.path.join(document3_checklist_for_human_folder_path, document3_checklist_for_human_file_name)
            pd.DataFrame(document3_checklist).to_excel(
                document3_checklist_for_human_file_path,
                index=False)
            # 書類4
            document4_checklist, document4_lists_checklist = make_document4_checklist_for_human(club_df, applied_club_df)
            os.makedirs(document4_checklist_for_human_folder_path, exist_ok=True)
            # 書類4のフォルダが存在しない場合は作成
            if not os.path.exists(document4_checklist_for_human_folder_path):
                os.makedirs(document4_checklist_for_human_folder_path)
            # 書類4のチェックリストをExcelファイルとして保存(1つのExcelで、複数のシートに分けて出力)
            document4_checklist_for_human_file_name = f'{club_name}_document4_checklist_申請{apried_date_str}.xlsx'
            document4_checklist_for_human_file_path = os.path.join(document4_checklist_for_human_folder_path, document4_checklist_for_human_file_name)
            with pd.ExcelWriter(document4_checklist_for_human_file_path, engine='openpyxl') as writer:
                # チェックリストのデータフレームをシートに書き込む
                pd.DataFrame(document4_checklist).to_excel(writer, sheet_name='チェックリスト', index=False)
                # リストのチェックリストのデータフレームをシートに書き込む(5つの同内容のリストをそれぞれのシートに分けて出力)
                pd.DataFrame(document4_lists_checklist).to_excel(writer, sheet_name='リストチェック_1', index=False)
                pd.DataFrame(document4_lists_checklist).to_excel(writer, sheet_name='リストチェック_2', index=False)
                pd.DataFrame(document4_lists_checklist).to_excel(writer, sheet_name='リストチェック_3', index=False)
                pd.DataFrame(document4_lists_checklist).to_excel(writer, sheet_name='リストチェック_4', index=False)
                pd.DataFrame(document4_lists_checklist).to_excel(writer, sheet_name='リストチェック_5', index=False)

            # 書類5_事業計画
            document5_plan_checklist, document5_plan_checklist_discipline = make_document5_plan_checklist_for_human(club_df, applied_club_df)
            os.makedirs(document5_plan_checklist_for_human_folder_path, exist_ok=True)
            # 書類5_事業計画のフォルダが存在しない場合は作成
            if not os.path.exists(document5_plan_checklist_for_human_folder_path):
                os.makedirs(document5_plan_checklist_for_human_folder_path)
            # 書類5_事業計画のチェックリストをExcelファイルとして保存(1つのExcelで、複数のシートに分けて出力)
            document5_plan_checklist_for_human_file_name = f'{club_name}_document5_plan_checklist_申請{apried_date_str}.xlsx'
            document5_plan_checklist_for_human_file_path = os.path.join(document5_plan_checklist_for_human_folder_path, document5_plan_checklist_for_human_file_name)
            with pd.ExcelWriter(document5_plan_checklist_for_human_file_path, engine='openpyxl') as writer:
                # チェックリストのデータフレームをシートに書き込む
                pd.DataFrame(document5_plan_checklist).to_excel(writer, sheet_name='チェックリスト', index=False)
                # 競技種目のデータフレームをシートに書き込む
                pd.DataFrame(document5_plan_checklist_discipline).to_excel(writer, sheet_name='活動種目', index=False)
            # 書類5_予算
            document5_budget_checklist = make_document5_budget_checklist_for_human(club_df, applied_club_df)
            os.makedirs(document5_budget_checklist_for_human_folder_path, exist_ok=True)
            # 書類5_予算のフォルダが存在しない場合は作成
            if not os.path.exists(document5_budget_checklist_for_human_folder_path):
                os.makedirs(document5_budget_checklist_for_human_folder_path)
            # 書類5_予算のチェックリストをExcelファイルとして保存
            document5_budget_checklist_for_human_file_name = f'{club_name}_document5_budget_checklist_申請{apried_date_str}.xlsx'
            document5_budget_checklist_for_human_file_path = os.path.join(document5_budget_checklist_for_human_folder_path, document5_budget_checklist_for_human_file_name)
            pd.DataFrame(document5_budget_checklist).to_excel(
                document5_budget_checklist_for_human_file_path,
                index=False)
            # 書類6_事業報告
            document6_report_checklist, document6_report_checklist_discipline = make_document6_report_checklist_for_human(club_df, applied_club_df)
            os.makedirs(document6_report_checklist_for_human_folder_path, exist_ok=True)
            # 書類6_事業報告のフォルダが存在しない場合は作成
            if not os.path.exists(document6_report_checklist_for_human_folder_path):
                os.makedirs(document6_report_checklist_for_human_folder_path)
            # 書類6_事業報告のチェックリストをExcelファイルとして保存(1つのExcelで、複数のシートに分けて出力)
            document6_report_checklist_for_human_file_name = f'{club_name}_document6_report_checklist_申請{apried_date_str}.xlsx'
            document6_report_checklist_for_human_file_path = os.path.join(document6_report_checklist_for_human_folder_path, document6_report_checklist_for_human_file_name)
            with pd.ExcelWriter(document6_report_checklist_for_human_file_path, engine='openpyxl') as writer:
                # チェックリストのデータフレームをシートに書き込む
                pd.DataFrame(document6_report_checklist).to_excel(writer, sheet_name='チェックリスト', index=False)
                # 競技種目のデータフレームをシートに書き込む
                pd.DataFrame(document6_report_checklist_discipline).to_excel(writer, sheet_name='活動種目', index=False)
            # 書類6_決算
            document6_financial_statements_checklist = make_document6_financial_statements_checklist_for_human(club_df, applied_club_df)
            os.makedirs(document6_financial_statements_checklist_for_human_folder_path, exist_ok=True)
            # 書類6_決算のフォルダが存在しない場合は作成
            if not os.path.exists(document6_financial_statements_checklist_for_human_folder_path):
                os.makedirs(document6_financial_statements_checklist_for_human_folder_path)
            # 書類6_決算のチェックリストをExcelファイルとして保存
            document6_financial_statements_checklist_for_human_file_name = f'{club_name}_document6_financial_statements_checklist_申請{apried_date_str}.xlsx'
            document6_financial_statements_checklist_for_human_file_path = os.path.join(document6_financial_statements_checklist_for_human_folder_path, document6_financial_statements_checklist_for_human_file_name)
            pd.DataFrame(document6_financial_statements_checklist).to_excel(
                document6_financial_statements_checklist_for_human_file_path,
                index=False)
            # 書類7
            document7_checklist = make_document7_checklist_for_human(club_df, applied_club_df)
            os.makedirs(document7_checklist_for_human_folder_path, exist_ok=True)
            # 書類7のフォルダが存在しない場合は作成
            if not os.path.exists(document7_checklist_for_human_folder_path):
                os.makedirs(document7_checklist_for_human_folder_path)
            # 書類7のチェックリストをExcelファイルとして保存
            document7_checklist_for_human_file_name = f'{club_name}_document7_checklist_申請{apried_date_str}.xlsx'
            document7_checklist_for_human_file_path = os.path.join(document7_checklist_for_human_folder_path, document7_checklist_for_human_file_name)
            pd.DataFrame(document7_checklist).to_excel(
                document7_checklist_for_human_file_path,
                index=False)
            # 書類8
            document8_checklist = make_document8_checklist_for_human(club_df, applied_club_df)
            os.makedirs(document8_checklist_for_human_folder_path, exist_ok=True)
            # 書類8のフォルダが存在しない場合は作成
            if not os.path.exists(document8_checklist_for_human_folder_path):
                os.makedirs(document8_checklist_for_human_folder_path)
            # 書類8のチェックリストをExcelファイルとして保存
            document8_checklist_for_human_file_name = f'{club_name}_document8_checklist_申請{apried_date_str}.xlsx'
            document8_checklist_for_human_file_path = os.path.join(document8_checklist_for_human_folder_path, document8_checklist_for_human_file_name)
            pd.DataFrame(document8_checklist).to_excel(
                document8_checklist_for_human_file_path,
                index=False)
            # 書類9
            document9_checklist = make_document9_checklist_for_human(club_df, applied_club_df)
            os.makedirs(document9_checklist_for_human_folder_path, exist_ok=True)
            # 書類9のフォルダが存在しない場合は作成
            if not os.path.exists(document9_checklist_for_human_folder_path):
                os.makedirs(document9_checklist_for_human_folder_path)
            # 書類9のチェックリストをExcelファイルとして保存
            document9_checklist_for_human_file_name = f'{club_name}_document9_checklist_申請{apried_date_str}.xlsx'
            document9_checklist_for_human_file_path = os.path.join(document9_checklist_for_human_folder_path, document9_checklist_for_human_file_name)
            pd.DataFrame(document9_checklist).to_excel(
                document9_checklist_for_human_file_path,
                index=False)

            # 処理完了のメッセージを表示
            logging.info(f"クラブ名: {club_name} の人間が確認する用のチェックリスト作成が完了しました")
            logging.info("人間が確認する用のチェックリストの作成が完了しました。")
        return checklist_status_df
    except Exception as e:
        logging.error(f"make_documents_checklist_for_humanでエラー: {e}", exc_info=True)
        # 空のDataFrameを返すことで後続のAttributeErrorを防ぐ
        return pd.DataFrame()

def write_checklist_by_human_check(checklist_status_df, applied_club_df, folder_of_checklist_create_status):
    """
    チェックリストの作成状況を更新する関数

    Args:
        checklist_status_df (pd.DataFrame): チェックリスト作成状況
        applied_club_df (pd.DataFrame): 申請済みクラブの一覧
        folder_of_checklist_create_status (str): 保存先フォルダパス
    """

    # チェックリスト作成状況ファイルのパス
    # checklist_status_path = os.path.join(folder_of_checklist_create_status, 'クラブごとのチェックリスト作成状況.csv')
    
    for idx, row in applied_club_df.iterrows():
        club_name = str(row['クラブ名']).strip()
        # 申請日時を取得(['申請日時']が存在しない場合はR8年度登録申請_タイムスタンプyyyymmddHHMMSSを流用)
        application_date = str(row['申請日時']).strip() if '申請日時' in row else str(row.get('R8年度登録申請_タイムスタンプyyyymmddHHMMSS', '')).strip()
        # チェックリスト作成日時を取得
        checklist_creation_date = str(row['チェックリスト作成日時']).strip()
        club_folder = os.path.join(folder_of_checklist_create_status, club_name)
        # 処理開始のメッセージを表示
        logging.info(f"クラブ名: {club_name} の人間によるチェック状況の確認を開始します")
        if not os.path.exists(club_folder):
            logging.warning(f"クラブ '{club_name}' のフォルダが存在しません。スキップします。")
            continue
        else:
            logging.info(f"クラブ '{club_name}' のフォルダが存在します。チェックリストの確認を行います。")
            files_in_club_folder = os.listdir(club_folder)
            logging.debug(f"クラブ '{club_name}' のフォルダ内のファイル: {files_in_club_folder}")
        # クラブごとのチェックリストのファイル名を定義
        checklist_file_name = f"{club_name}_申請{application_date}_作成{checklist_creation_date}.csv"
        checklist_file_path = os.path.join(club_folder, checklist_file_name)
        # チェックリストのファイルが存在しない場合はスキップ
        if not os.path.exists(checklist_file_path):
            logging.warning(f"クラブ '{club_name}' のチェックリストファイルが存在しません。スキップします。")
            continue
        try:
            checklist_df = pd.read_csv(checklist_file_path)
            logging.info(f"チェックリストファイル '{checklist_file_name}' を読み込みました。")
        except Exception as e:
            logging.error(f"チェックリストファイル '{checklist_file_name}' の読み込み中にエラーが発生しました: {e}")
            continue
        # チェックリストの人間によるチェック状況の確認を実行する必要があるかを確認
        # 申請時間が一致し、かつ人間によるチェック状況の確認更新時間が空でない場合のみスキップ
        mask = (
            (checklist_df['申請時間'] == application_date) &
            (checklist_df['書類チェック更新時間'].notna()) &
            (checklist_df['書類チェック更新時間'] != '')
        )
        if mask.any():
            logging.info(f"クラブ '{club_name}' の申請日時'{application_date}'の申請は人間によるチェック状況の確認が済んでいます。スキップします。")
            continue
        else:
            logging.info(f"クラブ '{club_name}' の申請日時'{application_date}'の申請は人間によるチェック状況の確認を実行します。")
            # エラーが無いかを記載していくための辞書を作成（まずは空）
            error_dict = {}
            # 日本の現在時刻を取得
            jst_now = get_jst_now()
            # 今日の日付を取得
            today_date = jst_now.date()
        
        # 書類の種類ごとにチェックリストが保存されているフォルダを確認
        document1_checklist_for_human_folder_name = 'document_1_checklist_for_human'
        document1_checklist_for_human_folder_path = os.path.join(club_folder, document1_checklist_for_human_folder_name)
        document2_1_checklist_for_human_folder_name = 'document_2_1_checklist_for_human'
        document2_1_checklist_for_human_folder_path = os.path.join(club_folder, document2_1_checklist_for_human_folder_name)
        document2_2_checklist_for_human_folder_name = 'document_2_2_checklist_for_human'
        document2_2_checklist_for_human_folder_path = os.path.join(club_folder, document2_2_checklist_for_human_folder_name)
        document3_checklist_for_human_folder_name = 'document_3_checklist_for_human'
        document3_checklist_for_human_folder_path = os.path.join(club_folder, document3_checklist_for_human_folder_name)
        document4_checklist_for_human_folder_name = 'document_4_checklist_for_human'
        document4_checklist_for_human_folder_path = os.path.join(club_folder, document4_checklist_for_human_folder_name)
        document5_plan_checklist_for_human_folder_name = 'document_5_plan_checklist_for_human'
        document5_plan_checklist_for_human_folder_path = os.path.join(club_folder, document5_plan_checklist_for_human_folder_name)
        document5_budget_checklist_for_human_folder_name = 'document_5_budget_checklist_for_human'
        document5_budget_checklist_for_human_folder_path = os.path.join(club_folder, document5_budget_checklist_for_human_folder_name)
        document6_report_checklist_for_human_folder_name = 'document_6_report_checklist_for_human'
        document6_report_checklist_for_human_folder_path = os.path.join(club_folder, document6_report_checklist_for_human_folder_name)
        document6_financial_statements_checklist_for_human_folder_name = 'document_6_financial_statements_checklist_for_human'
        document6_financial_statements_checklist_for_human_folder_path = os.path.join(club_folder, document6_financial_statements_checklist_for_human_folder_name)
        document7_checklist_for_human_folder_name = 'document_7_checklist_for_human'
        document7_checklist_for_human_folder_path = os.path.join(club_folder, document7_checklist_for_human_folder_name)
        document8_checklist_for_human_folder_name = 'document_8_checklist_for_human'
        document8_checklist_for_human_folder_path = os.path.join(club_folder, document8_checklist_for_human_folder_name)
        document9_checklist_for_human_folder_name = 'document_9_checklist_for_human'
        document9_checklist_for_human_folder_path = os.path.join(club_folder, document9_checklist_for_human_folder_name)
        
        # 各書類のチェックリストを確認
        # 書類1のチェックリストを確認
        if os.path.exists(document1_checklist_for_human_folder_path):
            document1_checklist_for_human_file_name = f'{club_name}_document1_checklist_申請{application_date}.xlsx'
            document1_checklist_for_human_file_path = os.path.join(document1_checklist_for_human_folder_path, document1_checklist_for_human_file_name)
            if os.path.exists(document1_checklist_for_human_file_path):
                try:
                    document1_checklist_df = pd.read_excel(document1_checklist_for_human_file_path)
                    if 'チェック者名_{}' in document1_checklist_df.columns:
                        checked = document1_checklist_df['チェック者名_{}'].notna().any()
                        if checked:
                            logging.info(f"クラブ '{club_name}' の書類1のチェックリストは人間によるチェックが完了しています。")
                        else:
                            logging.info(f"クラブ '{club_name}' の書類1のチェックリストは人間によるチェックが未完了です。")
                            error_dict['書類1'] = '人間によるチェックが未完了'
                    else:
                        logging.warning(f"クラブ '{club_name}' の書類1のチェックリストに 'チェック者名_{{}}' の列が存在しません。")
                        error_dict['書類1'] = 'チェック者名の列が存在しない'
                except Exception as e:
                    logging.error(f"クラブ '{club_name}' の書類1のチェックリストの読み込み中にエラーが発生しました: {e}")
            else:
                logging.warning(f"クラブ '{club_name}' の書類1のチェックリストファイルが存在しません。")
                error_dict['書類1'] = 'チェックリストファイルが存在しない'
        else:
            logging.warning(f"クラブ '{club_name}' の書類1のチェックリストフォルダが存在しません。")
        # 書類2_1のチェックリストを確認
        if os.path.exists(document2_1_checklist_for_human_folder_path):
            document2_1_checklist_for_human_file_name = f'{club_name}_document2_1_checklist_申請{application_date}.xlsx'
            document2_1_checklist_for_human_file_path = os.path.join(document2_1_checklist_for_human_folder_path, document2_1_checklist_for_human_file_name)
            if os.path.exists(document2_1_checklist_for_human_file_path):
                try:
                    document2_1_checklist_df = pd.read_excel(document2_1_checklist_for_human_file_path, sheet_name='チェックリスト')
                    # チェックリストの人間によるチェック状況の確認を実行
                    if 'チェック者名_{}' in document2_1_checklist_df.columns:
                        # チェック者名_{}の列にデータがあるかを確認
                        checked = document2_1_checklist_df['チェック者名_{}'].notna().any()
                        if checked:
                            logging.info(f"クラブ '{club_name}' の書類2_1のチェックリストは人間によるチェックが完了しています。")
                        else:
                            logging.info(f"クラブ '{club_name}' の書類2_1のチェックリストは人間によるチェックが未完了です。")
                            error_dict['書類2_1'] = '人間によるチェックが未完了'
                    else:
                        logging.warning(f"クラブ '{club_name}' の書類2_1のチェックリストに 'チェック者名_{{}}' の列が存在しません。")
                        error_dict['書類2_1'] = 'チェック者名の列が存在しない'
                except Exception as e:
                    logging.error(f"エラー: クラブ '{club_name}' の書類2_1のチェックリストの読み込み中にエラーが発生しました: {e}")
            else:
                logging.warning(f"クラブ '{club_name}' の書類2_1のチェックリストファイルが存在しません。")
                error_dict['書類2_1'] = 'チェックリストファイルが存在しない'
        else:
            logging.warning(f"クラブ '{club_name}' の書類2_1のチェックリストフォルダが存在しません。")
            error_dict['書類2_1'] = 'チェックリストフォルダが存在しない'
        # 書類2_2のチェックリストを確認
        if os.path.exists(document2_2_checklist_for_human_folder_path):
            document2_2_checklist_for_human_file_name = f'{club_name}_document2_2_checklist_申請{application_date}.xlsx'
            document2_2_checklist_for_human_file_path = os.path.join(document2_2_checklist_for_human_folder_path, document2_2_checklist_for_human_file_name)
            if os.path.exists(document2_2_checklist_for_human_file_path):
                try:
                    document2_2_checklist_df = pd.read_excel(document2_2_checklist_for_human_file_path, sheet_name='チェックリスト')
                    # チェックリストの人間によるチェック状況の確認を実行
                    if 'チェック者名_{}' in document2_2_checklist_df.columns:
                        # チェック者名_{}の列にデータがあるかを確認
                        checked = document2_2_checklist_df['チェック者名_{}'].notna().any()
                        if checked:
                            logging.info(f"クラブ '{club_name}' の書類2_2のチェックリストは人間によるチェックが完了しています。")
                        else:
                            logging.info(f"クラブ '{club_name}' の書類2_2のチェックリストは人間によるチェックが未完了です。")
                            error_dict['書類2_2'] = '人間によるチェックが未完了'
                    else:
                        logging.warning(f"クラブ '{club_name}' の書類2_2のチェックリストに 'チェック者名_{{}}' の列が存在しません。")
                        error_dict['書類2_2'] = 'チェック者名の列が存在しない'
                except Exception as e:
                    logging.error(f"クラブ '{club_name}' の書類2_2のチェックリストの読み込み中にエラーが発生しました: {e}")
            else:
                logging.warning(f"クラブ '{club_name}' の書類2_2のチェックリストファイルが存在しません。")
                error_dict['書類2_2'] = 'チェックリストファイルが存在しない'
        else:
            logging.warning(f"クラブ '{club_name}' の書類2_2のチェックリストフォルダが存在しません。")
            error_dict['書類2_2'] = 'チェックリストフォルダが存在しない'
        # 書類3のチェックリストを確認
        if os.path.exists(document3_checklist_for_human_folder_path):
            document3_checklist_for_human_file_name = f'{club_name}_document3_checklist_申請{application_date}.xlsx'
            document3_checklist_for_human_file_path = os.path.join(document3_checklist_for_human_folder_path, document3_checklist_for_human_file_name)
            if os.path.exists(document3_checklist_for_human_file_path):
                try:
                    document3_checklist_df = pd.read_excel(document3_checklist_for_human_file_path)
                    # チェックリストの人間によるチェック状況の確認を実行
                    if 'チェック者名_{}' in document3_checklist_df.columns:
                        # チェック者名_{}の列にデータがあるかを確認
                        checked = document3_checklist_df['チェック者名_{}'].notna().any()
                        if checked:
                            logging.info(f"クラブ '{club_name}' の書類3のチェックリストは人間によるチェックが完了しています。")
                        else:
                            logging.info(f"クラブ '{club_name}' の書類3のチェックリストは人間によるチェックが未完了です。")
                            error_dict['書類3'] = '人間によるチェックが未完了'
                    else:
                        logging.warning(f"クラブ '{club_name}' の書類3のチェックリストに 'チェック者名_{{}}' の列が存在しません。")
                        error_dict['書類3'] = 'チェック者名の列が存在しない'
                except Exception as e:
                    logging.error(f"クラブ '{club_name}' の書類3のチェックリストの読み込み中にエラーが発生しました: {e}")
            else:
                logging.warning(f"クラブ '{club_name}' の書類3のチェックリストファイルが存在しません。")
                error_dict['書類3'] = 'チェックリストファイルが存在しない'
        else:
            logging.warning(f"クラブ '{club_name}' の書類3のチェックリストフォルダが存在しません。")
            error_dict['書類3'] = 'チェックリストフォルダが存在しない'
        # 書類4のチェックリストを確認
        if os.path.exists(document4_checklist_for_human_folder_path):
            document4_checklist_for_human_file_name = f'{club_name}_document4_checklist_申請{application_date}.xlsx'
            document4_checklist_for_human_file_path = os.path.join(document4_checklist_for_human_folder_path, document4_checklist_for_human_file_name)
            if os.path.exists(document4_checklist_for_human_file_path):
                try:
                    document4_checklist_df = pd.read_excel(document4_checklist_for_human_file_path, sheet_name='チェックリスト')
                    # チェックリストの人間によるチェック状況の確認を実行
                    if 'チェック者名_{}' in document4_checklist_df.columns:
                        # チェック者名_{}の列にデータがあるかを確認
                        checked = document4_checklist_df['チェック者名_{}'].notna().any()
                        if checked:
                            logging.info(f"クラブ '{club_name}' の書類4のチェックリストは人間によるチェックが完了しています。")
                        else:
                            logging.info(f"クラブ '{club_name}' の書類4のチェックリストは人間によるチェックが未完了です。")
                            error_dict['書類4'] = '人間によるチェックが未完了'
                    else:
                        logging.warning(f"クラブ '{club_name}' の書類4のチェックリストに 'チェック者名_{{}}' の列が存在しません。")
                        error_dict['書類4'] = 'チェック者名の列が存在しない'
                except Exception as e:
                    logging.error(f"クラブ '{club_name}' の書類4のチェックリストの読み込み中にエラーが発生しました: {e}")
            else:
                logging.warning(f"クラブ '{club_name}' の書類4のチェックリストファイルが存在しません。")
                error_dict['書類4'] = 'チェックリストファイルが存在しない'
        else:
            logging.warning(f"クラブ '{club_name}' の書類4のチェックリストフォルダが存在しません。")
            error_dict['書類4'] = 'チェックリストフォルダが存在しない'
        # 書類5_事業計画のチェックリストを確認
        if os.path.exists(document5_plan_checklist_for_human_folder_path):
            document5_plan_checklist_for_human_file_name = f'{club_name}_document5_plan_checklist_申請{application_date}.xlsx'
            document5_plan_checklist_for_human_file_path = os.path.join(document5_plan_checklist_for_human_folder_path, document5_plan_checklist_for_human_file_name)
            if os.path.exists(document5_plan_checklist_for_human_file_path):
                try:
                    document5_plan_checklist_df = pd.read_excel(document5_plan_checklist_for_human_file_path, sheet_name='チェックリスト')
                    # チェックリストの人間によるチェック状況の確認を実行
                    if 'チェック者名_{}' in document5_plan_checklist_df.columns:
                        # チェック者名_{}の列にデータがあるかを確認
                        checked = document5_plan_checklist_df['チェック者名_{}'].notna().any()
                        if checked:
                            logging.info(f"クラブ '{club_name}' の書類5_事業計画のチェックリストは人間によるチェックが完了しています。")
                        else:
                            logging.info(f"クラブ '{club_name}' の書類5_事業計画のチェックリストは人間によるチェックが未完了です。")
                            error_dict['書類5_事業計画'] = '人間によるチェックが未完了'
                    else:
                        logging.warning(f"クラブ '{club_name}' の書類5_事業計画のチェックリストに 'チェック者名_{{}}' の列が存在しません。")
                        error_dict['書類5_事業計画'] = 'チェック者名の列が存在しない'
                except Exception as e:
                    logging.error(f"クラブ '{club_name}' の書類5_事業計画のチェックリストの読み込み中にエラーが発生しました: {e}")
            else:
                logging.warning(f"クラブ '{club_name}' の書類5_事業計画のチェックリストファイルが存在しません。")
                error_dict['書類5_事業計画'] = 'チェックリストファイルが存在しない'
        else:
            logging.warning(f"クラブ '{club_name}' の書類5_事業計画のチェックリストフォルダが存在しません。")
            error_dict['書類5_事業計画'] = 'チェックリストフォルダが存在しない'
        # 書類5_予算のチェックリストを確認
        if os.path.exists(document5_budget_checklist_for_human_folder_path):
            document5_budget_checklist_for_human_file_name = f'{club_name}_document5_budget_checklist_申請{application_date}.xlsx'
            document5_budget_checklist_for_human_file_path = os.path.join(document5_budget_checklist_for_human_folder_path, document5_budget_checklist_for_human_file_name)
            if os.path.exists(document5_budget_checklist_for_human_file_path):
                try:
                    document5_budget_checklist_df = pd.read_excel(document5_budget_checklist_for_human_file_path)
                    # チェックリストの人間によるチェック状況の確認を実行
                    if 'チェック者名_{}' in document5_budget_checklist_df.columns:
                        # チェック者名_{}の列にデータがあるかを確認
                        checked = document5_budget_checklist_df['チェック者名_{}'].notna().any()
                        if checked:
                            logging.info(f"クラブ '{club_name}' の書類5_予算のチェックリストは人間によるチェックが完了しています。")
                        else:
                            logging.info(f"クラブ '{club_name}' の書類5_予算のチェックリストは人間によるチェックが未完了です。")
                            error_dict['書類5_予算'] = '人間によるチェックが未完了'
                    else:
                        logging.warning(f"クラブ '{club_name}' の書類5_予算のチェックリストに 'チェック者名_{{}}' の列が存在しません。")
                        error_dict['書類5_予算'] = 'チェック者名の列が存在しない'
                except Exception as e:
                    logging.error(f"クラブ '{club_name}' の書類5_予算のチェックリストの読み込み中にエラーが発生しました: {e}")
            else:
                logging.warning(f"クラブ '{club_name}' の書類5_予算のチェックリストファイルが存在しません。")
                error_dict['書類5_予算'] = 'チェックリストファイルが存在しない'
        else:
            logging.warning(f"クラブ '{club_name}' の書類5_予算のチェックリストフォルダが存在しません。")
            error_dict['書類5_予算'] = 'チェックリストフォルダが存在しない'
        # 書類6_事業報告のチェックリストを確認
        if os.path.exists(document6_report_checklist_for_human_folder_path):
            document6_report_checklist_for_human_file_name = f'{club_name}_document6_report_checklist_申請{application_date}.xlsx'
            document6_report_checklist_for_human_file_path = os.path.join(document6_report_checklist_for_human_folder_path, document6_report_checklist_for_human_file_name)
            if os.path.exists(document6_report_checklist_for_human_file_path):
                try:
                    document6_report_checklist_df = pd.read_excel(document6_report_checklist_for_human_file_path, sheet_name='チェックリスト')
                    # チェックリストの人間によるチェック状況の確認を実行
                    if 'チェック者名_{}' in document6_report_checklist_df.columns:
                        # チェック者名_{}の列にデータがあるかを確認
                        checked = document6_report_checklist_df['チェック者名_{}'].notna().any()
                        if checked:
                            logging.info(f"クラブ '{club_name}' の書類6_事業報告のチェックリストは人間によるチェックが完了しています。")
                        else:
                            logging.info(f"クラブ '{club_name}' の書類6_事業報告のチェックリストは人間によるチェックが未完了です。")
                            error_dict['書類6_事業報告'] = '人間によるチェックが未完了'
                    else:
                        logging.warning(f"クラブ '{club_name}' の書類6_事業報告のチェックリストに 'チェック者名_{{}}' の列が存在しません。")
                        error_dict['書類6_事業報告'] = 'チェック者名の列が存在しない'
                except Exception as e:
                    logging.error(f"クラブ '{club_name}' の書類6_事業報告のチェックリストの読み込み中にエラーが発生しました: {e}")
            else:
                logging.warning(f"クラブ '{club_name}' の書類6_事業報告のチェックリストファイルが存在しません。")
                error_dict['書類6_事業報告'] = 'チェックリストファイルが存在しない'
        else:
            logging.warning(f"クラブ '{club_name}' の書類6_事業報告のチェックリストフォルダが存在しません。")
            error_dict['書類6_事業報告'] = 'チェックリストフォルダが存在しない'
        # 書類6_決算のチェックリストを確認
        if os.path.exists(document6_financial_statements_checklist_for_human_folder_path):
            document6_financial_statements_checklist_for_human_file_name = f'{club_name}_document6_financial_statements_checklist_申請{application_date}.xlsx'
            document6_financial_statements_checklist_for_human_file_path = os.path.join(document6_financial_statements_checklist_for_human_folder_path, document6_financial_statements_checklist_for_human_file_name)
            if os.path.exists(document6_financial_statements_checklist_for_human_file_path):
                try:
                    document6_financial_statements_checklist_df = pd.read_excel(document6_financial_statements_checklist_for_human_file_path)
                    # チェックリストの人間によるチェック状況の確認を実行
                    if 'チェック者名_{}' in document6_financial_statements_checklist_df.columns:
                        # チェック者名_{}の列にデータがあるかを確認
                        checked = document6_financial_statements_checklist_df['チェック者名_{}'].notna().any()
                        if checked:
                            logging.info(f"クラブ '{club_name}' の書類6_決算のチェックリストは人間によるチェックが完了しています。")
                        else:
                            logging.info(f"クラブ '{club_name}' の書類6_決算のチェックリストは人間によるチェックが未完了です。")
                            error_dict['書類6_決算'] = '人間によるチェックが未完了'
                    else:
                        logging.warning(f"クラブ '{club_name}' の書類6_決算のチェックリストに 'チェック者名_{{}}' の列が存在しません。")
                        error_dict['書類6_決算'] = 'チェック者名の列が存在しない'
                except Exception as e:
                    logging.error(f"クラブ '{club_name}' の書類6_決算のチェックリストの読み込み中にエラーが発生しました: {e}")
            else:
                logging.warning(f"クラブ '{club_name}' の書類6_決算のチェックリストファイルが存在しません。")
                error_dict['書類6_決算'] = 'チェックリストファイルが存在しない'
        else:
            logging.warning(f"クラブ '{club_name}' の書類6_決算のチェックリストフォルダが存在しません。")
            error_dict['書類6_決算'] = 'チェックリストフォルダが存在しない'
        # 書類7のチェックリストを確認
        if os.path.exists(document7_checklist_for_human_folder_path):
            document7_checklist_for_human_file_name = f'{club_name}_document7_checklist_申請{application_date}.xlsx'
            document7_checklist_for_human_file_path = os.path.join(document7_checklist_for_human_folder_path, document7_checklist_for_human_file_name)
            if os.path.exists(document7_checklist_for_human_file_path):
                try:
                    document7_checklist_df = pd.read_excel(document7_checklist_for_human_file_path)
                    # チェックリストの人間によるチェック状況の確認を実行
                    if 'チェック者名_{}' in document7_checklist_df.columns:
                        # チェック者名_{}の列にデータがあるかを確認
                        checked = document7_checklist_df['チェック者名_{}'].notna().any()
                        if checked:
                            logging.info(f"クラブ '{club_name}' の書類7のチェックリストは人間によるチェックが完了しています。")
                        else:
                            logging.info(f"クラブ '{club_name}' の書類7のチェックリストは人間によるチェックが未完了です。")
                            error_dict['書類7'] = '人間によるチェックが未完了'
                    else:
                        logging.warning(f"クラブ '{club_name}' の書類7のチェックリストに 'チェック者名_{{}}' の列が存在しません。")
                        error_dict['書類7'] = 'チェック者名の列が存在しない'
                except Exception as e:
                    logging.error(f"クラブ '{club_name}' の書類7のチェックリストの読み込み中にエラーが発生しました: {e}")
            else:
                logging.warning(f"クラブ '{club_name}' の書類7のチェックリストファイルが存在しません。")
                error_dict['書類7'] = 'チェックリストファイルが存在しない'
        else:
            logging.warning(f"クラブ '{club_name}' の書類7のチェックリストフォルダが存在しません。")
            error_dict['書類7'] = 'チェックリストフォルダが存在しない'
        # 書類8のチェックリストを確認
        if os.path.exists(document8_checklist_for_human_folder_path):
            document8_checklist_for_human_file_name = f'{club_name}_document8_checklist_申請{application_date}.xlsx'
            document8_checklist_for_human_file_path = os.path.join(document8_checklist_for_human_folder_path, document8_checklist_for_human_file_name)
            if os.path.exists(document8_checklist_for_human_file_path):
                try:
                    document8_checklist_df = pd.read_excel(document8_checklist_for_human_file_path)
                    # チェックリストの人間によるチェック状況の確認を実行
                    if 'チェック者名_{}' in document8_checklist_df.columns:
                        # チェック者名_{}の列にデータがあるかを確認
                        checked = document8_checklist_df['チェック者名_{}'].notna().any()
                        if checked:
                            logging.info(f"クラブ '{club_name}' の書類8のチェックリストは人間によるチェックが完了しています。")
                        else:
                            logging.info(f"クラブ '{club_name}' の書類8のチェックリストは人間によるチェックが未完了です。")
                            error_dict['書類8'] = '人間によるチェックが未完了'
                    else:
                        logging.warning(f"クラブ '{club_name}' の書類8のチェックリストに 'チェック者名_{{}}' の列が存在しません。")
                        error_dict['書類8'] = 'チェック者名の列が存在しない'
                except Exception as e:
                    logging.error(f"クラブ '{club_name}' の書類8のチェックリストの読み込み中にエラーが発生しました: {e}")
            else:
                logging.warning(f"クラブ '{club_name}' の書類8のチェックリストファイルが存在しません。")
                error_dict['書類8'] = 'チェックリストファイルが存在しない'
        else:
            logging.warning(f"クラブ '{club_name}' の書類8のチェックリストフォルダが存在しません。")
            error_dict['書類8'] = 'チェックリストフォルダが存在しない'
        # 書類9のチェックリストを確認
        if os.path.exists(document9_checklist_for_human_folder_path):
            document9_checklist_for_human_file_name = f'{club_name}_document9_checklist_申請{application_date}.xlsx'
            document9_checklist_for_human_file_path = os.path.join(document9_checklist_for_human_folder_path, document9_checklist_for_human_file_name)
            if os.path.exists(document9_checklist_for_human_file_path):
                try:
                    document9_checklist_df = pd.read_excel(document9_checklist_for_human_file_path)
                    # チェックリストの人間によるチェック状況の確認を実行
                    if 'チェック者名_{}' in document9_checklist_df.columns:
                        # チェック者名_{}の列にデータがあるかを確認
                        checked = document9_checklist_df['チェック者名_{}'].notna().any()
                        if checked:
                            logging.info(f"クラブ '{club_name}' の書類9のチェックリストは人間によるチェックが完了しています。")
                        else:
                            logging.info(f"クラブ '{club_name}' の書類9のチェックリストは人間によるチェックが未完了です。")
                            error_dict['書類9'] = '人間によるチェックが未完了'
                    else:
                        logging.warning(f"クラブ '{club_name}' の書類9のチェックリストに 'チェック者名_{{}}' の列が存在しません。")
                        error_dict['書類9'] = 'チェック者名の列が存在しない'
                except Exception as e:
                    logging.error(f"クラブ '{club_name}' の書類9のチェックリストの読み込み中にエラーが発生しました: {e}")
            else:
                logging.warning(f"クラブ '{club_name}' の書類9のチェックリストファイルが存在しません。")
                error_dict['書類9'] = 'チェックリストファイルが存在しない'
        else:
            logging.warning(f"クラブ '{club_name}' の書類9のチェックリストフォルダが存在しません。")
            error_dict['書類9'] = 'チェックリストフォルダが存在しない'
        
        # error_dictが空の時は、問題が無いことを示すメッセージを追加
        if not error_dict:
            logging.info(f"クラブ '{club_name}' の申請日時'{application_date}'の書類は全て人間によるチェックが完了しています。")
            error_dict['全ての書類'] = '人間によるチェックが完了'

        # チェックリストの人間によるチェック状況の確認を更新
        checklist_df.loc[
            (checklist_df['クラブ名'] == club_name) & (checklist_df['申請時間'] == application_date),
            '書類チェック更新時間'
        ] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        checklist_df.loc[
            (checklist_df['クラブ名'] == club_name) & (checklist_df['申請時間'] == application_date),
            '人間によるチェック状況'
        ] = ', '.join(error_dict.values())

        # チェックリストファイルを保存
        checklist_file_path = os.path.join(club_folder, f'{club_name}_checklist_申請{application_date}.xlsx')
        checklist_df.to_excel(checklist_file_path, index=False)
        logging.info(f"クラブ '{club_name}' の申請日時'{application_date}'のチェックリストを更新しました。")
    checklist_status_path = os.path.join(folder_of_checklist_create_status, 'クラブごとのチェックリスト作成状況.csv')
    checklist_status_df.to_csv(checklist_status_path, index=False)
    logging.info('チェックリスト作成状況を更新しました。')
    return checklist_status_df