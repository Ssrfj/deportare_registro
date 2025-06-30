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

    from setting import content_check_folder_path
    from utils import get_jst_now
    from make_folders import setup_logging, create_folders

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
    
    # 書類01を軸とした一貫性チェックリストを作成
    logging.info("書類01のチェックリストを作成します")
    # 書類01to02_2のチェックリストを作成
    logging.info("書類01と書類02-2の一貫性チェックリストを作成します")
    make_consistency_checklist_01_to_02_2(latest_reception_data_date)
    logging.info("書類01と書類02-2の一貫性チェックリストを作成しました")

    # 書類01to03のチェックリストを作成
    logging.info("書類01と書類03の一貫性チェックリストを作成します")
    make_consistency_checklist_01_to_03(latest_reception_data_date)
    logging.info("書類01と書類03の一貫性チェックリストを作成しました")

    # 書類01to07のチェックリストを作成
    logging.info("書類01と書類07の一貫性チェックリストを作成します")
    make_consistency_checklist_01_to_07(latest_reception_data_date)
    logging.info("書類01と書類07の一貫性チェックリストを作成しました")

    # 書類01to08のチェックリストを作成
    logging.info("書類01と書類08の一貫性チェックリストを作成します")
    make_consistency_checklist_01_to_08(latest_reception_data_date)
    logging.info("書類01と書類08の一貫性チェックリストを作成しました")

    # 書類01to09のチェックリストを作成
    logging.info("書類01と書類09の一貫性チェックリストを作成します")
    make_consistency_checklist_01_to_09(latest_reception_data_date)
    logging.info("書類01と書類09の一貫性チェックリストを作成しました")

    # 書類01to10のチェックリストを作成
    logging.info("書類01と書類10の一貫性チェックリストを作成します")
    make_consistency_checklist_01_to_10(latest_reception_data_date)
    logging.info("書類01と書類10の一貫性チェックリストを作成しました")

    logging.info("書類01を軸とした一貫性チェックリストを作成しました")

    # 書類02_1を軸とした一貫性チェックリストを作成
    logging.info("書類02-1を軸とした一貫性チェックリストを作成します")

    # 書類02_1to03のチェックリストを作成
    logging.info("書類02-1と書類03の一貫性チェックリストを作成します")
    make_consistency_checklist_02_1_to_03(latest_reception_data_date)
    logging.info("書類02-1と書類03の一貫性チェックリストを作成しました")

    # 書類02_1to04のチェックリストを作成
    logging.info("書類02-1と書類04の一貫性チェックリストを作成します")
    make_consistency_checklist_02_1_to_04(latest_reception_data_date)
    logging.info("書類02-1と書類04の一貫性チェックリストを作成しました")

    # 書類02_1to05_planのチェックリストを作成
    logging.info("書類02-1と書類05の計画書の一貫性チェックリストを作成します")
    make_consistency_checklist_02_1_to_05_plan(latest_reception_data_date)
    logging.info("書類02-1と書類05の計画書の一貫性チェックリストを作成しました")

    # 書類02_1to05_budgetのチェックリストを作成
    logging.info("書類02-1と書類05の予算書の一貫性チェックリストを作成します")
    make_consistency_checklist_02_1_to_05_budget(latest_reception_data_date)
    logging.info("書類02-1と書類05の予算書の一貫性チェックリストを作成しました")

    # 書類02_1to06_reportのチェックリストを作成
    logging.info("書類02-1と書類06の報告書の一貫性チェックリストを作成します")
    make_consistency_checklist_02_1_to_06_report(latest_reception_data_date)
    logging.info("書類02-1と書類06の報告書の一貫性チェックリストを作成しました")

    # 書類02_1to06_financial_statementsのチェックリストを作成
    logging.info("書類02-1と書類06の決算書の一貫性チェックリストを作成します")
    make_consistency_checklist_02_1_to_06_financial_statements(latest_reception_data_date)
    logging.info("書類02-1と書類06の決算書の一貫性チェックリストを作成しました")

    # 書類02_1to07のチェックリストを作成
    logging.info("書類02-1と書類07の一貫性チェックリストを作成します")
    make_consistency_checklist_02_1_to_07(latest_reception_data_date)
    logging.info("書類02-1と書類07の一貫性チェックリストを作成しました")

    # 書類02_1to08のチェックリストを作成
    logging.info("書類02-1と書類08の一貫性チェックリストを作成します")
    make_consistency_checklist_02_1_to_08(latest_reception_data_date)
    logging.info("書類02-1と書類08の一貫性チェックリストを作成しました")

    logging.info("書類02-1を軸とした一貫性チェックリストを作成しました")

    # 書類02_2を軸とした一貫性チェックリストを作成
    logging.info("書類02-2を軸とした一貫性チェックリストを作成します")

    # 書類02_2to05_planのチェックリストを作成
    logging.info("書類02-2と書類05の計画書の一貫性チェックリストを作成します")
    make_consistency_checklist_02_2_to_05_plan(latest_reception_data_date)
    logging.info("書類02-2と書類05の計画書の一貫性チェックリストを作成しました")

    # 書類02_2to05_budgetのチェックリストを作成
    logging.info("書類02-2と書類05の予算書の一貫性チェックリストを作成します")
    make_consistency_checklist_02_2_to_05_budget(latest_reception_data_date)
    logging.info("書類02-2と書類05の予算書の一貫性チェックリストを作成しました")

    # 書類02_2to06_reportのチェックリストを作成
    logging.info("書類02-2と書類06の報告書の一貫性チェックリストを作成します")
    make_consistency_checklist_02_2_to_06_report(latest_reception_data_date)
    logging.info("書類02-2と書類06の報告書の一貫性チェックリストを作成しました")

    # 書類02_2to06_financial_statementsのチェックリストを作成
    logging.info("書類02-2と書類06の決算書の一貫性チェックリストを作成します")
    make_consistency_checklist_02_2_to_06_financial_statements(latest_reception_data_date)
    logging.info("書類02-2と書類06の決算書の一貫性チェックリストを作成しました")

    # 書類02_2to08のチェックリストを作成
    logging.info("書類02-2と書類08の一貫性チェックリストを作成します")
    make_consistency_checklist_02_2_to_08(latest_reception_data_date)
    logging.info("書類02-2と書類08の一貫性チェックリストを作成しました")

    logging.info("書類02-2を軸とした一貫性チェックリストを作成しました")

    # 書類03を軸とした一貫性チェックリストを作成
    logging.info("書類03を軸とした一貫性チェックリストを作成します")

    # 書類03to04のチェックリストを作成
    logging.info("書類03と書類04の一貫性チェックリストを作成します")
    make_consistency_checklist_03_to_04(latest_reception_data_date)
    logging.info("書類03と書類04の一貫性チェックリストを作成しました")

    # 書類03to08のチェックリストを作成
    logging.info("書類03と書類08の一貫性チェックリストを作成します")
    make_consistency_checklist_03_to_08(latest_reception_data_date)
    logging.info("書類03と書類08の一貫性チェックリストを作成しました")

    # 書類03to09のチェックリストを作成
    logging.info("書類03と書類09の一貫性チェックリストを作成します")
    make_consistency_checklist_03_to_09(latest_reception_data_date)
    logging.info("書類03と書類09の一貫性チェックリストを作成しました")

    logging.info("書類03を軸とした一貫性チェックリストを作成しました")

    # 書類04を軸とした一貫性チェックリストを作成
    logging.info("書類04を軸とした一貫性チェックリストを作成します")

    # 書類04to08のチェックリストを作成
    logging.info("書類04と書類08の一貫性チェックリストを作成します")
    make_consistency_checklist_04_to_08(latest_reception_data_date)
    logging.info("書類04と書類08の一貫性チェックリストを作成しました")

    logging.info("書類04を軸とした一貫性チェックリストを作成しました")

    # 書類05_planを軸とした一貫性チェックリストを作成
    logging.info("書類05の計画書を軸とした一貫性チェックリストを作成します")
    # 書類05_planto05_budgetのチェックリストを作成
    logging.info("書類05の計画書と予算書の一貫性チェックリストを作成します")
    make_consistency_checklist_05_plan_to_05_budget(latest_reception_data_date)
    logging.info("書類05の計画書と予算書の一貫性チェックリストを作成しました")

    # 書類05_planto06_reportのチェックリストを作成
    logging.info("書類05の計画書と報告書の一貫性チェックリストを作成します")
    make_consistency_checklist_05_plan_to_06_report(latest_reception_data_date)
    logging.info("書類05の計画書と報告書の一貫性チェックリストを作成しました")

    # 書類05_planto06_financial_statementsのチェックリストを作成
    logging.info("書類05の計画書と決算書の一貫性チェックリストを作成します")
    make_consistency_checklist_05_plan_to_06_financial_statements(latest_reception_data_date)
    logging.info("書類05の計画書と決算書の一貫性チェックリストを作成しました")

    # 書類05_planto08のチェックリストを作成
    logging.info("書類05の計画書と書類08の一貫性チェックリストを作成します")
    make_consistency_checklist_05_plan_to_08(latest_reception_data_date)
    logging.info("書類05の計画書と書類08の一貫性チェックリストを作成しました")

    logging.info("書類05の計画書を軸とした一貫性チェックリストを作成しました")

    # 書類05_budgetを軸とした一貫性チェックリストを作成
    logging.info("書類05の予算書を軸とした一貫性チェックリストを作成します")
    # 書類05_budgetto06_reportのチェックリストを作成
    logging.info("書類05の予算書と報告書の一貫性チェックリストを作成します")
    make_consistency_checklist_05_budget_to_06_report(latest_reception_data_date)
    logging.info("書類05の予算書と報告書の一貫性チェックリストを作成しました")

    # 書類05_budgetto06_financial_statementsのチェックリストを作成
    logging.info("書類05の予算書と決算書の一貫性チェックリストを作成します")
    make_consistency_checklist_05_budget_to_06_financial_statements(latest_reception_data_date)
    logging.info("書類05の予算書と決算書の一貫性チェックリストを作成しました")

    # 書類05_budgetto08のチェックリストを作成
    logging.info("書類05の予算書と書類08の一貫性チェックリストを作成します")
    make_consistency_checklist_05_budget_to_08(latest_reception_data_date)
    logging.info("書類05の予算書と書類08の一貫性チェックリストを作成しました")

    logging.info("書類05の予算書を軸とした一貫性チェックリストを作成しました")

    # 書類06_reportを軸とした一貫性チェックリストを作成
    logging.info("書類06の報告書を軸とした一貫性チェックリストを作成します")
    # 書類06_reportto06_financial_statementsのチェックリストを作成
    logging.info("書類06の報告書と決算書の一貫性チェックリストを作成します")
    make_consistency_checklist_06_report_to_06_financial_statements(latest_reception_data_date)
    logging.info("書類06の報告書と決算書の一貫性チェックリストを作成しました")

    # 書類06_reportto08のチェックリストを作成
    logging.info("書類06の報告書と書類08の一貫性チェックリストを作成します")
    make_consistency_checklist_06_report_to_08(latest_reception_data_date)
    logging.info("書類06の報告書と書類08の一貫性チェックリストを作成しました")

    logging.info("書類06の報告書を軸とした一貫性チェックリストを作成しました")

    # 書類06_financial_statementsを軸とした一貫性チェックリストを作成
    logging.info("書類06の決算書を軸とした一貫性チェックリストを作成します")
    # 書類06_financial_statementsto07のチェックリストを作成
    logging.info("書類06の決算書と書類07の一貫性チェックリストを作成します")
    make_consistency_checklist_06_financial_statements_to_07(latest_reception_data_date)
    logging.info("書類06の決算書と書類07の一貫性チェックリストを作成しました")

    # 書類06_financial_statementsto08のチェックリストを作成
    logging.info("書類06の決算書と書類08の一貫性チェックリストを作成します")
    make_consistency_checklist_06_financial_statements_to_08(latest_reception_data_date)
    logging.info("書類06の決算書と書類08の一貫性チェックリストを作成しました")

    logging.info("書類06の決算書を軸とした一貫性チェックリストを作成しました")
    
    logging.info("書類09を軸とした一貫性チェックリストを作成しました")
    logging.info("書類ごとの一貫性チェックリストを作成しました")