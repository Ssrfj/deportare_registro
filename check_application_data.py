#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
申請データの内容を確認するスクリプト
"""

import pandas as pd
import os

def check_application_data():
    """申請データの内容を確認"""
    
    # 申請データファイルのパス
    file_path = r"e:\oasobi\deportare_registro\data\applications\申請データ_20250401000000.xlsx"
    
    if not os.path.exists(file_path):
        print(f"ファイルが見つかりません: {file_path}")
        return
    
    try:
        # Excelファイルを読み込み
        df = pd.read_excel(file_path)
        
        print(f"申請データファイル: {file_path}")
        print(f"総行数: {len(df)}")
        print(f"列数: {len(df.columns)}")
        print()
        
        # 列名を表示
        print("=== 列名 ===")
        for i, col in enumerate(df.columns):
            print(f"{i+1:2d}. {col}")
        print()
        
        # 申請_クラブ名_選択の内容を確認
        if '申請_クラブ名_選択' in df.columns:
            print("=== 申請_クラブ名_選択の分布 ===")
            value_counts = df['申請_クラブ名_選択'].value_counts()
            print(value_counts)
            print()
            
            # 「この中にない」の件数
            kono_naka_ni_nai_count = len(df[df['申請_クラブ名_選択'] == 'この中にない'])
            print(f"「この中にない」のクラブ数: {kono_naka_ni_nai_count}")
            print(f"「この中にない」以外のクラブ数: {len(df) - kono_naka_ni_nai_count}")
            print()
            
            # 「この中にない」のクラブ名を表示（最初の10件）
            kono_naka_ni_nai_clubs = df[df['申請_クラブ名_選択'] == 'この中にない']
            if len(kono_naka_ni_nai_clubs) > 0:
                print("=== 「この中にない」のクラブ（最初の10件） ===")
                if 'クラブ名' in df.columns:
                    for i, club_name in enumerate(kono_naka_ni_nai_clubs['クラブ名'].head(10)):
                        print(f"{i+1:2d}. {club_name}")
                elif '申請_クラブ名_新設' in df.columns:
                    for i, club_name in enumerate(kono_naka_ni_nai_clubs['申請_クラブ名_新設'].head(10)):
                        print(f"{i+1:2d}. {club_name}")
                else:
                    print("クラブ名の列が見つかりません")
        else:
            print("「申請_クラブ名_選択」列が見つかりません")
        
        # クラブ名列の確認
        club_name_columns = [col for col in df.columns if 'クラブ名' in col]
        print(f"\n=== クラブ名関連の列 ===")
        for col in club_name_columns:
            print(f"- {col}")
            non_null_count = df[col].notna().sum()
            print(f"  非空値の数: {non_null_count}")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    check_application_data()
