import os
import logging

from src.core.setting_paths import (
    output_main_folder_path,
    log_folder_path,
    processed_reception_data_folder_path,
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
    clubs_details_data_folder_path,
    email_drafts_folder_path
)

def create_folders():
    # 出力先のフォルダをなければ作成
    folders_to_create = [
        output_main_folder_path,
        log_folder_path,
        processed_reception_data_folder_path,
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
        clubs_details_data_folder_path,
        email_drafts_folder_path
    ]
    for folder in folders_to_create:
        if not os.path.exists(folder):
            os.makedirs(folder)
            logging.info(f"フォルダを作成しました: {folder}")
