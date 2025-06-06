# 作業中に必要なときに使用しているもの
# 基本的に、使用後に削除しているため、空の状態
import os
import pandas as pd

def generate_check_template_paper4(path="templates/check_paper4_voting_rights_holders_list_template.xlsx"):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    data = [
        [1, "役員情報", "氏名が明記されている", "□", "全役員に記載があるか"],
        [2, "役員情報", "居住区市町村が明記されている", "□", "例：○○市、△△町など"]
    ]

    df = pd.DataFrame(data, columns=["No", "カテゴリ", "チェック項目", "確認欄", "備考例"])
    df.to_excel(path, index=False)
    print(f"✅ 書類④用テンプレートを出力しました → {path}")
