import os
import logging

from setting_paths import (
    output_main_folder,
    log_folder_path,
    reception_data_folder_path,
    reception_data_with_club_info_folder_path,
    Content_check_folder_path
)

def setup_logging():
    """ロギングの設定"""
    logging.basicConfig(
        filename=os.path.join(log_folder_path, 'reception.log'),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info("ロギングを設定しました")

def create_folders():
    # 出力先のフォルダをなければ作成
    folders_to_create = [
        output_main_folder,
        log_folder_path,
        reception_data_folder_path,
        reception_data_with_club_info_folder_path,
        Content_check_folder_path
    ]
    for folder in folders_to_create:
        if not os.path.exists(folder):
            os.makedirs(folder)
            logging.info(f"フォルダを作成しました: {folder}")
