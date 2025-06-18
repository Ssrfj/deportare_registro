import glob
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def load_latest_club_data():
    csv_files = glob.glob('クラブ名_*.csv')
    if not csv_files:
        logging.error("クラブ名_YYYYMMDD.csv ファイルが見つかりません。")
        return None
    latest_file = max(csv_files)
    df = pd.read_csv(latest_file)
    logging.info(f"最新のクラブデータ {latest_file} を読み込みました。")
    return df

if __name__ == "__main__":
    df = load_latest_club_data()
    if df is not None:
        logging.info(f"\n{df.head()}")