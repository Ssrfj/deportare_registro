#0. 登録制度東京都申請フォームの入力内容を整理
# 申請されたデータをExcelで出力したのち、csvに変換し、処理を容易に

# 作業用ファイルの指定
# グーグルフォームへの申請内容(Excel)
form_pass = '登録制度東京都申請フォーム（案）（回答）.xlsx'

# グーグルフォームへの申請内容(csv)
# form_pass = '登録制度東京都申請フォーム（案）（回答） - フォームの回答 1 (1).csv'

# カラム名修正用のcsvファイル
column_name_pass = 'column_name.csv'

# パッケージの読み込み(下準備）
import pandas as pd
from datetime import datetime, timezone, timedelta
import os


# 処理開始時間を取得
start_time = datetime.now(timezone(timedelta(hours=9)))
# 処理開始時間を日本時間に設定
start_time = start_time.astimezone(timezone(timedelta(hours=9)))
# 処理開始時間をYYYYMMDDHHMMSS形式に変換
start_time_str = start_time.strftime('%Y%m%d%H%M%S')
# 処理開始時間を表示
print('カラム名修正処理_開始時間:', start_time_str)

# グーグルフォームへの申請内容(Excel)のシート名
form_sheet_name = 'フォームの回答 1'

# グーグルフォームへの申請内容(Excel)を読み込む
form_df = pd.read_excel(form_pass, sheet_name=form_sheet_name)

# 修正後のカラム名がリストされているカラム名修正用のcsvファイルを読み込む
column_name_df = pd.read_csv(column_name_pass, encoding='utf-8')

# 読み込み完了のメッセージを表示
print('必要なデータを読み込みました。')

# カラム名修正用のデータとグーグルフォームへの申請内容のカラム数を照合
if len(column_name_df) != len(form_df.columns):
    print('カラム名修正用のデータとグーグルフォームへの申請内容のカラム数が一致しません。')
    print('カラム名修正用のデータ:', len(column_name_df), 'カラム')
    print('グーグルフォームへの申請内容:', len(form_df.columns), 'カラム')
    exit()
# カラム名修正用のデータをリストに変換
column_name_list = column_name_df['修正後'].tolist()
# グーグルフォームへの申請内容のカラム名を修正後のカラム名に変更
form_df.columns = column_name_list
# 修正後のカラム名を表示
print('修正後のカラム名:', form_df.columns.tolist())
# 修正後のデータの保存フォルダを作成（作成済みの場合は処理をパス）
if not os.path.join('R7_登録申請処理','申請内容'):
    # フォルダが存在しない場合は作成
    form_folder = os.path.join('R7_登録申請処理', '申請内容')
    os.makedirs(form_folder, exist_ok=True)
    print('フォルダが作成されました')
else:
    print('フォルダは既に存在しています')
# 修正後のデータを保存するフォルダを指定
form_output_folder = os.path.join('R7_登録申請処理','申請内容')
# 修正後のデータのファイル名を指定
form_output_file_path = os.path.join(form_output_folder, f'申請内容_{start_time_str}.csv')
# 修正後のデータをCSVファイルに保存
form_df.to_csv(form_output_file_path, index=False, encoding='utf-8-sig')

# 修正完了のメッセージを表示
print('申請内容のカラム名を修正し、CSVファイルに保存しました。')

#1. 登録制度東京都申請フォームの自動受付
# 申請されたデータをもとに、まず申請状況をリスト化

# クラブ名のリスト(csv):f'クラブリスト_{YYYYMMDDHHMMSS}.csvの形式で保存されているので、最新のクラブリストを読み込む
try:
    # クラブ名のクラブリスト_{YYYYMMDDHHMMSS}.csvのファイルを探し、最新のものを読み込む
    club_list_files = [f for f in os.listdir('.') if f.startswith('クラブリスト_') and f.endswith('.csv')]
    if not club_list_files:
        raise FileNotFoundError("クラブリストのCSVファイルが見つかりません。")
    # 最新のクラブリストファイルを取得
    club_list_file_for_acceptance = max(club_list_files, key=os.path.getctime)
    # 最新のクラブリストを読み込む
    club_list_df_for_acceptance = pd.read_csv(club_list_file_for_acceptance, encoding='utf-8-sig')
    # クラブ名のリストを確認
    print(club_list_df_for_acceptance.head())
    print("クラブリストの読み込みが完了しました")
except Exception as e:
    print(f"クラブリストの読み込み中にエラーが発生しました: {e}")

# クラブからの申請内容が申請内容_{start_time_str}.csvの形式で保存されているので、最新の申請内容を読み込む
try:
    # クラブ名の申請内容_{start_time_str}.csvのファイルを探し、最新のものを読み込む
    # 保存先のフォルダを指定
    form_output_file_path = os.path.join('R7_登録申請処理','申請内容')
    if not os.path.exists(form_output_file_path):
        raise FileNotFoundError("申請内容のフォルダが見つかりません。")
    # フォルダ内のファイルをリストアップ
    # 申請内容のCSVファイルを探す
    form_files = [f for f in os.listdir(form_output_file_path) if f.startswith('申請内容_') and f.endswith('.csv')]
    print(f"申請内容のCSVファイル: {form_files}")
    if not form_files:
        raise FileNotFoundError("申請内容のCSVファイルが見つかりません。")
    # 最新の申請内容ファイルを取得
    form_file_for_acceptance = max(form_files, key=lambda f: os.path.getctime(os.path.join(form_output_file_path, f)))
    # 最新の申請内容を読み込む
    form_df_for_acceptance = pd.read_csv(os.path.join(form_output_file_path, form_file_for_acceptance), encoding='utf-8-sig')
    # 申請内容のデータを確認
    print(form_df_for_acceptance.head())
    print(form_df_for_acceptance.columns)
    print(form_df_for_acceptance.dtypes)
    print("申請内容の読み込みが完了しました")
except Exception as e:
    print(f"申請内容の読み込み中にエラーが発生しました: {e}")
    exit()

# タイムスタンプをdatetime型に変換
form_df_for_acceptance['申請_タイムスタンプ'] = pd.to_datetime(form_df_for_acceptance['申請_タイムスタンプ'], errors='coerce')
form_df_for_acceptance['申請_タイムスタンプyyyymmddHHMMSS'] = form_df_for_acceptance['申請_タイムスタンプ'].dt.strftime('%Y%m%d%H%M%S')

# club_list_dfに申請内容を基に申請した追記
# 最新の申請のみを抽出（クラブ名ごとに最新のタイムスタンプ）
latest_applied_clubs_df = form_df_for_acceptance.sort_values('申請_タイムスタンプ').drop_duplicates('申請_クラブ名_選択', keep='last')

# クラブ名でマージ
merged_club_list_df_for_acceptance = pd.merge(
    club_list_df_for_acceptance,
    latest_applied_clubs_df,
    left_on='選択肢（地区名：クラブ名：クラブ名（カタカナ））',
    right_on='申請_クラブ名_選択',
    how='left'
    )

# 申請フラグとタイムスタンプ列を追加
merged_club_list_df_for_acceptance['R8年度登録申請クラブ'] = merged_club_list_df_for_acceptance['申請_タイムスタンプ'].notna().astype(int)
merged_club_list_df_for_acceptance['R8年度登録申請_タイムスタンプ'] = merged_club_list_df_for_acceptance['申請_タイムスタンプ']

# 結果確認
print(merged_club_list_df_for_acceptance[['選択肢（地区名：クラブ名：クラブ名（カタカナ））', 'R8年度登録申請クラブ', 'R8年度登録申請_タイムスタンプ']].head())

# merged_club_list_dfを'クラブリスト_yyyymmddhhmmss.csv'に出力
# 日本の現在時刻を取得
jst_now = datetime.now(timezone(timedelta(hours=9)))

# 時刻をyyyymmddHHMMSS形式に変換
timestamp_for_acceptance = jst_now.strftime("%Y%m%d%H%M%S")

# 出力時のファイル名を指定
output_folder_path_for_acceptance = os.path.join('R7_登録申請処理', '申請受付リスト')
output_file_name_for_acceptance = f'申請受付リスト_{timestamp_for_acceptance}.csv'
output_file_path_for_acceptance = os.path.join(output_folder_path_for_acceptance, output_file_name_for_acceptance)

# csvを出力
merged_club_list_df_for_acceptance.to_csv(output_file_path_for_acceptance, index=False)
print(f"出力ファイルパス: {output_file_path_for_acceptance}")

#2. クラブごとチェックリスト作成
# 申請されたデータをもとにクラブごとのチェックリストを作成

# 日本の現在時刻を取得
jst_now = datetime.now(timezone(timedelta(hours=9)))

# 時刻をyyyymmddHHMMSS形式に変換
timestamp_for_make_checklist = jst_now.strftime("%Y%m%d%H%M%S")

# クラブリスト_{timestamp}.csvを読み込む
# folderを参照して、最新のクラブリストを探す
foldr_path_for_make_checklist = os.path.join('R7_登録申請処理','申請受付リスト')
latest_file = max([os.path.join(foldr_path_for_make_checklist, f) for f in os.listdir(foldr_path_for_make_checklist)], key=os.path.getctime)

# 最新のクラブリストを読み込む
club_list_df_for_make_checklist = pd.read_csv(latest_file)
print(club_list_df_for_make_checklist.head())
print(club_list_df_for_make_checklist.columns)
print(club_list_df_for_make_checklist.dtypes)
print("クラブリストの読み込みが完了しました")

# R8年度登録申請クラブが1のデータのみ保持
application_club_list_df_for_make_checklist = club_list_df_for_make_checklist[club_list_df_for_make_checklist['R8年度登録申請クラブ'] == 1].copy()

# タイムスタンプをdatetime型に変換
application_club_list_df_for_make_checklist['R8年度登録申請_タイムスタンプ'] = pd.to_datetime(application_club_list_df_for_make_checklist['R8年度登録申請_タイムスタンプ'], errors='coerce')

# さらに、yyyymmddHHMMSS形式に変換
application_club_list_df_for_make_checklist['R8年度登録申請_タイムスタンプyyyymmddHHMMSS'] = application_club_list_df_for_make_checklist['R8年度登録申請_タイムスタンプ'].dt.strftime('%Y%m%d%H%M%S')

# 出力フォルダの作成（作成済みの場合は処理をパス）
checklist_output_folder = os.path.join('R7_登録申請処理', '申請入力内容')
if not os.path.exists(checklist_output_folder):
    os.makedirs(checklist_output_folder,exist_ok=True)
    checklist_output_folder = os.path.join('R7_登録申請処理', '申請入力内容')
    print('フォルダが作成されました')
else:
    checklist_output_folder = os.path.join('R7_登録申請処理', '申請入力内容')
    print('フォルダは既に存在しています')

# クラブごとのチェックリストを保存するための出力フォルダを作成('R7_登録申請処理/申請入力内容'の下にクラブごとに別のチェックリストフォルダを作成)
for _, row in application_club_list_df_for_make_checklist.iterrows():
    club_name = row['クラブ名']
    # クラブごとのフォルダを作成
    club_folder_path = os.path.join(checklist_output_folder, club_name)
    if not os.path.exists(club_folder_path):
        os.makedirs(club_folder_path, exist_ok=True)
        print(f"{club_name}のフォルダが作成されました")
    else:
        print(f"{club_name}のフォルダはすでに存在しています")

# クラブごとのチェックリスト作成状況を保存するcsvを読み込み（ない場合は作成）
folder_of_checklist_create_status = os.path.join('R7_登録申請処理', '申請入力内容')
file_of_checklist_create_status = os.path.join(folder_of_checklist_create_status, 'クラブごとのチェックリスト作成状況.csv')

# ディレクトリがなければ作成
if not os.path.exists(folder_of_checklist_create_status):
    os.makedirs(folder_of_checklist_create_status, exist_ok=True)

if os.path.exists(file_of_checklist_create_status):
    checklist_create_df = pd.read_csv(file_of_checklist_create_status)
    print('クラブごとのチェックリスト作成状況.csvはすでに存在しています')
else:
    checklist_create_df = pd.DataFrame(columns=['クラブ名','申請日時', 'チェックリスト作成日時'])
    checklist_create_df.to_csv(file_of_checklist_create_status, index=False)
    print('クラブごとのチェックリスト作成状況.csvが作成されました')

# クラブごとのチェックリストを作成
# クラブごとの処理
for _, row in application_club_list_df_for_make_checklist.iterrows():
    try:
        club_data = {
            'クラブ名': [row['クラブ名']],
            '地区名': [row['地区名']],
            '担当者名': [row['申請_申請担当者名']],
            '役職名': [row['申請_申請担当者役職']],
            'メールアドレス': [row['申請_メールアドレス']],
            '電話番号': [row['申請_TEL']],
            'FAX番号': [row['申請_FAX(任意)']],
            '申請時間': [row['R8年度登録申請_タイムスタンプyyyymmddHHMMSS']],
            '自動チェック': [''],
            '自動チェック更新時間': [''],
            '書類チェック': [''],
            '書類チェック更新時間': [''],
            '書類間チェック': [''],
            '書類間チェック更新時間': [''],
            '担当者登録基準最終チェック': [''],
            '担当者登録基準最終チェック更新時間': [''],
            }
        club_df_for_make_checklist = pd.DataFrame(club_data)
        print(f"{row['クラブ名']}のclub_dfが作成されました")
        # checklist_create_dfにクラブ名があるかを確認
        if row['クラブ名'] not in checklist_create_df['クラブ名'].values:
            print('クラブ名がまだ存在しません')
            # checklist_create_dfにクラブ名の列を追加
            new_row = pd.DataFrame([{
                'クラブ名': row['クラブ名'],
                '申請日時': row['R8年度登録申請_タイムスタンプyyyymmddHHMMSS'],
                'チェックリスト作成日時': timestamp_for_make_checklist
                }])
            checklist_create_df = pd.concat([checklist_create_df, new_row], ignore_index=True)
            print(f"{row['クラブ名']}の列が追加されました")
        else:
            print('クラブ名がすでに存在します')

            # checklist_create_dfにある申請日時と申請時間を照合
            print('checklist_create_dfにある申請日時と申請時間を照合に移行します')
        if row['R8年度登録申請_タイムスタンプyyyymmddHHMMSS'] == checklist_create_df.loc[checklist_create_df['クラブ名'] == row['クラブ名'], '申請日時'].values[0]:
            # その後の処理
            # クラブごとのチェックリスト保存先を指定
            output_folder = os.path.join(checklist_output_folder, row['クラブ名'])
            # csvに出力
            file_name = f"{row['クラブ名']}_申請{row['R8年度登録申請_タイムスタンプyyyymmddHHMMSS']}_作成{timestamp_for_make_checklist}.csv"
            print(f"file_name: {file_name}")
            print(f"output_folder: {output_folder}")
            file_path = os.path.join(output_folder, file_name)
            print(f"file_path: {file_path}")
            print(f"出力ファイルパス: {file_path}")
            club_df_for_make_checklist.to_csv(file_path, index=False)
            # checklist_create_dfのアップデート
            checklist_create_df.loc[checklist_create_df['クラブ名'] == row['クラブ名'], '申請日時'] = row['R8年度登録申請_タイムスタンプyyyymmddHHMMSS']
            checklist_folder_path = os.path.join('R7_登録申請処理', '申請入力内容')
            checklist_file_name = 'クラブごとのチェックリスト作成状況.csv'
            checklist_path = os.path.join(checklist_folder_path, checklist_file_name)
            checklist_create_df.to_csv(checklist_path, index=False)
            print(f"{row['クラブ名']}の申請日時が更新されました")
        else:
            print('申請日時が同じチェックリストを作成済みです')
    except Exception as e:
        print(f"クラブ {row['クラブ名']} の処理中にエラーが発生しました: {e}")

#3. クラブごとに自動チェック
# 申請されたデータをもとに記入漏れ等をチェック
# 必須項目に入力があるかをチェックする関数
def check_must_columns(application_row):
    """
    必須の項目が記入されているかをチェックします。
    """
    error_dict = {}
    # 必須ではない項目を指定（変更があればここを修正）
    not_must_column = [
        '申請_届出_書類_(選択時必須)',
        '申請_建物名(任意)',
        '申請_FAX(任意)',
        '申請_種目_その他_数(選択時必須)',
        '申請_種目_その他_テキスト(選択時必須)',
        '申請_規約_改定時議事録_書類(選択時必須)',
        '申請_規約_改定前規約_書類(選択時必須)',
        '申請_規約_書類(選択時必須)',
        '申請_役員名簿_種類(選択時必須)',
        '申請_役員名簿_書類(選択時必須)',
        '申請_事業報告_決議機関名称(選択時必須)',
        '申請_事業報告_決議日(選択時必須)',
        '申請_事業報告_事業報告_書類(選択時必須)',
        '申請_事業報告_議事録_書類(選択時必須)',
        '申請_決算_決議機関名称(選択時必須)',
        '申請_決算_決議日(選択時必須)',
        '申請_決算_書類(選択時必須)',
        '申請_決算_議事録_書類(選択時必須)',
    ]

    # 必須のカラムを指定（全column-not_must_column)
    must_column = [col for col in application_row.columns if col not in not_must_column]

    # 必須のカラムが空白（NaN）ではないかをチェック
    if application_row[must_column].isna().any().any():
        error_at_must_column = []
        for col in must_column:
            if not application_row.empty and pd.isna(application_row[col].iloc[0]):
                 error_at_must_column.append(col)
        if error_at_must_column:
            error_dict['e_a_000'] = f'必須の項目が入力されていない:{error_at_must_column}'
    else:
        print('必須項目が入力されている')

    return error_dict

# 届け出中のクラブが資料を提出しているかをチェックする関数
def check_submitting_now(form_row):
    """
    form_row['申請_クラブ名_選択']が「この中に無い」の時に
    form_row['所在する区市町村を通じ、東京都に総合型クラブ設立の「届出」を提出中であることを確認できる資料を提出してください。']にデータがあるかをチェックします。
    """
    error_dict = {}
    # form_rowが空でないことを確認
    if not form_row.empty:
        # form_row['申請_クラブ名_選択']が'この中に無い'の時に専用のフラグを立てる
        flag_submitting_now = 0 # 初期値を0に設定
        if (form_row['申請_クラブ名_選択'] == 'この中に無い').any():
            flag_submitting_now = 1 # 条件を満たす行が1つでもあればフラグを1に設定
            print('このクラブは東京都に「届出」提出中です')
        else:
            flag_submitting_now = 0 # 条件を満たす行がなければフラグは0のまま
            print('このクラブは東京都に「届出」済です')

        if flag_submitting_now == 1 and pd.isna(form_row['申請_届出_書類_(選択時必須)'].iloc[0]):
            error_dict['e_a_001'] = '非届出クラブだが、都に「届出」中であると確認できる資料が提出されていない'
        else:
            print('クラブ名の記載に問題がない')
    else:
        print("警告: check_submitting_now 関数に空のform_rowが渡されました。")

    return error_dict

# クラブの所在地が正しいかをチェックする関数
def check_club_location(form_row):
    """
    form_row['地区名']と['申請_区市町村名']が同じであるかを確認
    """
    error_dict = {}
    # form_rowが空でないことを確認
    if not form_row.empty:
        # "地区名"と"申請_区市町村名"が同じであるかを確認
        if form_row['地区名'].iloc[0] != form_row['申請_区市町村名'].iloc[0]:
            error_dict['e_a_002'] = '地区名と申請区市町村名が一致しない'
        else:
            print('地区名と申請区市町村名が一致している')
    return error_dict

# 電話番号をチェックする関数
def check_phone_number(form_row):
    """
    form_row['申請担当者の日中連絡がつく電話番号を入力してください']が電話番号形式かをチェックします。
    （ハイフンを除いて10桁もしくは11桁であるかをチェック）
    """
    error_dict = {}
    if not form_row.empty:
        phone_number = form_row['申請_TEL'].iloc[0]
        # NaNでないことを確認
        if not pd.isna(phone_number):
             # 電話番号からハイフンを取り除く
            phone_number_cleaned = str(phone_number).replace('-', '')
            if not (len(phone_number_cleaned) == 10 or len(phone_number_cleaned) == 11):
                error_dict['e_a_003-a'] = '電話番号が不正である（ハイフンを除いて10桁もしくは11桁ではない）'
            else:
                print('電話番号の記載に問題がない')
        else:
            error_dict['e_a_003-b'] = '電話番号が入力されていない'
    else:
        print("警告: check_phone_number 関数に空のform_rowが渡されました。")
    return error_dict

# FAX番号をチェックする関数
def check_fax_number(form_row):
    """
    form_row['（必要があれば）申請担当者のFAX番号を入力してください']が電話番号形式かをチェックします。
    （ハイフンを除いて10桁であるかをチェック）
    """
    error_dict = {}
    if not form_row.empty:
        fax_number = form_row['申請_FAX(任意)'].iloc[0]
        # NaNでないことを確認
        if not pd.isna(fax_number):
            # FAX番号からハイフンを取り除く
            fax_number_cleaned = str(fax_number).replace('-', '')
            if not len(fax_number_cleaned) == 10:
                error_dict['e_a_004-a'] = 'FAX番号が不正である（ハイフンを除いて10桁ではない）'
            else:
                print('FAX番号の記載に問題がない')
        else:
            error_dict['e_a_004-b'] = 'FAX番号が入力されていない'
    else:
        print("警告: check_fax_number 関数に空のform_rowが渡されました。")
    return error_dict

# 申請種別を確認する関数
def check_application_type(application_row, application_data_df, club_name):
    """
    application_row['申請種別を選択してください']が application_data_df のR7年度の登録状況と一致するかをチェックします。
    """
    error_dict = {}
    if not application_row.empty:
        # application_data_df に現在のクラブ名に対応する行があるかを確認
        application_data_match_row = application_data_df[application_data_df['クラブ名'] == club_name]
        if not application_data_match_row.empty:
            if application_row['申請_申請種別'].iloc[0] == '新規（R7年度には登録していない）' and application_data_match_row['R7年度登録クラブ'].iloc[0] == 1:
                error_dict['e_a_005-a'] = 'R7年度の登録クラブだが、新規登録として申請されている'
            elif application_row['申請_申請種別'].iloc[0] == '更新（R7年度に登録済み）' and application_data_match_row['R7年度登録クラブ'].iloc[0] == 0:
                error_dict['e_a_005-b'] = 'R7年度の登録クラブではないが、更新として申請されている'
            else:
                print('申請種別が正しい')
        else:
            print(f"警告: クラブ名 '{club_name}' は申請内容を含むデータに見つかりませんでした。")
            error_dict['e_a_005-c'] = f'クラブ名 {club_name} が申請内容に見つかりませんでした。'
    else:
        print("警告: check_application_type 関数に空の application_row が渡されました。")
        error_dict['e_a_005-d'] = '申請種別が空です。'
    return error_dict

# 基準適合状況の入力を確認する関数
def check_standard_compliance(application_row):
    """
    基準適合状況について全て「適合している」となっているかをチェックします。
    （R8は(1)③については経過措置のためチェックを排除）
    """
    error_dict = {}
    if not application_row.empty:
        standard_column = [
            '申請_適合状況(1)①',
            '申請_適合状況(1)②',
            #'申請_適合状況(1)③', # R8ではチェックしない
            '申請_適合状況(1)④',
            '申請_適合状況(2)⑤',
            '申請_適合状況(3)⑥',
            '申請_適合状況(3)⑦'
            ]
        # 各カラムをループして '適合していない' が含まれているかを確認
        error_at_standard_column = [col for col in standard_column if not application_row.empty and application_row[col].iloc[0] == '適合していない']
        if error_at_standard_column:
             error_dict['e_a_006-a'] = f'登録基準に適合していない:{error_at_standard_column}'
        else:
            print('基準に適合している')
    else:
        print("警告: check_standard_compliance 関数に空のapplication_rowが渡されました。")
        error_dict['e_a_006-b'] = '基準適合状況の入力が空です。'
    return error_dict

# 会員数の入力をチェックする関数
def check_number_of_members(application_row):
    """
    会員数に関するカラムに数字が記入されているかをチェックします。
    """
    error_dict = {}
    if not application_row.empty:
        num_of_members_column = [
            '申請_会員_未就_男_数',
            '申請_会員_未就_女_数',
            '申請_会員_未就_不_数',
            '申請_会員_小_男_数',
            '申請_会員_小_女_数',
            '申請_会員_小_不_数',
            '申請_会員_中_男_数',
            '申請_会員_中_女_数',
            '申請_会員_中_不_数',
            '申請_会員_高_男_数',
            '申請_会員_高_女_数',
            '申請_会員_高_不_数',
            '申請_会員_20s_男_数',
            '申請_会員_20s_女_数',
            '申請_会員_20s_不_数',
            '申請_会員_30s_男_数',
            '申請_会員_30s_女_数',
            '申請_会員_30s_不_数',
            '申請_会員_40s_男_数',
            '申請_会員_40s_女_数',
            '申請_会員_40s_不_数',
            '申請_会員_50s_男_数',
            '申請_会員_50s_女_数',
            '申請_会員_50s_不_数',
            '申請_会員_60s_男_数',
            '申請_会員_60s_女_数',
            '申請_会員_60s_不_数',
            '申請_会員_70s_男_数',
            '申請_会員_70s_女_数',
            '申請_会員_70s_不_数'
            ]
        num_of_annual_fee_members_column = [
            '申請_年会_未就_男_数',
            '申請_年会_未就_女_数',
            '申請_年会_未就_不_数',
            '申請_年会_小_男_数',
            '申請_年会_小_女_数',
            '申請_年会_小_不_数',
            '申請_年会_中_男_数',
            '申請_年会_中_女_数',
            '申請_年会_中_不_数',
            '申請_年会_高_男_数',
            '申請_年会_高_女_数',
            '申請_年会_高_不_数',
            '申請_年会_20s_男_数',
            '申請_年会_20s_女_数',
            '申請_年会_20s_不_数',
            '申請_年会_30s_男_数',
            '申請_年会_30s_女_数',
            '申請_年会_30s_不_数',
            '申請_年会_40s_男_数',
            '申請_年会_40s_女_数',
            '申請_年会_40s_不_数',
            '申請_年会_50s_男_数',
            '申請_年会_50s_女_数',
            '申請_年会_50s_不_数',
            '申請_年会_60s_男_数',
            '申請_年会_60s_女_数',
            '申請_年会_60s_不_数',
            '申請_年会_70s_男_数',
            '申請_年会_70s_女_数',
            '申請_年会_70s_不_数'
            ]

        error_at_num_of_members_column = []
        for col in num_of_members_column:
            # form_rowが空でないことと、値がNaNでないことを確認してから型をチェック
            if not application_row.empty and not pd.isna(application_row[col].iloc[0]) and not isinstance(application_row[col].iloc[0], (int, float)): # floatも許容する
                error_at_num_of_members_column.append(col)
        if error_at_num_of_members_column:
            error_dict['e_a_007-a'] = f'会員数の入力欄に数字ではないデータが入力されている:{error_at_num_of_members_column}'
        else:
            print('会員数の入力に問題が無い')

        error_at_num_of_annual_fee_members_column = []
        for col in num_of_annual_fee_members_column:
             # form_rowが空でないことと、値がNaNでないことを確認してから型をチェック
            if not application_row.empty and not pd.isna(application_row[col].iloc[0]) and not isinstance(application_row[col].iloc[0], (int, float)): # floatも許容する
                error_at_num_of_annual_fee_members_column.append(col)
        if error_at_num_of_annual_fee_members_column:
            error_dict['e_a_007-b'] = f'年会費等を支払っている会員数の入力欄に数字ではないデータが入力されている:{error_at_num_of_annual_fee_members_column}'
        else:
            print('年会費を払っている会員数の入力に問題が無い')
    else:
        print("警告: check_number_of_members 関数に空のapplication_rowが渡されました。")
        error_dict['e_a_007-c'] = '会員数の入力が空です。'
    return error_dict

# 定期的な活動が2種目以上かをチェックする関数
def check_number_of_disciplines(application_row):
    """
    定期的な活動が2種目以上かをチェックします。
    """
    error_dict = {}

    # 種目リストのcsvファイルを読み込み
    try:
        disciplines_df = pd.read_csv('list_of_disciplines.csv')
    except FileNotFoundError:
        print("list_of_disciplines.csv が見つかりません。")
        return error_dict

    # disciplines_dfの['disciplines']から種目のカラムを取得
    if 'disciplines' in disciplines_df.columns:
        disciplines_columns_for_disciplines = disciplines_df['disciplines'].tolist()
    else:
        print("list_of_disciplines.csv に 'disciplines' カラムが見つかりません。")
        return error_dict

    # 種目のカラムを修正（'申請_種目_'を付記）
    disciplines_columns = [f'申請_種目_{discipline}' for discipline in disciplines_columns_for_disciplines]

    if not application_row.empty:
        extra_disciplines_column = '申請_種目_その他_数(選択時必須)'
        count_of_disciplines = 0
        # 各種目カラムをループし、「定期的に行っている」が選択されているかを確認
        for col in disciplines_columns:
            if col in application_row.columns and application_row[col].iloc[0] == '定期的に行っている':
                count_of_disciplines += 1

        # リストに含まれていない種目について処理
        if '申請_種目_その他' in application_row.columns and application_row['申請_種目_その他'].iloc[0] == '定期的に行っている':
            # リスト外の活動種目数の項目に数字が入力されているかをチェック
            extra_num = application_row[extra_disciplines_column].iloc[0]
            if pd.isna(extra_num) or not isinstance(extra_num, (int, float)):
                error_dict['e_a_008-b'] = 'リスト外の活動種目数の項目に数字が入力されていない'
            else:
                count_of_disciplines += int(extra_num)

        # 2種目以上かを確認する
        if count_of_disciplines < 2:
            error_dict['e_a_008-a'] = f'定期的に活動を2種目以上行っていない: {count_of_disciplines}種目'
        else:
            print('活動種目の入力に問題は無い')
    else:
        print("警告: check_number_of_disciplines 関数に空のapplication_rowが渡されました。")
        error_dict['e_a_008-c'] = '活動種目の入力が空です。'
    
    return error_dict

# 指導者の配置をチェックする関数（R8は、ほぼ機能なし）
def check_coaches(application_row):
    """
    指導者の配置状況をチェックします。
    """
    error_dict = {}
    if not application_row.empty:
        # 種目のカラムをdisciplines_columnとして指定
        disciplines_of_coach_column = [
            '申請_指導者_アーチェリー',
            '申請_指導者_アイスホッケー',
            '申請_指導者_アメフト',
            '申請_指導者_ウエイトリフティング',
            '申請_指導者_エアロビック',
            '申請_指導者_オリエンテーリング',
            '申請_指導者_カーリング',
            '申請_指導者_カヌー',
            '申請_指導者_空手道',
            '申請_指導者_弓道',
            '申請_指導者_グラウンド・ゴルフ',
            '申請_指導者_クレー射撃',
            '申請_指導者_ゲートボール',
            '申請_指導者_剣道',
            '申請_指導者_ゴルフ',
            '申請_指導者_サッカー',
            '申請_指導者_山岳',
            '申請_指導者_自転車競技',
            '申請_指導者_銃剣道',
            '申請_指導者_柔道',
            '申請_指導者_新体操',
            '申請_指導者_水泳',
            '申請_指導者_スキー・スノボ',
            '申請_指導者_スクーバ',
            '申請_指導者_スケート',
            '申請_指導者_クライミング',
            '申請_指導者_相撲',
            '申請_指導者_セーリング',
            '申請_指導者_ソフトテニス',
            '申請_指導者_ソフトボール',
            '申請_指導者_体操',
            '申請_指導者_体操競技',
            '申請_指導者_卓球',
            '申請_指導者_ダンススポーツ',
            '申請_指導者_チアダンス',
            '申請_指導者_チアリーディング',
            '申請_指導者_綱引',
            '申請_指導者_テニス',
            '申請_指導者_ドッジボール',
            '申請_指導者_トライアスロン',
            '申請_指導者_トランポリン',
            '申請_指導者_なぎなた',
            '申請_指導者_軟式野球',
            '申請_指導者_バイアスロン',
            '申請_指導者_バウンドテニス',
            '申請_指導者_馬術',
            '申請_指導者_バスケ',
            '申請_指導者_バドミントン',
            '申請_指導者_バレー',
            '申請_指導者_パワーリフティング',
            '申請_指導者_ハンドボール',
            '申請_指導者_フェンシング',
            '申請_指導者_フットサル',
            '申請_指導者_プロゴルフ',
            '申請_指導者_プロスキー',
            '申請_指導者_プロテニス',
            '申請_指導者_ボウリング',
            '申請_指導者_ボート',
            '申請_指導者_ボクシング',
            '申請_指導者_ホッケー',
            '申請_指導者_ボブスレー',
            '申請_指導者_ライフル射撃',
            '申請_指導者_ラグビー',
            '申請_指導者_陸上',
            '申請_指導者_レスリング'
        ]
        # 各種目カラムをループし、「配置している」が選択されているかを確認
        error_at_coach_column = []
        for col in disciplines_of_coach_column:
            if not application_row.empty and application_row[col].iloc[0] == '配置している':
                error_at_coach_column.append(col)
        # ex.配置している種目が1つもない場合はエラーとする場合
        # if error_at_coach_column:
        # # error_dict['e_a_009'] = f'指導者の配置状況に問題がある: {error_at_coach_column}'
        # else:
        # print('指導者の配置状況に問題は無い')

        print('指導者の処理が終了しました（現段階では審査に不要のため）')
    return error_dict

# マネジメント指導者資格の入力をチェックする関数
def check_managers(application_row):
  """
  クラマネ・アシマネの配置状況と人数の入力をチェックします。
  """
  error_dict = {}
  if not application_row.empty:
      # カラムを指定
      manager_column = [
          '申請_マネジャー_マネ資格_数',
          '申請_マネジャー_アシマネ資格_数',
          '申請_事務局_マネ資格_数',
          '申請_事務局_アシマネ資格_数'
      ]

      # まず配置有無を確認（配置していたら、次の処理へ）
      if application_row['申請_マネジャー_配置状況'].iloc[0] == '配置している':
          # manager_column に数字が入力されているかをチェック
          error_at_manager_num = []
          manager_num = 0
          for col in manager_column:
              value = application_row[col].iloc[0]
              if pd.isna(value) or not isinstance(value, (int, float)): # floatも許容する
                  error_at_manager_num.append(col)
              else:
                  manager_num += int(value)

          if error_at_manager_num:
              error_dict['e_a_010-a'] = f'マネジメント指導者数の入力欄に数字ではないデータが入力されている:{error_at_manager_num}'
          else:
              print('マネジメント指導者数の入力に問題が無い')

          # 現段階ではこれ以上の処理はしない
      else:
          print('マネジメント指導者は配置されていない')
  else:
      print("警告: check_managers 関数に空のapplication_rowが渡されました。")
      error_dict['e_a_010-b'] = 'マネジメント指導者の配置状況の入力が空です。'
  return error_dict

# 規約等の改廃状況を確認する関数
def check_rule_revision(application_row):
  """
  規約等の改廃に関する提出書類をチェックします。
  """
  error_dict = {}
  if not application_row.empty:
      # 改廃状況を確認
      if application_row['申請_規約_改定有無'].iloc[0] == '前年度の申請以降、改定をした':
          # 議事録が提出されているかを確認
          if not application_row['申請_規約_改定時議事録_書類(選択時必須)'].iloc[0]:
              error_dict['e_a_011-a'] = '規約等の改廃を決議した議事録が提出されていない'
          else:
              print('規約改廃時の議事録が提出されている')
          # 改正前の規約が提出されているかを確認
          if not application_row['申請_規約_改定前規約_書類(選択時必須)'].iloc[0]:
              error_dict['e_a_011-b'] = '改正前の規約等が提出されていない'
          else:
              print('規約改廃前の規約が提出されている')
      else:
          print('規約等の改廃は行われていない')
  else:
      print("警告: check_rule_revision 関数に空のapplication_rowが渡されました。")
      error_dict['e_a_011-c'] = '規約等の改廃状況の入力が空です。'
  return error_dict

# （現行の）規約等の提出確認をする関数
def check_rule_submission(application_row):
  """
  規約等の提出状況をチェックします。
  """
  error_dict = {}
  if not application_row.empty:
      # 提出の確認(新規登録なのに、提出していない場合はエラー)
      if application_row['申請_規約_提出有無'].iloc[0] == '提出しない' and application_row['申請_申請種別'].iloc[0] == '新規（R7年度には登録していない）':
          error_dict['e_a_012-a'] = '新規登録なのに、規約等の提出がされていない'
      # 更新で、改正済みなのに、提出していない場合はエラー
      elif application_row['申請_規約_提出有無'].iloc[0] == '提出しない' and application_row['申請_申請種別'].iloc[0] == '更新（R7年度に登録済み）' and application_row['申請_規約_改定有無'].iloc[0] == '前年度の申請以降、改定をした':
          error_dict['e_a_012-b'] = '更新で、改正済みなのに、提出していない'
      # 提出する場合は、提出されているかを確認
      elif application_row['申請_規約_提出有無'].iloc[0] == '提出する':
          # 提出状況の確認
          if not application_row['申請_規約_書類(選択時必須)'].iloc[0]: # Googleフォームのファイルのアップロード項目はファイルがアップロードされるとFalse以外になることを想定
              error_dict['e_a_012-c'] = '規約等の提出がされていない'
          else:
              print('規約の提出に問題が無い')
      else:
          print('規約は提出されていないが、更新のため問題は無い（前年度に提出された議事録に問題が無いかを確認する必要がある）')
          # ここに、手動での確認表に追記するような処理を挿入する
  else:
      print("警告: check_rule_submission 関数に空のapplication_rowが渡されました。")
      error_dict['e_a_012-d'] = '規約等の提出状況の入力が空です。'
  return error_dict

# 役員名簿（議決権保有者名簿）の提出をチェックする関数
def check_officer_list_submission(application_row):
  """
  役員名簿（議決権保有者名簿）の提出状況をチェックします。
  """
  error_dict = {}
  if not application_row.empty:
      # 提出の確認(新規登録なのに、提出していない場合はエラー)
      if application_row['申請_役員名簿_提出有無'].iloc[0] == '提出しない' and application_row['申請_申請種別'].iloc[0] == '新規（R7年度には登録していない）':
          error_dict['e_a_013-a'] = '新規登録なのに、役員名簿（議決権保有者名簿）の提出がされていない'
      # 更新で、改正済みなのに、提出していない場合はエラー
      elif application_row['申請_役員名簿_提出有無'].iloc[0] == '提出しない' and application_row['申請_申請種別'].iloc[0] == '更新（R7年度に登録済み）':
          error_dict['e_a_013-b'] = '更新なのに、提出していない'
      # 提出する場合は、提出されているかを確認
      elif application_row['申請_役員名簿_提出有無'].iloc[0] == '提出する':
          # 提出状況の確認
          if not application_row['申請_役員名簿_書類(選択時必須)'].iloc[0]:
              error_dict['e_a_013-c'] = '役員名簿（議決権保有者名簿）の提出がされていない'
          else:
              print('役員名簿の提出に問題が無い')
  else:
      print("警告: check_officer_list_submission 関数に空のapplication_rowが渡されました。")
      error_dict['e_a_013-d'] = '役員名簿の提出状況の入力が空です。'
  return error_dict

# 事業計画とそれを決議した議事録の提出状況を確認する関数
def check_business_plan_submission(application_row):
  """
  事業計画と決議した議事録の提出状況をチェックします。
  """
  error_dict = {}
  if not application_row.empty:
      # 事業計画が提出されているかを確認
      if not application_row['申請_事業計画_書類'].iloc[0]: 
          error_dict['e_a_014-a'] = '事業計画が提出されていない'
      else:
          print('事業計画が提出されている')
      # 事業計画を決議した際の議事録が提出されているかを確認
      if not application_row['申請_事業計画_議事録_書類'].iloc[0]: 
          error_dict['e_a_014-b'] = '事業計画を決議した議事録が提出されていない'
      else:
          print('事業計画を決議した議事録が提出されている')
  else:
      print("警告: check_business_plan_submission 関数に空のapplication_rowが渡されました。")
      error_dict['e_a_014-c'] = '事業計画の提出状況の入力が空です。'
  return error_dict

# 予算とそれを決議した議事録の提出状況を確認する関数
def check_budget_submission(application_row):
  """
  予算と決議した議事録の提出状況をチェックします。
  """
  error_dict = {}
  if not application_row.empty:
      # 予算が提出されているかを確認
      if not application_row['申請_予算_書類'].iloc[0]:
          error_dict['e_a_015-a'] = '予算が提出されていない'
      else:
          print('予算が提出されている')
      # 予算を決議した際の議事録が提出されているかを確認
      if not application_row['申請_予算_議事録_書類'].iloc[0]: 
          error_dict['e_a_015-b'] = '予算を決議した議事録が提出されていない'
      else:
          print('予算を決議した議事録が提出されている')
  else:
      print("警告: check_budget_submission 関数に空のapplication_rowが渡されました。")
      error_dict['e_a_015-c'] = '予算の提出状況の入力が空です。'
  return error_dict

# 事業報告とそれを決議した議事録の提出状況を確認する関数
def check_business_report_submission(application_row,today_date):
  """
  事業報告と決議した議事録の提出状況をチェックします。
  今年度新設クラブの場合は免除されます。
  """
  error_dict = {}
  if not application_row.empty:
      # 1年前の日付を計算
      one_year_ago = today_date - timedelta(days=365) # 厳密には年度で判定すべきですが、ここでは1年前としています

      is_new_club = False
      if not pd.isna(application_row['申請_設立日'].iloc[0]):
          try:
              establishment_date = pd.to_datetime(application_row['申請_設立日'].iloc[0]).date()
              if establishment_date >= one_year_ago:
                  is_new_club = True
          except ValueError:
              print(f"警告: クラブ設立日のフォーマットが不正です: {application_row['申請_設立日'].iloc[0]}")
              error_dict['e_a_016-d'] = 'クラブ設立日のフォーマットが不正です。'

      if application_row['申請_事業報告_提出有無'].iloc[0] == '今年度新設されたクラブのため、提出しない' and not is_new_club:
          error_dict['e_a_016-a'] = '昨年度以前の設立クラブだが、事業報告が提出されていない'
      # 提出がなされているかをチェック
      elif application_row['申請_事業報告_提出有無'].iloc[0] == '提出する':
          if not application_row['申請_事業報告_事業報告_書類(選択時必須)'].iloc[0]:
              error_dict['e_a_016-b'] = '事業報告が提出されていない'
          else:
              print('事業報告が提出されている')
          if not application_row['申請_事業報告_議事録_書類(選択時必須)'].iloc[0]: 
              error_dict['e_a_016-c'] = '事業報告を決議した議事録が提出されていない'
          else:
              print('事業報告を決議した議事録が提出されている')
      else:
          print('事業報告は提出されていないが、今年度新設クラブのため問題は無い（処理にエラーがある可能性や、クラブの事業年度上は2年目に突入している可能性を確認する必要がある）')
          # ここに、手動での確認表に追記するような処理を挿入する
  else:
      print("警告: check_business_report_submission 関数に空のapplication_rowが渡されました。")
      error_dict['e_a_016-e'] = '事業報告の提出状況の入力が空です。'
  return error_dict

# 決算とそれを決議した議事録の提出状況を確認する関数
def check_financial_statement_submission(application_row, today_date):
  """
  決算と決議した議事録の提出状況をチェックします。
  今年度新設クラブの場合は免除されます。
  """
  error_dict = {}
  if not application_row.empty:
      # 今年度新設クラブは未提出が許されるので、未提出かつ新設かをチェック
      one_year_ago = today_date - timedelta(days=365) # 厳密には年度で判定すべきですが、ここでは1年前としています

      is_new_club = False
      if not pd.isna(application_row['申請_設立日'].iloc[0]):
          try:
              establishment_date = pd.to_datetime(application_row['申請_設立日'].iloc[0]).date()
              if establishment_date >= one_year_ago:
                  is_new_club = True
          except ValueError:
              print(f"警告: クラブ設立日のフォーマットが不正です: {application_row['申請_設立日'].iloc[0]}")
              error_dict['e_a_017-d'] = 'クラブ設立日のフォーマットが不正です。'

      if application_row['申請_決算_提出有無'].iloc[0] == '今年度新設されたクラブのため、提出しない' and not is_new_club:
          error_dict['e_a_017-a'] = '昨年度以前の設立クラブだが、決算が提出されていない'
      elif application_row['申請_決算_提出有無'].iloc[0] == '提出する':
          if not application_row['申請_決算_書類(選択時必須)'].iloc[0]:
              error_dict['e_a_017-b'] = '決算が提出されていない'
          else:
              print('決算が提出されている')
          if not application_row['申請_決算_議事録_書類(選択時必須)'].iloc[0]:
              error_dict['e_a_017-c'] = '決算を決議した議事録が提出されていない'
          else:
              print('決算を決議した議事録が提出されている')
      else:
          print('決算は提出されていないが、今年度新設クラブのため問題は無い（処理にエラーがある可能性や、クラブの事業年度上は2年目に突入している可能性を確認する必要がある）')
          # ここに、手動での確認表に追記するような処理を挿入する
  else:
      print("警告: check_financial_statement_submission 関数に空のapplication_rowが渡されました。")
      error_dict['e_a_017-e'] = '決算の提出状況の入力が空です。'
  return error_dict

# チェックシートの提出状況を確認する関数
def check_checklist_submission(application_row):
  """
  チェックシートの提出状況をチェックします。
  """
  error_dict = {}
  if not application_row.empty:
      if not application_row['申請_自己点検シート_書類'].iloc[0]: # Googleフォームのファイルのアップロード項目はファイルがアップロードされるとFalse以外になることを想定
          error_dict['e_a_018-a'] = 'チェックシートが提出されていない'
      else:
          print('チェックシートが提出されている')
          # 内容に問題が無いかをチェックする機能を今後追加
  else:
      print("警告: check_checklist_submission 関数に空のapplication_rowが渡されました。")
      error_dict['e_a_018-b'] = 'チェックシートの提出状況の入力が空です。'
  return error_dict

# 自己説明・公表確認書の提出状況を確認する関数
def check_self_explanation_submission(application_row):
  """
  自己説明・公表確認書の提出状況をチェックします。
  """
  error_dict = {}
  if not application_row.empty:
      if not application_row['申請_自己説明_書類'].iloc[0]: # Googleフォームのファイルのアップロード項目はファイルがアップロードされるとFalse以外になることを想定
          error_dict['e_a_019-a'] = '自己説明・公表確認書が提出されていない'
      else:
          print('自己説明・公表確認書が提出されている')
          # 内容に問題が無いかをチェックする機能を今後追加
  else:
      print("警告: check_self_explanation_submission 関数に空のapplication_rowが渡されました。")
      error_dict['e_a_019-b'] = '自己説明・公表確認書の提出状況の入力が空です。'
  return error_dict

# クラブごとの自動チェックを行う関数
def perform_automatic_checks(club_name, application_data_df, checklist_folder_path, checklist_create_df, timestamp):
    """
    指定されたクラブに対して自動チェックを行います。

    Args:
        club_name (str): チェックを行うクラブ名。
        application_data_df (pd.DataFrame): 申請内容を含むDataFrame（マージ済みの club_list_df）。
        checklist_folder_path (str): チェックリストが保存されているフォルダパス。
        checklist_create_df (pd.DataFrame): チェックリスト作成状況を含むDataFrame。
        timestamp (str): 現在のタイムスタンプ（yyyymmddHHMMSS形式）。

    Returns:
        None: チェック結果はチェックリストファイルに書き込まれます。
    """
    print(f"クラブ名: {club_name}")

    # 申請日時を取得（checklist_create_df から）
    # checklist_create_df にクラブ名が存在することを確認
    if club_name not in checklist_create_df['クラブ名'].values:
        print(f"警告: クラブ名 '{club_name}' はチェックリスト作成状況に見つかりませんでした。このクラブの処理をスキップします。")
        return

    application_date_str_from_checklist = checklist_create_df.loc[checklist_create_df['クラブ名'] == club_name, '申請日時'].iloc[0]
    checklist_creation_date_str = checklist_create_df.loc[checklist_create_df['クラブ名'] == club_name, 'チェックリスト作成日時'].iloc[0]

    print(f"申請日時 (from checklist): {application_date_str_from_checklist}")
    print(f"チェックリスト作成日時: {checklist_creation_date_str}")

    # 対象クラブのチェックリストを読み込み
    # row['申請日時']をyyyymmddhhmmssに変換
    try:
        # checklist_create_dfに保存されている申請日時が文字列の場合を考慮
        if isinstance(application_date_str_from_checklist, str):
             application_date_from_checklist = datetime.strptime(application_date_str_from_checklist, '%Y-%m-%d %H:%M:%S')
        else: # datetime型の場合
             application_date_from_checklist = application_date_str_from_checklist
        application_date_str_yyyymmddHHMMSS = str(application_date_from_checklist)
    except ValueError:
        print(f"エラー: クラブ '{club_name}' の申請日時のフォーマットが不正です: {application_date_str_from_checklist}")
        return

    checklist_file_name = f"{club_name}_申請{application_date_str_yyyymmddHHMMSS}_作成{checklist_creation_date_str}.csv"
    checklist_file_path = os.path.join(checklist_folder_path, checklist_file_name)
    print(f"チェックリストファイルパス: {checklist_file_path}")
    print(f"チェックリストの読み込みを開始しました: {club_name}")

    # チェックリストファイルが存在するかどうかを確認
    if not os.path.exists(checklist_file_path):
        print(f"警告: チェックリストファイル '{checklist_file_path}' が見つかりませんでした。このクラブの処理をスキップします。")
    
    try:
        checklist_df = pd.read_csv(checklist_file_path)
    except Exception as e:
        print(f"エラー: チェックリストファイル '{checklist_file_path}' の読み込み中にエラーが発生しました: {e}")
    print('チェックリストファイルが見つかりました')

    # application_data_dfから現在のクラブの行を取得
    print(application_data_df)
    print(application_data_df.head)
    print(application_data_df['クラブ名'])
    application_row = application_data_df.loc[application_data_df['クラブ名'] == club_name]

    if application_row.empty:
        print(f"警告: クラブ名 '{club_name}' は申請内容を含むデータに見つかりませんでした。このクラブの処理をスキップします。")
        return
    else:
        print('クラブ名が申請内容に存在')

    # 入力エラーが無いかを記載していくための辞書を作成（まずは空）
    error_dict = {}

    # 日本の現在時刻を取得
    jst_now = datetime.now(timezone(timedelta(hours=9)))

    # 今日の日付を取得
    today_date = jst_now.date()

    # チェック項目を関数に分割し、呼び出す
    # 各チェック関数に application_row を渡すように変更
    error_dict.update(check_must_columns(application_row))
    error_dict.update(check_submitting_now(application_row))
    error_dict.update(check_club_location(application_row))
    error_dict.update(check_phone_number(application_row))
    error_dict.update(check_fax_number(application_row))
    # check_application_type 関数には application_data_df を渡す
    error_dict.update(check_application_type(application_row, application_data_df, club_name))
    error_dict.update(check_standard_compliance(application_row))
    error_dict.update(check_number_of_members(application_row))
    error_dict.update(check_number_of_disciplines(application_row))
    # error_dict.update(check_coaches(application_row)) # 現段階では不要
    error_dict.update(check_managers(application_row))
    error_dict.update(check_rule_revision(application_row))
    error_dict.update(check_rule_submission(application_row))
    error_dict.update(check_officer_list_submission(application_row))
    error_dict.update(check_business_plan_submission(application_row))
    error_dict.update(check_budget_submission(application_row))
    error_dict.update(check_business_report_submission(application_row,today_date))
    error_dict.update(check_financial_statement_submission(application_row,today_date))
    error_dict.update(check_checklist_submission(application_row))
    error_dict.update(check_self_explanation_submission(application_row))

    # error_dictが空の時は、問題が無いことを示すメッセージを追加
    if not error_dict:
        error_dict['info'] = '自動チェックで問題は見つかりませんでした。'
    else:
        # エラーがある場合は、infoキーを追加してエラーメッセージを記載
        print('自動チェックで問題が見つかりました。')

    # 一旦、チェックリストをprint
    print(f"チェック結果: {error_dict}")

    # 自動でチェックした内容をチェックリストに書き出し(チェックリストの上書き）
    # error_dictが空の場合は空文字列を書き込む
    checklist_df['自動チェック'] = str(error_dict) if error_dict else ''
    checklist_df['自動チェック更新時間'] = datetime.now(timezone(timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S')

    # 追記したカラムをチェック
    print(checklist_df[['自動チェック','自動チェック更新時間']].iloc[0])

    # チェックリストファイルを保存
    try:
        checklist_df.to_csv(checklist_file_path, index=False)
        print(f"チェックリストファイル '{checklist_file_path}' を更新しました。")
    except Exception as e:
        print(f"エラー: チェックリストファイル '{checklist_file_path}' の書き込み中にエラーが発生しました: {e}")

# チェック処理の実行部分
# 必要なデータを読み込み
folder_of_checklist_create_status = os.path.join('R7_登録申請処理', '申請入力内容')
file_of_checklist_create_status = os.path.join(folder_of_checklist_create_status, 'クラブごとのチェックリスト作成状況.csv')

# ディレクトリがなければ作成
if not os.path.exists(folder_of_checklist_create_status):
    os.makedirs(folder_of_checklist_create_status, exist_ok=True)

if os.path.exists(file_of_checklist_create_status):
    checklist_create_df = pd.read_csv(file_of_checklist_create_status)
    print('クラブごとのチェックリスト作成状況.csvはすでに存在しています')
else:
    checklist_create_df = pd.DataFrame(columns=['クラブ名','申請日時', 'チェックリスト作成日時'])
    checklist_create_df.to_csv(file_of_checklist_create_status, index=False)
    print('クラブごとのチェックリスト作成状況.csvが作成されました')

# クラブリストを読み込み
# クラブリスト_{timestamp}.csvを読み込む
# folderを参照して、最新のクラブリストを探す
foldr_path = os.path.join('R7_登録申請処理','申請受付リスト')
latest_file = max([os.path.join(foldr_path, f) for f in os.listdir(foldr_path)], key=os.path.getctime)

# 最新のクラブリストを読み込む
club_list_df = pd.read_csv(latest_file)

try:
    club_list_df = pd.read_csv(latest_file)
    # タイムスタンプをdatetime型に変換
    club_list_df['R8年度登録申請_タイムスタンプ'] = pd.to_datetime(club_list_df['R8年度登録申請_タイムスタンプ'], errors='coerce')
    club_list_df['R8年度登録申請_タイムスタンプyyyymmddHHMMSS'] = club_list_df['R8年度登録申請_タイムスタンプ'].dt.strftime('%Y%m%d%H%M%S')
    print("申請内容の読み込みが完了しました")
except Exception as e:
    print(f"申請内容の読み込み中にエラーが発生しました: {e}")

# チェックリストのフォルダを指定
checklist_folder_path = os.path.join('R7_登録申請処理','申請入力内容')

# timestampを定義（日本時間の現在時刻をyyyymmddHHMMSS形式で取得）
timestamp = datetime.now(timezone(timedelta(hours=9))).strftime('%Y%m%d%H%M%S')

# クラブリストの各行に対して自動チェックを実行
# checklist_create_df をイテレートして、各クラブに対してチェックを実行
for index, row in checklist_create_df.iterrows():
    club_name = row['クラブ名']
    print(f"クラブ名: {club_name} の自動チェックを開始します")
    perform_automatic_checks(club_name, club_list_df, checklist_folder_path, checklist_create_df, timestamp)
    print(f"クラブ名: {club_name} の自動チェックが完了しました\n")

print('全てのクラブの自動チェックが完了しました。')

# 5. 人間がチェックする用のリストを作成
## 必要なデータの読み込み
# 申請内容の読み込み
acceptance_file_path = os.path.join('R7_登録申請処理','申請受付リスト')
acceptance_latest_file = max([os.path.join(acceptance_file_path, f) for f in os.listdir(acceptance_file_path)], key=os.path.getctime)
acceptance_club_list_df = pd.read_csv(acceptance_latest_file)

# チェックリスト作成状況のリスト読み込み
checklist_folder_path = os.path.join('R7_登録申請処理', '申請入力内容')
checklist_file_name = 'クラブごとのチェックリスト作成状況.csv'
checklist_file_path = os.path.join(checklist_folder_path, checklist_file_name)
checklist_create_df = pd.read_csv(checklist_file_path)

## 書類ごとの内容
# 書類1に関するチェックリストを作成する関数
def make_document1_checklist_for_human(applicastion_row_for_human):
    """
    書類1に関する人間がチェックするためのチェックリストを作成します。
    """
    # チェックリストの初期化
    document1_checklist = []

    # 各クラブの行をイテレート
    for index, row in applicastion_row_for_human.iterrows():
        club_name = row['クラブ名']
        application_date = row['R8年度登録申請_タイムスタンプyyyymmddHHMMSS']
        
        # 昨年度の登録情報を基に、データを作成
        last_year_status = '登録済み' if row['R7年度登録クラブ'] == 1 else '未登録'
        
        # チェックリストの行を作成
        checklist_row = {
            'クラブ名': club_name,
            '入力されたクラブ名': row['申請_クラブ名_テキスト'],
            'チェック項目_クラブ名': '',
            '申請_法人格': row['申請_法人格'],
            'チェック項目_法人格': '',
            '申請_代表者名': row['申請_代表者名'],
            'チェック項目_代表者名': '',
            '昨年度登録状況': last_year_status,
            '申請種別': row['申請_申請種別'],
            'チェック項目_申請種別': '',
            '申請_設立日': row['申請_設立日'],
            'チェック項目_設立日': '',
            '申請_住所': row['申請_住所'],
            'チェック項目_住所': '',
            '申請_建物名(任意)': row['申請_建物名(任意)'],
            'チェック項目_建物名': '',
            '申請_電話番号': row['申請_電話番号'],
            'チェック項目_電話番号': '',
            '申請_FAX番号': row['申請_FAX番号'],
            'チェック項目_FAX番号': '',
            '申請_メールアドレス': row['申請_メールアドレス'],
            'チェック項目_メールアドレス': '',
            '申請_申請担当者名': row['申請_申請担当者名'],
            'チェック項目_申請担当者名': '',
            '申請_申請担当者役職': row['申請_申請担当者役職'],
            'チェック項目_申請担当者役職': '',
            '申請_適合状況(1)①': row['申請_適合状況(1)①'],
            'チェック項目_適合状況(1)①': '',
            '申請_適合状況(1)②': row['申請_適合状況(1)②'],
            'チェック項目_適合状況(1)②': '',
            '申請_適合状況(1)③': row['申請_適合状況(1)③'],
            'チェック項目_適合状況(1)③': '',
            '申請_適合状況(1)④': row['申請_適合状況(1)④'],
            'チェック項目_適合状況(1)④': '',
            '申請_適合状況(2)⑤': row['申請_適合状況(2)⑤'],
            'チェック項目_適合状況(2)⑤': '',
            '申請_適合状況(3)⑥': row['申請_適合状況(3)⑥'],
            'チェック項目_適合状況(3)⑥': '',
            '申請_適合状況(3)⑦': row['申請_適合状況(3)⑦'],
            'チェック項目_適合状況(3)⑦': '',
            '申請日時': application_date,
            '備考': ''
        }
        
        # checklist_create_dfから申請日時を取得
        if club_name in checklist_create_df['クラブ名'].values:
            application_date_str = checklist_create_df.loc[checklist_create_df['クラブ名'] == club_name, '申請日時'].iloc[0]
            checklist_row['申請日時'] = application_date_str
        else:
            checklist_row['申請日時'] = '不明'
        
        # チェックリストに追加
        document1_checklist.append(checklist_row)

    return document1_checklist

# 書類2_1に関するチェックリストを作成する関数
def make_document2_1_checklist_for_human(applicastion_row_for_human):
    """
    書類2_1に関する人間がチェックするためのチェックリストを作成します。
    """
    # チェックリストの初期化
    document2_1_checklist = []

    # 各クラブの行をイテレート
    for index, row in applicastion_row_for_human.iterrows():
        club_name = row['クラブ名']
        application_date = row['R8年度登録申請_タイムスタンプyyyymmddHHMMSS']
        
        # 入力内容を基に会員数を算出
        columns_of_number_of_members = [
            '申請_会員_未就_男_数',
            '申請_会員_未就_女_数',
            '申請_会員_未就_不_数',
            '申請_会員_小_男_数',
            '申請_会員_小_女_数',
            '申請_会員_小_不_数',
            '申請_会員_中_男_数',
            '申請_会員_中_女_数',
            '申請_会員_中_不_数',
            '申請_会員_高_男_数',
            '申請_会員_高_女_数',
            '申請_会員_高_不_数',
            '申請_会員_20s_男_数',
            '申請_会員_20s_女_数',
            '申請_会員_20s_不_数',
            '申請_会員_30s_男_数',
            '申請_会員_30s_女_数',
            '申請_会員_30s_不_数',
            '申請_会員_40s_男_数',
            '申請_会員_40s_女_数',
            '申請_会員_40s_不_数',
            '申請_会員_50s_男_数',
            '申請_会員_50s_女_数',
            '申請_会員_50s_不_数',
            '申請_会員_60s_男_数',
            '申請_会員_60s_女_数',
            '申請_会員_60s_不_数',
            '申請_会員_70s_男_数',
            '申請_会員_70s_女_数',
            '申請_会員_70s_不_数'
        ]
        number_of_members = 0
        # 各列の値を足し合わせて会員数を算出
        for column in columns_of_number_of_members:
            if column in row and not pd.isna(row[column]):
                try:
                    number_of_members += int(row[column])
                except ValueError:
                    print(f"警告: クラブ '{club_name}' の列 '{column}' の値が整数に変換できません: {row[column]}")
                    number_of_members += 0
        # 会員数が0の場合は、'0'と記載
        if number_of_members == 0:
            number_of_members = '0'
        else:
            number_of_members = str(number_of_members)
        
        # 入力内容を基に年会費を払っている会員数を算出
        columns_of_annual_fee_members = [
            '申請_年会_未就_男_数',
            '申請_年会_未就_女_数',
            '申請_年会_未就_不_数',
            '申請_年会_小_男_数',
            '申請_年会_小_女_数',
            '申請_年会_小_不_数',
            '申請_年会_中_男_数',
            '申請_年会_中_女_数',
            '申請_年会_中_不_数',
            '申請_年会_高_男_数',
            '申請_年会_高_女_数',
            '申請_年会_高_不_数',
            '申請_年会_20s_男_数',
            '申請_年会_20s_女_数',
            '申請_年会_20s_不_数',
            '申請_年会_30s_男_数',
            '申請_年会_30s_女_数',
            '申請_年会_30s_不_数',
            '申請_年会_40s_男_数',
            '申請_年会_40s_女_数',
            '申請_年会_40s_不_数',
            '申請_年会_50s_男_数',
            '申請_年会_50s_女_数',
            '申請_年会_50s_不_数',
            '申請_年会_60s_男_数',
            '申請_年会_60s_女_数',
            '申請_年会_60s_不_数',
            '申請_年会_70s_男_数',
            '申請_年会_70s_女_数',
            '申請_年会_70s_不_数'
        ]
        number_of_annual_fee_members = 0
        # 各列の値を足し合わせて年会費を払っている会員数を算出
        for column in columns_of_annual_fee_members:
            if column in row and not pd.isna(row[column]):
                try:
                    number_of_annual_fee_members += int(row[column])
                except ValueError:
                    print(f"警告: クラブ '{club_name}' の列 '{column}' の値が整数に変換できません: {row[column]}")
                    number_of_annual_fee_members += 0
        # 年会費を払っている会員数が0の場合は、'0'と記載
        if number_of_annual_fee_members == 0:
            number_of_annual_fee_members = '0'
        else:
            number_of_annual_fee_members = str(number_of_annual_fee_members)

        # チェックリストの行を作成
        checklist_row = {
            'クラブ名': club_name,
            '会員数': number_of_members,
            '年会費を払っている会員数': number_of_annual_fee_members,
            'チェック項目_会員数': '',            
            '申請日時': application_date,
            '備考': ''
        }
        # checklist_create_dfから申請日時を取得
        if club_name in checklist_create_df['クラブ名'].values:
            application_date_str = checklist_create_df.loc[checklist_create_df['クラブ名'] == club_name, '申請日時'].iloc[0]
            checklist_row['申請日時'] = application_date_str
        else:
            checklist_row['申請日時'] = '不明'
        # チェックリストに追加
        document2_1_checklist.append(checklist_row)
    return document2_1_checklist

# 書類2_2に関するチェックリストを作成する関数
def make_document2_2_checklist_for_human(applicastion_row_for_human):
    """
    書類2_2に関する人間がチェックするためのチェックリストを作成します。
    """
    # チェックリストの初期化
    document2_2_checklist = []

    # 各クラブの行をイテレート
    for index, row in applicastion_row_for_human.iterrows():
        club_name = row['クラブ名']
        application_date = row['R8年度登録申請_タイムスタンプyyyymmddHHMMSS']
        
        # チェックリストの行を作成
        checklist_row = {
            'クラブ名': club_name,
            '申請_コーチ数': row['申請_コーチ数'],
            'チェック項目_コーチ数': '',
            '申請_マネージャー数': row['申請_マネージャー数'],
            'チェック項目_マネージャー数': '',
            '申請日時': application_date,
            '備考': ''
        }
        # checklist_create_dfから申請日時を取得
        if club_name in checklist_create_df['クラブ名'].values:
            application_date_str = checklist_create_df.loc[checklist_create_df['クラブ名'] == club_name, '申請日時'].iloc[0]
            checklist_row['申請日時'] = application_date_str
        else:
            checklist_row['申請日時'] = '不明'
        # チェックリストに追加
        document2_2_checklist.append(checklist_row)
    return document2_2_checklist

# ファイル名作成関数
def make_checklist_filename(club_name, application_date_str, checklist_creation_date_str):
    # 余計な空白や改行を除去
    club_name = str(club_name).strip()
    return f"{club_name}_申請{application_date_str}_作成{checklist_creation_date_str}.csv"

# 実装するべき機能
# 更新かつ、規約等改正無しかつ、規約等の提出が無い場合は、チェック項目を追加
# 事業報告・決算を新設としたクラブは、設立年と事業年度をチェック

# 書類間の整合性チェックリスト

# 担当者登録基準最終チェック

# 6. 人間がチェックしたチェックリストを基にクラブごとのチェックリストを更新

# 7. チェックリストの更新をクラブリストに反映

# 8. 人間がチェックした書類間の整合性チェックリストを基にクラブごとのチェックリストを更新

# 9. クラブごとのチェックリストを基に、クラブリストを更新

# 10. 人間がチェックした担当者登録基準最終チェックリストを基にクラブごとのチェックリストを更新

# 11. クラブごとのチェックリストを基に、クラブリストを更新

# 12. クラブごとに審査結果を出力

# ここまでの処理が完了したら、処理が終了したことを通知
print('処理が終了しました')