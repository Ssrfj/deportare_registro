def make_documents_checklists(latest_reception_data_date):
    import os
    import logging
    import pandas as pd

    from src.core.setting_paths import content_check_folder_path, clubs_reception_data_path
    from src.core.utils import get_jst_now
    from src.checklist.generators.documents.make_document01_checklist import make_document01_checklist
    from src.checklist.generators.documents.make_document02_1_checklist import make_document02_1_checklist
    from src.checklist.generators.documents.make_document02_2_checklist import make_document02_2_checklist
    from src.checklist.generators.documents.make_document03_checklist import make_document03_checklist
    from src.checklist.generators.documents.make_document04_checklist import make_document04_checklist
    from src.checklist.generators.documents.make_document05_plan_checklist import make_document05_plan_checklist
    from src.checklist.generators.documents.make_document05_budget_checklist import make_document05_budget_checklist
    from src.checklist.generators.documents.make_document06_report_checklist import make_document06_report_checklist
    from src.checklist.generators.documents.make_document06_financial_statements_checklist import make_document06_financial_statements_checklist
    from src.checklist.generators.documents.make_document07_checklist import make_document07_checklist
    from src.checklist.generators.documents.make_document08_checklist import make_document08_checklist
    from src.checklist.generators.documents.make_document09_checklist import make_document09_checklist
    from src.checklist.generators.documents.make_document10_checklist import make_document10_checklist

    # latest_reception_data_dateが既にdatetimeオブジェクトの場合は文字列に変換
    if isinstance(latest_reception_data_date, pd.Timestamp) or hasattr(latest_reception_data_date, 'strftime'):
        latest_reception_data_date_str = latest_reception_data_date.strftime('%Y%m%d%H%M%S')
    else:
        # 文字列の場合はそのまま使用
        latest_reception_data_date_str = str(latest_reception_data_date)
    
    logging.info(f"受付データの日付: {latest_reception_data_date_str}")

    # 1. 最新のクラブ情報付き受付データファイルを取得(クラブ情報付き受付データ_受付{latest_reception_data_date_str}_*.xlsxを使用)
    logging.info("最新のクラブ情報付き受付データファイルを取得します")
    # 最新のクラブ情報付き受付データと同じ日付のファイルを取得
    if not latest_reception_data_date_str:
        logging.error("最新の受付データの日付が指定されていません")
        return
    
    latest_club_reception_files = [
        f for f in os.listdir(clubs_reception_data_path)
        if os.path.isfile(os.path.join(clubs_reception_data_path, f)) and
        f.startswith(f'クラブ情報付き受付データ_受付{latest_reception_data_date_str}') and f.endswith('.xlsx')
    ]
    latest_club_reception_files.sort(reverse=True)
    if not latest_club_reception_files:
        logging.error(f"クラブ情報付き受付データファイルが見つかりません: クラブ情報付き受付データ_受付{latest_reception_data_date_str}*.xlsx")
        return
    latest_club_reception_file = latest_club_reception_files[0]
    logging.info(f"最新のクラブ情報付き受付データファイル: {latest_club_reception_file}")
    club_reception_df = pd.read_excel(os.path.join(clubs_reception_data_path, latest_club_reception_file))
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