import pandas as pd
import sys
import os

# パスを追加
sys.path.append(r'e:\oasobi\deportare_registro')

from src.core.load_latest_club_data import load_latest_club_reception_data, get_club_data_by_name_and_date
from src.checklist.automation.check_functions import check_managers

def test_check_managers():
    print("=== マネジャーチェック関数のテスト ===")
    
    # 統合されたクラブ情報付き受付データを読み込み
    print("1. データの読み込み...")
    integrated_club_data = load_latest_club_reception_data()
    if integrated_club_data is None:
        print("ERROR: 統合されたクラブ情報付き受付データの読み込みに失敗しました")
        return
    
    # テスト用のクラブ名
    test_club_name = "日本橋クラブ"
    test_date = "2025-06-05 17:29:33.531"
    
    print(f"2. テスト対象: {test_club_name}, {test_date}")
    
    # 該当行を取得
    target_row = get_club_data_by_name_and_date(integrated_club_data, test_club_name, test_date)
    
    if target_row.empty:
        print(f"ERROR: 該当クラブのデータが見つかりません")
        return
    
    print(f"対象行数: {len(target_row)}")
    
    # check_managers関数をテスト
    print(f"\n3. check_managers関数の実行...")
    result = check_managers(target_row)
    
    print(f"結果: {result}")
    
    if not result:
        print("✅ マネジャーチェックが正常に通りました（エラーなし）")
    else:
        print("❌ マネジャーチェックでエラーが発生しました")

if __name__ == "__main__":
    test_check_managers()
