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

    # チェックリスト作成状況ファイルの読み込み
    try:
        # folder_of_checklist_create_statusを取得
        from src.core.setting_paths import output_path
        folder_of_checklist_create_status = os.path.join(output_path, 'R7_登録受付処理')
        checklist_status_path = os.path.join(folder_of_checklist_create_status, 'クラブごとのチェックリスト作成状況.xlsx')
        
        if os.path.exists(checklist_status_path):
            checklist_status_df = pd.read_excel(checklist_status_path)
            logging.info("チェックリスト作成状況ファイルを読み込みました")
        else:
            logging.warning("チェックリスト作成状況ファイルが存在しません")
            return overall_checklist_df
            
    except Exception as e:
        logging.error(f"チェックリスト作成状況ファイルの読み込み中にエラーが発生しました: {e}")
        return overall_checklist_df

    # overall_checklist_dfの行ごとに処理を行う
    for index, row in overall_checklist_df.iterrows():
        club_name = str(row['クラブ名']).strip()
        apried_date_str = str(row.get('受付日時')).strip()
        
        # ここで小数点以下を除去
        if '.' in apried_date_str:
            apried_date_str = apried_date_str.split('.')[0]
            
        # 処理開始のメッセージを表示
        logging.info(f"クラブ名: {club_name} の人間によるチェック結果の反映を開始します")
        
        # 人間によるチェックが既に反映済みかを確認（書類チェック結果で判断）
        document_check_result = overall_checklist_df.loc[index, '書類チェック結果']
        document_check_update_time = overall_checklist_df.loc[index, '書類チェック更新日時']
        
        # チェックリスト作成状況から該当クラブの人間チェック状況を取得
        human_check_mask = (
            (checklist_status_df['クラブ名'] == club_name) & 
            (checklist_status_df['申請日時'].astype(str).str.strip() == apried_date_str)
        )
        
        if not human_check_mask.any():
            logging.warning(f"クラブ '{club_name}' のチェックリスト作成状況が見つかりません")
            continue
            
        # 該当する行を取得
        human_check_row = checklist_status_df[human_check_mask].iloc[0]
        human_check_status = human_check_row.get('書類チェック', '')
        human_check_update_time = human_check_row.get('書類チェック更新時間', '')
        
        # 人間によるチェックが完了しているかを確認
        if pd.isna(human_check_status) or str(human_check_status).strip() == '':
            logging.info(f"クラブ '{club_name}' の人間によるチェックはまだ実行されていません")
            continue
        
        # 人間によるチェック更新時間が空でないかを確認
        if pd.isna(human_check_update_time) or str(human_check_update_time).strip() == '':
            logging.info(f"クラブ '{club_name}' の人間によるチェック更新時間が設定されていません")
            continue
            
        # 既に総合チェックリストに人間チェック結果が反映されているかを確認
        # 書類チェック更新日時が人間チェック更新時間以降であれば、既に反映済みと判断
        try:
            if pd.notna(document_check_update_time) and str(document_check_update_time).strip() != '':
                overall_update_time = pd.to_datetime(str(document_check_update_time))
                human_update_time = pd.to_datetime(str(human_check_update_time))
                
                if overall_update_time >= human_update_time:
                    logging.info(f"クラブ '{club_name}' の人間によるチェック結果は既に総合チェックリストに反映済みです")
                    continue
        except Exception as e:
            logging.warning(f"日時の比較中にエラーが発生しました: {e}")
        
        # 人間によるチェック結果を総合チェックリストに反映
        try:
            jst_now = datetime.now(timezone(timedelta(hours=9)))
            update_datetime = jst_now.strftime('%Y-%m-%d %H:%M:%S')
            
            # 人間によるチェック結果を解析
            human_check_errors = {}
            if 'info' in str(human_check_status) and '書類のチェックで問題は見つかりませんでした' in str(human_check_status):
                # 問題がない場合
                human_check_result = "人間チェック完了"
            else:
                # 問題がある場合
                human_check_result = f"人間チェック結果: {human_check_status}"
            
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
