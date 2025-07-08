def marge_reception_data_with_club_info(latest_reception_data_date):
    import os
    import pandas as pd
    import logging
    from src.core.setting_paths import clubs_reception_data_path, processed_reception_data_folder_path
    from src.core.utils import get_jst_now, get_latest_club_info_file

    # 1. クラブ情報付き受付データのフォルダを作成
    if not os.path.exists(clubs_reception_data_path):
        os.makedirs(clubs_reception_data_path)
        logging.info(f"クラブ情報付き受付データのフォルダを作成しました: {clubs_reception_data_path}")
    else:
        logging.info(f"クラブ情報付き受付データのフォルダは既に存在します: {clubs_reception_data_path}")

    # 2. 最新のクラブ情報付き受付データファイルを取得(クラブ情報付き受付データ_受付YYYYMMDDHHMMSS_作成YYYYMMDDHHMMSS.xlsx)
    logging.info("最新のクラブ情報付き受付データファイルを取得しています")
    club_reception_data_files = [
        f for f in os.listdir(clubs_reception_data_path)
        if os.path.isfile(os.path.join(clubs_reception_data_path, f)) and
        f.startswith('クラブ情報付き受付データ_受付') and f.endswith('.xlsx')
    ]
    # ファイル名の形式は「クラブ情報付き受付データ_受付YYYYMMDDHHMMSS_作成YYYYMMDDHHMMSS.xlsx」
    # クラブ情報付き受付データファイルを見つけたら、ファイル名の受付のYYYYMMDDHHMMSS形式でソート
    club_reception_data_files.sort(reverse=True)
    if not club_reception_data_files:
        logging.info("クラブ情報付き受付データファイルが見つかりません")
        latest_club_reception_data_file = None
    else:
        latest_club_reception_data_file = club_reception_data_files[0]
        logging.info(f"最新のクラブ情報付き受付データファイル: {latest_club_reception_data_file}")
    # 最新のクラブ情報付き受付データの作成日を取得（ファイル名のYYYYMMDDHHMMSS形式から）
    if latest_club_reception_data_file:
        latest_club_reception_data_date = latest_club_reception_data_file.split('_')[2].split('.')[0]
        # "作成20250702134214" から "作成" を除去
        latest_club_reception_data_date = latest_club_reception_data_date.replace('作成', '')
        latest_club_reception_data_date = pd.to_datetime(latest_club_reception_data_date, format='%Y%m%d%H%M%S')
        logging.info(f"最新のクラブ情報付き受付データの作成日: {latest_club_reception_data_date}")
        
        # 3. 最新のクラブ情報付き受付データを作成する必要があるかを判断
        if latest_club_reception_data_date >= latest_reception_data_date:
            logging.info("最新のクラブ情報付き受付データは既に最新です。処理を終了します。")
            return
    else:
        logging.info("クラブ情報付き受付データファイルが見つからないため、新規作成します。")
        latest_club_reception_data_date = None
    logging.info("クラブ情報付き受付データを作成します。処理を続行します。")

    # 4. 最新の処理済み受付データを読み込む（処理済み受付データ_受付{latest_reception_data_date}_処理YYYYMMDDHHMMSS.xlsx形式）
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
    # ファイル名形式: 処理済み受付データ_受付YYYYMMDDHHMMSS_処理YYYYMMDDHHMMSS.xlsx
    latest_processed_reception_data_date = latest_processed_reception_data_file.split('_')[1].replace('受付', '')
    latest_processed_reception_data_date = pd.to_datetime(latest_processed_reception_data_date, format='%Y%m%d%H%M%S')
    logging.info(f"最新の処理済み受付データの受付日: {latest_processed_reception_data_date}")
    # 最新の処理済み受付データを読み込む
    processed_reception_data_path = os.path.join(processed_reception_data_folder_path, latest_processed_reception_data_file)
    logging.info(f"最新の処理済み受付データを読み込みます: {processed_reception_data_path}")
    processed_reception_df = pd.read_excel(processed_reception_data_path)
    logging.info("最新の処理済み受付データを読み込みました")

    # 5. 最新のクラブ情報を読み込む（クラブ名_YYYYMMDD.xlsx形式）
    logging.info("最新のクラブ情報を読み込みます")
    club_info_df, latest_club_info_date = get_latest_club_info_file()
    if club_info_df is None:
        return

    # 6. 最新のクラブ情報と処理済み受付データをマージ
    # 基本は、club_info_dfの'選択肢（地区名：クラブ名：クラブ名（カタカナ））'とprocessed_reception_dfの'申請_クラブ名_選択'をキーにしてマージ
    # ただし、processed_reception_dfの'申請_クラブ名_選択'が「選択肢にない」の場合は行を追加＋'申請_クラブ名_テキスト'を'クラブ名'にコピー
    logging.info("最新のクラブ情報に処理済み受付データをマージします")
    
    # まず、受付データのある行のみを対象とする（申請_クラブ名_選択が空でない行）
    reception_data = processed_reception_df[processed_reception_df['申請_クラブ名_選択'].notna() & 
                                               (processed_reception_df['申請_クラブ名_選択'] != '')].copy()
    
    # 「選択肢にない」または「この中に無い」の場合と通常の選択肢の場合で処理を分ける
    # 通常の選択肢の場合：club_info_dfとマージ
    new_club_indicators = ['選択肢にない', 'この中に無い']
    normal_selection = reception_data[~reception_data['申請_クラブ名_選択'].isin(new_club_indicators)].copy()
    new_club_selection = reception_data[reception_data['申請_クラブ名_選択'].isin(new_club_indicators)].copy()
    
    logging.info(f"総受付データ行数: {len(reception_data)}")
    logging.info(f"通常選択の行数: {len(normal_selection)}")
    logging.info(f"新クラブ選択の行数: {len(new_club_selection)}")
    
    # 新クラブの詳細をログに出力
    if len(new_club_selection) > 0:
        logging.info("新クラブ申請の詳細:")
        for _, row in new_club_selection.iterrows():
            logging.info(f"  選択値: '{row['申請_クラブ名_選択']}', テキスト値: '{row['申請_クラブ名_テキスト']}'")
    
    # 通常の選択肢の場合のマージ
    clubs_reception_data_df = pd.merge(
        club_info_df,
        normal_selection,
        left_on='選択肢（地区名：クラブ名：クラブ名（カタカナ））',
        right_on='申請_クラブ名_選択',
        how='inner'  # 申請があったクラブのみ
    )
    logging.info(f"通常の選択肢でマージされた行数: {len(clubs_reception_data_df)}")
    
    # 「選択肢にない」または「この中に無い」の場合の処理
    if len(new_club_selection) > 0:
        logging.info(f"新クラブ申請（「選択肢にない」または「この中に無い」）の行数: {len(new_club_selection)}")
        
        # 新しいクラブの行を作成
        for index, row in new_club_selection.iterrows():
            logging.info(f"新クラブの行を追加中: {row['申請_クラブ名_テキスト']}")
            new_row = row.copy()
            # クラブ情報の列は空またはデフォルト値を設定
            new_row['地区名'] = ''  # または適切なデフォルト値
            new_row['クラブ名'] = row['申請_クラブ名_テキスト']  # テキスト入力をクラブ名として使用
            new_row['クラブ名（カタカナ）'] = ''  # または適切なデフォルト値
            new_row['選択肢（地区名：クラブ名：クラブ名（カタカナ））'] = row['申請_クラブ名_選択']  # 元の選択値を保持
            new_row['R7年度登録クラブ'] = 0  # 新しいクラブなので0
            
            # DataFrameに追加する前の行数
            before_count = len(clubs_reception_data_df)
            
            # DataFrameに追加
            clubs_reception_data_df = pd.concat([clubs_reception_data_df, new_row.to_frame().T], ignore_index=True)
            
            # DataFrameに追加した後の行数
            after_count = len(clubs_reception_data_df)
            logging.info(f"行追加前: {before_count}, 行追加後: {after_count}")
        
        logging.info(f"新クラブ申請を追加後の総行数: {len(clubs_reception_data_df)}")
    else:
        logging.info("新クラブ申請（「選択肢にない」または「この中に無い」）は見つかりませんでした")
    
    logging.info(f"マージ完了。最終的な行数: {len(clubs_reception_data_df)}")
    
    # 7. マージしたデータを保存
    current_time = get_jst_now()
    timestamp = current_time.strftime('%Y%m%d%H%M%S')
    reception_timestamp = latest_processed_reception_data_date.strftime('%Y%m%d%H%M%S')
    
    clubs_reception_data_file_name = f"クラブ情報付き受付データ_受付{reception_timestamp}_作成{timestamp}.xlsx"
    clubs_reception_data_file_path = os.path.join(clubs_reception_data_path, clubs_reception_data_file_name)
    
    clubs_reception_data_df.to_excel(clubs_reception_data_file_path, index=False)
    logging.info(f"クラブ情報付き受付データを保存しました: {clubs_reception_data_file_path}")