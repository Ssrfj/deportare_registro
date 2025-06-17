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
from column_names import (
    CLUB_NAME, APPLICATION_DATETIME, CHECKLIST_CREATION_DATETIME,
    APPLICATION_TIMESTAMP_STR
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
        print(f"エラー: {folder_path} にCSVファイルが存在しません。")
        return
    latest_file = max(files, key=os.path.getctime)
    try:
        club_list_df = pd.read_csv(latest_file)
        club_list_df['R8年度登録申請_タイムスタンプ'] = pd.to_datetime(club_list_df['R8年度登録申請_タイムスタンプ'], errors='coerce')
        club_list_df['R8年度登録申請_タイムスタンプyyyymmddHHMMSS'] = club_list_df['R8年度登録申請_タイムスタンプ'].dt.strftime('%Y%m%d%H%M%S')
        print("申請内容の読み込みが完了しました")
    except Exception as e:
        print(f"申請内容の読み込み中にエラーが発生しました: {e}")
        return

    # 5. チェックリスト作成状況ファイルの読み込みまたは新規作成
    folder_of_checklist_create_status = os.path.join('R7_登録申請処理', '申請入力内容')
    os.makedirs(folder_of_checklist_create_status, exist_ok=True)
    # チェックリスト作成状況のCSVファイルを読み込むか、新規作成
    file_of_checklist_create_status = os.path.join(folder_of_checklist_create_status, 'クラブごとのチェックリスト作成状況.csv')
    if os.path.exists(file_of_checklist_create_status):
        checklist_create_df = pd.read_csv(file_of_checklist_create_status)
        checklist_create_df = clean_column_names(checklist_create_df)
        # 必要なカラムがなければ追加
        for col in [CLUB_NAME, APPLICATION_DATETIME, CHECKLIST_CREATION_DATETIME]:
            if col not in checklist_create_df.columns:
                checklist_create_df[col] = ''
        # ここでカラム名の空白除去とリネーム
        checklist_create_df.columns = checklist_create_df.columns.str.strip()
        checklist_create_df = checklist_create_df.rename(
            columns={
                'チェックリスト作成日時': CHECKLIST_CREATION_DATETIME,
                '申請日時': APPLICATION_DATETIME,
                'クラブ名': CLUB_NAME
            }
        )
        print("checklist_create_df columns after rename:", checklist_create_df.columns.tolist())
        # 必要なカラムがなければ追加（再度チェック）
        for col in [CLUB_NAME, APPLICATION_DATETIME, CHECKLIST_CREATION_DATETIME]:
            if col not in checklist_create_df.columns:
                checklist_create_df[col] = ''
        print('クラブごとのチェックリスト作成状況.csvはすでに存在しています')
    else:
        checklist_create_df = pd.DataFrame(columns=['クラブ名','申請日時', 'チェックリスト作成日時'])
        checklist_create_df.to_csv(file_of_checklist_create_status, index=False)
        print('クラブごとのチェックリスト作成状況.csvが作成されました')

    # club_list_dfの['R8年度登録申請状況']が1のクラブのみを抽出
    # club_list_dfの['R8年度登録申請状況']が1のクラブのみを抽出
    club_list_df.columns = club_list_df.columns.str.strip()
    print("club_list_df columns:", club_list_df.columns.tolist())  # ←追加
    apried_club_list_df = club_list_df[club_list_df['R8年度登録申請状況'] == 1]
    print("apried_club_list_df columns:", apried_club_list_df.columns.tolist())  # ←追加
    if 'R7年度登録クラブ' not in apried_club_list_df.columns:
        print("エラー: apried_club_list_dfに'R7年度登録クラブ'カラムがありません")
    else:
        print("apried_club_list_dfに'R7年度登録クラブ'カラムが存在します")
    if apried_club_list_df.empty:
        print("R8年度登録申請状況が1のクラブが存在しません。")
    else:
        print(f"R8年度登録申請状況が1のクラブ数: {len(apried_club_list_df)}")

    # ここでmake_checklist_for_each_clubを呼び出す
    checklist_output_folder = folder_of_checklist_create_status
    timestamp_for_make_checklist = get_jst_now().strftime('%Y%m%d%H%M%S')
    make_checklist_for_each_club(
        apried_club_list_df,
        checklist_create_df,
        checklist_output_folder,
        timestamp_for_make_checklist
    )
   
    # 6. 各クラブに対して自動チェックを実行
    print('各クラブの自動チェックを実行します...')
    checklist_create_df.columns = checklist_create_df.columns.str.strip()
    checklist_create_df = checklist_create_df.rename(
        columns={
            'チェックリスト作成日時': CHECKLIST_CREATION_DATETIME,
            '申請日時': APPLICATION_DATETIME,
            'クラブ名': CLUB_NAME
        }
    )    
    perform_automatic_checks(checklist_create_df, apried_club_list_df) 
    print('全てのクラブの自動チェックが完了しました。')
    print('処理が終了しました')

    # 7. 人間がチェックする用チェックリストの作成とチェックリストのチェック状況をクラブごとに更新
    print('人間がチェックする用のリストの作成とチェックリストのチェック状況をクラブごとに更新します...')
    checklist_create_df.columns = checklist_create_df.columns.str.strip()
    checklist_create_df = checklist_create_df.rename(
        columns={
            CHECKLIST_CREATION_DATETIME: 'チェックリスト作成日時',
            APPLICATION_DATETIME: '申請日時',
            CLUB_NAME: 'クラブ名'
        }
    )
    print("checklist_create_df columns before make_documents_checklist_for_human:", checklist_create_df.columns.tolist())
    make_documents_checklist_for_human(checklist_create_df, apried_club_list_df)
    print('人間がチェックする用のリストの作成が完了しました。')

    # 8. 人間がチェックする用のリストの作成とチェックリストのチェック状況の更新
    print('人間がチェックする用のリストの作成とチェックリストのチェック状況の更新を行います...')
    checklist_create_df.columns = checklist_create_df.columns.str.strip()
    # ここでカラム名を「日本語名」にリネーム
    checklist_create_df = checklist_create_df.rename(
        columns={
            CHECKLIST_CREATION_DATETIME: 'チェックリスト作成日時',
            APPLICATION_DATETIME: '申請日時',
            CLUB_NAME: 'クラブ名'
        }
    )
    print("checklist_create_df columns before make_documents_checklist_for_human:", checklist_create_df.columns.tolist())
    write_checklist_by_human_check(checklist_create_df, apried_club_list_df, folder_of_checklist_create_status)
    print('人間がチェックする用のリストの作成とチェックリストのチェック状況の更新が完了しました。')
    print('全ての処理が完了しました。')

if __name__ == "__main__":
    main()