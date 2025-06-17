import pandas as pd

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    DataFrameのカラム名の前後の空白を除去する
    """
    df.columns = df.columns.str.strip()
    return df

def to_datetime_column(df: pd.DataFrame, column: str, errors='coerce') -> pd.DataFrame:
    """
    指定したカラムをdatetime型に変換する
    """
    if column in df.columns:
        df[column] = pd.to_datetime(df[column], errors=errors)
    return df

def add_datetime_str_column(df: pd.DataFrame, src_column: str, dest_column: str, fmt='%Y%m%d%H%M%S') -> pd.DataFrame:
    """
    datetime型カラムから yyyymmddHHMMSS 形式の文字列カラムを追加する
    """
    if src_column in df.columns:
        df[dest_column] = df[src_column].dt.strftime(fmt)
    return df