import pandas as pd
import os
from datetime import datetime

def check_human_results_reflection():
    """人間によるチェック結果が総合チェックリストに反映されているかを確認する"""
    
    # 最新の総合チェックリストファイルを取得
    checklist_folder = r"e:\oasobi\deportare_registro\output\R7_登録受付処理\受付内容チェック\総合チェックリスト"
    
    if not os.path.exists(checklist_folder):
        print("総合チェックリストフォルダが存在しません")
        return
    
    # 最新のファイルを取得
    files = [f for f in os.listdir(checklist_folder) if f.endswith('.xlsx')]
    if not files:
        print("総合チェックリストファイルが見つかりません")
        return
    
    latest_file = sorted(files)[-1]
    file_path = os.path.join(checklist_folder, latest_file)
    
    print(f"最新の総合チェックリスト: {latest_file}")
    
    try:
        # ファイルを読み込み
        df = pd.read_excel(file_path)
        
        print(f"データ件数: {len(df)}")
        print(f"列数: {len(df.columns)}")
        print("\n=== 列名一覧 ===")
        for i, col in enumerate(df.columns):
            print(f"{i+1}. {col}")
        
        # 書類チェック結果の列を確認
        if '書類チェック結果' in df.columns:
            print("\n=== 書類チェック結果 ===")
            check_results = df['書類チェック結果'].dropna()
            for i, result in enumerate(check_results):
                print(f"{i+1}. {result}")
        
        # 書類チェック更新日時の列を確認
        if '書類チェック更新日時' in df.columns:
            print("\n=== 書類チェック更新日時 ===")
            update_times = df['書類チェック更新日時'].dropna()
            for i, time in enumerate(update_times):
                print(f"{i+1}. {time}")
        
        # チェック者名の列を確認
        checker_columns = [col for col in df.columns if 'チェック者名' in col]
        if checker_columns:
            print(f"\n=== チェック者名の列（{len(checker_columns)}個） ===")
            for col in checker_columns:
                print(f"- {col}")
                values = df[col].dropna()
                if len(values) > 0:
                    print(f"  値の例: {list(values[:3])}")
        
        # 人間チェック結果の存在確認
        human_check_found = any(
            '人間' in str(result) or 'ヒューマン' in str(result) 
            for result in df['書類チェック結果'].dropna()
        ) if '書類チェック結果' in df.columns else False
        
        print(f"\n=== 判定結果 ===")
        print(f"人間によるチェック結果が反映されているか: {'YES' if human_check_found else 'NO'}")
        
        return df
        
    except Exception as e:
        print(f"ファイル読み込みエラー: {e}")
        return None

if __name__ == "__main__":
    result_df = check_human_results_reflection()
