import os
import logging

from src.core.setting_paths import (
    output_main_folder_path,
    log_folder_path,
    reception_data_folder_path,
    processed_reception_data_folder_path,
    club_info_data_path,
    clubs_reception_data_path,
    application_statues_folder_path,
    content_check_folder_path,
    overall_checklist_folder_path,
    document01_checklist_folder_path,
    document02_1_checklist_folder_path,
    document02_2_checklist_folder_path,
    document03_checklist_folder_path,
    document04_checklist_folder_path,
    document05_plan_checklist_folder_path,
    document05_budget_checklist_folder_path,
    document06_report_checklist_folder_path,
    document06_financial_statements_checklist_folder_path,
    document07_checklist_folder_path,
    document08_checklist_folder_path,
    document09_checklist_folder_path,
    document10_checklist_folder_path,
    consistency_checklist_members_and_voting_rights_folder_path,
    consistency_checklist_disciplines_folder_path,
    consistency_checklist_meeting_minutes_folder_path,
    clubs_details_data_folder_path
)

def setup_logging():
    """ロギングの設定"""
    import os
    
    # ログフォルダの作成
    if not os.path.exists(log_folder_path):
        os.makedirs(log_folder_path)
    
    # 既存のハンドラーをクリア
    logging.getLogger().handlers.clear()
    
    # UTF-8エンコーディングでファイルハンドラーを作成
    log_file_path = os.path.join(log_folder_path, 'reception.log')
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # フォーマッターの設定
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    # ロガーの設定
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    
    logging.info("ロギングを設定しました")

def create_folders():
    # 出力先のフォルダをなければ作成
    folders_to_create = [
        output_main_folder_path,
        log_folder_path,
        reception_data_folder_path,
        processed_reception_data_folder_path,
        club_info_data_path,
        clubs_reception_data_path,
        application_statues_folder_path,
        content_check_folder_path,
        overall_checklist_folder_path,
        document01_checklist_folder_path,
        document02_1_checklist_folder_path,
        document02_2_checklist_folder_path,
        document03_checklist_folder_path,
        document04_checklist_folder_path,
        document05_plan_checklist_folder_path,
        document05_budget_checklist_folder_path,
        document06_report_checklist_folder_path,
        document06_financial_statements_checklist_folder_path,
        document07_checklist_folder_path,
        document08_checklist_folder_path,
        document09_checklist_folder_path,
        document10_checklist_folder_path,
        consistency_checklist_members_and_voting_rights_folder_path,
        consistency_checklist_disciplines_folder_path,
        consistency_checklist_meeting_minutes_folder_path,
        clubs_details_data_folder_path
    ]
    for folder in folders_to_create:
        if not os.path.exists(folder):
            os.makedirs(folder)
            logging.info(f"フォルダを作成しました: {folder}")
