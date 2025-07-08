#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import sys
sys.path.append('.')
from src.core.load_latest_club_data import load_latest_club_reception_data

# 統合されたクラブ情報付き受付データを読み込み
data = load_latest_club_reception_data()
if data is not None:
    print('統合データのカラム一覧:')
    columns = data.columns.tolist()

    # チェック項目に関連するカラムを探す
    check_related_columns = [col for col in columns if 'チェック' in col]
    print(f'\nチェック関連のカラム ({len(check_related_columns)}個):')
    for col in check_related_columns:
        print(f'  {col}')

    # 書類1で期待されるカラムとの比較
    expected_columns = [
        'チェック項目_クラブ名',
        'チェック項目_申請種別',
        'チェック項目_住所',
        'チェック項目_担当者名',
        'チェック項目_連絡先',
        'チェック項目_適合状況'
    ]

    print(f'\n書類1で期待されるカラムの存在確認:')
    for col in expected_columns:
        exists = col in columns
        print(f'  {col}: {"存在" if exists else "不存在"}')
        
    # チェック担当者カラムの確認
    person_columns = [col for col in columns if 'チェック者名' in col]
    print(f'\nチェック者名関連のカラム ({len(person_columns)}個):')
    for col in person_columns:
        print(f'  {col}')
        
    # 書類関連のカラムも確認
    document_columns = [col for col in columns if '書類' in col]
    print(f'\n書類関連のカラム ({len(document_columns)}個):')
    for col in document_columns[:20]:  # 最初の20個のみ表示
        print(f'  {col}')
    if len(document_columns) > 20:
        print(f'  ... 他 {len(document_columns) - 20}個')
        
else:
    print('データの読み込みに失敗しました')
