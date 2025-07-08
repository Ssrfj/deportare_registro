import pandas as pd
import sys
import os

# パスを追加
sys.path.append(r'e:\oasobi\deportare_registro')

from src.core.load_latest_club_data import load_latest_club_reception_data, get_club_data_by_name_and_date

def test_member_number_data():
    print("=== 会員数データの型確認テスト ===")
    
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
    
    # 会員数関連の列をチェック
    member_columns = [
        '申請_会員_未就_男_数', '申請_会員_未就_女_数', '申請_会員_未就_不_数',
        '申請_会員_小_男_数', '申請_会員_小_女_数', '申請_会員_小_不_数',
        '申請_会員_中_男_数', '申請_会員_中_女_数', '申請_会員_中_不_数'
    ]
    
    print(f"\n3. 会員数データの詳細確認:")
    for col in member_columns[:5]:  # 最初の5列だけ確認
        if col in target_row.columns:
            value = target_row[col].iloc[0]
            print(f"  {col}:")
            print(f"    値: {value}")
            print(f"    型: {type(value)}")
            print(f"    NaN?: {pd.isna(value)}")
            print(f"    int/float?: {isinstance(value, (int, float))}")
            print(f"    文字列?: {isinstance(value, str)}")
            if isinstance(value, str):
                print(f"    文字列の内容: '{value}'")
                try:
                    as_int = int(value)
                    print(f"    int変換可能: {as_int}")
                except:
                    print(f"    int変換不可")
                try:
                    as_float = float(value)
                    print(f"    float変換可能: {as_float}")
                except:
                    print(f"    float変換不可")
            print()

if __name__ == "__main__":
    test_member_number_data()
