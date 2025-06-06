import os
import glob
import pandas as pd
from utils.checklist_reader import read_defects_from_checklist

CHECKLIST_DIR = "output/checklists"
LOG_DIR = "output/logs"
SUMMARY_FILE = "output/summary/defect_summary.xlsx"
PAPER_CODES = ["01", "02-1", "02-2", "03", "04", "05-1", "05-2", "06-1", "06-2", "07", "08", "09"]

def process_all_clubs():
    summary_rows = []
    os.makedirs(LOG_DIR, exist_ok=True)

    for club in os.listdir(CHECKLIST_DIR):
        club_path = os.path.join(CHECKLIST_DIR, club)
        if not os.path.isdir(club_path):
            continue

        club_row = {"クラブ名": club}
        log_lines = []

        for code in PAPER_CODES:
            pattern = os.path.join(club_path, f"{code}_*.xlsx")
            files = glob.glob(pattern)

            if not files:
                club_row[code] = "×"
                continue

            club_row[code] = "✔"

            defects = read_defects_from_checklist(files[0])
            if defects:
                club_row[f"{code}_status"] = "⚠️"
                log_lines.append(f"▼ 書類{code} の不備")
                for defect in defects:
                    log_lines.append(f"- No{defect['No']} {defect['カテゴリ']} : {defect['チェック項目']}")
            else:
                club_row[f"{code}_status"] = "OK"

        # ログ出力
        log_path = os.path.join(LOG_DIR, f"{club}_log.txt")
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(f"【クラブ】{club}\n\n")
            f.write("\n".join(log_lines) if log_lines else "✅ 不備は見つかりませんでした。")

        summary_rows.append(club_row)

    df = pd.DataFrame(summary_rows)
    os.makedirs(os.path.dirname(SUMMARY_FILE), exist_ok=True)
    df.to_excel(SUMMARY_FILE, index=False)
    print(f"✅ 不備サマリー出力完了 → {SUMMARY_FILE}")

if __name__ == "__main__":
    process_all_clubs()
