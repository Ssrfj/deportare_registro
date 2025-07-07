def update_document_check_status(overall_checklist_df, checklist_file_path, club_reception_df, latest_reception_data_date):
    import os
    import pandas as pd
    import logging
    from datetime import datetime, timezone, timedelta
    from src.folder_management.make_folders import setup_logging, create_folders
    from src.core.setting_paths import overall_checklist_folder_path
    from src.core.utils import get_jst_now, ensure_date_string
    from src.checklist.automation.documents_check_functions import (
        check_document_1, check_document_2_1, check_document_2_2, check_document_3,
        check_document_4, check_document_5_plan, check_document_5_budget,
        check_document_6_report, check_document_6_financial_statements,
        check_document_7, check_document_8, check_document_9, check_document_10
    )
    
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
            # カラムが存在しない場合は、現在時刻を使用
            checklist_creation_time = get_jst_now()
        else:
            checklist_creation_time_str = str(row.get('チェックリスト作成日時')).strip()
            if checklist_creation_time_str and checklist_creation_time_str != 'nan':
                try:
                    checklist_creation_time = pd.to_datetime(checklist_creation_time_str)
                except:
                    checklist_creation_time = get_jst_now()
            else:
                checklist_creation_time = get_jst_now()
        # 処理開始のメッセージを表示
        logging.info(f"クラブ名: {club_name} の自動チェックを開始します")
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
        mask = (checklist_df['申請時間'] == apried_date_str) & (checklist_df['自動チェック更新時間'].notna()) & (checklist_df['自動チェック更新時間'] != '')
        if mask.any():
            logging.info(f"クラブ '{club_name}' の申請日時'{apried_date_str}'の申請は自動チェック済みです。スキップします。")
            continue
        else:
            logging.info(f"クラブ '{club_name}' の申請日時'{apried_date_str}'の申請は自動チェックを実行します。")
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
        error_dict.update(check_document_1(target_row))
        error_dict.update(check_document_2_1(target_row))
        error_dict.update(check_document_2_2(target_row))
        error_dict.update(check_document_3(target_row))
        error_dict.update(check_document_4(target_row))
        error_dict.update(check_document_5_plan(target_row))
        error_dict.update(check_document_5_budget(target_row))
        error_dict.update(check_document_6_report(target_row))
        error_dict.update(check_document_6_financial_statements(target_row))
        error_dict.update(check_document_7(target_row))
        error_dict.update(check_document_8(target_row))
        error_dict.update(check_document_9(target_row))
        error_dict.update(check_document_10(target_row))

        # チェック結果をチェックリストに反映
        for key, value in error_dict.items():
            if key in checklist_df.columns:
                checklist_df.at[index, key] = value
            else:
                logging.warning(f"チェックリストに '{key}' カラムが存在しません。スキップします。")
        # チェックリストの更新日時を設定
        checklist_df.at[index, '自動チェック更新時間'] = jst_now.strftime('%Y-%m-%d %H:%M:%S')

        # チェックリストを保存
        try:
            checklist_df.to_excel(checklist_file_path, index=False)
            logging.info(f"チェックリスト '{checklist_file_name}' を更新しました。")
        except Exception as e:
            logging.error(f"チェックリスト '{checklist_file_name}' の保存中にエラーが発生しました: {e}")
            continue
    # チェックリストの更新が完了したことをログに記録
    logging.info("書類チェック状況の更新が完了しました")

    # 総合チェックリストのファイルを保存（ファイル名は「総合チェックリスト_受付{YYYYMMDDHHMMSS}_更新{YYYYMMDDHHMMSS}.xlsx」）
    logging.info("総合チェックリストのファイルを保存します")
    now_jst = get_jst_now()
    latest_reception_data_date_str = ensure_date_string(latest_reception_data_date)
    overall_checklist_file_name = f'総合チェックリスト_受付{latest_reception_data_date_str}_更新{now_jst.strftime("%Y%m%d%H%M%S")}.xlsx'
    overall_checklist_file_path = os.path.join(overall_checklist_folder_path, overall_checklist_file_name)
    overall_checklist_df.to_excel(overall_checklist_file_path, index=False)
    logging.info(f"総合チェックリストのファイルを保存しました: {overall_checklist_file_path}")
    logging.info("自動チェックが完了しました")
    return overall_checklist_df, checklist_file_path