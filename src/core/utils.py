from datetime import datetime, timezone, timedelta
import os
import pandas as pd
import logging

def get_jst_now():
    """
    日本標準時（JST）の現在時刻を返す。
    """
    return datetime.now(timezone(timedelta(hours=9)))

def ensure_date_string(date_input):
    """
    日付を文字列形式（YYYYMMDDHHMMSS）に変換する。
    
    Args:
        date_input: datetime、pandas.Timestamp、または文字列
        
    Returns:
        str: YYYYMMDDHHMMSS形式の文字列
    """
    if isinstance(date_input, (pd.Timestamp, datetime)):
        return date_input.strftime('%Y%m%d%H%M%S')
    elif isinstance(date_input, str):
        # 既に文字列の場合は、必要に応じて変換
        try:
            # 文字列がYYYYMMDDHHMMSS形式かチェック
            if len(date_input) == 14 and date_input.isdigit():
                return date_input
            # その他の形式の場合はパースして変換
            parsed_date = pd.to_datetime(date_input)
            return parsed_date.strftime('%Y%m%d%H%M%S')
        except:
            logging.warning(f"日付の変換に失敗しました: {date_input}")
            return str(date_input)
    else:
        logging.warning(f"未対応の日付形式です: {type(date_input)} - {date_input}")
        return str(date_input)

def normalize_reception_date_for_display(reception_date):
    """
    受付日を表示用形式（YYYY-MM-DD HH:MM:SS）に正規化する。
    
    Args:
        reception_date: datetime、pandas.Timestamp、または文字列
        
    Returns:
        str: YYYY-MM-DD HH:MM:SS形式の文字列
    """
    if isinstance(reception_date, (pd.Timestamp, datetime)):
        return reception_date.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(reception_date, str):
        try:
            if len(reception_date) == 14 and reception_date.isdigit():
                parsed_date = pd.to_datetime(reception_date, format='%Y%m%d%H%M%S')
                return parsed_date.strftime('%Y-%m-%d %H:%M:%S')
            else:
                parsed_date = pd.to_datetime(reception_date)
                return parsed_date.strftime('%Y-%m-%d %H:%M:%S')
        except:
            logging.warning(f"日付の変換に失敗しました: {reception_date}")
            return str(reception_date)
    else:
        logging.warning(f"未対応の日付形式です: {type(reception_date)} - {reception_date}")
        return str(reception_date)

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

def normalize_reception_date(latest_reception_data_date):
    """
    受付データの日付を正規化する関数
    datetime オブジェクトまたは文字列を受け取り、YYYYMMDDHHMMSS 形式の文字列を返す
    """
    import pandas as pd
    from datetime import datetime
    
    if latest_reception_data_date is None:
        return None
        
    if isinstance(latest_reception_data_date, str):
        # 既に文字列の場合は、そのまま返す（YYYYMMDDHHMMSS 形式と想定）
        return latest_reception_data_date
    elif isinstance(latest_reception_data_date, datetime):
        # datetime オブジェクトの場合は YYYYMMDDHHMMSS 形式に変換
        return latest_reception_data_date.strftime('%Y%m%d%H%M%S')
    else:
        # その他の場合は pandas.to_datetime を使って変換を試みる
        try:
            date_obj = pd.to_datetime(latest_reception_data_date)
            return date_obj.strftime('%Y%m%d%H%M%S')
        except Exception as e:
            logging.error(f"日付の正規化に失敗しました: {latest_reception_data_date}, エラー: {e}")
            return None

def get_latest_checklist_file(club_name, reception_date, club_folder):
    """
    指定されたクラブフォルダから最新のチェックリストファイルを取得する。
    
    Args:
        club_name (str): クラブ名
        reception_date (str): 受付日時
        club_folder (str): クラブフォルダのパス
    
    Returns:
        str: 最新のチェックリストファイルのパス（見つからない場合はNone）
    """
    if not os.path.exists(club_folder):
        logging.warning(f"クラブフォルダが存在しません: {club_folder}")
        return None
    
    # チェックリストファイルのパターンを探す
    checklist_files = [
        f for f in os.listdir(club_folder)
        if os.path.isfile(os.path.join(club_folder, f)) and
        f.startswith(f'{club_name}_受付{reception_date}') and 
        f.endswith('.xlsx') and
        'チェックリスト' in f
    ]
    
    if not checklist_files:
        logging.warning(f"クラブ '{club_name}' のチェックリストファイルが見つかりません")
        return None
    
    # 最新のファイルを返す（ファイル名でソート）
    latest_file = sorted(checklist_files)[-1]
    return os.path.join(club_folder, latest_file)