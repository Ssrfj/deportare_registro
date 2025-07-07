def make_document09_checklist(latest_reception_data_date):
    import os
    import pandas as pd
    import logging
    from src.core.setting_paths import content_check_folder_path, document09_checklist_folder_path, clubs_reception_data_path
    from src.core.utils import get_jst_now, get_config_file_path
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
    latest_reception_data_date_str = pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S').strftime('%Y%m%d%H%M%S')

    # 1. 最新のクラブ情報付き受付データファイルを取得(クラブ情報付き受付データ_受付{latest_reception_data_date_str}_*.xlsxを使用)
    logging.info("最新のクラブ情報付き受付データファイルを取得します")
    # 最新のクラブ情報付き受付データと同じ日付のファイルを取得
    if not latest_reception_data_date_str:
        logging.error("最新の受付データの日付が指定されていません")
        return    
    latest_club_reception_files = [
        f for f in os.listdir(clubs_reception_data_path)
        if os.path.isfile(os.path.join(clubs_reception_data_path, f)) and
        f.startswith(f'クラブ情報付き受付データ_受付{latest_reception_data_date_str}') and f.endswith('.xlsx')
    ]
    latest_club_reception_files.sort(reverse=True)
    if not latest_club_reception_files:
        logging.error(f"クラブ情報付き受付データファイルが見つかりません: クラブ情報付き受付データ_受付{latest_reception_data_date_str}*.xlsx")
        return
    latest_club_reception_file = latest_club_reception_files[0]
    logging.info(f"最新のクラブ情報付き受付データファイル: {latest_club_reception_file}")
    club_reception_df = pd.read_excel(os.path.join(clubs_reception_data_path, latest_club_reception_file))
    logging.info(f"最新のクラブ情報付き受付データを読み込みました: {latest_club_reception_file}")

    # 2. 書類09_のチェックリストを作成する必要があるか確認
    logging.info("書類09_のチェックリストを作成する必要があるか確認します")
    # 書類09_のチェックリストが既に存在するか確認
    existing_checklist_files = [
        f for f in os.listdir(document09_checklist_folder_path)
        if os.path.isfile(os.path.join(document09_checklist_folder_path, f)) and
        f.startswith('書類09_チェックリスト_') and f.endswith('.xlsx')
    ]
    
    # 既存の書類09_のチェックリストで同じ受付データのものがあるか確認
    existing_checklist_files.sort(reverse=True)
    for file in existing_checklist_files:
        # ファイル名から受付日時を抽出: 書類09_チェックリスト_受付{YYYYMMDDHHMMSS}_作成{YYYYMMDDHHMMSS}.xlsx
        file_parts = file.replace('書類09_チェックリスト_受付', '').replace('.xlsx', '').split('_作成')
        if len(file_parts) >= 1:
            file_reception_date_str = file_parts[0]
            try:
                file_reception_date = pd.to_datetime(file_reception_date_str, format='%Y%m%d%H%M%S')
                if file_reception_date == pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S'):
                    logging.info(f"同じ受付データの書類09_チェックリストが既に存在します: {file}")
                    logging.info("新しいチェックリストを作成しません。")
                    return
                elif file_reception_date < pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S'):
                    logging.info(f"古い受付データの書類09_チェックリストが存在します: {file}")
                    logging.info("新しい受付データ用のチェックリストを作成します。")
                    break
            except ValueError:
                logging.warning(f"ファイル名から受付日時を解析できませんでした: {file}")
                continue

    # 3. 書類09_のチェックリストのカラム名を取得
    logging.info("書類09_のチェックリストのカラム名を取得します")
    # jsonファイルを読み込む（document09_checklist_columns.jsonが必要）
    document09_checklist_columns_file_path = get_config_file_path('config/checklist_columns/document09_checklist_columns.json')
    if not os.path.exists(document09_checklist_columns_file_path):
        logging.error(f"書類09のチェックリストのカラム名ファイルが見つかりません: {document09_checklist_columns_file_path}")
        return
    document09_checklist_columns = pd.read_json(document09_checklist_columns_file_path, orient='records')
    logging.info(f"チェックリストのカラム名を読み込みました: {document09_checklist_columns_file_path}")

    # 4. 書類09のチェックリストのデータフレームを作成
    logging.info("書類09のチェックリストのデータフレームを作成します")
    document09_checklist_df = pd.DataFrame(columns=document09_checklist_columns['document09_checklist_columns'].tolist())
    logging.info("書類09のチェックリストのデータフレームを作成しました")

    # 書類09のチェックリストのデータフレームにクラブ情報を追加
    for index, row in club_reception_df.iterrows():
        club_name = row['クラブ名']
        document09_checklist_df.loc[index, '申請日時'] = row['申請_タイムスタンプ']
        document09_checklist_df.loc[index, 'クラブ名'] = club_name
        document09_checklist_df.loc[index, '申請_自己説明_書類'] = row['申請_自己説明_書類']

        # 書類チェックの結果を記載するカラムを指定
        document09_check_result_columns = [
            '書類チェック_自己説明',
        ]
        # 書類チェックの結果の初期状態は「書類未チェック」
        for col in document09_check_result_columns:
            document09_checklist_df.loc[index, col] = '書類未チェック'
        # 受付日時のカラムはlatest_reception_data_dateを使用
        document09_checklist_df.loc[index, '受付日時'] = pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
        # チェックリスト作成日時のカラムは現在のJST日時を使用
        document09_checklist_df.loc[index, 'チェックリスト作成日時'] = pd.to_datetime(get_jst_now()).strftime('%Y-%m-%d %H:%M:%S')
        # チェック項目のカラムを指定
        check_columns = [
            'チェック項目_自己説明',
        ]
        # チェック項目の初期状態は「未チェック」
        for col in check_columns:
            document09_checklist_df.loc[index, col] = '未チェック'
        # チェック項目_その他の初期状態は空文字列
        document09_checklist_df.loc[index, 'チェック項目_その他'] = ''
        # チェック者名の初期状態は「チェックが完了していません」
        document09_checklist_df.loc[index, 'チェック者名_自己説明'] = 'チェックが完了していません'
    logging.info("書類09のチェックリストのデータフレームを作成しました")

    # 5. 書類09のチェックリストのデータフレームを保存(ファイル名は「書類09チェックリスト_受付{latest_reception_data_date}_作成{YYYYMMDDHHMMSS}.xlsx」)
    logging.info("書類09のチェックリストのデータフレームを保存します")
    now_jst = get_jst_now()
    document09_checklist_file_name = f'書類09チェックリスト_受付{latest_reception_data_date_str}_作成{now_jst.strftime("%Y%m%d%H%M%S")}.xlsx'
    document09_checklist_file_path = os.path.join(document09_checklist_folder_path, document09_checklist_file_name)
    document09_checklist_df.to_excel(document09_checklist_file_path, index=False)
    logging.info(f"書類09のチェックリストのデータフレームを保存しました: {document09_checklist_file_path}")

    # 6. 書類09のチェックリストのファイルを保存
    logging.info("書類09のチェックリストのファイルを保存します")
    document09_checklist_df.to_excel(document09_checklist_file_path, index=False)
    logging.info(f"書類09のチェックリストのファイルを保存しました: {document09_checklist_file_path}")