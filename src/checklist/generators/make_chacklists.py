def make_chacklists(latest_reception_data_date):
    import os
    import pandas as pd
    import logging
    from src.core.setting_paths import content_check_folder_path, application_statues_folder_path, clubs_reception_data_path
    from src.core.utils import get_jst_now
    from src.folder_management.make_folders import setup_logging, create_folders
    from src.checklist.generators.make_overall_checklist import make_overall_checklist
    from src.checklist.generators.documents.make_documents_checklists import make_documents_checklists
    from src.checklist.consistency.make_consistency_checklists import make_consistency_checklists
    from src.data_processing.make_detailed_club_data import make_detailed_club_data

    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()
    logging.info("フォルダを作成しました")

    # 1. 最新のクラブ情報付き受付データファイルを取得
    logging.info("最新のクラブ情報付き受付データファイルを取得します")
    latest_club_reception_files = [
        f for f in os.listdir(clubs_reception_data_path)
        if os.path.isfile(os.path.join(clubs_reception_data_path, f)) and
        f.startswith('クラブ情報付き申請データ_') and f.endswith('.xlsx')
    ]
    latest_club_reception_files.sort(reverse=True)
    if not latest_club_reception_files:
        logging.error("クラブ情報付き受付データファイルが見つかりません")
        return
    latest_club_reception_file = latest_club_reception_files[0]
    latest_club_reception_date = latest_club_reception_file.split('_')[1].replace('申請', '')
    latest_club_reception_date = pd.to_datetime(latest_club_reception_date, format='%Y%m%d%H%M%S')
    logging.info(f"最新のクラブ情報付き受付データファイル: {latest_club_reception_file}")
    club_reception_df = pd.read_excel(os.path.join(clubs_reception_data_path, latest_club_reception_file))
    logging.info(f"最新のクラブ情報付き受付データを読み込みました: {latest_club_reception_file}")

    # 2. クラブごとの詳細データ保存するためのフォルダを作成
    logging.info("クラブごとの詳細データ保存フォルダを作成します")
    club_names = club_reception_df['クラブ名'].unique()
    for club_name in club_names:
        club_folder_name = f"{club_name}_詳細データ"
        club_folder_path = os.path.join(content_check_folder_path, club_folder_name)
        if not os.path.exists(club_folder_path):
            os.makedirs(club_folder_path)
            logging.info(f"クラブフォルダを作成しました: {club_folder_path}")
        else:
            logging.info(f"クラブフォルダは既に存在します: {club_folder_path}")
    logging.info("クラブごとの詳細データ保存フォルダを作成しました")

    # 4. （総合の）チェックリストの作成
    logging.info("総合のチェックリストを作成します")
    make_overall_checklist(latest_reception_data_date)
    logging.info("総合のチェックリストを作成しました")

    # 5. 書類ごとのチェックリスト
    logging.info("書類ごとのチェックリストを作成します")
    make_documents_checklists(latest_reception_data_date)
    logging.info("書類ごとのチェックリストを作成しました")

    # 6. 書類間の一貫性チェックリストの作成
    logging.info("書類間の一貫性チェックリストを作成します")
    make_consistency_checklists(latest_reception_data_date)
    logging.info("書類間の一貫性チェックリストを作成しました")

    # 7. クラブごとの詳細なデータを保存
    logging.info("クラブごとの詳細なデータを保存します")
    make_detailed_club_data(club_reception_df)
    logging.info("クラブごとの詳細なデータを保存しました")

    # 8. 最新のクラブ情報付き受付データファイルの更新日時を記録
    logging.info("最新のクラブ情報付き受付データファイルの更新日時を記録します")
    latest_reception_data_date = get_jst_now()
    latest_reception_data_file_path = os.path.join(application_statues_folder_path, 'latest_reception_data_date.txt')
    with open(latest_reception_data_file_path, 'w') as f:
        f.write(latest_reception_data_date.strftime('%Y-%m-%d %H:%M:%S'))
    logging.info(f"最新のクラブ情報付き受付データファイルの更新日時を記録しました: {latest_reception_data_date}")
    logging.info("チェックリストの作成が完了しました")