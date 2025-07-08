#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
各処理段階でのクラブ数の変化を追跡するスクリプト
"""

import pandas as pd
import os
from pathlib import Path

def track_club_count_changes():
    """各処理段階でのクラブ数の変化を追跡"""
    
    print("=== クラブ数の変化を追跡 ===\n")
    
    # 1. 元の申請データ
    application_file = r"e:\oasobi\deportare_registro\data\applications\申請データ_20250401000000.xlsx"
    if os.path.exists(application_file):
        df_app = pd.read_excel(application_file)
        print(f"1. 元の申請データ: {len(df_app)} クラブ")
    else:
        print("1. 元の申請データ: ファイルが見つかりません")
        return
    
    # 2. 処理済み受付データ
    processed_dir = r"e:\oasobi\deportare_registro\data\processed_reception_data"
    processed_files = []
    if os.path.exists(processed_dir):
        for file in Path(processed_dir).glob("処理済み受付データ_*.xlsx"):
            processed_files.append(file)
    
    if processed_files:
        # 最新のファイルを取得
        latest_processed = max(processed_files, key=lambda x: x.stat().st_mtime)
        df_processed = pd.read_excel(latest_processed)
        print(f"2. 処理済み受付データ: {len(df_processed)} クラブ")
        print(f"   ファイル: {latest_processed.name}")
    else:
        print("2. 処理済み受付データ: ファイルが見つかりません")
    
    # 3. クラブ情報が追加されたデータ
    merged_dir = r"e:\oasobi\deportare_registro\data\reception_data_with_club_info"
    merged_files = []
    if os.path.exists(merged_dir):
        for file in Path(merged_dir).glob("受付データ_クラブ情報付き_*.xlsx"):
            merged_files.append(file)
    
    if merged_files:
        latest_merged = max(merged_files, key=lambda x: x.stat().st_mtime)
        df_merged = pd.read_excel(latest_merged)
        print(f"3. クラブ情報付きデータ: {len(df_merged)} クラブ")
        print(f"   ファイル: {latest_merged.name}")
    else:
        print("3. クラブ情報付きデータ: ファイルが見つかりません")
    
    # 4. 受付状況データ
    status_dir = r"e:\oasobi\deportare_registro\data\reception_status"
    status_files = []
    if os.path.exists(status_dir):
        for file in Path(status_dir).glob("受付状況一覧_*.xlsx"):
            status_files.append(file)
    
    if status_files:
        latest_status = max(status_files, key=lambda x: x.stat().st_mtime)
        df_status = pd.read_excel(latest_status)
        print(f"4. 受付状況データ: {len(df_status)} クラブ")
        print(f"   ファイル: {latest_status.name}")
    else:
        print("4. 受付状況データ: ファイルが見つかりません")
    
    # 5. 最終的な総合チェックリスト
    output_dir = r"e:\oasobi\deportare_registro\output\R7_登録受付処理\受付内容チェック\総合チェックリスト"
    output_files = []
    if os.path.exists(output_dir):
        for file in Path(output_dir).glob("総合チェックリスト_*.xlsx"):
            output_files.append(file)
    
    if output_files:
        latest_output = max(output_files, key=lambda x: x.stat().st_mtime)
        df_output = pd.read_excel(latest_output)
        print(f"5. 最終総合チェックリスト: {len(df_output)} クラブ")
        print(f"   ファイル: {latest_output.name}")
        
        # クラブ名を確認
        if 'クラブ名' in df_output.columns:
            print(f"\n=== 最終出力に含まれるクラブ（最初の10件） ===")
            for i, club_name in enumerate(df_output['クラブ名'].head(10)):
                print(f"{i+1:2d}. {club_name}")
                
            print(f"\n=== 最終出力に含まれないクラブの確認 ===")
            # 元の申請データのクラブ名を取得
            if '申請_クラブ名_選択' in df_app.columns:
                app_clubs = set()
                for club_selection in df_app['申請_クラブ名_選択']:
                    if pd.notna(club_selection) and club_selection != 'この中に無い':
                        # クラブ名部分を抽出（区市町村名:クラブ名:読み仮名の形式から）
                        parts = club_selection.split('：')
                        if len(parts) >= 2:
                            club_name = parts[1].replace('クラブ', '')
                            app_clubs.add(club_name)
                
                output_clubs = set(df_output['クラブ名'].tolist())
                missing_clubs = app_clubs - output_clubs
                
                print(f"元の申請データのクラブ数: {len(app_clubs)}")
                print(f"最終出力のクラブ数: {len(output_clubs)}")
                print(f"除外されたクラブ数: {len(missing_clubs)}")
                
                if missing_clubs:
                    print(f"\n除外されたクラブ（最初の10件）:")
                    for i, club in enumerate(list(missing_clubs)[:10]):
                        print(f"{i+1:2d}. {club}")
    else:
        print("5. 最終総合チェックリスト: ファイルが見つかりません")

if __name__ == "__main__":
    track_club_count_changes()
