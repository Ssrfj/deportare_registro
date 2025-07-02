from datetime import datetime, timezone, timedelta
import os
import pandas as pd
import logging

def get_jst_now():
    """
    日本標準時（JST）の現在時刻を返す。
    """
    return datetime.now(timezone(timedelta(hours=9)))

def make_checklist_filename(club_name, reception_date_str):
    """
    クラブ名・受付日・作成日からチェックリスト用のファイル名を生成する。
    """
    club_name = str(club_name).strip()
    return f"{club_name}_受付{reception_date_str}.xlsx"

def get_latest_club_info_file():
    """
    プロジェクトのルートディレクトリからクラブ名_YYYYMMDD.xlsx形式の最新ファイルを取得する。
    """
    root_path = os.getcwd()
    
    # クラブ名_YYYYMMDD.xlsx形式のファイルを探す
    club_info_files = [
        f for f in os.listdir(root_path)
        if os.path.isfile(os.path.join(root_path, f)) and
        f.startswith('クラブ名_') and f.endswith('.xlsx')
    ]
    
    if not club_info_files:
        logging.error("クラブ情報ファイルが見つかりません")
        return None, None
    
    # ファイル名から日付を抽出してソート
    club_info_files.sort(reverse=True)
    latest_club_info_file = club_info_files[0]
    
    try:
        # ファイル名から日付を抽出 (クラブ名_YYYYMMDD.xlsx)
        date_str = latest_club_info_file.split('_')[1].split('.')[0]
        latest_club_info_date = pd.to_datetime(date_str, format='%Y%m%d')
        logging.info(f"最新のクラブ情報ファイル: {latest_club_info_file}")
        
        # ファイルを読み込む
        club_info_df = pd.read_excel(os.path.join(root_path, latest_club_info_file))
        logging.info(f"最新のクラブ情報を読み込みました: {latest_club_info_file}")
        
        return club_info_df, latest_club_info_date
    except Exception as e:
        logging.error(f"クラブ情報ファイルの読み込みに失敗しました: {e}")
        return None, None