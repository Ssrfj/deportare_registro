"""
メール文面案作成モジュール

チェック状況に応じたメールの文面案を作成する機能を提供します。
"""

import logging
import pandas as pd
import os
from .email_draft_generator import EmailDraftGenerator
from ..core.setting_paths import email_drafts_folder_path


def make_email_templates(latest_reception_data_date):
    """
    チェック状況に応じたメールの文面案を作成
    
    Args:
        latest_reception_data_date (str): 最新の受付データ日付
        
    Returns:
        dict: 生成されたファイルの辞書（クラブ名: ファイルパス）
        None: エラー時またはデータが見つからない場合
    """
    try:
        # 最新の総合チェックリストファイルを探す
        overall_checklist_folder = f"output/R7_登録受付処理/受付内容チェック/総合チェックリスト"
        
        if not os.path.exists(overall_checklist_folder):
            logging.warning(f"総合チェックリストフォルダが見つかりません: {overall_checklist_folder}")
            return None
        
        # 最新の総合チェックリストファイルを取得
        checklist_files = [f for f in os.listdir(overall_checklist_folder) if f.endswith('.xlsx')]
        if not checklist_files:
            logging.warning("総合チェックリストファイルが見つかりません")
            return None
        
        # 最新ファイルを選択
        latest_checklist_file = max(checklist_files)
        checklist_path = os.path.join(overall_checklist_folder, latest_checklist_file)
        
        logging.info(f"総合チェックリストを読み込み中: {checklist_path}")
        
        # 総合チェックリストを読み込み
        checklist_df = pd.read_excel(checklist_path)
        
        # メール文面案生成器を初期化
        email_generator = EmailDraftGenerator()
        
        # 一括でメール文面案を生成（EMLファイル有効、Outlookメールファイルは無効）
        generated_files = email_generator.generate_bulk_email_drafts(
            checklist_df=checklist_df,
            output_folder=email_drafts_folder_path,
            create_eml_files=True,  # EMLファイル作成を有効（メールアプリで開ける）
            create_outlook_files=False  # Outlookファイル作成を無効にして安定性を向上
        )
        
        if generated_files:
            logging.info(f"メール文面案を生成しました（{len(generated_files)}件）:")
            for club_name, file_path in generated_files.items():
                logging.info(f"  - {club_name}: {file_path}")
            return generated_files
        else:
            logging.info("エラーのあるクラブが見つからないため、メール文面案は生成されませんでした")
            return {}
        
    except Exception as e:
        logging.error(f"メール文面案作成中にエラーが発生しました: {e}")
        return None
