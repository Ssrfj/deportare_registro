import os
import pandas as pd
import logging
from datetime import datetime, timezone, timedelta
from check_functions import (
    check_must_columns, check_submitting_now, check_club_location, check_phone_number,
    check_fax_number, check_application_type, check_standard_compliance, check_number_of_members,
    check_number_of_disciplines, check_coaches, check_managers, check_rule_revision,
    check_rule_submission, check_officer_list_submission, check_business_plan_submission,
    check_budget_submission, check_business_report_submission, check_financial_statement_submission,
    check_checklist_submission, check_self_explanation_submission
)
from get_latest_checklist_file import get_latest_checklist_file

logging.basicConfig(
    level=logging.DEBUG,
    encoding='utf-8',
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def perform_automatic_checks(checklist_status_df, applied_club_df):
    """
    指定されたクラブに対して自動チェックを行います。

    Args:
        applied_club_df (pd.DataFrame): 申請済みクラブのDataFrame
        checklist_status_df (pd.DataFrame): チェックリスト作成状況のDataFrame
    """
    # チェックリストのフォルダを指定
    folder_path = os.path.join('R7_登録申請処理', '申請入力内容')

    # checklist_status_dfに 'クラブ名' と '申請日時' カラムが存在するか確認
    # checklist_status_dfがDataFrameであることを確認
    if not isinstance(checklist_status_df, pd.DataFrame):
        logging.error("checklist_status_dfはDataFrameではありません。")
        return
    # checklist_status_dfに 'クラブ名'カラムが存在するか確認
    if 'クラブ名' not in checklist_status_df.columns:
        logging.error("'クラブ名' カラムが checklist_status_df に存在しません。")
        return
    # checklist_status_dfに '申請日時'カラムが存在するか確認
    if '申請日時' not in checklist_status_df.columns:
        logging.error("'申請日時' カラムが checklist_status_df に存在しません。")
        return

    # applied_club_dfの行ごとに処理を行う
    for index, row in checklist_status_df.iterrows():
        club_name = str(row['クラブ名']).strip()
        apried_date_str = str(row.get('申請日時')).strip()
        if 'チェックリスト作成日時' not in row.index:
            logging.error(f"'チェックリスト作成日時' カラムが存在しません。rowのカラム: {row.index.tolist()}")
            continue
        # 処理開始のメッセージを表示
        logging.info(f"クラブ名: {club_name} の自動チェックを開始します")
        # 保存されているチェックリストを読み込み、チェックを実行
        club_folder_path = os.path.join(folder_path, club_name)
        if not os.path.exists(club_folder_path):
            os.makedirs(club_folder_path, exist_ok=True)
            logging.info(f"クラブ '{club_name}' のフォルダを新規作成しました。")
            continue
        checklist_file_name = f"{club_name}_申請{apried_date_str}.csv"
        each_folder_path = os.path.join(folder_path, club_name)
        checklist_file_path = get_latest_checklist_file(club_name, apried_date_str, each_folder_path)
        if not checklist_file_path or not os.path.exists(checklist_file_path):
            # デバッグ用にeach_folder_pathにあるファイルをリストアップ
            logging.debug(f"each_folder_path: {each_folder_path}")
            logging.debug(f"each_folder_pathにあるファイル: {os.listdir(each_folder_path)}")
            # チェックリストファイルが存在しない場合の処理
            logging.warning(f"クラブ '{club_name}' のチェックリストファイルが存在しません。スキップします。")
            continue

        try:
            checklist_df = pd.read_csv(checklist_file_path)
            # チェックリストのカラム名を確認
            logging.info(f"チェックリストファイル '{checklist_file_name}' を読み込みました。")
        except Exception as e:
            logging.error(f"チェックリストファイル '{checklist_file_name}' の読み込み中にエラーが発生しました: {e}")
            continue
        # チェックリストの自動チェックを実行する必要があるかを確認
        mask = (checklist_df['申請時間'] == apried_date_str) & (checklist_df['自動チェック更新時間'].notna()) & (checklist_df['自動チェック更新時間'] != '')
        if mask.any():
            logging.info(f"クラブ '{club_name}' の申請日時'{apried_date_str}'の申請は自動チェック済みです。スキップします。")
            continue
        else:
            logging.info(f"クラブ '{club_name}' の申請日時'{apried_date_str}'の申請は自動チェックを実行します。")
            error_dict = {}
            jst_now = datetime.now(timezone(timedelta(hours=9)))
            today_date = jst_now.date()
        
        checklist_status_df['クラブ名'] = checklist_status_df['クラブ名'].astype(str).str.strip()
        checklist_status_df['申請日時'] = checklist_status_df['申請日時'].astype(str).str.strip()
        # checklist_status_dfのクラブ名と申請日時をstr型に変換
        # 申請内容から該当行を抽出
        target_row = applied_club_df[
            (applied_club_df['クラブ名'] == club_name) &
            (applied_club_df['申請日時'] == apried_date_str)
        ]
        logging.debug(applied_club_df[['クラブ名', '申請日時']])
        logging.debug(f"検索値: クラブ名={club_name}, 申請日時={apried_date_str}")
        logging.debug(f"{repr(club_name)}, {repr(apried_date_str)}")
        logging.debug(applied_club_df[['クラブ名', '申請日時']].applymap(repr))
        if target_row.empty:
            logging.warning(f"申請内容に該当データがありません: {club_name}, {apried_date_str}")
            continue
        # 各チェック関数に row を渡すように変更
        error_dict.update(check_must_columns(target_row))
        error_dict.update(check_submitting_now(target_row))
        error_dict.update(check_club_location(target_row))
        error_dict.update(check_phone_number(target_row))
        error_dict.update(check_fax_number(target_row))
        error_dict.update(check_application_type(target_row, checklist_status_df, club_name))
        error_dict.update(check_standard_compliance(target_row))
        error_dict.update(check_number_of_members(target_row))
        error_dict.update(check_number_of_disciplines(target_row))
        # error_dict.update(check_coaches(application_row)) # 現段階では不要
        error_dict.update(check_managers(target_row))
        error_dict.update(check_rule_revision(target_row))
        error_dict.update(check_rule_submission(target_row))
        error_dict.update(check_officer_list_submission(target_row))
        error_dict.update(check_business_plan_submission(target_row))
        error_dict.update(check_budget_submission(target_row))
        error_dict.update(check_business_report_submission(target_row, today_date))
        error_dict.update(check_financial_statement_submission(target_row, today_date))
        error_dict.update(check_checklist_submission(target_row))
        error_dict.update(check_self_explanation_submission(target_row))

        if not error_dict:
            error_dict['info'] = '自動チェックで問題は見つかりませんでした。'
        else:
            logging.warning('自動チェックで問題が見つかりました。')

        logging.info(f"チェック結果: {error_dict}")

        checklist_df['自動チェック'] = str(error_dict) if error_dict else ''
        checklist_df['自動チェック更新時間'] = datetime.now(timezone(timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S')

        logging.debug(checklist_df[['自動チェック','自動チェック更新時間']].iloc[0])

        try:
            checklist_df.to_csv(checklist_file_path, index=False)
            logging.info(f"チェックリストファイル '{checklist_file_path}' を更新しました。")
        except Exception as e:
            logging.error(f"チェックリストファイル '{checklist_file_path}' の書き込み中にエラーが発生しました: {e}")
        logging.info(f"クラブ名: {club_name} の自動チェックが完了しました\n")
    logging.info("全てのクラブの自動チェックが完了しました。")

    # checklist_status_df を保存
    folder_of_checklist_create_status = os.path.join('R7_登録申請処理', '申請入力内容')
    file_of_checklist_create_status = os.path.join(folder_of_checklist_create_status, 'クラブごとのチェックリスト作成状況.csv')
    checklist_status_df.to_csv(file_of_checklist_create_status, index=False)
    logging.info('クラブごとのチェックリスト作成状況.csvを自動チェック後に保存しました。')
    return checklist_status_df

if __name__ == "__main__":
    folder_of_checklist_create_status = os.path.join('R7_登録申請処理', '申請入力内容')
    file_of_checklist_create_status = os.path.join(folder_of_checklist_create_status, 'クラブごとのチェックリスト作成状況.csv')
    if os.path.exists(file_of_checklist_create_status):
        checklist_create_df = pd.read_csv(file_of_checklist_create_status)
        logging.info('クラブごとのチェックリスト作成状況.csvはすでに存在しています')
        logging.debug(f"before: {checklist_create_df.columns.tolist()}")
        logging.debug(f"after: {checklist_create_df.columns.tolist()}")
    else:
        checklist_create_df = pd.DataFrame(columns=['クラブ名','申請日時', 'チェックリスト作成日時'])
        logging.debug(f"before: {checklist_create_df.columns.tolist()}")
        logging.debug(f"after: {checklist_create_df.columns.tolist()}")
        checklist_create_df.to_csv(file_of_checklist_create_status, index=False)
        logging.info('クラブごとのチェックリスト作成状況.csvが作成されました')
    for idx, row in checklist_create_df.iterrows():
        checklist_creation_date_str = row['チェックリスト作成日時']

    perform_automatic_checks(checklist_create_df)