﻿def make_document08_checklist(latest_reception_data_date):
    import os
    import pandas as pd
    import logging
    from src.core.setting_paths import content_check_folder_path, document08_checklist_folder_path, clubs_reception_data_path
    from src.core.utils import get_jst_now, ensure_date_string, get_config_file_path
    
    # ロギングの設定    logging.info("ロギングを設定しました")
    # フォルダの作成    logging.info("フォルダを作成しました")

    # 最新の受付データの日付をフォーマット
    if not latest_reception_data_date:
        logging.error("最新の受付データの日付が指定されていません")
        return
    
    # 日付を文字列形式に正規化
    latest_reception_data_date_str = ensure_date_string(latest_reception_data_date)
    logging.info(f"受付データの日付: {latest_reception_data_date_str}")

    # 1. 最新のクラブ情報付き受付データファイルを取得(クラブ情報付き受付データ_受付{latest_reception_data_date_str}_*.xlsxを使用)
    logging.info("最新のクラブ情報付き受付データファイルを取得します")
    # 最新のクラブ情報付き受付データと同じ日付のファイルを取得
    latest_club_reception_files = [
        f for f in os.listdir(clubs_reception_data_path)
        if os.path.isfile(os.path.join(clubs_reception_data_path, f)) and
        f.startswith(f'クラブ情報付き受付データ_受付{latest_reception_data_date_str}') and f.endswith('.xlsx')
    ]
    latest_club_reception_files.sort(reverse=True)
    if not latest_club_reception_files:
        logging.error(f"クラブ情報付き受付データファイルが見つかりません: クラブ情報付き受付データ_受付{latest_reception_data_date_str}*.xlsx")
        return
    latest_club_reception_file = latest_club_reception_files[0]
    logging.info(f"最新のクラブ情報付き受付データファイル: {latest_club_reception_file}")
    club_reception_df = pd.read_excel(os.path.join(clubs_reception_data_path, latest_club_reception_file))
    logging.info(f"最新のクラブ情報付き受付データを読み込みました: {latest_club_reception_file}")

    # 2. 書類08_のチェックリストを作成する必要があるか確認
    logging.info("書類08_のチェックリストを作成する必要があるか確認します")
    # 書類08_のチェックリストが既に存在するか確認
    existing_checklist_files = [
        f for f in os.listdir(document08_checklist_folder_path)
        if os.path.isfile(os.path.join(document08_checklist_folder_path, f)) and
        f.startswith('書類08_チェックリスト_') and f.endswith('.xlsx')
    ]
    
    # 既存の書類08_のチェックリストで同じ受付データのものがあるか確認
    existing_checklist_files.sort(reverse=True)
    for file in existing_checklist_files:
        # ファイル名から受付日時を抽出: 書類08_チェックリスト_受付{YYYYMMDDHHMMSS}_作成{YYYYMMDDHHMMSS}.xlsx
        file_parts = file.replace('書類08_チェックリスト_受付', '').replace('.xlsx', '').split('_作成')
        if len(file_parts) >= 1:
            file_reception_date_str = file_parts[0]
            try:
                file_reception_date = pd.to_datetime(file_reception_date_str, format='%Y%m%d%H%M%S')
                if file_reception_date == pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S'):
                    logging.info(f"同じ受付データの書類08_チェックリストが既に存在します: {file}")
                    logging.info("新しいチェックリストを作成しません。")
                    return
                elif file_reception_date < pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S'):
                    logging.info(f"古い受付データの書類08_チェックリストが存在します: {file}")
                    logging.info("新しい受付データ用のチェックリストを作成します。")
                    break
            except ValueError:
                logging.warning(f"ファイル名から受付日時を解析できませんでした: {file}")
                continue

    # 3. 書類08_のチェックリストのカラム名を取得
    logging.info("書類08_のチェックリストのカラム名を取得します")
    # jsonファイルを読み込む（document08_checklist_columns.jsonが必要）
    document08_checklist_columns_file_path = get_config_file_path('config/checklist_columns/document08_checklist_columns.json')
    if not os.path.exists(document08_checklist_columns_file_path):
        logging.error(f"書類08のチェックリストのカラム名ファイルが見つかりません: {document08_checklist_columns_file_path}")
        return
    document08_checklist_columns = pd.read_json(document08_checklist_columns_file_path, orient='records')
    logging.info(f"チェックリストのカラム名を読み込みました: {document08_checklist_columns_file_path}")

    # 4. 書類08のチェックリストのデータフレームを作成
    logging.info("書類08のチェックリストのデータフレームを作成します")
    document08_checklist_df = pd.DataFrame(columns=document08_checklist_columns['document08_checklist_columns'].tolist())
    logging.info("書類08のチェックリストのデータフレームを作成しました")

    # 書類08のチェックリストのデータフレームにクラブ情報を追加
    for index, row in club_reception_df.iterrows():
        club_name = row['クラブ名']
        document08_checklist_df.loc[index, '申請日時'] = row['申請_タイムスタンプ']
        document08_checklist_df.loc[index, 'クラブ名'] = club_name
        document08_checklist_df.loc[index, '申請_規約_改定有無'] = row['申請_規約_改定有無']
        document08_checklist_df.loc[index, '申請_規約_改定時議事録_書類(選択時必須)'] = row['申請_規約_改定時議事録_書類(選択時必須)']
        document08_checklist_df.loc[index, '申請_事業計画_議事録_書類'] = row['申請_事業計画_議事録_書類']
        document08_checklist_df.loc[index, '申請_予算_議事録_書類'] = row['申請_予算_議事録_書類']
        document08_checklist_df.loc[index, '申請_事業報告_提出有無'] = row['申請_事業報告_提出有無']
        document08_checklist_df.loc[index, '申請_事業報告_議事録_書類(選択時必須)'] = row['申請_事業報告_議事録_書類(選択時必須)']
        document08_checklist_df.loc[index, '申請_決算_提出有無'] = row['申請_決算_提出有無']
        document08_checklist_df.loc[index, '申請_決算_議事録_書類(選択時必須)'] = row['申請_決算_議事録_書類(選択時必須)']

        # 書類チェックの結果を記載するカラムを指定
        document08_check_result_columns = [
            '書類チェック_議事録_規約等_名称',
            '書類チェック_議事録_規約等_開催日時',
            '書類チェック_議事録_規約等_開催場所',
            '書類チェック_議事録_規約等_議決権保有者数',
            '書類チェック_議事録_規約等_議決権行使者数',
            '書類チェック_議事録_規約等_議案',
            '書類チェック_議事録_規約等_審議・議決結果',
            '書類チェック_議事録_規約等_議決方法',
            '書類チェック_議事録_規約等_署名',
            '書類チェック_議事録_事業計画_名称',
            '書類チェック_議事録_事業計画_開催日時',
            '書類チェック_議事録_事業計画_開催場所',
            '書類チェック_議事録_事業計画_議決権保有者数',
            '書類チェック_議事録_事業計画_議決権行使者数',
            '書類チェック_議事録_事業計画_議案',
            '書類チェック_議事録_事業計画_審議・議決結果',
            '書類チェック_議事録_事業計画_議決方法',
            '書類チェック_議事録_事業計画_署名',
            '書類チェック_議事録_予算_名称',
            '書類チェック_議事録_予算_開催日時',
            '書類チェック_議事録_予算_開催場所',
            '書類チェック_議事録_予算_議決権保有者数',
            '書類チェック_議事録_予算_議決権行使者数',
            '書類チェック_議事録_予算_議案',
            '書類チェック_議事録_予算_審議・議決結果',
            '書類チェック_議事録_予算_議決方法',
            '書類チェック_議事録_予算_署名',
            '書類チェック_議事録_事業報告_名称',
            '書類チェック_議事録_事業報告_開催日時',
            '書類チェック_議事録_事業報告_開催場所',
            '書類チェック_議事録_事業報告_議決権保有者数',
            '書類チェック_議事録_事業報告_議決権行使者数',
            '書類チェック_議事録_事業報告_議案',
            '書類チェック_議事録_事業報告_審議・議決結果',
            '書類チェック_議事録_事業報告_議決方法',
            '書類チェック_議事録_事業報告_署名',
            '書類チェック_議事録_決算_名称',
            '書類チェック_議事録_決算_開催日時',
            '書類チェック_議事録_決算_開催場所',
            '書類チェック_議事録_決算_議決権保有者数',
            '書類チェック_議事録_決算_議決権行使者数',
            '書類チェック_議事録_決算_議案',
            '書類チェック_議事録_決算_審議・議決結果',
            '書類チェック_議事録_決算_議決方法',
            '書類チェック_議事録_決算_署名'
        ]
        # 書類チェックの結果の初期状態は「書類未チェック」
        for col in document08_check_result_columns:
            document08_checklist_df.loc[index, col] = '書類未チェック'
        # 受付日時のカラムはlatest_reception_data_dateを使用
        document08_checklist_df.loc[index, '受付日時'] = pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
        # チェックリスト作成日時のカラムは現在のJST日時を使用
        document08_checklist_df.loc[index, 'チェックリスト作成日時'] = pd.to_datetime(get_jst_now()).strftime('%Y-%m-%d %H:%M:%S')
        # チェック項目のカラムを指定
        check_columns = [
            'チェック項目_議事録',
        ]
        # チェック項目の初期状態は「未チェック」
        for col in check_columns:
            document08_checklist_df.loc[index, col] = '未チェック'
        # チェック項目_その他の初期状態は空文字列
        document08_checklist_df.loc[index, 'チェック項目_その他'] = ''
        # チェック者名の初期状態は「チェックが完了していません」
        document08_checklist_df.loc[index, 'チェック者名_議事録'] = 'チェックが完了していません'
    logging.info("書類08のチェックリストのデータフレームを作成しました")

    # 5. 書類08のチェックリストのデータフレームを保存(ファイル名は「書類08チェックリスト_受付{latest_reception_data_date_str}_作成{YYYYMMDDHHMMSS}.xlsx」)
    logging.info("書類08のチェックリストのデータフレームを保存します")
    now_jst = get_jst_now()
    document08_checklist_file_name = f'書類08チェックリスト_受付{latest_reception_data_date_str}_作成{now_jst.strftime("%Y%m%d%H%M%S")}.xlsx'
    document08_checklist_file_path = os.path.join(document08_checklist_folder_path, document08_checklist_file_name)
    document08_checklist_df.to_excel(document08_checklist_file_path, index=False)
    logging.info(f"書類08のチェックリストのデータフレームを保存しました: {document08_checklist_file_path}")

    # 6. 書類08のチェックリストのファイルを保存
    logging.info("書類08のチェックリストのファイルを保存します")
    document08_checklist_df.to_excel(document08_checklist_file_path, index=False)
    logging.info(f"書類08のチェックリストのファイルを保存しました: {document08_checklist_file_path}")
