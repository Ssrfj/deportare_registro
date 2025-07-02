def make_document02_2_checklist(latest_reception_data_date):
    import os
    import pandas as pd
    import logging
    from src.core.setting_paths import content_check_folder_path, document02_2_checklist_folder_path, clubs_reception_data_path
    from src.core.utils import get_jst_now, get_config_file_path, ensure_date_string
    from src.folder_management.make_folders import setup_logging, create_folders

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
    latest_reception_data_date = ensure_date_string(latest_reception_data_date)

    # 1. 最新のクラブ情報付き受付データファイルを取得(クラブ情報付き受付データ_受付{latest_reception_data_date}_*.xlsxを使用)
    logging.info("最新のクラブ情報付き受付データファイルを取得します")
    # 最新のクラブ情報付き受付データと同じ日付のファイルを取得
    if not latest_reception_data_date:
        logging.error("最新の受付データの日付が指定されていません")
        return    
    latest_club_reception_files = [
        f for f in os.listdir(clubs_reception_data_path)
        if os.path.isfile(os.path.join(clubs_reception_data_path, f)) and
        f.startswith(f'クラブ情報付き受付データ_受付{latest_reception_data_date}') and f.endswith('.xlsx')
    ]
    latest_club_reception_files.sort(reverse=True)
    if not latest_club_reception_files:
        logging.error(f"クラブ情報付き受付データファイルが見つかりません: クラブ情報付き受付データ_受付{latest_reception_data_date}*.xlsx")
        return
    latest_club_reception_file = latest_club_reception_files[0]
    logging.info(f"最新のクラブ情報付き受付データファイル: {latest_club_reception_file}")
    club_reception_df = pd.read_excel(os.path.join(clubs_reception_data_path, latest_club_reception_file))
    logging.info(f"最新のクラブ情報付き受付データを読み込みました: {latest_club_reception_file}")

    # 2. 書類02_2_のチェックリストを作成する必要があるか確認
    logging.info("書類02_2_のチェックリストを作成する必要があるか確認します")
    # 書類02_2_のチェックリストが既に存在するか確認
    existing_checklist_files = [
        f for f in os.listdir(document02_2_checklist_folder_path)
        if os.path.isfile(os.path.join(document02_2_checklist_folder_path, f)) and
        f.startswith('書類02_2_チェックリスト_') and f.endswith('.xlsx')
    ]
    
    # 既存の書類02_2_のチェックリストで同じ受付データのものがあるか確認
    existing_checklist_files.sort(reverse=True)
    for file in existing_checklist_files:
        # ファイル名から受付日時を抽出: 書類02_2_チェックリスト_受付{YYYYMMDDHHMMSS}_作成{YYYYMMDDHHMMSS}.xlsx
        file_parts = file.replace('書類02_2_チェックリスト_受付', '').replace('.xlsx', '').split('_作成')
        if len(file_parts) >= 1:
            file_reception_date_str = file_parts[0]
            try:
                file_reception_date = pd.to_datetime(file_reception_date_str, format='%Y%m%d%H%M%S')
                if file_reception_date == pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S'):
                    logging.info(f"同じ受付データの書類02_2_チェックリストが既に存在します: {file}")
                    logging.info("新しいチェックリストを作成しません。")
                    return
                elif file_reception_date < pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S'):
                    logging.info(f"古い受付データの書類02_2_チェックリストが存在します: {file}")
                    logging.info("新しい受付データ用のチェックリストを作成します。")
                    break
            except ValueError:
                logging.warning(f"ファイル名から受付日時を解析できませんでした: {file}")
                continue

    # 3. 書類02_2_のチェックリストのカラム名を取得
    logging.info("書類02_2_のチェックリストのカラム名を取得します")
    # jsonファイルを読み込む（document02_2_checklist_columns.jsonが必要）
    from src.core.utils import get_config_file_path
    document02_2_checklist_columns_file_path = get_config_file_path('config/checklist_columns/document02_2_checklist_columns.json')
    if not os.path.exists(document02_2_checklist_columns_file_path):
        logging.error(f"書類02_2のチェックリストのカラム名ファイルが見つかりません: {document02_2_checklist_columns_file_path}")
        return
    document02_2_checklist_columns = pd.read_json(document02_2_checklist_columns_file_path, orient='records')
    logging.info(f"チェックリストのカラム名を読み込みました: {document02_2_checklist_columns_file_path}")

    # 4. 書類02_2のチェックリストのデータフレームを作成
    logging.info("書類02_2のチェックリストのデータフレームを作成します")
    document02_2_checklist_df = pd.DataFrame(columns=document02_2_checklist_columns['document02_2_checklist_columns'].tolist())
    logging.info("書類02_2のチェックリストのデータフレームを作成しました")
    # 競技種目のリストを読み込む
    logging.info("競技種目のリストを読み込みます")
    discipline_file_path = get_config_file_path('config/reference_data/list_of_disciplines.xlsx')
    discipline_df = pd.read_excel(discipline_file_path)  
    discipline = discipline_df['disciplines']
    logging.info("競技種目のリストを読み込みました")

    # 5. 書類02_2のチェックリストのデータフレームにクラブ情報を追加
    logging.info("書類02_2のチェックリストのデータフレームにクラブ情報を追加します")
    # 書類02_2のチェックリストのデータフレームにクラブ情報を追加
    for index, row in club_reception_df.iterrows():
        club_name = row['クラブ名']
        logging.info(f"クラブ名: {club_name} のチェックリストを作成します")
        document02_2_checklist_df.loc[index, '申請日時'] = row['申請_タイムスタンプ']
        document02_2_checklist_df.loc[index, 'クラブ名'] = club_name
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
        document02_2_checklist_df.loc[index, '活動種目数'] = count_of_disciplines
        # 指導者数の取得(discipline_df['coach']が1のカラムに限定)
        coaches_discipline = discipline_df[discipline_df['coach'] == 1]['disciplines'].tolist()
        coaches_columns = [f'申請_指導者_{discipline}' for discipline in coaches_discipline]
        count_of_coaches = 0
        # 各指導者カラムをループし、「配置している」が選択されているかを確認
        for col in coaches_columns:
            if col in row and row[col] == '配置している':
                count_of_coaches += 1
        # 指導者数が0の場合は、'0'と記載
        if count_of_coaches == 0:
            count_of_coaches = '0'
        else:
            count_of_coaches = str(count_of_coaches)
        document02_2_checklist_df.loc[index, '指導者数'] = count_of_coaches
        document02_2_checklist_df.loc[index, '申請_クラブマネジャー_配置'] = row['申請_マネジャー_配置状況']
        document02_2_checklist_df.loc[index, '申請_クラブマネジャー資格数（クラブマネジャー）'] = row['申請_マネジャー_マネ資格_数']
        document02_2_checklist_df.loc[index, '申請_アシスタントマネジャー資格数（クラブマネジャー）'] = row['申請_マネジャー_アシマネ資格_数']
        document02_2_checklist_df.loc[index, '申請_クラブマネジャー資格数（事務局）'] = row['申請_事務局_マネ資格_数']
        document02_2_checklist_df.loc[index, '申請_アシスタントマネジャー資格数（事務局）'] = row['申請_事務局_アシマネ資格_数']
        # 受付日時のカラムはlatest_reception_data_dateを使用
        document02_2_checklist_df.loc[index, '受付日時'] = pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
        # チェックリスト作成日時のカラムは現在のJST日時を使用
        document02_2_checklist_df.loc[index, 'チェックリスト作成日時'] = pd.to_datetime(get_jst_now()).strftime('%Y-%m-%d %H:%M:%S')
        # チェック項目のカラムを指定
        check_columns = [
            'チェック項目_活動種目',
            'チェック項目_指導者',
            'チェック項目_種目・指導者',
            'チェック項目_クラブマネジャー配置',
            'チェック項目_マネジメント指導者資格',
        ]
        # チェック項目の初期状態は「未チェック」
        for col in check_columns:
            document02_2_checklist_df.loc[index, col] = '未チェック'
        # チェック項目_その他の初期状態は空文字列
        document02_2_checklist_df.loc[index, 'チェック項目_その他'] = ''
        # チェック者名の初期状態は「チェックが完了していません」
        document02_2_checklist_df.loc[index, 'チェック者名_活動内容'] = 'チェックが完了していません'
        logging.info(f"クラブ名: {club_name} のチェックリストを作成しました")
    logging.info("書類02_2のチェックリストのデータフレームを作成しました")

    # 5. 書類02_2のチェックリストのデータフレームを保存(ファイル名は「書類02_2チェックリスト_受付{latest_reception_data_date}_作成{YYYYMMDDHHMMSS}.xlsx」)
    logging.info("書類02_2のチェックリストのデータフレームを保存します")
    now_jst = get_jst_now()
    document02_2_checklist_file_name = f'書類02_2チェックリスト_受付{latest_reception_data_date}_作成{now_jst.strftime("%Y%m%d%H%M%S")}.xlsx'
    document02_2_checklist_file_path = os.path.join(document02_2_checklist_folder_path, document02_2_checklist_file_name)
    document02_2_checklist_df.to_excel(document02_2_checklist_file_path, index=False)
    logging.info(f"書類02_2のチェックリストのデータフレームを保存しました: {document02_2_checklist_file_path}")

    # 6. 書類02_2のチェックリストのファイルを保存
    logging.info("書類02_2のチェックリストのファイルを保存します")
    document02_2_checklist_df.to_excel(document02_2_checklist_file_path, index=False)
    logging.info(f"書類02_2のチェックリストのファイルを保存しました: {document02_2_checklist_file_path}")