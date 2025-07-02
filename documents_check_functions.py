import pandas as pd
import logging
from datetime import datetime, date
from setting_paths import content_check_folder_path, reception_statues_folder_path
from make_folders import setup_logging, create_folders

def check_document_1(row):
    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()
    logging.info("フォルダを作成しました")

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
        
        # 必要なカラムが存在するかチェック
        # 書類1のチェック項目
        check_columns_document_1 = [
            'チェック項目_クラブ名',
            'チェック項目_申請種別',
            'チェック項目_住所',
            'チェック項目_担当者名',
            'チェック項目_連絡先',
            'チェック項目_適合状況'
        ]
        # 書類1のチェック担当者のカラム
        person_in_charge_column_document_1 = 'チェック者名_受付内容'
        
        # まず通常のチェック項目をチェック
        for column in check_columns_document_1:
            if column in row_data.index:
                # カラムが存在する場合、値のチェック
                # 値がNaNまたは空文字列の場合、error_dictにf'{column}が未入力です'を追加
                if pd.isna(row_data[column]) or str(row_data[column]).strip() == '':
                    error_dict[f'e_d_1_{check_columns_document_1.index(column) + 1:03d}'] = f'{column}が未入力です'
                # 「0」であれば、error_dictにf'{column}に不備があります'を追加
                elif str(row_data[column]).strip() == '0':
                    error_dict[f'e_d_1_{check_columns_document_1.index(column) + 1:03d}'] = f'{column}に不備があります'
                # 「1」であれば、error_dictに追加しない
                elif str(row_data[column]).strip() == '1':
                    pass
                # それ以外の値の場合、error_dictにf'{column}の値が不正です'を追加
                else:
                    error_dict[f'e_d_1_{check_columns_document_1.index(column) + 1:03d}'] = f'{column}の値が不正です'
            # カラムが存在しない場合、error_dictにf'{column}のカラムが見つかりません'を追加
            else:
                error_dict[f'e_d_1_{check_columns_document_1.index(column) + 1:03d}'] = f'{column}のカラムが見つかりません'
        
        # チェック担当者のカラムを別途チェック
        if person_in_charge_column_document_1 in row_data.index:
            value = row_data[person_in_charge_column_document_1]
            # 値がNaNまたは空文字列の場合は何もしない
            if not (pd.isna(value) or str(value).strip() == ''):
                value_str = str(value).strip()
                # 数字のみの場合は「不正です」エラーを返す
                if value_str.isdigit():
                    error_dict['e_d_1_003'] = '書類1のチェック担当者欄に数字が入力されています。文字列を入力してください。'
                # 文字列が入っている場合はerror_dictに担当者名を追加
                else:
                    error_dict['書類1_チェック担当者'] = value_str
        else:
            error_dict[f'e_d_1_{len(check_columns_document_1) + 1:03d}'] = f'{person_in_charge_column_document_1}のカラムが見つかりません'
            
    except Exception as e:
        logging.error(f"書類1のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_1_002'] = f'書類1のチェック状況の反映中にエラーが発生しました: {str(e)}'  
    return error_dict

def check_document_2_1(row):
    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()
    logging.info("フォルダを作成しました")

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
        
        # 書類2-1のチェック項目
        check_columns_document_2_1 = [
            'チェック項目_会員数'
        ]
        # 書類2-1のチェック担当者のカラム
        person_in_charge_column_document_2_1 = 'チェック者名_会員数'
        
        # まず通常のチェック項目をチェック
        for column in check_columns_document_2_1:
            if column in row_data.index:
                # カラムが存在する場合、値のチェック
                # 値がNaNまたは空文字列の場合、error_dictにf'{column}が未入力です'を追加
                if pd.isna(row_data[column]) or str(row_data[column]).strip() == '':
                    error_dict[f'e_d_2_1_{check_columns_document_2_1.index(column) + 1:03d}'] = f'{column}が未入力です'
                # 「0」であれば、error_dictにf'{column}に不備があります'を追加
                elif str(row_data[column]).strip() == '0':
                    error_dict[f'e_d_2_1_{check_columns_document_2_1.index(column) + 1:03d}'] = f'{column}に不備があります'
                # 「1」であれば、error_dictに追加しない
                elif str(row_data[column]).strip() == '1':
                    pass
                # それ以外の値の場合、error_dictにf'{column}の値が不正です'を追加
                else:
                    error_dict[f'e_d_2_1_{check_columns_document_2_1.index(column) + 1:03d}'] = f'{column}の値が不正です'
            # カラムが存在しない場合、error_dictにf'{column}のカラムが見つかりません'を追加
            else:
                error_dict[f'e_d_2_1_{check_columns_document_2_1.index(column) + 1:03d}'] = f'{column}のカラムが見つかりません'
        
        # チェック担当者のカラムを別途チェック
        if person_in_charge_column_document_2_1 in row_data.index:
            value = row_data[person_in_charge_column_document_2_1]
            # 値がNaNまたは空文字列の場合は何もしない
            if not (pd.isna(value) or str(value).strip() == ''):
                value_str = str(value).strip()
                # 数字のみの場合は「不正です」エラーを返す
                if value_str.isdigit():
                    error_dict['e_d_2_1_003'] = '書類2-1のチェック担当者欄に数字が入力されています。文字列を入力してください。'
                # 文字列が入っている場合はerror_dictに担当者名を追加
                else:
                    error_dict['書類2_1_チェック担当者'] = value_str
        else:
            error_dict[f'e_d_2_1_{len(check_columns_document_2_1) + 1:03d}'] = f'{person_in_charge_column_document_2_1}のカラムが見つかりません'
            
    except Exception as e:
        logging.error(f"書類2-1のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_2_1_002'] = f'書類2-1のチェック状況の反映中にエラーが発生しました: {str(e)}'  
    return error_dict

def check_document_2_2(row):
    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()
    logging.info("フォルダを作成しました")

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
        
        # 書類2-2のチェック項目
        check_columns_document_2_2 = [
            'チェック項目_活動種目',
            'チェック項目_指導者',
            'チェック項目_種目・指導者',
            'チェック項目_クラブマネジャー配置',
            '申請_チェック項目_マネジメント指導者資格'
        ]
        # 書類2-2のチェック担当者のカラム
        person_in_charge_column_document_2_2 = 'チェック者名_活動内容'
        
        # まず通常のチェック項目をチェック
        for column in check_columns_document_2_2:
            if column in row_data.index:
                # カラムが存在する場合、値のチェック
                # 値がNaNまたは空文字列の場合、error_dictにf'{column}が未入力です'を追加
                if pd.isna(row_data[column]) or str(row_data[column]).strip() == '':
                    error_dict[f'e_d_2_2_{check_columns_document_2_2.index(column) + 1:03d}'] = f'{column}が未入力です'
                # 「0」であれば、error_dictにf'{column}に不備があります'を追加
                elif str(row_data[column]).strip() == '0':
                    error_dict[f'e_d_2_2_{check_columns_document_2_2.index(column) + 1:03d}'] = f'{column}に不備があります'
                # 「1」であれば、error_dictに追加しない
                elif str(row_data[column]).strip() == '1':
                    pass
                # それ以外の値の場合、error_dictにf'{column}の値が不正です'を追加
                else:
                    error_dict[f'e_d_2_2_{check_columns_document_2_2.index(column) + 1:03d}'] = f'{column}の値が不正です'
            # カラムが存在しない場合、error_dictにf'{column}のカラムが見つかりません'を追加
            else:
                error_dict[f'e_d_2_2_{check_columns_document_2_2.index(column) + 1:03d}'] = f'{column}のカラムが見つかりません'
        
        # チェック担当者のカラムを別途チェック
        if person_in_charge_column_document_2_2 in row_data.index:
            value = row_data[person_in_charge_column_document_2_2]
            # 値がNaNまたは空文字列の場合は何もしない
            if not (pd.isna(value) or str(value).strip() == ''):
                value_str = str(value).strip()
                # 数字のみの場合は「不正です」エラーを返す
                if value_str.isdigit():
                    error_dict['e_d_2_2_003'] = '書類2-2のチェック担当者欄に数字が入力されています。文字列を入力してください。'
                # 文字列が入っている場合はerror_dictに担当者名を追加
                else:
                    error_dict['書類2_2_チェック担当者'] = value_str
        else:
            error_dict[f'e_d_2_2_{len(check_columns_document_2_2) + 1:03d}'] = f'{person_in_charge_column_document_2_2}のカラムが見つかりません'
            
    except Exception as e:
        logging.error(f"書類2-2のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_2_2_002'] = f'書類2-2のチェック状況の反映中にエラーが発生しました: {str(e)}'  
    return error_dict

def check_document_3(row):
    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()
    logging.info("フォルダを作成しました")

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
        
        # 書類3のチェック項目
        check_columns_document_3 = [
            'チェック項目_組織の規約等である',
            'チェック項目_法人格',
            'チェック項目_会員資格',
            'チェック項目_規約等の改廃意思決定機関',
            'チェック項目_事業計画の意思決定機関',
            'チェック項目_予算の意思決定機関',
            'チェック項目_事業報告の意思決定機関',
            'チェック項目_決算の意思決定機関',
            'チェック項目_役員資格・選任規程',
            'チェック項目_その他規程'
        ]
        # 書類3のチェック担当者のカラム
        person_in_charge_column_document_3 = 'チェック者名_規約等'
        
        # まず通常のチェック項目をチェック
        for column in check_columns_document_3:
            if column in row_data.index:
                # カラムが存在する場合、値のチェック
                # 値がNaNまたは空文字列の場合、error_dictにf'{column}が未入力です'を追加
                if pd.isna(row_data[column]) or str(row_data[column]).strip() == '':
                    error_dict[f'e_d_3_{check_columns_document_3.index(column) + 1:03d}'] = f'{column}が未入力です'
                # 「0」であれば、error_dictにf'{column}に不備があります'を追加
                elif str(row_data[column]).strip() == '0':
                    error_dict[f'e_d_3_{check_columns_document_3.index(column) + 1:03d}'] = f'{column}に不備があります'
                # 「1」であれば、error_dictに追加しない
                elif str(row_data[column]).strip() == '1':
                    pass
                # それ以外の値の場合、error_dictにf'{column}の値が不正です'を追加
                else:
                    error_dict[f'e_d_3_{check_columns_document_3.index(column) + 1:03d}'] = f'{column}の値が不正です'
            # カラムが存在しない場合、error_dictにf'{column}のカラムが見つかりません'を追加
            else:
                error_dict[f'e_d_3_{check_columns_document_3.index(column) + 1:03d}'] = f'{column}のカラムが見つかりません'
        
        # チェック担当者のカラムを別途チェック
        if person_in_charge_column_document_3 in row_data.index:
            value = row_data[person_in_charge_column_document_3]
            # 値がNaNまたは空文字列の場合は何もしない
            if not (pd.isna(value) or str(value).strip() == ''):
                value_str = str(value).strip()
                # 数字のみの場合は「不正です」エラーを返す
                if value_str.isdigit():
                    error_dict['e_d_3_003'] = '書類3のチェック担当者欄に数字が入力されています。文字列を入力してください。'
                # 文字列が入っている場合はerror_dictに担当者名を追加
                else:
                    error_dict['書類3_チェック担当者'] = value_str
        else:
            error_dict[f'e_d_3_{len(check_columns_document_3) + 1:03d}'] = f'{person_in_charge_column_document_3}のカラムが見つかりません'
            
    except Exception as e:
        logging.error(f"書類3のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_3_002'] = f'書類3のチェック状況の反映中にエラーが発生しました: {str(e)}'  
    return error_dict

def check_document_4(row):
    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()
    logging.info("フォルダを作成しました")

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
        
        # 書類4のチェック項目
        check_columns_document_4 = [
            'チェック項目_議決権保有者名簿1',
            'チェック項目_議決権保有者名簿2',
            'チェック項目_議決権保有者名簿3',
            'チェック項目_議決権保有者名簿4',
            'チェック項目_議決権保有者名簿5'
        ]
        # 書類4のチェック担当者のカラム
        person_in_charge_column_document_4 = 'チェック者名_議決権保有者名簿'
        
        # まず通常のチェック項目をチェック
        for column in check_columns_document_4:
            if column in row_data.index:
                # カラムが存在する場合、値のチェック
                # 値がNaNまたは空文字列の場合、error_dictにf'{column}が未入力です'を追加
                if pd.isna(row_data[column]) or str(row_data[column]).strip() == '':
                    error_dict[f'e_d_4_{check_columns_document_4.index(column) + 1:03d}'] = f'{column}が未入力です'
                # 「0」であれば、error_dictにf'{column}に不備があります'を追加
                elif str(row_data[column]).strip() == '0':
                    error_dict[f'e_d_4_{check_columns_document_4.index(column) + 1:03d}'] = f'{column}に不備があります'
                # 「1」であれば、error_dictに追加しない
                elif str(row_data[column]).strip() == '1':
                    pass
                # それ以外の値の場合、error_dictにf'{column}の値が不正です'を追加
                else:
                    error_dict[f'e_d_4_{check_columns_document_4.index(column) + 1:03d}'] = f'{column}の値が不正です'
            # カラムが存在しない場合、error_dictにf'{column}のカラムが見つかりません'を追加
            else:
                error_dict[f'e_d_4_{check_columns_document_4.index(column) + 1:03d}'] = f'{column}のカラムが見つかりません'
        
        # チェック担当者のカラムを別途チェック
        if person_in_charge_column_document_4 in row_data.index:
            value = row_data[person_in_charge_column_document_4]
            # 値がNaNまたは空文字列の場合は何もしない
            if not (pd.isna(value) or str(value).strip() == ''):
                value_str = str(value).strip()
                # 数字のみの場合は「不正です」エラーを返す
                if value_str.isdigit():
                    error_dict['e_d_4_003'] = '書類4のチェック担当者欄に数字が入力されています。文字列を入力してください。'
                # 文字列が入っている場合はerror_dictに担当者名を追加
                else:
                    error_dict['書類4_チェック担当者'] = value_str
        else:
            error_dict[f'e_d_4_{len(check_columns_document_4) + 1:03d}'] = f'{person_in_charge_column_document_4}のカラムが見つかりません'
            
    except Exception as e:
        logging.error(f"書類4のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_4_002'] = f'書類4のチェック状況の反映中にエラーが発生しました: {str(e)}'  
    return error_dict

def check_document_5_budget(row):
    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()
    logging.info("フォルダを作成しました")

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
        
        # 書類5（予算）のチェック項目
        check_columns_document_5_budget = [
            'チェック項目_予算'
        ]
        # 書類5（予算）のチェック担当者のカラム
        person_in_charge_column_document_5_budget = 'チェック者名_予算'
        
        # まず通常のチェック項目をチェック
        for column in check_columns_document_5_budget:
            if column in row_data.index:
                # カラムが存在する場合、値のチェック
                # 値がNaNまたは空文字列の場合、error_dictにf'{column}が未入力です'を追加
                if pd.isna(row_data[column]) or str(row_data[column]).strip() == '':
                    error_dict[f'e_d_5_b_{check_columns_document_5_budget.index(column) + 1:03d}'] = f'{column}が未入力です'
                # 「0」であれば、error_dictにf'{column}に不備があります'を追加
                elif str(row_data[column]).strip() == '0':
                    error_dict[f'e_d_5_b_{check_columns_document_5_budget.index(column) + 1:03d}'] = f'{column}に不備があります'
                # 「1」であれば、error_dictに追加しない
                elif str(row_data[column]).strip() == '1':
                    pass
                # それ以外の値の場合、error_dictにf'{column}の値が不正です'を追加
                else:
                    error_dict[f'e_d_5_b_{check_columns_document_5_budget.index(column) + 1:03d}'] = f'{column}の値が不正です'
            # カラムが存在しない場合、error_dictにf'{column}のカラムが見つかりません'を追加
            else:
                error_dict[f'e_d_5_b_{check_columns_document_5_budget.index(column) + 1:03d}'] = f'{column}のカラムが見つかりません'
        
        # チェック担当者のカラムを別途チェック
        if person_in_charge_column_document_5_budget in row_data.index:
            value = row_data[person_in_charge_column_document_5_budget]
            # 値がNaNまたは空文字列の場合は何もしない
            if not (pd.isna(value) or str(value).strip() == ''):
                value_str = str(value).strip()
                # 数字のみの場合は「不正です」エラーを返す
                if value_str.isdigit():
                    error_dict['e_d_5_b_003'] = '書類5（予算）のチェック担当者欄に数字が入力されています。文字列を入力してください。'
                # 文字列が入っている場合はerror_dictに担当者名を追加
                else:
                    error_dict['書類5_予算_チェック担当者'] = value_str
        else:
            error_dict[f'e_d_5_b_{len(check_columns_document_5_budget) + 1:03d}'] = f'{person_in_charge_column_document_5_budget}のカラムが見つかりません'
            
    except Exception as e:
        logging.error(f"書類5（予算）のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_5_b_002'] = f'書類5（予算）のチェック状況の反映中にエラーが発生しました: {str(e)}'  
    return error_dict

def check_document_5_plan(row):
    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()
    logging.info("フォルダを作成しました")

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
        
        # 書類5（計画）のチェック項目
        check_columns_document_5_plan = [
            'チェック項目_計画'
        ]
        # 書類5（計画）のチェック担当者のカラム
        person_in_charge_column_document_5_plan = 'チェック者名_計画'
        
        # まず通常のチェック項目をチェック
        for column in check_columns_document_5_plan:
            if column in row_data.index:
                # カラムが存在する場合、値のチェック
                # 値がNaNまたは空文字列の場合、error_dictにf'{column}が未入力です'を追加
                if pd.isna(row_data[column]) or str(row_data[column]).strip() == '':
                    error_dict[f'e_d_5_p_{check_columns_document_5_plan.index(column) + 1:03d}'] = f'{column}が未入力です'
                # 「0」であれば、error_dictにf'{column}に不備があります'を追加
                elif str(row_data[column]).strip() == '0':
                    error_dict[f'e_d_5_p_{check_columns_document_5_plan.index(column) + 1:03d}'] = f'{column}に不備があります'
                # 「1」であれば、error_dictに追加しない
                elif str(row_data[column]).strip() == '1':
                    pass
                # それ以外の値の場合、error_dictにf'{column}の値が不正です'を追加
                else:
                    error_dict[f'e_d_5_p_{check_columns_document_5_plan.index(column) + 1:03d}'] = f'{column}の値が不正です'
            # カラムが存在しない場合、error_dictにf'{column}のカラムが見つかりません'を追加
            else:
                error_dict[f'e_d_5_p_{check_columns_document_5_plan.index(column) + 1:03d}'] = f'{column}のカラムが見つかりません'
        
        # チェック担当者のカラムを別途チェック
        if person_in_charge_column_document_5_plan in row_data.index:
            value = row_data[person_in_charge_column_document_5_plan]
            # 値がNaNまたは空文字列の場合は何もしない
            if not (pd.isna(value) or str(value).strip() == ''):
                value_str = str(value).strip()
                # 数字のみの場合は「不正です」エラーを返す
                if value_str.isdigit():
                    error_dict['e_d_5_p_003'] = '書類5（計画）のチェック担当者欄に数字が入力されています。文字列を入力してください。'
                # 文字列が入っている場合はerror_dictに担当者名を追加
                else:
                    error_dict['書類5_計画_チェック担当者'] = value_str
        else:
            error_dict[f'e_d_5_p_{len(check_columns_document_5_plan) + 1:03d}'] = f'{person_in_charge_column_document_5_plan}のカラムが見つかりません'
            
    except Exception as e:
        logging.error(f"書類5（計画）のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_5_p_002'] = f'書類5（計画）のチェック状況の反映中にエラーが発生しました: {str(e)}'  
    return error_dict

def check_document_6_financial_statements(row):
    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()
    logging.info("フォルダを作成しました")

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
        
        # 書類6（決算）のチェック項目
        check_columns_document_6_financial = [
            'チェック項目_決算'
        ]
        # 書類6（決算）のチェック担当者のカラム
        person_in_charge_column_document_6_financial = 'チェック者名_決算'
        
        # まず通常のチェック項目をチェック
        for column in check_columns_document_6_financial:
            if column in row_data.index:
                # カラムが存在する場合、値のチェック
                # 値がNaNまたは空文字列の場合、error_dictにf'{column}が未入力です'を追加
                if pd.isna(row_data[column]) or str(row_data[column]).strip() == '':
                    error_dict[f'e_d_6_f_{check_columns_document_6_financial.index(column) + 1:03d}'] = f'{column}が未入力です'
                # 「0」であれば、error_dictにf'{column}に不備があります'を追加
                elif str(row_data[column]).strip() == '0':
                    error_dict[f'e_d_6_f_{check_columns_document_6_financial.index(column) + 1:03d}'] = f'{column}に不備があります'
                # 「1」であれば、error_dictに追加しない
                elif str(row_data[column]).strip() == '1':
                    pass
                # それ以外の値の場合、error_dictにf'{column}の値が不正です'を追加
                else:
                    error_dict[f'e_d_6_f_{check_columns_document_6_financial.index(column) + 1:03d}'] = f'{column}の値が不正です'
            # カラムが存在しない場合、error_dictにf'{column}のカラムが見つかりません'を追加
            else:
                error_dict[f'e_d_6_f_{check_columns_document_6_financial.index(column) + 1:03d}'] = f'{column}のカラムが見つかりません'
        
        # チェック担当者のカラムを別途チェック
        if person_in_charge_column_document_6_financial in row_data.index:
            value = row_data[person_in_charge_column_document_6_financial]
            # 値がNaNまたは空文字列の場合は何もしない
            if not (pd.isna(value) or str(value).strip() == ''):
                value_str = str(value).strip()
                # 数字のみの場合は「不正です」エラーを返す
                if value_str.isdigit():
                    error_dict['e_d_6_f_003'] = '書類6（決算）のチェック担当者欄に数字が入力されています。文字列を入力してください。'
                # 文字列が入っている場合はerror_dictに担当者名を追加
                else:
                    error_dict['書類6_決算_チェック担当者'] = value_str
        else:
            error_dict[f'e_d_6_f_{len(check_columns_document_6_financial) + 1:03d}'] = f'{person_in_charge_column_document_6_financial}のカラムが見つかりません'
            
    except Exception as e:
        logging.error(f"書類6（決算）のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_6_f_002'] = f'書類6（決算）のチェック状況の反映中にエラーが発生しました: {str(e)}'  
    return error_dict

def check_document_6_report(row):
    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()
    logging.info("フォルダを作成しました")

    error_dict = {}
    
    try:
        # DataFrameの場合は最初の行を取得
        if isinstance(row, pd.DataFrame):
            if row.empty:
                error_dict['e_d_6_r_001'] = '書類6（報告）のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row
        
        # 書類6（報告）のチェック項目
        check_columns_document_6_report = [
            'チェック項目_報告'
        ]
        # 書類6（報告）のチェック担当者のカラム
        person_in_charge_column_document_6_report = 'チェック者名_報告'
        
        # まず通常のチェック項目をチェック
        for column in check_columns_document_6_report:
            if column in row_data.index:
                # カラムが存在する場合、値のチェック
                # 値がNaNまたは空文字列の場合、error_dictにf'{column}が未入力です'を追加
                if pd.isna(row_data[column]) or str(row_data[column]).strip() == '':
                    error_dict[f'e_d_6_r_{check_columns_document_6_report.index(column) + 1:03d}'] = f'{column}が未入力です'
                # 「0」であれば、error_dictにf'{column}に不備があります'を追加
                elif str(row_data[column]).strip() == '0':
                    error_dict[f'e_d_6_r_{check_columns_document_6_report.index(column) + 1:03d}'] = f'{column}に不備があります'
                # 「1」であれば、error_dictに追加しない
                elif str(row_data[column]).strip() == '1':
                    pass
                # それ以外の値の場合、error_dictにf'{column}の値が不正です'を追加
                else:
                    error_dict[f'e_d_6_r_{check_columns_document_6_report.index(column) + 1:03d}'] = f'{column}の値が不正です'
            # カラムが存在しない場合、error_dictにf'{column}のカラムが見つかりません'を追加
            else:
                error_dict[f'e_d_6_r_{check_columns_document_6_report.index(column) + 1:03d}'] = f'{column}のカラムが見つかりません'
        
        # チェック担当者のカラムを別途チェック
        if person_in_charge_column_document_6_report in row_data.index:
            value = row_data[person_in_charge_column_document_6_report]
            # 値がNaNまたは空文字列の場合は何もしない
            if not (pd.isna(value) or str(value).strip() == ''):
                value_str = str(value).strip()
                # 数字のみの場合は「不正です」エラーを返す
                if value_str.isdigit():
                    error_dict['e_d_6_r_003'] = '書類6（報告）のチェック担当者欄に数字が入力されています。文字列を入力してください。'
                # 文字列が入っている場合はerror_dictに担当者名を追加
                else:
                    error_dict['書類6_報告_チェック担当者'] = value_str
        else:
            error_dict[f'e_d_6_r_{len(check_columns_document_6_report) + 1:03d}'] = f'{person_in_charge_column_document_6_report}のカラムが見つかりません'
            
    except Exception as e:
        logging.error(f"書類6（報告）のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_6_r_002'] = f'書類6（報告）のチェック状況の反映中にエラーが発生しました: {str(e)}'  
    return error_dict

def check_document_7(row):
    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()
    logging.info("フォルダを作成しました")

    error_dict = {}
    
    try:
        # DataFrameの場合は最初の行を取得
        if isinstance(row, pd.DataFrame):
            if row.empty:
                error_dict['e_d_7_001'] = '書類7のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row
        
        # 書類7のチェック項目
        check_columns_document_7 = [
            'チェック項目_自己点検・評価'
        ]
        # 書類7のチェック担当者のカラム
        person_in_charge_column_document_7 = 'チェック者名_自己点検・評価'
        
        # まず通常のチェック項目をチェック
        for column in check_columns_document_7:
            if column in row_data.index:
                # カラムが存在する場合、値のチェック
                # 値がNaNまたは空文字列の場合、error_dictにf'{column}が未入力です'を追加
                if pd.isna(row_data[column]) or str(row_data[column]).strip() == '':
                    error_dict[f'e_d_7_{check_columns_document_7.index(column) + 1:03d}'] = f'{column}が未入力です'
                # 「0」であれば、error_dictにf'{column}に不備があります'を追加
                elif str(row_data[column]).strip() == '0':
                    error_dict[f'e_d_7_{check_columns_document_7.index(column) + 1:03d}'] = f'{column}に不備があります'
                # 「1」であれば、error_dictに追加しない
                elif str(row_data[column]).strip() == '1':
                    pass
                # それ以外の値の場合、error_dictにf'{column}の値が不正です'を追加
                else:
                    error_dict[f'e_d_7_{check_columns_document_7.index(column) + 1:03d}'] = f'{column}の値が不正です'
            # カラムが存在しない場合、error_dictにf'{column}のカラムが見つかりません'を追加
            else:
                error_dict[f'e_d_7_{check_columns_document_7.index(column) + 1:03d}'] = f'{column}のカラムが見つかりません'
        
        # チェック担当者のカラムを別途チェック
        if person_in_charge_column_document_7 in row_data.index:
            value = row_data[person_in_charge_column_document_7]
            # 値がNaNまたは空文字列の場合は何もしない
            if not (pd.isna(value) or str(value).strip() == ''):
                value_str = str(value).strip()
                # 数字のみの場合は「不正です」エラーを返す
                if value_str.isdigit():
                    error_dict['e_d_7_003'] = '書類7のチェック担当者欄に数字が入力されています。文字列を入力してください。'
                # 文字列が入っている場合はerror_dictに担当者名を追加
                else:
                    error_dict['書類7_チェック担当者'] = value_str
        else:
            error_dict[f'e_d_7_{len(check_columns_document_7) + 1:03d}'] = f'{person_in_charge_column_document_7}のカラムが見つかりません'
            
    except Exception as e:
        logging.error(f"書類7のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_7_002'] = f'書類7のチェック状況の反映中にエラーが発生しました: {str(e)}'  
    return error_dict

def check_document_8(row):
    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()
    logging.info("フォルダを作成しました")

    error_dict = {}
    
    try:
        # DataFrameの場合は最初の行を取得
        if isinstance(row, pd.DataFrame):
            if row.empty:
                error_dict['e_d_8_001'] = '書類8のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row
        
        # 書類8のチェック項目
        check_columns_document_8 = [
            'チェック項目_議事録'
        ]
        # 書類8のチェック担当者のカラム
        person_in_charge_column_document_8 = 'チェック者名_議事録'
        
        # まず通常のチェック項目をチェック
        for column in check_columns_document_8:
            if column in row_data.index:
                # カラムが存在する場合、値のチェック
                # 値がNaNまたは空文字列の場合、error_dictにf'{column}が未入力です'を追加
                if pd.isna(row_data[column]) or str(row_data[column]).strip() == '':
                    error_dict[f'e_d_8_{check_columns_document_8.index(column) + 1:03d}'] = f'{column}が未入力です'
                # 「0」であれば、error_dictにf'{column}に不備があります'を追加
                elif str(row_data[column]).strip() == '0':
                    error_dict[f'e_d_8_{check_columns_document_8.index(column) + 1:03d}'] = f'{column}に不備があります'
                # 「1」であれば、error_dictに追加しない
                elif str(row_data[column]).strip() == '1':
                    pass
                # それ以外の値の場合、error_dictにf'{column}の値が不正です'を追加
                else:
                    error_dict[f'e_d_8_{check_columns_document_8.index(column) + 1:03d}'] = f'{column}の値が不正です'
            # カラムが存在しない場合、error_dictにf'{column}のカラムが見つかりません'を追加
            else:
                error_dict[f'e_d_8_{check_columns_document_8.index(column) + 1:03d}'] = f'{column}のカラムが見つかりません'
        
        # チェック担当者のカラムを別途チェック
        if person_in_charge_column_document_8 in row_data.index:
            value = row_data[person_in_charge_column_document_8]
            # 値がNaNまたは空文字列の場合は何もしない
            if not (pd.isna(value) or str(value).strip() == ''):
                value_str = str(value).strip()
                # 数字のみの場合は「不正です」エラーを返す
                if value_str.isdigit():
                    error_dict['e_d_8_003'] = '書類8のチェック担当者欄に数字が入力されています。文字列を入力してください。'
                # 文字列が入っている場合はerror_dictに担当者名を追加
                else:
                    error_dict['書類8_チェック担当者'] = value_str
        else:
            error_dict[f'e_d_8_{len(check_columns_document_8) + 1:03d}'] = f'{person_in_charge_column_document_8}のカラムが見つかりません'
            
    except Exception as e:
        logging.error(f"書類8のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_8_002'] = f'書類8のチェック状況の反映中にエラーが発生しました: {str(e)}'  
    return error_dict

def check_document_9(row):
    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()
    logging.info("フォルダを作成しました")

    error_dict = {}
    
    try:
        # DataFrameの場合は最初の行を取得
        if isinstance(row, pd.DataFrame):
            if row.empty:
                error_dict['e_d_9_001'] = '書類9のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row
        
        # 書類9のチェック項目
        check_columns_document_9 = [
            'チェック項目_自己説明'
        ]
        # 書類9のチェック担当者のカラム
        person_in_charge_column_document_9 = 'チェック者名_自己説明'
        
        # まず通常のチェック項目をチェック
        for column in check_columns_document_9:
            if column in row_data.index:
                # カラムが存在する場合、値のチェック
                # 値がNaNまたは空文字列の場合、error_dictにf'{column}が未入力です'を追加
                if pd.isna(row_data[column]) or str(row_data[column]).strip() == '':
                    error_dict[f'e_d_9_{check_columns_document_9.index(column) + 1:03d}'] = f'{column}が未入力です'
                # 「0」であれば、error_dictにf'{column}に不備があります'を追加
                elif str(row_data[column]).strip() == '0':
                    error_dict[f'e_d_9_{check_columns_document_9.index(column) + 1:03d}'] = f'{column}に不備があります'
                # 「1」であれば、error_dictに追加しない
                elif str(row_data[column]).strip() == '1':
                    pass
                # それ以外の値の場合、error_dictにf'{column}の値が不正です'を追加
                else:
                    error_dict[f'e_d_9_{check_columns_document_9.index(column) + 1:03d}'] = f'{column}の値が不正です'
            # カラムが存在しない場合、error_dictにf'{column}のカラムが見つかりません'を追加
            else:
                error_dict[f'e_d_9_{check_columns_document_9.index(column) + 1:03d}'] = f'{column}のカラムが見つかりません'
        
        # チェック担当者のカラムを別途チェック
        if person_in_charge_column_document_9 in row_data.index:
            value = row_data[person_in_charge_column_document_9]
            # 値がNaNまたは空文字列の場合は何もしない
            if not (pd.isna(value) or str(value).strip() == ''):
                value_str = str(value).strip()
                # 数字のみの場合は「不正です」エラーを返す
                if value_str.isdigit():
                    error_dict['e_d_9_003'] = '書類9のチェック担当者欄に数字が入力されています。文字列を入力してください。'
                # 文字列が入っている場合はerror_dictに担当者名を追加
                else:
                    error_dict['書類9_チェック担当者'] = value_str
        else:
            error_dict[f'e_d_9_{len(check_columns_document_9) + 1:03d}'] = f'{person_in_charge_column_document_9}のカラムが見つかりません'
            
    except Exception as e:
        logging.error(f"書類9のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_9_002'] = f'書類9のチェック状況の反映中にエラーが発生しました: {str(e)}'  
    return error_dict

def check_document_10(row):
    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()
    logging.info("フォルダを作成しました")

    error_dict = {}
    
    try:
        # DataFrameの場合は最初の行を取得
        if isinstance(row, pd.DataFrame):
            if row.empty:
                error_dict['e_d_10_001'] = '書類10のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row
        
        # 書類10のチェック項目
        check_columns_document_10 = [
            'チェック項目_届出'
        ]
        # 書類10のチェック担当者のカラム
        person_in_charge_column_document_10 = 'チェック者名_届出'
        
        # まず通常のチェック項目をチェック
        for column in check_columns_document_10:
            if column in row_data.index:
                # カラムが存在する場合、値のチェック
                # 値がNaNまたは空文字列の場合、error_dictにf'{column}が未入力です'を追加
                if pd.isna(row_data[column]) or str(row_data[column]).strip() == '':
                    error_dict[f'e_d_10_{check_columns_document_10.index(column) + 1:03d}'] = f'{column}が未入力です'
                # 「0」であれば、error_dictにf'{column}に不備があります'を追加
                elif str(row_data[column]).strip() == '0':
                    error_dict[f'e_d_10_{check_columns_document_10.index(column) + 1:03d}'] = f'{column}に不備があります'
                # 「1」であれば、error_dictに追加しない
                elif str(row_data[column]).strip() == '1':
                    pass
                # それ以外の値の場合、error_dictにf'{column}の値が不正です'を追加
                else:
                    error_dict[f'e_d_10_{check_columns_document_10.index(column) + 1:03d}'] = f'{column}の値が不正です'
            # カラムが存在しない場合、error_dictにf'{column}のカラムが見つかりません'を追加
            else:
                error_dict[f'e_d_10_{check_columns_document_10.index(column) + 1:03d}'] = f'{column}のカラムが見つかりません'
        
        # チェック担当者のカラムを別途チェック
        if person_in_charge_column_document_10 in row_data.index:
            value = row_data[person_in_charge_column_document_10]
            # 値がNaNまたは空文字列の場合は何もしない
            if not (pd.isna(value) or str(value).strip() == ''):
                value_str = str(value).strip()
                # 数字のみの場合は「不正です」エラーを返す
                if value_str.isdigit():
                    error_dict['e_d_10_003'] = '書類10のチェック担当者欄に数字が入力されています。文字列を入力してください。'
                # 文字列が入っている場合はerror_dictに担当者名を追加
                else:
                    error_dict['書類10_チェック担当者'] = value_str
        else:
            error_dict[f'e_d_10_{len(check_columns_document_10) + 1:03d}'] = f'{person_in_charge_column_document_10}のカラムが見つかりません'
            
    except Exception as e:
        logging.error(f"書類10のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_10_002'] = f'書類10のチェック状況の反映中にエラーが発生しました: {str(e)}'  
    return error_dict


