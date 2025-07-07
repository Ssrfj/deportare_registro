def auto_check(club_reception_df, overall_checklist_df, latest_reception_data_date):
    import os
    import pandas as pd
    import logging
    from datetime import datetime, timezone, timedelta
    from src.folder_management.make_folders import setup_logging, create_folders
    from src.core.setting_paths import overall_checklist_folder_path
    from src.core.utils import get_jst_now, ensure_date_string
    from src.core.load_latest_club_data import load_latest_club_reception_data, get_club_data_by_name_and_date
    from src.checklist.automation.check_functions import (
        check_must_columns, check_submitting_now, check_club_location, check_phone_number,
        check_fax_number, check_reception_type, check_standard_compliance, check_number_of_members,
        check_number_of_disciplines, check_coaches, check_managers, check_rule_revision,
        check_rule_submission, check_officer_list_submission, check_business_plan_submission,
        check_budget_submission, check_business_report_submission, check_financial_statement_submission,
        check_checklist_submission, check_self_explanation_submission
    )

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
        return overall_checklist_df, None

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
            # チェックリスト作成日時がない場合は、受付日時を使用
            checklist_created_date_str = apried_date_str
        else:
            checklist_created_date_str = str(row.get('チェックリスト作成日時')).strip()
            # ここで小数点以下を除去
            if '.' in checklist_created_date_str:
                checklist_created_date_str = checklist_created_date_str.split('.')[0]
        # 処理開始のメッセージを表示
        logging.info(f"クラブ名: {club_name} の自動チェックを開始します")
        
        # 統合されたクラブ情報付き受付データから該当行を取得
        target_row = get_club_data_by_name_and_date(integrated_club_data, club_name, apried_date_str)
        
        if target_row.empty:
            logging.warning(f"統合データに該当クラブのデータが見つかりません: {club_name}, {apried_date_str}")
            continue
        
        # 自動チェックが既に実行済みかを確認（総合チェックリストで判断）
        if pd.notna(overall_checklist_df.loc[index, '自動チェック更新日時']) and overall_checklist_df.loc[index, '自動チェック更新日時'] != '':
            logging.info(f"クラブ '{club_name}' の申請日時'{apried_date_str}'の申請は自動チェック済みです。スキップします。")
            continue
        else:
            logging.info(f"クラブ '{club_name}' の申請日時'{apried_date_str}'の申請は自動チェックを実行します。")
            error_dict = {}
            jst_now = datetime.now(timezone(timedelta(hours=9)))
            today_date = jst_now.date()
        
        overall_checklist_df['クラブ名'] = overall_checklist_df['クラブ名'].astype(str).str.strip()
        overall_checklist_df['受付日時'] = overall_checklist_df['受付日時'].astype(str).str.strip()
        
        # 各チェック関数に target_row を渡す
        error_dict.update(check_must_columns(target_row))
        error_dict.update(check_submitting_now(target_row))
        error_dict.update(check_club_location(target_row))
        error_dict.update(check_phone_number(target_row))
        error_dict.update(check_fax_number(target_row))
        error_dict.update(check_reception_type(target_row, overall_checklist_df, club_name))
        error_dict.update(check_standard_compliance(target_row))
        error_dict.update(check_number_of_members(target_row))
        error_dict.update(check_number_of_disciplines(target_row))
        # error_dict.update(check_coaches(reception_row)) # 現段階では不要
        error_dict.update(check_managers(target_row))
        error_dict.update(check_rule_revision(target_row))
        error_dict.update(check_rule_submission(target_row))
        error_dict.update(check_officer_list_submission(target_row))
        error_dict.update(check_business_plan_submission(target_row))
        error_dict.update(check_budget_submission(target_row))
        error_dict.update(check_business_report_submission(target_row, today_date))
        error_dict.update(check_financial_statement_submission(target_row, today_date))
        error_dict.update(check_checklist_submission(target_row))
        error_dict.update(check_self_explanation_submission(target_row))

        if not error_dict:
            error_dict['info'] = '自動チェックで問題は見つかりませんでした。'
        else:
            logging.warning('自動チェックで問題が見つかりました。')

        logging.info(f"チェック結果: {error_dict}")

        # 総合チェックリストに結果を反映
        overall_checklist_df.loc[index, '自動チェック結果'] = 'チェック済み' if not error_dict or 'info' in error_dict else 'エラーあり'
        overall_checklist_df.loc[index, '自動チェック更新日時'] = datetime.now(timezone(timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S')

        logging.info(f"クラブ名: {club_name} の自動チェックが完了しました\n")
    logging.info("全てのクラブの自動チェックが完了しました。")

    # 総合チェックリストのファイルを保存（ファイル名は「総合チェックリスト_受付{YYYYMMDDHHMMSS}_更新{YYYYMMDDHHMMSS}.xlsx」）
    logging.info("総合チェックリストのファイルを保存します")
    now_jst = get_jst_now()
    latest_reception_data_date_str = ensure_date_string(latest_reception_data_date)
    overall_checklist_file_name = f'総合チェックリスト_受付{latest_reception_data_date_str}_更新{now_jst.strftime("%Y%m%d%H%M%S")}.xlsx'
    overall_checklist_file_path = os.path.join(overall_checklist_folder_path, overall_checklist_file_name)
    overall_checklist_df.to_excel(overall_checklist_file_path, index=False)
    logging.info(f"総合チェックリストのファイルを保存しました: {overall_checklist_file_path}")
    logging.info("自動チェックが完了しました")
    return overall_checklist_df, overall_checklist_file_path