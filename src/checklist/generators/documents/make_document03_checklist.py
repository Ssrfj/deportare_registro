﻿def make_document03_checklist(latest_reception_data_date):
    import os
    import pandas as pd
    import logging
    from src.core.setting_paths import content_check_folder_path, document03_checklist_folder_path, clubs_reception_data_path
    from src.core.utils import get_jst_now, ensure_date_string
    
    # ロギングの設定    logging.info("ロギングを設定しました")
    # フォルダの作成    logging.info("フォルダを作成しました")

    # 最新の受付データの日付をフォーマット
    if not latest_reception_data_date:
        logging.error("最新の受付データの日付が指定されていません")
        return
    latest_reception_data_date_str = ensure_date_string(latest_reception_data_date)

    # 1. 最新のクラブ情報付き受付データファイルを取得(クラブ情報付き受付データ_受付{latest_reception_data_date_str}_*.xlsxを使用)
    logging.info("最新のクラブ情報付き受付データファイルを取得します")
    # 最新のクラブ情報付き受付データと同じ日付のファイルを取得
    if not latest_reception_data_date_str:
        logging.error("最新の受付データの日付が指定されていません")
        return    
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

    # 2. 書類03_のチェックリストを作成する必要があるか確認
    logging.info("書類03_のチェックリストを作成する必要があるか確認します")
    # 書類03_のチェックリストが既に存在するか確認
    existing_checklist_files = [
        f for f in os.listdir(document03_checklist_folder_path)
        if os.path.isfile(os.path.join(document03_checklist_folder_path, f)) and
        f.startswith('書類03_チェックリスト_') and f.endswith('.xlsx')
    ]
    
    # 既存の書類03_のチェックリストで同じ受付データのものがあるか確認
    existing_checklist_files.sort(reverse=True)
    for file in existing_checklist_files:
        # ファイル名から受付日時を抽出: 書類03_チェックリスト_受付{YYYYMMDDHHMMSS}_作成{YYYYMMDDHHMMSS}.xlsx
        file_parts = file.replace('書類03_チェックリスト_受付', '').replace('.xlsx', '').split('_作成')
        if len(file_parts) >= 1:
            file_reception_date_str = file_parts[0]
            try:
                file_reception_date = pd.to_datetime(file_reception_date_str, format='%Y%m%d%H%M%S')
                if file_reception_date == pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S'):
                    logging.info(f"同じ受付データの書類03_チェックリストが既に存在します: {file}")
                    logging.info("新しいチェックリストを作成しません。")
                    return
                elif file_reception_date < pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S'):
                    logging.info(f"古い受付データの書類03_チェックリストが存在します: {file}")
                    logging.info("新しい受付データ用のチェックリストを作成します。")
                    break
            except ValueError:
                logging.warning(f"ファイル名から受付日時を解析できませんでした: {file}")
                continue

    # 3. 書類03_のチェックリストのカラム名を取得
    logging.info("書類03_のチェックリストのカラム名を取得します")
    # jsonファイルを読み込む（document03_checklist_columns.jsonが必要）
    from src.core.utils import get_config_file_path
    document03_checklist_columns_file_path = get_config_file_path('config/checklist_columns/document03_checklist_columns.json')
    if not os.path.exists(document03_checklist_columns_file_path):
        logging.error(f"書類03のチェックリストのカラム名ファイルが見つかりません: {document03_checklist_columns_file_path}")
        return
    document03_checklist_columns = pd.read_json(document03_checklist_columns_file_path, orient='records')
    logging.info(f"チェックリストのカラム名を読み込みました: {document03_checklist_columns_file_path}")

    # 4. 書類03のチェックリストのデータフレームを作成
    logging.info("書類03のチェックリストのデータフレームを作成します")
    document03_checklist_df = pd.DataFrame(columns=document03_checklist_columns['document03_checklist_columns'].tolist())
    logging.info("書類03のチェックリストのデータフレームを作成しました")

    # 書類03のチェックリストのデータフレームにクラブ情報を追加
    logging.info("書類03のチェックリストのデータフレームにクラブ情報を追加します")
    for index, row in club_reception_df.iterrows():
        club_name = row['クラブ名']
        logging.info(f"クラブ名: {club_name} のチェックリストを作成します")
        document03_checklist_df.loc[index, '申請日時'] = row['申請_タイムスタンプ']
        document03_checklist_df.loc[index, 'クラブ名'] = club_name
        # 書類チェックの結果を記載するカラムを指定
        document03_check_result_columns = [
            '担当者入力_法人格',
            '担当者入力_会員資格',
            '担当者入力_規約等の改廃意思決定機関',
            "担当者入力_規約等の改廃意思決定機関の議決権保有者",
            "担当者入力_規約等の改廃意思決定機関の定足数",
            "担当者入力_規約等の改廃意思決定機関の議決数",
            "担当者入力_規約等の改廃意思決定機関の議事録",
            '担当者入力_事業計画の意思決定機関',
            '担当者入力_事業計画の意思決定機関の議決権保有者',
            '担当者入力_事業計画の意思決定機関の定足数',
            '担当者入力_事業計画の意思決定機関の議決数',
            '担当者入力_事業計画の意思決定機関の議事録',
            '担当者入力_予算の意思決定機関',
            '担当者入力_予算の意思決定機関の議決権保有者',
            '担当者入力_予算の意思決定機関の定足数',
            '担当者入力_予算の意思決定機関の議決数',
            '担当者入力_予算の意思決定機関の議事録',
            '担当者入力_事業報告の意思決定機関',
            '担当者入力_事業報告の意思決定機関の議決権保有者',
            '担当者入力_事業報告の意思決定機関の定足数',
            '担当者入力_事業報告の意思決定機関の議決数',
            '担当者入力_事業報告の意思決定機関の議事録',
            '担当者入力_決算の意思決定機関',
            '担当者入力_決算の意思決定機関の議決権保有者',
            '担当者入力_決算の意思決定機関の定足数',
            '担当者入力_決算の意思決定機関の議決数',
            '担当者入力_決算の意思決定機関の議事録',
            '担当者入力_役員資格・選任規程',
            '担当者入力_その他規程'
        ]
        # 書類チェックの結果の初期状態は「書類未チェック」
        for col in document03_check_result_columns:
            document03_checklist_df.loc[index, col] = '書類未チェック'
        # 受付日時のカラムはlatest_reception_data_dateを使用
        document03_checklist_df.loc[index, '受付日時'] = pd.to_datetime(latest_reception_data_date, format='%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
        # チェックリスト作成日時のカラムは現在のJST日時を使用
        document03_checklist_df.loc[index, 'チェックリスト作成日時'] = pd.to_datetime(get_jst_now()).strftime('%Y-%m-%d %H:%M:%S')
        # チェック項目のカラムを指定
        check_columns = [
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
        # チェック項目の初期状態は「未チェック」
        for col in check_columns:
            document03_checklist_df.loc[index, col] = '未チェック'
        # チェック項目_その他の初期状態は空文字列
        document03_checklist_df.loc[index, 'チェック項目_その他'] = ''
        # チェック者名の初期状態は「チェックが完了していません」
        document03_checklist_df.loc[index, 'チェック者名_活動内容'] = 'チェックが完了していません'
    logging.info("書類03のチェックリストのデータフレームを作成しました")

    # 5. 書類03のチェックリストのデータフレームを保存(ファイル名は「書類03チェックリスト_受付{latest_reception_data_date_str}_作成{YYYYMMDDHHMMSS}.xlsx」)
    logging.info("書類03のチェックリストのデータフレームを保存します")
    now_jst = get_jst_now()
    document03_checklist_file_name = f'書類03チェックリスト_受付{latest_reception_data_date_str}_作成{now_jst.strftime("%Y%m%d%H%M%S")}.xlsx'
    document03_checklist_file_path = os.path.join(document03_checklist_folder_path, document03_checklist_file_name)
    document03_checklist_df.to_excel(document03_checklist_file_path, index=False)
    logging.info(f"書類03のチェックリストのデータフレームを保存しました: {document03_checklist_file_path}")

    # 6. 書類03のチェックリストのファイルを保存
    logging.info("書類03のチェックリストのファイルを保存します")
    document03_checklist_df.to_excel(document03_checklist_file_path, index=False)
    logging.info(f"書類03のチェックリストのファイルを保存しました: {document03_checklist_file_path}")
