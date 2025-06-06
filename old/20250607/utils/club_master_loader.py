import pandas as pd
import logging
from config.paths import CLUB_MASTER_FILE, CLUB_MASTER_SHEET

def load_club_master(path=CLUB_MASTER_FILE, sheet_name=CLUB_MASTER_SHEET):
    try:
        df = pd.read_excel(path, sheet_name=sheet_name)
        df = df[["クラブ名", "過年度の登録"]].dropna()

        def convert_to_application_type(value):
            value = str(value).strip()
            if value == "あり":
                return "更新"
            elif value == "なし":
                return "新規"
            else:
                return "不明"

        df["申請区分"] = df["過年度の登録"].apply(convert_to_application_type)
        master_dict = df.set_index("クラブ名")["申請区分"].to_dict()

        logging.info(f"🗂 クラブ名簿を読み込みました（{len(master_dict)}件）")
        return master_dict

    except Exception as e:
        logging.exception("クラブ名簿の読み込みに失敗しました")
        return {}
