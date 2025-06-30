def make_chacklists(latest_reception_data_date):
    import os
    import pandas as pd
    import logging
    from setting_paths import content_check_folder_path, reception_statues_folder_path
    from utils import get_jst_now
    from make_folders import setup_logging, create_folders
    from make_overall_checklist import make_overall_checklist
    from make_documents_checklists import make_documents_checklists
    from make_consistency_checklists import make_consistency_checklists

    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()
    logging.info("フォルダを作成しました")

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

'''今後の作業memo
作るファイル
一貫性のチェックリスト
基準に適合しているかのチェックリスト
クラブごと＊書類ごとの詳細なデータ
※ファイルについては処理ごとに、また別のPythonファイルを作る
'''