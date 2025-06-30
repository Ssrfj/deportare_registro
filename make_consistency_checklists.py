'''
    #このファイルでは使わない関数（これを参考に新たな関数を作成する）
    from make_document01_checklist import make_document01_checklist
    from make_document02_1_checklist import make_document02_1_checklist
    from make_document02_2_checklist import make_document02_2_checklist
    from make_document03_checklist import make_document03_checklist
    from make_document04_checklist import make_document04_checklist
    from make_document05_plan_checklist import make_document05_plan_checklist
    from make_document05_budget_checklist import make_document05_budget_checklist
    from make_document06_report_checklist import make_document06_report_checklist
    from make_document06_financial_statements_checklist import make_document06_financial_statements_checklist
    from make_document07_checklist import make_document07_checklist
    from make_document08_checklist import make_document08_checklist
    from make_document09_checklist import make_document09_checklist
    from make_document10_checklist import make_document10_checklist
'''

def make_consistency_checklists(latest_reception_data_date):
    import os
    import logging
    import pandas as pd

    from setting_paths import content_check_folder_path
    from utils import get_jst_now
    from make_folders import setup_logging, create_folders

    from make_consistency_checklist_members_and_voting_rights import make_consistency_checklist_members_and_voting_rights
    from make_consistency_checklist_disciplines import make_consistency_checklist_disciplines
    from make_consistency_checklist_signatures import make_consistency_checklist_signatures

    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()
    logging.info("フォルダを作成しました")

    latest_reception_data_date = pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S').strftime('%Y%m%d%H%M%S')

    # 1. 最新のクラブ情報付き受付データファイルを取得(クラブ情報付き受付データ_受付{latest_reception_data_date}_*.xlsxを使用)
    logging.info("最新のクラブ情報付き受付データファイルを取得します")
    # 最新のクラブ情報付き受付データと同じ日付のファイルを取得
    if not latest_reception_data_date:
        logging.error("最新の受付データの日付が指定されていません")
        return
    
    latest_club_reception_files = [
        f for f in os.listdir(content_check_folder_path)
        if os.path.isfile(os.path.join(content_check_folder_path, f)) and
        f.startswith(f'クラブ情報付き受付データ_受付{latest_reception_data_date}') and f.endswith('.xlsx')
    ]
    latest_club_reception_files.sort(reverse=True)
    if not latest_club_reception_files:
        logging.error(f"クラブ情報付き受付データファイルが見つかりません: クラブ情報付き受付データ_受付{latest_reception_data_date}*.xlsx")
        return
    latest_club_reception_file = latest_club_reception_files[0]
    logging.info(f"最新のクラブ情報付き受付データファイル: {latest_club_reception_file}")
    club_reception_df = pd.read_excel(os.path.join(content_check_folder_path, latest_club_reception_file))
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

    # 議事録への署名の一貫性チェックリストを作成 # 03と08の議事録への署名との一貫性をチェック
    logging.info("議事録への署名の一貫性チェックリストを作成します")
    make_consistency_checklist_signatures(latest_reception_data_date)
    logging.info("議事録への署名の一貫性チェックリストを作成しました")

    logging.info("一貫性のチェックリストを作成しました")

    