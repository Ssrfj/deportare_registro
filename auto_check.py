import os
import pandas as pd
from datetime import datetime, timezone, timedelta
from check_functions import (
    check_must_columns, check_submitting_now, check_club_location, check_phone_number,
    check_fax_number, check_application_type, check_standard_compliance, check_number_of_members,
    check_number_of_disciplines, check_coaches, check_managers, check_rule_revision,
    check_rule_submission, check_officer_list_submission, check_business_plan_submission,
    check_budget_submission, check_business_report_submission, check_financial_statement_submission,
    check_checklist_submission, check_self_explanation_submission
)
from dataframe_utils import clean_column_names
from column_names import CHECKLIST_CREATION_DATETIME
from column_names import CHECKLIST_CREATION_DATETIME
from dataframe_utils import clean_column_names
from column_names import CHECKLIST_CREATION_DATETIME


def perform_automatic_checks(checklist_status_df, applied_club_df):
    """
    指定されたクラブに対して自動チェックを行います。

    Args:
        applied_club_df (pd.DataFrame): 申請済みクラブのDataFrame
        checklist_status_df (pd.DataFrame): チェックリスト作成状況のDataFrame
    """
    # チェックリストのフォルダを指定
    folder_path = os.path.join('R7_登録申請処理', '申請入力内容')

    # applied_club_dfの行ごとに処理を行う
    for index, row in applied_club_df.iterrows():
        club_name = str(row['クラブ名']).strip()
        apried_date_str = str(row.get('申請日時', row.get('R8年度登録申請_タイムスタンプyyyymmddHHMMSS', ''))).strip()

        checklist_creation_date_str = row[CHECKLIST_CREATION_DATETIME]
        # 処理開始のメッセージを表示
        print(f"クラブ名: {club_name} の自動チェックを開始します")
        # 保存されているチェックリストを読み込み、チェックを実行
        club_folder_path = os.path.join(folder_path, club_name)
        if not os.path.exists(club_folder_path):
            print(f"警告: クラブ '{club_name}' のフォルダが存在しません。スキップします。")
            continue
        checklist_file_name = f"{club_name}_申請{apried_date_str}_作成{checklist_creation_date_str}.csv"
        checklist_file_path = os.path.join(club_folder_path, checklist_file_name)
        if not os.path.exists(checklist_file_path):
            print(f"警告: クラブ '{club_name}' のチェックリストファイルが存在しません。スキップします。")
            continue
        try:
            checklist_df = pd.read_csv(checklist_file_path)
            checklist_df = clean_column_names(checklist_df)
            print(f"チェックリストファイル '{checklist_file_name}' を読み込みました。")
        except Exception as e:
            print(f"エラー: チェックリストファイル '{checklist_file_name}' の読み込み中にエラーが発生しました: {e}")
            continue
        # チェックリストの自動チェックを実行する必要があるかを確認
        # 申請時間が一致し、かつ自動チェック更新時間が空でない場合のみスキップ
        mask = (checklist_df['申請時間'] == apried_date_str) & (checklist_df['自動チェック更新時間'].notna()) & (checklist_df['自動チェック更新時間'] != '')
        if mask.any():
            print(f"クラブ '{club_name}' の申請日時'{apried_date_str}'の申請は自動チェック済みです。スキップします。")
            continue
        else:
            print(f"クラブ '{club_name}' の申請日時'{apried_date_str}'の申請は自動チェックを実行します。")
            # エラーが無いかを記載していくための辞書を作成（まずは空）
            error_dict = {}
            # 日本の現在時刻を取得
            jst_now = datetime.now(timezone(timedelta(hours=9)))
            # 今日の日付を取得
            today_date = jst_now.date()
        
        checklist_status_df['クラブ名'] = checklist_status_df['クラブ名'].astype(str).str.strip()
        checklist_status_df['R8年度登録申請_タイムスタンプyyyymmddHHMMSS'] = checklist_status_df['R8年度登録申請_タイムスタンプyyyymmddHHMMSS'].astype(str).str.strip()


        # 申請内容から該当行を抽出
        target_row = checklist_status_df[
            (checklist_status_df['クラブ名'] == club_name) &
            (checklist_status_df['R8年度登録申請_タイムスタンプyyyymmddHHMMSS'] == apried_date_str)
        ]
        print(checklist_status_df[['クラブ名', 'R8年度登録申請_タイムスタンプyyyymmddHHMMSS']])
        print(f"検索値: クラブ名={club_name}, 申請日時={apried_date_str}")
        print(repr(club_name), repr(apried_date_str))
        print(checklist_status_df[['クラブ名', 'R8年度登録申請_タイムスタンプyyyymmddHHMMSS']].applymap(repr))
        if target_row.empty:
            print(f"申請内容に該当データがありません: {club_name}, {apried_date_str}")
            continue
        # 各チェック関数に row を渡すように変更
        error_dict.update(check_must_columns(target_row))
        error_dict.update(check_submitting_now(target_row))
        error_dict.update(check_club_location(target_row))
        error_dict.update(check_phone_number(target_row))
        error_dict.update(check_fax_number(target_row))
        # check_application_type 関数には application_data_df を渡す
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
        error_dict.update(check_business_report_submission(target_row,today_date))
        error_dict.update(check_financial_statement_submission(target_row,today_date))
        error_dict.update(check_checklist_submission(target_row))
        error_dict.update(check_self_explanation_submission(target_row))

        # error_dictが空の時は、問題が無いことを示すメッセージを追加
        if not error_dict:
            error_dict['info'] = '自動チェックで問題は見つかりませんでした。'
        else:
            # エラーがある場合は、infoキーを追加してエラーメッセージを記載
            print('自動チェックで問題が見つかりました。')

        # 一旦、チェックリストをprint
        print(f"チェック結果: {error_dict}")

        # 自動でチェックした内容をチェックリストに書き出し(チェックリストの上書き）
        # error_dictが空の場合は空文字列を書き込む
        checklist_df['自動チェック'] = str(error_dict) if error_dict else ''
        checklist_df['自動チェック更新時間'] = datetime.now(timezone(timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S')

        # 追記したカラムをチェック
        print(checklist_df[['自動チェック','自動チェック更新時間']].iloc[0])

        # チェックリストファイルを保存
        try:
            checklist_df.to_csv(checklist_file_path, index=False)
            print(f"チェックリストファイル '{checklist_file_path}' を更新しました。")
        except Exception as e:
            print(f"エラー: チェックリストファイル '{checklist_file_path}' の書き込み中にエラーが発生しました: {e}")
        # チェックが完了したことを表示
        print(f"クラブ名: {club_name} の自動チェックが完了しました\n")
    print("全てのクラブの自動チェックが完了しました。")

if __name__ == "__main__":
    # チェックリスト作成状況ファイルの読み込みまたは新規作成
    folder_of_checklist_create_status = os.path.join('R7_登録申請処理', '申請入力内容')
    file_of_checklist_create_status = os.path.join(folder_of_checklist_create_status, 'クラブごとのチェックリスト作成状況.csv')
    if os.path.exists(file_of_checklist_create_status):
        checklist_create_df = pd.read_csv(file_of_checklist_create_status)
        print('クラブごとのチェックリスト作成状況.csvはすでに存在しています')
        checklist_create_df = clean_column_names(checklist_create_df)
    else:
        checklist_create_df = pd.DataFrame(columns=['クラブ名','申請日時', 'チェックリスト作成日時'])
        checklist_create_df = clean_column_names(checklist_create_df)
        checklist_create_df.to_csv(file_of_checklist_create_status, index=False)
        print('クラブごとのチェックリスト作成状況.csvが作成されました')
    for idx, row in checklist_create_df.iterrows():
        checklist_creation_date_str = row[CHECKLIST_CREATION_DATETIME]

    # 自動チェックを実行
    perform_automatic_checks(checklist_create_df)