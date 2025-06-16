import os
import pandas as pd

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
from datetime import datetime, timezone, timedelta

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

def make_documents_checklist_for_human(application_df, list_df):
    """
    人間がチェックする用のリストを作成する関数
    :param apried_club_list_df: 申請済みクラブのDataFrame
    :param checklist_create_df: チェックリスト作成状況のDataFrame
    """
    print("人間が確認する用のチェックリストを作成しています...")
    # チェックリストの大まかなフォルダを指定
    folder_path = os.path.join('R7_登録申請処理', '申請入力内容')

    # application_dfの行ごとに処理を行う
    for index, row in application_df.iterrows():
        club_name = str(row['クラブ名']).strip()
        apried_date_str = str(row['申請日時']).strip()

        # checklist_create_dfから該当クラブ・申請日時の「チェックリスト作成日時」を取得
        checklist_creation_date_str = ''
        match = list_df[
            (list_df['クラブ名'] == club_name) &
            (list_df['R8年度登録申請_タイムスタンプyyyymmddHHMMSS'] == apried_date_str)
        ]
        if 'チェックリスト作成日時' in match.columns and not match.empty:
            checklist_creation_date_str = match.iloc[0]['チェックリスト作成日時']
        # 処理開始のメッセージを表示
        print(f"クラブ名: {club_name} の人間が確認する用のチェックリスト作成を開始します")
        # 保存されているチェックリストを読み込み、チェックを実行
        club_folder_path = os.path.join(folder_path, club_name)
        if not os.path.exists(club_folder_path):
            print(f"警告: クラブ '{club_name}' のフォルダが存在しません。スキップします。")
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
        club_df = list_df[
            (list_df['クラブ名'] == club_name) &
            (list_df['R8年度登録申請_タイムスタンプyyyymmddHHMMSS'] == apried_date_str)
        ]
        # 書類1
        document1_checklist = make_document1_checklist_for_human(club_df, application_df)
        os.makedirs(document1_checklist_for_human_folder_path, exist_ok=True)
        # 書類1のチェックリストをExcelファイルとして保存
        document1_checklist_for_human_file_name = f'{club_name}_document1_checklist_申請{apried_date_str}.xlsx'
        pd.DataFrame(document1_checklist).to_excel(
            os.path.join(document1_checklist_for_human_folder_path, document1_checklist_for_human_file_name),
            index=False
        )
        # 書類2_1
        document2_1_checklist,document2_1_number_of_menbers,document2_1_number_of_annual_fee_members = make_document2_1_checklist_for_human(club_df, application_df)
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
        document2_2_checklist, document2_2_discipline_and_coaches = make_document2_2_checklist_for_human(club_df, application_df)
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
        document3_checklist = make_document3_checklist_for_human(club_df, application_df)
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
        document4_checklist, document4_lists_checklist = make_document4_checklist_for_human(club_df, application_df)
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
        document5_plan_checklist, document5_plan_checklist_discipline = make_document5_plan_checklist_for_human(club_df, application_df)
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
        document5_budget_checklist = make_document5_budget_checklist_for_human(club_df, application_df)
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
        document6_report_checklist, document6_report_checklist_discipline = make_document6_report_checklist_for_human(club_df, application_df)
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
        document6_financial_statements_checklist = make_document6_financial_statements_checklist_for_human(club_df, application_df)
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
        document7_checklist = make_document7_checklist_for_human(club_df, application_df)
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
        document8_checklist = make_document8_checklist_for_human(club_df, application_df)
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
        document9_checklist = make_document9_checklist_for_human(club_df, application_df)
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
        print(f"クラブ名: {club_name} の人間が確認する用のチェックリスト作成が完了しました")
    print("人間が確認する用のチェックリストの作成が完了しました。")

def write_checklist_by_human_check(apried_club_list_df, checklist_create_df, folder_of_checklist_create_status):
    pass  # TODO: 実装を追加