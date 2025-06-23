import glob
import pandas as pd
import logging

logging.basicConfig(
    level=logging.DEBUG,
    encoding='utf-8',
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def load_latest_club_data():
    xlsx_files = glob.glob('クラブ名_*.xlsx')
    if not xlsx_files:
        logging.error("クラブ名_YYYYMMDD.xlsx ファイルが見つかりません。")
        return None
    latest_file = max(xlsx_files)
    df = pd.read_excel(latest_file)
    logging.info(f"最新のクラブデータ {latest_file} を読み込みました。")
    return df

if __name__ == "__main__":
    df = load_latest_club_data()
    if df is not None:
        logging.info(f"\n{df.head()}")