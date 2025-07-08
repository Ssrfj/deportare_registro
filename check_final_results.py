#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
担当者登録基準最終チェック結果の確認スクリプト
"""

import os
import glob
import pandas as pd
from pathlib import Path

def check_final_results():
    """最新の総合チェックリストファイルから「担当者登録基準最終チェック結果」列を確認"""
    
    # 出力ディレクトリのパス
    output_dir = Path("output/R7_登録受付処理/受付内容チェック/総合チェックリスト")
    
    if not output_dir.exists():
        print(f"出力ディレクトリが見つかりません: {output_dir}")
        return
    
    # Excelファイルを探す
    excel_files = list(output_dir.glob("*.xlsx"))
    
    if not excel_files:
        print(f"Excelファイルが見つかりません: {output_dir}")
        return
    
    # 最新のファイルを選択
    latest_file = max(excel_files, key=os.path.getmtime)
    print(f"チェック対象ファイル: {latest_file}")
    
    try:
        # Excelファイルを読み込み
        df = pd.read_excel(latest_file, engine='openpyxl')
        
        # 列名を確認
        print(f"\nファイル内の列数: {len(df.columns)}")
        print("列名一覧:")
        for i, col in enumerate(df.columns):
            print(f"  {i+1:2d}: {col}")
        
        # 「担当者登録基準最終チェック結果」列を探す
        target_column = '担当者登録基準最終チェック結果'
        
        if target_column not in df.columns:
            print(f"\n「{target_column}」列が見つかりません。")
            # 類似の列名を探す
            similar_cols = [col for col in df.columns if '担当者' in col or '最終' in col]
            if similar_cols:
                print("類似の列名:")
                for col in similar_cols:
                    print(f"  - {col}")
            return
        
        # 結果を分析
        final_results = df[target_column]
        total_clubs = len(final_results)
        
        print(f"\n=== 分析結果 ===")
        print(f"総クラブ数: {total_clubs}")
        
        # NaN値（空のセル）をチェック
        nan_count = final_results.isna().sum()
        if nan_count > 0:
            print(f"空のセル数: {nan_count}")
        
        # 有効な値のみを取得（NaNを除く）
        valid_results = final_results.dropna()
        
        # ユニークな値を確認
        unique_values = valid_results.unique()
        print(f"\n最終チェック結果の値の種類:")
        for value in sorted(unique_values):
            count = (valid_results == value).sum()
            print(f"  '{value}': {count}件")
        
        # 「未チェック」の数をカウント
        unchecked_count = (valid_results == '未チェック').sum()
        print(f"\n「未チェック」の数: {unchecked_count}")
        print(f"全て「未チェック」かどうか: {unchecked_count == len(valid_results)}")
        
        # 「未チェック」以外の値がある場合、詳細を表示
        if unchecked_count < len(valid_results):
            print(f"\n「未チェック」以外の値を持つクラブ:")
            non_unchecked = df[df[target_column] != '未チェック']
            for idx, row in non_unchecked.iterrows():
                club_name = row.get('クラブ名', f'行{idx+1}')
                result_value = row[target_column]
                print(f"  {club_name}: '{result_value}'")
        
    except Exception as e:
        print(f"ファイル読み込みエラー: {e}")
        print(f"ファイルパス: {latest_file}")

if __name__ == "__main__":
    check_final_results()
