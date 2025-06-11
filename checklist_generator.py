import pandas as pd
import os
from datetime import datetime, timezone, timedelta

# 書類1に関するチェックリストを作成する関数
def make_document1_checklist_for_human(club_df, checklist_create_df):
    """
    書類1に関する人間がチェックするためのチェックリストを作成します。
    """
    document1_checklist = []

    for index, row in club_df.iterrows():
        club_name = row['クラブ名']
        # 申請日時はclub_dfにもあるが、checklist_create_df優先で取得
        if club_name in checklist_create_df['クラブ名'].values:
            application_date = checklist_create_df.loc[
                checklist_create_df['クラブ名'] == club_name, '申請日時'
            ].iloc[0]
        else:
            application_date = row.get('申請日時', '不明')

        last_year_status = '登録済み' if row.get('R7年度登録クラブ', 0) == 1 else '未登録'

        checklist_row = {
            'クラブ名': club_name,
            '入力されたクラブ名': row.get('申請_クラブ名_テキスト', ''),
            'チェック項目_クラブ名': '',
            '申請_法人格': row.get('申請_法人格', ''),
            'チェック項目_法人格': '',
            '申請_代表者名': row.get('申請_代表者名', ''),
            'チェック項目_代表者名': '',
            '昨年度登録状況': last_year_status,
            '申請種別': row.get('申請_申請種別', ''),
            'チェック項目_申請種別': '',
            '申請_設立日': row.get('申請_設立日', ''),
            'チェック項目_設立日': '',
            '申請_住所': row.get('申請_住所', ''),
            'チェック項目_住所': '',
            '申請_建物名(任意)': row.get('申請_建物名(任意)', ''),
            'チェック項目_建物名': '',
            '申請_電話番号': row.get('申請_TEL', ''),
            'チェック項目_電話番号': '',
            '申請_FAX番号': row.get('申請_FAX(任意)', ''),
            'チェック項目_FAX番号': '',
            '申請_メールアドレス': row.get('申請_メールアドレス', ''),
            'チェック項目_メールアドレス': '',
            '申請_申請担当者名': row.get('申請_申請担当者名', ''),
            'チェック項目_申請担当者名': '',
            '申請_申請担当者役職': row.get('申請_申請担当者役職', ''),
            'チェック項目_申請担当者役職': '',
            '申請_適合状況(1)①': row.get('申請_適合状況(1)①', ''),
            'チェック項目_適合状況(1)①': '',
            '申請_適合状況(1)②': row.get('申請_適合状況(1)②', ''),
            'チェック項目_適合状況(1)②': '',
            '申請_適合状況(1)③': row.get('申請_適合状況(1)③', ''),
            'チェック項目_適合状況(1)③': '',
            '申請_適合状況(1)④': row.get('申請_適合状況(1)④', ''),
            'チェック項目_適合状況(1)④': '',
            '申請_適合状況(2)⑤': row.get('申請_適合状況(2)⑤', ''),
            'チェック項目_適合状況(2)⑤': '',
            '申請_適合状況(3)⑥': row.get('申請_適合状況(3)⑥', ''),
            'チェック項目_適合状況(3)⑥': '',
            '申請_適合状況(3)⑦': row.get('申請_適合状況(3)⑦', ''),
            'チェック項目_適合状況(3)⑦': '',
            '申請日時': application_date,
            '備考': ''
        }

        document1_checklist.append(checklist_row)

    return document1_checklist

# 書類2_1に関するチェックリストを作成する関数
def make_document2_1_checklist_for_human(club_df, checklist_create_df):
    """
    書類2_1に関する人間がチェックするためのチェックリストを作成します。
    """
    # チェックリストの初期化
    document2_1_checklist = []

    # 各クラブの行をイテレート
    for index, row in club_df.iterrows():
        club_name = row['クラブ名']
        # 申請日時はclub_dfにもあるが、checklist_create_df優先で取得
        if club_name in checklist_create_df['クラブ名'].values:
            application_date = checklist_create_df.loc[
                checklist_create_df['クラブ名'] == club_name, '申請日時'
            ].iloc[0]
        else:
            application_date = row.get('申請日時', '不明')
        
        # 入力内容を基に会員数を算出
        columns_of_number_of_members = [
            '申請_会員_未就_男_数',
            '申請_会員_未就_女_数',
            '申請_会員_未就_不_数',
            '申請_会員_小_男_数',
            '申請_会員_小_女_数',
            '申請_会員_小_不_数',
            '申請_会員_中_男_数',
            '申請_会員_中_女_数',
            '申請_会員_中_不_数',
            '申請_会員_高_男_数',
            '申請_会員_高_女_数',
            '申請_会員_高_不_数',
            '申請_会員_20s_男_数',
            '申請_会員_20s_女_数',
            '申請_会員_20s_不_数',
            '申請_会員_30s_男_数',
            '申請_会員_30s_女_数',
            '申請_会員_30s_不_数',
            '申請_会員_40s_男_数',
            '申請_会員_40s_女_数',
            '申請_会員_40s_不_数',
            '申請_会員_50s_男_数',
            '申請_会員_50s_女_数',
            '申請_会員_50s_不_数',
            '申請_会員_60s_男_数',
            '申請_会員_60s_女_数',
            '申請_会員_60s_不_数',
            '申請_会員_70s_男_数',
            '申請_会員_70s_女_数',
            '申請_会員_70s_不_数'
        ]
        number_of_members = 0
        # 各列の値を足し合わせて会員数を算出
        for column in columns_of_number_of_members:
            if column in row and not pd.isna(row[column]):
                try:
                    number_of_members += int(row[column])
                except ValueError:
                    print(f"警告: クラブ '{club_name}' の列 '{column}' の値が整数に変換できません: {row[column]}")
                    number_of_members += 0
        # 会員数が0の場合は、'0'と記載
        if number_of_members == 0:
            number_of_members = '0'
        else:
            number_of_members = str(number_of_members)
        
        # 入力内容を基に年会費を払っている会員数を算出
        columns_of_annual_fee_members = [
            '申請_年会_未就_男_数',
            '申請_年会_未就_女_数',
            '申請_年会_未就_不_数',
            '申請_年会_小_男_数',
            '申請_年会_小_女_数',
            '申請_年会_小_不_数',
            '申請_年会_中_男_数',
            '申請_年会_中_女_数',
            '申請_年会_中_不_数',
            '申請_年会_高_男_数',
            '申請_年会_高_女_数',
            '申請_年会_高_不_数',
            '申請_年会_20s_男_数',
            '申請_年会_20s_女_数',
            '申請_年会_20s_不_数',
            '申請_年会_30s_男_数',
            '申請_年会_30s_女_数',
            '申請_年会_30s_不_数',
            '申請_年会_40s_男_数',
            '申請_年会_40s_女_数',
            '申請_年会_40s_不_数',
            '申請_年会_50s_男_数',
            '申請_年会_50s_女_数',
            '申請_年会_50s_不_数',
            '申請_年会_60s_男_数',
            '申請_年会_60s_女_数',
            '申請_年会_60s_不_数',
            '申請_年会_70s_男_数',
            '申請_年会_70s_女_数',
            '申請_年会_70s_不_数'
        ]
        number_of_annual_fee_members = 0
        # 各列の値を足し合わせて年会費を払っている会員数を算出
        for column in columns_of_annual_fee_members:
            if column in row and not pd.isna(row[column]):
                try:
                    number_of_annual_fee_members += int(row[column])
                except ValueError:
                    print(f"警告: クラブ '{club_name}' の列 '{column}' の値が整数に変換できません: {row[column]}")
                    number_of_annual_fee_members += 0
        # 年会費を払っている会員数が0の場合は、'0'と記載
        if number_of_annual_fee_members == 0:
            number_of_annual_fee_members = '0'
        else:
            number_of_annual_fee_members = str(number_of_annual_fee_members)

        # チェックリストの行を作成
        checklist_row = {
            'クラブ名': club_name,
            '会員数': number_of_members,
            '年会費を払っている会員数': number_of_annual_fee_members,
            'チェック項目_会員数': '',           
            '申請日時': application_date,
            '備考': ''
        }
        # チェックリストに追加
        document2_1_checklist.append(checklist_row)

        # 年代・性別ごとのカラム名マッピング
        age_gender_columns = {
            '未就学児':   {'男性': '申請_会員_未就_男_数', '女性': '申請_会員_未就_女_数', '性別不明': '申請_会員_未就_不_数'},
            '小学生':     {'男性': '申請_会員_小_男_数',   '女性': '申請_会員_小_女_数',   '性別不明': '申請_会員_小_不_数'},
            '中学生':     {'男性': '申請_会員_中_男_数',   '女性': '申請_会員_中_女_数',   '性別不明': '申請_会員_中_不_数'},
            '高校生':     {'男性': '申請_会員_高_男_数',   '女性': '申請_会員_高_女_数',   '性別不明': '申請_会員_高_不_数'},
            '20代':      {'男性': '申請_会員_20s_男_数',  '女性': '申請_会員_20s_女_数',  '性別不明': '申請_会員_20s_不_数'},
            '30代':      {'男性': '申請_会員_30s_男_数',  '女性': '申請_会員_30s_女_数',  '性別不明': '申請_会員_30s_不_数'},
            '40代':      {'男性': '申請_会員_40s_男_数',  '女性': '申請_会員_40s_女_数',  '性別不明': '申請_会員_40s_不_数'},
            '50代':      {'男性': '申請_会員_50s_男_数',  '女性': '申請_会員_50s_女_数',  '性別不明': '申請_会員_50s_不_数'},
            '60代':      {'男性': '申請_会員_60s_男_数',  '女性': '申請_会員_60s_女_数',  '性別不明': '申請_会員_60s_不_数'},
            '70代以上':  {'男性': '申請_会員_70s_男_数',  '女性': '申請_会員_70s_女_数',  '性別不明': '申請_会員_70s_不_数'},
        }
        genders = ['男性', '女性', '性別不明']
        ages = ['未就学児', '小学生', '中学生', '高校生', '20代', '30代', '40代', '50代', '60代', '70代以上']

        # 会員数表
        document2_1_number_of_menbers = []
        for gender in genders:
            row = {'性別': gender}
            for age in ages:
                col_name = age_gender_columns[age][gender]
                value = 0
                for _, club_row in club_df.iterrows():
                    if col_name in club_row and not pd.isna(club_row[col_name]):
                        try:
                            value += int(club_row[col_name])
                        except ValueError:
                            pass
                row[age] = value
            document2_1_number_of_menbers.append(row)

        # 年会費会員数表（カラム名だけ「申請_年会_...」に置換）
        annual_fee_age_gender_columns = {
            age: {g: col.replace('申請_会員_', '申請_年会_') for g, col in gender_dict.items()}
            for age, gender_dict in age_gender_columns.items()
        }
        document2_1_number_of_annual_fee_members = []
        for gender in genders:
            row = {'性別': gender}
            for age in ages:
                col_name = annual_fee_age_gender_columns[age][gender]
                value = 0
                for _, club_row in club_df.iterrows():
                    if col_name in club_row and not pd.isna(club_row[col_name]):
                        try:
                            value += int(club_row[col_name])
                        except ValueError:
                            pass
                row[age] = value
            document2_1_number_of_annual_fee_members.append(row)

    return document2_1_checklist, document2_1_number_of_menbers, document2_1_number_of_annual_fee_members

# 書類2_2に関するチェックリストを作成する関数
def make_document2_2_checklist_for_human(club_df, checklist_create_df):
    """
    書類2_2に関する人間がチェックするためのチェックリストを作成します。
    """
    document2_2_checklist = []

    for index, row in club_df.iterrows():
        club_name = row['クラブ名']
        # 申請日時はclub_dfにもあるが、checklist_create_df優先で取得
        if club_name in checklist_create_df['クラブ名'].values:
            application_date = checklist_create_df.loc[
                checklist_create_df['クラブ名'] == club_name, '申請日時'
            ].iloc[0]
        else:
            application_date = row.get('申請日時', '不明')

        checklist_row = {
            'クラブ名': club_name,
            '申請_活動内容': row.get('申請_活動内容', ''),
            'チェック項目_活動内容': '',
            '申請_活動目的': row.get('申請_活動目的', ''),
            'チェック項目_活動目的': '',
            '申請_活動計画': row.get('申請_活動計画', ''),
            'チェック項目_活動計画': '',
            '申請_活動実績': row.get('申請_活動実績', ''),
            'チェック項目_活動実績': '',
            '申請日時': application_date,
            '備考': ''
        }

        document2_2_checklist.append(checklist_row)

    return document2_2_checklist