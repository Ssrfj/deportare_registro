import glob
import os

def get_latest_checklist_file(club_name, application_timestamp, checklist_output_folder):
    folder = os.path.join(checklist_output_folder, club_name)
    pattern = f"{club_name}_申請{application_timestamp}_作成*.csv"
    files = glob.glob(os.path.join(folder, pattern))
    if not files:
        return None
    files.sort(reverse=True)
    return files[0]