from utils.logger import setup_logging
from utils.file_scanner import scan_club_folders
from utils.club_master_loader import load_club_master
from utils.excel_checker import check_submissions
from utils.summary_extractor import extract_paper1_summary
from utils.checklist_writer import copy_checklist_template_for_club
from config.paths import INPUT_DIR, SUMMARY_FILE
import pandas as pd
import os

if __name__ == "__main__":
    setup_logging()
    clubs = scan_club_folders()
    club_master = load_club_master()
    results = check_submissions(clubs, club_master)
    

    try:
        os.makedirs(os.path.dirname(SUMMARY_FILE), exist_ok=True)
        df = pd.DataFrame(results)
        df.to_excel(SUMMARY_FILE, index=False)
    except Exception as e:
        import logging
        logging.exception("提出状況一覧の出力に失敗しました")
