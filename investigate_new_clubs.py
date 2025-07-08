#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
「この中に無い」を選択したクラブの詳細を調査
"""

import pandas as pd
import os

def investigate_kono_naka_ni_nai_clubs():
    """「この中に無い」を選択したクラブの詳細を調査"""
    
    print("=== 「この中に無い」クラブの詳細調査 ===\n")
    
    # 申請データの読み込み
    application_file = r"e:\oasobi\deportare_registro\data\applications\申請データ_20250401000000.xlsx"
    df_app = pd.read_excel(application_file)
    
    # 「この中に無い」を選択したクラブを抽出
    kono_naka_ni_nai_clubs = df_app[df_app['申請_クラブ名_選択'] == 'この中に無い']
    
    print(f"総申請数: {len(df_app)}")
    print(f"「この中に無い」を選択したクラブ数: {len(kono_naka_ni_nai_clubs)}")
    print(f"既存クラブを選択したクラブ数: {len(df_app) - len(kono_naka_ni_nai_clubs)}")
    print()
    
    if len(kono_naka_ni_nai_clubs) > 0:
        print("=== 「この中に無い」クラブの詳細 ===")
        for i, (idx, row) in enumerate(kono_naka_ni_nai_clubs.iterrows()):
            club_text = row.get('申請_クラブ名_テキスト', 'N/A')
            municipality = row.get('申請_区市町村名', 'N/A')
            application_type = row.get('申請_申請種別', 'N/A')
            
            print(f"{i+1:2d}. クラブ名: {club_text}")
            print(f"    区市町村: {municipality}")
            print(f"    申請種別: {application_type}")
            print()
        
        # 区市町村別の分布
        print("=== 区市町村別分布 ===")
        municipality_counts = kono_naka_ni_nai_clubs['申請_区市町村名'].value_counts()
        for municipality, count in municipality_counts.items():
            print(f"{municipality}: {count}件")
        print()
        
        # 申請種別の分布
        print("=== 申請種別分布 ===")
        type_counts = kono_naka_ni_nai_clubs['申請_申請種別'].value_counts()
        for app_type, count in type_counts.items():
            print(f"{app_type}: {count}件")
        print()
        
        # クラブ名テキストが空でないものの確認
        valid_club_names = kono_naka_ni_nai_clubs[kono_naka_ni_nai_clubs['申請_クラブ名_テキスト'].notna()]
        print(f"クラブ名テキストが入力されているもの: {len(valid_club_names)}件")
        
        if len(valid_club_names) > 0:
            print("\n=== 有効なクラブ名テキスト ===")
            for i, club_name in enumerate(valid_club_names['申請_クラブ名_テキスト']):
                if pd.notna(club_name) and str(club_name).strip():
                    print(f"{i+1:2d}. {club_name}")
        
        # 処理に含まれるべきかどうかの判定
        print(f"\n=== 処理対象になるべきかの判定 ===")
        print("新規クラブ（「この中に無い」）も登録申請の処理対象になるべきですが、")
        print("現在のシステムでは除外されているようです。")
        print("これらのクラブも総合チェックリストに含めるべきかどうか確認が必要です。")

if __name__ == "__main__":
    investigate_kono_naka_ni_nai_clubs()
