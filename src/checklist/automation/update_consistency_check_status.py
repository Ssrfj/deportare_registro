import pandas as pd
import logging
from datetime import datetime, date
from src.core.setting_paths import content_check_folder_path, application_statues_folder_path
from src.folder_management.make_folders import setup_logging, create_folders

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
    from src.core.utils import get_jst_now
    
    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()
    logging.info("フォルダを作成しました")

    # チェックリストのフォルダを指定
    folder_path = os.path.join('R7_登録申請処理', '申請入力内容')

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
            logging.error(f"'チェックリスト作成日時' カラムが存在しません。rowのカラム: {row.index.tolist()}")
            continue
        # 処理開始のメッセージを表示
        logging.info(f"クラブ名: {club_name} の一貫性自動チェックを開始します")
        # 保存されているチェックリストを読み込み、チェックを実行
        club_folder_path = os.path.join(folder_path, club_name)
        if not os.path.exists(club_folder_path):
            os.makedirs(club_folder_path, exist_ok=True)
            logging.info(f"クラブ '{club_name}' のフォルダを新規作成しました。")
            continue
        checklist_file_name = f"{club_name}_申請{apried_date_str}.xlsx"
        each_folder_path = os.path.join(folder_path, club_name)
        checklist_file_path = os.path.join(each_folder_path, checklist_file_name)
        # パスの正規化を追加
        checklist_file_path = os.path.normpath(checklist_file_path)
        logging.info(f"debug; checklist_file_path: {checklist_file_path}")
        if not checklist_file_path or not os.path.exists(checklist_file_path):
            # デバッグ用にeach_folder_pathにあるファイルをリストアップ
            logging.info(f"debug; each_folder_path: {each_folder_path}")
            logging.info(f"debug; each_folder_pathにあるファイル: {os.listdir(each_folder_path)}")
            # チェックリストファイルが存在しない場合の処理
            logging.warning(f"クラブ '{club_name}' のチェックリストファイルが存在しません。スキップします。")
            continue

        try:
            checklist_df = pd.read_excel(checklist_file_path)
            # チェックリストのカラム名を確認
            logging.info(f"チェックリストファイル '{checklist_file_name}' を読み込みました。")
        except Exception as e:
            logging.error(f"チェックリストファイル '{checklist_file_name}' の読み込み中にエラーが発生しました: {e}")
            continue
        # チェックリストの自動チェックを実行する必要があるかを確認
        mask = (checklist_df['申請時間'] == apried_date_str) & (checklist_df['一貫性自動チェック更新時間'].notna()) & (checklist_df['一貫性自動チェック更新時間'] != '')
        if mask.any():
            logging.info(f"クラブ '{club_name}' の申請日時'{apried_date_str}'の申請は一貫性自動チェック済みです。スキップします。")
            continue
        else:
            logging.info(f"クラブ '{club_name}' の申請日時'{apried_date_str}'の申請は一貫性自動チェックを実行します。")
            error_dict = {}
            jst_now = datetime.now(timezone(timedelta(hours=9)))
            today_date = jst_now.date()
        
        overall_checklist_df['クラブ名'] = overall_checklist_df['クラブ名'].astype(str).str.strip()
        overall_checklist_df['受付日時'] = overall_checklist_df['受付日時'].astype(str).str.strip()
        # overall_checklist_dfのクラブ名と受付日時をstr型に変換
        # 申請内容から該当行を抽出
        target_row = club_reception_df[
            (club_reception_df['クラブ名'] == club_name) &
            (club_reception_df['受付_タイムスタンプ'] == apried_date_str)
        ]
        logging.debug(club_reception_df[['クラブ名', '受付_タイムスタンプ']])
        logging.debug(f"検索値: クラブ名={club_name}, 受付日時={apried_date_str}")
        logging.debug(f"{repr(club_name)}, {repr(apried_date_str)}")
        logging.debug(club_reception_df[['クラブ名', '受付_タイムスタンプ']].applymap(repr))
        if target_row.empty:
            logging.warning(f"申請内容に該当データがありません: {club_name}, {apried_date_str}")
            continue
        # 各チェック関数に row を渡す
        error_dict.update(check_consistency_disciplines(target_row))
        error_dict.update(check_consistency_members_and_voting_rights(target_row))
        error_dict.update(check_consistency_meeting_minutes(target_row))

        # チェック結果をチェックリストに反映
        for key, value in error_dict.items():
            if key in checklist_df.columns:
                checklist_df.at[index, key] = value
            else:
                logging.warning(f"チェックリストに '{key}' カラムが存在しません。スキップします。")
        # チェックリストの更新日時を設定
        checklist_df.at[index, '一貫性自動チェック更新時間'] = jst_now.strftime('%Y-%m-%d %H:%M:%S')

        # チェックリストを保存
        try:
            checklist_df.to_excel(checklist_file_path, index=False)
            logging.info(f"チェックリスト '{checklist_file_name}' を更新しました。")
        except Exception as e:
            logging.error(f"チェックリスト '{checklist_file_name}' の保存中にエラーが発生しました: {e}")
            continue
    # チェックリストの更新が完了したことをログに記録
    logging.info("一貫性チェック状況の更新が完了しました")

    # 総合チェックリストのファイルを保存（ファイル名は「総合チェックリスト_受付{YYYYMMDDHHMMSS}_更新{YYYYMMDDHHMMSS}.xlsx」）
    logging.info("総合チェックリストのファイルを保存します")
    now_jst = get_jst_now()
    overall_checklist_file_name = f'総合チェックリスト_受付{latest_reception_data_date}_更新{now_jst.strftime("%Y%m%d%H%M%S")}.xlsx'
    overall_checklist_file_path = os.path.join(overall_checklist_folder_path, overall_checklist_file_name)
    overall_checklist_df.to_excel(overall_checklist_file_path, index=False)
    logging.info(f"総合チェックリストのファイルを保存しました: {overall_checklist_file_path}")
    logging.info("一貫性自動チェックが完了しました")
    return overall_checklist_df, checklist_file_path