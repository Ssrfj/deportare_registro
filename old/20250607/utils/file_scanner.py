import os
import logging
from config.paths import INPUT_DIR

def scan_club_folders(input_dir=INPUT_DIR):
    clubs = []
    try:
        for name in os.listdir(input_dir):
            club_path = os.path.join(input_dir, name)
            if os.path.isdir(club_path):
                clubs.append((name, club_path))
        logging.info(f"📂 クラブフォルダ数: {len(clubs)} 件を検出しました。")
    except Exception as e:
        logging.exception("クラブフォルダのスキャン中にエラーが発生しました")
    return clubs
