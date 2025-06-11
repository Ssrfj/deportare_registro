import os
import pandas as pd
import glob
from utils import get_jst_now

def merge_and_save_apcption_data():
    # 申請内容の最新CSVを探す
    input_folder = os.path.join(os.path.dirname(__file__), 'R7_登録申請処理', '申請内容')
    csv_files = glob.glob(os.path.join(input_folder, '申請内容_*.csv'))
    if not csv_files:
        print(f"{input_folder} に申請内容_*.csv が見つかりません。")
        return
    input_csv = max(csv_files, key=os.path.getctime)
    df_form = pd.read_csv(input_csv)

    # 最新のクラブ名_YYYYMMDD.csvを探す
    club_files = glob.glob(os.path.join(os.path.dirname(__file__), 'クラブ名_*.csv'))
    if not club_files:
        print("クラブ名_YYYYMMDD.csv ファイルが見つかりません。")
        return
    latest_file = max(club_files, key=os.path.getctime)
    df_old = pd.read_csv(latest_file)

    # カラム名の前後の空白を除去
    df_form.columns = df_form.columns.str.strip()
    df_old.columns = df_old.columns.str.strip()

    # マージ
    df_merged = pd.merge(
        df_old,
        df_form,
        left_on='選択肢（地区名：クラブ名：クラブ名（カタカナ））',
        right_on='申請_クラブ名_選択',
        how='left'
    )
    # 新カラムの作成
    df_merged['R8年度登録申請状況'] = df_merged['申請_クラブ名_選択'].apply(lambda x: '0' if pd.isna(x) else '1')
    df_merged['R8年度登録申請_タイムスタンプ'] = df_merged['申請_タイムスタンプ']
    df_merged['R8年度登録申請_タイムスタンプyyyymmddHHMMSS'] = df_merged['R8年度登録申請_タイムスタンプ'].apply(
        lambda x: pd.to_datetime(x, errors='coerce').strftime('%Y%m%d%H%M%S') if pd.notna(x) else ''
    )
    # カラムの順序を指定
    main_columns = [
        '地区名', 'クラブ名', 'クラブ名（カタカナ）',
        '選択肢（地区名：クラブ名：クラブ名（カタカナ））',
        'R7年度登録クラブ', 'R8年度登録申請状況',
        'R8年度登録申請_タイムスタンプ', 
        'R8年度登録申請_タイムスタンプyyyymmddHHMMSS'
    ]
    columns_order = main_columns + [col for col in df_merged.columns if col not in main_columns]
    df_merged = df_merged[columns_order]
    # 保存先
    save_folder = os.path.join(os.path.dirname(__file__), 'R7_登録申請処理', '申請受付リスト')
    os.makedirs(save_folder, exist_ok=True)
    save_path = os.path.join(save_folder, f'申請受付リスト_{get_jst_now().strftime("%Y%m%d%H%M%S")}.csv')
    df_merged.to_csv(save_path, index=False)
    print("df_merged columns:", df_merged.columns.tolist())
    print(f"結合データを {save_path} に保存しました。")

if __name__ == "__main__":
    merge_and_save_apcption_data()