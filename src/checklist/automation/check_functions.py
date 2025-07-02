import pandas as pd
import pandas as pd
from datetime import timedelta
import logging
from datetime import datetime, timezone
import os

# ログの設定
logging.basicConfig(
    level=logging.DEBUG,
    encoding='utf-8',
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# 必須項目に入力があるかをチェックする関数
def check_must_columns(form_row):
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
    must_column = [col for col in form_row.columns if col not in not_must_column]

    # 必須のカラムが空白（NaN）ではないかをチェック
    if form_row[must_column].isna().any().any():
        error_at_must_column = []
        for col in must_column:
            if not form_row.empty and pd.isna(form_row[col].iloc[0]):
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
def check_reception_type(reception_row, reception_data_df, club_name):
    error_dict = {}
    if not reception_row.empty:
        # まずクラブ名を正規化
        reception_data_df['クラブ名'] = reception_data_df['クラブ名'].astype(str).str.strip()
        club_name = str(club_name).strip()
        # ここで抽出
        reception_data_match_row = reception_data_df[reception_data_df['クラブ名'] == club_name]
        print("reception_data_match_row columns:", reception_data_match_row.columns.tolist())
        print("reception_data_match_row head:", reception_data_match_row.head())
        # カラム名のバリエーションに対応
        r7_col = None
        for col in reception_data_match_row.columns:
            if col.startswith('R7年度登録クラブ'):
                r7_col = col
                break
        if r7_col is None:
            print("R7年度登録クラブカラムが見つかりません:", reception_data_match_row.columns.tolist())
            error_dict['e_a_005-d'] = 'R7年度登録クラブカラムが見つかりません'
            return error_dict
        # 以降は r7_col を使って参照
        if reception_row['申請_申請種別'].iloc[0] == '新規（R7年度には登録していない）' and reception_data_match_row[r7_col].iloc[0] == 1:
            error_dict['e_a_005-a'] = 'R7年度の登録クラブだが、新規登録として申請されている'
        elif reception_row['申請_申請種別'].iloc[0] == '更新（R7年度に登録済み）' and reception_data_match_row[r7_col].iloc[0] == 0:
            error_dict['e_a_005-b'] = 'R7年度の登録クラブではないが、更新として申請されている'
        else:
            print('申請種別が正しい')
    else:
        logging.info(f"クラブ名 '{club_name}' に一致する行が見つかりませんでした。候補一覧:")
        print(reception_data_df['クラブ名'].unique())
        logging.warning(f"クラブ名 '{club_name}' は申請内容を含むデータに見つかりませんでした。")
        error_dict['e_a_005-c'] = f'クラブ名 {club_name} が申請内容に見つかりませんでした。'
    return error_dict

# 基準適合状況の入力を確認する関数
def check_standard_compliance(reception_row):
    """
    基準適合状況について全て「適合している」となっているかをチェックします。
    （R8は(1)③については経過措置のためチェックを排除）
    """
    error_dict = {}
    if not reception_row.empty:
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
        error_at_standard_column = [col for col in standard_column if not reception_row.empty and reception_row[col].iloc[0] == '適合していない']
        if error_at_standard_column:
             error_dict['e_a_006-a'] = f'登録基準に適合していない:{error_at_standard_column}'
        else:
            print('基準に適合している')
    else:
        print("警告: check_standard_compliance 関数に空のreception_rowが渡されました。")
        error_dict['e_a_006-b'] = '基準適合状況の入力が空です。'
    return error_dict

# 会員数の入力をチェックする関数
def check_number_of_members(reception_row):
    """
    会員数に関するカラムに数字が記入されているかをチェックします。
    """
    error_dict = {}
    if not reception_row.empty:
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
            if not reception_row.empty and not pd.isna(reception_row[col].iloc[0]) and not isinstance(reception_row[col].iloc[0], (int, float)): # floatも許容する
                error_at_num_of_members_column.append(col)
        if error_at_num_of_members_column:
            error_dict['e_a_007-a'] = f'会員数の入力欄に数字ではないデータが入力されている:{error_at_num_of_members_column}'
        else:
            print('会員数の入力に問題が無い')

        error_at_num_of_annual_fee_members_column = []
        for col in num_of_annual_fee_members_column:
             # form_rowが空でないことと、値がNaNでないことを確認してから型をチェック
            if not reception_row.empty and not pd.isna(reception_row[col].iloc[0]) and not isinstance(reception_row[col].iloc[0], (int, float)): # floatも許容する
                error_at_num_of_annual_fee_members_column.append(col)
        if error_at_num_of_annual_fee_members_column:
            error_dict['e_a_007-b'] = f'年会費等を支払っている会員数の入力欄に数字ではないデータが入力されている:{error_at_num_of_annual_fee_members_column}'
        else:
            print('年会費を払っている会員数の入力に問題が無い')
    else:
        print("警告: check_number_of_members 関数に空のreception_rowが渡されました。")
        error_dict['e_a_007-c'] = '会員数の入力が空です。'
    return error_dict

# 定期的な活動が2種目以上かをチェックする関数
def check_number_of_disciplines(reception_row):
    """
    定期的な活動が2種目以上かをチェックします。
    """
    error_dict = {}

    # 種目リストのxlsxファイルを読み込み
    try:
        disciplines_df = pd.read_excel('list_of_disciplines.xlsx')
    except FileNotFoundError:
        print("list_of_disciplines.xlsx が見つかりません。")
        return error_dict

    # disciplines_dfの['disciplines']から種目のカラムを取得
    if 'disciplines' in disciplines_df.columns:
        disciplines_columns_for_disciplines = disciplines_df['disciplines'].tolist()
    else:
        print("list_of_disciplines.xlsx に 'disciplines' カラムが見つかりません。")
        return error_dict

    # 種目のカラムを修正（'申請_種目_'を付記）
    disciplines_columns = [f'申請_種目_{discipline}' for discipline in disciplines_columns_for_disciplines]

    if not reception_row.empty:
        extra_disciplines_column = '申請_種目_その他_数(選択時必須)'
        count_of_disciplines = 0
        # 各種目カラムをループし、「定期的に行っている」が選択されているかを確認
        for col in disciplines_columns:
            if col in reception_row.columns and reception_row[col].iloc[0] == '定期的に行っている':
                count_of_disciplines += 1

        # リストに含まれていない種目について処理
        if '申請_種目_その他' in reception_row.columns and reception_row['申請_種目_その他'].iloc[0] == '定期的に行っている':
            # リスト外の活動種目数の項目に数字が入力されているかをチェック
            extra_num = reception_row[extra_disciplines_column].iloc[0]
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
        print("警告: check_number_of_disciplines 関数に空のreception_rowが渡されました。")
        error_dict['e_a_008-c'] = '活動種目の入力が空です。'
    
    return error_dict

# 指導者の配置をチェックする関数（R8は、ほぼ機能なし）
def check_coaches(reception_row):
    """
    指導者の配置状況をチェックします。
    """
    error_dict = {}
    if not reception_row.empty:
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
            if not reception_row.empty and reception_row[col].iloc[0] == '配置している':
                error_at_coach_column.append(col)
        # ex.配置している種目が1つもない場合はエラーとする場合
        # if error_at_coach_column:
        # # error_dict['e_a_009'] = f'指導者の配置状況に問題がある: {error_at_coach_column}'
        # else:
        # print('指導者の配置状況に問題は無い')

        print('指導者の処理が終了しました（現段階では審査に不要のため）')
    return error_dict

# マネジメント指導者資格の入力をチェックする関数
def check_managers(reception_row):
  """
  クラマネ・アシマネの配置状況と人数の入力をチェックします。
  """
  error_dict = {}
  if not reception_row.empty:
      # カラムを指定
      manager_column = [
          '申請_マネジャー_マネ資格_数',
          '申請_マネジャー_アシマネ資格_数',
          '申請_事務局_マネ資格_数',
          '申請_事務局_アシマネ資格_数'
      ]

      # まず配置有無を確認（配置していたら、次の処理へ）
      if reception_row['申請_マネジャー_配置状況'].iloc[0] == '配置している':
          # manager_column に数字が入力されているかをチェック
          error_at_manager_num = []
          manager_num = 0
          for col in manager_column:
              value = reception_row[col].iloc[0]
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
      print("警告: check_managers 関数に空のreception_rowが渡されました。")
      error_dict['e_a_010-b'] = 'マネジメント指導者の配置状況の入力が空です。'
  return error_dict

# 規約等の改廃状況を確認する関数
def check_rule_revision(reception_row):
  """
  規約等の改廃に関する提出書類をチェックします。
  """
  error_dict = {}
  if not reception_row.empty:
      # 改廃状況を確認
      if reception_row['申請_規約_改定有無'].iloc[0] == '前年度の申請以降、改定をした':
          # 議事録が提出されているかを確認
          if not reception_row['申請_規約_改定時議事録_書類(選択時必須)'].iloc[0]:
              error_dict['e_a_011-a'] = '規約等の改廃を決議した議事録が提出されていない'
          else:
              print('規約改廃時の議事録が提出されている')
          # 改正前の規約が提出されているかを確認
          if not reception_row['申請_規約_改定前規約_書類(選択時必須)'].iloc[0]:
              error_dict['e_a_011-b'] = '改正前の規約等が提出されていない'
          else:
              print('規約改廃前の規約が提出されている')
      else:
          print('規約等の改廃は行われていない')
  else:
      print("警告: check_rule_revision 関数に空のreception_rowが渡されました。")
      error_dict['e_a_011-c'] = '規約等の改廃状況の入力が空です。'
  return error_dict

# （現行の）規約等の提出確認をする関数
def check_rule_submission(reception_row):
  """
  規約等の提出状況をチェックします。
  """
  error_dict = {}
  if not reception_row.empty:
      # 提出の確認(新規登録なのに、提出していない場合はエラー)
      if reception_row['申請_規約_提出有無'].iloc[0] == '提出しない' and reception_row['申請_申請種別'].iloc[0] == '新規（R7年度には登録していない）':
          error_dict['e_a_012-a'] = '新規登録なのに、規約等の提出がされていない'
      # 更新で、改正済みなのに、提出していない場合はエラー
      elif reception_row['申請_規約_提出有無'].iloc[0] == '提出しない' and reception_row['申請_申請種別'].iloc[0] == '更新（R7年度に登録済み）' and reception_row['申請_規約_改定有無'].iloc[0] == '前年度の申請以降、改定をした':
          error_dict['e_a_012-b'] = '更新で、改正済みなのに、提出していない'
      # 提出する場合は、提出されているかを確認
      elif reception_row['申請_規約_提出有無'].iloc[0] == '提出する':
          # 提出状況の確認
          if not reception_row['申請_規約_書類(選択時必須)'].iloc[0]: # Googleフォームのファイルのアップロード項目はファイルがアップロードされるとFalse以外になることを想定
              error_dict['e_a_012-c'] = '規約等の提出がされていない'
          else:
              print('規約の提出に問題が無い')
      else:
          print('規約は提出されていないが、更新のため問題は無い（前年度に提出された議事録に問題が無いかを確認する必要がある）')
          # ここに、手動での確認表に追記するような処理を挿入する
  else:
      print("警告: check_rule_submission 関数に空のreception_rowが渡されました。")
      error_dict['e_a_012-d'] = '規約等の提出状況の入力が空です。'
  return error_dict

# 役員名簿（議決権保有者名簿）の提出をチェックする関数
def check_officer_list_submission(reception_row):
  """
  役員名簿（議決権保有者名簿）の提出状況をチェックします。
  """
  error_dict = {}
  if not reception_row.empty:
      # 提出の確認(新規登録なのに、提出していない場合はエラー)
      if reception_row['申請_役員名簿_提出有無'].iloc[0] == '提出しない' and reception_row['申請_申請種別'].iloc[0] == '新規（R7年度には登録していない）':
          error_dict['e_a_013-a'] = '新規登録なのに、役員名簿（議決権保有者名簿）の提出がされていない'
      # 更新で、改正済みなのに、提出していない場合はエラー
      elif reception_row['申請_役員名簿_提出有無'].iloc[0] == '提出しない' and reception_row['申請_申請種別'].iloc[0] == '更新（R7年度に登録済み）':
          error_dict['e_a_013-b'] = '更新なのに、提出していない'
      # 提出する場合は、提出されているかを確認
      elif reception_row['申請_役員名簿_提出有無'].iloc[0] == '提出する':
          # 提出状況の確認
          if not reception_row['申請_役員名簿_書類(選択時必須)'].iloc[0]:
              error_dict['e_a_013-c'] = '役員名簿（議決権保有者名簿）の提出がされていない'
          else:
              print('役員名簿の提出に問題が無い')
  else:
      print("警告: check_officer_list_submission 関数に空のreception_rowが渡されました。")
      error_dict['e_a_013-d'] = '役員名簿の提出状況の入力が空です。'
  return error_dict

# 事業計画とそれを決議した議事録の提出状況を確認する関数
def check_business_plan_submission(reception_row):
  """
  事業計画と決議した議事録の提出状況をチェックします。
  """
  error_dict = {}
  if not reception_row.empty:
      # 事業計画が提出されているかを確認
      if not reception_row['申請_事業計画_書類'].iloc[0]: 
          error_dict['e_a_014-a'] = '事業計画が提出されていない'
      else:
          print('事業計画が提出されている')
      # 事業計画を決議した際の議事録が提出されているかを確認
      if not reception_row['申請_事業計画_議事録_書類'].iloc[0]: 
          error_dict['e_a_014-b'] = '事業計画を決議した議事録が提出されていない'
      else:
          print('事業計画を決議した議事録が提出されている')
  else:
      print("警告: check_business_plan_submission 関数に空のreception_rowが渡されました。")
      error_dict['e_a_014-c'] = '事業計画の提出状況の入力が空です。'
  return error_dict

# 予算とそれを決議した議事録の提出状況を確認する関数
def check_budget_submission(reception_row):
  """
  予算と決議した議事録の提出状況をチェックします。
  """
  error_dict = {}
  if not reception_row.empty:
      # 予算が提出されているかを確認
      if not reception_row['申請_予算_書類'].iloc[0]:
          error_dict['e_a_015-a'] = '予算が提出されていない'
      else:
          print('予算が提出されている')
      # 予算を決議した際の議事録が提出されているかを確認
      if not reception_row['申請_予算_議事録_書類'].iloc[0]: 
          error_dict['e_a_015-b'] = '予算を決議した議事録が提出されていない'
      else:
          print('予算を決議した議事録が提出されている')
  else:
      print("警告: check_budget_submission 関数に空のreception_rowが渡されました。")
      error_dict['e_a_015-c'] = '予算の提出状況の入力が空です。'
  return error_dict

# 事業報告とそれを決議した議事録の提出状況を確認する関数
def check_business_report_submission(reception_row,today_date):
  """
  事業報告と決議した議事録の提出状況をチェックします。
  今年度新設クラブの場合は免除されます。
  """
  error_dict = {}
  if not reception_row.empty:
      # 1年前の日付を計算
      one_year_ago = today_date - timedelta(days=365) # 厳密には年度で判定すべきですが、ここでは1年前としています

      is_new_club = False
      if not pd.isna(reception_row['申請_設立日'].iloc[0]):
          try:
              establishment_date = pd.to_datetime(reception_row['申請_設立日'].iloc[0]).date()
              if establishment_date >= one_year_ago:
                  is_new_club = True
          except ValueError:
              logging.warning(f"クラブ設立日のフォーマットが不正です: {reception_row['申請_設立日'].iloc[0]}")
              error_dict['e_a_016-d'] = 'クラブ設立日のフォーマットが不正です。'

      if reception_row['申請_事業報告_提出有無'].iloc[0] == '今年度新設されたクラブのため、提出しない' and not is_new_club:
          error_dict['e_a_016-a'] = '昨年度以前の設立クラブだが、事業報告が提出されていない'
      # 提出がなされているかをチェック
      elif reception_row['申請_事業報告_提出有無'].iloc[0] == '提出する':
          if not reception_row['申請_事業報告_事業報告_書類(選択時必須)'].iloc[0]:
              error_dict['e_a_016-b'] = '事業報告が提出されていない'
          else:
              print('事業報告が提出されている')
          if not reception_row['申請_事業報告_議事録_書類(選択時必須)'].iloc[0]: 
              error_dict['e_a_016-c'] = '事業報告を決議した議事録が提出されていない'
          else:
              print('事業報告を決議した議事録が提出されている')
      else:
          print('事業報告は提出されていないが、今年度新設クラブのため問題は無い（処理にエラーがある可能性や、クラブの事業年度上は2年目に突入している可能性を確認する必要がある）')
          # ここに、手動での確認表に追記するような処理を挿入する
  else:
      print("警告: check_business_report_submission 関数に空のreception_rowが渡されました。")
      error_dict['e_a_016-e'] = '事業報告の提出状況の入力が空です。'
  return error_dict

# 決算とそれを決議した議事録の提出状況を確認する関数
def check_financial_statement_submission(reception_row, today_date):
  """
  決算と決議した議事録の提出状況をチェックします。
  今年度新設クラブの場合は免除されます。
  """
  error_dict = {}
  if not reception_row.empty:
      # 今年度新設クラブは未提出が許されるので、未提出かつ新設かをチェック
      one_year_ago = today_date - timedelta(days=365) # 厳密には年度で判定すべきですが、ここでは1年前としています

      is_new_club = False
      if not pd.isna(reception_row['申請_設立日'].iloc[0]):
          try:
              establishment_date = pd.to_datetime(reception_row['申請_設立日'].iloc[0]).date()
              if establishment_date >= one_year_ago:
                  is_new_club = True
          except ValueError:
              logging.warning(f"クラブ設立日のフォーマットが不正です: {reception_row['申請_設立日'].iloc[0]}")
              error_dict['e_a_017-d'] = 'クラブ設立日のフォーマットが不正です。'

      if reception_row['申請_決算_提出有無'].iloc[0] == '今年度新設されたクラブのため、提出しない' and not is_new_club:
          error_dict['e_a_017-a'] = '昨年度以前の設立クラブだが、決算が提出されていない'
      elif reception_row['申請_決算_提出有無'].iloc[0] == '提出する':
          if not reception_row['申請_決算_書類(選択時必須)'].iloc[0]:
              error_dict['e_a_017-b'] = '決算が提出されていない'
          else:
              print('決算が提出されている')
          if not reception_row['申請_決算_議事録_書類(選択時必須)'].iloc[0]:
              error_dict['e_a_017-c'] = '決算を決議した議事録が提出されていない'
          else:
              print('決算を決議した議事録が提出されている')
      else:
          print('決算は提出されていないが、今年度新設クラブのため問題は無い（処理にエラーがある可能性や、クラブの事業年度上は2年目に突入している可能性を確認する必要がある）')
          # ここに、手動での確認表に追記するような処理を挿入する
  else:
      print("警告: check_financial_statement_submission 関数に空のreception_rowが渡されました。")
      error_dict['e_a_017-e'] = '決算の提出状況の入力が空です。'
  return error_dict

# チェックシートの提出状況を確認する関数
def check_checklist_submission(reception_row):
  """
  チェックシートの提出状況をチェックします。
  """
  error_dict = {}
  if not reception_row.empty:
      if not reception_row['申請_自己点検シート_書類'].iloc[0]: # Googleフォームのファイルのアップロード項目はファイルがアップロードされるとFalse以外になることを想定
          error_dict['e_a_018-a'] = 'チェックシートが提出されていない'
      else:
          print('チェックシートが提出されている')
          # 内容に問題が無いかをチェックする機能を今後追加
  else:
      print("警告: check_checklist_submission 関数に空のreception_rowが渡されました。")
      error_dict['e_a_018-b'] = 'チェックシートの提出状況の入力が空です。'
  return error_dict

# 自己説明・公表確認書の提出状況を確認する関数
def check_self_explanation_submission(reception_row):
  """
  自己説明・公表確認書の提出状況をチェックします。
  """
  error_dict = {}
  if not reception_row.empty:
      if not reception_row['申請_自己説明_書類'].iloc[0]: # Googleフォームのファイルのアップロード項目はファイルがアップロードされるとFalse以外になることを想定
          error_dict['e_a_019-a'] = '自己説明・公表確認書が提出されていない'
      else:
          print('自己説明・公表確認書が提出されている')
          # 内容に問題が無いかをチェックする機能を今後追加
  else:
      print("警告: check_self_explanation_submission 関数に空のreception_rowが渡されました。")
      error_dict['e_a_019-b'] = '自己説明・公表確認書の提出状況の入力が空です。'
  return error_dict