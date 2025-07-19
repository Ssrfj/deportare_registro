import pandas as pd
import os

# 最新の総合チェックリストファイルを開く
files = [f for f in os.listdir('output/R7_登録受付処理/受付内容チェック/総合チェックリスト') if f.endswith('.xlsx')]
latest_file = sorted(files)[-1]
print(f'最新ファイル: {latest_file}')

# ファイルを読み込み
df = pd.read_excel(f'output/R7_登録受付処理/受付内容チェック/総合チェックリスト/{latest_file}')

# 人間チェック関連の列を確認
human_check_columns = [col for col in df.columns if '人間チェック' in col or 'チェック者' in col or '書類チェック' in col]
print(f'人間チェック関連列: {human_check_columns}')

# 日本橋クラブの人間チェック状況を確認
if not df.empty:
    nihonbashi_rows = df[df['クラブ名'] == '日本橋クラブ']
    print(f'日本橋クラブの行数: {len(nihonbashi_rows)}')
    
    if len(nihonbashi_rows) > 0:
        print("\n=== 日本橋クラブの人間チェック状況 ===")
        for col in ['書類チェック結果', '書類チェック更新日時']:
            if col in nihonbashi_rows.columns:
                value = nihonbashi_rows[col].iloc[0]
                print(f'{col}: {value}')
            else:
                print(f'{col}: 列なし')
        
        # すべての列名を表示
        print(f"\n=== すべての列名（最初の20個） ===")
        for i, col in enumerate(df.columns[:20]):
            print(f'{i+1}: {col}')
