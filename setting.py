import os

output_main_folder = 'R7_登録申請処理'
log_folder_name = 'log'
log_folder_path = os.path.join(output_main_folder, log_folder_name)
application_data_folder_name = '申請データ'
application_data_folder_path = os.path.join(output_main_folder, application_data_folder_name)
processed_application_data_folder_name = '処理済み申請データ'
processed_application_data_folder_path = os.path.join(output_main_folder, processed_application_data_folder_name)
club_info_data_folder_name = 'クラブ情報'
club_info_data_path = os.path.join(output_main_folder, club_info_data_folder_name)
clubs_application_data_folder_name = 'クラブ情報付き申請データ'
clubs_application_data_path = os.path.join(output_main_folder, clubs_application_data_folder_name)
content_check_folder_name = '申請内容チェック'
content_check_folder_path = os.path.join(output_main_folder, content_check_folder_name)
application_statues_folder_name = '申請状況'
application_statues_folder_path = os.path.join(output_main_folder, application_statues_folder_name)