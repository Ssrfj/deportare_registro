import pandas as pd

def read_defects_from_checklist(path):
    df = pd.read_excel(path)
    defects = []

    for _, row in df.iterrows():
        if str(row.get("確認欄", "")).strip() == "":
            defects.append({
                "No": row.get("No"),
                "カテゴリ": row.get("カテゴリ"),
                "チェック項目": row.get("チェック項目")
            })

    return defects
