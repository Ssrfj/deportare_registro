import glob
import os
import logging

logging.basicConfig(
    level=logging.DEBUG,
    encoding='utf-8',
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def get_latest_checklist_file(club_name, applied_date, checklist_output_folder):
    pattern = f"{club_name}_申請{applied_date}_作成*.csv"
    search_path = os.path.join(checklist_output_folder, pattern)
    logging.debug(f"glob search_path: {search_path}")
    files = glob.glob(search_path)
    logging.debug(f"glob found files: {files}")
    if not files:
        return None
    files.sort(reverse=True)
    return files[0]