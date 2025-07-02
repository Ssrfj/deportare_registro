def make_consistency_checklist_meeting_minutes(latest_reception_data_date):
    import os
    import pandas as pd
    import logging
    from src.core.setting_paths import content_check_folder_path, consistency_checklist_meeting_minutes_folder_path
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

    # 2. 議事録の一貫性チェックリストを作成する必要があるか確認
    logging.info("議事録の一貫性チェックリストを作成する必要があるか確認します")
    # 議事録の一貫性チェックリストが既に存在するか確認
    existing_checklist_files = [
        f for f in os.listdir(consistency_checklist_meeting_minutes_folder_path)
        if os.path.isfile(os.path.join(consistency_checklist_meeting_minutes_folder_path, f)) and
        f.startswith('議事録の一貫性チェックリスト_') and f.endswith('.xlsx')
    ]
    
    # 既存の議事録の一貫性のチェックリストで同じ受付データのものがあるか確認
    existing_checklist_files.sort(reverse=True)
    for file in existing_checklist_files:
        # ファイル名から受付日時を抽出: 議事録の一貫性チェックリスト_受付{YYYYMMDDHHMMSS}_作成{YYYYMMDDHHMMSS}.xlsx
        file_parts = file.replace('議事録の一貫性チェックリスト_受付', '').replace('.xlsx', '').split('_作成')
        if len(file_parts) >= 1:
            file_reception_date_str = file_parts[0]
            try:
                file_reception_date = pd.to_datetime(file_reception_date_str, format='%Y%m%d%H%M%S')
                if file_reception_date == pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S'):
                    logging.info(f"同じ受付データの議事録の一貫性チェックリストが既に存在します: {file}")
                    logging.info("新しいチェックリストを作成しません。")
                    return
                elif file_reception_date < pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S'):
                    logging.info(f"古い受付データの議事録の一貫性チェックリストが存在します: {file}")
                    logging.info("新しい受付データ用のチェックリストを作成します。")
                    break
            except ValueError:
                logging.warning(f"ファイル名から受付日時を解析できませんでした: {file}")
                continue

    # 3. 議事録の一貫性のチェックリストのカラム名を取得
    logging.info("議事録の一貫性のチェックリストのカラム名を取得します")
    # jsonファイルを読み込む（consistency_checklist_meeting_minutes_columns.jsonが必要）
    consistency_checklist_meeting_minutes_columns_file_name = 'consistency_checklist_meeting_minutes_columns.json'
    consistency_checklist_meeting_minutes_columns_file_path = get_config_file_path(f'checklist_columns/{consistency_checklist_meeting_minutes_columns_file_name}')
    if not os.path.exists(consistency_checklist_meeting_minutes_columns_file_path):
        logging.error(f"議事録の一貫性のチェックリストのカラム名ファイルが見つかりません: {consistency_checklist_meeting_minutes_columns_file_path}")
        return
    consistency_checklist_meeting_minutes_columns = pd.read_json(consistency_checklist_meeting_minutes_columns_file_path, orient='records')
    logging.info(f"議事録の一貫性のチェックリストのカラム名を読み込みました: {consistency_checklist_meeting_minutes_columns_file_name}")

    # 4. 議事録の一貫性のチェックリストのデータフレームを作成
    logging.info("議事録の一貫性のチェックリストのデータフレームを作成します")
    consistency_checklist_meeting_minutes_df = pd.DataFrame(columns=consistency_checklist_meeting_minutes_columns['consistency_checklist_meeting_minutes_columns'].tolist())
    logging.info("議事録の一貫性のチェックリストのデータフレームを作成しました")
    # 議事録の一貫性のチェックリストのデータフレームにクラブ情報を追加
    for index, row in club_reception_df.iterrows():
        club_name = row['クラブ名']
        consistency_checklist_meeting_minutes_df.loc[index, '申請日時'] = row['申請_タイムスタンプ']
        consistency_checklist_meeting_minutes_df.loc[index, 'クラブ名'] = club_name
        consistency_checklist_meeting_minutes_df.loc[index, '申請_法人格'] = row['申請_法人格']
        
        # 書類チェックの結果を記載するカラムを指定
        documents_check_result_columns = [
            "担当者入力_規約等_規約等の改廃意思決定機関の議事録",
            "担当者入力_規約等_事業計画の意思決定機関の議事録",
            "担当者入力_規約等_予算の意思決定機関の議事録",
            "担当者入力_規約等_事業報告の意思決定機関の議事録",
            "担当者入力_規約等_決算の意思決定機関の議事録"
        ]
        # 書類チェックの結果の初期状態は「書類未チェック」
        for col in documents_check_result_columns:
            consistency_checklist_meeting_minutes_df.loc[index, col] = '書類未チェック'
        # 受付日時のカラムはlatest_reception_data_dateを使用
        consistency_checklist_meeting_minutes_df.loc[index, '受付日時'] = pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
        # チェックリスト作成日時のカラムは現在のJST日時を使用
        consistency_checklist_meeting_minutes_df.loc[index, 'チェックリスト作成日時'] = pd.to_datetime(get_jst_now()).strftime('%Y-%m-%d %H:%M:%S')

        # チェック項目のカラムを指定
        check_columns = [
            'チェック項目_一貫性_議決権'
        ]
        # チェック項目の初期状態は「未チェック」
        for col in check_columns:
            consistency_checklist_meeting_minutes_df.loc[index, col] = '未チェック'
        # チェック項目_その他の初期状態は空文字列
        consistency_checklist_meeting_minutes_df.loc[index, 'チェック項目_その他'] = ''
        # チェック者名の初期状態は「チェックが完了していません」
        consistency_checklist_meeting_minutes_df.loc[index, 'チェック者名_一貫性_議事録'] = 'チェックが完了していません'
    logging.info("議事録の一貫性のチェックリストのデータフレームを作成しました")

    # 5. 議事録の一貫性のチェックリストのデータフレームを保存(ファイル名は「議事録の一貫性チェックリスト_受付{latest_reception_data_date}_作成{YYYYMMDDHHMMSS}.xlsx」)
    logging.info("議事録の一貫性のチェックリストのデータフレームを保存します")
    now_jst = get_jst_now()
    consistency_checklist_meeting_minutes_file_name = f'議事録の一貫性チェックリスト_受付{latest_reception_data_date}_作成{now_jst.strftime("%Y%m%d%H%M%S")}.xlsx'
    consistency_checklist_meeting_minutes_file_path = os.path.join(consistency_checklist_meeting_minutes_folder_path, consistency_checklist_meeting_minutes_file_name)
    consistency_checklist_meeting_minutes_df.to_excel(consistency_checklist_meeting_minutes_file_path, index=False)
    logging.info(f"議事録の一貫性のチェックリストのデータフレームを保存しました: {consistency_checklist_meeting_minutes_file_path}")

    # 6. 議事録の一貫性のチェックリストのファイルを保存
    logging.info("議事録の一貫性のチェックリストのファイルを保存します")
    consistency_checklist_meeting_minutes_df.to_excel(consistency_checklist_meeting_minutes_file_path, index=False)
    logging.info(f"議事録の一貫性のチェックリストのファイルを保存しました: {consistency_checklist_meeting_minutes_file_path}")