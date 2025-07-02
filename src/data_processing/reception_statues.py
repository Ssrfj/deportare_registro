def reception_statues(latest_reception_data_date):
    import os
    import pandas as pd
    import logging
    from src.core.setting_paths import application_statues_folder_path, processed_reception_data_folder_path
    from src.folder_management.make_folders import setup_logging, create_folders
    from src.core.utils import get_jst_now, get_latest_club_info_file
    
    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()
    logging.info("フォルダを作成しました")

    # 1. クラブ情報付き受付データのフォルダを作成
    if not os.path.exists(application_statues_folder_path):
        os.makedirs(application_statues_folder_path)
        logging.info(f"クラブ情報付き受付データのフォルダを作成しました: {application_statues_folder_path}")
    else:
        logging.info(f"クラブ情報付き受付データのフォルダは既に存在します: {application_statues_folder_path}")

    # 2. 最新のクラブ情報を読み込む（クラブ名_YYYYMMDD.xlsx形式）
    logging.info("最新のクラブ情報を読み込みます")
    club_info_df, latest_club_info_date = get_latest_club_info_file()
    if club_info_df is None:
        return

    # 3. 最新のクラブ申請状況を読み込む（申請状況_YYYYMMDDHHMMSS.xlsx形式）
    logging.info("最新のクラブ申請状況を読み込みます")
    latest_application_statues_files = [
        f for f in os.listdir(application_statues_folder_path)
        if os.path.isfile(os.path.join(application_statues_folder_path, f)) and
        f.startswith('申請状況_') and f.endswith('.xlsx')
    ]
    latest_application_statues_files.sort(reverse=True)
    if not latest_application_statues_files:
        logging.info("申請状況ファイルが見つかりません")
        latest_application_statues_file = None
    else:
        latest_application_statues_file = latest_application_statues_files[0]
        logging.info(f"最新の申請状況ファイル: {latest_application_statues_file}")
    if latest_application_statues_file:
        latest_application_statues_date = latest_application_statues_file.split('_')[1].split('.')[0]
        latest_application_statues_date = pd.to_datetime(latest_application_statues_date, format='%Y%m%d%H%M%S')
        logging.info(f"最新の申請状況の作成日: {latest_application_statues_date}")
    else:
        logging.error("最新の申請状況ファイルが見つかりません")
        latest_application_statues_date = None

    # 4. 最新の申請状況を作成する必要があるかを判断
    if latest_application_statues_date and latest_application_statues_date >= latest_reception_data_date:
        logging.info("最新の申請状況は既に最新です。処理を終了します。")
        return
    logging.info("最新の申請状況を作成する必要があります。処理を続行します。")
    
    # 5. 最新の処理済み受付データを読み込む（処理済み受付データ_受付{latest_reception_data_date}_処理YYYYMMDDHHMMSS.xlsx形式）
    logging.info("最新の処理済み受付データを読み込みます")
    processed_reception_data_files = [
        f for f in os.listdir(processed_reception_data_folder_path)
        if os.path.isfile(os.path.join(processed_reception_data_folder_path, f)) and
        f.startswith('処理済み受付データ_受付') and f.endswith('.xlsx')
    ]
    # ファイル名の形式は「処理済み受付データ_受付YYYYMMDDHHMMSS_処理YYYYMMDDHHMMSS.xlsx」
    # 処理済み受付データファイルを見つけたら、ファイル名の受付のYYYYMMDDHHMMSS形式でソート
    processed_reception_data_files.sort(reverse=True)
    if not processed_reception_data_files:
        logging.error("処理済み受付データファイルが見つかりません")
        return
    latest_processed_reception_data_file = processed_reception_data_files[0]
    logging.info(f"最新の処理済み受付データファイル: {latest_processed_reception_data_file}")
    # 最新の処理済み受付データの受付日を取得（ファイル名の受付YYYYMMDDHHMMSS形式から）
    latest_processed_reception_data_date = latest_processed_reception_data_file.split('_')[1].replace('受付', '')
    latest_processed_reception_data_date = pd.to_datetime(latest_processed_reception_data_date, format='%Y%m%d%H%M%S')
    logging.info(f"最新の処理済み受付データの受付日: {latest_processed_reception_data_date}")
    # 最新の処理済み受付データを読み込む
    processed_reception_data_path = os.path.join(processed_reception_data_folder_path, latest_processed_reception_data_file)
    logging.info(f"最新の処理済み受付データを読み込みます: {processed_reception_data_path}")
    processed_reception_df = pd.read_excel(processed_reception_data_path)
    logging.info("最新の処理済み受付データを読み込みました")

    # 6. 処理済み受付データから申請があったクラブのデータを抽出
    logging.info("申請があったクラブのデータを抽出します")
    # club_info_dfをreception_statues_dfにコピー
    reception_statues_df = club_info_df
    # reception_statues_dfに'R8_受付状況'列と'R8_受付日時'列を追加
    reception_statues_df['R8_申請状況'] = '申請なし'
    reception_statues_df['R8_申請日時'] = pd.NaT
    # 処理済み受付データから申請があったクラブのデータを抽出
    logging.info("処理済み受付データから申請があったクラブのデータを抽出します")   
    # processed_reception_dfの各行について処理
    for index, row in processed_reception_df.iterrows():
        club_name = row['申請_クラブ名_選択']
        reception_timestamp = row['申請_タイムスタンプ']
        
        # reception_statues_dfでクラブ名が一致する行を検索
        matching_rows = reception_statues_df[reception_statues_df['クラブ名'] == club_name]
        
        if not matching_rows.empty:
            # reception_statues_dfの'クラブ名'に記載があり、processed_reception_dfの'クラブ名'に記載がある場合
            logging.info(f"クラブ名 '{club_name}' の申請状況を更新します")
            reception_statues_df.loc[reception_statues_df['クラブ名'] == club_name, 'R8_申請状況'] = '申請あり'
            reception_statues_df.loc[reception_statues_df['クラブ名'] == club_name, 'R8_申請日時'] = reception_timestamp
        else:
            # reception_statues_dfの'クラブ名'に記載がないけれども、processed_reception_dfの'クラブ名'に記載がある場合
            logging.info(f"新しいクラブ '{club_name}' を申請状況リストに追加します")
            # 新しい行を作成
            new_row = pd.DataFrame({
                'クラブ名': [club_name],
                'R8_申請状況': ['申請あり'],
                'R8_申請日時': [reception_timestamp]
            })
            # reception_statues_dfに新しい行を追加
            reception_statues_df = pd.concat([reception_statues_df, new_row], ignore_index=True)
    
    logging.info("申請状況の更新が完了しました")
    
    # 7. 申請状況データをファイルに保存
    current_time = get_jst_now()
    reception_statues_filename = f"申請状況_{current_time.strftime('%Y%m%d%H%M%S')}.xlsx"
    reception_statues_file_path = os.path.join(application_statues_folder_path, reception_statues_filename)
    
    logging.info(f"申請状況データを保存します: {reception_statues_file_path}")
    reception_statues_df.to_excel(reception_statues_file_path, index=False)
    logging.info(f"申請状況データを保存しました: {reception_statues_filename}")
    
    # 8. 処理結果のサマリーを出力
    total_clubs = len(reception_statues_df)
    applied_clubs = len(reception_statues_df[reception_statues_df['R8_申請状況'] == '申請あり'])
    not_applied_clubs = total_clubs - applied_clubs
    
    logging.info("=== 申請状況処理結果サマリー ===")
    logging.info(f"総クラブ数: {total_clubs}")
    logging.info(f"申請ありクラブ数: {applied_clubs}")
    logging.info(f"申請なしクラブ数: {not_applied_clubs}")
    logging.info(f"保存ファイル: {reception_statues_filename}")
    logging.info("申請状況の更新処理が完了しました")
    
    return reception_statues_file_path