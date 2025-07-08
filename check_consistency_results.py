#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os
import sys

def check_consistency_results():
    """最新の総合チェックリストファイルから「書類間チェック結果」列を確認"""
    
    # 総合チェックリストフォルダのパス
    output_path = r"e:\oasobi\deportare_registro\output\R7_登録受付処理\受付内容チェック\総合チェックリスト"
    
    if not os.path.exists(output_path):
        print(f"出力パスが存在しません: {output_path}")
        return
    
    # 総合チェックリストファイルを検索
    files = [f for f in os.listdir(output_path) if f.startswith('総合チェックリスト_') and f.endswith('.xlsx')]
    
    if not files:
        print("総合チェックリストファイルが見つかりません")
        return
    
    # 最新のファイルを取得（ファイル名でソート）
    files.sort(reverse=True)
    latest_file = os.path.join(output_path, files[0])
    
    print(f"チェック対象ファイル: {latest_file}")
    
    try:
        # Excelファイルを読み込み
        df = pd.read_excel(latest_file, engine='openpyxl')
        
        # 列名を確認
        print(f"\nファイル内の列数: {len(df.columns)}")
        
        # 「書類間チェック結果」列を探す
        target_column = '書類間チェック結果'
        if target_column not in df.columns:
            print(f"\n「{target_column}」列が見つかりません。")
            # 類似の列名を探す
            similar_cols = [col for col in df.columns if '書類間' in col or 'チェック結果' in col]
            if similar_cols:
                print("類似の列名:")
                for col in similar_cols:
                    print(f"  - {col}")
            return
        
        # 結果を分析
        consistency_results = df[target_column]
        total_clubs = len(consistency_results)
        
        print(f"\n=== 分析結果 ===")
        print(f"総クラブ数: {total_clubs}")
        
        # NaN値（空のセル）をチェック
        nan_count = consistency_results.isna().sum()
        if nan_count > 0:
            print(f"空のセル数: {nan_count}")
        
        # 有効な値のみを取得（NaNを除く）
        valid_results = consistency_results.dropna()
        
        # ユニークな値を確認
        unique_values = valid_results.unique()
        print(f"\n書類間チェック結果の値の種類:")
        for value in sorted(unique_values):
            count = (valid_results == value).sum()
            print(f"  '{value}': {count}件")
        
        # 特定の値をカウント
        unchecked_count = (valid_results == '未チェック').sum()
        checked_count = (valid_results == 'チェック済み').sum()
        error_count = total_clubs - unchecked_count - checked_count - nan_count
        
        print(f"\n=== サマリー ===")
        print(f"「未チェック」: {unchecked_count}件")
        print(f"「チェック済み」: {checked_count}件")
        print(f"エラーあり: {error_count}件")
        print(f"空/その他: {nan_count}件")
        
        # エラーがある場合の詳細表示（最初の5件のみ）
        if error_count > 0:
            print(f"\nエラーがあるクラブ（最初の5件）:")
            error_clubs = df[(~df[target_column].isna()) & 
                            (df[target_column] != '未チェック') & 
                            (df[target_column] != 'チェック済み')]
            
            for idx, row in error_clubs.head(5).iterrows():
                club_name = row.get('クラブ名', f'行{idx+1}')
                result_value = row[target_column]
                print(f"  - {club_name}: {result_value}")
            
            if len(error_clubs) > 5:
                print(f"  ... 他 {len(error_clubs) - 5}件")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_consistency_results()
