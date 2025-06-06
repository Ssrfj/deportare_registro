import pdfplumber
import pandas as pd
import csv

# PDFファイルのパス
pdf_path = "_申請書類①_東京都.pdf"
csv_output_path = "申請書類①_東京都.csv"

# 全ページの表をまとめるリスト
all_tables = []

# PDFを開いて表を抽出
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for table_num, table in enumerate(tables):
            if table:  # 空でない場合
                df = pd.DataFrame(table)
                df["ページ"] = i + 1
                df["表番号"] = table_num + 1
                all_tables.append(df)

# すべての表を1つのDataFrameに統合
if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_csv(csv_output_path, index=False, encoding="utf-8-sig")
    print(f"✅ CSVに出力完了: {csv_output_path}")
else:
    print("⚠️ 表が検出されませんでした。")
