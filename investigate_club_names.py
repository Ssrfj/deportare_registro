#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
クラブ名の抽出処理を詳細に調査するスクリプト
"""

import pandas as pd
import os

def investigate_club_name_extraction():
    """クラブ名の抽出処理を詳細に調査"""
    
    print("=== クラブ名抽出処理の詳細調査 ===\n")
    
    # 1. 元の申請データの確認
    application_file = r"e:\oasobi\deportare_registro\data\applications\申請データ_20250401000000.xlsx"
    df_app = pd.read_excel(application_file)
    
    print(f"元の申請データ: {len(df_app)} 行")
    print(f"申請_クラブ名_選択の例（最初の10件）:")
    for i, club_selection in enumerate(df_app['申請_クラブ名_選択'].head(10)):
        print(f"{i+1:2d}. {club_selection}")
    
    print(f"\n申請_クラブ名_テキストの例（最初の10件）:")
    for i, club_text in enumerate(df_app['申請_クラブ名_テキスト'].head(10)):
        print(f"{i+1:2d}. {club_text}")
    
    # 2. 最終出力データの確認
    output_dir = r"e:\oasobi\deportare_registro\output\R7_登録受付処理\受付内容チェック\総合チェックリスト"
    from pathlib import Path
    output_files = list(Path(output_dir).glob("総合チェックリスト_*.xlsx"))
    
    if output_files:
        latest_output = max(output_files, key=lambda x: x.stat().st_mtime)
        df_output = pd.read_excel(latest_output)
        
        print(f"\n最終出力データ: {len(df_output)} 行")
        print(f"最終出力のクラブ名（最初の10件）:")
        for i, club_name in enumerate(df_output['クラブ名'].head(10)):
            print(f"{i+1:2d}. {club_name}")
        
        # 3. 処理ロジックの推測とマッチング
        print(f"\n=== クラブ名マッチング分析 ===")
        
        # 申請データから想定されるクラブ名を抽出
        extracted_club_names = []
        for club_selection in df_app['申請_クラブ名_選択']:
            if pd.notna(club_selection) and club_selection != 'この中に無い':
                # 形式: 区市町村名：クラブ名：読み仮名
                parts = club_selection.split('：')
                if len(parts) >= 2:
                    club_name = parts[1]  # クラブ名部分を取得
                    extracted_club_names.append(club_name)
        
        print(f"申請データから抽出したクラブ名数: {len(extracted_club_names)}")
        print(f"最終出力のクラブ名数: {len(df_output)}")
        
        # マッチするクラブ名を確認
        output_club_names = df_output['クラブ名'].tolist()
        matched_clubs = []
        unmatched_from_app = []
        unmatched_from_output = []
        
        for app_club in extracted_club_names:
            if app_club in output_club_names:
                matched_clubs.append(app_club)
            else:
                unmatched_from_app.append(app_club)
        
        for output_club in output_club_names:
            if output_club not in extracted_club_names:
                unmatched_from_output.append(output_club)
        
        print(f"\nマッチしたクラブ数: {len(matched_clubs)}")
        print(f"申請データにあるが最終出力にないクラブ数: {len(unmatched_from_app)}")
        print(f"最終出力にあるが申請データにないクラブ数: {len(unmatched_from_output)}")
        
        if unmatched_from_app:
            print(f"\n申請データにあるが最終出力にないクラブ（最初の10件）:")
            for i, club in enumerate(unmatched_from_app[:10]):
                print(f"{i+1:2d}. {club}")
        
        if unmatched_from_output:
            print(f"\n最終出力にあるが申請データにないクラブ（最初の10件）:")
            for i, club in enumerate(unmatched_from_output[:10]):
                print(f"{i+1:2d}. {club}")
        
        # 4. クラブ情報マスタファイルの確認
        club_info_file = r"e:\oasobi\deportare_registro\data\club_info\総合クラブ情報_マスタ.xlsx"
        if os.path.exists(club_info_file):
            df_master = pd.read_excel(club_info_file)
            print(f"\nクラブ情報マスタ: {len(df_master)} 行")
            if 'クラブ名' in df_master.columns:
                master_club_names = df_master['クラブ名'].tolist()
                print(f"マスタのクラブ名（最初の10件）:")
                for i, club_name in enumerate(master_club_names[:10]):
                    print(f"{i+1:2d}. {club_name}")
                
                # 申請データのクラブがマスタに存在するかチェック
                missing_in_master = []
                for app_club in extracted_club_names:
                    if app_club not in master_club_names:
                        missing_in_master.append(app_club)
                
                print(f"\n申請データのクラブでマスタに存在しないもの: {len(missing_in_master)}")
                if missing_in_master:
                    for i, club in enumerate(missing_in_master[:10]):
                        print(f"{i+1:2d}. {club}")
        else:
            print(f"\nクラブ情報マスタファイルが見つかりません: {club_info_file}")

if __name__ == "__main__":
    investigate_club_name_extraction()
