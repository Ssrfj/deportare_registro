import os
import pandas as pd
from datetime import datetime
from openpyxl import load_workbook

VERSION = "R6"  # 令和6年度版
DATE_STR = datetime.now().strftime("%Y-%m-%d")

def generate_check_template_paper_1(path=f"templates/check_paper1_registration_criteria_confirmation_formtemplate_{VERSION}.xlsx"):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # チェック対象項目の一覧
    data = [
        # 基本情報
        [1, "基本情報", "A1", "クラブ名", "空欄チェック", "○", "名簿と一致"],
        [2, "基本情報", "A3", "申請区分", "値チェック", "○", "名簿と一致（新規／更新）"],

        # 基準①〜⑦
        [3, "基準①", "A6", "多種目実施（2種目以上）", "○の有無", "○", ""],
        [4, "基準②", "A7", "多世代対象（2区分以上）", "○の有無", "○", ""],
        [5, "基準③", "A8", "指導者配置", "○の有無", "○", ""],
        [6, "基準④", "A9", "緊急連絡体制", "○の有無", "○", ""],
        [7, "基準⑤", "A10", "地域住民主体運営／非営利", "○の有無", "○", ""],
        [8, "基準⑥", "A11", "規約整備", "○の有無", "○", ""],
        [9, "基準⑦", "A12", "事業計画・決算の議決", "○の有無", "○", ""],

        # 添付書類①〜⑩
        [10, "添付書類", "A15", "申請書類① 登録基準確認用紙", "○の有無", "○", ""],
        [11, "添付書類", "A16", "申請書類② 基礎情報書類", "○の有無", "○", "データ提出必須"],
        [12, "添付書類", "A17", "申請書類③ 規約・会則・定款等", "○の有無", "条件付", "新規は必須／更新は変更時"],
        [13, "添付書類", "A18", "申請書類④ 役員名簿", "○の有無", "条件付", "新規は必須／更新は変更時"],
        [14, "添付書類", "A19", "申請書類⑤ 事業計画・予算", "○の有無", "○", ""],
        [15, "添付書類", "A20", "申請書類⑥ 事業報告・決算", "○の有無", "条件付", "創設年度クラブは不要"],
        [16, "添付書類", "A21", "申請書類⑦ 自己点検・評価", "○の有無", "○", "データ提出必須"],
        [17, "添付書類", "A22", "申請書類⑧ 議事録", "○の有無", "条件付", "⑥に関する議事録は創設年度不要"],
        [18, "添付書類", "A23", "申請書類⑨ 自己説明・公表", "○の有無", "○", ""],
        [19, "添付書類", "A24", "申請書類⑩ 独自提出物", "○の有無", "条件付", "都道府県協議会の基準次第"],

        # 連絡先
        [20, "連絡先", "A27", "フリガナ", "空欄チェック", "○", ""],
        [21, "連絡先", "A28", "担当者氏名", "空欄チェック", "○", ""],
        [22, "連絡先", "A29", "役職", "空欄チェック", "○", ""],
        [23, "連絡先", "A30", "電話番号", "形式チェック", "○", "090-xxxx-xxxx 形式"],
        [24, "連絡先", "A31", "メールアドレス", "形式チェック", "○", "`@` が含まれること"]
    ]

    df = pd.DataFrame(data, columns=["No", "セクション", "セル位置", "項目名", "チェック種別", "必須か", "備考"])
    
    # Excel書き出し（テンプレート）
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="登録基準確認用紙", index=False)

        # メタ情報のシートを追加
        meta = pd.DataFrame({
            "項目": ["バージョン", "作成日", "適用基準年度", "備考"],
            "値": [VERSION, DATE_STR, "令和6年度", "全国協議会基準2025準拠"] # 適用基準年度・備考は適宜変更
        })
        meta.to_excel(writer, sheet_name="meta", index=False)

    logging.info(f"✅ チェックテンプレート1（{VERSION}）を出力しました → {path}")

def generate_check_template_paper2_1(path=f"templates/check_paper2_1_memberships_template_{VERSION}.xlsx"):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    data = [
        [1, "事務局", "A1", "クラブ名", "空欄チェック", "○", ""],
        [2, "事務局", "A2", "設立年", "数値チェック", "○", "西暦で記入"],
        [3, "事務局", "A3", "フリガナ", "空欄チェック", "○", ""],
        [4, "事務局", "A4", "担当者氏名", "空欄チェック", "○", ""],
        [5, "事務局", "A5", "電話番号", "形式チェック", "○", "090-xxxx-xxxx"],
        [6, "事務局", "A6", "メールアドレス", "形式チェック", "○", "`@` が含まれること"],
        # ... 会員構成など（詳細は要Excel構造確認）
    ]
    df = pd.DataFrame(data, columns=["No", "セクション", "セル位置", "項目名", "チェック種別", "必須か", "備考"])

    # Excel書き出し（テンプレート）
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="登録基準確認用紙", index=False)

        # メタ情報のシートを追加
        meta = pd.DataFrame({
            "項目": ["バージョン", "作成日", "適用基準年度", "備考"],
            "値": [VERSION, DATE_STR, "令和6年度", "全国協議会基準2025準拠"] # 適用基準年度・備考は適宜変更
        })
        meta.to_excel(writer, sheet_name="meta", index=False)

    logging.info(f"✅ チェックテンプレート2-1（{VERSION}）を出力しました → {path}")

def generate_check_template_paper2_2(path=f"templates/check_paper2_2_activities_leaders_and_administration_template_{VERSION}.xlsx"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = [
        [1, "活動種目", "D3", "定期活動実施", "○の有無", "○", "12回以上の活動"],
        [2, "活動種目", "E3", "指導者配置", "○の有無", "○", ""],
        [3, "マネジャー", "G3", "クラブマネジャー配置", "○の有無", "○", "有 or 無"],
        [4, "マネジャー", "G4", "公認クラブマネジャー資格者", "数値チェック", "○", ""],
        [5, "マネジャー", "G5", "公認アシスタント資格者", "数値チェック", "○", ""]
    ]
    df = pd.DataFrame(data, columns=["No", "セクション", "セル位置", "項目名", "チェック種別", "必須か", "備考"])

    # Excel書き出し（テンプレート）
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="登録基準確認用紙", index=False)

        # メタ情報のシートを追加
        meta = pd.DataFrame({
            "項目": ["バージョン", "作成日", "適用基準年度", "備考"],
            "値": [VERSION, DATE_STR, "令和6年度", "全国協議会基準2025準拠"] # 適用基準年度・備考は適宜変更
        })
        meta.to_excel(writer, sheet_name="meta", index=False)

    logging.info(f"✅ チェックテンプレート2-2（{VERSION}）を出力しました → {path}")

def generate_check_template_paper3(path=f"templates/check_paper3_article_of_association_template_{VERSION}.xlsx"):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # 基本チェック項目
    data = [
        [1, "組織の目的", "団体の設立目的が記載されている", "□", "「地域貢献」「スポーツ振興」等"],
        [2, "会員の定義", "会員の種別が明記されている", "□", "「正会員」「準会員」等"],
        [3, "会員の定義", "会員資格の取得条件が定められている", "□", "申請・承認など"],
        [4, "会員の定義", "退会・除名の手続きが定められている", "□", "自由退会の可否、除名事由"],
        [5, "意思決定機関", "最高意思決定機関の名称が記載されている", "□", "総会、社員総会、代表者会議など"],
        [6, "意思決定機関", "構成員が誰か明記されている", "□", "会員全員、代議員など"],
        [7, "意思決定機関", "開催頻度・招集手続きが定められている", "□", "年1回以上、通知方法等"],
        [8, "意思決定機関", "成立要件（定足数）が定められている", "□", "「過半数の出席」等"],
        [9, "意思決定機関", "議決方法（賛成率など）が定められている", "□", "「過半数の賛成」等"],
        [10, "執行体制", "代表者（理事長等）の設置が明記されている", "□", "選任方法・任期含む"],
        [11, "執行体制", "理事会などの執行機関が設置されている", "□", "任意団体では設けていない場合も"],
        [12, "執行体制", "執行機関の職務・役割分担が定められている", "□", "代表・副代表・会計・監事など"],
        [13, "会計", "予算・決算に関する手続きが記載されている", "□", "予算編成、事業報告等"],
        [14, "会計", "会計監査の実施に関する規定がある", "□", "監査役、外部監査など"],
        [15, "非営利性", "非営利であることが明記されている", "□", "公益性の明示"],
        [16, "解散・残余財産", "解散の要件・手続きが明記されている", "□", "総会議決など"],
        [17, "解散・残余財産", "残余財産の帰属先が明記されている", "□", "公益団体、自治体など"]
    ]

    # 意思決定対象とその観点
    targets = [
        "規約等の改廃", "予算の決定", "事業計画の決定", "決算の承認", "事業報告の承認"
    ]
    points = [
        "意思決定機関が明記されている",
        "構成員が明記されている",
        "開催頻度・招集手続きが定められている",
        "成立要件（定足数）が定められている",
        "議決方法（賛成率など）が定められている"
    ]
    notes = [
        "総会、社員総会、代表者会議など",
        "会員全員、代議員など",
        "年1回以上、通知方法等",
        "『過半数の出席』等",
        "『過半数の賛成』等"
    ]

    no = len(data) + 1
    for category in targets:
        for i in range(len(points)):
            data.append([
                no,
                category,
                f"{category}の{points[i]}",
                "□",
                notes[i]
            ])
            no += 1

    df = pd.DataFrame(data, columns=["No", "カテゴリ", "チェック項目", "確認欄", "備考"])

    # Excel書き出し（テンプレート）
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="登録基準確認用紙", index=False)

        # メタ情報のシートを追加
        meta = pd.DataFrame({
            "項目": ["バージョン", "作成日", "適用基準年度", "備考"],
            "値": [VERSION, DATE_STR, "令和6年度", "全国協議会基準2025準拠"] # 適用基準年度・備考は適宜変更
        })
        meta.to_excel(writer, sheet_name="meta", index=False)

    logging.info(f"✅ チェックテンプレート3（{VERSION}）を出力しました → {path}")

def generate_check_template_paper4(path=f"templates/check_paper4_list_of_voting_rights_holders_template_{VERSION}.xlsx"):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    data = [
        [1, "役員情報", "氏名が明記されている", "□", "全役員に記載があるか"],
        [2, "役員情報", "居住区市町村が明記されている", "□", "例：○○市、△△町など"]
    ]

    df = pd.DataFrame(data, columns=["No", "カテゴリ", "チェック項目", "確認欄", "備考例"])
    # Excel書き出し（テンプレート）
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="登録基準確認用紙", index=False)

        # メタ情報のシートを追加
        meta = pd.DataFrame({
            "項目": ["バージョン", "作成日", "適用基準年度", "備考"],
            "値": [VERSION, DATE_STR, "令和6年度", "全国協議会基準2025準拠"] # 適用基準年度・備考は適宜変更
        })
        meta.to_excel(writer, sheet_name="meta", index=False)

    logging.info(f"✅ チェックテンプレート4（{VERSION}）を出力しました → {path}")

def generate_check_template_paper5_1_business_plan(path=f"templates/check_paper5_1_business_plan_template_{VERSION}.xlsx"):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    data = [
        [1, "活動記載", "種目ごとの活動頻度が明記されている", "□", "週◯回、月◯回など"],
        [2, "活動記載", "複数種目についての記載がある", "□", "2種目以上の活動内容が記載されている"]
    ]

    df = pd.DataFrame(data, columns=["No", "カテゴリ", "チェック項目", "確認欄", "備考例"])
    # Excel書き出し（テンプレート）
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="登録基準確認用紙", index=False)

        # メタ情報のシートを追加
        meta = pd.DataFrame({
            "項目": ["バージョン", "作成日", "適用基準年度", "備考"],
            "値": [VERSION, DATE_STR, "令和6年度", "全国協議会基準2025準拠"] # 適用基準年度・備考は適宜変更
        })
        meta.to_excel(writer, sheet_name="meta", index=False)

    logging.info(f"✅ チェックテンプレート5(事業計画書）（{VERSION}）を出力しました → {path}")

def generate_check_template_paper5_2_budget(path=f"templates/check_paper5_2_budget_template_{VERSION}.xlsx"):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    data = [
        [1, "収入・支出", "収入の内訳が明記されている", "□", "会費、補助金、助成金など"],
        [2, "収入・支出", "支出の内訳が明記されている", "□", "備品、謝金、交通費など"],
        [3, "収支バランス", "収支差額（黒字 or 赤字）が明記されている", "□", "差額の金額も含めて記載"],
        [4, "項目の具体性", "各費目に金額が記載されている", "□", "金額未記入はNG"],
        [5, "項目の具体性", "「雑費」や「その他」に多くの金額が集約されていない", "□", "具体的な用途ごとの明記が必要"],
        [6, "妥当性・透明性", "支出項目が概算でなく、理由が明示されている", "□", "「◯◯人×◯◯円」のような内訳があるか"]
    ]

    df = pd.DataFrame(data, columns=["No", "カテゴリ", "チェック項目", "確認欄", "備考例"])
    
    # Excel書き出し（テンプレート）
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="登録基準確認用紙", index=False)

        # メタ情報のシートを追加
        meta = pd.DataFrame({
            "項目": ["バージョン", "作成日", "適用基準年度", "備考"],
            "値": [VERSION, DATE_STR, "令和6年度", "全国協議会基準2025準拠"] # 適用基準年度・備考は適宜変更
        })
        meta.to_excel(writer, sheet_name="meta", index=False)
    logging.info(f"✅ チェックテンプレート5（予算書）（{VERSION}）を出力しました → {path}")


def generate_check_template_paper6_1_business_report(path=f"templates/check_paper6_1_business_report_template_{VERSION}.xlsx"):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    data = [
        [1, "報告内容", "活動種目ごとの実施状況が記載されている", "□", "実施・未実施の明記"],
        [2, "報告内容", "活動頻度・期間・場所等が具体的に記載されている", "□", "例：週1回、年間40回、○○体育館 等"]
    ]

    df = pd.DataFrame(data, columns=["No", "カテゴリ", "チェック項目", "確認欄", "備考例"])
    # Excel書き出し（テンプレート）
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="登録基準確認用紙", index=False)

        # メタ情報のシートを追加
        meta = pd.DataFrame({
            "項目": ["バージョン", "作成日", "適用基準年度", "備考"],
            "値": [VERSION, DATE_STR, "令和6年度", "全国協議会基準2025準拠"] # 適用基準年度・備考は適宜変更
        })
        meta.to_excel(writer, sheet_name="meta", index=False)
    logging.info(f"✅ チェックテンプレート6（事業報告書書）（{VERSION}）を出力しました → {path}")

def generate_check_template_paper6_2_financial_statements(path=f"templates/check_paper6_2_financial_statements_template_{VERSION}.xlsx"):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    data = [
        [1, "決算情報", "収入と支出が両方記載されている", "□", "金額の整合性含む"],
        [2, "決算情報", "収支のバランス（赤字・黒字）が明示されている", "□", "収支差額が記載されている"],
        [3, "決算情報", "支出項目が明確に分類されている", "□", "交通費、備品、報酬など"],
        [4, "決算情報", "収入の内訳が具体的に記載されている", "□", "会費、助成金、参加費など"],
        [5, "決算情報", "大まかすぎない予算管理がされている", "□", "目的や内訳がある（≠どんぶり勘定）"]
    ]

    df = pd.DataFrame(data, columns=["No", "カテゴリ", "チェック項目", "確認欄", "備考例"])
    # Excel書き出し（テンプレート）
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="登録基準確認用紙", index=False)

        # メタ情報のシートを追加
        meta = pd.DataFrame({
            "項目": ["バージョン", "作成日", "適用基準年度", "備考"],
            "値": [VERSION, DATE_STR, "令和6年度", "全国協議会基準2025準拠"] # 適用基準年度・備考は適宜変更
        })
        meta.to_excel(writer, sheet_name="meta", index=False)
    logging.info(f"✅ チェックテンプレート6（決算書）（{VERSION}）を出力しました → {path}")

def generate_check_template_paper7(path=f"templates/check_paper7_self_evaluation_template_{VERSION}.xlsx"):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    data = [
        [1, "プロフィール", "プロフィールシートが記入されている", "□", "所属、役職、日付などが記載されているか"],
        [2, "評価", "自己評価（0〜4）の記入漏れがない", "□", "全項目にスコア（0〜4）が入力されているか"]
    ]

    df = pd.DataFrame(data, columns=["No", "カテゴリ", "チェック項目", "確認欄", "備考例"])
    # Excel書き出し（テンプレート）
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="登録基準確認用紙", index=False)

        # メタ情報のシートを追加
        meta = pd.DataFrame({
            "項目": ["バージョン", "作成日", "適用基準年度", "備考"],
            "値": [VERSION, DATE_STR, "令和6年度", "全国協議会基準2025準拠"] # 適用基準年度・備考は適宜変更
        })
        meta.to_excel(writer, sheet_name="meta", index=False)
    logging.info(f"✅ チェックテンプレート7（{VERSION}）を出力しました → {path}")

def generate_check_template_paper8(path=f"templates/check_paper8_minutes_template_{VERSION}.xlsx"):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    data = [
        [1, "基本情報", "開催日時が明記されている", "□", "例：2024年5月1日 14:00〜"],
        [2, "基本情報", "開催場所が明記されている", "□", "例：○○市民センター会議室"],
        [3, "出席者", "出席者の氏名が記載されている", "□", "理事・監事など"],
        [4, "出席者", "委任状や書面表決による出席が明記されている", "□", "該当があれば"],
        [5, "議長", "議長の氏名が記載されている", "□", "議事を進行した人物"],
        [6, "議事の記録", "議事の経過が簡潔に記載されている", "□", "要点が記録されている"],
        [7, "議事の記録", "決議の結果が明記されている", "□", "賛否・決議内容など"],
        [8, "事業計画の議決", "事業計画の承認が記載されている", "□", "承認・否決など"],
        [9, "予算の議決", "予算の承認が記載されている", "□", "承認・否決など"],
        [10, "事業報告の議決", "事業報告の承認が記載されている", "□", "承認・否決など"],
        [11, "決算の議決", "決算の承認が記載されている", "□", "承認・否決など"],
        [12, "その他", "その他の重要事項が記載されている", "□", "例：役員選任、定款変更など"],
        [13, "署名", "議事録作成日が記載されている", "□", ""],
        [14, "署名", "議事録作成者の氏名が記載されている", "□", ""],
        [15, "署名", "押印がされている", "□", "署名人・議長の押印など"],
        [16, "その他", "定款・法令に基づく必要事項が記載されている", "□", "例：承認機関、定足数など"]
    ]

    df = pd.DataFrame(data, columns=["No", "カテゴリ", "チェック項目", "確認欄", "備考"])
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="登録基準確認用紙", index=False)

        # メタ情報のシートを追加
        meta = pd.DataFrame({
            "項目": ["バージョン", "作成日", "適用基準年度", "備考"],
            "値": [VERSION, DATE_STR, "令和6年度", "全国協議会基準2025準拠"] # 適用基準年度・備考は適宜変更
        })
        meta.to_excel(writer, sheet_name="meta", index=False)
    logging.info(f"✅ チェックテンプレート8（{VERSION}）を出力しました → {path}")

def generate_check_template_paper9(path=f"templates/check_paper9_self_disclosure_template_{VERSION}.xlsx"):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    data = [
        [1, "提出有無", "自己説明・公表の書類が提出されている", "□", "PDF・HP掲載のスクリーンショットなどでも可"]
    ]

    df = pd.DataFrame(data, columns=["No", "カテゴリ", "チェック項目", "確認欄", "備考"])
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="登録基準確認用紙", index=False)

        # メタ情報のシートを追加
        meta = pd.DataFrame({
            "項目": ["バージョン", "作成日", "適用基準年度", "備考"],
            "値": [VERSION, DATE_STR, "令和6年度", "全国協議会基準2025準拠"] # 適用基準年度・備考は適宜変更
        })
        meta.to_excel(writer, sheet_name="meta", index=False)
    logging.info(f"✅ チェックテンプレート8（{VERSION}）を出力しました → {path}")

if __name__ == "__main__":
    generate_check_template_paper_1()
    generate_check_template_paper2_1()
    generate_check_template_paper2_2()
    generate_check_template_paper3()
    generate_check_template_paper4()
    generate_check_template_paper5_1_business_plan()
    generate_check_template_paper5_2_budget()
    generate_check_template_paper6_1_business_report()
    generate_check_template_paper6_2_financial_statements()
    generate_check_template_paper7()
    generate_check_template_paper8()
    generate_check_template_paper9()
    # 追加のテンプレート生成関数をここに呼び出す
    print("📋 テンプレートを生成しました。")