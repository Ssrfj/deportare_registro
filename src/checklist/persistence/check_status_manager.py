import os
import pandas as pd
import logging
from datetime import datetime, timezone, timedelta
from src.core.setting_paths import output_main_folder_path

class CheckStatusManager:
    """
    各クラブのチェック状況を永続化して管理するクラス
    """
    
    def __init__(self):
        self.status_file_path = os.path.join(output_main_folder_path, "check_status_database.xlsx")
        
    def load_check_status(self):
        """
        保存されたチェック状況を読み込み
        """
        if os.path.exists(self.status_file_path):
            try:
                return pd.read_excel(self.status_file_path)
            except Exception as e:
                logging.warning(f"チェック状況ファイルの読み込みに失敗: {e}")
                return self.create_empty_status_df()
        else:
            return self.create_empty_status_df()
    
    def create_empty_status_df(self):
        """
        空のチェック状況DataFrameを作成
        """
        return pd.DataFrame(columns=[
            'クラブ名', 
            '受付日時',
            '書類チェック結果',
            '書類チェック更新日時',
            'チェック完了フラグ',
            '最終チェック者',
            'チェック詳細'
        ])
    
    def update_check_status(self, club_name, reception_date, check_result, checker_name):
        """
        特定クラブのチェック状況を更新
        """
        status_df = self.load_check_status()
        
        # JST現在時刻
        jst_now = datetime.now(timezone(timedelta(hours=9)))
        update_time = jst_now.strftime('%Y-%m-%d %H:%M:%S')
        
        # 既存のレコードを探す
        mask = (status_df['クラブ名'] == club_name) & (status_df['受付日時'] == reception_date)
        
        if mask.any():
            # 既存レコードを更新
            status_df.loc[mask, '書類チェック結果'] = check_result
            status_df.loc[mask, '書類チェック更新日時'] = update_time
            status_df.loc[mask, 'チェック完了フラグ'] = self.determine_completion_flag(check_result)
            status_df.loc[mask, '最終チェック者'] = checker_name
            status_df.loc[mask, 'チェック詳細'] = check_result
        else:
            # 新規レコードを追加
            new_record = pd.DataFrame([{
                'クラブ名': club_name,
                '受付日時': reception_date,
                '書類チェック結果': check_result,
                '書類チェック更新日時': update_time,
                'チェック完了フラグ': self.determine_completion_flag(check_result),
                '最終チェック者': checker_name,
                'チェック詳細': check_result
            }])
            status_df = pd.concat([status_df, new_record], ignore_index=True)
        
        # 保存
        self.save_check_status(status_df)
        logging.info(f"クラブ '{club_name}' のチェック状況を更新しました")
        
        return status_df
    
    def determine_completion_flag(self, check_result):
        """
        チェック結果からチェック完了フラグを判定
        """
        if not check_result or pd.isna(check_result):
            return False
        
        # 簡潔形式の場合：エラー有や未チェックがない場合は完了
        result_str = str(check_result)
        if "エラー有" in result_str or "未チェック" in result_str:
            return False
        return True
    
    def get_completed_checks(self):
        """
        チェック完了済みのクラブリストを取得
        """
        status_df = self.load_check_status()
        completed_df = status_df[status_df['チェック完了フラグ'] == True]
        return completed_df
    
    def save_check_status(self, status_df):
        """
        チェック状況を保存
        """
        try:
            status_df.to_excel(self.status_file_path, index=False)
            logging.info(f"チェック状況を保存しました: {self.status_file_path}")
        except Exception as e:
            logging.error(f"チェック状況の保存に失敗: {e}")
    
    def merge_with_current_checklist(self, current_checklist_df):
        """
        現在のチェックリストと保存済みのチェック状況をマージ
        """
        saved_status_df = self.load_check_status()
        
        # 保存済みの完了チェック情報を現在のチェックリストに反映
        for index, row in current_checklist_df.iterrows():
            club_name = row['クラブ名']
            reception_date = str(row['受付日時'])
            
            # 保存済み情報から該当するレコードを検索
            mask = (saved_status_df['クラブ名'] == club_name) & (saved_status_df['受付日時'] == reception_date)
            matched_records = saved_status_df[mask]
            
            if not matched_records.empty and matched_records.iloc[0]['チェック完了フラグ']:
                # 完了済みの情報を反映
                saved_record = matched_records.iloc[0]
                current_checklist_df.at[index, '書類チェック結果'] = saved_record['書類チェック結果']
                current_checklist_df.at[index, '書類チェック更新日時'] = saved_record['書類チェック更新日時']
                logging.info(f"クラブ '{club_name}' の完了済みチェック結果を復元しました")
        
        return current_checklist_df
