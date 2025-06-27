def make_overall_checklist(latest_reception_data_date):
    import os
    import pandas as pd
    import logging
    from setting import content_check_folder_path, settting_folder_path, overall_checklist_folder_path
    from utils import get_jst_now
    from make_folders import setup_logging, create_folders


    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()
    logging.info("フォルダを作成しました")

    # 受付データの日付を取得
    if not latest_reception_data_date:
        logging.error("最新の受付データの日付が指定されていません")
        return
    latest_reception_data_date = pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S').strftime('%Y%m%d%H%M%S')

    # 1. 最新のクラブ情報付き受付データファイルを取得
    logging.info("最新のクラブ情報付き受付データファイルを取得します")
    latest_club_reception_files = [
        f for f in os.listdir(content_check_folder_path)
        if os.path.isfile(os.path.join(content_check_folder_path, f)) and
        f.startswith('クラブ情報付き受付データ_') and f.endswith('.xlsx')
    ]
    latest_club_reception_files.sort(reverse=True)
    if not latest_club_reception_files:
        logging.error("クラブ情報付き受付データファイルが見つかりません")
        return
    latest_club_reception_file = latest_club_reception_files[0]
    latest_club_reception_date = latest_club_reception_file.split('_')[1].split('.')[0]
    latest_club_reception_date = pd.to_datetime(latest_club_reception_date, format='%Y%m%d%H%M%S')
    logging.info(f"最新のクラブ情報付き受付データファイル: {latest_club_reception_file}")
    club_reception_df = pd.read_excel(os.path.join(content_check_folder_path, latest_club_reception_file))
    logging.info(f"最新のクラブ情報付き受付データを読み込みました: {latest_club_reception_file}")

    # 2. 総合チェックリストのカラム名を取得
    logging.info("総合チェックリストのカラム名を取得します")
    # jsonファイルを読み込む（overall_checklist_columns.jsonが必要）
    overall_checklist_columns_file_name = 'overall_checklist_columns.json'
    overall_checklist_columns_file_path = os.path.join(settting_folder_path, overall_checklist_columns_file_name)
    if not os.path.exists(overall_checklist_columns_file_path):
        logging.error(f"総合チェックリストのカラム名ファイルが見つかりません: {overall_checklist_columns_file_path}")
        return
    overall_checklist_columns = pd.read_json(overall_checklist_columns_file_path, orient='records')
    logging.info(f"総合チェックリストのカラム名を読み込みました: {overall_checklist_columns_file_name}")

    # 3. 総合チェックリストのデータフレームを作成
    logging.info("総合チェックリストのデータフレームを作成します")
    overall_checklist_df = pd.DataFrame(columns=overall_checklist_columns['overall_checklist_columns'].tolist())
    logging.info("総合チェックリストのデータフレームを作成しました")

    # 4. 各クラブの受付データを総合チェックリストに追加
    logging.info("各クラブの受付データを総合チェックリストに追加します")
    # 各クラブの受付データを総合チェックリストに追加
    now_jst = get_jst_now()
    for index, row in club_reception_df.iterrows():
        # 各クラブの受付データを取得
        club_name = row['クラブ名']
        # 各クラブの受付データを総合チェックリストに追加
        overall_checklist_df.loc[index, 'クラブ名'] = club_name
        overall_checklist_df.loc[index, '受付日時'] = row['受付_タイムスタンプ']
        overall_checklist_df.loc[index, '担当者名'] = row['担当者名']
        overall_checklist_df.loc[index, '担当者役職名'] = row['担当者役職名']
        overall_checklist_df.loc[index, 'メールアドレス'] = row['メールアドレス']
        overall_checklist_df.loc[index, '電話番号'] = row['電話番号']
        overall_checklist_df.loc[index, 'FAX番号'] = row['FAX番号']
        # 結果のカラムは未チェックとする
        overall_checklist_df.loc[index, '自動チェック結果'] = '未チェック'
        overall_checklist_df.loc[index, '書類チェック結果'] = '未チェック'
        overall_checklist_df.loc[index, '書類間チェック結果'] = '未チェック'
        overall_checklist_df.loc[index, '担当者登録基準最終チェック結果'] = '未チェック'
        # 更新時間のカラムは現在時刻とする
        overall_checklist_df.loc[index, '自動チェック更新日時'] = now_jst.strftime('%Y-%m-%d %H:%M:%S')
        overall_checklist_df.loc[index, '書類チェック更新日時'] = now_jst.strftime('%Y-%m-%d %H:%M:%S')
        overall_checklist_df.loc[index, '書類間チェック更新日時'] = now_jst.strftime('%Y-%m-%d %H:%M:%S')
        overall_checklist_df.loc[index, '担当者登録基準最終チェック更新日時'] = now_jst.strftime('%Y-%m-%d %H:%M:%S')
    logging.info("各クラブの受付データを総合チェックリストに追加しました")
    
    # 5. 総合チェックリストのファイルを保存（ファイル名は「総合チェックリスト_受付{YYYYMMDDHHMMSS}_更新{YYYYMMDDHHMMSS}.xlsx」）
    logging.info("総合チェックリストのファイルを保存します")
    now_jst = get_jst_now()
    overall_checklist_file_name = f'総合チェックリスト_受付{latest_reception_data_date}_更新{now_jst.strftime("%Y%m%d%H%M%S")}.xlsx'
    overall_checklist_file_path = os.path.join(overall_checklist_folder_path, overall_checklist_file_name)
    overall_checklist_df.to_excel(overall_checklist_file_path, index=False)
    logging.info(f"総合チェックリストのファイルを保存しました: {overall_checklist_file_path}")