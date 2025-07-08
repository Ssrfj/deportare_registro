def make_consistency_checklists(latest_reception_data_date):
    import os
    import logging
    import pandas as pd

    from src.core.setting_paths import content_check_folder_path, clubs_reception_data_path
    from src.core.utils import get_jst_now

    from src.checklist.consistency.make_consistency_checklist_members_and_voting_rights import make_consistency_checklist_members_and_voting_rights
    from src.checklist.consistency.make_consistency_checklist_disciplines import make_consistency_checklist_disciplines
    from src.checklist.consistency.make_consistency_checklist_meeting_minutes import make_consistency_checklist_meeting_minutes

    latest_reception_data_date = pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S').strftime('%Y%m%d%H%M%S')

    # 1. 最新のクラブ情報付き受付データファイルを取得(クラブ情報付き受付データ_受付{latest_reception_data_date}_*.xlsxを使用)
    logging.info("最新のクラブ情報付き受付データファイルを取得します")
    # 最新のクラブ情報付き受付データと同じ日付のファイルを取得
    if not latest_reception_data_date:
        logging.error("最新の受付データの日付が指定されていません")
        return
    
    logging.info(f"検索パス: {clubs_reception_data_path}")
    logging.info(f"検索パターン: クラブ情報付き受付データ_受付{latest_reception_data_date}*.xlsx")
    
    # パスが存在するか確認
    if not os.path.exists(clubs_reception_data_path):
        logging.error(f"クラブ情報付き受付データのパスが存在しません: {clubs_reception_data_path}")
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

    # 2. 一貫性のチェックリストを作成
    logging.info("一貫性のチェックリストを作成します")
    
    # 会員と議決権保有者の一貫性チェックリストを作成 #02-1と05、06の人数（会費収入）との一貫性をチェック
    logging.info("会員と議決権保有者の一貫性チェックリストを作成します")
    make_consistency_checklist_members_and_voting_rights(latest_reception_data_date)
    logging.info("会員と議決権保有者の一貫性チェックリストを作成しました")

    # 活動種目の一貫性チェックリストを作成 # 02-2と05、06の活動種目との一貫性をチェック
    logging.info("活動種目の一貫性チェックリストを作成します")
    make_consistency_checklist_disciplines(latest_reception_data_date)
    logging.info("活動種目の一貫性チェックリストを作成しました")

    # 議事録の一貫性チェックリストを作成 # 03と08の議事録の一貫性をチェック
    logging.info("議事録の一貫性チェックリストを作成します")
    make_consistency_checklist_meeting_minutes(latest_reception_data_date)
    logging.info("議事録の一貫性チェックリストを作成しました")

    logging.info("一貫性のチェックリストを作成しました")