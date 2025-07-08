def make_consistency_checklist_members_and_voting_rights(latest_reception_data_date):
    import os
    import pandas as pd
    import logging
    from src.core.setting_paths import consistency_checklist_members_and_voting_rights_folder_path, clubs_reception_data_path
    from src.core.utils import get_jst_now, get_config_file_path
    
    # ロギングの設定    logging.info("ロギングを設定しました")
    # フォルダの作成    logging.info("フォルダを作成しました")

    # 1. 最新のクラブ情報付き受付データファイルを取得(クラブ情報付き受付データ_受付{latest_reception_data_date}_*.xlsxを使用)
    logging.info("最新のクラブ情報付き受付データファイルを取得します")
    # 最新のクラブ情報付き受付データと同じ日付のファイルを取得
    if not latest_reception_data_date:
        logging.error("最新の受付データの日付が指定されていません")
        return    
    latest_club_reception_files = [
        f for f in os.listdir(clubs_reception_data_path)
        if os.path.isfile(os.path.join(clubs_reception_data_path, f)) and
        f.startswith(f'クラブ情報付き受付データ_受付{latest_reception_data_date}') and f.endswith('.xlsx')
    ]
    latest_club_reception_files.sort(reverse=True)
    if not latest_club_reception_files:
        logging.error(f"クラブ情報付き受付データファイルが見つかりません: クラブ情報付き受付データ_受付{latest_reception_data_date}*.xlsx")
        return
    latest_club_reception_file = latest_club_reception_files[0]
    logging.info(f"最新のクラブ情報付き受付データファイル: {latest_club_reception_file}")
    club_reception_df = pd.read_excel(os.path.join(clubs_reception_data_path, latest_club_reception_file))
    logging.info(f"最新のクラブ情報付き受付データを読み込みました: {latest_club_reception_file}")

    # 2. 会員と議決権保有者の一貫性チェックリストを作成する必要があるか確認
    logging.info("会員と議決権保有者の一貫性チェックリストを作成する必要があるか確認します")
    # 会員と議決権保有者の一貫性チェックリストが既に存在するか確認
    existing_checklist_files = [
        f for f in os.listdir(consistency_checklist_members_and_voting_rights_folder_path)
        if os.path.isfile(os.path.join(consistency_checklist_members_and_voting_rights_folder_path, f)) and
        f.startswith('会員と議決権保有者の一貫性チェックリスト_') and f.endswith('.xlsx')
    ]
    
    # 既存の会員と議決権保有者の一貫性のチェックリストで同じ受付データのものがあるか確認
    existing_checklist_files.sort(reverse=True)
    for file in existing_checklist_files:
        # ファイル名から受付日時を抽出: 会員と議決権保有者の一貫性チェックリスト_受付{YYYYMMDDHHMMSS}_作成{YYYYMMDDHHMMSS}.xlsx
        file_parts = file.replace('会員と議決権保有者の一貫性チェックリスト_受付', '').replace('.xlsx', '').split('_作成')
        if len(file_parts) >= 1:
            file_reception_date_str = file_parts[0]
            try:
                file_reception_date = pd.to_datetime(file_reception_date_str, format='%Y%m%d%H%M%S')
                if file_reception_date == pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S'):
                    logging.info(f"同じ受付データの会員と議決権保有者の一貫性チェックリストが既に存在します: {file}")
                    logging.info("新しいチェックリストを作成しません。")
                    return
                elif file_reception_date < pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S'):
                    logging.info(f"古い受付データの会員と議決権保有者の一貫性チェックリストが存在します: {file}")
                    logging.info("新しい受付データ用のチェックリストを作成します。")
                    break
            except ValueError:
                logging.warning(f"ファイル名から受付日時を解析できませんでした: {file}")
                continue

    # 3. 会員と議決権保有者の一貫性のチェックリストのカラム名を取得
    logging.info("会員と議決権保有者の一貫性のチェックリストのカラム名を取得します")
    # jsonファイルを読み込む（consistency_checklist_members_and_voting_rights_columns.jsonが必要）
    consistency_checklist_members_and_voting_rights_columns_file_name = 'consistency_checklist_members_and_voting_rights_columns.json'
    consistency_checklist_members_and_voting_rights_columns_file_path = get_config_file_path(f'config/checklist_columns/{consistency_checklist_members_and_voting_rights_columns_file_name}')
    if not os.path.exists(consistency_checklist_members_and_voting_rights_columns_file_path):
        logging.error(f"会員と議決権保有者の一貫性のチェックリストのカラム名ファイルが見つかりません: {consistency_checklist_members_and_voting_rights_columns_file_path}")
        return
    consistency_checklist_members_and_voting_rights_columns = pd.read_json(consistency_checklist_members_and_voting_rights_columns_file_path, orient='records')
    logging.info(f"会員と議決権保有者の一貫性のチェックリストのカラム名を読み込みました: {consistency_checklist_members_and_voting_rights_columns_file_name}")

    # 4. 会員と議決権保有者の一貫性のチェックリストのデータフレームを作成
    logging.info("会員と議決権保有者の一貫性のチェックリストのデータフレームを作成します")
    consistency_checklist_members_and_voting_rights_df = pd.DataFrame(columns=consistency_checklist_members_and_voting_rights_columns['consistency_checklist_members_and_voting_rights_columns'].tolist())
    logging.info("会員と議決権保有者の一貫性のチェックリストのデータフレームを作成しました")
    # 会員と議決権保有者の一貫性のチェックリストのデータフレームにクラブ情報を追加
    for index, row in club_reception_df.iterrows():
        club_name = row['クラブ名']
        consistency_checklist_members_and_voting_rights_df.loc[index, '申請日時'] = row['申請_タイムスタンプ']
        consistency_checklist_members_and_voting_rights_df.loc[index, 'クラブ名'] = club_name
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
        consistency_checklist_members_and_voting_rights_df.loc[index, '会員数の合計'] = number_of_members

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
        consistency_checklist_members_and_voting_rights_df.loc[index, '年会費を払っている会員数の合計'] = number_of_annual_fee_members
        consistency_checklist_members_and_voting_rights_df.loc[index, '申請_法人格'] = row['申請_法人格']
        
        # 書類チェックの結果を記載するカラムを指定
        documents_check_result_columns = [
            "担当者入力_規約等_法人格",
            "担当者入力_規約等_会員資格",
            "担当者入力_規約等_規約等の改廃意思決定機関の議決権保有者",
            "担当者入力_規約等_事業計画の意思決定機関の議決権保有者",
            "担当者入力_規約等_予算の意思決定機関の議決権保有者",
            "担当者入力_規約等_事業報告の意思決定機関の議決権保有者",
            "担当者入力_規約等_決算の意思決定機関の議決権保有者",
            "担当者入力_議決権保有者名簿1_構成員",
            "担当者入力_議決権保有者名簿1_記載人数",
            "担当者入力_議決権保有者名簿2_構成員",
            "担当者入力_議決権保有者名簿2_記載人数",
            "担当者入力_議決権保有者名簿3_構成員",
            "担当者入力_議決権保有者名簿3_記載人数",
            "担当者入力_議決権保有者名簿4_構成員",
            "担当者入力_議決権保有者名簿4_記載人数",
            "担当者入力_議決権保有者名簿5_構成員",
            "担当者入力_議決権保有者名簿5_記載人数",
            "担当者入力_予算_会費の会員数",
            "担当者入力_決算_会費の会員数",      
            "書類チェック_議事録_規約等_議決権保有者数",
            "書類チェック_議事録_規約等_議決権行使者数",
            "書類チェック_議事録_事業計画_議決権保有者数",
            "書類チェック_議事録_事業計画_議決権行使者数",
            "書類チェック_議事録_予算_議決権保有者数",
            "書類チェック_議事録_予算_議決権行使者数",
            "書類チェック_議事録_事業報告_議決権保有者数",
            "書類チェック_議事録_事業報告_議決権行使者数",
            "書類チェック_議事録_決算_議決権保有者数",
            "書類チェック_議事録_決算_議決権行使者数"
        ]
        # 書類チェックの結果の初期状態は「書類未チェック」
        for col in documents_check_result_columns:
            consistency_checklist_members_and_voting_rights_df.loc[index, col] = '書類未チェック'
        # 受付日時のカラムはlatest_reception_data_dateを使用
        consistency_checklist_members_and_voting_rights_df.loc[index, '受付日時'] = pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
        # チェックリスト作成日時のカラムは現在のJST日時を使用
        consistency_checklist_members_and_voting_rights_df.loc[index, 'チェックリスト作成日時'] = pd.to_datetime(get_jst_now()).strftime('%Y-%m-%d %H:%M:%S')

        # チェック項目のカラムを指定
        check_columns = [
            'チェック項目_会員',
            'チェック項目_議決権保有者'
        ]
        # チェック項目の初期状態は「未チェック」
        for col in check_columns:
            consistency_checklist_members_and_voting_rights_df.loc[index, col] = '未チェック'
        # チェック項目_その他の初期状態は空文字列
        consistency_checklist_members_and_voting_rights_df.loc[index, 'チェック項目_その他'] = ''
        # チェック者名の初期状態は「チェックが完了していません」
        consistency_checklist_members_and_voting_rights_df.loc[index, 'チェック者名_一貫性_会員と議決権保有者'] = 'チェックが完了していません'
    logging.info("会員と議決権保有者の一貫性のチェックリストのデータフレームを作成しました")

    # 5. 会員と議決権保有者の一貫性のチェックリストのデータフレームを保存(ファイル名は「会員と議決権保有者の一貫性チェックリスト_受付{latest_reception_data_date}_作成{YYYYMMDDHHMMSS}.xlsx」)
    logging.info("会員と議決権保有者の一貫性のチェックリストのデータフレームを保存します")
    now_jst = get_jst_now()
    consistency_checklist_members_and_voting_rights_file_name = f'会員と議決権保有者の一貫性チェックリスト_受付{latest_reception_data_date}_作成{now_jst.strftime("%Y%m%d%H%M%S")}.xlsx'
    consistency_checklist_members_and_voting_rights_file_path = os.path.join(consistency_checklist_members_and_voting_rights_folder_path, consistency_checklist_members_and_voting_rights_file_name)
    consistency_checklist_members_and_voting_rights_df.to_excel(consistency_checklist_members_and_voting_rights_file_path, index=False)
    logging.info(f"会員と議決権保有者の一貫性のチェックリストのデータフレームを保存しました: {consistency_checklist_members_and_voting_rights_file_path}")

    # 6. 会員と議決権保有者の一貫性のチェックリストのファイルを保存
    logging.info("会員と議決権保有者の一貫性のチェックリストのファイルを保存します")
    consistency_checklist_members_and_voting_rights_df.to_excel(consistency_checklist_members_and_voting_rights_file_path, index=False)
    logging.info(f"会員と議決権保有者の一貫性のチェックリストのファイルを保存しました: {consistency_checklist_members_and_voting_rights_file_path}")
