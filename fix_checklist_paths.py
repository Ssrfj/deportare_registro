import os
import re

def fix_checklist_file_paths():
    """
    チェックリスト生成ファイルのパス参照を修正する
    """
    documents_dir = "src/checklist/generators/documents"
    
    # 修正対象のファイル名パターン
    file_pattern = re.compile(r'make_document\d+.*_checklist\.py$')
    
    for file in os.listdir(documents_dir):
        if file_pattern.match(file):
            file_path = os.path.join(documents_dir, file)
            print(f"修正中: {file_path}")
            
            # ファイルを読み込み
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # パターン1: 相対パス設定の修正
            old_pattern1 = re.compile(r"(\w+)_checklist_columns_file_name = 'config/checklist_columns/(\w+)_checklist_columns\.json'\s*\n\s*(\w+)_checklist_columns_file_path = os\.path\.join\(os\.path\.dirname\(os\.path\.abspath\(__file__\)\), \w+_checklist_columns_file_name\)")
            
            def replacement1(match):
                var_name = match.group(1)
                json_name = match.group(2)
                path_var = match.group(3)
                return f"from src.core.utils import get_config_file_path\n    {path_var}_checklist_columns_file_path = get_config_file_path('config/checklist_columns/{json_name}_checklist_columns.json')"
            
            content = old_pattern1.sub(replacement1, content)
            
            # パターン2: ログメッセージの修正
            old_pattern2 = re.compile(r"logging\.info\(f\".*のチェックリストのカラム名を読み込みました: \{(\w+)_checklist_columns_file_name\}\"\)")
            
            def replacement2(match):
                var_name = match.group(1)
                return f"logging.info(f\"チェックリストのカラム名を読み込みました: {{{var_name}_checklist_columns_file_path}}\")"
            
            content = old_pattern2.sub(replacement2, content)
            
            # ファイルに書き戻し
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"修正完了: {file_path}")

if __name__ == "__main__":
    fix_checklist_file_paths()
    print("すべてのチェックリストファイルのパス修正が完了しました")
