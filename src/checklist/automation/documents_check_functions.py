import pandas as pd
import logging
import json
import os

def load_checklist_config(config_name):
    """設定ファイルからチェックリスト列を読み込む"""
    config_path = os.path.join('config', 'checklist_columns', f'{config_name}.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"設定ファイル {config_path} の読み込みに失敗しました: {e}")
        return None

def check_document_1(row):
    error_dict = {}
    
    try:
        # DataFrameの場合は最初の行を取得
        if isinstance(row, pd.DataFrame):
            if row.empty:
                error_dict['e_d_1_001'] = '書類1のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row
        
        # 書類1: 人間のチェック結果を確認
        check_items = {
            'クラブ名': 'チェック項目_クラブ名',
            '申請種別': 'チェック項目_申請種別', 
            '住所': 'チェック項目_住所',
            '担当者名': 'チェック項目_担当者名',
            '連絡先': 'チェック項目_連絡先',
            '適合状況': 'チェック項目_適合状況'
        }
        
        # 各チェック項目を確認
        for item_name, check_column in check_items.items():
            if check_column in row_data.index:
                check_value = row_data[check_column]
                if pd.isna(check_value) or str(check_value).strip() == '' or str(check_value).strip() == '未チェック':
                    error_code = f'e_d_1_{list(check_items.keys()).index(item_name) + 1:03d}'
                    error_dict[error_code] = f'書類1: {item_name}が未チェックです'
                elif str(check_value).strip() == '0':
                    error_code = f'e_d_1_{list(check_items.keys()).index(item_name) + 1:03d}'
                    error_dict[error_code] = f'書類1: {item_name}に問題があります'
                # '1'の場合はエラーなし（何も追加しない）
            else:
                # チェック項目カラムが存在しない場合は「未チェック」として扱う
                error_code = f'e_d_1_{list(check_items.keys()).index(item_name) + 1:03d}'
                error_dict[error_code] = f'書類1: {item_name}が未チェックです'
                
    except Exception as e:
        logging.error(f"書類1のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_1_099'] = f'書類1のチェック状況の反映中にエラーが発生しました: {str(e)}'  
    
    return error_dict

def check_document_2_1(row):
    error_dict = {}
    
    try:
        # DataFrameの場合は最初の行を取得
        if isinstance(row, pd.DataFrame):
            if row.empty:
                error_dict['e_d_2_1_001'] = '書類2-1のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row
        
        # 書類2-1: 人間のチェック結果を確認
        check_items = {
            '会員数': 'チェック項目_会員数',
            'その他': 'チェック項目_その他'
        }
        
        # 各チェック項目を確認
        for item_name, check_column in check_items.items():
            if check_column in row_data.index:
                check_value = row_data[check_column]
                if pd.isna(check_value) or str(check_value).strip() == '' or str(check_value).strip() == '未チェック':
                    error_code = f'e_d_2_1_{list(check_items.keys()).index(item_name) + 1:03d}'
                    error_dict[error_code] = f'書類2-1: {item_name}が未チェックです'
                elif str(check_value).strip() == '0':
                    error_code = f'e_d_2_1_{list(check_items.keys()).index(item_name) + 1:03d}'
                    error_dict[error_code] = f'書類2-1: {item_name}に問題があります'
                # '1'の場合はエラーなし（何も追加しない）
            else:
                # チェック項目カラムが存在しない場合は「未チェック」として扱う
                error_code = f'e_d_2_1_{list(check_items.keys()).index(item_name) + 1:03d}'
                error_dict[error_code] = f'書類2-1: {item_name}が未チェックです'
        
        # 会員数の自動チェック（会員数データの存在と妥当性）
        member_columns = [
            '申請_会員_未就_男_数', '申請_会員_未就_女_数', '申請_会員_未就_不_数',
            '申請_会員_小_男_数', '申請_会員_小_女_数', '申請_会員_小_不_数',
            '申請_会員_中_男_数', '申請_会員_中_女_数', '申請_会員_中_不_数',
            '申請_会員_高_男_数', '申請_会員_高_女_数', '申請_会員_高_不_数',
            '申請_会員_20s_男_数', '申請_会員_20s_女_数', '申請_会員_20s_不_数',
            '申請_会員_30s_男_数', '申請_会員_30s_女_数', '申請_会員_30s_不_数',
            '申請_会員_40s_男_数', '申請_会員_40s_女_数', '申請_会員_40s_不_数',
            '申請_会員_50s_男_数', '申請_会員_50s_女_数', '申請_会員_50s_不_数',
            '申請_会員_60s_男_数', '申請_会員_60s_女_数', '申請_会員_60s_不_数',
            '申請_会員_70s_男_数', '申請_会員_70s_女_数', '申請_会員_70s_不_数'
        ]
        
        total_members = 0
        missing_columns = []
        
        # 自動チェックのエラーコードは5番以降を使用
        for column in member_columns:
            if column in row_data.index:
                value = row_data[column]
                if pd.isna(value) or str(value).strip() == '':
                    # 空の場合は0として扱う
                    continue
                try:
                    num_value = int(float(str(value)))
                    if num_value < 0:
                        error_dict[f'e_d_2_1_{member_columns.index(column) + 5:03d}'] = f'書類2-1: {column}に負の値が入力されています'
                    else:
                        total_members += num_value
                except (ValueError, TypeError):
                    error_dict[f'e_d_2_1_{member_columns.index(column) + 5:03d}'] = f'書類2-1: {column}に無効な値が入力されています'
            else:
                missing_columns.append(column)
        
        # 必要最小限のカラムが不足している場合
        if len(missing_columns) > len(member_columns) // 2:
            error_dict['e_d_2_1_095'] = f'書類2-1: 会員数データの必要な情報が不足しています'
        
        # 会員数が0の場合
        if total_members == 0:
            error_dict['e_d_2_1_096'] = '書類2-1: 総会員数が0です'
            
    except Exception as e:
        logging.error(f"書類2-1のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_2_1_099'] = f'書類2-1のチェック状況の反映中にエラーが発生しました: {str(e)}'  
    return error_dict

def check_document_2_2(row):
    error_dict = {}
    
    try:
        # DataFrameの場合は最初の行を取得
        if isinstance(row, pd.DataFrame):
            if row.empty:
                error_dict['e_d_2_2_001'] = '書類2-2のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row
        
        # 書類2-2: 人間のチェック結果を確認
        check_items = {
            '活動種目': 'チェック項目_活動種目',
            '指導者': 'チェック項目_指導者',
            '種目・指導者': 'チェック項目_種目・指導者',
            'クラブマネジャー配置': 'チェック項目_クラブマネジャー配置',
            'その他': 'チェック項目_その他'
        }
        
        # 各チェック項目を確認
        for item_name, check_column in check_items.items():
            if check_column in row_data.index:
                check_value = row_data[check_column]
                if pd.isna(check_value) or str(check_value).strip() == '' or str(check_value).strip() == '未チェック':
                    error_code = f'e_d_2_2_{list(check_items.keys()).index(item_name) + 1:03d}'
                    error_dict[error_code] = f'書類2-2: {item_name}が未チェックです'
                elif str(check_value).strip() == '0':
                    error_code = f'e_d_2_2_{list(check_items.keys()).index(item_name) + 1:03d}'
                    error_dict[error_code] = f'書類2-2: {item_name}に問題があります'
                # '1'の場合はエラーなし（何も追加しない）
            else:
                # チェック項目カラムが存在しない場合は「未チェック」として扱う
                error_code = f'e_d_2_2_{list(check_items.keys()).index(item_name) + 1:03d}'
                error_dict[error_code] = f'書類2-2: {item_name}が未チェックです'
        
        # 活動内容・指導者情報の自動チェック（エラーコードは10番以降を使用）
        
        # 活動種目のチェック（申請_種目_で始まるカラム）
        sport_columns = [col for col in row_data.index if col.startswith('申請_種目_') and not col.endswith('_数') and not col.endswith('_テキスト')]
        active_sports = []
        
        for col in sport_columns:
            value = row_data[col]
            if not pd.isna(value) and str(value).strip().lower() in ['1', 'true', 'yes', '○']:
                sport_name = col.replace('申請_種目_', '')
                active_sports.append(sport_name)
        
        if not active_sports:
            error_dict['e_d_2_2_010'] = '書類2-2: 活動種目が選択されていません'
        
        # 指導者のチェック（申請_指導者_で始まるカラム）
        instructor_columns = [col for col in row_data.index if col.startswith('申請_指導者_')]
        active_instructors = []
        
        for col in instructor_columns:
            value = row_data[col]
            if not pd.isna(value) and str(value).strip().lower() in ['1', 'true', 'yes', '○']:
                instructor_sport = col.replace('申請_指導者_', '')
                active_instructors.append(instructor_sport)
        
        if not active_instructors:
            error_dict['e_d_2_2_011'] = '書類2-2: 指導者情報が登録されていません'
        
        # マネジャー配置状況のチェック
        manager_placement = row_data.get('申請_マネジャー_配置状況')
        if pd.isna(manager_placement) or str(manager_placement).strip() == '':
            error_dict['e_d_2_2_003'] = '書類2-2: クラブマネジャー配置状況が未入力です'
        
        # マネジメント指導者資格のチェック
        management_cert = row_data.get('申請_マネジャー_マネ資格_数')
        if pd.isna(management_cert) or str(management_cert).strip() == '':
            error_dict['e_d_2_2_004'] = '書類2-2: マネジメント指導者資格数が未入力です'
        else:
            try:
                cert_count = int(float(str(management_cert)))
                if cert_count < 0:
                    error_dict['e_d_2_2_005'] = '書類2-2: マネジメント指導者資格数に負の値が入力されています'
            except (ValueError, TypeError):
                error_dict['e_d_2_2_006'] = '書類2-2: マネジメント指導者資格数に無効な値が入力されています'
            
    except Exception as e:
        logging.error(f"書類2-2のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_2_2_099'] = f'書類2-2のチェック状況の反映中にエラーが発生しました: {str(e)}'  
    return error_dict

def check_document_3(row):
    error_dict = {}
    
    try:
        # DataFrameの場合は最初の行を取得
        if isinstance(row, pd.DataFrame):
            if row.empty:
                error_dict['e_d_3_001'] = '書類3のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row
        
        # 書類3: 人間のチェック結果を確認
        check_items = {
            '組織の規約等である': 'チェック項目_組織の規約等である',
            '法人格': 'チェック項目_法人格',
            '会員資格': 'チェック項目_会員資格',
            '規約等の改廃意思決定機関': 'チェック項目_規約等の改廃意思決定機関',
            '事業計画の意思決定機関': 'チェック項目_事業計画の意思決定機関',
            '会計の意思決定機関': 'チェック項目_会計の意思決定機関',
            '監査': 'チェック項目_監査',
            'その他': 'チェック項目_その他'
        }
        
        # 各チェック項目を確認
        for item_name, check_column in check_items.items():
            if check_column in row_data.index:
                check_value = row_data[check_column]
                if pd.isna(check_value) or str(check_value).strip() == '' or str(check_value).strip() == '未チェック':
                    error_code = f'e_d_3_{list(check_items.keys()).index(item_name) + 1:03d}'
                    error_dict[error_code] = f'書類3: {item_name}が未チェックです'
                elif str(check_value).strip() == '0':
                    error_code = f'e_d_3_{list(check_items.keys()).index(item_name) + 1:03d}'
                    error_dict[error_code] = f'書類3: {item_name}に問題があります'
                # '1'の場合はエラーなし（何も追加しない）
            else:
                # チェック項目カラムが存在しない場合は「未チェック」として扱う
                error_code = f'e_d_3_{list(check_items.keys()).index(item_name) + 1:03d}'
                error_dict[error_code] = f'書類3: {item_name}が未チェックです'

    except Exception as e:
        logging.error(f"書類3のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_3_099'] = f'書類3のチェック状況の反映中にエラーが発生しました: {str(e)}'
    return error_dict

def check_document_4(row):
    error_dict = {}

    try:
        # DataFrameの場合は最初の行を取得
        if isinstance(row, pd.DataFrame):
            if row.empty:
                error_dict['e_d_4_001'] = '書類4のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row

        # 書類4: 人間のチェック結果を確認
        check_items = {
            '議決権保有者名簿1': 'チェック項目_議決権保有者名簿1',
            '議決権保有者名簿2': 'チェック項目_議決権保有者名簿2', 
            '議決権保有者名簿3': 'チェック項目_議決権保有者名簿3',
            '議決権保有者名簿4': 'チェック項目_議決権保有者名簿4',
            '議決権保有者名簿5': 'チェック項目_議決権保有者名簿5',
            'その他': 'チェック項目_その他'
        }
        
        # 各チェック項目を確認
        for item_name, check_column in check_items.items():
            if check_column in row_data.index:
                check_value = row_data[check_column]
                if pd.isna(check_value) or str(check_value).strip() == '' or str(check_value).strip() == '未チェック':
                    error_code = f'e_d_4_{list(check_items.keys()).index(item_name) + 1:03d}'
                    error_dict[error_code] = f'書類4: {item_name}が未チェックです'
                elif str(check_value).strip() == '0':
                    error_code = f'e_d_4_{list(check_items.keys()).index(item_name) + 1:03d}'
                    error_dict[error_code] = f'書類4: {item_name}に問題があります'
                # '1'の場合はエラーなし（何も追加しない）
            else:
                # チェック項目カラムが存在しない場合は「未チェック」として扱う
                error_code = f'e_d_4_{list(check_items.keys()).index(item_name) + 1:03d}'
                error_dict[error_code] = f'書類4: {item_name}が未チェックです'

    except Exception as e:
        logging.error(f"書類4のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_4_099'] = f'書類4のチェック状況の反映中にエラーが発生しました: {str(e)}'      
    return error_dict

def check_document_5_budget(row):
    error_dict = {}
    
    try:
        # DataFrameの場合は最初の行を取得
        if isinstance(row, pd.DataFrame):
            if row.empty:
                error_dict['e_d_5_b_001'] = '書類5（予算）のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row
        
        # 書類5（予算）: 人間のチェック結果を確認
        check_items = {
            '予算': 'チェック項目_予算',
            'その他': 'チェック項目_その他'
        }
        
        # 各チェック項目を確認
        for item_name, check_column in check_items.items():
            if check_column in row_data.index:
                check_value = row_data[check_column]
                if pd.isna(check_value) or str(check_value).strip() == '' or str(check_value).strip() == '未チェック':
                    error_code = f'e_d_5_b_{list(check_items.keys()).index(item_name) + 1:03d}'
                    error_dict[error_code] = f'書類5（予算）: {item_name}が未チェックです'
                elif str(check_value).strip() == '0':
                    error_code = f'e_d_5_b_{list(check_items.keys()).index(item_name) + 1:03d}'
                    error_dict[error_code] = f'書類5（予算）: {item_name}に問題があります'
                # '1'の場合はエラーなし（何も追加しない）
            else:
                # チェック項目カラムが存在しない場合は「未チェック」として扱う
                error_code = f'e_d_5_b_{list(check_items.keys()).index(item_name) + 1:03d}'
                error_dict[error_code] = f'書類5（予算）: {item_name}が未チェックです'
            
    except Exception as e:
        logging.error(f"書類5（予算）のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_5_b_099'] = f'書類5（予算）のチェック状況の反映中にエラーが発生しました: {str(e)}'  
    return error_dict

def check_document_5_plan(row):
    # ロギングの設定    logging.info("ロギングを設定しました")
    # フォルダの作成    logging.info("フォルダを作成しました")

    error_dict = {}
    
    try:
        # DataFrameの場合は最初の行を取得
        if isinstance(row, pd.DataFrame):
            if row.empty:
                error_dict['e_d_5_p_001'] = '書類5（計画）のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row

        # 設定ファイルから列情報を読み込み
        config = load_checklist_config('document05_plan_checklist_columns')
        check_column = 'チェック項目_計画' if config else None
        
        # 書類5（計画）: 事業計画書の提出状況チェック
        plan_file = row_data.get('申請_事業計画_書類')
        if pd.isna(plan_file) or str(plan_file).strip() == '':
            error_dict['e_d_5_p_001'] = '書類5（計画）: 事業計画書が提出されていません'
        else:
            # 書類が提出されている場合は人間のチェック結果を確認
            if check_column and check_column in row_data.index:
                check_value = row_data[check_column]
                if pd.isna(check_value) or str(check_value).strip() == '' or str(check_value).strip() == '未チェック':
                    error_dict['e_d_5_p_002'] = '書類5（計画）: 未チェックです'
                elif str(check_value).strip() == '0':
                    error_dict['e_d_5_p_002'] = '書類5（計画）: 事業計画書に問題があります'
                # '1'の場合はエラーなし（何も追加しない）
            else:
                # チェック列が存在しない場合は「未チェック」として扱う
                error_dict['e_d_5_p_002'] = '書類5（計画）: 未チェックです'
        
        # 決議機関名称のチェック
        plan_authority = row_data.get('申請_事業計画_決議機関名称')
        if pd.isna(plan_authority) or str(plan_authority).strip() == '':
            error_dict['e_d_5_p_003'] = '書類5（計画）: 事業計画決議機関名称が未入力です'
        
        # 決議日のチェック
        plan_decision_date = row_data.get('申請_事業計画_決議日')
        if pd.isna(plan_decision_date) or str(plan_decision_date).strip() == '':
            error_dict['e_d_5_p_004'] = '書類5（計画）: 事業計画決議日が未入力です'
            
    except Exception as e:
        logging.error(f"書類5（計画）のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_5_p_099'] = f'書類5（計画）のチェック状況の反映中にエラーが発生しました: {str(e)}'  
    return error_dict

def check_document_6_financial_statements(row):
    # ロギングの設定    logging.info("ロギングを設定しました")
    # フォルダの作成    logging.info("フォルダを作成しました")

    error_dict = {}
    
    try:
        # DataFrameの場合は最初の行を取得
        if isinstance(row, pd.DataFrame):
            if row.empty:
                error_dict['e_d_6_f_001'] = '書類6（決算）のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row

        # 設定ファイルから列情報を読み込み
        config = load_checklist_config('document06_financial_statements_checklist_columns')
        check_column = 'チェック項目_決算' if config else None
        
        # 書類6（決算）: 申請データの存在確認
        # 提出有無の確認
        submission_status = row_data.get('申請_決算_提出有無')
        if pd.isna(submission_status) or str(submission_status).strip() == '':
            error_dict['e_d_6_f_001'] = '書類6（決算）: 提出有無が未選択です'
        elif str(submission_status).strip().lower() in ['1', 'true', 'yes', '提出']:
            # 提出する場合は書類ファイルをチェック
            document_file = row_data.get('申請_決算_書類(選択時必須)')
            if pd.isna(document_file) or str(document_file).strip() == '':
                error_dict['e_d_6_f_002'] = '書類6（決算）: 書類が提出されていません'
            else:
                # 書類が提出されている場合は人間のチェック結果を確認
                if check_column and check_column in row_data.index:
                    check_value = row_data[check_column]
                    if pd.isna(check_value) or str(check_value).strip() == '' or str(check_value).strip() == '未チェック':
                        error_dict['e_d_6_f_003'] = '書類6（決算）: 未チェックです'
                    elif str(check_value).strip() == '0':
                        error_dict['e_d_6_f_003'] = '書類6（決算）: 決算書類に問題があります'
                    # '1'の場合はエラーなし（何も追加しない）
                else:
                    # チェック列が存在しない場合は「未チェック」として扱う
                    error_dict['e_d_6_f_003'] = '書類6（決算）: 未チェックです'
        # 提出しない場合は何もしない
            
    except Exception as e:
        logging.error(f"書類6（決算）のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_6_f_099'] = f'書類6（決算）のチェック状況の反映中にエラーが発生しました: {str(e)}'  
    return error_dict

def check_document_6_report(row):
    # ロギングの設定    logging.info("ロギングを設定しました")
    # フォルダの作成    logging.info("フォルダを作成しました")

    error_dict = {}

    try:
        # DataFrameの場合は最初の行を取得
        if isinstance(row, pd.DataFrame):
            if row.empty:
                error_dict['e_d_6_r_001'] = '書類6（事業報告）のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row

        # 設定ファイルから列情報を読み込み
        config = load_checklist_config('document06_report_checklist_columns')
        check_column = 'チェック項目_報告' if config else None

        # 書類6（事業報告）: 申請データの存在確認
        # 提出有無の確認
        submission_status = row_data.get('申請_事業報告_提出有無')
        if pd.isna(submission_status) or str(submission_status).strip() == '':
            error_dict['e_d_6_r_001'] = '書類6（事業報告）: 提出有無が未選択です'
        elif str(submission_status).strip().lower() in ['1', 'true', 'yes', '提出']:
            # 提出する場合は書類ファイルをチェック
            document_file = row_data.get('申請_事業報告_事業報告_書類(選択時必須)')
            if pd.isna(document_file) or str(document_file).strip() == '':
                error_dict['e_d_6_r_002'] = '書類6（事業報告）: 書類が提出されていません'
            else:
                # 書類が提出されている場合は人間のチェック結果を確認
                if check_column and check_column in row_data.index:
                    check_value = row_data[check_column]
                    if pd.isna(check_value) or str(check_value).strip() == '' or str(check_value).strip() == '未チェック':
                        error_dict['e_d_6_r_003'] = '書類6（事業報告）: 未チェックです'
                    elif str(check_value).strip() == '0':
                        error_dict['e_d_6_r_003'] = '書類6（事業報告）: 事業報告書類に問題があります'
                    # '1'の場合はエラーなし（何も追加しない）
                else:
                    # チェック列が存在しない場合は「未チェック」として扱う
                    error_dict['e_d_6_r_003'] = '書類6（事業報告）: 未チェックです'
        # 提出しない場合は何もしない

    except Exception as e:
        logging.error(f"書類6（事業報告）のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_6_r_099'] = f'書類6（事業報告）のチェック状況の反映中にエラーが発生しました: {str(e)}'
    return error_dict

def check_document_7(row):
    # ロギングの設定    logging.info("ロギングを設定しました")
    # フォルダの作成    logging.info("フォルダを作成しました")

    error_dict = {}

    try:
        # DataFrameの場合は最初の行を取得
        if isinstance(row, pd.DataFrame):
            if row.empty:
                error_dict['e_d_7_001'] = '書類7（自己点検）のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row

        # 書類7（自己点検）: 人間のチェック結果を確認
        check_column = 'チェック項目_自己点検・評価'
        
        if check_column in row_data.index:
            check_value = row_data[check_column]
            if pd.isna(check_value) or str(check_value).strip() == '' or str(check_value).strip() == '未チェック':
                error_dict['e_d_7_001'] = '書類7（自己点検）: 自己点検・評価が未チェックです'
            elif str(check_value).strip() == '0':
                error_dict['e_d_7_001'] = '書類7（自己点検）: 自己点検・評価に問題があります'
            # '1'の場合はエラーなし（何も追加しない）
        else:
            error_dict['e_d_7_001'] = '書類7（自己点検）: 自己点検・評価が未チェックです'

    except Exception as e:
        logging.error(f"書類7（自己点検）のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_7_099'] = f'書類7（自己点検）のチェック状況の反映中にエラーが発生しました: {str(e)}'      
    return error_dict

def check_document_8(row):
    # ロギングの設定    logging.info("ロギングを設定しました")
    # フォルダの作成    logging.info("フォルダを作成しました")

    error_dict = {}

    try:
        # DataFrameの場合は最初の行を取得
        if isinstance(row, pd.DataFrame):
            if row.empty:
                error_dict['e_d_8_001'] = '書類8（議事録）のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row

        # 設定ファイルから列情報を読み込み
        config = load_checklist_config('document08_checklist_columns')
        check_column = 'チェック項目_議事録' if config else None

        # 書類8（議事録）: 申請データの存在確認
        # 議事録関連のファイルが複数存在するため、関連するファイルをチェック
        
        # 事業計画議事録
        plan_minutes = row_data.get('申請_事業計画_議事録_書類')
        if pd.isna(plan_minutes) or str(plan_minutes).strip() == '':
            error_dict['e_d_8_001'] = '書類8（議事録）: 事業計画議事録が提出されていません'

        # 予算議事録
        budget_minutes = row_data.get('申請_予算_議事録_書類')
        if pd.isna(budget_minutes) or str(budget_minutes).strip() == '':
            error_dict['e_d_8_002'] = '書類8（議事録）: 予算議事録が提出されていません'
        
        # いずれかの議事録が提出されている場合は人間のチェック結果を確認
        if not pd.isna(plan_minutes) and str(plan_minutes).strip() != '' or \
           not pd.isna(budget_minutes) and str(budget_minutes).strip() != '':
            if check_column and check_column in row_data.index:
                check_value = row_data[check_column]
                if pd.isna(check_value) or str(check_value).strip() == '' or str(check_value).strip() == '未チェック':
                    error_dict['e_d_8_003'] = '書類8（議事録）: 未チェックです'
                elif str(check_value).strip() == '0':
                    error_dict['e_d_8_003'] = '書類8（議事録）: 議事録に問題があります'
                # '1'の場合はエラーなし（何も追加しない）
            else:
                # チェック列が存在しない場合は「未チェック」として扱う
                error_dict['e_d_8_003'] = '書類8（議事録）: 未チェックです'

    except Exception as e:
        logging.error(f"書類8（議事録）のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_8_099'] = f'書類8（議事録）のチェック状況の反映中にエラーが発生しました: {str(e)}'        
    return error_dict

def check_document_9(row):
    # ロギングの設定    logging.info("ロギングを設定しました")
    # フォルダの作成    logging.info("フォルダを作成しました")

    error_dict = {}

    try:
        # DataFrameの場合は最初の行を取得
        if isinstance(row, pd.DataFrame):
            if row.empty:
                error_dict['e_d_9_001'] = '書類9（自己説明）のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row

        # 書類9（自己説明）: 人間のチェック結果を確認
        check_column = 'チェック項目_自己説明'
        
        if check_column in row_data.index:
            check_value = row_data[check_column]
            if pd.isna(check_value) or str(check_value).strip() == '' or str(check_value).strip() == '未チェック':
                error_dict['e_d_9_001'] = '書類9（自己説明）: 自己説明が未チェックです'
            elif str(check_value).strip() == '0':
                error_dict['e_d_9_001'] = '書類9（自己説明）: 自己説明に問題があります'
            # '1'の場合はエラーなし（何も追加しない）
        else:
            error_dict['e_d_9_001'] = '書類9（自己説明）: 自己説明が未チェックです'

    except Exception as e:
        logging.error(f"書類9（自己説明）のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_9_099'] = f'書類9（自己説明）のチェック状況の反映中にエラーが発生しました: {str(e)}'      
    return error_dict

def check_document_10(row):
    # ロギングの設定    logging.info("ロギングを設定しました")
    # フォルダの作成    logging.info("フォルダを作成しました")

    error_dict = {}

    try:
        # DataFrameの場合は最初の行を取得
        if isinstance(row, pd.DataFrame):
            if row.empty:
                error_dict['e_d_10_001'] = '書類10（届出）のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row

        # 設定ファイルから列情報を読み込み
        config = load_checklist_config('document10_checklist_columns')
        check_column = 'チェック項目_届出' if config else None

        # 書類10（届出）: 人間のチェック結果を確認
        if check_column and check_column in row_data.index:
            check_value = row_data[check_column]
            if pd.isna(check_value) or str(check_value).strip() == '' or str(check_value).strip() == '未チェック':
                error_dict['e_d_10_001'] = '書類10（届出）: 未チェックです'
            elif str(check_value).strip() == '0':
                error_dict['e_d_10_001'] = '書類10（届出）: 届出に問題があります'
            # '1'の場合はエラーなし（何も追加しない）
        else:
            # チェック列が存在しない場合は「未チェック」として扱う
            error_dict['e_d_10_001'] = '書類10（届出）: 未チェックです'

    except Exception as e:
        logging.error(f"書類10（届出）のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_10_099'] = f'書類10（届出）のチェック状況の反映中にエラーが発生しました: {str(e)}'        
    return error_dict



