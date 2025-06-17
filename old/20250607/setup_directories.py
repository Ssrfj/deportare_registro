import os
import pandas as pd

# 生成するディレクトリ一覧（共通フォルダ）
BASE_FOLDERS = [
    "input",
    "output/checklist",
    "output/summary",
    "output/logs",
    "templates",
    "config"
]

# クラブ名簿ファイル
CLUB_MASTER_PATH = "club_master.xlsx"
CLUB_MASTER_SHEET = "クラブ一覧"

def create_base_directories(base_path="."):
    for folder in BASE_FOLDERS:
        path = os.path.join(base_path, folder)
        os.makedirs(path, exist_ok=True)
        logging.info(f"✔ 作成: {path}")

def create_club_folders(base_path="input"):
    try:
        df = pd.read_excel(CLUB_MASTER_PATH, sheet_name=CLUB_MASTER_SHEET)
        df = df[["クラブID", "クラブ名"]].dropna()

        for _, row in df.iterrows():
            club_id = str(row["クラブID"]).strip()
            club_name = str(row["クラブ名"]).strip()

            # フォルダ名：clubID_クラブ名（例：club001_あさひスポーツクラブ）
            folder_name = f"{club_id}_{club_name}"
            folder_path = os.path.join(base_path, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            logging.info(f"📂 クラブフォルダ作成: {folder_path}")
    except Exception as e:
        print("❌ クラブフォルダの作成に失敗しました。")
        logging.info(f"原因: {e}")

if __name__ == "__main__":
    print("📁 初期ディレクトリ構成を作成中...")
    create_base_directories()

    print("📋 クラブ名簿に基づくフォルダを作成中...")
    create_club_folders()

    print("✅ 完了しました。")
