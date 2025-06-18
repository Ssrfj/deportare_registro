import os
import glob
import pandas as pd
import logging
from utils import get_jst_now

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def excel_to_csv():
    # main.pyと同じフォルダのExcelファイルを探す
    excel_files = glob.glob('申請データ.xlsx')
    logging.info(f"探すExcelファイル: {excel_files}")
    if not excel_files:
        logging.error("Excelファイルが見つかりません。")
        return
    else:
        # 複数のファイルが見つかった場合は最初のファイルを使用
        logging.info("Excelファイルが見つかりました。")
    excel_path = excel_files[0]
    df = pd.read_excel(excel_path)
    if df.empty:
        logging.warning(f"{excel_path} は空のファイルです。")
        return
    
    # カラム名を指定したリストを基に返還
    column_name_list_file = 'column_name.csv'
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
    
    # 保存先フォルダ
    save_folder = os.path.join('R7_登録申請処理', '申請内容')
    save_file_name = f"申請内容_{get_jst_now().strftime('%Y%m%d%H%M%S')}.csv"
    os.makedirs(save_folder, exist_ok=True)
    save_path = os.path.join(save_folder, save_file_name)
    df.to_csv(save_path, index=False)
    logging.info(f"{excel_path} を {save_path} に保存しました。")

if __name__ == "__main__":
    excel_to_csv()