import pandas as pd
import os

# 処理済み受付データファイルのパス
file_path = "output/R7_登録受付処理/処理済み受付データ/処理済み受付データ_受付20250401000000_処理20250702171108.xlsx"

try:
    # ファイルを読み込み
    df = pd.read_excel(file_path)
    
    print("=== 処理済み受付データファイルの情報 ===")
    print(f"ファイルパス: {file_path}")
    print(f"行数: {len(df)}")
    print(f"列数: {len(df.columns)}")
    print("\n=== 列名一覧 ===")
    for i, col in enumerate(df.columns):
        print(f"{i+1}. {col}")
    
    print("\n=== 最初の3行のデータ ===")
    print(df.head(3).to_string())
    
    # クラブ名に関連する列を検索
    club_columns = [col for col in df.columns if 'クラブ' in col or 'club' in col.lower()]
    if club_columns:
        print(f"\n=== クラブ名関連の列 ===")
        for col in club_columns:
            print(f"- {col}")
    
except Exception as e:
    print(f"エラー: {e}")
