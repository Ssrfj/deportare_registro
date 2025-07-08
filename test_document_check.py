#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import sys
import os

# パスの設定
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.checklist.automation.documents_check_functions import (
    check_document_1, check_document_2_1, check_document_2_2, check_document_3,
    check_document_4, check_document_5_plan, check_document_5_budget,
    check_document_6_report, check_document_6_financial_statements,
    check_document_7, check_document_8, check_document_9, check_document_10
)
from src.core.load_latest_club_data import load_latest_club_reception_data, get_club_data_by_name_and_date

def test_document_checks():
    print("=== 書類チェック関数のテスト ===")
    
    # 統合されたクラブ情報付き受付データを読み込み
    print("統合されたクラブ情報付き受付データを読み込みます...")
    integrated_club_data = load_latest_club_reception_data()
    
    if integrated_club_data is None:
        print("エラー: 統合されたクラブ情報付き受付データの読み込みに失敗しました")
        return
    
    print(f"データ行数: {len(integrated_club_data)}")
    print(f"利用可能なクラブ: {integrated_club_data['クラブ名'].unique().tolist()}")
    print(f"カラム名: {integrated_club_data.columns.tolist()}")
    
    # テスト用のクラブを選択（最初の有効なクラブ）
    if len(integrated_club_data) == 0:
        print("エラー: データが空です")
        return
    
    test_club_name = integrated_club_data['クラブ名'].iloc[0]
    test_date = integrated_club_data['申請_タイムスタンプ'].iloc[0]
    
    print(f"\nテスト対象クラブ: {test_club_name}")
    print(f"受付日時: {test_date}")
    
    # 該当行を取得
    target_row = get_club_data_by_name_and_date(integrated_club_data, test_club_name, str(test_date))
    
    if target_row.empty:
        print("エラー: 該当行が見つかりません")
        return
    
    print(f"対象行のデータ取得成功")
    
    # 各書類チェック関数をテスト
    check_functions = [
        ("書類01: クラブ基本情報", check_document_1),
        ("書類02_1: 役員名簿", check_document_2_1),
        ("書類02_2: コーチ名簿", check_document_2_2),
        ("書類03: 会員名簿", check_document_3),
        ("書類04: 規約", check_document_4),
        ("書類05: 事業計画書", check_document_5_plan),
        ("書類05: 予算書", check_document_5_budget),
        ("書類06: 事業報告書", check_document_6_report),
        ("書類06: 財務諸表", check_document_6_financial_statements),
        ("書類07: チェックリスト", check_document_7),
        ("書類08: 一覧表", check_document_8),
        ("書類09: 承認印申請書", check_document_9),
        ("書類10: 説明書", check_document_10)
    ]
    
    all_document_errors = {}
    
    for doc_name, check_function in check_functions:
        try:
            print(f"\n--- {doc_name} ---")
            result = check_function(target_row)
            
            if result:
                print(f"エラー検出: {result}")
                all_document_errors.update(result)
            else:
                print("チェック済み（エラーなし）")
                
        except Exception as e:
            print(f"エラー: {doc_name} のチェック中にエラーが発生しました: {e}")
    
    print(f"\n=== 統合されたエラー辞書 ===")
    if all_document_errors:
        print(f"エラー総数: {len(all_document_errors)}")
        print(f"統合結果: {all_document_errors}")
        print(f"文字列形式: {str(all_document_errors)}")
    else:
        print("エラーなし: 全書類チェック済み")

if __name__ == "__main__":
    test_document_checks()
