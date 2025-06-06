import pdfplumber
import re

def clean_line_repeats(line):
    # 行の中で、「文字＋同じ文字」が連続するものを1つに（数字や記号を残すための緩和）
    return re.sub(r'([\u4e00-\u9fff])\1+', r'\1', line)  # 漢字のみ対象

pdf_path = "_申請書類①_東京都.pdf"
txt_output_path = "申請書類①_東京都_cleaned.txt"

all_text = []

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        raw_text = page.extract_text()
        if raw_text:
            lines = raw_text.splitlines()
            cleaned_lines = [clean_line_repeats(line) for line in lines]
            page_text = "\n".join(cleaned_lines)
            all_text.append(f"--- Page {i+1} ---\n{page_text}")

with open(txt_output_path, "w", encoding="utf-8") as f:
    f.write("\n\n".join(all_text))

print(f"整形済みテキストを保存しました: {txt_output_path}")
