import pandas as pd
import os
from datetime import datetime, timezone, timedelta
from src.core.utils import get_jst_now
import logging


# 書類1に関するチェックリストを作成する関数
def make_document1_checklist_for_human(checklist_status_df, applied_club_df):
    """
    書類1に関する人間がチェックするためのチェックリストを作成します。
    """
    document1_checklist = []

    for index, row in applied_club_df.iterrows():
        club_name = row['クラブ名']
        # 申請日時はapplied_club_dfにもあるが、checklist_status_df優先で取得
        if club_name in checklist_status_df['クラブ名'].values:
            reception_date = checklist_status_df.loc[
                checklist_status_df['クラブ名'] == club_name, '申請日時'
            ].iloc[0]
        else:
            reception_date = row.get('申請日時', '不明')

        last_year_status = '登録済み' if row.get('R7年度登録クラブ', 0) == 1 else '未登録'
        jst_now = get_jst_now()

        checklist_row = {
            '申請日時': reception_date,
            'クラブ名': club_name,
            '入力されたクラブ名': row.get('申請_クラブ名_テキスト', ''),
            'チェック項目_クラブ名': '',
            '申請_法人格': row.get('申請_法人格', ''),
            '申請_代表者名': row.get('申請_代表者名', ''),
            '昨年度登録状況': last_year_status,
            '申請種別': row.get('申請_申請種別', ''),
            '申請_設立日': row.get('申請_設立日', ''),
            'チェック項目_申請種別': '',
            '申請_都道府県': row.get('申請_東京チェック', ''),
            '地区名': row.get('地区名', ''),
            '申請_区市町村名': row.get('区市町村名', ''),
            '申請_住所': row.get('申請_住所', ''),
            '申請_建物名(任意)': row.get('申請_建物名(任意)', ''),
            'チェック項目_住所': '',
            '申請_申請担当者名': row.get('申請_担当者名', ''),
            '申請_担当者役職名': row.get('申請_申請担当者役職', ''),
            'チェック項目_担当者名': '',
            '申請_メールアドレス': row.get('申請_メールアドレス', ''),
            '申請_電話番号': row.get('申請_TEL', ''),
            '申請_FAX番号': row.get('申請_FAX(任意)', ''),
            'チェック項目_連絡先': '',
            '申請_適合状況(1)①': row.get('申請_適合状況(1)①', ''),
            '申請_適合状況(1)②': row.get('申請_適合状況(1)②', ''),
            '申請_適合状況(1)③': row.get('申請_適合状況(1)③', ''),
            '申請_適合状況(1)④': row.get('申請_適合状況(1)④', ''),
            '申請_適合状況(2)⑤': row.get('申請_適合状況(2)⑤', ''),
            '申請_適合状況(3)⑥': row.get('申請_適合状況(3)⑥', ''),
            '申請_適合状況(3)⑦': row.get('申請_適合状況(3)⑦', ''),
            'チェック項目_適合状況': '',
            'チェック者名_申請内容': '',
            '受付日時': row.get('受付日時', ''),
            'チェックリスト作成日時': jst_now.strftime('%Y-%m-%d %H:%M:%S'),
            'チェック項目_その他': '',
            'チェック者名_受付内容': '',
            '備考': ''
        }

        document1_checklist.append(checklist_row)

    return document1_checklist

# 書類2_1に関するチェックリストを作成する関数
def make_document2_1_checklist_for_human(checklist_status_df, applied_club_df):
    """
    書類2_1に関する人間がチェックするためのチェックリストを作成します。
    """
    # チェックリストの初期化
    document2_1_checklist = []
    document2_1_number_of_menbers = []
    document2_1_number_of_annual_fee_members = []
    jst_now = get_jst_now()

    # 各クラブの行をイテレート
    for index, row in applied_club_df.iterrows():
        club_name = row['クラブ名']
        if club_name in checklist_status_df['クラブ名'].values:
            reception_date = checklist_status_df.loc[
                checklist_status_df['クラブ名'] == club_name, '申請日時'
            ].iloc[0]
        else:
            reception_date = row.get('申請日時', '不明')
        
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
        warning_issued = set()
        number_of_members = 0
        # 各列の値を足し合わせて会員数を算出
        for column in columns_of_number_of_members:
            if column in row and not pd.isna(row[column]):
                try:
                    number_of_members += int(row[column])
                except ValueError:
                    key = (club_name, column)
                    if key not in warning_issued:
                        logging.warning(f"クラブ '{club_name}' の列 '{column}' の値が整数に変換できません: {row[column]}")
                        warning_issued.add(key)
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
                        key = (club_name, column)
                        if key not in warning_issued:
                            logging.warning(f"クラブ '{club_name}' の列 '{column}' の値が整数に変換できません: {row[column]}")
                            warning_issued.add(key)
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
            'チェック者名_会員数': '',           
            '申請日時': reception_date,
            'チェックリスト作成日時': jst_now.strftime('%Y-%m-%d %H:%M:%S'),
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
            row_gender = {'性別': gender}
            for age in ages:
                col_name = age_gender_columns[age][gender]
                value = 0
                if col_name in row and not pd.isna(row[col_name]):
                    try:
                        value = int(row[col_name])
                    except ValueError:
                        pass
                row_gender[age] = value
            document2_1_number_of_menbers.append(row_gender)

        # 年会費会員数表（カラム名だけ「申請_年会_...」に置換）
        annual_fee_age_gender_columns = {
            age: {g: col.replace('申請_会員_', '申請_年会_') for g, col in gender_dict.items()}
            for age, gender_dict in age_gender_columns.items()
        }
        document2_1_number_of_annual_fee_members = []
        for gender in genders:
            row_gender = {'性別': gender}
            for age in ages:
                col_name = annual_fee_age_gender_columns[age][gender]
                value = 0
                if col_name in row and not pd.isna(row[col_name]):
                    try:
                        value = int(row[col_name])
                    except ValueError:
                        pass
                row_gender[age] = value
            document2_1_number_of_annual_fee_members.append(row_gender)

    return document2_1_checklist, document2_1_number_of_menbers, document2_1_number_of_annual_fee_members

# 書類2_2に関するチェックリストを作成する関数
def make_document2_2_checklist_for_human(checklist_status_df, applied_club_df):
    """
    書類2_2に関する人間がチェックするためのチェックリストを作成します。
    """
    document2_2_checklist = []
    document2_2_discipline_and_coaches = []
    
    jst_now = get_jst_now()

    for index, row in applied_club_df.iterrows():
        club_name = row['クラブ名']
        discipline_df = pd.read_excel('list_of_disciplines.xlsx')  # 競技種目のリストを読み込む
        discipline = discipline_df['disciplines']
        # 申請日時はapplied_club_dfにもあるが、checklist_status_df優先で取得
        if club_name in checklist_status_df['クラブ名'].values:
            reception_date = checklist_status_df.loc[
                checklist_status_df['クラブ名'] == club_name, '申請日時'
            ].iloc[0]
        else:
            reception_date = row.get('申請日時', '不明')
        # 競技種目数の取得  
        # 種目のカラムを修正（'申請_種目_'を付記）
        disciplines_columns = [f'申請_種目_{discipline}' for discipline in discipline]
        extra_disciplines_column = row.get('申請_種目_その他_数(選択時必須)', 0)
        count_of_disciplines = 0
        # 各種目カラムをループし、「定期的に行っている」が選択されているかを確認
        for col in disciplines_columns:
            if col in row and row[col] == '定期的に行っている':
                count_of_disciplines += 1
        count_of_disciplines += extra_disciplines_column in row and row[extra_disciplines_column] != '' and row[extra_disciplines_column] != '0'
        # 競技種目数が0の場合は、'0'と記載
        if count_of_disciplines == 0:
            count_of_disciplines = '0'
        else:
            count_of_disciplines = str(count_of_disciplines)
        
        # 指導者数の取得(discipline_df['coach']が1のカラムに限定)
        coaches_discipline = discipline_df[discipline_df['coach'] == 1]['disciplines'].tolist()
        coaches_columns = [f'申請_指導者_{discipline}' for discipline in coaches_discipline]
        count_of_coaches = 0
        # 各指導者カラムをループし、「配置している」が選択されているかを確認
        for col in coaches_columns:
            if col in row and row[col] == '配置している':
                count_of_coaches += 1
        # 指導者数が0の場合は、'0'と記載
        if count_of_coaches == 0:
            count_of_coaches = '0'
        else:
            count_of_coaches = str(count_of_coaches)
        
        # クラブマネジャーの配置状況を取得
        club_manager_columns = row.get('申請_マネジャー_配置状況', '')
        club_manager_status = club_manager_columns

        # マネジメント指導者資格の数
        num_of_club_managers_as_manager = row.get('申請_マネジャー_マネ資格_数', 0)
        num_of_assistant_managers_as_manager = row.get('申請_マネジャー_アシマネ資格_数', 0)
        num_of_club_managers_as_staff = row.get('申請_事務局_マネ資格_数', 0)
        num_of_assistant_managers_as_staff = row.get('申請_事務局_アシマネ資格_数', 0)

        checklist_row = {
            'クラブ名': club_name,
            '活動種目数': count_of_disciplines,
            'チェック項目_活動種目': '',
            '指導者数': count_of_coaches,
            'チェック項目_指導者': '',
            'チェック項目_種目・指導者': '',
            'クラブマネジャー': club_manager_status,
            'チェック項目_クラブマネジャー配置': '',
            'クラブマネジャー資格数（クラブマネジャー）': num_of_club_managers_as_manager,
            'アシスタントマネジャー資格数（クラブマネジャー）': num_of_assistant_managers_as_manager,
            'クラブマネジャー資格数（事務局）': num_of_club_managers_as_staff,
            'アシスタントマネジャー資格数（事務局）': num_of_assistant_managers_as_staff,
            'チェック項目_マネジメント指導者資格': '',
            'チェック者名_活動内容': '',
            '申請日時': reception_date,
            'チェックリスト作成日時': jst_now.strftime('%Y-%m-%d %H:%M:%S'),
            '備考': ''
        }

        document2_2_checklist.append(checklist_row)

        # 書類2_2の競技種目と指導者のリストを作成
        # discipline_dfの読み込み
        discipline_df = pd.read_excel('list_of_disciplines.xlsx')
        disciplines = discipline_df['disciplines'].tolist()

        # 種目ごとの実施有無・指導者有無の表を作成
        document2_2_discipline_and_coaches = []

        for discipline in disciplines:
            row_dict = {}
            row_dict['種目'] = discipline

            # 実施有無
            col_name = f'申請_種目_{discipline}'
            if col_name in row:
                # 例: '定期的に行っている' など
                row_dict['実施有無'] = row[col_name]
            else:
                row_dict['実施有無'] = ''

            # 指導者有無
            coach_flag = discipline_df.loc[discipline_df['disciplines'] == discipline, 'coach'].values[0]
            if coach_flag == 1:
                # 指導者カラム名
                coach_col = f'申請_指導者_{discipline}'
                if coach_col in row:
                    row_dict['指導者有無'] = row[coach_col]
                else:
                    row_dict['指導者有無'] = ''
            else:
                row_dict['指導者有無'] = '/'

            document2_2_discipline_and_coaches.append(row_dict)

        # 「その他」種目の追加
        if '申請_種目_その他_数(選択時必須)' in row and row['申請_種目_その他_数(選択時必須)'] not in ['', '0', 0]:
            # 自由記述の種目名（例: '申請_種目_その他_テキスト(選択時必須)'）
            other_name = row.get('申請_種目_その他_テキスト(選択時必須)', 'その他')
            row_dict = {
                '種目': other_name,
                '実施有無': row.get('申請_種目_その他_数(選択時必須)', ''),
                '指導者有無': row.get('申請_指導者_その他', '')
            }
            document2_2_discipline_and_coaches.append(row_dict)

    return document2_2_checklist, document2_2_discipline_and_coaches

# 書類3に関するチェックリストを作成する関数(規約についてのチェックリスト)
def make_document3_checklist_for_human(checklist_status_df, applied_club_df):
    """
    書類3に関する人間がチェックするためのチェックリストを作成します。
    """
    document3_checklist = []
    jst_now = get_jst_now()
    for index, row in applied_club_df.iterrows():
        club_name = row['クラブ名']
        # 申請日時はapplied_club_dfにもあるが、checklist_status_df優先
        if club_name in checklist_status_df['クラブ名'].values:
            reception_date = checklist_status_df.loc[
                checklist_status_df['クラブ名'] == club_name, '申請日時'
            ].iloc[0]
        else:
            reception_date = row.get('申請日時', '不明')
        # チェックリストの行を作成
        checklist_row = {
            'クラブ名': club_name,
            'チェック項目_組織の規約等である': '',
            'チェック項目_法人格': '',
            'チェック項目_会員資格': '',
            'チェック項目_規約等の改廃意思決定機関': '',
            'チェック項目_規約等の改廃意思決定機関の議決権保有者': '',
            'チェック項目_規約等の改廃意思決定機関の定足数': '',
            'チェック項目_規約等の改廃意思決定機関の議決数': '',
            'チェック項目_規約等の改廃意思決定機関の議事録': '',
            'チェック項目_事業計画の意思決定機関': '',
            'チェック項目_事業計画の意思決定機関の議決権保有者': '',
            'チェック項目_事業計画の意思決定機関の定足数': '',
            'チェック項目_事業計画の意思決定機関の議決数': '',
            'チェック項目_事業計画の意思決定機関の議事録': '',
            'チェック項目_予算の意思決定機関': '',
            'チェック項目_予算の意思決定機関の議決権保有者': '',
            'チェック項目_予算の意思決定機関の定足数': '',
            'チェック項目_予算の意思決定機関の議決数': '',
            'チェック項目_予算の意思決定機関の議事録': '',
            'チェック項目_事業報告の意思決定機関': '',
            'チェック項目_事業報告の意思決定機関の議決権保有者': '',
            'チェック項目_事業報告の意思決定機関の定足数': '',
            'チェック項目_事業報告の意思決定機関の議決数': '',
            'チェック項目_事業報告の意思決定機関の議事録': '',
            'チェック項目_決算の意思決定機関': '',
            'チェック項目_決算の意思決定機関の議決権保有者': '',
            'チェック項目_決算の意思決定機関の定足数': '',
            'チェック項目_決算の意思決定機関の議決数': '',
            'チェック項目_決算の意思決定機関の議事録': '',
            'チェック項目_役員資格・選任規程': '',
            'チェック者名_規約': '',
            '申請日時': reception_date,
            'チェックリスト作成日時': jst_now.strftime('%Y-%m-%d %H:%M:%S'),
            '備考': ''
        }
        document3_checklist.append(checklist_row)

    return document3_checklist

# 書類4に関するチェックリストを作成する関数(議決権保有者名簿についてのチェックリスト)
def make_document4_checklist_for_human(checklist_status_df, applied_club_df):
    """
    書類4に関する人間がチェックするためのチェックリストを作成します。
    """
    document4_checklist = []
    jst_now = get_jst_now()
    for index, row in applied_club_df.iterrows():
        club_name = row['クラブ名']
        # 申請日時はapplied_club_dfにもあるが、checklist_status_df優先
        if club_name in checklist_status_df['クラブ名'].values:
            reception_date = checklist_status_df.loc[
                checklist_status_df['クラブ名'] == club_name, '申請日時'
            ].iloc[0]
        else:
            reception_date = row.get('申請日時', '不明')
        # チェックリストの行を作成
        checklist_row = {
            'クラブ名': club_name,
            '区市町村名': row.get('申請_区市町村名', ''),
            'チェック項目_議決権保有者名簿_1の構成員': '',
            'チェック項目_議決権保有者名簿_1の記載人数': '',
            'チェック項目_議決権保有者名簿_1の近隣住民数': '',
            'チェック者名_議決権保有者名簿_1': '',
            'チェック項目_議決権保有者名簿_2の構成員': '',
            'チェック項目_議決権保有者名簿_2の記載人数': '',
            'チェック項目_議決権保有者名簿_2の近隣住民数': '',
            'チェック者名_議決権保有者名簿_2': '',
            'チェック項目_議決権保有者名簿_3の構成員': '',
            'チェック項目_議決権保有者名簿_3の記載人数': '',
            'チェック項目_議決権保有者名簿_3の近隣住民数': '',
            'チェック者名_議決権保有者名簿_3': '',
            'チェック項目_議決権保有者名簿_4の構成員': '',
            'チェック項目_議決権保有者名簿_4の記載人数': '',
            'チェック項目_議決権保有者名簿_4の近隣住民数': '',
            'チェック者名_議決権保有者名簿_4': '',
            'チェック項目_議決権保有者名簿_5の構成員': '',
            'チェック項目_議決権保有者名簿_5の記載人数': '',
            'チェック項目_議決権保有者名簿_5の近隣住民数': '',
            'チェック者名_議決権保有者名簿_5': '',
            '申請日時': reception_date,
            'チェックリスト作成日時': jst_now.strftime('%Y-%m-%d %H:%M:%S'),
            '備考': ''
        }
        document4_checklist.append(checklist_row)

    # 書類4のリスト1からリスト5のチェックリストを作成
    document4_lists_checklist = []

    # 隣接自治体リストの読み込み
    municipalities_df = pd.read_excel('municipality_test_tokyo.xlsx')

    for index, row in applied_club_df.iterrows():
        club_name = row['クラブ名']
        address = row['申請_区市町村名']

        # チェックリスト本体（省略、既存のまま）

        # 隣接自治体リスト作成
        muni_row = municipalities_df[municipalities_df['市区町村'] == address]
        # address自身＋隣接自治体をリスト化
        adjacent_list = [address]
        if not muni_row.empty:
            for i in range(1, 10):
                col = f'隣接市区町村{i}'
                val = muni_row.iloc[0].get(col, '')
                if pd.notna(val) and str(val).strip() != '':
                    adjacent_list.append(str(val).strip())
        # DataFrame形式で追加
        for muni in adjacent_list:
            document4_lists_checklist.append({'自治体名': muni, '数': ''})

    return document4_checklist, document4_lists_checklist

# 書類5_事業計画に関するチェックリストを作成する関数(事業計画書についてのチェックリスト)
def make_document5_plan_checklist_for_human(checklist_status_df, applied_club_df):
    """
    書類5_事業計画に関する人間がチェックするためのチェックリストを作成します。
    """
    document5_plan_checklist = []    
    # 書類5の競技種目ごとの事業計画書チェックリストを作成
    document5_plan_checklist_discipline = []
    jst_now = get_jst_now()

    for index, row in applied_club_df.iterrows():
        club_name = row['クラブ名']
        # 申請日時はapplied_club_dfにもあるが、checklist_status_df優先
        if club_name in checklist_status_df['クラブ名'].values:
            reception_date = checklist_status_df.loc[
                checklist_status_df['クラブ名'] == club_name, '申請日時'
            ].iloc[0]
        else:
            reception_date = row.get('申請日時', '不明')
        # チェックリストの行を作成
        checklist_row = {
            'クラブ名': club_name,
            'チェック者名_活動頻度': '',
            '申請日時': reception_date,
            'チェックリスト作成日時': jst_now.strftime('%Y-%m-%d %H:%M:%S'),
            '備考': ''
        }
        document5_plan_checklist.append(checklist_row)

        # discipline_dfの読み込み
        discipline_df = pd.read_excel('list_of_disciplines.xlsx')
        disciplines = discipline_df['disciplines'].tolist()

        # 実施種目ごとのリスト（実施しているもののみ）
        for discipline in disciplines:
            col_name = f'申請_種目_{discipline}'
            if col_name in row and row[col_name] == '実施している':
                row_dict = {
                    'クラブ名': club_name,
                    '種目': discipline,
                    '実施有無': row[col_name]
                }
                document5_plan_checklist_discipline.append(row_dict)

        # 「その他」種目の追加（実施している場合のみ）
        if '申請_種目_その他_数(選択時必須)' in row and row['申請_種目_その他_数(選択時必須)'] not in ['', '0', 0]:
            other_name = row.get('申請_種目_その他_テキスト(選択時必須)', 'その他')
            # 「実施している」かどうか判定（値が「実施している」または数値が1以上など、要件に応じて調整）
            if row['申請_種目_その他_数(選択時必須)'] == '実施している' or str(row['申請_種目_その他_数(選択時必須)']).isdigit():
                row_dict = {
                    'クラブ名': club_name,
                    '種目': other_name,
                    '実施有無': row['申請_種目_その他_数(選択時必須)']
                }
                document5_plan_checklist_discipline.append(row_dict)

    return document5_plan_checklist, document5_plan_checklist_discipline

# 書類5_予算に関するチェックリストを作成する関数(予算書についてのチェックリスト)
def make_document5_budget_checklist_for_human(checklist_status_df, applied_club_df):
    """
    書類5_予算に関する人間がチェックするためのチェックリストを作成します。
    """
    document5_budget_checklist = []
    jst_now = get_jst_now()
    for index, row in applied_club_df.iterrows():
        club_name = row['クラブ名']
        # 申請日時はapplied_club_dfにもあるが、checklist_status_df優先
        if club_name in checklist_status_df['クラブ名'].values:
            reception_date = checklist_status_df.loc[
                checklist_status_df['クラブ名'] == club_name, '申請日時'
            ].iloc[0]
        else:
            reception_date = row.get('申請日時', '不明')
        # チェックリストの行を作成
        checklist_row = {
            'クラブ名': club_name,
            'チェック者名_予算書': '',
            '申請日時': reception_date,
            'チェックリスト作成日時': jst_now.strftime('%Y-%m-%d %H:%M:%S'),
            '備考': ''
        }
        document5_budget_checklist.append(checklist_row)
    return document5_budget_checklist

# 書類6_事業報告に関するチェックリストを作成する関数(事業報告書についてのチェックリスト)(事業計画とほぼ同じ)
def make_document6_report_checklist_for_human(checklist_status_df, applied_club_df):
    """
    書類6_事業報告に関する人間がチェックするためのチェックリストを作成します。
    """
    document6_report_checklist = []
    # 書類6の競技種目ごとの事業報告書チェックリストを作成
    document6_report_checklist_discipline = []
    jst_now = get_jst_now()
    for index, row in applied_club_df.iterrows():
        club_name = row['クラブ名']
        # 申請日時はapplied_club_dfにもあるが、checklist_status_df優先
        if club_name in checklist_status_df['クラブ名'].values:
            reception_date = checklist_status_df.loc[
                checklist_status_df['クラブ名'] == club_name, '申請日時'
            ].iloc[0]
        else:
            reception_date = row.get('申請日時', '不明')
        # チェックリストの行を作成
        checklist_row = {
            'クラブ名': club_name,
            'チェック者名_活動頻度': '',
            '申請日時': reception_date,
            'チェックリスト作成日時': jst_now.strftime('%Y-%m-%d %H:%M:%S'),
            '備考': ''
        }
        document6_report_checklist.append(checklist_row)
        # discipline_dfの読み込み
        discipline_df = pd.read_excel('list_of_disciplines.xlsx')
        disciplines = discipline_df['disciplines'].tolist()
        # 実施種目ごとのリスト（実施しているもののみ）
        # 実施種目ごとのリスト（実施しているもののみ）
        for discipline in disciplines:
            col_name = f'申請_種目_{discipline}'
            if col_name in row and row[col_name] == '実施している':
                row_dict = {
                    'クラブ名': club_name,
                    '種目': discipline,
                    '実施有無': row[col_name]
                }
                document6_report_checklist_discipline.append(row_dict)

        # 「その他」種目の追加（実施している場合のみ）
        if '申請_種目_その他_数(選択時必須)' in row and row['申請_種目_その他_数(選択時必須)'] not in ['', '0', 0]:
            other_name = row.get('申請_種目_その他_テキスト(選択時必須)', 'その他')
            # 「実施している」かどうか判定（値が「実施している」または数値が1以上など、要件に応じて調整）
            if row['申請_種目_その他_数(選択時必須)'] == '実施している' or str(row['申請_種目_その他_数(選択時必須)']).isdigit():
                row_dict = {
                    'クラブ名': club_name,
                    '種目': other_name,
                    '実施有無': row['申請_種目_その他_数(選択時必須)']
                }
                document6_report_checklist_discipline.append(row_dict)
    return document6_report_checklist, document6_report_checklist_discipline

# 書類6_決算に関するチェックリストを作成する関数(決算書についてのチェックリスト)
def make_document6_financial_statements_checklist_for_human(checklist_status_df, applied_club_df):
    """
    書類6_決算に関する人間がチェックするためのチェックリストを作成します。
    """
    document6_financial_statements_checklist = []
    jst_now = get_jst_now()
    for index, row in applied_club_df.iterrows():
        club_name = row['クラブ名']
        # 申請日時はapplied_club_dfにもあるが、checklist_status_df優先
        if club_name in checklist_status_df['クラブ名'].values:
            reception_date = checklist_status_df.loc[
                checklist_status_df['クラブ名'] == club_name, '申請日時'
            ].iloc[0]
        else:
            reception_date = row.get('申請日時', '不明')
        # チェックリストの行を作成
        checklist_row = {
            'クラブ名': club_name,
            'チェック者名_決算書': '',
            '申請日時': reception_date,
            'チェックリスト作成日時': jst_now.strftime('%Y-%m-%d %H:%M:%S'),
            '備考': ''
        }
        document6_financial_statements_checklist.append(checklist_row)
    return document6_financial_statements_checklist

# 書類7に関するチェックリストを作成する関数
def make_document7_checklist_for_human(checklist_status_df, applied_club_df):
    """
    書類7に関する人間がチェックするためのチェックリストを作成します。
    """
    document7_checklist = []
    jst_now = get_jst_now()
    for index, row in applied_club_df.iterrows():
        club_name = row['クラブ名']
        # 申請日時はapplied_club_dfにもあるが、checklist_status_df優先
        if club_name in checklist_status_df['クラブ名'].values:
            reception_date = checklist_status_df.loc[
                checklist_status_df['クラブ名'] == club_name, '申請日時'
            ].iloc[0]
        else:
            reception_date = row.get('申請日時', '不明')
        # チェックリストの行を作成
        checklist_row = {
            'クラブ名': club_name,
            'チェック者名_自己点検・評価シート': '',
            '申請日時': reception_date,
            'チェックリスト作成日時': jst_now.strftime('%Y-%m-%d %H:%M:%S'),
            '備考': ''
        }
        document7_checklist.append(checklist_row)
    return document7_checklist
# 書類8に関するチェックリストを作成する関数
def make_document8_checklist_for_human(checklist_status_df, applied_club_df):
    """
    書類8に関する人間がチェックするためのチェックリストを作成します。
    """
    document8_checklist = []
    jst_now = get_jst_now()
    for index, row in applied_club_df.iterrows():
        club_name = row['クラブ名']
        # 申請日時はapplied_club_dfにもあるが、checklist_status_df優先
        if club_name in checklist_status_df['クラブ名'].values:
            reception_date = checklist_status_df.loc[
                checklist_status_df['クラブ名'] == club_name, '申請日時'
            ].iloc[0]
        else:
            reception_date = row.get('申請日時', '不明')
        # チェックリストの行を作成
        checklist_row = {
            'クラブ名': club_name,
            'チェック項目_議事録_規約等_開催日時': '',
            'チェック項目_議事録_規約等_開催場所': '',
            'チェック項目_議事録_規約等_出席役員': '',
            'チェック項目_議事録_規約等_出席議決権保有者数': '',
            'チェック項目_議事録_規約等_議事': '',
            'チェック項目_議事録_規約等_決議': '',
            'チェック項目_議事録_規約等_署名等': '',
            'チェック者名_議事録_規約等': '',
            'チェック項目_議事録_事業計画_開催日時': '',
            'チェック項目_議事録_事業計画_開催場所': '',
            'チェック項目_議事録_事業計画_出席役員': '',
            'チェック項目_議事録_事業計画_出席議決権保有者数': '',
            'チェック項目_議事録_事業計画_議事': '',
            'チェック項目_議事録_事業計画_決議': '',
            'チェック項目_議事録_事業計画_署名等': '',
            'チェック者名_議事録_事業計画': '',
            'チェック項目_議事録_予算_開催日時': '',
            'チェック項目_議事録_予算_開催場所': '',
            'チェック項目_議事録_予算_出席役員': '',
            'チェック項目_議事録_予算_出席議決権保有者数': '',
            'チェック項目_議事録_予算_議事': '',
            'チェック項目_議事録_予算_決議': '',
            'チェック項目_議事録_予算_署名等': '',
            'チェック者名_議事録_予算': '',
            'チェック項目_議事録_事業報告_開催日時': '',
            'チェック項目_議事録_事業報告_開催場所': '',
            'チェック項目_議事録_事業報告_出席役員': '',
            'チェック項目_議事録_事業報告_出席議決権保有者数': '',
            'チェック項目_議事録_事業報告_議事': '',
            'チェック項目_議事録_事業報告_決議': '',
            'チェック項目_議事録_事業報告_署名等': '',
            'チェック者名_議事録_事業報告': '',
            'チェック項目_議事録_決算_開催日時': '',
            'チェック項目_議事録_決算_開催場所': '',
            'チェック項目_議事録_決算_出席役員': '',
            'チェック項目_議事録_決算_出席議決権保有者数': '',
            'チェック項目_議事録_決算_議事': '',
            'チェック項目_議事録_決算_決議': '',
            'チェック項目_議事録_決算_署名等': '',
            'チェック者名_議事録_決算': '',
            '申請日時': reception_date,
            'チェックリスト作成日時': jst_now.strftime('%Y-%m-%d %H:%M:%S'),
            '備考': ''
        }
        document8_checklist.append(checklist_row)

    return document8_checklist

# 書類9に関するチェックリストを作成する関数
def make_document9_checklist_for_human(checklist_status_df, applied_club_df):
    """
    書類9に関する人間がチェックするためのチェックリストを作成します。
    """
    document9_checklist = []
    jst_now = get_jst_now()
    for index, row in applied_club_df.iterrows():
        club_name = row['クラブ名']
        # 申請日時はapplied_club_dfにもあるが、checklist_status_df優先
        if club_name in checklist_status_df['クラブ名'].values:
            reception_date = checklist_status_df.loc[
                checklist_status_df['クラブ名'] == club_name, '申請日時'
            ].iloc[0]
        else:
            reception_date = row.get('申請日時', '不明')
        # チェックリストの行を作成
        checklist_row = {
            'クラブ名': club_name,
            'チェック者名_自己説明・公表確認書': '',
            '申請日時': reception_date,
            'チェックリスト作成日時': jst_now.strftime('%Y-%m-%d %H:%M:%S'),
            '備考': ''
        }
        document9_checklist.append(checklist_row)
    return document9_checklist