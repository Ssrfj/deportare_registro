import pandas as pd
import logging
import json
import os
from datetime import datetime, timezone, timedelta

def load_consistency_check_config():
    """一貫性チェック設定ファイルを読み込む"""
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
        'config', 'checklist_columns', 'consistency_check_config.json'
    )
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        logging.info(f"一貫性チェック設定を読み込みました: {config_path}")
        return config
    except Exception as e:
        logging.error(f"一貫性チェック設定の読み込みに失敗しました: {e}")
        return None

def check_consistency_with_config(row, consistency_type):
    """設定ベースの一貫性チェック"""
    error_dict = {}
    
    try:
        # 設定を読み込み
        config = load_consistency_check_config()
        if not config or consistency_type not in config:
            error_dict[f'e_config_001'] = f'{consistency_type}の設定が見つかりません'
            return error_dict
        
        type_config = config[consistency_type]
        check_columns = type_config.get('check_columns', [])
        error_prefix = type_config.get('error_prefix', 'e_c')
        display_name = type_config.get('display_name', consistency_type)
        
        # DataFrameの場合は最初の行を取得
        if isinstance(row, pd.DataFrame):
            if row.empty:
                error_dict[f'{error_prefix}_001'] = f'{display_name}一貫性のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row
        
        # 各チェック項目を確認
        for i, check_column in enumerate(check_columns, 1):
            if check_column in row_data.index:
                check_value = row_data[check_column]
                if pd.isna(check_value) or str(check_value).strip() == '' or str(check_value).strip() == '未チェック':
                    error_dict[f'{error_prefix}_{i:03d}'] = f'{display_name}: {check_column.replace("チェック項目_", "")}が未チェックです'
                elif str(check_value).strip() == '0':
                    error_dict[f'{error_prefix}_{i:03d}'] = f'{display_name}: {check_column.replace("チェック項目_", "")}に問題があります'
                # '1'の場合はエラーなし（何も追加しない）
            else:
                # チェック列が存在しない場合は「未チェック」として扱う
                error_dict[f'{error_prefix}_{i:03d}'] = f'{display_name}: {check_column.replace("チェック項目_", "")}が未チェックです'
                
    except Exception as e:
        logging.error(f"{display_name}一貫性のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict[f'{error_prefix}_099'] = f'{display_name}一貫性のチェック状況の反映中にエラーが発生しました: {str(e)}'
    
    return error_dict

def check_consistency_disciplines(row):
    """活動種目の一貫性チェック"""
    return check_consistency_with_config(row, 'consistency_disciplines')

def check_consistency_members_and_voting_rights(row):
    """会員と議決権の一貫性チェック"""
    return check_consistency_with_config(row, 'consistency_members_and_voting_rights')

def check_consistency_meeting_minutes(row):
    """議事録の一貫性チェック"""
    return check_consistency_with_config(row, 'consistency_meeting_minutes')

def update_consistency_check_status(overall_checklist_df, checklist_file_path, club_reception_df, latest_reception_data_date):
    import os
    import pandas as pd
    import logging
    from datetime import datetime, timezone, timedelta
    from src.core.setting_paths import overall_checklist_folder_path
    from src.core.utils import get_jst_now, ensure_date_string
    from src.core.load_latest_club_data import load_latest_club_reception_data, get_club_data_by_name_and_date

    # 統合されたクラブ情報付き受付データを読み込み
    logging.info("統合されたクラブ情報付き受付データを読み込みます")
    integrated_club_data = load_latest_club_reception_data()
    if integrated_club_data is None:
        logging.error("統合されたクラブ情報付き受付データの読み込みに失敗しました")
        return overall_checklist_df

    # checklist_status_dfに 'クラブ名' と '申請日時' カラムが存在するか確認
    # overall_checklist_dfがDataFrameであることを確認
    if not isinstance(overall_checklist_df, pd.DataFrame):
        logging.error("overall_checklist_dfはDataFrameではありません。")
        return
    # overall_checklist_dfに 'クラブ名'カラムが存在するか確認
    if 'クラブ名' not in overall_checklist_df.columns:
        logging.error("'クラブ名' カラムが overall_checklist_df に存在しません。")
        return
    # overall_checklist_dfに '受付日時'カラムが存在するか確認
    if '受付日時' not in overall_checklist_df.columns:
        logging.error("'受付日時' カラムが overall_checklist_df に存在しません。")
        return

    # overall_checklist_dfの行ごとに処理を行う
    for index, row in overall_checklist_df.iterrows():
        club_name = str(row['クラブ名']).strip()
        apried_date_str = str(row.get('受付日時')).strip()
        # ここで小数点以下を除去
        if '.' in apried_date_str:
            apried_date_str = apried_date_str.split('.')[0]
        if 'チェックリスト作成日時' not in row.index:
            logging.warning(f"'チェックリスト作成日時' カラムが存在しません。クラブ '{club_name}' をスキップします。rowのカラム: {row.index.tolist()}")
            continue
            
        # 処理開始のメッセージを表示
        logging.info(f"クラブ名: {club_name} の一貫性チェックを開始します")
        
        # 統合されたクラブ情報付き受付データから該当行を取得
        target_row = get_club_data_by_name_and_date(integrated_club_data, club_name, apried_date_str)
        
        if target_row.empty:
            logging.warning(f"統合データに該当クラブのデータが見つかりません: {club_name}, {apried_date_str}")
            continue
        
        # 一貫性チェックが既に実行済みかを確認（書類間チェック結果で判断）
        consistency_check_result = overall_checklist_df.loc[index, '書類間チェック結果']
        if pd.notna(consistency_check_result) and str(consistency_check_result).strip() not in ['', '未チェック']:
            logging.info(f"クラブ '{club_name}' の申請日時'{apried_date_str}'の申請は一貫性チェック済みです（結果: {consistency_check_result}）。スキップします。")
            continue
        else:
            logging.info(f"クラブ '{club_name}' の申請日時'{apried_date_str}'の申請は一貫性チェックを実行します。")
        
        jst_now = datetime.now(timezone(timedelta(hours=9)))
        update_datetime = jst_now.strftime('%Y-%m-%d %H:%M:%S')
        
        # 各一貫性チェック関数を実行して結果を統合
        try:
            all_consistency_errors = {}
            
            # 活動種目の一貫性チェック
            disciplines_result = check_consistency_disciplines(target_row)
            if disciplines_result:
                all_consistency_errors.update(disciplines_result)
            
            # 会議録の一貫性チェック
            meeting_minutes_result = check_consistency_meeting_minutes(target_row)
            if meeting_minutes_result:
                all_consistency_errors.update(meeting_minutes_result)
            
            # 会員情報と議決権の一貫性チェック
            member_voting_result = check_consistency_members_and_voting_rights(target_row)
            if member_voting_result:
                all_consistency_errors.update(member_voting_result)
            
            # 統合されたエラー辞書を文字列として書類間チェック結果に設定
            if all_consistency_errors:
                consistency_result_summary = str(all_consistency_errors)
            else:
                consistency_result_summary = "チェック済み"
            
            overall_checklist_df.loc[index, '書類間チェック結果'] = consistency_result_summary
            overall_checklist_df.loc[index, '書類間チェック更新日時'] = update_datetime
            
            logging.info(f"クラブ名: {club_name} の一貫性チェックが完了しました")
            logging.debug(f"一貫性チェック結果: {consistency_result_summary}")
            
        except Exception as e:
            logging.error(f"クラブ '{club_name}' の一貫性チェック中にエラーが発生しました: {e}")
            continue
            
    logging.info("全てのクラブの一貫性チェックが完了しました。")

    # 総合チェックリストのファイルを保存（ファイル名は「総合チェックリスト_受付{YYYYMMDDHHMMSS}_更新{YYYYMMDDHHMMSS}.xlsx」）
    logging.info("総合チェックリストのファイルを保存します")
    now_jst = get_jst_now()
    reception_date_str = ensure_date_string(latest_reception_data_date)
    overall_checklist_file_name = f'総合チェックリスト_受付{reception_date_str}_更新{now_jst.strftime("%Y%m%d%H%M%S")}.xlsx'
    overall_checklist_file_path = os.path.join(overall_checklist_folder_path, overall_checklist_file_name)
    overall_checklist_df.to_excel(overall_checklist_file_path, index=False)
    logging.info(f"総合チェックリストのファイルを保存しました: {overall_checklist_file_path}")
    logging.info("一貫性チェックが完了しました")
    return overall_checklist_df