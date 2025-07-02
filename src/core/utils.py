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
    data/clubsディレクトリからクラブ名_YYYYMMDD.csv形式の最新ファイルを取得する。
    """
    root_path = os.getcwd()
    clubs_folder = os.path.join(root_path, 'data', 'clubs')
    
    # フォルダが存在しない場合は空のリストを返す
    if not os.path.exists(clubs_folder):
        logging.error(f"クラブ情報フォルダが見つかりません: {clubs_folder}")
        return None, None
    
    # クラブ名_YYYYMMDD.csv形式のファイルを探す
    club_info_files = [
        f for f in os.listdir(clubs_folder)
        if os.path.isfile(os.path.join(clubs_folder, f)) and
        f.startswith('クラブ名_') and f.endswith('.csv')
    ]
    
    if not club_info_files:
        logging.error("クラブ情報ファイルが見つかりません")
        return None, None
    
    # ファイル名から日付を抽出してソート
    club_info_files.sort(reverse=True)
    latest_club_info_file = club_info_files[0]
    
    try:
        # ファイル名から日付を抽出 (クラブ名_YYYYMMDD.csv)
        date_str = latest_club_info_file.split('_')[1].split('.')[0]
        latest_club_info_date = pd.to_datetime(date_str, format='%Y%m%d')
        logging.info(f"最新のクラブ情報ファイル: {latest_club_info_file}")
        
        # ファイルを読み込む
        club_info_df = pd.read_csv(os.path.join(clubs_folder, latest_club_info_file))
        logging.info(f"最新のクラブ情報を読み込みました: {latest_club_info_file}")
        
        return club_info_df, latest_club_info_date
    except Exception as e:
        logging.error(f"クラブ情報ファイルの読み込みに失敗しました: {e}")
        return None, None

def get_project_root():
    """
    プロジェクトルートディレクトリのパスを取得する。
    """
    # このファイル（utils.py）からプロジェクトルートまでは2階層上
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
    return project_root

def get_config_file_path(relative_path):
    """
    プロジェクトルートからの相対パスで設定ファイルのパスを取得する。
    """
    project_root = get_project_root()
    return os.path.join(project_root, relative_path)