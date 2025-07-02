def processing_reception_data():
    import os
    import logging
    import pandas as pd
    from src.core.setting_paths import (
        reception_data_folder_path,
        processed_reception_data_folder_path,
    )
    from src.folder_management.make_folders import setup_logging, create_folders
    from src.core.utils import get_jst_now
    from src.data_processing.column_name_change import column_name_change

    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()

    # 1. 最新の申請データを探す
    logging.info("申請データを探しています")
    # 申請データはdata/applicationsフォルダにある
    project_root = os.getcwd()
    applications_folder = os.path.join(project_root, 'data', 'applications')
    
    # フォルダが存在しない場合は空のリストを返す
    if not os.path.exists(applications_folder):
        logging.error(f"申請データフォルダが見つかりません: {applications_folder}")
        reception_data_files = []
    else:
        reception_data_files = [
            f for f in os.listdir(applications_folder)
            if os.path.isfile(os.path.join(applications_folder, f)) and
            f.startswith('申請データ_') and f.endswith('.xlsx')
        ]
    # ファイル名の形式は「申請データ_YYYYMMDDHHMMSS.xlsx」
    # 申請データファイルを見つけたら、ファイル名のYYYYMMDDHHMMSS形式でソート
    reception_data_files.sort(reverse=True)
    if not reception_data_files:
        logging.error("申請データファイルが見つかりません")
    # 見つかったら、見つかったファイルの数をログに記録
    else:
        logging.info(f"見つかった申請データファイルの数: {len(reception_data_files)}")
    # 最新の申請データファイルを特定
    logging.info(f"最新の申請データファイルを特定しています")
    latest_reception_data_file = reception_data_files[0] if reception_data_files else None
    logging.info(f"最新の申請データファイル: {latest_reception_data_file}")
    # 最新の申請データの作成日を取得（ファイル名のYYYYMMDDHHMMSS形式から）
    if latest_reception_data_file:
        latest_reception_data_date = latest_reception_data_file.split('_')[1].split('.')[0]
        latest_reception_data_date = pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S')
        logging.info(f"最新の申請データの作成日: {latest_reception_data_date}")
    else:
        logging.error("最新の申請データファイルが見つかりません")

    # 2. 最新の申請データの作成日から、申請データを読み込み処理を必要があるかを判断
    logging.info("最新の申請データの作成日から、申請データを読み込む必要があるかを判断しています")
    # 処理後のデータのフォルダパス(processed_reception_data_folder_path)に保存されている最新の申請データを特定
    # ファイル名は「処理済み申請データ_申請YYYYMMDDHHMMSS_処理YYYYMMDDHHMMSS.xlsx」
    reception_data_files = [
        f for f in os.listdir(processed_reception_data_folder_path)
        if os.path.isfile(os.path.join(processed_reception_data_folder_path, f)) and
        f.startswith('処理済み申請データ_申請') and f.endswith('.xlsx')
    ]
    # ファイル名の形式は「処理済み申請データ_申請YYYYMMDDHHMMSS_処理YYYYMMDDHHMMSS.xlsx」
    # 処理済み申請データファイルを見つけたら、ファイル名の申請のYYYYMMDDHHMMSS形式でソート
    reception_data_files.sort(reverse=True)
    if not reception_data_files:
        logging.info("処理済み申請データファイルが見つかりません")
    # 見つかったら、見つかったファイルの数をログに記録
    else:
        logging.info(f"見つかった処理済み申請データファイルの数: {len(reception_data_files)}")
    # 最新の処理済み申請データファイルを特定
    logging.info(f"最新の処理済み申請データファイルを特定しています")
    latest_processed_reception_data_file = reception_data_files[0] if reception_data_files else None
    logging.info(f"最新の処理済み申請データファイル: {latest_processed_reception_data_file}")
    # 最新の処理済み申請データの申請日を取得（ファイル名の申請YYYYMMDDHHMMSS形式から）
    if latest_processed_reception_data_file:
        # 申請日時を取得: "申請20250401000000" から "申請" を除去
        latest_processed_reception_data_date = latest_processed_reception_data_file.split('_')[1].replace('申請', '')
        latest_processed_reception_data_date = pd.to_datetime(latest_processed_reception_data_date, format='%Y%m%d%H%M%S')
        logging.info(f"最新の処理済み申請データの申請日: {latest_processed_reception_data_date}")
    else:
        logging.error("最新の処理済み申請データファイルが見つかりません")
        latest_processed_reception_data_date = None
    # 最新の申請データの作成日と最新の処理済み申請データの申請日を比較
    if latest_reception_data_file and latest_processed_reception_data_file:
        if latest_reception_data_date > latest_processed_reception_data_date:
            logging.info("最新の申請データを読み込む必要があります")
            latest_reception_data_file = os.path.join(applications_folder, latest_reception_data_file)
        else:
            logging.info("最新の申請データを読み込む必要はありません")
            latest_reception_data_file = None
    elif latest_reception_data_file and not latest_processed_reception_data_file:
        # 処理済みデータがない場合は初回実行として処理
        logging.info("処理済みデータが見つからないため、初回実行として申請データを処理します")
        latest_reception_data_file = os.path.join(applications_folder, latest_reception_data_file)
    else:
        logging.error("申請データファイルが見つかりません")
        latest_reception_data_file = None
    # 申請データを読み込む必要がない場合は、最新の処理済みデータの日付を返して正常終了
    if not latest_reception_data_file:
        logging.info("申請データを読み込む必要がないため、既存の処理済みデータを使用します")
        if latest_processed_reception_data_date:
            logging.info(f"最新の処理済み申請データの日付: {latest_processed_reception_data_date}")
            return latest_processed_reception_data_date
        else:
            logging.info("処理済みデータも申請データも見つからないため、処理をスキップします")
            return "no_data"

    # 3. 最新の申請データを読み込む
    logging.info(f"最新の申請データファイルを読み込みます: {latest_reception_data_file}") 
    try:
        reception_data_df = pd.read_excel(latest_reception_data_file)
        logging.info(f"申請データの読み込みに成功しました: {reception_data_df.shape[0]}件のデータが読み込まれました")
    except Exception as e:
        logging.error(f"申請データの読み込みに失敗しました: {e}", exc_info=True)
        return
    
    # 4. 申請データのカラム名を修正処理
    logging.info("申請データの処理を開始します")
    # カラム名の変更
    processed_reception_data_df = column_name_change(reception_data_df)
    if processed_reception_data_df is None:
        logging.error("カラム名の変更に失敗しました")
        return
    logging.info("申請データのカラム名を変更しました")
    # 処理済み申請データのフォルダが存在しない場合は作成
    if not os.path.exists(processed_reception_data_folder_path):
        os.makedirs(processed_reception_data_folder_path)
        logging.info(f"処理済み申請データのフォルダを作成しました: {processed_reception_data_folder_path}")
    # 処理済み申請データのファイル名を指定（処理済み申請データ_申請YYYYMMDDHHMMSS_処理YYYYMMDDHHMMSS.xlsx）
    processed_reception_data_date = get_jst_now().strftime('%Y%m%d%H%M%S')
    processed_reception_data_file_name = f"処理済み申請データ_申請{latest_reception_data_date.strftime('%Y%m%d%H%M%S')}_処理{processed_reception_data_date}.xlsx"
    processed_reception_data_file_path = os.path.join(processed_reception_data_folder_path, processed_reception_data_file_name)
    # 処理済み申請データを保存
    try:
        processed_reception_data_df.to_excel(processed_reception_data_file_path, index=False)
        logging.info(f"処理済み申請データを保存しました: {processed_reception_data_file_path}")
    except Exception as e:
        logging.error(f"処理済み申請データの保存に失敗しました: {e}", exc_info=True)
        return
    # latest_reception_data_dateを返す
    return latest_reception_data_date