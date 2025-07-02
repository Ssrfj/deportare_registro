def make_detailed_data_folders():
    import os
    import pandas as pd
    import logging
    from setting_paths import application_statues_folder_path, clubs_reception_data_path, content_check_folder_path, clubs_details_data_folder_path
    from utils import get_jst_now
    from make_folders import setup_logging, create_folders

    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()
    logging.info("フォルダを作成しました")

    # 1. 最新のクラブ情報付き申請データのファイルを取得
    logging.info("最新のクラブ情報付き申請データのファイルを取得します")
    latest_club_reception_files = [
        f for f in os.listdir(clubs_reception_data_path)
        if os.path.isfile(os.path.join(clubs_reception_data_path, f)) and
        f.startswith('クラブ情報付き申請データ_') and f.endswith('.xlsx')
    ]
    latest_club_reception_files.sort(reverse=True)
    if not latest_club_reception_files:
        logging.error("クラブ情報付き申請データファイルが見つかりません")
        return
    latest_club_reception_file = latest_club_reception_files[0]
    latest_club_reception_date = latest_club_reception_file.split('_')[1].replace('申請', '')
    latest_club_reception_date = pd.to_datetime(latest_club_reception_date, format='%Y%m%d%H%M%S')
    logging.info(f"最新のクラブ情報付き申請データファイル: {latest_club_reception_file}")
    club_reception_df = pd.read_excel(os.path.join(clubs_reception_data_path, latest_club_reception_file))
    logging.info(f"最新のクラブ情報付き申請データを読み込みました: {latest_club_reception_file}")

    # 2. 申請しているクラブのリストを取得
    logging.info("申請しているクラブのリストを取得します")
    applied_clubs = club_reception_df['クラブ名'].unique()
    if len(applied_clubs) == 0:
        logging.error("申請しているクラブが見つかりません")
        return
    logging.info(f"申請しているクラブ数: {len(applied_clubs)}")

    # 3. 各クラブの詳細フォルダをclubs_details_data_folder_pathの下に作成
    logging.info("各クラブの詳細フォルダを作成します")
    for club_name in applied_clubs:
        club_folder_name = f"{club_name}_申請内容チェック"
        club_folder_path = os.path.join(clubs_details_data_folder_path, club_folder_name)
        if not os.path.exists(club_folder_path):
            os.makedirs(club_folder_path)
            logging.info(f"クラブフォルダを作成しました: {club_folder_path}")
        else:
            logging.info(f"クラブフォルダは既に存在します: {club_folder_path}")