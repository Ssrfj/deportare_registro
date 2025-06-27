def make_documents_checklists(latest_reception_data_date):
    import os
    import logging
    import pandas as pd

    from setting import content_check_folder_path
    from utils import get_jst_now
    from make_folders import setup_logging, create_folders
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

    # 2. 書類ごとのチェックリストを作成
    logging.info("書類ごとのチェックリストを作成します")
    # 書類1のチェックリストを作成
    logging.info("書類01のチェックリストを作成します")
    make_document01_checklist(latest_reception_data_date)
    logging.info("書類01のチェックリストを作成しました")

    # 書類2-1のチェックリストを作成
    logging.info("書類02-1のチェックリストを作成します")
    make_document02_1_checklist(latest_reception_data_date)
    logging.info("書類02-1のチェックリストを作成しました")

    # 書類2-2のチェックリストを作成
    logging.info("書類02-2のチェックリストを作成します")
    make_document02_2_checklist(latest_reception_data_date)
    logging.info("書類02-2のチェックリストを作成しました")

    # 書類3のチェックリストを作成
    logging.info("書類03のチェックリストを作成します")
    make_document03_checklist(latest_reception_data_date)
    logging.info("書類03のチェックリストを作成しました")

    # 書類4のチェックリストを作成
    logging.info("書類04のチェックリストを作成します")
    make_document04_checklist(latest_reception_data_date)
    logging.info("書類04のチェックリストを作成しました")

    # 書類5の計画書チェックリストを作成
    logging.info("書類05の計画書チェックリストを作成します")
    make_document05_plan_checklist(latest_reception_data_date)
    logging.info("書類05の計画書チェックリストを作成しました")

    # 書類5の予算書チェックリストを作成
    logging.info("書類05の予算書チェックリストを作成します")
    make_document05_budget_checklist(latest_reception_data_date)
    logging.info("書類05の予算書チェックリストを作成しました")

    # 書類6の報告書チェックリストを作成
    logging.info("書類06の報告書チェックリストを作成します")
    make_document06_report_checklist(latest_reception_data_date)
    logging.info("書類06の報告書チェックリストを作成しました")

    # 書類6の決算書チェックリストを作成
    logging.info("書類06の決算書チェックリストを作成します")
    make_document06_financial_statements_checklist(latest_reception_data_date)
    logging.info("書類06の決算書チェックリストを作成しました" )

    # 書類7のチェックリストを作成
    logging.info("書類07のチェックリストを作成します")
    make_document07_checklist(latest_reception_data_date)
    logging.info("書類07のチェックリストを作成しました")

    # 書類8のチェックリストを作成
    logging.info("書類08のチェックリストを作成します")
    make_document08_checklist(latest_reception_data_date)
    logging.info("書類08のチェックリストを作成しました")

    # 書類9のチェックリストを作成
    logging.info("書類09のチェックリストを作成します")
    make_document09_checklist(latest_reception_data_date)
    logging.info("書類09のチェックリストを作成しました")

    # 書類10のチェックリストを作成
    logging.info("書類10のチェックリストを作成します")
    make_document10_checklist(latest_reception_data_date)
    logging.info("書類10のチェックリストを作成しました")
    logging.info("書類ごとのチェックリストを作成しました")