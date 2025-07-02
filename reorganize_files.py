#!/usr/bin/env python3
"""
ファイルを適切なフォルダに移動するスクリプト
"""
import os
import shutil

def move_file(src, dst):
    """ファイルを移動（存在しない場合はスキップ）"""
    if os.path.exists(src):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.move(src, dst)
        print(f"移動: {src} -> {dst}")
    else:
        print(f"スキップ（存在しない）: {src}")

def main():
    base_path = "e:/oasobi/deportare_registro"
    
    # データ処理関連のファイル移動
    data_processing_files = [
        "processing_reception_data.py",
        "marge_reception_data_with_club_info.py",
        "reception_statues.py",
        "column_name_change.py",
        "make_detailed_club_data.py"
    ]
    
    for file in data_processing_files:
        src = os.path.join(base_path, file)
        dst = os.path.join(base_path, "src", "data_processing", file)
        move_file(src, dst)
    
    # フォルダ管理関連のファイル移動
    folder_management_files = [
        "make_folders.py",
        "make_detailed_data_folders.py"
    ]
    
    for file in folder_management_files:
        src = os.path.join(base_path, file)
        dst = os.path.join(base_path, "src", "folder_management", file)
        move_file(src, dst)
    
    # チェックリスト生成関連のファイル移動
    checklist_generators_files = [
        "checklist_generator.py",
        "make_chacklists.py",
        "make_overall_checklist.py"
    ]
    
    for file in checklist_generators_files:
        src = os.path.join(base_path, file)
        dst = os.path.join(base_path, "src", "checklist", "generators", file)
        move_file(src, dst)
    
    # 書類チェックリスト生成関連のファイル移動
    document_checklist_files = [
        "make_document01_checklist.py",
        "make_document02_1_checklist.py",
        "make_document02_2_checklist.py",
        "make_document03_checklist.py",
        "make_document04_checklist.py",
        "make_document05_budget_checklist.py",
        "make_document05_plan_checklist.py",
        "make_document06_financial_statements_checklist.py",
        "make_document06_report_checklist.py",
        "make_document07_checklist.py",
        "make_document08_checklist.py",
        "make_document09_checklist.py",
        "make_document10_checklist.py",
        "make_documents_checklists.py"
    ]
    
    for file in document_checklist_files:
        src = os.path.join(base_path, file)
        dst = os.path.join(base_path, "src", "checklist", "generators", "documents", file)
        move_file(src, dst)
    
    # 整合性チェック関連のファイル移動
    consistency_files = [
        "make_consistency_checklists.py",
        "make_consistency_checklist_disciplines.py",
        "make_consistency_checklist_meeting_minutes.py",
        "make_consistency_checklist_members_and_voting_rights.py"
    ]
    
    for file in consistency_files:
        src = os.path.join(base_path, file)
        dst = os.path.join(base_path, "src", "checklist", "consistency", file)
        move_file(src, dst)
    
    # 自動チェック関連のファイル移動
    automation_files = [
        "automation_check_and_update_checklist.py",
        "auto_check.py",
        "check_functions.py",
        "documents_check_functions.py",
        "update_consistency_check_status.py",
        "update_document_check_status.py"
    ]
    
    for file in automation_files:
        src = os.path.join(base_path, file)
        dst = os.path.join(base_path, "src", "checklist", "automation", file)
        move_file(src, dst)
    
    # 人間用インターフェース関連のファイル移動
    human_interface_files = [
        "make_and_write_documents_checklist_for_human.py"
    ]
    
    for file in human_interface_files:
        src = os.path.join(base_path, file)
        dst = os.path.join(base_path, "src", "human_interface", file)
        move_file(src, dst)
    
    # 設定ファイル移動 - チェックリストカラム設定
    checklist_column_files = [
        "consistency_checklist_disciplines_columns.json",
        "consistency_checklist_meeting_minutes_columns.json",
        "consistency_checklist_members_and_voting_rights_columns.json",
        "document01_checklist_columns.json",
        "document02_1_checklist_columns.json",
        "document02_2_checklist_columns.json",
        "document03_checklist_columns.json",
        "document04_checklist_columns.json",
        "document05_budget_checklist_columns.json",
        "document05_plan_checklist_columns.json",
        "document06_financial_statements_checklist_columns.json",
        "document06_report_checklist_columns.json",
        "document07_checklist_columns.json",
        "document08_checklist_columns.json",
        "document09_checklist_columns.json",
        "document10_checklist_columns.json",
        "overall_checklist_columns.json"
    ]
    
    for file in checklist_column_files:
        src = os.path.join(base_path, file)
        dst = os.path.join(base_path, "config", "checklist_columns", file)
        move_file(src, dst)
    
    # 参照データファイル移動
    reference_data_files = [
        "column_name.csv",
        "list_of_disciplines.csv",
        "list_of_disciplines.xlsx",
        "municipality_test_tokyo.csv",
        "municipality_test_tokyo.xlsx"
    ]
    
    for file in reference_data_files:
        src = os.path.join(base_path, file)
        dst = os.path.join(base_path, "config", "reference_data", file)
        move_file(src, dst)
    
    # データファイル移動
    club_data_files = [
        "クラブ名_20220401.csv",
        "クラブ名_20220401.xlsx"
    ]
    
    for file in club_data_files:
        src = os.path.join(base_path, file)
        dst = os.path.join(base_path, "data", "clubs", file)
        move_file(src, dst)
    
    application_data_files = [
        "申請データ_20250401000000.xlsx"
    ]
    
    for file in application_data_files:
        src = os.path.join(base_path, file)
        dst = os.path.join(base_path, "data", "applications", file)
        move_file(src, dst)
    
    # 出力フォルダの移動
    if os.path.exists(os.path.join(base_path, "R7_登録受付処理")):
        dst = os.path.join(base_path, "output", "R7_登録受付処理")
        if not os.path.exists(dst):
            shutil.move(os.path.join(base_path, "R7_登録受付処理"), dst)
            print(f"移動: R7_登録受付処理 -> output/R7_登録受付処理")
    
    print("ファイル移動完了！")

if __name__ == "__main__":
    main()
