import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pandas as pd
from utils.settings_loader import load_settings
import re

settings = load_settings()
this_year = settings.get("this_year", "")
prefecture_name = settings.get("prefecture_name", "")

def convert_year_label_to_seireki(year_label: str) -> int:
    """
    「令和6年度」→ 2024 のように変換
    """
    if year_label.startswith("令和"):
        n = int(year_label.replace("令和", "").replace("年度", "").replace("年", ""))
        return 2018 + n
    elif year_label.startswith("平成"):
        n = int(year_label.replace("平成", "").replace("年度", "").replace("年", ""))
        return 1988 + n
    else:
        raise ValueError(f"対応していない年度形式です: {year_label}")



def is_valid_phone_number(value):
    pattern = re.compile(r"^\d{2,4}-\d{2,4}-\d{3,4}$")
    return pattern.match(str(value)) is not None

def rule_based_check_paper1(row, club_name, club_master_dict):
    """
    書類①のチェック項目ごとに判定を行う
    """
    item = str(row.get("チェック項目", "")).strip()
    value = str(row.get("確認欄", "")).strip()
    設立年 = int(club_master_dict.get(club_name, {}).get("設立年", 0))
    提出年度 = convert_year_label_to_seireki(this_year)

    # 0.基本事項のチェック
    if item == "クラブ名":
        if not value:
            return True, "クラブ名が未記載です"
        elif value not in club_master_dict:
            return True, f"クラブ名『{value}』はクラブ名簿に存在しません"
        elif value != club_name:
            return True, f"クラブ名が名簿と一致しません（名簿：{club_name}）"
        return False, ""

    status_to_application = {
        "登録": "更新",
        "未登録": "新規"
        }

    申請区分 = row.get("申請区分")
    登録状況 = club_master_dict.get(club_name, {}).get("登録状況")

    expected = status_to_application.get(登録状況)

    if not 申請区分:
        return True, "申請区分が未記載です"
    elif expected and 申請区分 != expected:
        return True, f"申請区分が名簿と一致しません（正：{expected}）"

    elif item == "代表者氏名":
        # 代表者氏名の項目が"○"であればOK
        if not value:
            return True, "代表者氏名が未記載です"
        return False, ""

    # 1.基準適合状況のチェック    
    elif item == "分類(1)①":
        if not value:
            return True, "分類(1)①が未記載です"
        # 分類(1)①の項目が"○"であればOK
        elif value not in ["○"]:
            return True, "「分類（１）活動実態に関する基準①多種目（複数種目）のスポーツ活動を実施している。」に『○』がありません"
        return False, ""

    elif item == "分類(1)②":
        if not value:
            return True, "分類(1)②が未記載です"
        # 分類(1)②の項目が"○"であればOK
        elif value not in ["○"]:
            return True, "「分類（１）活動実態に関する基準②多世代（複数世代）を対象としている。」に『○』がありません"
        return False, ""

    # elif item == "分類(1)③": 
    # 「分類（１）活動実態に関する基準③適切なスポーツ指導者を配置している。」は審査において参照しないためコメントアウト
            #if not value:
                # return True, "分類(1)③が未記載です"
            # 分類(1)③の項目が"○"であればOK
            # elif value not in ["○"]:
                # return True, "「分類（１）活動実態に関する基準③適切なスポーツ指導者を配置している。」に『○』がありません"
            # return False, ""

    elif item == "分類(1)④":
        if not value:
            return True, "分類(1)④が未記載です"
        # 分類(1)④の項目が"○"であればOK
        elif value not in ["○"]:
            return True, "「分類（１）活動実態に関する基準④安全管理体制を整備している。」に『○』がありません"
        return False, ""
    
    elif item == "分類(2)⑤":
        if not value:
            return True, "分類(2)⑤が未記載です"
        # 分類(2)⑤の項目が"○"であればOK
        elif value not in ["○"]:
            return True, "「分類（２）活運営形態に関する基準⑤地域住民が主体的に運営している。」に『○』がありません"
        return False, ""
    
    elif item == "分類(3)⑥":
        if not value:
            return True, "分類(3)⑥が未記載です"
        # 分類(3)⑥の項目が"○"であればOK
        elif value not in ["○"]:
            return True, "「分類（３）ガバナンスに関する基準⑥規約等が意思決定機関の議決により整備され、当該規約等に基づいて運営している。」に『○』がありません"
        return False, ""

    elif item == "分類(3)⑦":
        if not value:
            return True, "分類(3)⑦が未記載です"
        # 分類(3)⑦の項目が"○"であればOK
        elif value not in ["○"]:
            return True, "「分類（３）ガバナンスに関する基準⑦事業計画・予算、事業報告・決算が、意思決定機関で議決されている。」に『○』がありません"
        return False, ""

    # 2.添付申請書類のチェック
    elif item == "申請書類②":
        if not value:
            return True, "申請書類②の提出書類欄が未記載です"
        # 添付書類の項目が"○"であればOK
        elif value not in ["○"]:
            return True, "申請書類②の「添付書類」欄に『○』がありません"
        return False, ""
    
    elif item == "申請書類③":
        # 添付書類の項目が空白の場合はclub_master_dictの一覧で、前年度の登録状況を確認するチェック
        # 申請書類③の項目が空白で、前年度の登録状況が"登録あり"であればOK
        # 申請書類③の項目が空白で、前年度の登録状況が"登録なし"であれば未記載と判断
        # 申請書類③の項目が"○"であればOK
        if not value:
            if club_master_dict["登録状況"] == "登録あり":
                return False, ""
            else:
                return True, "申請書類③の提出書類欄が未記載です"
        elif value not in ["○"]:
            return True, "申請書類③の「添付書類」欄に『○』がありません"
        return False, ""
    
    elif item == "申請書類④":
        # 添付書類の項目が空白の場合はclub_master_dictの一覧で、前年度の登録状況を確認するチェック
        # 申請書類④の項目が空白で、前年度の登録状況が"登録あり"であればOK
        # 申請書類④の項目が空白で、前年度の登録状況が"登録なし"であれば未記載と判断
        # 申請書類④の項目が"○"であればOK
        if not value:
            if club_master_dict["登録状況"] == "登録あり":
                return False, ""
            else:
                return True, "申請書類④の提出書類欄が未記載です"
        elif value not in ["○"]:
            return True, "申請書類④の「添付書類」欄に『○』がありません"
        return False, ""
    
    elif item == "申請書類⑤":
        # 添付書類の項目が"○"であればOK
        if not value:
            return True, "申請書類⑤の提出書類欄が未記載です"
        elif value not in ["○"]:
            return True, "申請書類⑤の「添付書類」欄に『○』がありません"
        return False, ""
    
    elif item == "申請書類⑥":
        # 添付書類の項目が空白の場合はこのチェックリスト内で記載されているクラブの設立年を確認するチェック
        # 申請書類⑥の項目が空白で、クラブの設立年が申請年度であればOK
        # 申請書類⑥の項目が空白で、クラブの設立年が申請年度で以前であれば未記載と判断
        # 申請書類⑥の項目が"○"であればOK
        if not value:
            if 設立年 == 提出年度:
                return False, ""
            else:
                return True, "申請書類⑥の提出書類欄が未記載です"
        elif value not in ["○"]:
            return True, "申請書類⑥の「添付書類」欄に『○』がありません"
        return False, ""
    
    elif item == "申請書類⑦":
        # 添付書類の項目が"○"であればOK
        if not value:
            return True, "申請書類⑦の提出書類欄が未記載です"
        elif value not in ["○"]:
            return True, "申請書類⑦の「添付書類」欄に『○』がありません"
        return False, ""
    
    elif item == "申請書類⑧":
        # 添付書類の項目が空白の場合はこのチェックリスト内で記載されているクラブの設立年を確認するチェック
        # 申請書類⑧の項目が空白で、クラブの設立年が申請年度であればOK
        # 申請書類⑧の項目が空白で、クラブの設立年が申請年度で以前であれば未記載と判断
        # 申請書類⑧の項目が"○"であればOK
        if not value:
            if 設立年 == 提出年度:
                return False, ""
            else:
                return True, "申請書類⑧の提出書類欄が未記載です"
        elif value not in ["○"]:
            return True, "申請書類⑧の「添付書類」欄に『○』がありません"
        return False, ""
    
    elif item == "申請書類⑨":
        # 添付書類の項目が"○"であればOK
        if not value:
            return True, "申請書類⑨の提出書類欄が未記載です"
        elif value not in ["○"]:
            return True, "申請書類⑨の「添付書類」欄に『○』がありません"
        return False, ""    
    
    # 3.連絡先情報のチェック
    elif item == "郵便番号":
        # 記載されている郵便番号が正しい形式であればOK
        if not value:
            return True, "郵便番号が未記載です"
        elif len(value) != 7 or not value.isdigit():
            return True, "郵便番号の形式が正しくありません（例：1234567）"
        return False, ""
    
    elif item == "都道府県":
        # 記載されている都道府県がprefecture_nameと同じであればOK
        if not value:
            return True, "都道府県が未記載です"
        elif value != prefecture_name:
            return True, f"都道府県が異なります（正しい都道府県名：{prefecture_name}）"
        return False, ""

    elif item == "市区町村":
        # 記載されている市区町村がclub_master_dictの一覧に記載されているものと同じであればOK
        if not value:
            return True, "市区町村が未記載です"
        elif value not in club_master_dict["市区町村"]:
            return True, f"市区町村が異なります（正しい市区町村名：{club_master_dict['市区町村']}）"
        return False, ""
    
    elif item == "住所":
        # 記載されていればOK
        if not value:
            return True, "住所が未記載です"
        return False, ""
    
    elif item == "e-mail":
        # 記載されているメールアドレスが正しい形式であればOK
        if not value:
            return True, "e-mailが未記載です"
        elif "@" not in value or "." not in value.split("@")[-1]:
            return True, "e-mailの形式が正しくありません"
        return False, ""
    
    elif check_type == "形式チェック":
        if "電話" in name and (not value or not is_valid_phone_number(value)):
            issues.append(f"{prefix}❗ {name}（{cell}）の形式が不正です。")

        elif "FAX番号" in name and (not value or not is_valid_phone_number(value)):
            issues.append(f"{prefix}❗ {name}（{cell}）の形式が不正です。")
        return False, ""
    
    elif item == "事務担当者名":
        # 記載されていればOK
        if not value:
            return True, "事務担当者名が未記載です"
        return False, ""
    
    elif item == "事務担当者役職":
        # 記載されていればOK
        if not value:
            return True, "事務担当者役職が未記載です"
        return False, ""

    # fallback
    return False, ""

def extract_errors_paper1(filepath, club_name, club_master_dict):
    import pandas as pd
    try:
        df = pd.read_excel(filepath)
    except Exception as e:
        return [{
            "クラブ名": club_name,
            "書類コード": "01",
            "書類名": "登録基準確認用紙",
            "チェック項目": "ファイル読み込みエラー",
            "備考": str(e)
        }]

    errors = []

    for _, row in df.iterrows():
        is_invalid, reason = rule_based_check_paper1(row, club_name, club_master_dict)
        if is_invalid:
            errors.append({
                "クラブ名": club_name,
                "書類コード": "01",
                "書類名": "登録基準確認用紙",
                "チェック項目": row.get("チェック項目", ""),
                "備考": reason or row.get("備考", "")
            })

    return errors