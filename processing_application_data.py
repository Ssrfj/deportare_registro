def processing_application_data():
    import os
    import logging
    import pandas as pd
    from setting import (
        application_data_folder_path,
        processed_application_data_folder_path,
    )
    from make_folders import setup_logging, create_folders
    from utils import get_jst_now
    from column_name_change import column_name_change

    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()

    # 1. 最新の申請データを探す
    logging.info("申請データを探しています")
    # 申請データはPythonファイルと同じフォルダにある
    application_data_files = [
        f for f in os.listdir(application_data_folder_path)
        if os.path.isfile(os.path.join(application_data_folder_path, f)) and
        f.startswith('申請データ_') and f.endswith('.xlsx')
    ]
    # ファイル名の形式は「申請データ_YYYYMMDDHHMMSS.xlsx」
    # 申請データファイルを見つけたら、ファイル名のYYYYMMDDHHMMSS形式でソート
    application_data_files.sort(reverse=True)
    if not application_data_files:
        logging.error("申請データファイルが見つかりません")
    # 見つかったら、見つかったファイルの数をログに記録
    else:
        logging.info(f"見つかった申請データファイルの数: {len(application_data_files)}")
    # 最新の申請データファイルを特定
    logging.info(f"最新の申請データファイルを特定しています")
    latest_application_data_file = application_data_files[0] if application_data_files else None
    logging.info(f"最新の申請データファイル: {latest_application_data_file}")
    # 最新の申請データの作成日を取得（ファイル名のYYYYMMDDHHMMSS形式から）
    if latest_application_data_file:
        latest_application_data_date = latest_application_data_file.split('_')[2].split('.')[0]
        latest_application_data_date = pd.to_datetime(latest_application_data_date, format='%Y%m%d%H%M%S')
        logging.info(f"最新の申請データの作成日: {latest_application_data_date}")
    else:
        logging.error("最新の申請データファイルが見つかりません")

    # 2. 最新の申請データの作成日から、申請データを読み込み処理を必要があるかを判断
    logging.info("最新の申請データの作成日から、申請データを読み込む必要があるかを判断しています")
    # 処理後のデータのフォルダパス(processed_application_data_folder_path)に保存されている最新の申請データを特定
    # ファイル名は「処理済み申請データ_申請YYYYMMDDHHMMSS_処理YYYYMMDDHHMMSS.xlsx」
    application_data_files = [
        f for f in os.listdir(processed_application_data_folder_path)
        if os.path.isfile(os.path.join(processed_application_data_folder_path, f)) and
        f.startswith('処理済み申請データ_申請') and f.endswith('.xlsx')
    ]
    # ファイル名の形式は「処理済み申請データ_申請YYYYMMDDHHMMSS_処理YYYYMMDDHHMMSS.xlsx」
    # 処理済み申請データファイルを見つけたら、ファイル名の申請のYYYYMMDDHHMMSS形式でソート
    application_data_files.sort(reverse=True)
    if not application_data_files:
        logging.info("処理済み申請データファイルが見つかりません")
    # 見つかったら、見つかったファイルの数をログに記録
    else:
        logging.info(f"見つかった処理済み申請データファイルの数: {len(application_data_files)}")
    # 最新の処理済み申請データファイルを特定
    logging.info(f"最新の処理済み申請データファイルを特定しています")
    latest_processed_application_data_file = application_data_files[0] if application_data_files else None
    logging.info(f"最新の処理済み申請データファイル: {latest_processed_application_data_file}")
    # 最新の処理済み申請データの申請日を取得（ファイル名の申請YYYYMMDDHHMMSS形式から）
    if latest_processed_application_data_file:
        latest_processed_application_data_date = latest_processed_application_data_file.split('_')[2].split('.')[0]
        latest_processed_application_data_date = pd.to_datetime(latest_processed_application_data_date, format='%Y%m%d%H%M%S')
        logging.info(f"最新の処理済み申請データの申請日: {latest_processed_application_data_date}")
    else:
        logging.error("最新の処理済み申請データファイルが見つかりません")
    # 最新の申請データの作成日と最新の処理済み申請データの申請日を比較
    if latest_application_data_file and latest_processed_application_data_file:
        if latest_application_data_date > latest_processed_application_data_date:
            logging.info("最新の申請データを読み込む必要があります")
            latest_application_data_file = os.path.join(application_data_folder_path, latest_application_data_file)
        else:
            logging.info("最新の申請データを読み込む必要はありません")
            latest_application_data_file = None
    else:
        logging.error("最新の申請データファイルまたは最新の処理済み申請データファイルが見つかりません")
        latest_application_data_file = None
    # 申請データを読み込む必要がない場合は終了
    if not latest_application_data_file:
        logging.info("申請データを読み込む必要がないため、処理を終了します")
        return

    # 3. 最新の申請データを読み込む
    logging.info(f"最新の申請データファイルを読み込みます: {latest_application_data_file}") 
    try:
        application_data_df = pd.read_excel(latest_application_data_file)
        logging.info(f"申請データの読み込みに成功しました: {application_data_df.shape[0]}件のデータが読み込まれました")
    except Exception as e:
        logging.error(f"申請データの読み込みに失敗しました: {e}", exc_info=True)
        return
    
    # 4. 申請データのカラム名を修正処理
    logging.info("申請データの処理を開始します")
    # カラム名の変更
    processed_application_data_df = column_name_change(application_data_df)
    if processed_application_data_df is None:
        logging.error("カラム名の変更に失敗しました")
        return
    logging.info("申請データのカラム名を変更しました")
    # 処理済み申請データのフォルダが存在しない場合は作成
    if not os.path.exists(processed_application_data_folder_path):
        os.makedirs(processed_application_data_folder_path)
        logging.info(f"処理済み申請データのフォルダを作成しました: {processed_application_data_folder_path}")
    # 処理済み申請データのファイル名を指定（処理済み申請データ_申請YYYYMMDDHHMMSS_処理YYYYMMDDHHMMSS.xlsx）
    processed_application_data_date = get_jst_now().strftime('%Y%m%d%H%M%S')
    processed_application_data_file_name = f"処理済み申請データ_申請{latest_application_data_date.strftime('%Y%m%d%H%M%S')}_処理{processed_application_data_date}.xlsx"
    processed_application_data_file_path = os.path.join(processed_application_data_folder_path, processed_application_data_file_name)
    # 処理済み申請データを保存
    try:
        processed_application_data_df.to_excel(processed_application_data_file_path, index=False)
        logging.info(f"処理済み申請データを保存しました: {processed_application_data_file_path}")
    except Exception as e:
        logging.error(f"処理済み申請データの保存に失敗しました: {e}", exc_info=True)
        return
    # latest_application_data_dateを返す
    return latest_application_data_date