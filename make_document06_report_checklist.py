def make_document06_report_checklist(latest_reception_data_date):
    import os
    import pandas as pd
    import logging
    from setting_paths import content_check_folder_path, document06_report_checklist_folder_path, clubs_reception_data_path
    from utils import get_jst_now
    from make_folders import setup_logging, create_folders

    # ロギングの設定
    setup_logging()
    logging.info("ロギングを設定しました")
    # フォルダの作成
    create_folders()
    logging.info("フォルダを作成しました")

    # 最新の受付データの日付をフォーマット
    if not latest_reception_data_date:
        logging.error("最新の受付データの日付が指定されていません")
        return
    latest_reception_data_date = pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S').strftime('%Y%m%d%H%M%S')

    # 1. 最新のクラブ情報付き受付データファイルを取得(クラブ情報付き受付データ_受付{latest_reception_data_date}_*.xlsxを使用)
    logging.info("最新のクラブ情報付き受付データファイルを取得します")
    # 最新のクラブ情報付き受付データと同じ日付のファイルを取得
    if not latest_reception_data_date:
        logging.error("最新の受付データの日付が指定されていません")
        return    
    latest_club_reception_files = [
        f for f in os.listdir(content_check_folder_path)
        if os.path.isfile(os.path.join(content_check_folder_path, f)) and
        f.startswith(f'クラブ情報付き受付データ_受付{latest_reception_data_date}') and f.endswith('.xlsx')
    ]
    latest_club_reception_files.sort(reverse=True)
    if not latest_club_reception_files:
        logging.error(f"クラブ情報付き受付データファイルが見つかりません: クラブ情報付き受付データ_受付{latest_reception_data_date}*.xlsx")
        return
    latest_club_reception_file = latest_club_reception_files[0]
    logging.info(f"最新のクラブ情報付き受付データファイル: {latest_club_reception_file}")
    club_reception_df = pd.read_excel(os.path.join(content_check_folder_path, latest_club_reception_file))
    logging.info(f"最新のクラブ情報付き受付データを読み込みました: {latest_club_reception_file}")

    # 2. 書類06_報告_のチェックリストを作成する必要があるか確認
    logging.info("書類06_報告_のチェックリストを作成する必要があるか確認します")
    # 書類06_報告_のチェックリストが既に存在するか確認
    existing_checklist_files = [
        f for f in os.listdir(document06_report_checklist_folder_path)
        if os.path.isfile(os.path.join(document06_report_checklist_folder_path, f)) and
        f.startswith('書類06_報告_チェックリスト_') and f.endswith('.xlsx')
    ]
    
    # 既存の書類06_報告_のチェックリストで同じ受付データのものがあるか確認
    existing_checklist_files.sort(reverse=True)
    for file in existing_checklist_files:
        # ファイル名から受付日時を抽出: 書類06_報告_チェックリスト_受付{YYYYMMDDHHMMSS}_作成{YYYYMMDDHHMMSS}.xlsx
        file_parts = file.replace('書類06_報告_チェックリスト_受付', '').replace('.xlsx', '').split('_作成')
        if len(file_parts) >= 1:
            file_reception_date_str = file_parts[0]
            try:
                file_reception_date = pd.to_datetime(file_reception_date_str, format='%Y%m%d%H%M%S')
                if file_reception_date == pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S'):
                    logging.info(f"同じ受付データの書類06_報告_チェックリストが既に存在します: {file}")
                    logging.info("新しいチェックリストを作成しません。")
                    return
                elif file_reception_date < pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S'):
                    logging.info(f"古い受付データの書類06_報告_チェックリストが存在します: {file}")
                    logging.info("新しい受付データ用のチェックリストを作成します。")
                    break
            except ValueError:
                logging.warning(f"ファイル名から受付日時を解析できませんでした: {file}")
                continue

    # 3. 書類06_報告_のチェックリストのカラム名を取得
    logging.info("書類06_報告_のチェックリストのカラム名を取得します")
    # jsonファイルを読み込む（document06_report_checklist_columns.jsonが必要）
    document06_report_checklist_columns_file_name = 'document06_report_checklist_columns.json'
    document06_report_checklist_columns_file_path = os.path.join(content_check_folder_path, document06_report_checklist_columns_file_name)
    if not os.path.exists(document06_report_checklist_columns_file_path):
        logging.error(f"書類06_報告のチェックリストのカラム名ファイルが見つかりません: {document06_report_checklist_columns_file_path}")
        return
    document06_report_checklist_columns = pd.read_json(document06_report_checklist_columns_file_path, orient='records')
    logging.info(f"書類06_報告のチェックリストのカラム名を読み込みました: {document06_report_checklist_columns_file_name}")

    # 4. 書類06_報告のチェックリストのデータフレームを作成
    logging.info("書類06_報告のチェックリストのデータフレームを作成します")
    document06_report_checklist_df = pd.DataFrame(columns=document06_report_checklist_columns['document06_report_checklist_columns'].tolist())
    logging.info("書類06_報告のチェックリストのデータフレームを作成しました")

    logging.info("競技種目のリストを読み込みます")
    discipline_df = pd.read_excel('list_of_disciplines.xlsx')  
    discipline = discipline_df['disciplines']
    logging.info("競技種目のリストを読み込みました")

    # 書類06_reportのチェックリストのデータフレームにクラブ情報を追加
    for index, row in club_reception_df.iterrows():
        club_name = row['クラブ名']
        document06_report_checklist_df.loc[index, '申請日時'] = row['申請_タイムスタンプ']
        document06_report_checklist_df.loc[index, 'クラブ名'] = club_name
        
        # 競技種目数の取得   
        # 種目のカラムを修正（'申請_種目_'を付記）
        disciplines_columns = [f'申請_種目_{discipline}' for discipline in discipline]
        extra_disciplines_column = row.get('申請_種目_その他_数(選択時必須)', 0)
        count_of_disciplines = 0
        # 各種目カラムをループし、「定期的に行っている」が選択されているかを確認
        for col in disciplines_columns:
            if col in row and row[col] == '定期的に行っている':
                count_of_disciplines += 1
        count_of_disciplines += extra_disciplines_column in row and row[extra_disciplines_column] != '' and row[extra_disciplines_column] != '0'
        # 競技種目数が0の場合は、'0'と記載
        if count_of_disciplines == 0:
            count_of_disciplines = '0'
        else:
            count_of_disciplines = str(count_of_disciplines)
        document06_report_checklist_df.loc[index, '申請_活動種目数'] = count_of_disciplines

        # 書類チェックの結果を記載するカラムを指定
        document06_report_check_result_columns = [
            '担当者入力_活動種目数',
            '担当者入力_種目実施チェック',
        ]
        # 書類チェックの結果の初期状態は「書類未チェック」
        for col in document06_report_check_result_columns:
            document06_report_checklist_df.loc[index, col] = '書類未チェック'
        # 受付日時のカラムはlatest_reception_data_dateを使用
        document06_report_checklist_df.loc[index, '受付日時'] = pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
        # チェックリスト作成日時のカラムは現在のJST日時を使用
        document06_report_checklist_df.loc[index, 'チェックリスト作成日時'] = pd.to_datetime(get_jst_now()).strftime('%Y-%m-%d %H:%M:%S')
        # チェック項目のカラムを指定
        check_columns = [
            'チェック項目_報告',
        ]
        # チェック項目の初期状態は「未チェック」
        for col in check_columns:
            document06_report_checklist_df.loc[index, col] = '未チェック'
        # チェック項目_その他の初期状態は空文字列
        document06_report_checklist_df.loc[index, 'チェック項目_その他'] = ''
        # チェック者名の初期状態は「チェックが完了していません」
        document06_report_checklist_df.loc[index, 'チェック者名_報告'] = 'チェックが完了していません'
    logging.info("書類06_報告のチェックリストのデータフレームを作成しました")

    # 5. 書類06_報告のチェックリストのデータフレームを保存(ファイル名は「書類06_報告チェックリスト_受付{latest_reception_data_date}_作成{YYYYMMDDHHMMSS}.xlsx」)
    logging.info("書類06_報告のチェックリストのデータフレームを保存します")
    now_jst = get_jst_now()
    document06_report_checklist_file_name = f'書類06_報告チェックリスト_受付{latest_reception_data_date}_作成{now_jst.strftime("%Y%m%d%H%M%S")}.xlsx'
    document06_report_checklist_file_path = os.path.join(document06_report_checklist_df, document06_report_checklist_file_name)
    document06_report_checklist_df.to_excel(document06_report_checklist_file_path, index=False)
    logging.info(f"書類06_報告のチェックリストのデータフレームを保存しました: {document06_report_checklist_file_path}")

    # 6. 書類06_報告のチェックリストのファイルを保存
    logging.info("書類06_報告のチェックリストのファイルを保存します")
    document06_report_checklist_df.to_excel(document06_report_checklist_file_path, index=False)
    logging.info(f"書類06_報告のチェックリストのファイルを保存しました: {document06_report_checklist_file_path}")