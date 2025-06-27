def marge_reception_data_with_club_info(latest_reception_data_date):
    import os
    import pandas as pd
    import logging
    from setting import clubs_reception_data_path, processed_reception_data_folder_path, club_info_data_path
    from make_folders import setup_logging, create_folders
    from utils import get_jst_now

    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()
    logging.info("フォルダを作成しました")
    # 1. クラブ情報付き申請データのフォルダを作成
    if not os.path.exists(clubs_reception_data_path):
        os.makedirs(clubs_reception_data_path)
        logging.info(f"クラブ情報付き申請データのフォルダを作成しました: {clubs_reception_data_path}")
    else:
        logging.info(f"クラブ情報付き申請データのフォルダは既に存在します: {clubs_reception_data_path}")

    # 2. 最新のクラブ情報付き申請データファイルを取得(クラブ情報付き申請データ_申請YYYYMMDDHHMMSS_作成YYYYMMDDHHMMSS.xlsx)
    logging.info("最新のクラブ情報付き申請データファイルを取得しています")
    club_reception_data_files = [
        f for f in os.listdir(clubs_reception_data_path)
        if os.path.isfile(os.path.join(clubs_reception_data_path, f)) and
        f.startswith('クラブ情報付き申請データ_申請') and f.endswith('.xlsx')
    ]
    # ファイル名の形式は「クラブ情報付き申請データ_申請YYYYMMDDHHMMSS_作成YYYYMMDDHHMMSS.xlsx」
    # クラブ情報付き申請データファイルを見つけたら、ファイル名の申請のYYYYMMDDHHMMSS形式でソート
    club_reception_data_files.sort(reverse=True)
    if not club_reception_data_files:
        logging.info("クラブ情報付き申請データファイルが見つかりません")
        latest_club_reception_data_file = None
    else:
        latest_club_reception_data_file = club_reception_data_files[0]
        logging.info(f"最新のクラブ情報付き申請データファイル: {latest_club_reception_data_file}")
    # 最新のクラブ情報付き申請データの作成日を取得（ファイル名のYYYYMMDDHHMMSS形式から）
    if latest_club_reception_data_file:
        latest_club_reception_data_date = latest_club_reception_data_file.split('_')[2].split('.')[0]
        latest_club_reception_data_date = pd.to_datetime(latest_club_reception_data_date, format='%Y%m%d%H%M%S')
        logging.info(f"最新のクラブ情報付き申請データの作成日: {latest_club_reception_data_date}")
    else:
        logging.error("最新のクラブ情報付き申請データファイルが見つかりません")
        return
    
    # 3. 最新のクラブ情報付き申請データを作成する必要があるかを判断
    if latest_club_reception_data_date and latest_club_reception_data_date >= latest_reception_data_date:
        logging.info("最新のクラブ情報付き申請データは既に最新です。処理を終了します。")
        return
    logging.info("最新のクラブ情報付き申請データを作成する必要があります。処理を続行します。")

    # 4. 最新の処理済み申請データを読み込む（処理済み申請データ_申請{latest_reception_data_date}_処理YYYYMMDDHHMMSS.xlsx形式）
    logging.info("最新の処理済み申請データを読み込みます")
    processed_reception_data_files = [
        f for f in os.listdir(processed_reception_data_folder_path)
        if os.path.isfile(os.path.join(processed_reception_data_folder_path, f)) and
        f.startswith('処理済み申請データ_申請') and f.endswith('.xlsx')
    ]
    # ファイル名の形式は「処理済み申請データ_申請YYYYMMDDHHMMSS_処理YYYYMMDDHHMMSS.xlsx」
    # 処理済み申請データファイルを見つけたら、ファイル名の申請のYYYYMMDDHHMMSS形式でソート
    processed_reception_data_files.sort(reverse=True)
    if not processed_reception_data_files:
        logging.error("処理済み申請データファイルが見つかりません")
        return
    latest_processed_reception_data_file = processed_reception_data_files[0]
    logging.info(f"最新の処理済み申請データファイル: {latest_processed_reception_data_file}")
    # 最新の処理済み申請データの申請日を取得（ファイル名の申請YYYYMMDDHHMMSS形式から）
    latest_processed_reception_data_date = latest_processed_reception_data_file.split('_')[2].split('.')[0]
    latest_processed_reception_data_date = pd.to_datetime(latest_processed_reception_data_date, format='%Y%m%d%H%M%S')
    logging.info(f"最新の処理済み申請データの申請日: {latest_processed_reception_data_date}")
    # 最新の処理済み申請データを読み込む
    processed_reception_data_path = os.path.join(processed_reception_data_folder_path, latest_processed_reception_data_file)
    logging.info(f"最新の処理済み申請データを読み込みます: {processed_reception_data_path}")
    processed_reception_df = pd.read_excel(processed_reception_data_path)
    logging.info("最新の処理済み申請データを読み込みました")

    # 5. 最新のクラブ情報を読み込む（クラブ名_YYYYMMDDHHMMSS.xlsx形式）
    logging.info("最新のクラブ情報を読み込みます")
    latest_club_info_files = [
        f for f in os.listdir(club_info_data_path)
        if os.path.isfile(os.path.join(club_info_data_path, f)) and
        f.startswith('クラブ情報_') and f.endswith('.xlsx')
    ]
    latest_club_info_files.sort(reverse=True)
    if not latest_club_info_files:
        logging.error("クラブ情報ファイルが見つかりません")
        return
    latest_club_info_file = latest_club_info_files[0]
    latest_club_info_date = latest_club_info_file.split('_')[1].split('.')[0]
    latest_club_info_date = pd.to_datetime(latest_club_info_date, format='%Y%m%d%H%M%S')
    logging.info(f"最新のクラブ情報ファイル: {latest_club_info_file}")
    club_info_df = pd.read_excel(os.path.join(club_info_data_path, latest_club_info_file))
    logging.info(f"最新のクラブ情報を読み込みました: {latest_club_info_file}")

    # 6. 最新のクラブ情報と処理済み申請データをマージ
    # 基本は、club_info_dfの'選択肢（地区名：クラブ名：クラブ名（カタカナ））'とprocessed_reception_dfの'申請_クラブ名_選択'をキーにしてマージ
    # ただし、processed_reception_dfの'申請_クラブ名_選択'が「選択肢にない」の場合は行を追加＋'申請_クラブ名_テキスト'を'クラブ名'にコピー
    logging.info("最新のクラブ情報に処理済み申請データをマージします")
    
    # まず、申請データのある行のみを対象とする（申請_クラブ名_選択が空でない行）
    reception_data = processed_reception_df[processed_reception_df['申請_クラブ名_選択'].notna() & 
                                               (processed_reception_df['申請_クラブ名_選択'] != '')].copy()
    
    # 「選択肢にない」の場合と通常の選択肢の場合で処理を分ける
    # 通常の選択肢の場合：club_info_dfとマージ
    normal_selection = reception_data[reception_data['申請_クラブ名_選択'] != '選択肢にない'].copy()
    new_club_selection = reception_data[reception_data['申請_クラブ名_選択'] == '選択肢にない'].copy()
    
    # 通常の選択肢の場合のマージ
    clubs_reception_data_df = pd.merge(
        club_info_df,
        normal_selection,
        left_on='選択肢（地区名：クラブ名：クラブ名（カタカナ））',
        right_on='申請_クラブ名_選択',
        how='inner'  # 申請があったクラブのみ
    )
    logging.info(f"通常の選択肢でマージされた行数: {len(clubs_reception_data_df)}")
    
    # 「選択肢にない」の場合の処理
    if len(new_club_selection) > 0:
        logging.info(f"「選択肢にない」申請の行数: {len(new_club_selection)}")
        
        # 新しいクラブの行を作成
        for _, row in new_club_selection.iterrows():
            new_row = row.copy()
            # クラブ情報の列は空またはデフォルト値を設定
            new_row['地区名'] = ''  # または適切なデフォルト値
            new_row['クラブ名'] = row['申請_クラブ名_テキスト']  # テキスト入力をクラブ名として使用
            new_row['クラブ名（カタカナ）'] = ''  # または適切なデフォルト値
            new_row['選択肢（地区名：クラブ名：クラブ名（カタカナ））'] = '選択肢にない'
            new_row['R7年度登録クラブ'] = 0  # 新しいクラブなので0
            
            # DataFrameに追加
            clubs_reception_data_df = pd.concat([clubs_reception_data_df, new_row.to_frame().T], ignore_index=True)
        
        logging.info(f"「選択肢にない」申請を追加後の総行数: {len(clubs_reception_data_df)}")
    
    logging.info(f"マージ完了。最終的な行数: {len(clubs_reception_data_df)}")
    
    # 7. マージしたデータを保存
    current_time = get_jst_now()
    timestamp = current_time.strftime('%Y%m%d%H%M%S')
    reception_timestamp = latest_processed_reception_data_date.strftime('%Y%m%d%H%M%S')
    
    clubs_reception_data_file_name = f"クラブ情報付き申請データ_申請{reception_timestamp}_作成{timestamp}.xlsx"
    clubs_reception_data_file_path = os.path.join(clubs_reception_data_path, clubs_reception_data_file_name)
    
    clubs_reception_data_df.to_excel(clubs_reception_data_file_path, index=False)
    logging.info(f"クラブ情報付き申請データを保存しました: {clubs_reception_data_file_path}")