"""
最新のクラブ情報付き受付データファイルを読み込むためのユーティリティ関数
"""
import os
import pandas as pd
import logging
from src.core.setting_paths import clubs_reception_data_path


def get_latest_club_reception_data_file():
    """
    最新のクラブ情報付き受付データファイルのパスを取得
    
    Returns:
        str: 最新のクラブ情報付き受付データファイルのフルパス、見つからない場合はNone
    """
    try:
        logging.info("最新のクラブ情報付き受付データファイルを取得しています")
        
        if not os.path.exists(clubs_reception_data_path):
            logging.error(f"クラブ情報付き受付データフォルダが存在しません: {clubs_reception_data_path}")
            return None
        
        club_reception_data_files = [
            f for f in os.listdir(clubs_reception_data_path)
            if os.path.isfile(os.path.join(clubs_reception_data_path, f)) and
            f.startswith('クラブ情報付き受付データ_受付') and f.endswith('.xlsx')
        ]
        
        if not club_reception_data_files:
            logging.error("クラブ情報付き受付データファイルが見つかりません")
            return None
        
        # ファイル名の受付日時でソート（降順）
        club_reception_data_files.sort(reverse=True)
        latest_file = club_reception_data_files[0]
        latest_file_path = os.path.join(clubs_reception_data_path, latest_file)
        
        logging.info(f"最新のクラブ情報付き受付データファイル: {latest_file}")
        return latest_file_path
        
    except Exception as e:
        logging.error(f"最新のクラブ情報付き受付データファイルの取得中にエラーが発生しました: {e}")
        return None


def load_latest_club_reception_data():
    """
    最新のクラブ情報付き受付データを読み込む
    
    Returns:
        pd.DataFrame: クラブ情報付き受付データのDataFrame、エラーの場合はNone
    """
    try:
        latest_file_path = get_latest_club_reception_data_file()
        if latest_file_path is None:
            return None
        
        logging.info(f"クラブ情報付き受付データを読み込みます: {latest_file_path}")
        club_data_df = pd.read_excel(latest_file_path)
        logging.info(f"クラブ情報付き受付データを正常に読み込みました。行数: {len(club_data_df)}")
        
        return club_data_df
        
    except Exception as e:
        logging.error(f"クラブ情報付き受付データの読み込み中にエラーが発生しました: {e}")
        return None


def get_club_data_by_name_and_date(club_data_df, club_name, reception_date):
    """
    クラブ名と受付日時でデータを抽出
    
    Args:
        club_data_df (pd.DataFrame): クラブ情報付き受付データ
        club_name (str): クラブ名
        reception_date (str): 受付日時
    
    Returns:
        pd.DataFrame: 該当するデータ行、見つからない場合は空のDataFrame
    """
    try:
        # データをコピーして元のデータを変更しないようにする
        club_data_df_copy = club_data_df.copy()
        
        # データ型を文字列に統一して検索
        club_data_df_copy['クラブ名'] = club_data_df_copy['クラブ名'].astype(str).str.strip()
        
        # 受付日時のカラム名を確認して適切なカラムを使用
        timestamp_column = None
        if '申請_タイムスタンプ' in club_data_df_copy.columns:
            timestamp_column = '申請_タイムスタンプ'
        elif '申請_タイムスタンプ' in club_data_df_copy.columns:
            timestamp_column = '申請_タイムスタンプ'
        else:
            logging.error(f"受付/申請日時のカラムが見つかりません。利用可能なカラム: {club_data_df_copy.columns.tolist()}")
            return pd.DataFrame()
        
        # タイムスタンプを文字列に変換し、統一した形式にする
        club_data_df_copy[timestamp_column] = club_data_df_copy[timestamp_column].astype(str).str.strip()
        
        club_name = str(club_name).strip()
        reception_date = str(reception_date).strip()
        
        # 両方の日時から小数点以下を除去して比較用の文字列を作成
        club_data_df_copy['timestamp_comparison'] = club_data_df_copy[timestamp_column].apply(lambda x: str(x).split('.')[0] if '.' in str(x) else str(x))
        reception_date_comparison = reception_date.split('.')[0] if '.' in reception_date else reception_date
        
        # 該当行を抽出
        target_rows = club_data_df_copy[
            (club_data_df_copy['クラブ名'] == club_name) &
            (club_data_df_copy['timestamp_comparison'] == reception_date_comparison)
        ]
        
        # 比較用カラムを削除
        if 'timestamp_comparison' in target_rows.columns:
            target_rows = target_rows.drop('timestamp_comparison', axis=1)
        
        if target_rows.empty:
            logging.warning(f"該当データが見つかりません: クラブ名={club_name}, 受付日時={reception_date_comparison}, 使用カラム={timestamp_column}")
            # デバッグ用：該当クラブの全データを表示
            club_only_data = club_data_df_copy[club_data_df_copy['クラブ名'] == club_name]
            if not club_only_data.empty:
                logging.info(f"該当クラブの全データ: {club_only_data[['クラブ名', timestamp_column]].values.tolist()}")
        else:
            logging.info(f"該当データが見つかりました: クラブ名={club_name}, 受付日時={reception_date_comparison}, 使用カラム={timestamp_column}")
        
        return target_rows
        
    except Exception as e:
        logging.error(f"データ抽出中にエラーが発生しました: {e}")
        return pd.DataFrame()
