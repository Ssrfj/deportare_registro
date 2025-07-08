#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 新しい書類チェック関数（書類4以降）

import pandas as pd
import logging
from src.folder_management.make_folders import setup_logging, create_folders

def check_document_4(row):
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
                error_dict['e_d_4_001'] = '書類4（役員名簿）のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row

        # 書類4（役員名簿）: 基本的な書類提出状況チェック
        # 書類ファイルの提出確認
        document_file = row_data.get('申請_役員名簿_書類(選択時必須)')
        if pd.isna(document_file) or str(document_file).strip() == '':
            error_dict['e_d_4_001'] = '書類4（役員名簿）: 書類が提出されていません'

        # 提出有無の確認
        submission_status = row_data.get('申請_役員名簿_提出有無')
        if pd.isna(submission_status) or str(submission_status).strip() == '':
            error_dict['e_d_4_002'] = '書類4（役員名簿）: 提出有無が未選択です'

    except Exception as e:
        logging.error(f"書類4（役員名簿）のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_4_099'] = f'書類4（役員名簿）のチェック状況の反映中にエラーが発生しました: {str(e)}'      
    return error_dict


def check_document_5_plan(row):
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
                error_dict['e_d_5_p_001'] = '書類5（計画）のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row

        # 書類5（計画）: 基本的な書類提出状況チェック
        # 書類ファイルの提出確認
        document_file = row_data.get('申請_事業計画_書類')
        if pd.isna(document_file) or str(document_file).strip() == '':
            error_dict['e_d_5_p_001'] = '書類5（計画）: 書類が提出されていません'

        # 決議機関名称の確認
        decision_body = row_data.get('申請_事業計画_決議機関名称')
        if pd.isna(decision_body) or str(decision_body).strip() == '':
            error_dict['e_d_5_p_002'] = '書類5（計画）: 決議機関名称が未入力です'

        # 決議日の確認
        decision_date = row_data.get('申請_事業計画_決議日')
        if pd.isna(decision_date) or str(decision_date).strip() == '':
            error_dict['e_d_5_p_003'] = '書類5（計画）: 決議日が未入力です'

    except Exception as e:
        logging.error(f"書類5（計画）のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_5_p_099'] = f'書類5（計画）のチェック状況の反映中にエラーが発生しました: {str(e)}'
    return error_dict


def check_document_5_budget(row):
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
                error_dict['e_d_5_b_001'] = '書類5（予算）のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row

        # 書類5（予算）: 基本的な書類提出状況チェック
        # 書類ファイルの提出確認
        document_file = row_data.get('申請_予算_書類')
        if pd.isna(document_file) or str(document_file).strip() == '':
            error_dict['e_d_5_b_001'] = '書類5（予算）: 書類が提出されていません'

        # 決議機関名称の確認
        decision_body = row_data.get('申請_予算_決議機関名称')
        if pd.isna(decision_body) or str(decision_body).strip() == '':
            error_dict['e_d_5_b_002'] = '書類5（予算）: 決議機関名称が未入力です'

        # 決議日の確認
        decision_date = row_data.get('申請_予算_決議日')
        if pd.isna(decision_date) or str(decision_date).strip() == '':
            error_dict['e_d_5_b_003'] = '書類5（予算）: 決議日が未入力です'

    except Exception as e:
        logging.error(f"書類5（予算）のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_5_b_099'] = f'書類5（予算）のチェック状況の反映中にエラーが発生しました: {str(e)}'
    return error_dict


def check_document_6_report(row):
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
                error_dict['e_d_6_r_001'] = '書類6（事業報告）のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row

        # 書類6（事業報告）: 基本的な書類提出状況チェック
        # 提出有無の確認
        submission_status = row_data.get('申請_事業報告_提出有無')
        if pd.isna(submission_status) or str(submission_status).strip() == '':
            error_dict['e_d_6_r_001'] = '書類6（事業報告）: 提出有無が未選択です'
        elif str(submission_status).strip().lower() in ['1', 'true', 'yes', '提出']:
            # 提出する場合は書類ファイルをチェック
            document_file = row_data.get('申請_事業報告_事業報告_書類(選択時必須)')
            if pd.isna(document_file) or str(document_file).strip() == '':
                error_dict['e_d_6_r_002'] = '書類6（事業報告）: 書類が提出されていません'

    except Exception as e:
        logging.error(f"書類6（事業報告）のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_6_r_099'] = f'書類6（事業報告）のチェック状況の反映中にエラーが発生しました: {str(e)}'
    return error_dict


def check_document_6_financial_statements(row):
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
                error_dict['e_d_6_f_001'] = '書類6（決算）のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row

        # 書類6（決算）: 基本的な書類提出状況チェック
        # 提出有無の確認
        submission_status = row_data.get('申請_決算_提出有無')
        if pd.isna(submission_status) or str(submission_status).strip() == '':
            error_dict['e_d_6_f_001'] = '書類6（決算）: 提出有無が未選択です'
        elif str(submission_status).strip().lower() in ['1', 'true', 'yes', '提出']:
            # 提出する場合は書類ファイルをチェック
            document_file = row_data.get('申請_決算_書類(選択時必須)')
            if pd.isna(document_file) or str(document_file).strip() == '':
                error_dict['e_d_6_f_002'] = '書類6（決算）: 書類が提出されていません'

    except Exception as e:
        logging.error(f"書類6（決算）のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_6_f_099'] = f'書類6（決算）のチェック状況の反映中にエラーが発生しました: {str(e)}'
    return error_dict


def check_document_7(row):
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
                error_dict['e_d_7_001'] = '書類7（自己点検）のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row

        # 書類7（自己点検）: 基本的な書類提出状況チェック
        # 書類ファイルの提出確認
        document_file = row_data.get('申請_自己点検シート_書類')
        if pd.isna(document_file) or str(document_file).strip() == '':
            error_dict['e_d_7_001'] = '書類7（自己点検）: 書類が提出されていません'

    except Exception as e:
        logging.error(f"書類7（自己点検）のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_7_099'] = f'書類7（自己点検）のチェック状況の反映中にエラーが発生しました: {str(e)}'      
    return error_dict


def check_document_8(row):
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
                error_dict['e_d_8_001'] = '書類8（議事録）のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row

        # 書類8（議事録）: 基本的な書類提出状況チェック
        # 議事録関連のファイルが複数存在するため、関連するファイルをチェック
        
        # 事業計画議事録
        plan_minutes = row_data.get('申請_事業計画_議事録_書類')
        if pd.isna(plan_minutes) or str(plan_minutes).strip() == '':
            error_dict['e_d_8_001'] = '書類8（議事録）: 事業計画議事録が提出されていません'

        # 予算議事録
        budget_minutes = row_data.get('申請_予算_議事録_書類')
        if pd.isna(budget_minutes) or str(budget_minutes).strip() == '':
            error_dict['e_d_8_002'] = '書類8（議事録）: 予算議事録が提出されていません'

    except Exception as e:
        logging.error(f"書類8（議事録）のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_8_099'] = f'書類8（議事録）のチェック状況の反映中にエラーが発生しました: {str(e)}'        
    return error_dict


def check_document_9(row):
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
                error_dict['e_d_9_001'] = '書類9（自己説明）のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row

        # 書類9（自己説明）: 基本的な書類提出状況チェック
        # 書類ファイルの提出確認
        document_file = row_data.get('申請_自己説明_書類')
        if pd.isna(document_file) or str(document_file).strip() == '':
            error_dict['e_d_9_001'] = '書類9（自己説明）: 書類が提出されていません'

    except Exception as e:
        logging.error(f"書類9（自己説明）のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_9_099'] = f'書類9（自己説明）のチェック状況の反映中にエラーが発生しました: {str(e)}'      
    return error_dict


def check_document_10(row):
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
                error_dict['e_d_10_001'] = '書類10（届出）のデータが見つかりません'
                return error_dict
            row_data = row.iloc[0]
        else:
            row_data = row

        # 書類10（届出）: 基本的な書類提出状況チェック
        # 書類ファイルの提出確認
        document_file = row_data.get('申請_届出_書類_(選択時必須)')
        if pd.isna(document_file) or str(document_file).strip() == '':
            error_dict['e_d_10_001'] = '書類10（届出）: 書類が提出されていません'

    except Exception as e:
        logging.error(f"書類10（届出）のチェック状況の反映中にエラーが発生しました: {e}")
        error_dict['e_d_10_099'] = f'書類10（届出）のチェック状況の反映中にエラーが発生しました: {str(e)}'        
    return error_dict
