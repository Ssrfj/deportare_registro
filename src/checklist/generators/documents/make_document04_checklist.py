def make_document04_checklist(latest_reception_data_date):
    import os
    import pandas as pd
    import logging
    from src.core.setting_paths import content_check_folder_path, document04_checklist_folder_path, clubs_reception_data_path
    from src.core.utils import get_jst_now, ensure_date_string
    from src.folder_management.make_folders import setup_logging, create_folders

    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()
    logging.info("フォルダを作成しました")

    # 受付データの日付を正規化
    latest_reception_data_date_str = ensure_date_string(latest_reception_data_date)
    logging.info(f"受付データの日付: {latest_reception_data_date_str}")

    # 1. 最新のクラブ情報付き受付データファイルを取得
    logging.info("最新のクラブ情報付き受付データファイルを取得します")
    
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

    # 2. 書類04_のチェックリストを作成する必要があるか確認
    logging.info("書類04_のチェックリストを作成する必要があるか確認します")
    # 書類04_のチェックリストが既に存在するか確認
    existing_checklist_files = [
        f for f in os.listdir(document04_checklist_folder_path)
        if os.path.isfile(os.path.join(document04_checklist_folder_path, f)) and
        f.startswith('書類04_チェックリスト_') and f.endswith('.xlsx')
    ]
    
    # 既存の書類04_のチェックリストで同じ受付データのものがあるか確認
    existing_checklist_files.sort(reverse=True)
    for file in existing_checklist_files:
        # ファイル名から受付日時を抽出: 書類04_チェックリスト_受付{YYYYMMDDHHMMSS}_作成{YYYYMMDDHHMMSS}.xlsx
        file_parts = file.replace('書類04_チェックリスト_受付', '').replace('.xlsx', '').split('_作成')
        if len(file_parts) >= 1:
            file_reception_date_str = file_parts[0]
            try:
                file_reception_date = pd.to_datetime(file_reception_date_str, format='%Y%m%d%H%M%S')
                if file_reception_date == pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S'):
                    logging.info(f"同じ受付データの書類04_チェックリストが既に存在します: {file}")
                    logging.info("新しいチェックリストを作成しません。")
                    return
                elif file_reception_date < pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S'):
                    logging.info(f"古い受付データの書類04_チェックリストが存在します: {file}")
                    logging.info("新しい受付データ用のチェックリストを作成します。")
                    break
            except ValueError:
                logging.warning(f"ファイル名から受付日時を解析できませんでした: {file}")
                continue

    # 3. 書類04_のチェックリストのカラム名を取得
    logging.info("書類04_のチェックリストのカラム名を取得します")
    # jsonファイルを読み込む（document04_checklist_columns.jsonが必要）
    document04_checklist_columns_file_name = 'config/checklist_columns/document04_checklist_columns.json'
    document04_checklist_columns_file_path = os.path.join(content_check_folder_path, document04_checklist_columns_file_name)
    if not os.path.exists(document04_checklist_columns_file_path):
        logging.error(f"書類04のチェックリストのカラム名ファイルが見つかりません: {document04_checklist_columns_file_path}")
        return
    document04_checklist_columns = pd.read_json(document04_checklist_columns_file_path, orient='records')
    logging.info(f"チェックリストのカラム名を読み込みました: {document04_checklist_columns_file_path}")

    # 4. 書類04のチェックリストのデータフレームを作成
    logging.info("書類04のチェックリストのデータフレームを作成します")
    document04_checklist_df = pd.DataFrame(columns=document04_checklist_columns['document04_checklist_columns'].tolist())
    logging.info("書類04のチェックリストのデータフレームを作成しました")
    # 書類04のチェックリストのデータフレームにクラブ情報を追加
    for index, row in club_reception_df.iterrows():
        club_name = row['クラブ名']
        document04_checklist_df.loc[index, '申請日時'] = row['申請_タイムスタンプ']
        document04_checklist_df.loc[index, 'クラブ名'] = club_name
        document04_checklist_df.loc[index, '地区名'] = row['地区名']
        # 書類チェックの結果を記載するカラムを指定
        document04_check_result_columns = [
            '担当者入力_議決権保有者名簿1_種類',
            '担当者入力_議決権保有者名簿1_構成員',
            '担当者入力_議決権保有者名簿1_記載人数',
            '担当者入力_議決権保有者名簿1_近隣住民数',
            '担当者入力_議決権保有者名簿1_その他',
            '担当者入力_議決権保有者名簿2_種類',
            '担当者入力_議決権保有者名簿2_構成員',
            '担当者入力_議決権保有者名簿2_記載人数',
            '担当者入力_議決権保有者名簿2_近隣住民数',
            '担当者入力_議決権保有者名簿2_その他',
            '担当者入力_議決権保有者名簿3_種類',
            '担当者入力_議決権保有者名簿3_構成員',
            '担当者入力_議決権保有者名簿3_記載人数',
            '担当者入力_議決権保有者名簿3_近隣住民数',
            '担当者入力_議決権保有者名簿3_その他',
            '担当者入力_議決権保有者名簿4_種類',
            '担当者入力_議決権保有者名簿4_構成員',
            '担当者入力_議決権保有者名簿4_記載人数',
            '担当者入力_議決権保有者名簿4_近隣住民数',
            '担当者入力_議決権保有者名簿4_その他',
            '担当者入力_議決権保有者名簿5_種類',
            '担当者入力_議決権保有者名簿5_構成員',
            '担当者入力_議決権保有者名簿5_記載人数',
            '担当者入力_議決権保有者名簿5_近隣住民数',
            '担当者入力_議決権保有者名簿5_その他'
        ]
        # 書類チェックの結果の初期状態は「書類未チェック」
        for col in document04_check_result_columns:
            document04_checklist_df.loc[index, col] = '書類未チェック'
        # 受付日時のカラムはlatest_reception_data_dateを使用
        document04_checklist_df.loc[index, '受付日時'] = pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
        # チェックリスト作成日時のカラムは現在のJST日時を使用
        document04_checklist_df.loc[index, 'チェックリスト作成日時'] = pd.to_datetime(get_jst_now()).strftime('%Y-%m-%d %H:%M:%S')
        # チェック項目のカラムを指定
        check_columns = [
            'チェック項目_議決権保有者名簿1',
            'チェック項目_議決権保有者名簿2',
            'チェック項目_議決権保有者名簿3',
            'チェック項目_議決権保有者名簿4',
            'チェック項目_議決権保有者名簿5'
        ]
        # チェック項目の初期状態は「未チェック」
        for col in check_columns:
            document04_checklist_df.loc[index, col] = '未チェック'
        # チェック項目_その他の初期状態は空文字列
        document04_checklist_df.loc[index, 'チェック項目_その他'] = ''
        # チェック者名の初期状態は「チェックが完了していません」
        document04_checklist_df.loc[index, 'チェック者名_議決権保有者名簿'] = 'チェックが完了していません'
    logging.info("書類04のチェックリストのデータフレームを作成しました")

    # 5. 書類04のチェックリストのデータフレームを保存
    logging.info("書類04のチェックリストのデータフレームを保存します")
    now_jst = get_jst_now()
    document04_checklist_file_name = f'書類04チェックリスト_受付{latest_reception_data_date_str}_作成{now_jst.strftime("%Y%m%d%H%M%S")}.xlsx'
    document04_checklist_file_path = os.path.join(document04_checklist_folder_path, document04_checklist_file_name)
    document04_checklist_df.to_excel(document04_checklist_file_path, index=False)
    logging.info(f"書類04のチェックリストのデータフレームを保存しました: {document04_checklist_file_path}")

    # 6. 書類04のチェックリストのファイルを保存
    logging.info("書類04のチェックリストのファイルを保存します")
    document04_checklist_df.to_excel(document04_checklist_file_path, index=False)
    logging.info(f"書類04のチェックリストのファイルを保存しました: {document04_checklist_file_path}")