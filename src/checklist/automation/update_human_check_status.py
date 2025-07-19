def update_human_check_status_to_overall_checklist(overall_checklist_df, checklist_file_path, club_reception_df, latest_reception_data_date):
    """
    人間によるチェック結果を総合チェックリストに反映する関数
    
    Args:
        overall_checklist_df (pd.DataFrame): 総合チェックリスト
        checklist_file_path (str): チェックリストファイルのパス
        club_reception_df (pd.DataFrame): 受付データ
        latest_reception_data_date (str): 最新受付データ日付
    
    Returns:
        pd.DataFrame: 更新された総合チェックリスト
    """
    import os
    import pandas as pd
    import logging
    from datetime import datetime, timezone, timedelta
    from src.core.setting_paths import overall_checklist_folder_path
    from src.core.utils import get_jst_now, ensure_date_string
    from src.core.load_latest_club_data import load_latest_club_reception_data, get_club_data_by_name_and_date
    
    logging.info("人間によるチェック結果を総合チェックリストに反映を開始します")
    
    # 統合されたクラブ情報付き受付データを読み込み
    logging.info("統合されたクラブ情報付き受付データを読み込みます")
    integrated_club_data = load_latest_club_reception_data()
    if integrated_club_data is None:
        logging.error("統合されたクラブ情報付き受付データの読み込みに失敗しました")
        return overall_checklist_df

    # overall_checklist_dfがDataFrameであることを確認
    if not isinstance(overall_checklist_df, pd.DataFrame):
        logging.error("overall_checklist_dfはDataFrameではありません。")
        return overall_checklist_df
    
    # overall_checklist_dfに 'クラブ名'カラムが存在するか確認
    if 'クラブ名' not in overall_checklist_df.columns:
        logging.error("'クラブ名' カラムが overall_checklist_df に存在しません。")
        return overall_checklist_df
    
    # overall_checklist_dfに '受付日時'カラムが存在するか確認
    if '受付日時' not in overall_checklist_df.columns:
        logging.error("'受付日時' カラムが overall_checklist_df に存在しません。")
        return overall_checklist_df

    # 個別書類チェックリストファイルから人間チェック結果を読み込む
    from src.core.setting_paths import output_main_folder_path
    checklist_base_folder = os.path.join(output_main_folder_path, "受付内容チェック")
    
    # 書類チェックリストフォルダのマッピング
    document_folder_mapping = {
        '書類01': '書類01チェックリスト',
        '書類02-1': '書類02-1チェックリスト', 
        '書類02-2': '書類02-2チェックリスト',
        '書類03': '書類03チェックリスト',
        '書類04': '書類04チェックリスト',
        '書類05予算': '書類05予算書チェックリスト',
        '書類05計画': '書類05計画書チェックリスト',
        '書類06決算': '書類06決算書チェックリスト',
        '書類06報告': '書類06報告書チェックリスト',
        '書類07': '書類07チェックリスト',
        '書類08': '書類08チェックリスト',
        '書類09': '書類09チェックリスト',
        '書類10': '書類10チェックリスト'
    }

    # overall_checklist_dfの行ごとに処理を行う
    for index, row in overall_checklist_df.iterrows():
        club_name = str(row['クラブ名']).strip()
        apried_date_str = str(row.get('受付日時')).strip()
        
        # 受付日時をファイル名形式（YYYYMMDDHHMMSS）に変換
        try:
            # まず小数点以下を除去
            if '.' in apried_date_str:
                apried_date_str = apried_date_str.split('.')[0]
            
            # pandas.to_datetimeで解析してからYYYYMMDDHHMMSS形式に変換
            dt = pd.to_datetime(apried_date_str)
            apried_date_formatted = dt.strftime('%Y%m%d%H%M%S')
            
            logging.info(f"受付日時: {apried_date_str} -> {apried_date_formatted}")
            
        except Exception as e:
            logging.warning(f"受付日時の変換に失敗しました: {apried_date_str}, エラー: {e}")
            continue
            
        # 処理開始のメッセージを表示
        logging.info(f"クラブ名: {club_name} の人間によるチェック結果の反映を開始します")
        
        # 人間によるチェック結果を集約する変数
        human_check_found = False
        human_check_results = []
        human_check_found_docs = set()  # 重複を避けるためのセット
        latest_human_check_time = None
        
        # 各書類のチェックリストファイルを確認
        for doc_key, folder_name in document_folder_mapping.items():
            folder_path = os.path.join(checklist_base_folder, folder_name)
            
            if not os.path.exists(folder_path):
                continue
                
            # フォルダ内のExcelファイルを検索
            try:
                files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx') and not f.startswith('~$')]
                for file_name in files:
                    # ファイル名での照合をやめて、すべてのファイルをチェック
                    file_path = os.path.join(folder_path, file_name)
                    
                    logging.info(f"ファイルをチェック中: {file_name}")
                    
                    try:
                        # Excelファイルを読み込み
                        df = pd.read_excel(file_path)
                        
                        # クラブ名でフィルタリング
                        if 'クラブ名' in df.columns:
                            club_rows = df[df['クラブ名'] == club_name]
                            
                            if not club_rows.empty:
                                logging.info(f"クラブ '{club_name}' がファイル {file_name} に見つかりました")
                                
                                # 人間チェック結果の詳細を収集
                                detailed_check_results = []
                                has_human_input = False
                                
                                # チェック者名の列を探す
                                checker_columns = [col for col in df.columns if 'チェック者名' in col]
                                
                                for _, club_row in club_rows.iterrows():
                                    # チェック者名の確認
                                    checker_name = None
                                    for col in checker_columns:
                                        cell_value = club_row.get(col)
                                        if pd.notna(cell_value) and str(cell_value).strip() != '':
                                            checker_name = str(cell_value).strip()
                                            has_human_input = True
                                            logging.info(f"チェック者発見: {checker_name}")
                                            break
                                    
                                    if has_human_input and checker_name:
                                        # 各チェック項目の状態を確認
                                        check_items = []
                                        
                                        # チェック項目の列を特定
                                        check_item_columns = [col for col in df.columns if 'チェック項目' in col]
                                        
                                        for check_col in check_item_columns:
                                            check_value = club_row.get(check_col)
                                            if pd.notna(check_value):
                                                check_status = str(check_value).strip()
                                                # チェック項目名を取得
                                                item_name = check_col.replace('チェック項目_', '')
                                                
                                                if check_status == '未チェック':
                                                    check_items.append(f"{item_name}: 未チェック")
                                                elif check_status == '1':
                                                    check_items.append(f"{item_name}: 正常")
                                                elif check_status == '0':
                                                    check_items.append(f"{item_name}: 異常あり")
                                        
                                        # 入力内容の異常をチェック
                                        input_issues = []
                                        
                                        # クラブ名の確認
                                        club_name_input = club_row.get('入力されたクラブ名', '')
                                        if pd.isna(club_name_input) or str(club_name_input).strip() == '':
                                            input_issues.append("クラブ名が未入力")
                                        elif str(club_name_input).strip() != club_name:
                                            input_issues.append(f"クラブ名不一致 (入力値: {str(club_name_input).strip()})")
                                        
                                        # 申請種別の確認
                                        application_type = club_row.get('申請種別', '')
                                        if pd.isna(application_type) or str(application_type).strip() == '':
                                            input_issues.append("申請種別が未入力")
                                        
                                        # 担当者名の確認
                                        contact_person = club_row.get('申請_申請担当者名', '')
                                        if pd.isna(contact_person) or str(contact_person).strip() == '':
                                            input_issues.append("申請担当者名が未入力")
                                        
                                        # 結果をまとめる
                                        if doc_key not in human_check_found_docs:
                                            result_parts = [f"チェック者: {checker_name}"]
                                            
                                            if check_items:
                                                result_parts.append("項目状況: " + ", ".join(check_items))
                                            
                                            if input_issues:
                                                result_parts.append("入力問題: " + ", ".join(input_issues))
                                                
                                            detailed_check_results.append(f"{doc_key}: {'; '.join(result_parts)}")
                                            human_check_found_docs.add(doc_key)
                                            logging.info(f"クラブ '{club_name}' で {doc_key} の詳細チェック結果を記録しました")
                                        
                                        # ファイルの最終更新時間を取得
                                        file_stat = os.stat(file_path)
                                        file_mtime = datetime.fromtimestamp(file_stat.st_mtime, tz=timezone(timedelta(hours=9)))
                                        
                                        if latest_human_check_time is None or file_mtime > latest_human_check_time:
                                            latest_human_check_time = file_mtime
                                
                                if has_human_input:
                                    human_check_found = True
                                    human_check_results.extend(detailed_check_results)
                    
                    except Exception as e:
                        logging.warning(f"ファイル {file_path} の読み込み中にエラーが発生しました: {e}")
                        continue
                            
            except Exception as e:
                logging.warning(f"フォルダ {folder_path} の処理中にエラーが発生しました: {e}")
                continue
        
        # 人間チェック結果が見つからない場合はスキップ
        if not human_check_found:
            logging.info(f"クラブ '{club_name}' の人間によるチェック結果が見つかりませんでした")
            continue
        
        # 既に総合チェックリストに人間チェック結果が反映されているかを確認
        document_check_update_time = overall_checklist_df.loc[index, '書類チェック更新日時']
        try:
            if pd.notna(document_check_update_time) and str(document_check_update_time).strip() != '':
                overall_update_time = pd.to_datetime(str(document_check_update_time))
                
                if latest_human_check_time and overall_update_time >= latest_human_check_time:
                    logging.info(f"クラブ '{club_name}' の人間によるチェック結果は既に総合チェックリストに反映済みです")
                    continue
        except Exception as e:
            logging.warning(f"日時の比較中にエラーが発生しました: {e}")
        
        # 人間によるチェック結果を総合チェックリストに反映
        try:
            jst_now = datetime.now(timezone(timedelta(hours=9)))
            update_datetime = jst_now.strftime('%Y-%m-%d %H:%M:%S')
            
            # 人間によるチェック結果をまとめる
            human_check_result = "; ".join(human_check_results)
            
            # 総合チェックリストの書類チェック結果を更新
            overall_checklist_df.loc[index, '書類チェック結果'] = human_check_result
            overall_checklist_df.loc[index, '書類チェック更新日時'] = update_datetime
            
            logging.info(f"クラブ名: {club_name} の人間によるチェック結果を総合チェックリストに反映しました")
            
        except Exception as e:
            logging.error(f"クラブ '{club_name}' の人間によるチェック結果の反映中にエラーが発生しました: {e}")
            continue
    
    logging.info("全てのクラブの人間によるチェック結果の反映が完了しました")

    # 総合チェックリストのファイルを保存（ファイル名は「総合チェックリスト_受付{YYYYMMDDHHMMSS}_更新{YYYYMMDDHHMMSS}.xlsx」）
    logging.info("総合チェックリストのファイルを保存します")
    now_jst = get_jst_now()
    latest_reception_data_date_str = ensure_date_string(latest_reception_data_date)
    overall_checklist_file_name = f'総合チェックリスト_受付{latest_reception_data_date_str}_更新{now_jst.strftime("%Y%m%d%H%M%S")}.xlsx'
    overall_checklist_file_path = os.path.join(overall_checklist_folder_path, overall_checklist_file_name)
    overall_checklist_df.to_excel(overall_checklist_file_path, index=False)
    logging.info(f"総合チェックリストのファイルを保存しました: {overall_checklist_file_path}")
    logging.info("人間によるチェック結果の反映が完了しました")
    
    return overall_checklist_df
