import os
import pandas as pd

def ensure_directory_exists(dir_path):
    """
    指定したディレクトリが存在しない場合は作成する。
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)

def read_csv_if_exists(file_path, columns=None):
    """
    指定したCSVファイルが存在すれば読み込み、なければ空のDataFrameを返す。
    columnsを指定した場合はそのカラムで空DataFrameを作成。
    """
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        if columns is not None:
            return pd.DataFrame(columns=columns)
        else:
            return pd.DataFrame()

def save_csv(df, file_path, index=False):
    """
    DataFrameをCSVファイルとして保存する。
    """
    df.to_csv(file_path, index=index)

def get_latest_file(folder_path, ext=".csv"):
    """
    指定フォルダ内で最新の拡張子ファイルを返す。
    """
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(ext)]
    if not files:
        return None
    return max(files, key=os.path.getctime)