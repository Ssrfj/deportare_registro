def make_document05_plan_checklist(latest_reception_data_date):
    import os
    import pandas as pd
    import logging
    from setting import content_check_folder_path, document05_plan_checklist_folder_path
    from utils import get_jst_now
    from make_folders import setup_logging, create_folders

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
    club_reception_df = pd.read_excel(os.path.join(content_check_folder_path, latest_club_reception_file))
    logging.info(f"最新のクラブ情報付き受付データを読み込みました: {latest_club_reception_file}")

    # 2. 書類05_計画_のチェックリストを作成する必要があるか確認
    logging.info("書類05_計画_のチェックリストを作成する必要があるか確認します")
    # 書類05_計画_のチェックリストが既に存在するか確認
    existing_checklist_files = [
        f for f in os.listdir(document05_plan_checklist_folder_path)
        if os.path.isfile(os.path.join(document05_plan_checklist_folder_path, f)) and
        f.startswith('書類05_計画_チェックリスト_') and f.endswith('.xlsx')
    ]
    
    # 既存の書類05_計画_のチェックリストで同じ受付データのものがあるか確認
    existing_checklist_files.sort(reverse=True)
    for file in existing_checklist_files:
        # ファイル名から受付日時を抽出: 書類05_計画_チェックリスト_受付{YYYYMMDDHHMMSS}_作成{YYYYMMDDHHMMSS}.xlsx
        file_parts = file.replace('書類05_計画_チェックリスト_受付', '').replace('.xlsx', '').split('_作成')
        if len(file_parts) >= 1:
            file_reception_date_str = file_parts[0]
            try:
                file_reception_date = pd.to_datetime(file_reception_date_str, format='%Y%m%d%H%M%S')
                if file_reception_date == pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S'):
                    logging.info(f"同じ受付データの書類05_計画_チェックリストが既に存在します: {file}")
                    logging.info("新しいチェックリストを作成しません。")
                    return
                elif file_reception_date < pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S'):
                    logging.info(f"古い受付データの書類05_計画_チェックリストが存在します: {file}")
                    logging.info("新しい受付データ用のチェックリストを作成します。")
                    break
            except ValueError:
                logging.warning(f"ファイル名から受付日時を解析できませんでした: {file}")
                continue

    # 3. 書類05_計画_のチェックリストのカラム名を取得
    logging.info("書類05_計画_のチェックリストのカラム名を取得します")
    # jsonファイルを読み込む（document05_plan_checklist_columns.jsonが必要）
    document05_plan_checklist_columns_file_name = 'document05_plan_checklist_columns.json'
    document05_plan_checklist_columns_file_path = os.path.join(content_check_folder_path, document05_plan_checklist_columns_file_name)
    if not os.path.exists(document05_plan_checklist_columns_file_path):
        logging.error(f"書類05_計画のチェックリストのカラム名ファイルが見つかりません: {document05_plan_checklist_columns_file_path}")
        return
    document05_plan_checklist_columns = pd.read_json(document05_plan_checklist_columns_file_path, orient='records')
    logging.info(f"書類05_計画のチェックリストのカラム名を読み込みました: {document05_plan_checklist_columns_file_name}")

    # 4. 書類05_計画のチェックリストのデータフレームを作成
    logging.info("書類05_計画のチェックリストのデータフレームを作成します")
    document05_plan_checklist_df = pd.DataFrame(columns=document05_plan_checklist_columns['document05_plan_checklist_columns'].tolist())
    logging.info("書類05_計画のチェックリストのデータフレームを作成しました")
    # 書類05_planのチェックリストのデータフレームにクラブ情報を追加
    for index, row in club_reception_df.iterrows():
        club_name = row['クラブ名']
        document05_plan_checklist_df.loc[index, '申請日時'] = row['申請_タイムスタンプ']
        document05_plan_checklist_df.loc[index, 'クラブ名'] = club_name
        document05_plan_checklist_df.loc[index, '地区名'] = row['地区名']
        # 書類チェックの結果を記載するカラムを指定
        document05_plan_check_result_columns = [
            '書類チェック結果_議決権保有者名簿1_種類',
            '書類チェック結果_議決権保有者名簿1_構成員',
            '書類チェック結果_議決権保有者名簿1_記載人数',
            '書類チェック結果_議決権保有者名簿1_近隣住民数',
            '書類チェック結果_議決権保有者名簿1_その他',
            '書類チェック結果_議決権保有者名簿2_種類',
            '書類チェック結果_議決権保有者名簿2_構成員',
            '書類チェック結果_議決権保有者名簿2_記載人数',
            '書類チェック結果_議決権保有者名簿2_近隣住民数',
            '書類チェック結果_議決権保有者名簿2_その他',
            '書類チェック結果_議決権保有者名簿3_種類',
            '書類チェック結果_議決権保有者名簿3_構成員',
            '書類チェック結果_議決権保有者名簿3_記載人数',
            '書類チェック結果_議決権保有者名簿3_近隣住民数',
            '書類チェック結果_議決権保有者名簿3_その他',
            '書類チェック結果_議決権保有者名簿4_種類',
            '書類チェック結果_議決権保有者名簿4_構成員',
            '書類チェック結果_議決権保有者名簿4_記載人数',
            '書類チェック結果_議決権保有者名簿4_近隣住民数',
            '書類チェック結果_議決権保有者名簿4_その他',
            '書類チェック結果_議決権保有者名簿5_種類',
            '書類チェック結果_議決権保有者名簿5_構成員',
            '書類チェック結果_議決権保有者名簿5_記載人数',
            '書類チェック結果_議決権保有者名簿5_近隣住民数',
            '書類チェック結果_議決権保有者名簿5_その他'
        ]
        # 書類チェックの結果の初期状態は「書類未チェック」
        for col in document05_plan_check_result_columns:
            document05_plan_checklist_df.loc[index, col] = '書類未チェック'
        # 受付日時のカラムはlatest_reception_data_dateを使用
        document05_plan_checklist_df.loc[index, '受付日時'] = pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
        # チェックリスト作成日時のカラムは現在のJST日時を使用
        document05_plan_checklist_df.loc[index, 'チェックリスト作成日時'] = pd.to_datetime(get_jst_now()).strftime('%Y-%m-%d %H:%M:%S')
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
            document05_plan_checklist_df.loc[index, col] = '未チェック'
        # チェック項目_その他の初期状態は空文字列
        document05_plan_checklist_df.loc[index, 'チェック項目_その他'] = ''
        # チェック者名の初期状態は「チェックが完了していません」
        document05_plan_checklist_df.loc[index, 'チェック者名_議決権保有者名簿'] = 'チェックが完了していません'
    logging.info("書類05_計画のチェックリストのデータフレームを作成しました")

    # 5. 書類05_計画のチェックリストのデータフレームを保存(ファイル名は「書類05_計画チェックリスト_受付{latest_reception_data_date}_作成{YYYYMMDDHHMMSS}.xlsx」)
    logging.info("書類05_計画のチェックリストのデータフレームを保存します")
    now_jst = get_jst_now()
    document05_plan_checklist_file_name = f'書類05_計画チェックリスト_受付{latest_reception_data_date}_作成{now_jst.strftime("%Y%m%d%H%M%S")}.xlsx'
    document05_plan_checklist_file_path = os.path.join(document05_plan_checklist_df, document05_plan_checklist_file_name)
    document05_plan_checklist_df.to_excel(document05_plan_checklist_file_path, index=False)
    logging.info(f"書類05_計画のチェックリストのデータフレームを保存しました: {document05_plan_checklist_file_path}")

    # 6. 書類05_計画のチェックリストのファイルを保存
    logging.info("書類05_計画のチェックリストのファイルを保存します")
    document05_plan_checklist_df.to_excel(document05_plan_checklist_file_path, index=False)
    logging.info(f"書類05_計画のチェックリストのファイルを保存しました: {document05_plan_checklist_file_path}")