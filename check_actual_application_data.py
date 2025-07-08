import pandas as pd
import os

def check_actual_application_data():
    """実際の申請データを分析する"""
    
    # 実際の申請データファイルのパス
    application_file = r"e:\oasobi\deportare_registro\data\applications\申請データ_20250401000000.xlsx"
    
    if not os.path.exists(application_file):
        print(f"ファイルが見つかりません: {application_file}")
        return
    
    try:
        # データを読み込み
        df = pd.read_excel(application_file)
        print(f"申請データを読み込みました: {application_file}")
        print(f"総行数: {len(df)}")
        print(f"列数: {len(df.columns)}")
        print("\n列名:")
        for i, col in enumerate(df.columns):
            print(f"  {i+1}: {col}")
        
        # 申請_クラブ名_選択の分布を確認
        if "申請_クラブ名_選択" in df.columns:
            print(f"\n申請_クラブ名_選択の分布:")
            selection_counts = df["申請_クラブ名_選択"].value_counts()
            print(selection_counts)
            
            # "この中に無い"のクラブを確認
            new_clubs = df[df["申請_クラブ名_選択"] == "この中に無い"]
            print(f"\n「この中に無い」を選択したクラブ数: {len(new_clubs)}")
            
            if len(new_clubs) > 0 and "申請_クラブ名_テキスト" in df.columns:
                print("新クラブの名前:")
                for i, club_name in enumerate(new_clubs["申請_クラブ名_テキスト"], 1):
                    print(f"  {i}: {club_name}")
            
            # 既存クラブを選択したもの
            existing_clubs = df[df["申請_クラブ名_選択"] != "この中に無い"]
            print(f"\n既存クラブを選択したクラブ数: {len(existing_clubs)}")
            
        else:
            print("\n「申請_クラブ名_選択」列が見つかりません")
            
        # 最初の数行を表示
        print(f"\n最初の3行のデータ:")
        print(df.head(3).to_string())
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    check_actual_application_data()
