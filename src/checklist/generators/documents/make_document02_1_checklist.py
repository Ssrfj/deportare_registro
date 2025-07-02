def make_document02_1_checklist(latest_reception_data_date):
    import os
    import pandas as pd
    import logging
    from src.core.setting_paths import content_check_folder_path, document02_1_checklist_folder_path, clubs_reception_data_path
    from src.core.utils import get_jst_now, ensure_date_string
    from src.folder_management.make_folders import setup_logging, create_folders

    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()
    logging.info("フォルダを作成しました")

    # 最新の受付データの日付をフォーマット
    if not latest_reception_data_date:
        logging.error("最新の受付データの日付が指定されていません")
        return
    latest_reception_data_date = ensure_date_string(latest_reception_data_date)

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

    # 2. 書類02_1_のチェックリストを作成する必要があるか確認
    logging.info("書類02_1_のチェックリストを作成する必要があるか確認します")
    # 書類02_1_のチェックリストが既に存在するか確認
    existing_checklist_files = [
        f for f in os.listdir(document02_1_checklist_folder_path)
        if os.path.isfile(os.path.join(document02_1_checklist_folder_path, f)) and
        f.startswith('書類02_1_チェックリスト_') and f.endswith('.xlsx')
    ]
    
    # 既存の書類02_1_のチェックリストで同じ受付データのものがあるか確認
    existing_checklist_files.sort(reverse=True)
    for file in existing_checklist_files:
        # ファイル名から受付日時を抽出: 書類02_1_チェックリスト_受付{YYYYMMDDHHMMSS}_作成{YYYYMMDDHHMMSS}.xlsx
        file_parts = file.replace('書類02_1_チェックリスト_受付', '').replace('.xlsx', '').split('_作成')
        if len(file_parts) >= 1:
            file_reception_date_str = file_parts[0]
            try:
                file_reception_date = pd.to_datetime(file_reception_date_str, format='%Y%m%d%H%M%S')
                if file_reception_date == pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S'):
                    logging.info(f"同じ受付データの書類02_1_チェックリストが既に存在します: {file}")
                    logging.info("新しいチェックリストを作成しません。")
                    return
                elif file_reception_date < pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S'):
                    logging.info(f"古い受付データの書類02_1_チェックリストが存在します: {file}")
                    logging.info("新しい受付データ用のチェックリストを作成します。")
                    break
            except ValueError:
                logging.warning(f"ファイル名から受付日時を解析できませんでした: {file}")
                continue

    # 3. 書類02_1_のチェックリストのカラム名を取得
    logging.info("書類02_1_のチェックリストのカラム名を取得します")
    # jsonファイルを読み込む（document02_1_checklist_columns.jsonが必要）
    from src.core.utils import get_config_file_path
    document02_1_checklist_columns_file_path = get_config_file_path('config/checklist_columns/document02_1_checklist_columns.json')
    if not os.path.exists(document02_1_checklist_columns_file_path):
        logging.error(f"書類02_1のチェックリストのカラム名ファイルが見つかりません: {document02_1_checklist_columns_file_path}")
        return
    document02_1_checklist_columns = pd.read_json(document02_1_checklist_columns_file_path, orient='records')
    logging.info(f"チェックリストのカラム名を読み込みました: {document02_1_checklist_columns_file_path}")

    # 4. 書類02_1のチェックリストのデータフレームを作成
    logging.info("書類02_1のチェックリストのデータフレームを作成します")
    document02_1_checklist_df = pd.DataFrame(columns=document02_1_checklist_columns['document02_1_checklist_columns'].tolist())
    logging.info("書類02_1のチェックリストのデータフレームを作成しました")
    # 書類02_1のチェックリストのデータフレームにクラブ情報を追加
    for index, row in club_reception_df.iterrows():
        club_name = row['クラブ名']
        document02_1_checklist_df.loc[index, '申請日時'] = row['申請_タイムスタンプ']
        document02_1_checklist_df.loc[index, 'クラブ名'] = club_name
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
        document02_1_checklist_df.loc[index, '会員数の合計'] = number_of_members
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
        document02_1_checklist_df.loc[index, '年会費を払っている会員数の合計'] = number_of_annual_fee_members
        # 受付日時のカラムはlatest_reception_data_dateを使用
        document02_1_checklist_df.loc[index, '受付日時'] = pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
        # チェックリスト作成日時のカラムは現在のJST日時を使用
        document02_1_checklist_df.loc[index, 'チェックリスト作成日時'] = pd.to_datetime(get_jst_now()).strftime('%Y-%m-%d %H:%M:%S')
        # チェック項目のカラムを指定
        check_columns = [
            'チェック項目_会員数',
        ]
        # チェック項目の初期状態は「未チェック」
        for col in check_columns:
            document02_1_checklist_df.loc[index, col] = '未チェック'
        # チェック項目_その他の初期状態は空文字列
        document02_1_checklist_df.loc[index, 'チェック項目_その他'] = ''
        # チェック者名の初期状態は「チェックが完了していません」
        document02_1_checklist_df.loc[index, 'チェック者名_会員数'] = 'チェックが完了していません'
    logging.info("書類02_1のチェックリストのデータフレームを作成しました")

    # 5. 書類02_1のチェックリストのデータフレームを保存(ファイル名は「書類02_1チェックリスト_受付{latest_reception_data_date}_作成{YYYYMMDDHHMMSS}.xlsx」)
    logging.info("書類02_1のチェックリストのデータフレームを保存します")
    now_jst = get_jst_now()
    document02_1_checklist_file_name = f'書類02_1チェックリスト_受付{latest_reception_data_date}_作成{now_jst.strftime("%Y%m%d%H%M%S")}.xlsx'
    document02_1_checklist_file_path = os.path.join(document02_1_checklist_folder_path, document02_1_checklist_file_name)
    document02_1_checklist_df.to_excel(document02_1_checklist_file_path, index=False)
    logging.info(f"書類02_1のチェックリストのデータフレームを保存しました: {document02_1_checklist_file_path}")

    # 6. 書類02_1のチェックリストのファイルを保存
    logging.info("書類02_1のチェックリストのファイルを保存します")
    document02_1_checklist_df.to_excel(document02_1_checklist_file_path, index=False)
    logging.info(f"書類02_1のチェックリストのファイルを保存しました: {document02_1_checklist_file_path}")