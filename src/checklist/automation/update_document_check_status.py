def update_document_check_status(overall_checklist_df, checklist_file_path, club_reception_df, latest_reception_data_date):
    import os
    import pandas as pd
    import logging
    from datetime import datetime, timezone, timedelta
    from src.core.setting_paths import overall_checklist_folder_path
    from src.core.utils import get_jst_now, ensure_date_string
    from src.core.load_latest_club_data import load_latest_club_reception_data, get_club_data_by_name_and_date
    from src.checklist.automation.documents_check_functions import (
        check_document_1, check_document_2_1, check_document_2_2, check_document_3,
        check_document_4, check_document_5_plan, check_document_5_budget,
        check_document_6_report, check_document_6_financial_statements,
        check_document_7, check_document_8, check_document_9, check_document_10
    )
    
    # ロギングとフォルダ設定は main.py で実行済み

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
            logging.warning(f"'チェックリスト作成日時' カラムが存在しません。rowのカラム: {row.index.tolist()}")
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
        logging.info(f"クラブ名: {club_name} の書類チェックを開始します")
        
        # 統合されたクラブ情報付き受付データから該当行を取得
        target_row = get_club_data_by_name_and_date(integrated_club_data, club_name, apried_date_str)
        
        if target_row.empty:
            logging.warning(f"統合データに該当クラブのデータが見つかりません: {club_name}, {apried_date_str}")
            continue
        
        # 書類チェックが既に実行済みかを確認（書類チェック結果で判断）
        document_check_result = overall_checklist_df.loc[index, '書類チェック結果']
        if pd.notna(document_check_result) and str(document_check_result).strip() not in ['', '未チェック']:
            logging.info(f"クラブ '{club_name}' の申請日時'{apried_date_str}'の申請は書類チェック済みです（結果: {document_check_result}）。スキップします。")
            continue
        else:
            logging.info(f"クラブ '{club_name}' の申請日時'{apried_date_str}'の申請は書類チェックを実行します。")
        
        jst_now = datetime.now(timezone(timedelta(hours=9)))
        update_datetime = jst_now.strftime('%Y-%m-%d %H:%M:%S')
        
        overall_checklist_df['クラブ名'] = overall_checklist_df['クラブ名'].astype(str).str.strip()
        overall_checklist_df['受付日時'] = overall_checklist_df['受付日時'].astype(str).str.strip()
        
        # 各書類チェック関数を実行して結果を統合
        try:
            # 全ての書類チェック結果を集約する辞書
            all_document_errors = {}
            
            # 書類01: クラブ基本情報
            doc1_result = check_document_1(target_row)
            if doc1_result:
                all_document_errors.update(doc1_result)
            
            # 書類02_1: 役員名簿
            doc2_1_result = check_document_2_1(target_row)
            if doc2_1_result:
                all_document_errors.update(doc2_1_result)
            
            # 書類02_2: コーチ名簿
            doc2_2_result = check_document_2_2(target_row)
            if doc2_2_result:
                all_document_errors.update(doc2_2_result)
            
            # 書類03: 会員名簿
            doc3_result = check_document_3(target_row)
            if doc3_result:
                all_document_errors.update(doc3_result)
            
            # 書類04: 規約
            doc4_result = check_document_4(target_row)
            if doc4_result:
                all_document_errors.update(doc4_result)
            
            # 書類05: 事業計画書
            doc5_plan_result = check_document_5_plan(target_row)
            if doc5_plan_result:
                all_document_errors.update(doc5_plan_result)
            
            # 書類05: 予算書
            doc5_budget_result = check_document_5_budget(target_row)
            if doc5_budget_result:
                all_document_errors.update(doc5_budget_result)
            
            # 書類06: 事業報告書
            doc6_report_result = check_document_6_report(target_row)
            if doc6_report_result:
                all_document_errors.update(doc6_report_result)
            
            # 書類06: 財務諸表
            doc6_financial_result = check_document_6_financial_statements(target_row)
            if doc6_financial_result:
                all_document_errors.update(doc6_financial_result)
            
            # 書類07: チェックリスト
            doc7_result = check_document_7(target_row)
            if doc7_result:
                all_document_errors.update(doc7_result)
            
            # 書類08: 一覧表
            doc8_result = check_document_8(target_row)
            if doc8_result:
                all_document_errors.update(doc8_result)
            
            # 書類09: 承認印申請書
            doc9_result = check_document_9(target_row)
            if doc9_result:
                all_document_errors.update(doc9_result)
            
            # 書類10: 説明書
            doc10_result = check_document_10(target_row)
            if doc10_result:
                all_document_errors.update(doc10_result)
            
            # 統合されたエラー辞書を文字列として書類チェック結果に設定
            if all_document_errors:
                # エラーがある場合は詳細なエラー辞書を文字列として保存
                overall_checklist_df.loc[index, '書類チェック結果'] = str(all_document_errors)
            else:
                # エラーがない場合は「チェック済み」を設定
                overall_checklist_df.loc[index, '書類チェック結果'] = "チェック済み"
            overall_checklist_df.loc[index, '書類チェック更新日時'] = update_datetime
            
            logging.info(f"クラブ名: {club_name} の書類チェックが完了しました")
            
        except Exception as e:
            logging.error(f"クラブ '{club_name}' の書類チェック中にエラーが発生しました: {e}")
            continue
    
    logging.info("全てのクラブの書類チェックが完了しました。")

    # 総合チェックリストのファイルを保存（ファイル名は「総合チェックリスト_受付{YYYYMMDDHHMMSS}_更新{YYYYMMDDHHMMSS}.xlsx」）
    logging.info("総合チェックリストのファイルを保存します")
    now_jst = get_jst_now()
    latest_reception_data_date_str = ensure_date_string(latest_reception_data_date)
    overall_checklist_file_name = f'総合チェックリスト_受付{latest_reception_data_date_str}_更新{now_jst.strftime("%Y%m%d%H%M%S")}.xlsx'
    overall_checklist_file_path = os.path.join(overall_checklist_folder_path, overall_checklist_file_name)
    overall_checklist_df.to_excel(overall_checklist_file_path, index=False)
    logging.info(f"総合チェックリストのファイルを保存しました: {overall_checklist_file_path}")
    logging.info("書類チェックが完了しました")
    
    return overall_checklist_df
    return overall_checklist_df, checklist_file_path
