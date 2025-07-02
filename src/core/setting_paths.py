import os

output_main_folder_name = 'R7_登録受付処理'
output_main_folder_path = os.path.join(os.getcwd(), output_main_folder_name)
settting_folder_name = 'setting'
settting_folder_path = os.path.join(output_main_folder_path, settting_folder_name)
log_folder_name = 'log'
log_folder_path = os.path.join(output_main_folder_path, log_folder_name)
reception_data_folder_name = '受付データ'
reception_data_folder_path = os.path.join(output_main_folder_path, reception_data_folder_name)
processed_reception_data_folder_name = '処理済み受付データ'
processed_reception_data_folder_path = os.path.join(output_main_folder_path, processed_reception_data_folder_name)
club_info_data_folder_name = 'クラブ情報'
club_info_data_path = os.path.join(output_main_folder_path, club_info_data_folder_name)
clubs_reception_data_folder_name = 'クラブ情報付き受付データ'
clubs_reception_data_path = os.path.join(output_main_folder_path, clubs_reception_data_folder_name)
application_statues_folder_name = '申請状況'
application_statues_folder_path = os.path.join(output_main_folder_path, application_statues_folder_name)
content_check_folder_name = '受付内容チェック'
content_check_folder_path = os.path.join(output_main_folder_path, content_check_folder_name)

# 受付内容チェックの下部フォルダ
overall_checklist_folder_name = '総合チェックリスト'
overall_checklist_folder_path = os.path.join(content_check_folder_path, overall_checklist_folder_name)
document01_checklist_folder_name = '書類01チェックリスト'
document01_checklist_folder_path = os.path.join(content_check_folder_path, document01_checklist_folder_name)
document02_1_checklist_folder_name = '書類02-1チェックリスト'
document02_1_checklist_folder_path = os.path.join(content_check_folder_path, document02_1_checklist_folder_name)
document02_2_checklist_folder_name = '書類02-2チェックリスト'
document02_2_checklist_folder_path = os.path.join(content_check_folder_path, document02_2_checklist_folder_name)
document03_checklist_folder_name = '書類03チェックリスト'
document03_checklist_folder_path = os.path.join(content_check_folder_path, document03_checklist_folder_name)
document04_checklist_folder_name = '書類04チェックリスト'
document04_checklist_folder_path = os.path.join(content_check_folder_path, document04_checklist_folder_name)
document05_plan_checklist_folder_name = '書類05計画書チェックリスト'
document05_plan_checklist_folder_path = os.path.join(content_check_folder_path, document05_plan_checklist_folder_name)
document05_budget_checklist_folder_name = '書類05予算書チェックリスト'
document05_budget_checklist_folder_path = os.path.join(content_check_folder_path, document05_budget_checklist_folder_name)
document06_report_checklist_folder_name = '書類06報告書チェックリスト'
document06_report_checklist_folder_path = os.path.join(content_check_folder_path, document06_report_checklist_folder_name)
document06_financial_statements_checklist_folder_name = '書類06決算書チェックリスト'
document06_financial_statements_checklist_folder_path = os.path.join(content_check_folder_path, document06_financial_statements_checklist_folder_name)
document07_checklist_folder_name = '書類07チェックリスト'
document07_checklist_folder_path = os.path.join(content_check_folder_path, document07_checklist_folder_name)
document08_checklist_folder_name = '書類08チェックリスト'
document08_checklist_folder_path = os.path.join(content_check_folder_path, document08_checklist_folder_name)
document09_checklist_folder_name = '書類09チェックリスト'
document09_checklist_folder_path = os.path.join(content_check_folder_path, document09_checklist_folder_name)
document10_checklist_folder_name = '書類10チェックリスト'
document10_checklist_folder_path = os.path.join(content_check_folder_path, document10_checklist_folder_name)

# 一貫性チェックリストのフォルダ
consistency_checklist_members_and_voting_rights_folder_name = '会員と議決権保有者の一貫性チェックリスト'
consistency_checklist_members_and_voting_rights_folder_path = os.path.join(content_check_folder_path, consistency_checklist_members_and_voting_rights_folder_name)
consistency_checklist_disciplines_folder_name = '活動種目の一貫性チェックリスト'
consistency_checklist_disciplines_folder_path = os.path.join(content_check_folder_path, consistency_checklist_disciplines_folder_name)
consistency_checklist_meeting_minutes_folder_name = '議事録の一貫性チェックリスト'
consistency_checklist_meeting_minutes_folder_path = os.path.join(content_check_folder_path, consistency_checklist_meeting_minutes_folder_name)

# 書類チェック・一貫性チェックに使うクラブごとの詳細データ保存フォルダ
clubs_details_data_folder_name = 'クラブごとの詳細データ'
clubs_details_data_folder_path = os.path.join(content_check_folder_path, clubs_details_data_folder_name)