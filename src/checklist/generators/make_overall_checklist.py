def make_overall_checklist(latest_reception_data_date):
    import os
    import pandas as pd
    import logging
    from src.core.setting_paths import content_check_folder_path, settting_folder_path, overall_checklist_folder_path, clubs_reception_data_path
    from src.core.utils import get_jst_now
    from src.folder_management.make_folders import setup_logging, create_folders


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
    logging.info(f"検索パス: {clubs_reception_data_path}")
    logging.info(f"検索パターン: クラブ情報付き受付データ_受付{latest_reception_data_date}*.xlsx")
    
    # パスが存在するか確認
    if not os.path.exists(clubs_reception_data_path):
        logging.error(f"クラブ情報付き受付データのパスが存在しません: {clubs_reception_data_path}")
        return
    
    # パス内のファイル一覧を取得してデバッグ
    try:
        all_files = os.listdir(clubs_reception_data_path)
        logging.info(f"パス内のファイル数: {len(all_files)}")
        xlsx_files = [f for f in all_files if f.endswith('.xlsx')]
        logging.info(f"Excelファイル数: {len(xlsx_files)}")
        club_info_files = [f for f in xlsx_files if 'クラブ情報付き受付データ' in f]
        logging.info(f"クラブ情報付き受付データファイル数: {len(club_info_files)}")
        for f in club_info_files:
            logging.info(f"見つかったファイル: {f}")
    except Exception as e:
        logging.error(f"ファイル一覧取得エラー: {e}")
        return
    
    latest_club_reception_files = [
        f for f in os.listdir(clubs_reception_data_path)
        if os.path.isfile(os.path.join(clubs_reception_data_path, f)) and
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

    # 2. 総合チェックリストのカラム名を取得
    logging.info("総合チェックリストのカラム名を取得します")
    # jsonファイルを読み込む（overall_checklist_columns.jsonが必要）
    from src.core.utils import get_config_file_path
    overall_checklist_columns_file_path = get_config_file_path('config/checklist_columns/overall_checklist_columns.json')
    if not os.path.exists(overall_checklist_columns_file_path):
        logging.error(f"総合チェックリストのカラム名ファイルが見つかりません: {overall_checklist_columns_file_path}")
        return
    overall_checklist_columns = pd.read_json(overall_checklist_columns_file_path, orient='records')
    logging.info(f"総合チェックリストのカラム名を読み込みました: {overall_checklist_columns_file_path}")

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
        overall_checklist_df.loc[index, '受付日時'] = row['申請_タイムスタンプ']
        overall_checklist_df.loc[index, '担当者名'] = row['申請_申請担当者名']
        overall_checklist_df.loc[index, '担当者役職名'] = row['申請_申請担当者役職']
        overall_checklist_df.loc[index, 'メールアドレス'] = row['申請_メールアドレス']
        overall_checklist_df.loc[index, '電話番号'] = row['申請_TEL']
        overall_checklist_df.loc[index, 'FAX番号'] = row['申請_FAX(任意)']
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