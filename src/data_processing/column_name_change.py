import os
import glob
import pandas as pd
import logging
from src.core.utils import get_jst_now

logging.basicConfig(
    level=logging.DEBUG,
    encoding='utf-8',
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def column_name_change(df):
    # カラム名を指定したリストを基に返還
    column_name_list_file = os.path.join(os.getcwd(), 'config', 'reference_data', 'column_name.csv')
    if not os.path.exists(column_name_list_file):
        logging.error(f"{column_name_list_file} が存在しません。")
        return
    column_name_df = pd.read_csv(column_name_list_file)
    column_name_list = column_name_df['修正後'].tolist()
    if len(column_name_list) != len(df.columns):
        logging.error(f"カラム名の数が一致しません: {len(column_name_list)} vs {len(df.columns)}")
        return
    # カラム名を設定
    if len(column_name_list) == 0:
        logging.error("カラム名のリストが空です。")
        return
    df.columns = column_name_list
    logging.info(f"カラム名を変更しました: {df.columns.tolist()}")
    return df