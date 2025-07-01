def make_detailed_club_data(club_reception_df):
    import os
    import pandas as pd
    import logging
    from make_folders import setup_logging, create_folders
    from setting_paths import content_check_folder_path, clubs_details_data_folder_path

    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()
    logging.info("フォルダを作成しました")

    # discipline_dfの読み込み
    discipline_df = pd.read_excel('list_of_disciplines.xlsx')
    disciplines = discipline_df['disciplines'].tolist()


    # クラブごとに処理
    club_names = club_reception_df['クラブ名'].unique()
    for club_name in club_names:
        logging.info(f"クラブ名: {club_name} の詳細データを処理します")

        # クラブごとのデータを抽出
        club_data = club_reception_df[club_reception_df['クラブ名'] == club_name]
        if club_data.empty:
            logging.warning(f"クラブ名: {club_name} のデータが見つかりません")
            continue

        # 1.クラブごとの詳細データ保存フォルダを作成（存在しない場合）
        club_detail_data_folder_name = f"{club_name}_詳細データ"
        club_detail_data_folder_path = os.path.join(clubs_details_data_folder_path, club_detail_data_folder_name)
        if not os.path.exists(club_detail_data_folder_path):
            os.makedirs(club_detail_data_folder_path)
            logging.info(f"クラブフォルダを作成しました: {club_detail_data_folder_path}")
        else:
            logging.info(f"クラブフォルダは既に存在します: {club_detail_data_folder_path}")

        # 2. クラブごとの詳細データを作成  
        # 申請日時をYYYYMMDDHHMMSS形式に変換し、指定
        application_date = pd.to_datetime(club_reception_df['申請_タイムスタンプ']).dt.strftime('%Y%m%d%H%M%S')
        # 2.1. 会員数のリストを作成
        logging.info(f"クラブ名: {club_name} の会員数の詳細データを作成します")
        # 2.1.1. 会員数のリストを作成する必要があるかを判断（ファイル名「{club_name}_申請{application_date}_会員数詳細データ.xlsx」の申請日時と同じなら作成しない）
        club_member_count_file_name = f"{club_name}_申請{application_date}_会員数詳細データ.xlsx"
        club_member_count_file_path = os.path.join(club_detail_data_folder_path, club_member_count_file_name)
        if not os.path.exists(club_member_count_file_path):
            # 2.1.2. 会員数のリストを作成
            detailed_member_columns = {
                '未就学児':   {'男性': '申請_会員_未就_男_数', '女性': '申請_会員_未就_女_数', '性別不明': '申請_会員_未就_不_数'},
                '小学生':     {'男性': '申請_会員_小_男_数',   '女性': '申請_会員_小_女_数',   '性別不明': '申請_会員_小_不_数'},
                '中学生':     {'男性': '申請_会員_中_男_数',   '女性': '申請_会員_中_女_数',   '性別不明': '申請_会員_中_不_数'},
                '高校生':     {'男性': '申請_会員_高_男_数',   '女性': '申請_会員_高_女_数',   '性別不明': '申請_会員_高_不_数'},
                '20代':      {'男性': '申請_会員_20s_男_数',  '女性': '申請_会員_20s_女_数',  '性別不明': '申請_会員_20s_不_数'},
                '30代':      {'男性': '申請_会員_30s_男_数',  '女性': '申請_会員_30s_女_数',  '性別不明': '申請_会員_30s_不_数'},
                '40代':      {'男性': '申請_会員_40s_男_数',  '女性': '申請_会員_40s_女_数',  '性別不明': '申請_会員_40s_不_数'},
                '50代':      {'男性': '申請_会員_50s_男_数',  '女性': '申請_会員_50s_女_数',  '性別不明': '申請_会員_50s_不_数'},
                '60代':      {'男性': '申請_会員_60s_男_数',  '女性': '申請_会員_60s_女_数',  '性別不明': '申請_会員_60s_不_数'},
                '70代以上':   {'男性': '申請_会員_70s_男_数',  '女性': '申請_会員_70s_女_数',  '性別不明': '申請_会員_70s_不_数'},
                }
            genders = ['男性', '女性', '性別不明']
            ages = ['未就学児', '小学生', '中学生', '高校生', '20代', '30代', '40代', '50代', '60代', '70代以上']
            detailed_member_df = []
            for gender in genders:
                row_gender = {'性別': gender}
                for age in ages:
                    col_name = detailed_member_columns[age][gender]
                    value = 0
                    if col_name in club_reception_df and not pd.isna(club_reception_df[col_name]):
                        try:
                            value = int(club_reception_df[col_name])
                        except ValueError:
                            pass
                    row_gender[age] = value
                detailed_member_df.append(row_gender)
            detailed_member_df = pd.DataFrame(detailed_member_df)
            # 2.1.3. 会員数のリストを保存
            detailed_member_df.to_excel(club_member_count_file_path, index=False)
            logging.info(f"クラブ名: {club_name} の会員数の詳細データを保存しました: {club_member_count_file_path}")
        else:
            logging.info(f"クラブ名: {club_name} の会員数の詳細データは既に存在します: {club_member_count_file_path}")
        
        # 2.2. 年会費を支払っている会員数のリストを作成
        logging.info(f"クラブ名: {club_name} の年会費を支払っている会員数の詳細データを作成します")
        # 2.2.1. 年会費を支払っている会員数のリストを作成する必要があるかを判断（ファイル名「{club_name}_申請{application_date}_年会費支払会員数詳細データ.xlsx」の申請日時と同じなら作成しない）
        club_membership_fee_file_name = f"{club_name}_申請{application_date}_年会費支払会員数詳細データ.xlsx"
        club_membership_fee_file_path = os.path.join(club_detail_data_folder_path, club_membership_fee_file_name)
        if not os.path.exists(club_membership_fee_file_path):
            # 2.2.2. 年会費を支払っている会員数のリストを作成
            detailed_annual_fee_members_columns = {
                '未就学児':   {'男性': '申請_年会_未就_男_数', '女性': '申請_年会_未就_女_数', '性別不明': '申請_年会_未就_不_数'},
                '小学生':     {'男性': '申請_年会_小_男_数',   '女性': '申請_年会_小_女_数',   '性別不明': '申請_年会_小_不_数'},
                '中学生':     {'男性': '申請_年会_中_男_数',   '女性': '申請_年会_中_女_数',   '性別不明': '申請_年会_中_不_数'},
                '高校生':     {'男性': '申請_年会_高_男_数',   '女性': '申請_年会_高_女_数',   '性別不明': '申請_年会_高_不_数'},
                '20代':      {'男性': '申請_年会_20s_男_数',  '女性': '申請_年会_20s_女_数',  '性別不明': '申請_年会_20s_不_数'},
                '30代':      {'男性': '申請_年会_30s_男_数',  '女性': '申請_年会_30s_女_数',  '性別不明': '申請_年会_30s_不_数'},
                '40代':      {'男性': '申請_年会_40s_男_数',  '女性': '申請_年会_40s_女_数',  '性別不明': '申請_年会_40s_不_数'},
                '50代':      {'男性': '申請_年会_50s_男_数',  '女性': '申請_年会_50s_女_数',  '性別不明': '申請_年会_50s_不_数'},
                '60代':      {'男性': '申請_年会_60s_男_数',  '女性': '申請_年会_60s_女_数',  '性別不明': '申請_年会_60s_不_数'},
                '70代以上':   {'男性': '申請_年会_70s_男_数',  '女性': '申請_年会_70s_女_数',  '性別不明': '申請_年会_70s_不_数'},
                }
            genders = ['男性', '女性', '性別不明']
            ages = ['未就学児', '小学生', '中学生', '高校生', '20代', '30代', '40代', '50代', '60代', '70代以上']

            detailed_annual_fee_members_df = []
            for gender in genders:
                row_gender = {'性別': gender}
                for age in ages:
                    col_name = detailed_annual_fee_members_columns[age][gender]
                    value = 0
                    if col_name in club_data.columns and not pd.isna(club_data[col_name].iloc[0]):
                        try:
                            value = int(club_data[col_name].iloc[0])
                        except ValueError:
                            pass
                    row_gender[age] = value
                detailed_annual_fee_members_df.append(row_gender)
            detailed_annual_fee_members_df = pd.DataFrame(detailed_annual_fee_members_df)
            # 2.2.3. 年会費を支払っている会員数のリストを保存
            detailed_annual_fee_members_df.to_excel(club_membership_fee_file_path, index=False)
            logging.info(f"クラブ名: {club_name} の年会費を支払っている会員数の詳細データを保存しました: {club_membership_fee_file_path}")
        else:
            logging.info(f"クラブ名: {club_name} の年会費を支払っている会員数の詳細データは既に存在します: {club_membership_fee_file_path}")
        
        # 2.3. 種目のリストを作成
        logging.info(f"クラブ名: {club_name} の種目の詳細データを作成します")
        # 2.3.1. 種目のリストを作成する必要があるかを判断（ファイル名「{club_name}_申請{application_date}_種目詳細データ.xlsx」の申請日時と同じなら作成しない）
        club_disciplines_file_name = f"{club_name}_申請{application_date}_種目詳細データ.xlsx"
        club_disciplines_file_path = os.path.join(club_detail_data_folder_path, club_disciplines_file_name)
        if not os.path.exists(club_disciplines_file_path):
            # 2.3.2. 種目のリストを作成
            detailed_disciplines_df = []
            for discipline in disciplines:
                row_dict = {}
                row_dict['種目'] = discipline

                # 実施有無
                col_name = f'申請_種目_{discipline}'
                if col_name in club_reception_df:
                    # 例: '定期的に行っている' など
                    row_dict['実施有無'] = club_reception_df[col_name]
                else:
                    row_dict['実施有無'] = ''
                detailed_disciplines_df.append(row_dict)
                    # 「その他」種目の追加
            # 「その他」種目の行を追加
            other_rows = {'申請_種目_その他': club_reception_df['申請_種目_その他'].iloc[0],
                          '申請_種目_その他_数(選択時必須)': club_reception_df['申請_種目_その他_数(選択時必須)'].iloc[0],
                          '申請_種目_その他_テキスト(選択時必須)': club_reception_df['申請_種目_その他_テキスト(選択時必須)'].iloc[0]}
            detailed_disciplines_df.append(other_rows)
            # 種目数のカウント（row_dict['実施有無']が「実施している」の数と'申請_種目_その他_数(選択時必須)'の数値を合計）
            total_discipline_count = sum(1 for row in detailed_disciplines_df if row.get('実施有無') == '実施している')
            if '申請_種目_その他_数(選択時必須)' in club_reception_df.columns:
                try:
                    other_count = int(club_reception_df['申請_種目_その他_数(選択時必須)'].iloc[0])
                    total_discipline_count += other_count
                except ValueError:
                    logging.warning(f"クラブ名: {club_name} の「その他」種目の数値が不正です: {club_reception_df['申請_種目_その他_数(選択時必須)'].iloc[0]}")
            else:
                other_count = 0
            # 種目数のカウントを追加
            row_dict['種目数合計'] = total_discipline_count
            detailed_disciplines_df = pd.DataFrame(detailed_disciplines_df)
            # 2.3.3. 種目のリストを保存
            detailed_disciplines_df.to_excel(club_disciplines_file_path, index=False)
            logging.info(f"クラブ名: {club_name} の種目の詳細データを保存しました: {club_disciplines_file_path}")
        else:
            logging.info(f"クラブ名: {club_name} の種目の詳細データは既に存在します: {club_disciplines_file_path}")

    logging.info("全てのクラブの詳細データを処理しました")