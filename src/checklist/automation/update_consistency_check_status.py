import pandas as pd
import logging
from datetime import datetime, date
from src.core.setting_paths import content_check_folder_path, application_statues_folder_path, application_input_content_folder_path, clubs_details_data_folder_path
from src.folder_management.make_folders import setup_logging, create_folders
from src.core.utils import ensure_date_string

def check_consistency_disciplines(row):
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
                error_dict['e_c_d_001'] = '活動種目一貫性のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row
        
        # 活動種目一貫性のチェック項目
        check_columns_consistency_disciplines = [
            'チェック項目_活動種目'
        ]
        # 活動種目一貫性のチェック担当者のカラム
        person_in_charge_column_consistency_disciplines = 'チェック者名_一貫性_活動種目'
        
        # まず通常のチェック項目をチェック
        for column in check_columns_consistency_disciplines:
            if column in row_data.index:
                # カラムが存在する場合、値のチェック
                # 値がNaNまたは空文字列の場合、error_dictにf'{column}が未入力です'を追加
                if pd.isna(row_data[column]) or str(row_data[column]).strip() == '':
                    error_dict[f'e_c_d_{check_columns_consistency_disciplines.index(column) + 1:03d}'] = f'{column}が未入力です'
                # 「0」であれば、error_dictにf'{column}に不備があります'を追加
                elif str(row_data[column]).strip() == '0':
                    error_dict[f'e_c_d_{check_columns_consistency_disciplines.index(column) + 1:03d}'] = f'{column}に不備があります'
                # 「1」であれば、error_dictに追加しない
                elif str(row_data[column]).strip() == '1':
                    pass
                # それ以外の値の場合、error_dictにf'{column}の値が不正です'を追加
                else:
                    error_dict[f'e_c_d_{check_columns_consistency_disciplines.index(column) + 1:03d}'] = f'{column}の値が不正です'
            # カラムが存在しない場合、error_dictにf'{column}のカラムが見つかりません'を追加
            else:
                error_dict[f'e_c_d_{check_columns_consistency_disciplines.index(column) + 1:03d}'] = f'{column}のカラムが見つかりません'
        
        # チェック担当者のカラムを別途チェック
        if person_in_charge_column_consistency_disciplines in row_data.index:
            value = row_data[person_in_charge_column_consistency_disciplines]
            # 値がNaNまたは空文字列の場合は何もしない
            if not (pd.isna(value) or str(value).strip() == ''):
                value_str = str(value).strip()
                # 数字のみの場合は「不正です」エラーを返す
                if value_str.isdigit():
                    error_dict['e_c_d_003'] = '活動種目一貫性のチェック担当者欄に数字が入力されています。文字列を入力してください。'
                # 文字列が入っている場合はerror_dictに担当者名を追加
                else:
                    error_dict['活動種目一貫性_チェック担当者'] = value_str
        else:
            error_dict[f'e_c_d_{len(check_columns_consistency_disciplines) + 1:03d}'] = f'{person_in_charge_column_consistency_disciplines}のカラムが見つかりません'
            
    except Exception as e:
        logging.error(f"活動種目一貫性のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_c_d_002'] = f'活動種目一貫性のチェック状況の反映中にエラーが発生しました: {str(e)}'  
    return error_dict

def check_consistency_members_and_voting_rights(row):
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
                error_dict['e_c_m_001'] = '会員と議決権保有者一貫性のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row
        
        # 会員と議決権保有者一貫性のチェック項目
        check_columns_consistency_members = [
            'チェック項目_会員',
            'チェック項目_議決権保有者'
        ]
        # 会員と議決権保有者一貫性のチェック担当者のカラム
        person_in_charge_column_consistency_members = 'チェック者名_一貫性_会員と議決権保有者'
        
        # まず通常のチェック項目をチェック
        for column in check_columns_consistency_members:
            if column in row_data.index:
                # カラムが存在する場合、値のチェック
                # 値がNaNまたは空文字列の場合、error_dictにf'{column}が未入力です'を追加
                if pd.isna(row_data[column]) or str(row_data[column]).strip() == '':
                    error_dict[f'e_c_m_{check_columns_consistency_members.index(column) + 1:03d}'] = f'{column}が未入力です'
                # 「0」であれば、error_dictにf'{column}に不備があります'を追加
                elif str(row_data[column]).strip() == '0':
                    error_dict[f'e_c_m_{check_columns_consistency_members.index(column) + 1:03d}'] = f'{column}に不備があります'
                # 「1」であれば、error_dictに追加しない
                elif str(row_data[column]).strip() == '1':
                    pass
                # それ以外の値の場合、error_dictにf'{column}の値が不正です'を追加
                else:
                    error_dict[f'e_c_m_{check_columns_consistency_members.index(column) + 1:03d}'] = f'{column}の値が不正です'
            # カラムが存在しない場合、error_dictにf'{column}のカラムが見つかりません'を追加
            else:
                error_dict[f'e_c_m_{check_columns_consistency_members.index(column) + 1:03d}'] = f'{column}のカラムが見つかりません'
        
        # チェック担当者のカラムを別途チェック
        if person_in_charge_column_consistency_members in row_data.index:
            value = row_data[person_in_charge_column_consistency_members]
            # 値がNaNまたは空文字列の場合は何もしない
            if not (pd.isna(value) or str(value).strip() == ''):
                value_str = str(value).strip()
                # 数字のみの場合は「不正です」エラーを返す
                if value_str.isdigit():
                    error_dict['e_c_m_003'] = '会員と議決権保有者一貫性のチェック担当者欄に数字が入力されています。文字列を入力してください。'
                # 文字列が入っている場合はerror_dictに担当者名を追加
                else:
                    error_dict['会員と議決権保有者一貫性_チェック担当者'] = value_str
        else:
            error_dict[f'e_c_m_{len(check_columns_consistency_members) + 1:03d}'] = f'{person_in_charge_column_consistency_members}のカラムが見つかりません'
            
    except Exception as e:
        logging.error(f"会員と議決権保有者一貫性のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_c_m_002'] = f'会員と議決権保有者一貫性のチェック状況の反映中にエラーが発生しました: {str(e)}'  
    return error_dict

def check_consistency_meeting_minutes(row):
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
                error_dict['e_c_mt_001'] = '議事録一貫性のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row
        
        # 議事録一貫性のチェック項目
        check_columns_consistency_meeting = [
            'チェック項目_一貫性_議決権'
        ]
        # 議事録一貫性のチェック担当者のカラム
        person_in_charge_column_consistency_meeting = 'チェック者名_一貫性_議決権'
        
        # まず通常のチェック項目をチェック
        for column in check_columns_consistency_meeting:
            if column in row_data.index:
                # カラムが存在する場合、値のチェック
                # 値がNaNまたは空文字列の場合、error_dictにf'{column}が未入力です'を追加
                if pd.isna(row_data[column]) or str(row_data[column]).strip() == '':
                    error_dict[f'e_c_mt_{check_columns_consistency_meeting.index(column) + 1:03d}'] = f'{column}が未入力です'
                # 「0」であれば、error_dictにf'{column}に不備があります'を追加
                elif str(row_data[column]).strip() == '0':
                    error_dict[f'e_c_mt_{check_columns_consistency_meeting.index(column) + 1:03d}'] = f'{column}に不備があります'
                # 「1」であれば、error_dictに追加しない
                elif str(row_data[column]).strip() == '1':
                    pass
                # それ以外の値の場合、error_dictにf'{column}の値が不正です'を追加
                else:
                    error_dict[f'e_c_mt_{check_columns_consistency_meeting.index(column) + 1:03d}'] = f'{column}の値が不正です'
            # カラムが存在しない場合、error_dictにf'{column}のカラムが見つかりません'を追加
            else:
                error_dict[f'e_c_mt_{check_columns_consistency_meeting.index(column) + 1:03d}'] = f'{column}のカラムが見つかりません'
        
        # チェック担当者のカラムを別途チェック
        if person_in_charge_column_consistency_meeting in row_data.index:
            value = row_data[person_in_charge_column_consistency_meeting]
            # 値がNaNまたは空文字列の場合は何もしない
            if not (pd.isna(value) or str(value).strip() == ''):
                value_str = str(value).strip()
                # 数字のみの場合は「不正です」エラーを返す
                if value_str.isdigit():
                    error_dict['e_c_mt_003'] = '議事録一貫性のチェック担当者欄に数字が入力されています。文字列を入力してください。'
                # 文字列が入っている場合はerror_dictに担当者名を追加
                else:
                    error_dict['議事録一貫性_チェック担当者'] = value_str
        else:
            error_dict[f'e_c_mt_{len(check_columns_consistency_meeting) + 1:03d}'] = f'{person_in_charge_column_consistency_meeting}のカラムが見つかりません'
            
    except Exception as e:
        logging.error(f"議事録一貫性のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_c_mt_002'] = f'議事録一貫性のチェック状況の反映中にエラーが発生しました: {str(e)}'  
    return error_dict

def update_consistency_check_status(overall_checklist_df, checklist_file_path, club_reception_df, latest_reception_data_date):
    import os
    import pandas as pd
    import logging
    from datetime import datetime, timezone, timedelta
    from src.folder_management.make_folders import setup_logging, create_folders
    from src.core.setting_paths import overall_checklist_folder_path
    from src.core.utils import get_jst_now, ensure_date_string
    from src.core.load_latest_club_data import load_latest_club_reception_data, get_club_data_by_name_and_date
    
    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()
    logging.info("フォルダを作成しました")

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
        
        # 一貫性チェックが既に実行済みかを確認（総合チェックリストで判断）
        consistency_columns = [
            '一貫性チェック_活動種目', '一貫性チェック_会議録', '一貫性チェック_会員情報と議決権'
        ]
        
        # いずれかの一貫性チェック列に日時が入っていればスキップ
        consistency_check_done = any(
            pd.notna(overall_checklist_df.loc[index, col + '_更新日時']) and 
            overall_checklist_df.loc[index, col + '_更新日時'] != ''
            for col in consistency_columns if col + '_更新日時' in overall_checklist_df.columns
        )
        
        if consistency_check_done:
            logging.info(f"クラブ '{club_name}' の申請日時'{apried_date_str}'の申請は一貫性チェック済みです。スキップします。")
            continue
        else:
            logging.info(f"クラブ '{club_name}' の申請日時'{apried_date_str}'の申請は一貫性チェックを実行します。")
        
        jst_now = datetime.now(timezone(timedelta(hours=9)))
        update_datetime = jst_now.strftime('%Y-%m-%d %H:%M:%S')
        
        # 各一貫性チェック関数を実行して結果を総合チェックリストに反映
        try:
            # 活動種目の一貫性チェック
            disciplines_result = check_consistency_disciplines(target_row)
            overall_checklist_df.loc[index, '一貫性チェック_活動種目'] = 'チェック済み' if not disciplines_result else 'エラーあり'
            overall_checklist_df.loc[index, '一貫性チェック_活動種目_更新日時'] = update_datetime
            
            # 会議録の一貫性チェック
            meeting_minutes_result = check_consistency_meeting_minutes(target_row)
            overall_checklist_df.loc[index, '一貫性チェック_会議録'] = 'チェック済み' if not meeting_minutes_result else 'エラーあり'
            overall_checklist_df.loc[index, '一貫性チェック_会議録_更新日時'] = update_datetime
            
            # 会員情報と議決権の一貫性チェック
            member_voting_result = check_consistency_members_and_voting_rights(target_row)
            overall_checklist_df.loc[index, '一貫性チェック_会員情報と議決権'] = 'チェック済み' if not member_voting_result else 'エラーあり'
            overall_checklist_df.loc[index, '一貫性チェック_会員情報と議決権_更新日時'] = update_datetime
            
            logging.info(f"クラブ名: {club_name} の一貫性チェックが完了しました")
            
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