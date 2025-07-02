def make_document10_checklist(latest_reception_data_date):
    import os
    import pandas as pd
    import logging
    from src.core.setting_paths import content_check_folder_path, document10_checklist_folder_path, clubs_reception_data_path
    from src.core.utils import get_jst_now
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
    latest_reception_data_date = pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S').strftime('%Y%m%d%H%M%S')

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
    club_reception_df = pd.read_excel(os.path.join(clubs_reception_data_path, latest_club_reception_file))
    logging.info(f"最新のクラブ情報付き受付データを読み込みました: {latest_club_reception_file}")

    # 2. 書類10_のチェックリストを作成する必要があるか確認
    logging.info("書類10_のチェックリストを作成する必要があるか確認します")
    # 書類10_のチェックリストが既に存在するか確認
    existing_checklist_files = [
        f for f in os.listdir(document10_checklist_folder_path)
        if os.path.isfile(os.path.join(document10_checklist_folder_path, f)) and
        f.startswith('書類10_チェックリスト_') and f.endswith('.xlsx')
    ]
    
    # 既存の書類10_のチェックリストで同じ受付データのものがあるか確認
    existing_checklist_files.sort(reverse=True)
    for file in existing_checklist_files:
        # ファイル名から受付日時を抽出: 書類10_チェックリスト_受付{YYYYMMDDHHMMSS}_作成{YYYYMMDDHHMMSS}.xlsx
        file_parts = file.replace('書類10_チェックリスト_受付', '').replace('.xlsx', '').split('_作成')
        if len(file_parts) >= 1:
            file_reception_date_str = file_parts[0]
            try:
                file_reception_date = pd.to_datetime(file_reception_date_str, format='%Y%m%d%H%M%S')
                if file_reception_date == pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S'):
                    logging.info(f"同じ受付データの書類10_チェックリストが既に存在します: {file}")
                    logging.info("新しいチェックリストを作成しません。")
                    return
                elif file_reception_date < pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S'):
                    logging.info(f"古い受付データの書類10_チェックリストが存在します: {file}")
                    logging.info("新しい受付データ用のチェックリストを作成します。")
                    break
            except ValueError:
                logging.warning(f"ファイル名から受付日時を解析できませんでした: {file}")
                continue

    # 3. 書類10_のチェックリストのカラム名を取得
    logging.info("書類10_のチェックリストのカラム名を取得します")
    # jsonファイルを読み込む（document10_checklist_columns.jsonが必要）
    document10_checklist_columns_file_name = 'config/checklist_columns/document10_checklist_columns.json'
    document10_checklist_columns_file_path = os.path.join(content_check_folder_path, document10_checklist_columns_file_name)
    if not os.path.exists(document10_checklist_columns_file_path):
        logging.error(f"書類10のチェックリストのカラム名ファイルが見つかりません: {document10_checklist_columns_file_path}")
        return
    document10_checklist_columns = pd.read_json(document10_checklist_columns_file_path, orient='records')
    logging.info(f"チェックリストのカラム名を読み込みました: {document10_checklist_columns_file_path}")

    # 4. 書類10のチェックリストのデータフレームを作成
    logging.info("書類10のチェックリストのデータフレームを作成します")
    document10_checklist_df = pd.DataFrame(columns=document10_checklist_columns['document10_checklist_columns'].tolist())
    logging.info("書類10のチェックリストのデータフレームを作成しました")

    # 書類10のチェックリストのデータフレームにクラブ情報を追加
    for index, row in club_reception_df.iterrows():
        club_name = row['クラブ名']
        document10_checklist_df.loc[index, '申請日時'] = row['申請_タイムスタンプ']
        document10_checklist_df.loc[index, 'クラブ名'] = club_name
        document10_checklist_df.loc[index, '申請_クラブ名_選択'] = row['申請_クラブ名_選択']
        document10_checklist_df.loc[index, '申請_届出_書類_(選択時必須)'] = row['申請_届出_書類_(選択時必須)']
        document10_checklist_df.loc[index, '申請_東京チェック'] = row['申請_東京チェック']
        document10_checklist_df.loc[index, '申請_区市町村名'] = row['申請_区市町村名']

        # 書類チェックの結果を記載するカラムを指定
        document10_check_result_columns = [
            '書類チェック_届出',
        ]
        # 書類チェックの結果の初期状態はrow['申請_クラブ名_選択']が「この中に無い」の時には「書類未チェック」、それ以外は「届出済（チェック不要）」とする
        if row['申請_クラブ名_選択'] == 'この中に無い':
            document10_checklist_df.loc[index, '書類チェック_届出'] = '書類未チェック'
        else:
            document10_checklist_df.loc[index, '書類チェック_届出'] = '届出済（チェック不要）'
        # 受付日時のカラムはlatest_reception_data_dateを使用
        document10_checklist_df.loc[index, '受付日時'] = pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
        # チェックリスト作成日時のカラムは現在のJST日時を使用
        document10_checklist_df.loc[index, 'チェックリスト作成日時'] = pd.to_datetime(get_jst_now()).strftime('%Y-%m-%d %H:%M:%S')
        # チェック項目のカラムを指定
        check_columns = [
            'チェック項目_届出',
        ]
        # チェック項目の初期状態は「未チェック」
        for col in check_columns:
            document10_checklist_df.loc[index, col] = '未チェック'
        # チェック項目_その他の初期状態は空文字列
        document10_checklist_df.loc[index, 'チェック項目_その他'] = ''
        # チェック者名の初期状態は「チェックが完了していません」
        document10_checklist_df.loc[index, 'チェック者名_届出'] = 'チェックが完了していません'
    logging.info("書類10のチェックリストのデータフレームを作成しました")

    # 5. 書類10のチェックリストのデータフレームを保存(ファイル名は「書類10チェックリスト_受付{latest_reception_data_date}_作成{YYYYMMDDHHMMSS}.xlsx」)
    logging.info("書類10のチェックリストのデータフレームを保存します")
    now_jst = get_jst_now()
    document10_checklist_file_name = f'書類10チェックリスト_受付{latest_reception_data_date}_作成{now_jst.strftime("%Y%m%d%H%M%S")}.xlsx'
    document10_checklist_file_path = os.path.join(document10_checklist_folder_path, document10_checklist_file_name)
    document10_checklist_df.to_excel(document10_checklist_file_path, index=False)
    logging.info(f"書類10のチェックリストのデータフレームを保存しました: {document10_checklist_file_path}")

    # 6. 書類10のチェックリストのファイルを保存
    logging.info("書類10のチェックリストのファイルを保存します")
    document10_checklist_df.to_excel(document10_checklist_file_path, index=False)
    logging.info(f"書類10のチェックリストのファイルを保存しました: {document10_checklist_file_path}")