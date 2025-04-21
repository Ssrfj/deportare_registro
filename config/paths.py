import os
from datetime import datetime

# === ベースディレクトリ ===
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# === 入力ディレクトリ ===
INPUT_DIR = os.path.join(BASE_DIR, "input")

# === 出力関連ディレクトリ ===
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
CHECKLIST_DIR = os.path.join(OUTPUT_DIR, "checklist")
SUMMARY_DIR = os.path.join(OUTPUT_DIR, "summary")
LOGS_DIR = os.path.join(OUTPUT_DIR, "logs")

# === 出力ファイル ===
SUMMARY_FILE = os.path.join(SUMMARY_DIR, "submission_status.xlsx")
PROCESS_LOG_FILE = os.path.join(LOGS_DIR, "process.log")

# === クラブ名簿 ===
CLUB_MASTER_FILE = os.path.join(BASE_DIR, "club_master.xlsx")
CLUB_MASTER_SHEET = "クラブ一覧"

# === テンプレート ===
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
CHECK_TEMPLATE_FILE = os.path.join(TEMPLATE_DIR, "check_paper1_registration_criteria_confirmation_formtemplate_R6.xlsx")

# === 日付（任意）===
RUN_DATE = datetime.now().strftime("%Y-%m-%d")

# === 書類のファイル名定義（書類コード → ファイル名）===
REQUIRED_FILES = {
    "01": "登録基準確認用紙.xlsx",
    "02-1": "基礎情報書類.xlsx",
    "02-2": "活動・マネジャー書類.xlsx",
    "03": "規約・会則・定款等.pdf",
    "06": "事業報告・決算.xlsx",
    "08": "議事録.pdf"
}