def automation_check_and_update_checklist(latest_reception_data_date):
    import os
    import pandas as pd
    import logging
    from src.core.setting_paths import content_check_folder_path, application_statues_folder_path, clubs_reception_data_path, overall_checklist_folder_path
    from src.core.utils import get_jst_now
    from src.folder_management.make_folders import setup_logging, create_folders
    from src.checklist.generators.make_overall_checklist import make_overall_checklist
    from src.checklist.generators.documents.make_documents_checklists import make_documents_checklists
    from src.checklist.consistency.make_consistency_checklists import make_consistency_checklists
    from src.data_processing.make_detailed_club_data import make_detailed_club_data
    from src.checklist.automation.auto_check import auto_check
    from src.checklist.automation.update_document_check_status import update_document_check_status
    from src.checklist.automation.update_consistency_check_status import update_consistency_check_status

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
        f.startswith('クラブ情報付き受付データ_') and f.endswith('.xlsx')
    ]
    latest_club_reception_files.sort(reverse=True)
    if not latest_club_reception_files:
        logging.error("クラブ情報付き受付データファイルが見つかりません")
        return
    latest_club_reception_file = latest_club_reception_files[0]
    latest_club_reception_date = latest_club_reception_file.split('_')[1].replace('受付', '')
    latest_club_reception_date = pd.to_datetime(latest_club_reception_date, format='%Y%m%d%H%M%S')
    logging.info(f"最新のクラブ情報付き受付データファイル: {latest_club_reception_file}")
    club_reception_df = pd.read_excel(os.path.join(clubs_reception_data_path, latest_club_reception_file))
    logging.info(f"最新のクラブ情報付き受付データを読み込みました: {latest_club_reception_file}")

    # 2. 最新の総合チェックリストの読み込み（overall_checklist_folder_path、ファイル名は「総合チェックリスト_受付{YYYYMMDDHHMMSS}_更新{YYYYMMDDHHMMSS}.xlsx」）
    logging.info("総合チェックリストのファイルを読み込みます")
    overall_checklist_files = [
        f for f in os.listdir(overall_checklist_folder_path)
        if os.path.isfile(os.path.join(overall_checklist_folder_path, f)) and
        f.startswith('総合チェックリスト_受付') and f.endswith('.xlsx')
    ]
    overall_checklist_files.sort(reverse=True)
    if not overall_checklist_files:
        logging.error("総合チェックリストのファイルが見つかりません")
        return
    latest_overall_checklist_file = overall_checklist_files[0]
    latest_overall_checklist_path = os.path.join(overall_checklist_folder_path, latest_overall_checklist_file)
    overall_checklist_df = pd.read_excel(latest_overall_checklist_path)
    logging.info(f"最新の総合チェックリストを読み込みました: {latest_overall_checklist_file}")
    
    # 「チェックリスト作成日時」カラムが存在しない場合は追加
    if 'チェックリスト作成日時' not in overall_checklist_df.columns:
        logging.warning("総合チェックリストに'チェックリスト作成日時'カラムが存在しないため、追加します")
        # 受付日時をベースにチェックリスト作成日時を設定
        overall_checklist_df['チェックリスト作成日時'] = overall_checklist_df['受付日時']
        logging.info("'チェックリスト作成日時'カラムを追加しました")
    
    # 「チェックリスト作成日時」カラムが空の場合は受付日時で補完
    checklist_creation_mask = overall_checklist_df['チェックリスト作成日時'].isnull() | (overall_checklist_df['チェックリスト作成日時'] == '')
    if checklist_creation_mask.any():
        overall_checklist_df.loc[checklist_creation_mask, 'チェックリスト作成日時'] = overall_checklist_df.loc[checklist_creation_mask, '受付日時']
        logging.info("空の'チェックリスト作成日時'を受付日時で補完しました")

    # 3. 受付データの自動チェックを実行
    logging.info("受付データの自動チェックを実行します")
    # 受付データの自動チェックを実行するための関数を呼び出す
    overall_checklist_df, overall_checklist_file_path = auto_check(club_reception_df, overall_checklist_df, latest_reception_data_date=latest_club_reception_date)
    logging.info("受付データの自動チェックが完了しました")

    # 5. 書類チェック状況を総合チェックリストに反映
    logging.info("書類チェック状況を総合チェックリストに反映します")
    overall_checklist_df = update_document_check_status(overall_checklist_df, overall_checklist_file_path, club_reception_df, latest_reception_data_date=latest_club_reception_date)
    logging.info("書類チェック状況の反映が完了しました")

    # 作業memo（今後の作業）
    # 6. 整合性チェック状況を総合チェックリストに反映
    logging.info("整合性チェック状況を総合チェックリストに反映します")
    update_consistency_check_status(overall_checklist_df, overall_checklist_file_path, club_reception_df, latest_club_reception_date)
    logging.info("整合性チェック状況の反映が完了しました")

    logging.info("チェックリストの更新・自動チェックが完了しました")