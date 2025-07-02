def make_consistency_checklist_disciplines(latest_reception_data_date):
    import os
    import pandas as pd
    import logging
    from src.core.setting_paths import content_check_folder_path, consistency_checklist_disciplines_folder_path
    from src.core.utils import get_jst_now, get_config_file_path
    from src.folder_management.make_folders import setup_logging, create_folders

    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()
    logging.info("フォルダを作成しました")

    # 1. 最新のクラブ情報付き受付データファイルを取得(クラブ情報付き受付データ_受付{latest_reception_data_date}_*.xlsxを使用)
    logging.info("最新のクラブ情報付き受付データファイルを取得します")
    # 最新のクラブ情報付き受付データと同じ日付のファイルを取得
    if not latest_reception_data_date:
        logging.error("最新の受付データの日付が指定されていません")
        return    
    latest_club_reception_files = [
        f for f in os.listdir(content_check_folder_path)
        if os.path.isfile(os.path.join(content_check_folder_path, f)) and
        f.startswith(f'クラブ情報付き受付データ_受付{latest_reception_data_date}') and f.endswith('.xlsx')
    ]
    latest_club_reception_files.sort(reverse=True)
    if not latest_club_reception_files:
        logging.error(f"クラブ情報付き受付データファイルが見つかりません: クラブ情報付き受付データ_受付{latest_reception_data_date}*.xlsx")
        return
    latest_club_reception_file = latest_club_reception_files[0]
    logging.info(f"最新のクラブ情報付き受付データファイル: {latest_club_reception_file}")
    club_reception_df = pd.read_excel(os.path.join(content_check_folder_path, latest_club_reception_file))
    logging.info(f"最新のクラブ情報付き受付データを読み込みました: {latest_club_reception_file}")

    # 2. 活動種目の一貫性チェックリストを作成する必要があるか確認
    logging.info("活動種目の一貫性チェックリストを作成する必要があるか確認します")
    # 活動種目の一貫性チェックリストが既に存在するか確認
    existing_checklist_files = [
        f for f in os.listdir(consistency_checklist_disciplines_folder_path)
        if os.path.isfile(os.path.join(consistency_checklist_disciplines_folder_path, f)) and
        f.startswith('活動種目の一貫性チェックリスト_') and f.endswith('.xlsx')
    ]
    
    # 既存の活動種目の一貫性のチェックリストで同じ受付データのものがあるか確認
    existing_checklist_files.sort(reverse=True)
    for file in existing_checklist_files:
        # ファイル名から受付日時を抽出: 活動種目の一貫性チェックリスト_受付{YYYYMMDDHHMMSS}_作成{YYYYMMDDHHMMSS}.xlsx
        file_parts = file.replace('活動種目の一貫性チェックリスト_受付', '').replace('.xlsx', '').split('_作成')
        if len(file_parts) >= 1:
            file_reception_date_str = file_parts[0]
            try:
                file_reception_date = pd.to_datetime(file_reception_date_str, format='%Y%m%d%H%M%S')
                if file_reception_date == pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S'):
                    logging.info(f"同じ受付データの活動種目の一貫性チェックリストが既に存在します: {file}")
                    logging.info("新しいチェックリストを作成しません。")
                    return
                elif file_reception_date < pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S'):
                    logging.info(f"古い受付データの活動種目の一貫性チェックリストが存在します: {file}")
                    logging.info("新しい受付データ用のチェックリストを作成します。")
                    break
            except ValueError:
                logging.warning(f"ファイル名から受付日時を解析できませんでした: {file}")
                continue

    # 3. 活動種目の一貫性のチェックリストのカラム名を取得
    logging.info("活動種目の一貫性のチェックリストのカラム名を取得します")
    # jsonファイルを読み込む（consistency_checklist_disciplines_columns.jsonが必要）
    consistency_checklist_disciplines_columns_file_name = 'consistency_checklist_disciplines_columns.json'
    consistency_checklist_disciplines_columns_file_path = get_config_file_path(f'checklist_columns/{consistency_checklist_disciplines_columns_file_name}')
    if not os.path.exists(consistency_checklist_disciplines_columns_file_path):
        logging.error(f"活動種目の一貫性のチェックリストのカラム名ファイルが見つかりません: {consistency_checklist_disciplines_columns_file_path}")
        return
    consistency_checklist_disciplines_columns = pd.read_json(consistency_checklist_disciplines_columns_file_path, orient='records')
    logging.info(f"活動種目の一貫性のチェックリストのカラム名を読み込みました: {consistency_checklist_disciplines_columns_file_name}")

    # 4. 活動種目の一貫性のチェックリストのデータフレームを作成
    logging.info("活動種目の一貫性のチェックリストのデータフレームを作成します")
    consistency_checklist_disciplines_df = pd.DataFrame(columns=consistency_checklist_disciplines_columns['consistency_checklist_disciplines_columns'].tolist())
    logging.info("活動種目の一貫性のチェックリストのデータフレームを作成しました")
    # 活動種目の一貫性のチェックリストのデータフレームにクラブ情報を追加
    for index, row in club_reception_df.iterrows():
        club_name = row['クラブ名']
        consistency_checklist_disciplines_df.loc[index, '申請日時'] = row['申請_タイムスタンプ']
        consistency_checklist_disciplines_df.loc[index, 'クラブ名'] = club_name
        
        
        # 書類チェックの結果を記載するカラムを指定
        automatic_check_result_columns = [
            "自動_チェック項目_活動種目_02_2_計画",
            "自動_チェック項目_活動種目_02_2_報告",
            "自動_チェック項目_活動種目_計画_報告"
        ]
        # 書類チェックの結果の初期状態は「書類未チェック」
        for col in automatic_check_result_columns:
            consistency_checklist_disciplines_df.loc[index, col] = '書類未チェック'
        # 受付日時のカラムはlatest_reception_data_dateを使用
        consistency_checklist_disciplines_df.loc[index, '受付日時'] = pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
        # チェックリスト作成日時のカラムは現在のJST日時を使用
        consistency_checklist_disciplines_df.loc[index, 'チェックリスト作成日時'] = pd.to_datetime(get_jst_now()).strftime('%Y-%m-%d %H:%M:%S')

        # チェック項目のカラムを指定
        check_columns = [
            'チェック項目_活動種目'
        ]
        # チェック項目の初期状態は「未チェック」
        for col in check_columns:
            consistency_checklist_disciplines_df.loc[index, col] = '未チェック'
        # チェック項目_その他の初期状態は空文字列
        consistency_checklist_disciplines_df.loc[index, 'チェック項目_その他'] = ''
        # チェック者名の初期状態は「チェックが完了していません」
        consistency_checklist_disciplines_df.loc[index, 'チェック者名_一貫性_活動種目'] = 'チェックが完了していません'
    logging.info("活動種目の一貫性のチェックリストのデータフレームを作成しました")

    # 5. 活動種目の一貫性のチェックリストのデータフレームを保存(ファイル名は「活動種目の一貫性チェックリスト_受付{latest_reception_data_date}_作成{YYYYMMDDHHMMSS}.xlsx」)
    logging.info("活動種目の一貫性のチェックリストのデータフレームを保存します")
    now_jst = get_jst_now()
    consistency_checklist_disciplines_file_name = f'活動種目の一貫性チェックリスト_受付{latest_reception_data_date}_作成{now_jst.strftime("%Y%m%d%H%M%S")}.xlsx'
    consistency_checklist_disciplines_file_path = os.path.join(consistency_checklist_disciplines_folder_path, consistency_checklist_disciplines_file_name)
    consistency_checklist_disciplines_df.to_excel(consistency_checklist_disciplines_file_path, index=False)
    logging.info(f"活動種目の一貫性のチェックリストのデータフレームを保存しました: {consistency_checklist_disciplines_file_path}")

    # 6. 活動種目の一貫性のチェックリストのファイルを保存
    logging.info("活動種目の一貫性のチェックリストのファイルを保存します")
    consistency_checklist_disciplines_df.to_excel(consistency_checklist_disciplines_file_path, index=False)
    logging.info(f"活動種目の一貫性のチェックリストのファイルを保存しました: {consistency_checklist_disciplines_file_path}")